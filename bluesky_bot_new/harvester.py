import os
import sys
import glob
import json
import re
import requests
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

# Default Reputable News Feeds
DEFAULT_FEEDS = [
    {"name": "ABC World", "url": "https://www.abc.net.au/news/feed/52278/rss.xml"},
    {"name": "ABC Top Stories", "url": "https://www.abc.net.au/news/feed/45910/rss.xml"},
    {"name": "The Guardian World", "url": "https://www.theguardian.com/world/rss"},
    {"name": "BBC News World", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"}
]

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.paragraphs = []
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p = False
            txt = "".join(self.cur).strip()
            if len(txt) > 30 and not any(bp in txt.lower() for bp in ["cookies", "subscribe", "newsletter", "sign in", "copyright"]):
                self.paragraphs.append(txt)
            self.cur = []

    def handle_data(self, data):
        if self.in_p:
            self.cur.append(data)

def normalize_url(url):
    if not url:
        return ""
    return url.split("?")[0].split("#")[0].rstrip("/").lower().strip()

def scrape_article_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            parser = HTMLTextExtractor()
            parser.feed(resp.text)
            body = "\n\n".join(parser.paragraphs)
            if len(body) >= 200:
                return body
    except Exception as e:
        print(f"  [Scrape Warning] Failed to scrape {url}: {e}")
    return ""

def load_seen_urls(live_dir):
    seen = set()
    if not os.path.exists(live_dir):
        return seen
    for f in glob.glob(os.path.join(live_dir, "factcheck_*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                d = json.load(fh)
            cfg = d[0] if isinstance(d, list) and len(d) > 0 else d
            u = normalize_url(cfg.get("link") or cfg.get("url"))
            if u:
                seen.add(u)
        except Exception:
            pass
    return seen

def harvest_candidates(feeds=None, live_dir=None, max_candidates=5):
    """
    Harvests clean, deduplicated news candidates from RSS feeds.
    """
    feeds = feeds or DEFAULT_FEEDS
    live_dir = live_dir or os.path.join(os.path.dirname(__file__), "stories", "live")
    seen_urls = load_seen_urls(live_dir)

    print(f"Harvesting candidates against {len(seen_urls)} previously published live stories...")
    candidates = []

    for feed in feeds:
        if len(candidates) >= max_candidates:
            break
        print(f"Checking feed: {feed['name']}...")
        try:
            resp = requests.get(feed["url"], timeout=10)
            if resp.status_code != 200:
                continue
            root = ET.fromstring(resp.content)
            items = root.findall(".//item")
            for it in items:
                title = (it.findtext("title") or "").strip()
                link = (it.findtext("link") or "").strip()
                desc = (it.findtext("description") or "").strip()

                norm = normalize_url(link)
                if not norm or norm in seen_urls:
                    continue

                # Quick check: scrape body
                print(f"  Fetching article body: {title[:50]}...")
                body = scrape_article_text(link)
                if not body:
                    body = desc

                candidates.append({
                    "subject": title,
                    "url": link,
                    "body": body
                })
                seen_urls.add(norm)
                if len(candidates) >= max_candidates:
                    break
        except Exception as fe:
            print(f"  Warning: Feed {feed['name']} failed: {fe}")

    print(f"Successfully harvested {len(candidates)} new candidates.")
    return candidates
