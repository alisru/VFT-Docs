import os
import sys
import json
import re
import time
import argparse

# Ensure UTF-8 output encoding to prevent Unicode/Cp1252 printing errors on Windows
if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr and sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from atproto import Client, IdResolver
import requests
from html.parser import HTMLParser

class ParagraphExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.paragraphs = []
        self.current_para = []

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p = False
            para_text = "".join(self.current_para).strip()
            if para_text:
                self.paragraphs.append(para_text)
            self.current_para = []

    def handle_data(self, data):
        if self.in_p:
            self.current_para.append(data)

def scrape_article_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"Error: Status code {response.status_code}"
        
        parser = ParagraphExtractor()
        parser.feed(response.text)
        return "\n\n".join(parser.paragraphs)
    except Exception as e:
        return f"Error: {e}"

# Resolve workspace directory
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(script_dir)
sys.path.append(script_dir)

from generate_graph import draw_graph
from aletheia_bot import save_and_sync_story

# Import rebuild_registries logic
def rebuild_registries_selector(use_son=False):
    if use_son:
        print("Invoking SON registry rebuilder...")
        from rebuild_registries_son import rebuild_registries as rebuild_son
        rebuild_son()
    else:
        print("Invoking standard registry rebuilder...")
        from rebuild_registries import rebuild_registries as rebuild_std
        rebuild_std()

# Deterministic actor extraction for the live pipeline (LLM backfill handles history)
from actor_extract import extract_actors

# Load environment variables
bot_env_path = os.path.join(script_dir, ".env")
load_dotenv(bot_env_path)

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
except ImportError:
    genai = None
    HarmCategory = None
    HarmBlockThreshold = None

# Per-request deadline for Gemini calls. Without it a rate-limited/stalled call
# hangs with no client-side timeout instead of raising into the fallback path.
GEMINI_TIMEOUT_SECS = int(os.environ.get("GEMINI_TIMEOUT_SECS", "90"))

# --- 0. HELPER FUNCTIONS FOR TOKEN MINIFICATION & ALTERNATIVE API ---
def minify_markdown(text):
    # Remove markdown link references e.g. [name](url) -> name
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove markdown alerts (e.g. > [!NOTE])
    text = re.sub(r'>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', '', text)
    
    # Process lines
    lines = [line.strip() for line in text.split('\n')]
    filtered_lines = []
    
    for line in lines:
        # Strip HTML/Markdown comments
        if line.startswith('<!--') or line.endswith('-->'):
            continue
        # Remove pure dividers
        if line.replace('-', '').strip() == '':
            continue
        # Skip empty lines
        if not line:
            continue
        
        filtered_lines.append(line)
        
    return '\n'.join(filtered_lines)

def call_agnes_api(api_key, system_prompt, user_content, model="agnes-2.0-flash"):
    url = "https://apihub.agnes-ai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.15
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        print(f"Posting request to Agnes AI API endpoint with model: {model}...")
        with urllib.request.urlopen(req, timeout=180) as response:
            res_data = json.loads(response.read().decode("utf-8"))
        print("Agnes AI API call successful!")
        return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling Agnes AI API: {e}")
        raise e

def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY environment variable not found. Gemini models will be unavailable.")
        return None
    if genai is None:
        print("Warning: Google Generative AI SDK is not installed. Gemini models will be unavailable.")
        return None
    genai.configure(api_key=api_key)
    return genai

def normalize_url(url):
    if not url:
        return ""
    url = url.strip()
    if "?" in url:
        url = url.split("?")[0]
    if "#" in url:
        url = url.split("#")[0]
    return url.lower().strip()

# --- 1. HISTORICAL STORIES LOADING & DEDUPLICATION ---
def load_historical_evaluations():
    seen_urls = set()
    seen_ids = set()
    seen_targets = set()
    bot_stories_dir = os.path.join(script_dir, "stories")

    # Posted stories get MOVED into live/ (and staged ones sit in darkroom/), so
    # scanning only the root would forget everything already posted and let the
    # bot re-harvest + re-evaluate it.
    scan_dirs = [
        bot_stories_dir,
        os.path.join(bot_stories_dir, "live"),
        os.path.join(bot_stories_dir, "darkroom"),
    ]
    for scan_dir in scan_dirs:
        if not os.path.isdir(scan_dir):
            continue
        try:
            story_files = [f for f in os.listdir(scan_dir) if f.startswith('factcheck_') and f.endswith('.json')]
            for sf in story_files:
                filepath = os.path.join(scan_dir, sf)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                config = data[0] if isinstance(data, list) else data
                
                url = config.get("link") or config.get("target_url")
                if url:
                    seen_urls.add(normalize_url(url))
                
                target_url = config.get("target_url")
                if target_url:
                    rkey = target_url.strip().lower().strip("/").split("/")[-1].split("?")[0].split("#")[0].strip()
                    if rkey:
                        seen_targets.add(rkey)
                    
                story_id = config.get("id")
                if story_id:
                    seen_ids.add(story_id.strip().lower())
        except Exception as e:
            print(f"Warning: Failed to load historical evaluations from {scan_dir}: {e}")
    print(f"Loaded {len(seen_urls)} historical URLs, {len(seen_targets)} target URLs, and {len(seen_ids)} historical story IDs.")
    return seen_urls, seen_ids, seen_targets

def extract_external_link(post):
    record = getattr(post, 'record', None)
    if record:
        embed = getattr(record, 'embed', None)
        if embed and hasattr(embed, 'external'):
            ext = getattr(embed, 'external', None)
            if ext and hasattr(ext, 'uri'):
                return ext.uri
    facets = getattr(record, 'facets', None) or []
    for facet in facets:
        features = getattr(facet, 'features', [])
        for feature in features:
            if hasattr(feature, 'uri'):
                return feature.uri
    embed_view = getattr(post, 'embed', None)
    if embed_view and hasattr(embed_view, 'external'):
        ext = getattr(embed_view, 'external', None)
        if ext and hasattr(ext, 'uri'):
            return ext.uri
    text = getattr(record, 'text', '') if record else ""
    url_match = re.search(r'(https?://[^\s]+)', text)
    if url_match:
        return url_match.group(1)
    return None

# Domains that are never a news article (social media, shorteners-to-self, junk, crypto, adult).
# We use a banlist (not an allowlist) so smaller/regional outlets still pass through.
NON_NEWS_DOMAINS = {
    'bsky.app', 'bsky.social', 'graze.social',
    'twitter.com', 'x.com', 't.co',
    'youtube.com', 'youtu.be', 'tiktok.com',
    'instagram.com', 'facebook.com', 'fb.watch', 'threads.net',
    'reddit.com', 'redd.it', 'twitch.tv', 'discord.gg', 'discord.com',
    'linktr.ee', 'patreon.com', 'ko-fi.com', 'onlyfans.com', 'fansly.com',
    'amazon.com', 'amzn.to', 'etsy.com', 'shopify.com', 'gofundme.com',
    'pinterest.com', 'tumblr.com', 'mastodon.social', 'snapchat.com',
    'coinbase.com', 'binance.com', 'pump.fun', 'opensea.io',
}

# Domains that consistently fail raw scraping due to paywalls, cloudflare blocks,
# or heavy client-side JavaScript requirements.
UNSCRAPABLE_DOMAINS = {
    'pbs.org', 'reut.rs', 'reuters.com',
    'on.wsj.com', 'wsj.com',
    'bloom.bg', 'bloomberg.com',
    'nyti.ms', 'nytimes.com',
    'washingtonpost.com', 'wapo.st',
    'ft.com', 'economist.com', 'afr.com'
}

# Dynamic list of scraping-banned domains loaded from disk
DYNAMIC_BANNED_DOMAINS = set(UNSCRAPABLE_DOMAINS)

# Whitelist of primary trusted news sources that should NEVER be banned dynamically
# due to temporary network timeouts or server glitches.
SCRAPING_WHITELIST = {
    'bbc.com', 'bbc.co.uk', 'bbci.co.uk',
    'abc.net.au',
    'thesaturdaypaper.com.au', 'saturdaypaper.com.au',
    'smh.com.au',
    'techcrunch.com',
    'npr.org'
}

def is_domain_whitelisted(domain):
    d = domain.strip().lower()
    return any(d == wl or d.endswith('.' + wl) for wl in SCRAPING_WHITELIST)

