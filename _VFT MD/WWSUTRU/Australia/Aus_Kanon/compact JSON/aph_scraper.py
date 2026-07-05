#!/usr/bin/env python3
"""
Federal APH Hansard scraper -- direct against aph.gov.au, bypassing the
OpenAustralia mirror's ~8000-result cap entirely.

Discovered by live reverse-engineering the search form at
https://www.aph.gov.au/Parliamentary_Business/Hansard (an ASP.NET
WebForms page), then confirmed working:

  https://www.aph.gov.au/Parliamentary_Business/Hansard/Search
      ?pv=<Full Name>       <- speaker name, MUST be the full name, e.g.
                               "Anthony Albanese" not just "Albanese"
      &pi=0                 <- person role filter; 0 = All roles (tested;
                               using pi=2 "Speaker" specifically returned
                               nothing, unclear why -- pi=0 is what works)
      &f=DD/MM/YYYY         <- from date
      &to=DD/MM/YYYY        <- to date
      &chi=0                <- chamber/committee filter (0 = All; see
                               CHAMBER_OPTIONS below for other values)
      &coi=0                <- context filter (0 = All)
      &page=N               <- page number (1-based)
      &ps=100                <- results per page (10/25/50/100 confirmed
                               valid options on the page's own dropdown)

Confirmed live: date filtering works correctly (a future date range
returns 0 results, a real range returns real results), and this reaches
much further back than OpenAustralia's capped mirror (that one hard-caps
at 8000 results / roughly 2011 for a prolific speaker; this one has no
such cap since it's the actual government archive).

Each result gives: title, date, chamber/committee, a link to the
human-readable Hansard_Display page, and a direct PDF link to the
official verbatim transcript. This script saves that metadata as JSONL
(same shape as hansard_scraper.py's records, for compatibility) and, if
--download-pdf is set, downloads each result's PDF into a local folder.

KNOWN LIMITATION: clean inline full-text extraction from the
Hansard_Display page itself isn't solved yet -- a generic text extractor
picks up the site's nav menu along with (or instead of) the actual
speech content. The PDF is the reliable full-text source for now; open
it directly, or use --download-pdf to grab it into a local folder next
to the JSONL index.

Usage:
    python3 aph_scraper.py "Anthony Albanese" --from 2006-06-01 --to 2006-07-01
    python3 aph_scraper.py "Anthony Albanese" --from 2020-01-01 --to 2020-12-31 --download-pdf
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse

import requests

BASE = "https://www.aph.gov.au/Parliamentary_Business/Hansard/Search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

CHAMBER_OPTIONS = {
    "all": 0, "senate": 1, "house": 2, "main_committee": 3,
    "joint_committees": 4, "estimates": 5, "other_committees": 6,
}

# The site's own "Context" filter -- restricting to real debate categories
# cuts a lot of bare procedural noise ("BUSINESS - 21 Jun 2006" with no
# actual subject) at the source instead of after the fact.
CONTEXT_OPTIONS = {
    "all": 0, "questions_without_notice": 1, "bills": 2, "adjournment": 3,
    "petitions": 4, "constituency_statements": 5, "statements_by_members": 6,
    "matters_of_public_importance": 7, "ministerial_statement": 8, "condolences": 9,
}

# Bare procedural markers with no actual subject -- e.g. a title that is
# EXACTLY "BUSINESS" (chamber moving to the next agenda item) rather than
# "BUSINESS;Some Actual Bill Name". Filtered out by default since they
# carry no substantive content, only overhead. --keep-procedural disables this.
_GENERIC_TITLE_RE = re.compile(r"^(BUSINESS|PRIME MINISTER|QUESTIONS TO THE SPEAKER)\s*-\s*\d")

RESULT_BLOCK_RE = re.compile(
    r'<p class="title"><a[^>]*href="([^"]+)"[^>]*>(.*?)</a></p>.*?'
    r'<a[^>]*id="[^"]*hlPDF[^"]*"[^>]*href="([^"]+)"',
    re.DOTALL,
)
DATE_DD_RE = re.compile(r"<dt>DATE</dt>\s*<dd>([^<&]+)")


def _to_ddmmyyyy(iso_date):
    """Convert YYYY-MM-DD -> DD/MM/YYYY for this site's date fields."""
    y, m, d = iso_date.split("-")
    return f"{d}/{m}/{y}"


