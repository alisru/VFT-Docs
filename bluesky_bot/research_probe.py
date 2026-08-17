"""research_probe.py \u2014 Targeted historical/topic harvesting for Aletheia Research Probe mode.

Replaces harvest_candidates.py when the user wants to judge a historical event
or specific topic rather than live news (e.g. "Hitler 1933", "Thatcher privatisation").

Usage:
    python research_probe.py --probe "Hitler 1933" --limit 5
    python research_probe.py --probe "Albanese housing policy" --year 2024 --limit 8
"""
import os
import sys
import json
import re
import time
import argparse
import urllib.parse
import urllib.request

import requests
from html.parser import HTMLParser
from dotenv import load_dotenv

# ── Resolve paths ─────────────────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

DEFAULT_OUTPUT = os.path.join(script_dir, "harvested_candidates.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}


# ── Simple paragraph extractor ────────────────────────────────────────────────
class ParagraphExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.paragraphs = []
        self.current = []

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == "p":
            self.in_p = False
            text = "".join(self.current).strip()
            if text:
                self.paragraphs.append(text)
            self.current = []

    def handle_data(self, data):
        if self.in_p:
            self.current.append(data)


def scrape_article_text(url: str, timeout: int = 10) -> str:
    """Fetch and extract paragraph text from a URL."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        if resp.status_code != 200:
            return ""
        parser = ParagraphExtractor()
        parser.feed(resp.text)
        text = "\n\n".join(parser.paragraphs)
        return text[:8000]
    except Exception as e:
        print(f"  [WARN] Failed to scrape {url}: {e}")
        return ""


# ── Wikipedia API ─────────────────────────────────────────────────────────────
def search_wikipedia(query: str, year: int = None) -> list:
    """Query Wikipedia search API and fetch summaries for top results."""
    candidates = []

    search_url = (
        "https://en.wikipedia.org/w/api.php"
        "?action=query&list=search&format=json&srlimit=5"
        f"&srsearch={urllib.parse.quote(query)}"
    )
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=10)
        data = resp.json()
        results = data.get("query", {}).get("search", [])
    except Exception as e:
        print(f"  [WARN] Wikipedia search failed: {e}")
        results = []

    for result in results[:5]:
        title = result.get("title", "")
        page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"

        rest_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
        try:
            r = requests.get(rest_url, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                info = r.json()
                extract = info.get("extract", "")
                if extract and len(extract) > 100:
                    if year and str(year) not in extract and str(year) not in title:
                        continue
                    candidates.append({
                        "url": page_url,
                        "text": extract[:5000],
                        "subject": f"{title} (Wikipedia)"
                    })
                    print(f"  [WIKI] Found: {title}")
        except Exception:
            pass

        if len(candidates) >= 3:
            break

    return candidates


# ── DuckDuckGo HTML scraping ───────────────────────────────────────────────────
class DDGResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self._in_result = False
        self._current_href = None
        self._current_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attr_dict = dict(attrs)
            cls = attr_dict.get("class", "")
            href = attr_dict.get("href", "")
            if "result__a" in cls and href.startswith("http"):
                self._in_result = True
                self._current_href = href
                self._current_text = []

    def handle_endtag(self, tag):
        if tag == "a" and self._in_result:
            self._in_result = False
            title = "".join(self._current_text).strip()
            if self._current_href and title:
                self.results.append((self._current_href, title))
            self._current_href = None

    def handle_data(self, data):
        if self._in_result:
            self._current_text.append(data)


def search_duckduckgo(query: str, year: int = None, limit: int = 8) -> list:
    """Scrape DuckDuckGo HTML search for URLs matching the query."""
    q = f"{query} {year}" if year else query
    encoded = urllib.parse.quote(q)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        if resp.status_code != 200:
            print(f"  [WARN] DDG returned status {resp.status_code}")
            return []
    except Exception as e:
        print(f"  [WARN] DDG search failed: {e}")
        return []

    parser = DDGResultParser()
    parser.feed(resp.text)

    SKIP_DOMAINS = {
        "bsky.app", "twitter.com", "x.com", "facebook.com", "instagram.com",
        "tiktok.com", "youtube.com", "reddit.com", "pinterest.com",
        "amazon.com", "ebay.com", "etsy.com", "duckduckgo.com"
    }
    results = []
    for href, title in parser.results:
        try:
            domain = urllib.parse.urlparse(href).netloc.lstrip("www.")
        except Exception:
            continue
        if any(domain == s or domain.endswith("." + s) for s in SKIP_DOMAINS):
            continue
        results.append((href, title))
        if len(results) >= limit:
            break

    return results


def harvest_from_web(query: str, year: int = None, limit: int = 5) -> list:
    """Get candidates from DuckDuckGo + scrape article text."""
    candidates = []
    urls_seen = set()

    search_results = search_duckduckgo(query, year=year, limit=limit * 2)
    print(f"  [DDG] Got {len(search_results)} search results")

    for href, title in search_results:
        if href in urls_seen:
            continue
        urls_seen.add(href)

        print(f"  [SCRAPE] Fetching: {href}")
        text = scrape_article_text(href)
        if not text or len(text) < 200:
            print(f"    -> Too short / empty, skipping")
            continue

        subject = re.sub(r"\s+", " ", title).strip()
        candidates.append({"url": href, "text": text, "subject": subject})
        print(f"    -> OK ({len(text)} chars)")
        time.sleep(0.5)

        if len(candidates) >= limit:
            break

    return candidates


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Aletheia Research Probe: historical/topic-targeted source harvesting"
    )
    parser.add_argument("--probe", type=str, required=True,
                        help="Research query (e.g. 'Hitler 1933', 'Albanese housing policy')")
    parser.add_argument("--year", type=int, default=None,
                        help="Optional year filter to scope results")
    parser.add_argument("--limit", type=int, default=5,
                        help="Number of sources to find (default: 5)")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT,
                        help="Output path for harvested_candidates.json")
    args = parser.parse_args()

    query = args.probe.strip()
    year = args.year

    # Auto-detect year in query if not specified
    if not year:
        year_match = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", query)
        if year_match:
            year = int(year_match.group(1))
            print(f"[PROBE] Auto-detected year: {year}")

    print("=" * 60)
    print(f"ALETHEIA RESEARCH PROBE")
    print(f"Query: {query}")
    if year:
        print(f"Year filter: {year}")
    print(f"Target sources: {args.limit}")
    print("=" * 60)

    all_candidates = []

    # Phase 1: Wikipedia
    print("\n[Phase 1] Wikipedia search...")
    wiki_candidates = search_wikipedia(query, year=year)
    all_candidates.extend(wiki_candidates)
    print(f"  -> {len(wiki_candidates)} Wikipedia sources found")

    # Phase 2: Web search
    remaining = args.limit - len(all_candidates)
    if remaining > 0:
        print(f"\n[Phase 2] Web search ({remaining} more needed)...")
        wiki_urls = {c["url"] for c in all_candidates}
        web_candidates = harvest_from_web(query, year=year, limit=remaining)
        for c in web_candidates:
            if c["url"] not in wiki_urls:
                all_candidates.append(c)

    all_candidates = all_candidates[:args.limit]

    if not all_candidates:
        print("\n[WARN] No sources found.")
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump([], f)
        sys.exit(0)

    print(f"\n[RESULT] {len(all_candidates)} sources harvested")
    for i, c in enumerate(all_candidates, 1):
        print(f"  {i}. {c['subject'][:70]}")

    print(f"\n[WRITE] Saving to {args.output}")
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(all_candidates, f, indent=2, ensure_ascii=False)

    print("[DONE] Research probe harvest complete.")


if __name__ == "__main__":
    main()