def load_dynamic_banned_domains():
    global DYNAMIC_BANNED_DOMAINS
    path = os.path.join(script_dir, "unscrapable_domains.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    # Keep static defaults in addition to loaded ones
                    DYNAMIC_BANNED_DOMAINS.update(data)
        except Exception as e:
            print(f"Warning: Failed to load dynamic banned domains: {e}")

def save_dynamic_banned_domains():
    path = os.path.join(script_dir, "unscrapable_domains.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sorted(list(DYNAMIC_BANNED_DOMAINS)), f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Failed to save dynamic banned domains: {e}")

def is_news_url(url):
    """Banlist gate: returns True for any real external http(s) URL not on the non-news denylist

    and not on the unscrapable/paywalled domain list.
    Matches the URL's hostname exactly or as a subdomain (suffix match on dot
    boundary). Plain substring matching is wrong: 't.co' would ban
    washingtonpost.com, 'x.com' would ban fox.com, etc.
    """
    if not url:
        return False
    u = url.strip().lower()
    if not u.startswith(('http://', 'https://')):
        return False
    try:
        host = urllib.parse.urlparse(u).hostname or ""
    except Exception:
        return False
    if not host:
        return False
    
    # Check non-news social media/shorteners
    if any(host == bad or host.endswith('.' + bad) for bad in NON_NEWS_DOMAINS):
        return False
        
    # Check paywalled or anti-scraping news domains (static & dynamic)
    if any(host == bad or host.endswith('.' + bad) for bad in DYNAMIC_BANNED_DOMAINS):
        return False
        
    return True

def is_banned(text, url, banned_keywords):
    if not banned_keywords:
        return False
    text_lower = text.lower()
    url_lower = url.lower() if url else ""
    for bk in banned_keywords:
        # Check direct match of the keyword
        if bk in text_lower or (url_lower and bk in url_lower):
            return True
        # If the keyword contains spaces, check hyphenated/underscored/condensed variants
        if " " in bk:
            variants = [bk.replace(" ", "-"), bk.replace(" ", "_"), bk.replace(" ", "")]
            for var in variants:
                if var in text_lower or (url_lower and var in url_lower):
                    return True
    return False

def harvest_bsky_search(client, topic, target, seen_urls, seen_ids, seen_targets, banned_keywords):
    """Open topic search across all of Bluesky via the authenticated searchPosts endpoint.

    Reaches the whole network (not just curated feeds) and keeps only posts whose external
    link is a real news URL (banlist-gated). Returns a list of 'reply'-mode candidates.
    Note: the public (unauthenticated) searchPosts endpoint now returns 403, so this uses
    the logged-in client.
    """
    candidates = []
    keywords = [k.strip() for k in topic.split(",") if k.strip()] if topic else []
    if not keywords:
        return candidates

    print(f"\nOpen-searching Bluesky network for topic(s): {keywords} (Target: {target})...")

    for kw in keywords:
        if len(candidates) >= target:
            break
        try:
            results = client.app.bsky.feed.search_posts(
                {"q": kw, "limit": 100, "sort": "latest", "lang": "en"}
            )
            posts = results.posts
        except Exception as e:
            print(f"Warning: searchPosts failed for '{kw}': {e}")
            continue

        print(f"  '{kw}': {len(posts)} raw posts returned.")
        for post in posts:
            if len(candidates) >= target:
                break
            text = getattr(post.record, 'text', '').strip()
            author_handle = post.author.handle
            rkey = post.uri.split('/')[-1]
            post_url = f"https://bsky.app/profile/{author_handle}/post/{rkey}"

            if len(text) < 45 or text.startswith('@') or text.startswith('Alethekanon'):
                continue
            # Only target ROOT posts. searchPosts returns replies too; replying to
            # someone's reply buried in a thread is not what we want — skip them.
            if getattr(post.record, 'reply', None) is not None:
                continue

            article_url = extract_external_link(post)
            if not is_news_url(article_url):
                continue

            if is_banned(text, article_url, banned_keywords):
                continue

            normalized = normalize_url(article_url)
            if normalized in seen_urls:
                continue
            post_rkey = post_url.strip().lower().strip("/").split("/")[-1].split("?")[0].split("#")[0].strip()
            if post_rkey in seen_targets:
                continue
            subject_approx = text[:30].lower().replace(" ", "_").replace("/", "_")
            if subject_approx in seen_ids:
                continue

            first_line = text.split('\n')[0].strip()
            if ":" in first_line:
                first_line = first_line.split(":")[0].strip()
            subj_cleaned = first_line[:120] if len(first_line) > 0 else "Assessment Summary"

            candidates.append({
                "url": article_url,
                "target_url": post_url,
                "mode": "root",
                "text": text,
                "subject": subj_cleaned
            })
            seen_urls.add(normalized)
            seen_targets.add(post_rkey)

    print(f"Open search yielded {len(candidates)} news-linked candidate(s).")
    return candidates

# --- PREFERRED OUTLETS CONFIGURATION ---
COMMON_OUTLETS = {
    "1": ["bloomberg.com"],
    "2": ["nytimes.com"],
    "3": ["thesaturdaypaper.com.au"],
    "4": ["reuters.com"],
    "5": ["bbc.com", "bbc.co.uk"],
    "6": ["smh.com.au"],
    "7": ["techcrunch.com"],
    "8": ["washingtonpost.com"],
    "9": ["npr.org"]
}

PREFERRED_OUTLET_DOMAINS = []

def is_preferred_outlet(url):
    if not url:
        return False
    u = url.strip().lower()
    try:
        host = urllib.parse.urlparse(u).hostname or ""
    except Exception:
        host = ""
    if not host:
        host = u
    return any(host == pref or host.endswith('.' + pref) for pref in PREFERRED_OUTLET_DOMAINS)

# --- 2. CANDIDATE HARVESTING ---
def harvest_news(target_rss, target_bsky, seen_urls, seen_ids, seen_targets, category="general", topic=None, banned_topic=None):
    candidates = []

    def is_english(text):
        if not text:
            return False
        cleaned_text = re.sub(r'https?://[^\s]+', '', text)
        cleaned_text = re.sub(r'\b[a-zA-Z0-9-]+\.[a-z]{2,}/[^\s]*', '', cleaned_text)
        
        cjk_re = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff\uac00-\ud7af\uff00-\uffef]')
        if cjk_re.search(cleaned_text):
            return False
            
        non_eng_chars = re.compile(r'[áéíóúñ¿¡àèùçâêîôûëïüöäüß]', re.IGNORECASE)
        if len(non_eng_chars.findall(cleaned_text)) > 2:
            return False
            
        english_words = re.compile(r'\b(the|with|they|have|what|which|there|their|about|would|could|this|that|from|some|more|news|study|report|said|and|for|out|but|been|has|was|were)\b', re.IGNORECASE)
        romance_words = re.compile(r'\b(de|la|el|los|las|en|y|que|un|una|des|du|pour|dans|avec|por|para|con|mais|es|est|une|les|se|ce|cette|del|al|ou|qui|dans)\b', re.IGNORECASE)
        
        eng_matches = len(english_words.findall(cleaned_text))
        romance_matches = len(romance_words.findall(cleaned_text))
        
        if eng_matches < 1:
            return False
        if romance_matches >= eng_matches:
            return False
            
        return True
    
    # Resolve category string (may be CSV) to a deduplicated list
    _CATEGORY_FEEDS = {
        "tech": [
            {"name": "BBC Tech", "url": "http://feeds.bbci.co.uk/news/technology/rss.xml"},
            {"name": "NYT Tech", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"},
            {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
            {"name": "The Guardian Tech", "url": "https://www.theguardian.com/technology/rss"},
        ],
        "business": [
            {"name": "BBC Business", "url": "http://feeds.bbci.co.uk/news/business/rss.xml"},
            {"name": "NYT Business", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"},
            {"name": "CNBC Business", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147"},
            {"name": "The Guardian Business", "url": "https://www.theguardian.com/business/rss"},
            {"name": "DW Business", "url": "https://rss.dw.com/xml/rss-en-bus"},
        ],
        "politics": [
            {"name": "BBC Politics", "url": "http://feeds.bbci.co.uk/news/politics/rss.xml"},
            {"name": "NYT Politics", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml"},
            {"name": "NPR Politics", "url": "https://feeds.npr.org/1014/rss.xml"},
            {"name": "The Guardian Politics", "url": "https://www.theguardian.com/politics/rss"},
        ],
        "science": [
            {"name": "BBC Science", "url": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"},
            {"name": "NYT Science", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml"},
            {"name": "The Guardian Science", "url": "https://www.theguardian.com/science/rss"},
            {"name": "DW Science", "url": "https://rss.dw.com/xml/rss-en-science"},
        ],
        "world": [
            {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
            {"name": "NYT World", "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"},
            {"name": "The Guardian World", "url": "https://www.theguardian.com/world/rss"},
            {"name": "NPR World", "url": "https://feeds.npr.org/1004/rss.xml"},
            {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
            {"name": "DW News World", "url": "https://rss.dw.com/xml/rss-en-all"},
            {"name": "France 24", "url": "https://www.france24.com/en/rss"},
            {"name": "CBC News", "url": "https://rss.cbc.ca/lineup/topstories.xml"},
            {"name": "UPI News", "url": "https://rss.upi.com/news/news.rss"},
            {"name": "Google News World", "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en"},
        ],
        "general": [
            {"name": "ABC News Australia", "url": "https://www.abc.net.au/news/feed/2942460/rss.xml"},
            {"name": "9News Australia", "url": "https://www.9news.com.au/rss"},
            {"name": "SBS News", "url": "https://www.sbs.com.au/news/feed"},
            {"name": "Sydney Morning Herald", "url": "https://www.smh.com.au/rss/feed.xml"},
            {"name": "Perth Now", "url": "https://www.perthnow.com.au/feed"},
            {"name": "The Age", "url": "https://www.theage.com.au/rss/feed.xml"},
            {"name": "Brisbane Times", "url": "https://www.brisbanetimes.com.au/rss/feed.xml"},
            {"name": "WA Today", "url": "https://www.watoday.com.au/rss/feed.xml"},
            {"name": "Canberra Times", "url": "https://www.canberratimes.com.au/rss.xml"},
            {"name": "BBC News", "url": "http://feeds.bbci.co.uk/news/rss.xml"},
            {"name": "NYT Home", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"},
            {"name": "The Guardian UK", "url": "https://www.theguardian.com/uk/rss"},
            {"name": "The Guardian World", "url": "https://www.theguardian.com/world/rss"},
            {"name": "NPR News", "url": "https://feeds.npr.org/1001/rss.xml"},
            {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
            {"name": "Google News World", "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News Australia", "url": "https://news.google.com/rss?hl=en-AU&gl=AU&ceid=AU:en"},
        ],
    }

    categories = [c.strip().lower() for c in (category or "general").split(",") if c.strip()]
    if not categories:
        categories = ["general"]
    seen_feed_urls: set = set()
    rss_feeds = []
    for cat in categories:
        for feed in _CATEGORY_FEEDS.get(cat, _CATEGORY_FEEDS["general"]):
            if feed["url"] not in seen_feed_urls:
                seen_feed_urls.add(feed["url"])
                rss_feeds.append(feed)

    print(f"Harvest category selected: {', '.join(c.upper() for c in categories)}")
    keywords = [k.strip().lower() for k in topic.split(",") if k.strip()] if topic else []
    if keywords:
        print(f"Applying topic filters (OR match): {keywords}")
        
    banned_keywords = [k.strip().lower() for k in banned_topic.split(",") if k.strip()] if banned_topic else []
    if banned_keywords:
        print(f"Applying banned topic filters (excluding): {banned_keywords}")
    
    # Harvest RSS
    if target_rss > 0:
        print(f"\nHarvesting from RSS feeds (Target: {target_rss})...")
        for feed in rss_feeds:
            print(f"Fetching from {feed['name']} RSS feed: {feed['url']}...")
            req = urllib.request.Request(feed['url'], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    content = response.read()
                root = ET.fromstring(content)
                items = root.findall('.//item')
                print(f"Found {len(items)} items in {feed['name']}.")
                
                for item in items:
                    title = item.find('title')
                    desc = item.find('description')
                    link = item.find('link')
                    
                    title_text = title.text.strip() if title is not None and title.text else ""
                    desc_text = desc.text.strip() if desc is not None and desc.text else ""
                    link_text = link.text.strip() if link is not None and link.text else ""
                    
                    if not title_text or not link_text:
                        continue
                        
                    if not is_news_url(link_text):
                        continue
                        
                    desc_cleaned = re.sub(r'<[^>]*>', '', desc_text)
                    text_body = f"{title_text}\n\n{desc_cleaned}"
                    
                    if len(text_body) < 45:
                        continue
                        
                    # Topic filtering
                    if keywords:
                        if not any(k in title_text.lower() or k in desc_cleaned.lower() for k in keywords):
                            continue
                            
                    # Banned topic filtering
                    if is_banned(title_text + "\n" + desc_cleaned, link_text, banned_keywords):
                        continue
                            
                    normalized = normalize_url(link_text)
                    if normalized in seen_urls:
                        continue
                    subject_approx = title_text[:30].lower().replace(" ", "_").replace("/", "_")
                    if subject_approx in seen_ids:
                        continue
                        
                    # Parse publication date
                    import datetime
                    pub_date = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
                    for child in item:
                        tag_lower = child.tag.lower()
                        if tag_lower.endswith('pubdate') or tag_lower.endswith('date'):
                            if child.text:
                                try:
                                    val = child.text.strip()
                                    if 'T' in val:
                                        pub_date = datetime.datetime.fromisoformat(val.replace('Z', '+00:00'))
                                    else:
                                        import email.utils
                                        pub_date = email.utils.parsedate_to_datetime(val)
                                    if pub_date.tzinfo is None:
                                        pub_date = pub_date.replace(tzinfo=datetime.timezone.utc)
                                    break
                                except Exception:
                                    pass

                    candidates.append({
                        "url": link_text,
                        "target_url": "",
                        "mode": "root",
                        "text": text_body,
                        "subject": title_text,
                        "pub_date": pub_date
                    })
                    seen_urls.add(normalized)
            except Exception as e:
                print(f"Warning: Failed to fetch {feed['name']} RSS: {e}")

    # Harvest Bluesky
    if target_bsky > 0:
        print(f"\nHarvesting from Bluesky feeds (Target: {target_bsky})...")
        handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
        password = os.environ.get('BSKY_PASSWORD')

        if password:
            client = Client()
            try:
                client.login(handle, password)
                resolver = IdResolver()

                # When a topic is set, first reach across the whole network via open search,
                # then let the curated feeds below top up any remaining slots (combined mode).
                if keywords:
                    candidates.extend(harvest_bsky_search(
                        client, topic, target_bsky, seen_urls, seen_ids, seen_targets, banned_keywords
                    ))

                bsky_feeds = [
                "https://bsky.app/profile/nickevershed.bsky.social/feed/aaaluca6lksmc",
                    "https://bsky.app/profile/aendra.com/feed/verified-news",
                    "https://bsky.app/profile/aendra.com/feed/news-2-0"
                ]
                

                for feed_url in bsky_feeds:
                    print(f"Fetching from feed: {feed_url}...")
                    parts = feed_url.strip("/").split("/")
                    feed_handle, feed_rkey = parts[parts.index("profile")+1], parts[parts.index("feed")+1]
                    feed_did = resolver.handle.resolve(feed_handle)
                    feed_uri = f"at://{feed_did}/app.bsky.feed.generator/{feed_rkey}"
                    
                    feed_data = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 60})
                    
                    for item in feed_data.feed:
                        text = getattr(item.post.record, 'text', '').strip()
                        author_handle = item.post.author.handle
                        rkey = item.post.uri.split('/')[-1]
                        post_url = f"https://bsky.app/profile/{author_handle}/post/{rkey}"
                        
                        if len(text) < 45 or text.startswith('@') or text.startswith('Alethekanon'):
                            continue
                        # Only target root posts — never reply to a reply buried in a thread.
                        if getattr(item.post.record, 'reply', None) is not None:
                            continue
                        if "PINNED POST" in text or "News feeds" in text or "Every feed I run" in text:
                            continue
                        if any(domain in post_url for domain in ['zeit.de', 'tijd.be', 'sapo.pt', 'demorgen.be', 'folha.com', 'nu.nl', 'gazeteoksijen.com', 'graze.social']):
                            continue
                        if not is_english(text):
                            continue
                            
                        # HARD RULE: only target posts that link to a real NEWS URL.
                        # No quote-only posts, no video posts, no bsky/social/junk links.
                        article_url = extract_external_link(item.post)
                        if not is_news_url(article_url):
                            continue

                        # Topic filtering
                        if keywords:
                            if not any(k in text.lower() for k in keywords):
                                continue
                                
                        # Banned topic filtering
                        if is_banned(text, article_url, banned_keywords):
                            continue

                        normalized = normalize_url(article_url)
                        
                        if normalized in seen_urls:
                            continue
                            
                        post_rkey = post_url.strip().lower().strip("/").split("/")[-1].split("?")[0].split("#")[0].strip()
                        if post_rkey in seen_targets:
                            continue
                            
                        subject_approx = text[:30].lower().replace(" ", "_").replace("/", "_")
                        if subject_approx in seen_ids:
                            continue
                            
                        first_line = text.split('\n')[0].strip()
                        if ":" in first_line:
                            first_line = first_line.split(":")[0].strip()
                        subj_cleaned = first_line[:120] if len(first_line) > 0 else "Assessment Summary"

                        candidates.append({
                            "url": article_url,
                            "target_url": post_url,
                            "mode": "root",
                            "text": text,
                            "subject": subj_cleaned
                        })
                        seen_urls.add(normalized)
                        seen_targets.add(post_rkey)
            except Exception as e:
                print(f"Warning: Bluesky login or retrieval failed: {e}")
        else:
            print("Warning: BSKY_PASSWORD not found. Skipping Bluesky harvesting.")
            
    # Separate candidates by mode (checking target_url since all are root now)
    rss_cands = [c for c in candidates if not c.get("target_url")]
    bsky_cands = [c for c in candidates if c.get("target_url")]

    # Sort all RSS candidates by pub_date descending (newest first)
    import datetime
    rss_cands = sorted(
        rss_cands,
        key=lambda c: c.get("pub_date", datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)),
        reverse=True
    )

    # Prioritize preferred outlets in Bluesky candidates
    preferred_bsky = [c for c in bsky_cands if is_preferred_outlet(c["url"])]
    regular_bsky = [c for c in bsky_cands if not is_preferred_outlet(c["url"])]
    print(f"Bluesky Harvest: {len(preferred_bsky)} preferred outlets, {len(regular_bsky)} regular outlets found.")
    bsky_cands = (preferred_bsky + regular_bsky)[:target_bsky]

    # Prioritize preferred outlets in RSS candidates
    preferred_rss = [c for c in rss_cands if is_preferred_outlet(c["url"])]
    regular_rss = [c for c in rss_cands if not is_preferred_outlet(c["url"])]
    rss_cands = (preferred_rss + regular_rss)[:target_rss]

    # Combine so preferred are processed first
    combined = rss_cands + bsky_cands
    preferred_final = [c for c in combined if is_preferred_outlet(c["url"])]
    regular_final = [c for c in combined if not is_preferred_outlet(c["url"])]
    
    final_cands = preferred_final + regular_final
    for c in final_cands:
        if "pub_date" in c and isinstance(c["pub_date"], datetime.datetime):
            c["pub_date"] = c["pub_date"].isoformat()
            
    return final_cands

# --- 3. EXECUTE SINGLE-SHOT BATCH EVALUATION VIA GOOGLE AI STUDIO API ---
DEFAULT_FALLBACKS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "vertex:gemini-3.1-flash-lite",
    "gemini-3-flash-preview",
    "gemma-4-31b-it",
    "gemma-4-26b-a4b-it",   
]

_RULES_CACHE = {}

def _load_rules(use_son=False):
    """Read + minify the rules files once per process; they don't change mid-run."""
    cache_key = "son" if use_son else "regular"
    if cache_key not in _RULES_CACHE:
        if use_son:
            convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son_lite.md")
            formatting_path = os.path.join(script_dir, "instructions", "thread_formatting_son.md")
        else:
            convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_lite.md")
            formatting_path = os.path.join(script_dir, "instructions", "thread_formatting.md")
        with open(convergence_path, "r", encoding="utf-8") as f:
            _RULES_CACHE[f"{cache_key}_convergence"] = minify_markdown(f.read())
        with open(formatting_path, "r", encoding="utf-8") as f:
            _RULES_CACHE[f"{cache_key}_formatting"] = minify_markdown(f.read())
    return _RULES_CACHE[f"{cache_key}_convergence"], _RULES_CACHE[f"{cache_key}_formatting"]

def run_one_shot_evaluations(genai_client, candidates, model_name, agnes_api_key=None, use_son=False, use_search=False, extra_context=None, model_sequence=None, compact=False):
    convergence_rules, formatting_rules = _load_rules(use_son=use_son)
        
    # Prepend compact mode directive to formatting rules if active
    if compact:
        override_text = (
            "=== COMPACT MODE DIRECTIVE ===\n"
            "- Posts 1 to 4 (indices 0 to 3 in the posts array: Hook, Claim, Reality, Verdict) will be posted as standard text on Bluesky. They MUST be kept strictly under 260 characters each.\n"
            "- Posts 5 to 13 (indices 4 to 12 in the posts array: Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Alethekanon, Awwthekanon, Brothekanon) will be rendered into a graphical image. They have NO character limits. They MUST be highly verbose, comprehensive, and detailed (typically 400-800 characters each) to explain the concepts fully. DO NOT compress or shorten them.\n\n"
        )
        formatting_rules = override_text + formatting_rules
        formatting_rules = formatting_rules.replace("Keep every single step strictly under **275 characters**", "Keep the first 4 steps under **275 characters** (steps 5-13 have no limits)")

    # System prompt: pure role declaration only
    if compact:
        system_instruction = (
            "You are the Master Aletheia Auditor. Respond ONLY with the exact delimited data rows requested. No commentary, no markdown, no preamble, no explanation. "
            "Use Google Search ONLY to fact-check names, dates, and medical/legal claims from the article. Do NOT use search results to alter your structural analysis or your Alethekanon persona. "
            "You are strictly forbidden from inventing, guessing, or inferring specific details not explicitly written in the text or verified by search. "
            "Adhere to a strict budget of AT MOST 1 search query per story to stay within API quota limits. "
            "If you used Google Search to verify any information in your response for a candidate, you MUST append the emoji 🌐 at the end of the first post (post 1) of that candidate's thread, and you should mention/cite the verified facts or source details in the Alethekanon post (post 11) if relevant. "
            "CRITICAL: Posts 1 to 4 (items 0 to 3 in the posts array) MUST be under 260 characters (hard limit) as they are posted as text. Posts 5 to 13 (items 4 to 12 in the posts array) have NO character limits and should be highly verbose, comprehensive, and detailed (typically 400-800 characters each) because they will be rendered into a high-fidelity visual image card."
        )
    else:
        system_instruction = (
            "You are the Master Aletheia Auditor. Respond ONLY with the exact delimited data rows requested. No commentary, no markdown, no preamble, no explanation. "
            "Use Google Search ONLY to fact-check names, dates, and medical/legal claims from the article. Do NOT use search results to alter your structural analysis or your Alethekanon persona. "
            "You are strictly forbidden from inventing, guessing, or inferring specific details not explicitly written in the text or verified by search. "
            "Adhere to a strict budget of AT MOST 1 search query per story to stay within API quota limits. "
            "If you used Google Search to verify any information in your response for a candidate, you MUST append the emoji 🌐 at the end of the first post (post 1) of that candidate's thread, and you should mention/cite the verified facts or source details in the Alethekanon post (post 11) if relevant. "
            "CRITICAL: EVERY SINGLE POST IN THE THREAD MUST BE UNDER 270 CHARACTERS. THIS IS A HARD LIMIT. BE CONCISE."
        )
    if extra_context:
        system_instruction += f"\n\nCRITICAL: You must actively incorporate the following background knowledge and additional context when performing the audits:\n{extra_context}"

    # Build the full user message: rules + candidates + strict JSON matrix output demand
    n = len(candidates)
    expected_len = 25 if use_son else 17
    output_format = (
        f"OUTPUT FORMAT — YOUR ENTIRE RESPONSE MUST BE A SINGLE VALID JSON LIST OF LISTS. NO commentary, NO markdown formatting (other than JSON code fences if desired), NO explanation.\n"
        f"The JSON array must contain exactly {n} elements (one per candidate, in the same order). Each element must be a list of exactly {expected_len} items representing the evaluation of that candidate in this specific structure:\n"
        "[\n"
        "  [\n"
        '    "thinking",                                // item[0]: detailed thinking/scratchpad calculations (Phase 1 to 5 calculations)\n'
        '    "id",                                      // item[1]: clean story id slug\n'
        '    "subject",                                 // item[2]: story subject\n'
        '    "link",                                    // item[3]: story link\n'
        '    "target_url",                              // item[4]: reply target post url\n'
        "    claim_u (float),                           // item[5]: stated morality\n"
        "    claim_psi (float),                         // item[6]: stated will\n"
        "    real_u (float),                            // item[7]: actual morality\n"
        "    real_psi (float),                          // item[8]: actual will\n"
        '    "mode",                                    // item[9]: root or reply\n'
        "    [\n"
        '      "post 1 (under 260 chars, ending with 1-2 hashtags)",\n'
        '      "post 2 (under 260 chars)",\n'
        "      ...\n"
        "      (exactly 13 posts)                       // item[10]: posts array\n"
        "    ],\n"
        '    ["Actor / Org / Geopolitical tag", ...],  // item[11]: actors array\n'
        '    "macro_event",                             // item[12]: overarching context name or "" if none\n'
        "    macro_claim_u (float or null),             // item[13]: macro stated morality, null if none\n"
        "    macro_claim_psi (float or null),           // item[14]: macro stated will, null if none\n"
        "    macro_real_u (float or null),              // item[15]: macro actual morality, null if none\n"
        "    macro_real_psi (float or null)             // item[16]: macro actual will, null if none\n"
    )
    if use_son:
        output_format += (
            ",\n"
            "    claim_rnet (float),                        // item[17]: stated R_net integrity score\n"
            "    real_rnet (float),                         // item[18]: actual R_net integrity score\n"
            "    claim_z (int),                             // item[19]: stated uncertainty score (blank count, sum of blank counts across planes)\n"
            "    real_z (int),                              // item[20]: actual uncertainty score\n"
            "    claim_z_profile (7-number array of ints),  // item[21]: stated blank profile [B_Q1, B_Q2, B_Q3, B_Q4, B_Q5, B_Q6, B_Q7]\n"
            "    real_z_profile (7-number array of ints),   // item[22]: actual blank profile\n"
            '    "claim_integrity",                         // item[23]: stated integrity label mapped from claim_rnet\n'
            '    "real_integrity"                           // item[24]: actual integrity label mapped from real_rnet\n'
        )
    output_format += (
        "\n"
        "  ]\n"
        "]\n\n"
        "CRITICAL FOR MACRO CONTEXT:\n"
        "Identify if the candidate news story exists within a distinct overarching macro-event context (e.g. an announcement happening at a political photo-op/rally, or a sports title win happening at a White House PR event). If so, provide the macro-event name in item[12] and evaluate its stated and actual u/psi coordinates in items[13] to [16]. If no distinct macro-context exists, use empty string for item[12] and null for items[13] to [16].\n\n"
        "item[11] = actors array: principal named individuals, orgs, nation-states, or blocs (CRINK/BRICS/NATO/AUKUS/G7/SCO/Five Eyes) the story is ABOUT. Canonical full names. Max 6. [] if none.\n\n"
    )
    if use_son:
        output_format += (
            "INTEGRITY TIER MAPPING FOR ITEMS [23] AND [24]:\n"
            "Map claim_rnet to item[23] (claim_integrity) and real_rnet to item[24] (real_integrity) using these strict boundaries:\n"
            "- R_net == 1.0: \"Absolute Truth\"\n"
            "- 1.0 < R_net <= 1.5: \"Trustworthy\"\n"
            "- 1.5 < R_net <= 2.0: \"Conditionally Sound\"\n"
            "- 2.0 < R_net <= 5.0: \"Partially Distorted\"\n"
            "- 5.0 < R_net <= 10.0: \"Meaningful Distortion\"\n"
            "- 10.0 < R_net <= 100.0: \"Severe Deception\"\n"
            "- R_net > 100.0: \"Baseless Lies\"\n\n"
        )
    output_format += (
        "EXAMPLE RESPONSE (for a single candidate, format exactly as JSON list of lists):\n"
        "[\n"
        "  [\n"
        '    "Detailed Phase 1-5 structural scan and calculations...",\n'
        '    "my_slug_id",\n'
        '    "Story Title",\n'
        '    "https://...",\n'
        '    "",\n'
        "    1.0,\n"
        "    0.0,\n"
        "    -1.0,\n"
        "    -1.0,\n"
        '    "root",\n'
        "    [\n"
        '      "Hook text here.\\nEvidence: a, b, c\\n#Aletheia #Topic",\n'
        '      "Claim text.\\nStated Judgement: (+1.0, 0.0) — Good Preference",\n'
        '      "Reality text.\\nResulting Judgement: (-1.0, -1.0) — Greater Evil",\n'
        '      "Verdict: FAIL — The Path of Deception.\\nExplanation.",\n'
        '      "Context paragraph.",\n'
        '      "The Bright Side:\\nNuance.",\n'
        '      "The Breakdown & Plane Error:\\nExplanation.",\n'
        '      "**Social Physics Analysis:**\\nDirect, conversational analysis in plain English detailing selfishness, pretexts, and projection.",\n'
        '      "The Trajectory: The Path of Deception.\\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward Greater Evil. Explanatory mathematical sentence.",\n'
        '      "The Unavoidable Truth: truth.\\n\\nThe Unavoidable Lie: lie.",\n'
        '      "Alethekanon:\\nAnalysis.",\n'
        '      "Awwthekanon:\\nEmpathy.",\n'
        '      "Brothekanon:\\nCasual take."\n'
        "    ],\n"
        '    ["Nigel Farage", "Reform UK", "United Kingdom"],\n'
        '    "",\n'
        "    null,\n"
        "    null,\n"
        "    null,\n"
        "    null"
    )
    if use_son:
        output_format += (
            ",\n"
            "    1.0,\n"
            "    12.5,\n"
            "    0,\n"
            "    4,\n"
            "    [0, 0, 0, 0, 0, 0, 0],\n"
            "    [1, 0, 0, 2, 1, 0, 0],\n"
            '    "Absolute Truth",\n'
            '    "Severe Deception"'
        )
    output_format += (
        "\n"
        "  ]\n"
        "]"
    )

    user_payload = [
        f"=== CONVERGENCE TEST RULES ===\n{convergence_rules}\n\n",
        f"=== THREAD FORMATTING & SCHEMAS ===\n{formatting_rules}\n\n"
    ]
    if extra_context:
        user_payload.append(f"=== ADDITIONAL CONTEXT / BACKGROUND TO CONSIDER ===\n{extra_context}\n\n")
    user_payload.extend([
        f"=== CANDIDATES TO EVALUATE ({n} total) ===\n{json.dumps(candidates, separators=(',', ':'), ensure_ascii=False)}\n\n",
        f"{output_format}"
    ])
    user_payload_str = "".join(user_payload)
    
    # Try the specified model, fallback if rate-limited or fails
    default_fallbacks = DEFAULT_FALLBACKS
    # Keep unique order, trying model_name first
    fallback_models = []
    if model_sequence:
        for m in model_sequence:
            if m not in fallback_models:
                fallback_models.append(m)
    else:
        for m in [model_name] + default_fallbacks:
            if m not in fallback_models:
                fallback_models.append(m)
            
    # Append Agnes AI at the very end of fallback list if key exists
    if agnes_api_key or os.environ.get("AGNES_API_KEY"):
        if "agnes-2.0-flash" not in fallback_models:
            fallback_models.append("agnes-2.0-flash")
        
    last_exception = None
    
    for model in fallback_models:
        print(f"Attempting batch evaluation call using model: {model}...")
        try:
            if model.startswith("agnes"):
                key = agnes_api_key or os.environ.get("AGNES_API_KEY")
                return call_agnes_api(key, system_instruction, user_payload_str, model=model), []
            elif model.startswith("vertex:"):
                # Dynamically import and initialize the new google-genai SDK for Vertex AI fallback
                from google import genai as vertex_genai
                from google.genai import types as vertex_types
                
                base_model = model.split(":", 1)[1]
                vertex_key = os.environ.get("VERTEX_API_KEY")
                project_id = os.environ.get("VERTEX_PROJECT_ID", "alethekanon")
                location = os.environ.get("VERTEX_LOCATION", "us-central1")
                
                client_args = {
                    "vertexai": True
                }
                if vertex_key:
                    client_args["api_key"] = vertex_key
                else:
                    client_args["project"] = project_id
                    client_args["location"] = location
                
                print(f"Initializing Vertex AI client (key present: {bool(vertex_key)})...")
                v_client = vertex_genai.Client(**client_args)
                
                v_tools = None
                if use_search:
                    v_tools = [vertex_types.Tool(google_search=vertex_types.GoogleSearch())]
                    
                v_safety = [
                    vertex_types.SafetySetting(category='HARM_CATEGORY_HATE_SPEECH', threshold='BLOCK_NONE'),
                    vertex_types.SafetySetting(category='HARM_CATEGORY_HARASSMENT', threshold='BLOCK_NONE'),
                    vertex_types.SafetySetting(category='HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold='BLOCK_NONE'),
                    vertex_types.SafetySetting(category='HARM_CATEGORY_DANGEROUS_CONTENT', threshold='BLOCK_NONE'),
                ]
                
                config = vertex_types.GenerateContentConfig(
                    temperature=0.15,
                    max_output_tokens=8192,
                    system_instruction=system_instruction,
                    tools=v_tools,
                    safety_settings=v_safety
                )
                
                response = v_client.models.generate_content(
                    model=base_model,
                    contents=user_payload_str,
                    config=config
                )
                result_text = response.text.strip()
            else:
                if not genai_client:
                    raise ValueError("Gemini API client not initialized.")
                config = genai_client.types.GenerationConfig(
                    temperature=0.15,
                    max_output_tokens=8192
                )
                
                # Setup tools if search grounding is enabled
                tools_list = None
                if use_search:
                    # Use 'google_search_retrieval' for 1.0/1.5 models, 'google_search' for 2.0+ models
                    if any(x in model for x in ["-1.5", "-1.0"]):
                        tools_list = [genai.protos.Tool(google_search_retrieval={})]
                    else:
                        tools_list = [genai.protos.Tool(google_search={})]

                model_instance = genai_client.GenerativeModel(
                    model_name=model,
                    system_instruction=system_instruction,
                    generation_config=config,
                    tools=tools_list
                )
                # Configure safety settings to prevent false-positive censorship of news content
                safety_settings = None
                if genai_client and HarmCategory and HarmBlockThreshold:
                    safety_settings = {
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    }

                # Without a timeout the gRPC call has no client-side deadline, so a
                # 429/quota stall hangs forever instead of raising into the except
                # below (which is what rotates to the next fallback model).
                response = model_instance.generate_content(
                    user_payload_str,
                    request_options={"timeout": GEMINI_TIMEOUT_SECS},
                    safety_settings=safety_settings
                )
                result_text = response.text.strip()

            # Pre-flight JSON validation to trigger fallback on truncation/corruption
            content = result_text
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            start_idx = content.find("[")
            end_idx = content.rfind("]")
            if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
                raise ValueError("Model output does not contain a valid JSON array structure (likely truncated or blocked by safety filters).")
            
            try:
                json.loads(content[start_idx:end_idx+1])
            except Exception as je:
                raise ValueError(f"Model output is not complete valid JSON (likely truncated): {je}")

            try:
                usage = response.usage_metadata
                tokens_str = f"(Prompt tokens: {usage.prompt_token_count}, Candidate tokens: {usage.candidates_token_count}, Total: {usage.total_token_count})"
            except Exception:
                tokens_str = ""
            print(f"API call successful with model: {model} {tokens_str}")

            # Check if search grounding was actually triggered and collect source URLs
            grounding_urls = []
            if use_search and response:
                try:
                    if hasattr(response, 'candidates') and response.candidates:
                        cand = response.candidates[0]
                        if hasattr(cand, 'grounding_metadata') and cand.grounding_metadata:
                            gm = cand.grounding_metadata
                            if hasattr(gm, 'grounding_chunks') and gm.grounding_chunks:
                                for chunk in gm.grounding_chunks:
                                    if hasattr(chunk, 'web') and chunk.web and hasattr(chunk.web, 'uri') and chunk.web.uri:
                                        url = chunk.web.uri
                                        if url not in grounding_urls:
                                            grounding_urls.append(url)
                except Exception as ge:
                    print(f"  Warning checking grounding chunks: {ge}")

            return result_text, grounding_urls
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "exhausted" in err_str or "quota" in err_str:
                print(f"Rate limited or quota exhausted on model {model}. Trying fallback...")
            elif "deadline" in err_str or "timeout" in err_str or "504" in err_str:
                print(f"Model {model} timed out after {GEMINI_TIMEOUT_SECS}s (likely stalled/rate-limited). Trying fallback...")
            else:
                print(f"Warning: Model {model} failed: {e}")
            last_exception = e
            time.sleep(2)
            
    print(f"CRITICAL: All models failed in one-shot batch evaluation. Last error: {last_exception}")
    sys.exit(1)

def transpose_flat_to_json(flat_text):
    # Strip markdown fences if present
    content = flat_text.strip()
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    # Locate array start [ and end ]
    start_idx = content.find("[")
    end_idx = content.rfind("]")
    if start_idx == -1 or end_idx == -1:
        print("ERROR: Could not find valid JSON array brackets in model output.")
        print("--- RAW MODEL OUTPUT (first 500 chars) ---")
        print(flat_text[:500])
        print("------------------------------------------")
        return []
        
    json_str = content[start_idx:end_idx+1]
    
    try:
        data = json.loads(json_str)
    except Exception as je:
        print(f"Warning: Failed to parse response as complete JSON ({je}). Attempting block-by-block recovery of completed elements...")
        
        # Block-by-block parsing recovery
        lines = content.split('\n')
        data = []
        current_block = []
        in_block = False
        
        for line in lines:
            if not in_block:
                if line.startswith("  ["):
                    in_block = True
                    current_block = [line]
            else:
                current_block.append(line)
                if line.startswith("  ]") or line.startswith("  ],"):
                    block_str = "\n".join(current_block).strip()
                    if block_str.endswith(","):
                        block_str = block_str[:-1].strip()
                    try:
                        parsed = json.loads(block_str)
                        if isinstance(parsed, list):
                            data.append(parsed)
                        in_block = False
                        current_block = []
                    except Exception:
                        pass
                        
        if not data:
            print("ERROR: Block-by-block parser could not recover any valid JSON elements.")
            print("--- EXTRACTED JSON STRING (first 500 chars) ---")
            print(json_str[:500])
            print("-----------------------------------------------")
            return []
        else:
            print(f"Successfully recovered {len(data)} completed evaluation element(s) from truncated JSON.")
        
    if not isinstance(data, list):
        print("ERROR: Parsed JSON is not a list.")
        return []
        
    evaluations = []
    
    for idx, item in enumerate(data):
        if not isinstance(item, list) or len(item) < 11:
            print(f"Warning: Skipping item {idx} - expected a list of at least 11 elements (got {type(item).__name__ if not isinstance(item, list) else len(item)}).")
            continue
            
        try:
            # Parse actors from item[11] if present (AI-provided), else empty list (fallback handled later)
            ai_actors = []
            if len(item) >= 12 and isinstance(item[11], list):
                ai_actors = [str(a).strip() for a in item[11] if isinstance(a, str) and str(a).strip()]

            # Parse optional macro-context fields with fallback to None/empty
            macro_event = str(item[12]).strip() if len(item) >= 13 and item[12] is not None else ""
            macro_claim_u = float(item[13]) if len(item) >= 14 and item[13] is not None else None
            macro_claim_psi = float(item[14]) if len(item) >= 15 and item[14] is not None else None
            macro_real_u = float(item[15]) if len(item) >= 16 and item[15] is not None else None
            macro_real_psi = float(item[16]) if len(item) >= 17 and item[16] is not None else None

            story = {
                "thinking": str(item[0]).strip(),
                "id": str(item[1]).strip(),
                "subject": str(item[2]).strip(),
                "link": str(item[3]).strip(),
                "target_url": str(item[4]).strip(),
                "claim_u": float(item[5]),
                "claim_psi": float(item[6]),
                "real_u": float(item[7]),
                "real_psi": float(item[8]),
                "mode": str(item[9]).strip(),
                "posts": [str(p) for p in item[10]],
                "actors": ai_actors,
                "macro_event": macro_event,
                "macro_claim_u": macro_claim_u,
                "macro_claim_psi": macro_claim_psi,
                "macro_real_u": macro_real_u,
                "macro_real_psi": macro_real_psi,
                "status": "COMPLETED DRY RUN"
            }

            # Parse optional integrity and uncertainty fields (items 17 to 24)
            if len(item) >= 18 and item[17] is not None:
                story["claim_rnet"] = float(item[17])
            if len(item) >= 19 and item[18] is not None:
                story["real_rnet"] = float(item[18])
            if len(item) >= 20 and item[19] is not None:
                story["claim_z"] = int(item[19])
            if len(item) >= 21 and item[20] is not None:
                story["real_z"] = int(item[20])
            if len(item) >= 22 and isinstance(item[21], list):
                story["claim_z_profile"] = list(item[21])
            if len(item) >= 23 and isinstance(item[22], list):
                story["real_z_profile"] = list(item[22])
            if len(item) >= 24 and item[23] is not None:
                story["claim_integrity"] = str(item[23]).strip()
            if len(item) >= 25 and item[24] is not None:
                story["real_integrity"] = str(item[24]).strip()
            evaluations.append(story)
        except Exception as e:
            print(f"Warning: Failed to parse item {idx}: {e}")
            continue
            
    return evaluations

# --- 4. SAVE TO DARKROOM ---
def extract_topic_from_posts(posts):
    if not posts or not isinstance(posts, list) or len(posts) == 0:
        return None
    first_post = posts[0]
    import re
    # Find all hashtags
    tags = re.findall(r"#(\w+)", first_post)
    for tag in tags:
        if tag.lower() not in ["aletheia", "claim", "reality", "verdict"]:
            return tag
    return None

# --- 4. SAVE TO DARKROOM ---
def process_evaluations(evaluations, category="general", topic=None, compact=False):
    """Write evaluated story configs to stories/darkroom/ for graph generation and promotion by rebuild_registries."""
    darkroom_dir = os.path.join(script_dir, "stories", "darkroom")
    os.makedirs(darkroom_dir, exist_ok=True)
    success_count = 0

    for story in evaluations:
        try:
            slug = story.get("id") or story.get("subject", "story").lower().replace(" ", "_").replace("/", "_")
            for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
                slug = slug.replace(char, '')
            story["id"] = slug
            story["status"] = "COMPLETED DRY RUN"
            if compact:
                story["compact"] = "single" if compact == "single" else True

            # Actors: AI-provided takes priority; fall back to deterministic extraction if empty
            if not story.get("actors"):
                story["actors"] = extract_actors(story.get("subject", ""))
            if story["actors"]:
                print(f"  actors: {story['actors']}")
            # Normalise category: store as a comma-joined string so it's JSON-friendly
            cats = [c.strip().lower() for c in (category or "general").split(",") if c.strip()] if isinstance(category, str) else (category or ["general"])
            story.setdefault("category", ",".join(cats) if len(cats) > 1 else (cats[0] if cats else "general"))
            
            # Topic: store explicitly or extract from hashtags in the first post
            t = topic
            if not t:
                t = extract_topic_from_posts(story.get("posts", []))
            if t:
                story.setdefault("topic", t.strip())

            story.setdefault("event", "")

            # Post count validation
            posts = story.get("posts", [])
            if len(posts) != 13:
                print(f"ERROR: Story '{story.get('subject')}' has {len(posts)} posts (expected 13). Skipping.")
                continue

            # Character limit warnings
            violations = [(i, len(p)) for i, p in enumerate(posts) if len(p) > 299]
            if violations:
                print(f"WARNING: '{story.get('subject')}' has char violations at posts {violations}")

            # Write to darkroom — rebuild_registries will generate the graph and promote it
            filename = f"factcheck_{slug}.json"
            filepath = os.path.join(darkroom_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([story], f, indent=2, ensure_ascii=False)

            print(f"  Staged to darkroom: {filename}")
            success_count += 1
        except Exception as e:
            print(f"ERROR: Failed to stage story '{story.get('subject')}': {e}")

    return success_count

def main():
    def int_or_default(default_val):
        def converter(val):
            if not val or not val.strip():
                return default_val
            try:
                return int(val)
            except ValueError:
                raise argparse.ArgumentTypeError(f"Invalid integer value: '{val}'")
        return converter

    parser = argparse.ArgumentParser(description="Google AI Studio One-Shot Batch Evaluator")
    parser.add_argument("--son", action="store_true", help="Use the 6-Attractor SON convergence model and formatting instructions")
    parser.add_argument("--compact", action="store_true", help="Enable compact posting mode formatting (lifting character limits on posts 4+ in API responses)")
    parser.add_argument("--compact-single", action="store_true", help="Enable compact single-post mode formatting (lifting character limits on posts 4+ and tagging story as single-post compact)")
    parser.add_argument("--search", action="store_true", help="Enable Google Search Grounding to fact-check claims (default: False)")
    parser.add_argument("--rss", type=int_or_default(0), default=5, help="Number of RSS stories to harvest (default: 5)")
    parser.add_argument("--bsky", type=int_or_default(0), default=15, help="Number of Bluesky stories to harvest (default: 15)")
    parser.add_argument("--model", type=str, default="gemini-3.5-flash", help="Generative model to use (default: gemini-3.5-flash)")
    parser.add_argument("--context", type=str, default=None, help="Additional context/background knowledge to send to the evaluator model")
    parser.add_argument("--model-sequence", type=str, default=None, help="Comma-separated list of models to try in sequence (overriding default fallbacks)")
    parser.add_argument("--chunk-size", type=int_or_default(1), default=1, help="Number of stories to process per API call (default: 1)")
    parser.add_argument("--category", type=str, default="all", help="Category (or comma-separated categories) of news to harvest (default: all). E.g. 'politics,tech'")
    parser.add_argument("--topic", type=str, default=None, help="Specific topic query to filter/search for (e.g. 'Ukraine', 'Trump')")
    parser.add_argument("--banned-topic", type=str, default="gardening,sport,sports,football,soccer,basketball,baseball,tennis,golf,olympics,nfl,nba,movie,movies,music,song,album,concert,gaming,actor,actress,hollywood,cinema,box office,festival,nintendo,playstation,xbox,tv show,travel,tourism,cruise,vacation,flight,hotel", help="Comma-separated topics/keywords to exclude from harvesting (default: sports, entertainment, and travel keywords)")
    parser.add_argument("--roundup", action="store_true", help="After evaluation, run consolidate_roundups to group overlapping stories into roundup threads (default: False)")
    parser.add_argument("--prefer", type=str, default="", help=(
        "Preferred outlets to prioritize. Comma-separated list of domains or numbers:\n"
        "1: Bloomberg, 2: NY Times, 3: The Saturday Paper, 4: Reuters, 5: BBC News,\n"
        "6: SMH, 7: TechCrunch, 8: Washington Post, 9: NPR.\n"
        "E.g., --prefer '1,2,5,theguardian.com'"
    ))
    parser.add_argument("--enabled-feeds", type=str, default=None, help="Comma-separated feed names (or URLs) to enable for harvesting.")
    args = parser.parse_args()
    
    compact_val = False
    if args.compact_single:
        compact_val = "single"
    elif args.compact:
        compact_val = True
    
    global PREFERRED_OUTLET_DOMAINS
    if args.prefer:
        new_prefs = []
        if args.prefer.strip().lower() in ("default", "all"):
            for token, domains in COMMON_OUTLETS.items():
                new_prefs.extend(domains)
        else:
            for token in args.prefer.split(","):
                token = token.strip().lower()
                if not token:
                    continue
                if token in COMMON_OUTLETS:
                    new_prefs.extend(COMMON_OUTLETS[token])
                else:
                    new_prefs.append(token)
        PREFERRED_OUTLET_DOMAINS = new_prefs
        
    print("=" * 80)
    print("GOOGLE AI STUDIO ONE-SHOT BATCH EVALUATOR")
    print("=" * 80)
    
    import subprocess
    
    harvest_script = os.path.join(script_dir, "harvest_candidates.py")
    cmd = [
        sys.executable,
        harvest_script,
        "--rss", str(args.rss),
        "--bsky", str(args.bsky)
    ]
    if args.prefer:
        cmd.extend(["--prefer", args.prefer])
    if args.category:
        cmd.extend(["--category", args.category])
    if args.topic:
        cmd.extend(["--topic", args.topic])
    if args.banned_topic:
        cmd.extend(["--banned-topic", args.banned_topic])
    if args.enabled_feeds:
        cmd.extend(["--enabled-feeds", args.enabled_feeds])
        
    print(f"Executing: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Candidate harvesting script failed with exit code {e.returncode}")
        sys.exit(1)
        
    scratch_candidates_path = os.path.join(script_dir, "harvested_candidates.json")
    if not os.path.exists(scratch_candidates_path):
        print(f"Error: {scratch_candidates_path} not found. Harvesting failed to generate output.")
        sys.exit(1)
        
    try:
        with open(scratch_candidates_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)
    except Exception as e:
        print(f"Error loading candidates from {scratch_candidates_path}: {e}")
        sys.exit(1)
        
    if not candidates:
        print("\nNo candidates found or remaining. Exiting.")
        sys.exit(0)
        
    print(f"\nLoaded {len(candidates)} total candidates for evaluation.")
    
    genai_client = get_gemini_client()
    agnes_api_key = os.environ.get("AGNES_API_KEY")
    
    # Calculate simple token savings metrics
    if args.son:
        convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son_lite.md")
        formatting_path = os.path.join(script_dir, "instructions", "thread_formatting_son.md")
    else:
        convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_lite.md")
        formatting_path = os.path.join(script_dir, "instructions", "thread_formatting.md")
    with open(convergence_path, "r", encoding="utf-8") as f:
        raw_ct = len(f.read())
    with open(formatting_path, "r", encoding="utf-8") as f:
        raw_tf = len(f.read())
    
    min_ct = len(minify_markdown(open(convergence_path, "r", encoding="utf-8").read()))
    min_tf = len(minify_markdown(open(formatting_path, "r", encoding="utf-8").read()))
    
    raw_total_chars = raw_ct + raw_tf
    min_total_chars = min_ct + min_tf
    percent_saved = (1.0 - (min_total_chars / raw_total_chars)) * 100
    
    print(f"\n--- PROMPT TOKENS MINIFICATION ---")
    print(f"Raw instructions size:      {raw_total_chars} characters (~{int(raw_total_chars/4)} tokens)")
    print(f"Minified instructions size: {min_total_chars} characters (~{int(min_total_chars/4)} tokens)")
    print(f"Total instructions token budget saved: {percent_saved:.1f}%")
    print(f"----------------------------------\n")
    
    # Process candidates in chunks, with retry for any the model skipped
    chunk_size = args.chunk_size
    all_evaluations = []
    MAX_RETRIES_PER_CHUNK = 2

    for i in range(0, len(candidates), chunk_size):
        chunk = candidates[i:i + chunk_size]
        total_chunks = (len(candidates) + chunk_size - 1) // chunk_size
        print(f"\nEvaluating chunk {i // chunk_size + 1}/{total_chunks} ({len(chunk)} candidates)...")

        remaining = list(chunk)  # candidates not yet evaluated
        chunk_evals = []

        for attempt in range(1, MAX_RETRIES_PER_CHUNK + 1):
            if not remaining:
                break
            if attempt > 1:
                print(f"  Retry {attempt - 1}: {len(remaining)} candidate(s) not returned — re-firing...")
                time.sleep(3)
            try:
                model_seq = None
                if args.model_sequence:
                    model_seq = [m.strip() for m in args.model_sequence.split(",") if m.strip()]
                raw_text, grounding_urls = run_one_shot_evaluations(
                    genai_client, remaining, args.model, agnes_api_key=agnes_api_key, 
                    use_son=args.son, use_search=args.search, 
                    extra_context=args.context, model_sequence=model_seq,
                    compact=compact_val
                )
                parsed = transpose_flat_to_json(raw_text)
                
                # If search was actually used, append 🌐 and link grounding URL
                if grounding_urls:
                    print(f"  Google Search grounding detected with {len(grounding_urls)} source(s).")
                    primary_url = grounding_urls[0]
                    # Strip tracking parameters to save character space
                    if "?" in primary_url:
                        primary_url = primary_url.split("?")[0]
                    primary_url = primary_url.strip()
                    
                    for item in parsed:
                        if len(item) > 10 and isinstance(item[10], list) and len(item[10]) > 0:
                            # 1. Append 🌐 emoji to first post
                            first_post = item[10][0]
                            if "🌐" not in first_post:
                                item[10][0] = first_post.rstrip() + " 🌐"
                            
                            # 2. Append the grounding URL to a post without attachments.
                            # Preferred target is post 11 (Alethekanon, index 10).
                            # Fallback sequence: post 3 (Reality, index 2), post 12 (Awwthekanon, index 11), post 13 (Brothekanon, index 12), post 5 (Context, index 4).
                            preferred_indices = [10, 2, 11, 12, 4]
                            appended = False
                            url_suffix = f"\n\nSource: {primary_url}"
                            
                            for idx in preferred_indices:
                                if idx < len(item[10]):
                                    current_text = item[10][idx]
                                    if len(current_text) + len(url_suffix) <= 290:
                                        item[10][idx] = current_text + url_suffix
                                        appended = True
                                        print(f"    Appended grounding source URL to post {idx+1}")
                                        break
                                        
                            if not appended:
                                # Fallback: search for the shortest post (excluding post 1) to fit it within 299 character limit
                                shortest_idx = -1
                                shortest_len = 9999
                                for idx in range(1, len(item[10])):
                                    current_text = item[10][idx]
                                    if len(current_text) < shortest_len:
                                        shortest_len = len(current_text)
                                        shortest_idx = idx
                                        
                                if shortest_idx != -1:
                                    current_text = item[10][shortest_idx]
                                    if len(current_text) + len(url_suffix) <= 299:
                                        item[10][shortest_idx] = current_text + url_suffix
                                        print(f"    Appended grounding source URL to shortest post {shortest_idx+1} (backup)")

                chunk_evals.extend(parsed)

                # Find which candidates still haven't been evaluated (match by URL)
                evaluated_urls = {normalize_url(e.get("link", "")) for e in chunk_evals}
                remaining = [c for c in remaining if normalize_url(c.get("url", "")) not in evaluated_urls]

                print(f"  Got {len(parsed)} row(s). {len(remaining)} candidate(s) still missing.")
            except Exception as pe:
                print(f"  Error on attempt {attempt}: {pe}")

        if remaining:
            print(f"  WARNING: {len(remaining)} candidate(s) could not be evaluated after {MAX_RETRIES_PER_CHUNK} attempt(s). Skipping.")

        if chunk_evals:
            chunk_success = process_evaluations(chunk_evals, category=args.category, topic=args.topic, compact=compact_val)
            print(f"  Processed {chunk_success}/{len(chunk_evals)} evaluations from chunk to darkroom.")
            print("  Promoting and generating graphs immediately...")
            rebuild_registries_selector(args.son)
            print("  Registries successfully rebuilt for this chunk.")
            
            # Deduct successfully processed candidates from the queue file
            queue_file_path = os.path.join(script_dir, "harvested_candidates.json")
            if os.path.exists(queue_file_path):
                try:
                    with open(queue_file_path, 'r', encoding='utf-8') as f:
                        q_data = json.load(f)
                    if isinstance(q_data, list):
                        # Filter out evaluated candidates
                        trimmed_q = [c for c in q_data if normalize_url(c.get("url", "")) not in evaluated_urls]
                        with open(queue_file_path, 'w', encoding='utf-8') as f:
                            json.dump(trimmed_q, f, indent=2, ensure_ascii=False)
                        print(f"  Deducted {len(q_data) - len(trimmed_q)} evaluated candidates from queue. Remaining: {len(trimmed_q)}")
                except Exception as qe:
                    print(f"  Warning: Failed to update queue file: {qe}")
        
        all_evaluations.extend(chunk_evals)
            
    print(f"\nReceived {len(all_evaluations)} total evaluations across all chunks.")
    if not all_evaluations:
        print("ERROR: No evaluations returned across all chunks. Exiting.")
        sys.exit(1)

    # ── Post-batch: roundup consolidation ────────────────────────────────────
    if args.roundup:
        print("\n" + "=" * 80)
        print("ROUNDUP CONSOLIDATION PASS")
        print("=" * 80)
        try:
            from consolidate_roundups import consolidate
            n_roundups = consolidate(
                dry_run      = False,
                min_outlets  = 2,
                max_outlets  = 4,
                actor_win    = 72,
                keyword_win  = 48,
                genai_client = genai_client,
                model_name   = args.model,
                agnes_api_key= agnes_api_key,
            )
            if n_roundups:
                print(f"  Created {n_roundups} roundup(s). Rebuilding registries...")
                rebuild_registries_selector(args.son)
            else:
                print("  No roundup groups found — all stories post individually.")
        except Exception as re_err:
            print(f"  WARNING: Roundup consolidation failed: {re_err}")

    print("\nOne-Shot Batch Evaluation Pipeline Completed Successfully!")

if __name__ == "__main__":
    main()