def search_page(name, date_from=None, date_to=None, chamber="all", context="all",
                 role="speaker", page=1, page_size=100):
    # NOTE: ind/st/sr/hto/expand/drvH/pnuH are NOT decorative -- confirmed by
    # direct testing that omitting them causes the backend to silently ignore
    # the pv (person name) filter and return 0 results. Keep all of them.
    params = {
        "ind": "0",
        "st": "1",
        "sr": "0",
        "q": "",
        "hto": "1",
        "expand": "False",
        "drvH": "0",
        "pnuH": "0",
        "pv": name,
        "pi": "2" if role == "speaker" else "0",  # 2 = Speaker role only, 0 = All roles
        "chi": str(CHAMBER_OPTIONS.get(chamber, 0)),
        "coi": str(CONTEXT_OPTIONS.get(context, 0)),
        "page": page,
        "ps": page_size,
    }
    if date_from:
        params["f"] = _to_ddmmyyyy(date_from)
    if date_to:
        params["to"] = _to_ddmmyyyy(date_to)

    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_results(html, drop_generic=True):
    """Extract (display_url, title, pdf_url, date) tuples from a search
    results page. Regex-based rather than a full HTML parser since the
    result blocks have a very consistent, simple structure -- confirmed
    against live pages during development.

    drop_generic=True skips bare procedural markers (e.g. a title that's
    just "BUSINESS - 21 Jun 2006" with no actual subject) that carry no
    substantive content -- pure noise for an audit."""
    results = []
    # Split on each result <li> so DATE_DD_RE matches the right block
    blocks = re.split(r'<li>\s*<p class="title">', html)[1:]
    for block in blocks:
        block = '<p class="title">' + block
        m = RESULT_BLOCK_RE.search(block)
        if not m:
            continue
        display_url, title, pdf_url = m.groups()
        title = re.sub(r"\s+", " ", title).strip()
        if drop_generic and _GENERIC_TITLE_RE.match(title):
            continue
        date_m = DATE_DD_RE.search(block)
        date_str = date_m.group(1).strip() if date_m else None
        if not display_url.startswith("http"):
            display_url = "https://www.aph.gov.au" + display_url
        results.append({
            "title": title,
            "date_display": date_str,
            "hansard_display_url": display_url,
            "pdf_url": pdf_url,
        })
    return results


def search_all(name, date_from=None, date_to=None, chamber="all", context="all",
               role="speaker", drop_generic=True, page_size=100, max_pages=200):
    """Yields result dicts across all pages until an empty page is hit."""
    page = 1
    while page <= max_pages:
        html = search_page(name, date_from, date_to, chamber, context, role, page, page_size)
        results = parse_results(html, drop_generic=drop_generic)
        if not results:
            break
        for r in results:
            yield r
        if len(results) < page_size:
            break  # last page
        page += 1
        time.sleep(0.5)  # be polite to the government server


def download_pdf(pdf_url, out_dir, filename):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    if os.path.exists(path):
        return path  # already downloaded
    try:
        resp = requests.get(pdf_url, headers=HEADERS, timeout=60)
        resp.raise_for_status()
        with open(path, "wb") as f:
            f.write(resp.content)
        time.sleep(0.3)
        return path
    except Exception as e:
        print(f"  [warn] PDF download failed for {pdf_url}: {e}", file=sys.stderr)
        return None


DEFAULT_PDF_CAP = 200  # sane default -- past this, require --force so a huge,
                       # accidental bulk download against a government server
                       # can't happen without the person explicitly asking for it


