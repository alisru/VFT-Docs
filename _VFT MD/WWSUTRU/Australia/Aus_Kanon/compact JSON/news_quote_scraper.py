#!/usr/bin/env python3
"""
News Quote Scraper (for /kanon-audit sourcing)

Finds news articles mentioning an actor, fetches each ONCE to extract
quotes attributed to that actor plus immediate surrounding context, and
discards the full article body immediately after extraction. Nothing but
the extracted quote + short context + source metadata is written to disk.

This is a deliberate design choice, not a limitation: a news article from
an outlet like the Guardian, News.com.au, ABC, etc. is copyrighted
journalism with no license for bulk redistribution, so this tool only
persists short, attributed excerpts (the quotes themselves) with a link
back to the original source for verification -- exactly what an audit
needs, without warehousing full copyrighted articles.

TWO discovery sources are supported:

  --source bigquery (default if google-cloud-bigquery is installed and
      credentials are available)
      Queries GDELT's public BigQuery dataset (gdelt-bq.gdeltv2.gkg_partitioned)
      for articles whose extracted V2Persons field mentions the actor.
      Deeper historical coverage, real date-range filtering, uses your
      GCP account's free 1TB/month BigQuery query allowance.
      Setup (one-time):
        pip install --break-system-packages google-cloud-bigquery
        gcloud auth application-default login
        gcloud config set project YOUR_PROJECT_ID
      (Or set GOOGLE_APPLICATION_CREDENTIALS to a service account key.)

  --source docapi
      Falls back to GDELT's free, keyless DOC 2.0 API. No setup, no GCP
      account needed, but shallower coverage and a 250-articles-per-query
      cap. Rate-limited to ~1 request per 5 seconds by GDELT.

This tool is INCREMENTAL: if the output file already exists, it loads the
article URLs already processed and skips them on the next run, appending
only newly-found quotes instead of starting over.

Usage:
    python3 news_quote_scraper.py "Anthony Albanese"
    python3 news_quote_scraper.py "Anthony Albanese" --source docapi
    python3 news_quote_scraper.py "Anthony Albanese" --from 2024-01-01 --to 2024-12-31
    python3 news_quote_scraper.py "Anthony Albanese" --full-rescan

Requires: trafilatura, requests, beautifulsoup4
    pip install --break-system-packages trafilatura requests beautifulsoup4
Optional (for --source bigquery): google-cloud-bigquery
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse

import requests
import trafilatura

GDELT_DOC_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
GDELT_RATE_LIMIT_SECONDS = 5.5  # free/no-key DOC API tier limit

ATTRIBUTION_VERBS = [
    "said", "says", "told", "tells", "stated", "state", "added", "argued",
    "claimed", "claims", "insisted", "declared", "announced", "wrote",
    "explained", "noted", "remarked", "warned", "urged", "responded",
    "replied", "asked", "confirmed", "described",
]

QUOTE_RE = re.compile(r'[“"]([^”"]{15,600})[”"]')

_last_docapi_call = 0.0


# ---------------------------------------------------------------------------
# Discovery: DOC API (free, keyless)
# ---------------------------------------------------------------------------

def gdelt_docapi_search(actor_name, date_from=None, date_to=None, max_records=75):
    global _last_docapi_call
    query = f'"{actor_name}"'
    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": min(max_records, 250),
        "format": "json",
        "sort": "datedesc",
    }
    if date_from:
        params["startdatetime"] = date_from.replace("-", "") + "000000"
    if date_to:
        params["enddatetime"] = date_to.replace("-", "") + "235959"

    wait = GDELT_RATE_LIMIT_SECONDS - (time.time() - _last_docapi_call)
    if wait > 0:
        time.sleep(wait)

    url = f"{GDELT_DOC_ENDPOINT}?{urllib.parse.urlencode(params)}"
    try:
        resp = requests.get(url, timeout=30, headers={"User-Agent": "kanon-audit-research-tool/1.0"})
        _last_docapi_call = time.time()
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        return [
            {"url": a.get("url"), "title": a.get("title"), "date": a.get("seendate", "")[:8], "domain": a.get("domain")}
            for a in articles
        ]
    except Exception as e:
        print(f"  [warn] GDELT DOC API search failed: {e}", file=sys.stderr)
        return []


# ---------------------------------------------------------------------------
# Discovery: BigQuery GDELT GKG dataset
# ---------------------------------------------------------------------------

def gdelt_bigquery_search(actor_name, date_from=None, date_to=None, max_records=500):
    """Query gdelt-bq.gdeltv2.gkg_partitioned for articles mentioning the
    actor in the extracted V2Persons field. Requires google-cloud-bigquery
    and valid GCP credentials (see module docstring for one-time setup)."""
    try:
        from google.cloud import bigquery
    except ImportError:
        print("  [error] google-cloud-bigquery not installed. Run:", file=sys.stderr)
        print("    pip install --break-system-packages google-cloud-bigquery", file=sys.stderr)
        return None

    # ADC from `gcloud auth application-default login` doesn't always carry
    # a project id -- resolve explicitly so we don't depend on that quirk.
    # Priority: GOOGLE_CLOUD_PROJECT env var, then GCP_PROJECT_ID env var,
    # then hardcoded fallback below (set to your project from `gcloud init`).
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT_ID") or "alethekanon"

    try:
        client = bigquery.Client(project=project_id)
    except Exception as e:
        print(f"  [error] Couldn't create BigQuery client for project '{project_id}' (check GCP auth): {e}", file=sys.stderr)
        return None

    # Default lookback if no range given, to keep bytes-scanned sane on the free tier.
    date_from_sql = (date_from or "2015-01-01").replace("-", "")
    date_to_sql = (date_to or "2030-12-31").replace("-", "")

    query = """
        SELECT
          DATE AS gkg_date,
          DocumentIdentifier AS url,
          SourceCommonName AS domain
        FROM `gdelt-bq.gdeltv2.gkg_partitioned`
        WHERE _PARTITIONTIME BETWEEN TIMESTAMP(@date_from) AND TIMESTAMP(@date_to)
          AND V2Persons LIKE @name_pattern
        ORDER BY DATE DESC
        LIMIT @max_records
    """
    # Convert YYYYMMDD -> YYYY-MM-DD for TIMESTAMP()
    df_iso = f"{date_from_sql[0:4]}-{date_from_sql[4:6]}-{date_from_sql[6:8]}"
    dt_iso = f"{date_to_sql[0:4]}-{date_to_sql[4:6]}-{date_to_sql[6:8]}"

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("date_from", "STRING", df_iso),
            bigquery.ScalarQueryParameter("date_to", "STRING", dt_iso),
            bigquery.ScalarQueryParameter("name_pattern", "STRING", f"%{actor_name}%"),
            bigquery.ScalarQueryParameter("max_records", "INT64", max_records),
        ]
    )

    try:
        print(f"  Running BigQuery search ({df_iso} to {dt_iso})... this uses your free query quota.", file=sys.stderr)
        results = client.query(query, job_config=job_config).result()
    except Exception as e:
        print(f"  [error] BigQuery query failed: {e}", file=sys.stderr)
        return None

    articles = []
    for row in results:
        gkg_date = str(row.gkg_date)[:8] if row.gkg_date else ""
        articles.append({
            "url": row.url,
            "title": None,  # GKG doesn't carry a clean headline field; pulled from the page itself later
            "date": gkg_date,
            "domain": row.domain,
        })
    return articles


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def extract_quotes_for_actor(article_text, actor_name):
    if not article_text:
        return []
    last_name = actor_name.strip().split()[-1]
    results = []
    for match in QUOTE_RE.finditer(article_text):
        quote = match.group(1).strip()
        start, end = match.span()
        window_start = max(0, start - 200)
        window_end = min(len(article_text), end + 200)
        context = article_text[window_start:window_end].strip()
        name_nearby = actor_name.lower() in context.lower() or last_name.lower() in context.lower()
        verb_nearby = any(v in context.lower() for v in ATTRIBUTION_VERBS)
        if name_nearby and verb_nearby:
            results.append((quote, context))
    return results


def compute_article_fingerprint(headline, article_text):
    """Returns a dedupe key for an article, preferring the headline over
    the body: syndicated copies of the same wire story (e.g. AAP copy
    republished on a dozen local mastheads) almost always keep the exact
    same headline verbatim, even when a local sub-editor rewrites the
    intro paragraph or injects different boilerplate/ads before the body
    -- which is why a body-only hash can miss real duplicates. Falls back
    to a body-text hash only when no usable headline exists."""
    import hashlib
    if headline:
        norm_title = re.sub(r"[^a-z0-9]", "", headline.lower())
        if len(norm_title) >= 8:  # skip near-empty/too-generic headlines
            return "title:" + hashlib.sha1(norm_title.encode("utf-8")).hexdigest()
    norm_body = re.sub(r"[^a-z0-9]", "", (article_text or "").lower())[:500]
    return "body:" + hashlib.sha1(norm_body.encode("utf-8")).hexdigest()


def scrape_article(article_meta, actor_name, seen_fingerprints=None):
    """Returns (records, fingerprint, is_duplicate).
    seen_fingerprints, if given, is a set of fingerprints already kept from
    prior articles/runs -- if this article's headline (or body, as
    fallback) matches one already seen, no quotes are extracted/written
    for it (duplicate syndicated story), but the fingerprint is still
    returned so the caller can decide whether to add it."""
    url = article_meta.get("url")
    if not url:
        return [], None, False
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return [], None, False
    full_text = trafilatura.extract(downloaded)
    metadata = trafilatura.extract_metadata(downloaded)
    if not full_text:
        return [], None, False

    headline = article_meta.get("title") or (metadata.title if metadata else None)
    fingerprint = compute_article_fingerprint(headline, full_text)
    if seen_fingerprints is not None and fingerprint in seen_fingerprints:
        return [], fingerprint, True

    quotes = extract_quotes_for_actor(full_text, actor_name)

    records = []
    for quote_text, context in quotes:
        records.append({
            "speaker_name": actor_name,
            "source_type": "news",
            "outlet": article_meta.get("domain"),
            "date": article_meta.get("date"),
            "headline": headline,
            "quote": quote_text,
            "context": context,
            "source_url": url,
            "article_fingerprint": fingerprint,
        })
    return records, fingerprint, False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Scrape news quotes attributed to an actor.")
    ap.add_argument("name", help="Full name of the actor, e.g. 'Anthony Albanese'")
    ap.add_argument("--out", default=None, help="Output JSONL path (default: <slug>_news.jsonl)")
    ap.add_argument("--from", dest="date_from", default=None, help="Earliest date YYYY-MM-DD")
    ap.add_argument("--to", dest="date_to", default=None, help="Latest date YYYY-MM-DD")
    ap.add_argument("--max-articles", type=int, default=200, help="Max candidate articles to check")
    ap.add_argument("--source", choices=["bigquery", "docapi"], default="bigquery",
                     help="Discovery backend: bigquery (deeper, needs GCP auth) or docapi (free, keyless)")
    ap.add_argument("--full-rescan", action="store_true",
                     help="Ignore existing output file and re-check every article from scratch")
    args = ap.parse_args()

    out_path = args.out or (args.name.lower().replace(" ", "_") + "_news.jsonl")

    # Resume support: skip URLs we've already extracted quotes from, and
    # skip content we've already kept a copy of under a different URL
    # (syndicated wire stories republished across multiple outlets).
    seen_urls = set()
    seen_fingerprints = set()
    if not args.full_rescan and os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if rec.get("source_url"):
                        seen_urls.add(rec["source_url"])
                    if rec.get("article_fingerprint"):
                        seen_fingerprints.add(rec["article_fingerprint"])
                except json.JSONDecodeError:
                    continue
        if seen_urls:
            print(f"Resuming: {len(seen_urls)} article(s) already processed in {out_path}, skipping those.", file=sys.stderr)

    print(f"Searching ({args.source}) for articles mentioning '{args.name}'...", file=sys.stderr)
    if args.source == "bigquery":
        articles = gdelt_bigquery_search(args.name, args.date_from, args.date_to, args.max_articles)
        if articles is None:
            print("Falling back to the free DOC API instead.", file=sys.stderr)
            articles = gdelt_docapi_search(args.name, args.date_from, args.date_to, args.max_articles)
    else:
        articles = gdelt_docapi_search(args.name, args.date_from, args.date_to, args.max_articles)

    print(f"  Found {len(articles)} candidate articles.", file=sys.stderr)

    new_urls = [a for a in articles if a.get("url") and a["url"] not in seen_urls]
    print(f"  {len(articles) - len(new_urls)} already processed, {len(new_urls)} new to check.", file=sys.stderr)

    file_mode = "w" if args.full_rescan or not seen_urls else "a"
    total_quotes = 0
    total_duplicates_skipped = 0
    with open(out_path, file_mode, encoding="utf-8") as f:
        for i, art in enumerate(new_urls, 1):
            print(f"  [{i}/{len(new_urls)}] {art.get('domain')}: {art.get('url')}", file=sys.stderr)
            try:
                records, fingerprint, is_dup = scrape_article(art, args.name, seen_fingerprints=seen_fingerprints)
            except Exception as e:
                print(f"    [warn] failed to process {art.get('url')}: {e}", file=sys.stderr)
                records, fingerprint, is_dup = [], None, False
            if is_dup:
                total_duplicates_skipped += 1
                print(f"    [skip] duplicate/syndicated content of an already-kept article", file=sys.stderr)
            elif fingerprint:
                seen_fingerprints.add(fingerprint)
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                total_quotes += 1
            time.sleep(0.5)  # be polite to news servers we're fetching directly

    print(f"\nDone. Extracted {total_quotes} new attributed quotes from {len(new_urls)} articles -> {out_path}", file=sys.stderr)
    print(f"Skipped {total_duplicates_skipped} duplicate/syndicated article(s) (same content, different outlet/URL).", file=sys.stderr)
    print("Note: only quotes + short context + source links were saved, not full article bodies.", file=sys.stderr)


if __name__ == "__main__":
    main()
