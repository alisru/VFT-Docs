#!/usr/bin/env python3
"""
search_oa.py  --  Fast OpenAustralia Hansard phrase-search for kanon-audit validation.

Given a distinctive phrase from a training-data hypothesis, returns the top N
Hansard speeches containing it, with date, speaker, snippet, gid permalink,
and optionally the full verbatim paragraph.

This is the missing link between hypothesis generation and quote verification:
  hypothesis → search_oa.py <phrase> --person "Albanese" → gid + snippet
             → confirm verbatim on permalink                → write node

Typical audit workflow
----------------------
  1. Model generates hypothesis: "Albanese said X around 2019 re: climate"
  2. Extract the most distinctive 4-6 word phrase from that hypothesis
  3. Run:  python search_oa.py "phrase words here" --person "Albanese" --fetch-full
  4. Top hits print: date, snippet (phrase in context), permalink URL, full paragraph
  5. Pick the best hit, copy the verbatim sentence, cite the permalink.

That's 1 tool call (run this script) + confirmation reading, vs the current
WebSearch → fetch → browser-fallback chain of 3-20 calls.

Usage
-----
  python search_oa.py "climate change future generations"
  python search_oa.py "climate change future generations" --person "Albanese"
  python search_oa.py "climate change future generations" --person-id 10514
  python search_oa.py "climate change future" --person "Albanese" --fetch-full --top 3
  python search_oa.py "WorkChoices" --person "Albanese" --from 2007-01-01 --to 2009-12-31
  python search_oa.py "native title" --person "Hanson" --person-id 10280

Flags
-----
  phrase          The distinctive phrase to search (wrap in quotes if multi-word)
  --person NAME   Look up person_id by name before searching (searches both
                  Representatives and Senators; picks first match by default)
  --person-id N   Use a known numeric OpenAustralia person_id directly
                  (skips name-lookup API call; Albanese=10514, Hanson=10280)
  --top N         Return top N hits (default: 5)
  --fetch-full    After search, fetch the full speech paragraph from the
                  Hansard permalink page. Adds one HTTP request per hit but
                  gives you the verbatim sentence in context.
  --from DATE     Only hits on or after YYYY-MM-DD
  --to DATE       Only hits on or before YYYY-MM-DD
  --exact         Wrap phrase in double-quotes in the API query (exact phrase match)
  --out FILE      Also write results as JSONL to FILE (default: print only)
  --quiet         Suppress progress output; only print results

Requires: requests, beautifulsoup4
  pip install --break-system-packages requests beautifulsoup4

Note: reuses the same OpenAustralia API key as hansard_scraper.py.
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request

import requests
from bs4 import BeautifulSoup

API_KEY = "F9TbUzGNMr3rDTBxkvG47QHG"
BASE = "https://www.openaustralia.org.au/api"


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def api_get(function, log=None, **params):
    params = {k: v for k, v in params.items() if v is not None}
    params["key"] = API_KEY
    params["output"] = "js"
    url = f"{BASE}/{function}?{urllib.parse.urlencode(params)}"
    if log:
        log(f"  → GET {url}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = resp.read().decode("utf-8")
                if not data.strip():
                    return None
                return json.loads(data)
        except Exception as e:
            if attempt == 2:
                print(f"  [warn] request failed after 3 tries: {e}", file=sys.stderr)
                return None
            time.sleep(1.5)


def find_person_id(name, log=None):
    """Search Representatives + Senators for name, return list of (person_id, full_name, house)."""
    candidates = []
    for endpoint, house_label in [("getRepresentatives", "House"), ("getSenators", "Senate")]:
        results = api_get(endpoint, log=log, search=name) or []
        for r in results:
            pid = r.get("person_id")
            full_name = r.get("full_name") or r.get("name") or name
            if pid:
                candidates.append((pid, full_name, house_label))
    return candidates


# ---------------------------------------------------------------------------
# Permalink construction
# ---------------------------------------------------------------------------

def gid_to_permalink(gid, chamber_hint=None):
    """
    gid format: YYYY-MM-DD.N.M
    Senate speeches live at /senate/?id=<gid>
    House speeches live at /debates/?id=<gid>
    We can't always tell from the gid alone which it is, so we return both
    and let --fetch-full try both.
    """
    if not gid:
        return None, None
    base = "https://www.openaustralia.org.au"
    if chamber_hint and "senate" in chamber_hint.lower():
        return f"{base}/senate/?id={gid}", f"{base}/debates/?id={gid}"
    # Default: try debates (House) first, senate as fallback
    return f"{base}/debates/?id={gid}", f"{base}/senate/?id={gid}"


# ---------------------------------------------------------------------------
# Full-text extraction (same logic as hansard_scraper.py)
# ---------------------------------------------------------------------------

_PAGE_CACHE = {}


def _fetch_soup(url, log=None):
    if url in _PAGE_CACHE:
        return _PAGE_CACHE[url]
    soup = None
    try:
        resp = requests.get(url, timeout=30, headers={"User-Agent": "kanon-audit-search/1.0"})
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
        time.sleep(0.25)
    except Exception as e:
        if log:
            log(f"  [warn] fetch failed {url}: {e}")
    _PAGE_CACHE[url] = soup
    return soup


def fetch_speech_paragraph(gid, log=None):
    """
    Fetch the verbatim speech paragraph(s) for this gid.
    Tries House URL first, then Senate URL as fallback.
    Returns (text, source_url) or (None, None).
    """
    if not gid:
        return None, None

    m = re.match(r"^\d{4}-\d{2}-\d{2}\.(.+)$", gid)
    if not m:
        return None, None
    anchor_name = "g" + m.group(1)

    primary_url, fallback_url = gid_to_permalink(gid)
    for url in filter(None, [primary_url, fallback_url]):
        soup = _fetch_soup(url, log=log)
        if soup is None:
            continue
        anchor = soup.find("a", attrs={"name": anchor_name})
        if anchor is None:
            continue

        # Walk forward from anchor collecting <p> tags until the next speech
        paragraphs = []
        node = anchor
        seen_speaker = False
        while True:
            node = node.find_next(["p", "a"])
            if node is None:
                break
            if node.name == "a":
                name_attr = node.get("name", "")
                if name_attr.startswith("g") and name_attr != anchor_name:
                    break
                continue
            classes = node.get("class") or []
            if "speaker" in classes:
                if seen_speaker:
                    break
                seen_speaker = True
                continue
            text = node.get_text(" ", strip=True)
            if not text or text.lower().startswith("view the") or "hansard source" in text.lower():
                continue
            paragraphs.append(text)

        if paragraphs:
            return "\n\n".join(paragraphs), url

    return None, None


# ---------------------------------------------------------------------------
# Core search
# ---------------------------------------------------------------------------

def search_hansard(phrase, person_id=None, top=5, date_from=None, date_to=None,
                   exact=False, fetch_full=False, log=None):
    """
    Call getHansard with the phrase (and optional person filter).
    Returns a list of result dicts.
    """
    query = f'"{phrase}"' if exact else phrase

    # NOTE: combining num + person on getHansard returns HTTP 500 (same quirk
    # as getDebates — documented in hansard_scraper.py). Drop num when filtering
    # by person; the API returns a default page (~10-20 results) which is enough.
    params = {"search": query}
    if person_id:
        params["person"] = person_id
    else:
        params["num"] = min(top, 20)

    raw = api_get("getHansard", log=log, **params)
    if not raw:
        return []

    # The API returns a dict with a "rows" key, or sometimes just a list
    rows = raw.get("rows") if isinstance(raw, dict) else raw
    if not rows:
        return []

    results = []
    for row in rows[:top]:
        hdate = row.get("hdate") or row.get("date", "")
        if date_from and hdate and hdate < date_from:
            continue
        if date_to and hdate and hdate > date_to:
            continue

        gid = row.get("gid", "")
        snippet = row.get("body", "").strip()

        # Determine house from the gid or listurl
        listurl = row.get("listurl", "")
        if "senate" in listurl.lower():
            chamber = "Senate"
        elif "debates" in listurl.lower() or "representatives" in listurl.lower():
            chamber = "House of Representatives"
        else:
            chamber = "unknown"

        # Build the clean permalink from listurl (strip any extra params)
        if listurl:
            permalink = "https://www.openaustralia.org.au" + listurl.split("&amp;")[0].split("&")[0]
        else:
            primary, _ = gid_to_permalink(gid, chamber_hint=chamber)
            permalink = primary or ""

        speaker_name = row.get("speaker", {}).get("name", "") if isinstance(row.get("speaker"), dict) else ""

        result = {
            "date": hdate,
            "speaker": speaker_name,
            "chamber": chamber,
            "gid": gid,
            "permalink": permalink,
            "snippet": snippet,
            "full_text": None,
            "full_text_url": None,
        }

        if fetch_full and gid:
            if log:
                log(f"  Fetching full text for {gid} ({hdate})...")
            full_text, source_url = fetch_speech_paragraph(gid, log=log)
            result["full_text"] = full_text
            result["full_text_url"] = source_url

        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_results(results, phrase, quiet=False):
    if not results:
        print(f'\n[No results found for: "{phrase}"]\n')
        return

    print(f'\n{"="*70}')
    print(f'Results for: "{phrase}"  ({len(results)} hit{"s" if len(results) != 1 else ""})')
    print(f'{"="*70}\n')

    for i, r in enumerate(results, 1):
        print(f'--- Hit {i} ---')
        print(f'Date:      {r["date"]}')
        if r["speaker"]:
            print(f'Speaker:   {r["speaker"]}')
        print(f'Chamber:   {r["chamber"]}')
        print(f'GID:       {r["gid"]}')
        print(f'Permalink: {r["permalink"]}')
        print()
        if r["snippet"]:
            print(f'Snippet (API, ~400 chars):')
            print(f'  {r["snippet"]}')
            print()
        if r["full_text"]:
            print(f'Full speech paragraph (fetched from {r["full_text_url"]}):')
            # Indent each paragraph
            for para in r["full_text"].split("\n\n"):
                print(f'  {para}')
            print()
        elif r["full_text"] is None and not r["snippet"]:
            print('  [no text available]')
        print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Fast OpenAustralia Hansard phrase-search for kanon-audit quote validation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("phrase", help="Distinctive phrase to search for (4-8 words ideal)")
    ap.add_argument("--person", default=None,
                    help="Look up person_id by name before searching (e.g. 'Albanese', 'Hanson')")
    ap.add_argument("--person-id", dest="person_id", default=None, type=int,
                    help="Use a known numeric person_id directly (Albanese=10514, Hanson=10280). "
                         "Skips the name-lookup API call.")
    ap.add_argument("--top", default=5, type=int,
                    help="Number of top hits to return (default: 5, max: 20)")
    ap.add_argument("--fetch-full", dest="fetch_full", action="store_true",
                    help="Fetch the full verbatim speech paragraph from each hit's permalink")
    ap.add_argument("--from", dest="date_from", default=None, help="Only hits on/after YYYY-MM-DD")
    ap.add_argument("--to", dest="date_to", default=None, help="Only hits on/before YYYY-MM-DD")
    ap.add_argument("--exact", action="store_true",
                    help="Wrap phrase in double-quotes for exact phrase match in the API")
    ap.add_argument("--out", default=None, help="Also write results as JSONL to this file")
    ap.add_argument("--quiet", action="store_true", help="Suppress progress/debug output")
    args = ap.parse_args()

    log = None if args.quiet else (lambda msg: print(msg, file=sys.stderr))

    # Resolve person_id
    person_id = args.person_id
    if not person_id and args.person:
        if log:
            log(f"Looking up person_id for: {args.person}")
        candidates = find_person_id(args.person, log=log)
        if not candidates:
            print(f"[warn] No person found matching '{args.person}' -- searching without person filter.",
                  file=sys.stderr)
        else:
            person_id, full_name, house = candidates[0]
            if log:
                log(f"  → Using person_id={person_id} ({full_name}, {house})")
            if len(candidates) > 1:
                if log:
                    log(f"  [note] Multiple matches: {[(c[0], c[1]) for c in candidates]}. "
                        f"Using first. Pass --person-id to be explicit.")

    if log:
        id_label = f"person_id={person_id}" if person_id else "all speakers"
        log(f'Searching getHansard: "{args.phrase}" ({id_label})')

    results = search_hansard(
        phrase=args.phrase,
        person_id=person_id,
        top=args.top,
        date_from=args.date_from,
        date_to=args.date_to,
        exact=args.exact,
        fetch_full=args.fetch_full,
        log=log,
    )

    print_results(results, args.phrase, quiet=args.quiet)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"[wrote {len(results)} results to {args.out}]", file=sys.stderr)

    sys.exit(0 if results else 1)


if __name__ == "__main__":
    main()
