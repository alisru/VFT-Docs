#!/usr/bin/env python3
"""
Fetch a list of tag:url source pages and write extracted text straight to
Sources_Archive/<tag>.txt, without the page text passing through chat context.
Only prints a short per-URL status line.

Usage: python3 fetch_archive.py sources.tsv
where sources.tsv has lines: TAG<TAB>URL<TAB>CITATION_TEXT
"""
import sys, os, requests, trafilatura
from datetime import date

ARCHIVE_DIR = "raw_fetches"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

def fetch_one(tag, url, citation):
    out_path = os.path.join(ARCHIVE_DIR, f"{tag}.txt")
    try:
        r = requests.get(url, headers=HEADERS, timeout=25)
        r.raise_for_status()
        html = r.text
        extracted = trafilatura.extract(html, include_comments=False, include_tables=False, favor_recall=True)
        if not extracted or len(extracted.strip()) < 100:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            for tag_el in soup(["script", "style", "nav", "footer", "header"]):
                tag_el.decompose()
            extracted = soup.get_text(separator="\n")
            extracted = "\n".join(line.strip() for line in extracted.splitlines() if line.strip())
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"SOURCE: [^{tag}]\n")
            f.write(f"CITATION: {citation}\n")
            f.write(f"URL: {url}\n")
            f.write(f"FETCHED: {date.today().isoformat()} (auto, via fetch_archive.py / trafilatura)\n")
            f.write(f"STATUS: fetched, NOT yet independently read/verified against any node claim -- update Sources_Verification_Checklist.md after review\n")
            f.write("\n---EXTRACTED TEXT---\n\n")
            f.write(extracted)
        print(f"OK    {tag}  ({len(extracted)} chars) -> {out_path}")
        return True
    except Exception as e:
        print(f"FAIL  {tag}  {url}  ERROR: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("usage: fetch_archive.py sources.tsv")
        sys.exit(1)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    ok, fail = 0, 0
    with open(sys.argv[1], encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                print(f"SKIP (bad line): {line}")
                continue
            tag, url = parts[0], parts[1]
            citation = parts[2] if len(parts) > 2 else ""
            if fetch_one(tag, url, citation):
                ok += 1
            else:
                fail += 1
    print(f"\nDone. {ok} succeeded, {fail} failed out of {ok+fail}.")

if __name__ == "__main__":
    main()
