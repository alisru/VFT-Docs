#!/usr/bin/env python3
"""
Hansard speech scraper via the OpenAustralia API.

Pulls every recorded speech by a named federal MP or Senator (House +
Senate Hansard) and writes it out as structured JSONL, one speech per
line, ready to feed into audit/analysis tooling.

Usage:
    python3 hansard_scraper.py "Anthony Albanese"
    python3 hansard_scraper.py "Anthony Albanese" --out albanese.jsonl
    python3 hansard_scraper.py "Anthony Albanese" --from 2020-01-01 --to 2024-12-31

Notes on the API (learned by testing, not documented anywhere):
  - `num` and `order` params return HTTP 500 when combined with `person`.
    Only `page` works reliably. Page size is fixed at 20 results/page.
  - person lookups need the numeric `person_id` (not `member_id`), found
    via getRepresentatives / getSenators search-by-name.
  - A person can appear in both House and Senate Hansard (rare, but
    possible for people who changed chambers), so both are queried.
  - IMPORTANT: getDebates' "body" field is only a ~400-character search
    snippet, NOT the full speech. To get the complete speech text this
    script fetches the actual Hansard debate page for each gid and pulls
    the full paragraph(s) between that speech's anchor tag and the next
    one. Pages are cached per-URL since one debate page holds many
    speeches, so this doesn't multiply requests per speech.
  - Resume is dedup-by-gid: once a gid is written to the output file AT
    ALL (even as a snippet, e.g. from a --no-full-text pass), a later run
    skips it -- it will NOT be re-fetched to upgrade it to full text.
    Re-running with full text enabled does not backfill snippet-only
    records. Use --upgrade-full-text-only for that instead (see below).

Two-pass workflow for a large backlog:
    1) Fast catalog pass (snippets only):
         python3 hansard_scraper.py "Name" --no-full-text
    2) Backfill full text into the existing file, without re-searching:
         python3 hansard_scraper.py "Name" --upgrade-full-text-only

Requires: requests, beautifulsoup4
    pip install --break-system-packages requests beautifulsoup4
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import requests
from bs4 import BeautifulSoup

API_KEY = "F9TbUzGNMr3rDTBxkvG47QHG"
BASE = "https://www.openaustralia.org.au/api"

# Cache of base_url -> BeautifulSoup, so multiple speeches on the same
# debate page only trigger one HTTP fetch.
_PAGE_CACHE = {}


def _fetch_page_soup(base_url):
    if base_url in _PAGE_CACHE:
        return _PAGE_CACHE[base_url]
    soup = None
    try:
        resp = requests.get(base_url, timeout=30, headers={"User-Agent": "kanon-audit-research-tool/1.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        time.sleep(0.3)  # be polite, this is a fresh page fetch (not cached)
    except Exception as e:
        print(f"  [warn] failed to fetch Hansard page {base_url}: {e}", file=sys.stderr)
    _PAGE_CACHE[base_url] = soup
    if len(_PAGE_CACHE) % 25 == 0:
        # crude cache trim so long runs don't grow memory unbounded
        for k in list(_PAGE_CACHE.keys())[:-25]:
            del _PAGE_CACHE[k]
    return soup


def fetch_full_speech_text(hansard_url, gid):
    """Fetch the complete speech text for a given gid from its Hansard
    debate page. Returns None if it can't be found (caller should fall
    back to the API's snippet)."""
    if not hansard_url or not gid:
        return None
    # anchor name is everything after the date portion of the gid,
    # e.g. gid "2026-07-02.106.1" -> anchor "g106.1"
    m = re.match(r"^\d{4}-\d{2}-\d{2}\.(.+)$", gid)
    if not m:
        return None
    anchor_name = "g" + m.group(1)

    soup = _fetch_page_soup(hansard_url)
    if soup is None:
        return None

    anchor = soup.find("a", attrs={"name": anchor_name})
    if anchor is None:
        return None

    paragraphs = []
    node = anchor
    seen_speaker_header = False
    while True:
        node = node.find_next(["p", "a"])
        if node is None:
            break
        if node.name == "a":
            name_attr = node.get("name", "")
            if name_attr.startswith("g") and name_attr != anchor_name:
                break  # hit the next speech's anchor
            continue
        classes = node.get("class") or []
        if "speaker" in classes:
            if seen_speaker_header:
                break  # a second speaker header means we've moved on
            seen_speaker_header = True
            continue  # skip the "Name (electorate, party) | Hansard source" line itself
        text = node.get_text(" ", strip=True)
        if not text or text.lower().startswith("view the") or "hansard source" in text.lower():
            continue
        paragraphs.append(text)

    if not paragraphs:
        return None
    return "\n\n".join(paragraphs)


def api_get(function, **params):
    params = {k: v for k, v in params.items() if v is not None}
    params["key"] = API_KEY
    params["output"] = "js"
    url = f"{BASE}/{function}?{urllib.parse.urlencode(params)}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = resp.read().decode("utf-8")
                if not data.strip():
                    return None
                return json.loads(data)
        except Exception as e:
            if attempt == 2:
                print(f"  [warn] request failed after 3 tries: {e}\n  url={url}", file=sys.stderr)
                return None
            time.sleep(1.5)