def main():
    ap = argparse.ArgumentParser(description="Scrape federal Hansard directly from aph.gov.au (no result cap).")
    ap.add_argument("name", help="Full name of the MP/Senator, e.g. 'Anthony Albanese' (must be the full name)")
    ap.add_argument("--out", default=None, help="Output JSONL path (default: <slug>_aph_hansard.jsonl)")
    ap.add_argument("--from", dest="date_from", default=None, help="Earliest date YYYY-MM-DD")
    ap.add_argument("--to", dest="date_to", default=None, help="Latest date YYYY-MM-DD")
    ap.add_argument("--chamber", default="all", choices=list(CHAMBER_OPTIONS.keys()),
                     help="Restrict to a chamber/committee type (default: all)")
    ap.add_argument("--context", default="all", choices=list(CONTEXT_OPTIONS.keys()),
                     help="Restrict to a debate context, e.g. bills, adjournment (default: all)")
    ap.add_argument("--role", default="speaker", choices=["speaker", "all"],
                     help="'speaker' (default) filters to their own speeches; 'all' includes every role "
                          "(author/reporter/presenter/questioner/responder), which is noisier")
    ap.add_argument("--keep-procedural", action="store_true",
                     help="Don't filter out bare procedural entries like 'BUSINESS - <date>' with no subject")
    ap.add_argument("--download-pdf", action="store_true",
                     help="Also download each result's official PDF into a local folder")
    ap.add_argument("--pdf-dir", default=None, help="Folder for downloaded PDFs (default: <slug>_pdfs/)")
    ap.add_argument("--force", action="store_true",
                     help=f"Required if --download-pdf would download more than {DEFAULT_PDF_CAP} PDFs "
                          "-- confirms you actually want that many individual requests against aph.gov.au")
    args = ap.parse_args()

    slug = args.name.lower().replace(" ", "_")
    out_path = args.out or f"{slug}_aph_hansard.jsonl"
    pdf_dir = args.pdf_dir or f"{slug}_pdfs"

    print(f"Searching aph.gov.au Hansard for '{args.name}'...", file=sys.stderr)
    results = list(search_all(
        args.name, args.date_from, args.date_to,
        chamber=args.chamber, context=args.context, role=args.role,
        drop_generic=not args.keep_procedural,
    ))
    print(f"  Found {len(results)} matching Hansard entries.", file=sys.stderr)

    do_pdf = args.download_pdf
    if do_pdf and len(results) > DEFAULT_PDF_CAP and not args.force:
        print(
            f"\n[refusing] --download-pdf would fetch {len(results)} individual PDFs from aph.gov.au, "
            f"well past the safety default of {DEFAULT_PDF_CAP}. That's a lot of individual requests "
            f"against a government server for one run.\n"
            f"Writing the JSONL index (with pdf_url for each entry) WITHOUT downloading. "
            f"Re-run with --force if you genuinely want all {len(results)} PDFs, or narrow the "
            f"--from/--to range / --context / --chamber first.\n",
            file=sys.stderr,
        )
        do_pdf = False

    total = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for r in results:
            total += 1
            rec = {
                "speaker_name": args.name,
                "source": "aph.gov.au",
                "title": r["title"],
                "date_display": r["date_display"],
                "hansard_display_url": r["hansard_display_url"],
                "pdf_url": r["pdf_url"],
                "pdf_local_path": None,
            }
            if do_pdf and r["pdf_url"]:
                fname = re.sub(r"[^A-Za-z0-9_.-]", "_", r["title"])[:100] + ".pdf"
                rec["pdf_local_path"] = download_pdf(r["pdf_url"], pdf_dir, fname)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"  [{total}] {r['date_display']}  {r['title'][:70]}", file=sys.stderr)

    print(f"\nDone. Wrote {total} matching Hansard entries -> {out_path}", file=sys.stderr)
    if do_pdf:
        print(f"PDFs saved to: {pdf_dir}/", file=sys.stderr)


if __name__ == "__main__":
    main()