def find_person(name):
    """Search both Representatives and Senators for a name match.
    Returns list of candidate dicts with person_id, full_name, house label."""
    candidates = []
    reps = api_get("getRepresentatives", search=name) or []
    for r in reps:
        candidates.append({
            "person_id": r.get("person_id"),
            "full_name": r.get("full_name") or r.get("name"),
            "house_label": "House of Representatives",
            "party": r.get("party"),
            "constituency": r.get("constituency"),
        })
    sens = api_get("getSenators", search=name) or []
    for s in sens:
        candidates.append({
            "person_id": s.get("person_id"),
            "full_name": s.get("full_name") or s.get("name"),
            "house_label": "Senate",
            "party": s.get("party"),
            "constituency": s.get("constituency"),
        })
    return candidates


def fetch_all_debates(person_id, chamber_type, date_from=None, date_to=None,
                       known_gids=None, stop_on_known_page=True):
    """Paginate getDebates for a person_id across one chamber ('representatives' or 'senate').
    Yields raw row dicts.

    If known_gids is provided (a set of gids already saved from a previous
    run) and stop_on_known_page is True, this stops paging as soon as it
    hits a page where every row is already known. The API returns newest
    speeches first by default, so once a whole page is "old news" there's
    nothing further to gain by continuing -- this is what makes repeat
    runs fast instead of re-walking all 8000+ results every time."""
    known_gids = known_gids or set()
    page = 1
    seen_total = None
    fetched = 0
    while True:
        result = api_get("getDebates", type=chamber_type, person=person_id, page=page)
        if not result or "rows" not in result:
            break
        info = result.get("info", {})
        if seen_total is None:
            seen_total = info.get("total_results", 0)
            print(f"  [{chamber_type}] total_results reported: {seen_total}", file=sys.stderr)
        rows = result["rows"]
        if not rows:
            break

        if stop_on_known_page and known_gids:
            page_gids = [r.get("gid") for r in rows]
            if page_gids and all(g in known_gids for g in page_gids):
                print(f"  [{chamber_type}] page {page} is entirely already-scraped, stopping here.", file=sys.stderr)
                break

        # Results come back newest-first by default. Once a whole page is
        # older than date_from, there's nothing further back that could
        # still be in range -- stop instead of silently walking through
        # the person's entire remaining history one page at a time.
        if date_from:
            page_dates = [r.get("hdate", "") for r in rows]
            if page_dates and all(d and d < date_from for d in page_dates):
                print(f"  [{chamber_type}] page {page} is entirely before --from {date_from}, stopping here.", file=sys.stderr)
                break

        for row in rows:
            hdate = row.get("hdate", "")
            if date_from and hdate < date_from:
                continue
            if date_to and hdate > date_to:
                continue
            yield row
        fetched += len(rows)
        if date_to and rows and rows[0].get("hdate", "") > date_to and page % 10 == 0:
            # heartbeat so a long walk through newer-than-range pages
            # (e.g. --to set well in the past) doesn't look frozen
            print(f"  [{chamber_type}] still paging toward --to {date_to}... (page {page}, currently at {rows[0].get('hdate')})", file=sys.stderr)
        page += 1
        time.sleep(0.3)  # be polite to a free non-commercial API
        # safety valve: if we've paged well past reported total, stop
        if seen_total and fetched >= seen_total:
            break
        if page > 2000:  # hard safety cap
            print("  [warn] hit hard page cap (2000 pages / ~40000 rows), stopping", file=sys.stderr)
            break


def normalise_row(row, person_full_name, chamber_type, fetch_full_text=True):
    gid = row.get("gid")
    hansard_url = (
        "https://www.openaustralia.org.au" + row["listurl"].split("&amp;")[0].split("&")[0]
        if row.get("listurl") else None
    )

    snippet = row.get("body")
    full_text = None
    is_full_text = False
    if fetch_full_text and hansard_url and gid:
        full_text = fetch_full_speech_text(hansard_url, gid)
        if full_text:
            is_full_text = True

    return {
        "speaker_name": person_full_name,
        "speaker_id": row.get("speaker_id"),
        "chamber": "House of Representatives" if chamber_type == "representatives" else "Senate",
        "date": row.get("hdate"),
        "gid": gid,
        "debate_title": (row.get("parent") or {}).get("body"),
        "text": full_text if is_full_text else snippet,
        "is_full_text": is_full_text,  # False means this fell back to the ~400-char API snippet
        "hansard_url": hansard_url,
    }


def upgrade_full_text_in_file(out_path, log_fn=None):
    """Re-read an existing output file and, for every record still marked
    is_full_text: false, fetch its full speech text and update that record
    in place. Does not search for or add any new speeches -- purely
    backfills snippet-only records already in the file. Rewrites the
    whole file at the end (records are held in memory; fine for
    JSONL files of this size, a few tens of thousands of records max)."""
    log_fn = log_fn or (lambda msg: print(msg, file=sys.stderr))

    if not os.path.exists(out_path):
        log_fn(f"No such file: {out_path}")
        return 0

    records = []
    with open(out_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    to_upgrade = [r for r in records if not r.get("is_full_text") and r.get("hansard_url") and r.get("gid")]
    log_fn(f"{len(records)} total records, {len(to_upgrade)} snippet-only records to upgrade.")

    upgraded = 0
    for i, rec in enumerate(to_upgrade, 1):
        full_text = fetch_full_speech_text(rec["hansard_url"], rec["gid"])
        if full_text:
            rec["text"] = full_text
            rec["is_full_text"] = True
            upgraded += 1
        log_fn(f"  [{i}/{len(to_upgrade)}] {rec.get('date')} - {'upgraded' if full_text else 'still snippet (page fetch failed)'}")

    with open(out_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    log_fn(f"Done. Upgraded {upgraded}/{len(to_upgrade)} snippet-only records to full text in {out_path}")
    return upgraded


def main():
    ap = argparse.ArgumentParser(description="Scrape all Hansard speeches by an actor via OpenAustralia API.")
    ap.add_argument("name", help="Full name of the MP/Senator, e.g. 'Anthony Albanese'")
    ap.add_argument("--out", default=None, help="Output JSONL path (default: <slug>_hansard.jsonl in cwd)")
    ap.add_argument("--from", dest="date_from", default=None, help="Earliest date YYYY-MM-DD (inclusive)")
    ap.add_argument("--to", dest="date_to", default=None, help="Latest date YYYY-MM-DD (inclusive)")
    ap.add_argument("--person-id", default=None, help="Skip name lookup, use this person_id directly")
    ap.add_argument("--full-rescan", action="store_true",
                     help="Ignore existing output file and re-fetch everything from scratch")
    ap.add_argument("--no-full-text", action="store_true",
                     help="Skip the per-speech full-text page fetch (fast, but 'text' will just be the "
                          "~400-char API snippet). Use this for a quick initial pass on a large backlog.")
    ap.add_argument("--upgrade-full-text-only", action="store_true",
                     help="Don't search for new speeches at all -- just backfill full text into existing "
                          "snippet-only records in --out (or the default output file for this name).")
    args = ap.parse_args()
    fetch_full_text = not args.no_full_text

    if args.upgrade_full_text_only:
        out_path = args.out or (args.name.lower().replace(" ", "_") + "_hansard.jsonl")
        upgrade_full_text_in_file(out_path)
        return

    if args.person_id:
        candidates = [{"person_id": args.person_id, "full_name": args.name,
                        "house_label": "unknown", "party": None, "constituency": None}]
    else:
        candidates = find_person(args.name)

    if not candidates:
        print(f"No match found for '{args.name}' in Representatives or Senators.", file=sys.stderr)
        sys.exit(1)

    if len(candidates) > 1 and not args.person_id:
        # Dedup by person_id (same person can show up once per house they've served in)
        by_id = {}
        for c in candidates:
            by_id.setdefault(c["person_id"], []).append(c["house_label"])
        print(f"Found {len(by_id)} distinct person_id match(es) for '{args.name}':", file=sys.stderr)
        for pid, houses in by_id.items():
            print(f"  person_id={pid}  houses={houses}", file=sys.stderr)

    out_path = args.out or (args.name.lower().replace(" ", "_") + "_hansard.jsonl")

    # Resume support: load gids already saved from a previous run so we
    # don't re-fetch or re-write them. --full-rescan skips this and starts clean.
    seen_gids = set()
    if not args.full_rescan and os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if rec.get("gid"):
                        seen_gids.add(rec["gid"])
                except json.JSONDecodeError:
                    continue
        if seen_gids:
            print(f"Resuming: found {len(seen_gids)} already-scraped speeches in {out_path}, will only fetch new ones.", file=sys.stderr)

    file_mode = "w" if args.full_rescan or not seen_gids else "a"
    total_written = 0
    with open(out_path, file_mode, encoding="utf-8") as f:
        # Query every distinct person_id found under both chamber types,
        # since a person_id can have speeches filed under either.
        distinct_ids = {c["person_id"]: c["full_name"] for c in candidates if c["person_id"]}
        for pid, full_name in distinct_ids.items():
            for chamber_type in ("representatives", "senate"):
                print(f"Fetching {chamber_type} speeches for person_id={pid} ({full_name})...", file=sys.stderr)
                for row in fetch_all_debates(pid, chamber_type, args.date_from, args.date_to,
                                              known_gids=seen_gids, stop_on_known_page=not args.full_rescan):
                    gid = row.get("gid")
                    if gid in seen_gids:
                        continue
                    seen_gids.add(gid)
                    rec = normalise_row(row, full_name, chamber_type, fetch_full_text=fetch_full_text)
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    total_written += 1
                    print(f"  [{total_written}] {row.get('hdate')}  {rec.get('debate_title')}", file=sys.stderr)

    print(f"\nDone. Wrote {total_written} new speeches to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
