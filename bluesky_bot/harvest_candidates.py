import os
import sys
import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import argparse
import datetime
import email.utils
from dotenv import load_dotenv
from atproto import Client, IdResolver
import requests
from html.parser import HTMLParser

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

script_dir = os.path.dirname(os.path.abspath(__file__))  # e:\Vector Field Theory\VFT Docs\bluesky_bot
root_dir = os.path.dirname(script_dir)                  # e:\Vector Field Theory\VFT Docs
bot_dir = script_dir                                    # e:\Vector Field Theory\VFT Docs\bluesky_bot
env_path = os.path.join(bot_dir, '.env')
load_dotenv(env_path)

# --- ARGUMENT PARSING ---
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

parser = argparse.ArgumentParser(description="Harvest news candidates from RSS and Bluesky feeds.")
parser.add_argument("--rss", "--rss-target", dest="rss_target", type=int, default=0, help="Target count for RSS feeds (default: 0)")
parser.add_argument("--bsky", "--bsky-target", dest="bsky_target", type=int, default=40, help="Target count for Bluesky feeds (default: 40)")
parser.add_argument("--prefer", type=str, default="", help=(
    "Preferred outlets to prioritize. Comma-separated list of domains or numbers:\n"
    "1: Bloomberg, 2: NY Times, 3: The Saturday Paper, 4: Reuters, 5: BBC News,\n"
    "6: SMH, 7: TechCrunch, 8: Washington Post, 9: NPR.\n"
    "E.g., --prefer '1,2,5,theguardian.com'"
))
parser.add_argument("--category", type=str, default="all", help="Category (or comma-separated categories) of news to harvest (default: all)")
parser.add_argument("--topic", type=str, default=None, help="Specific topic query to filter/search for (e.g. 'Ukraine', 'Trump')")
parser.add_argument("--banned-topic", type=str, default="gardening,sport,sports,football,soccer,basketball,baseball,tennis,golf,olympics,nfl,nba,movie,movies,music,song,album,concert,gaming,actor,actress,hollywood,cinema,box office,festival,nintendo,playstation,xbox,tv show,travel,tourism,cruise,vacation,flight,hotel", help="Comma-separated topics/keywords to exclude from harvesting")
parser.add_argument("--enabled-feeds", type=str, default=None, help="Comma-separated feed names (or URLs) to enable for harvesting")

args = parser.parse_args()

TARGET_RSS = args.rss_target
TARGET_BSKY = args.bsky_target

# Parse preferred outlets from arguments if provided
PREFERRED_OUTLET_DOMAINS = []
if args.prefer:
    if args.prefer.strip().lower() in ("default", "all"):
        for token, domains in COMMON_OUTLETS.items():
            PREFERRED_OUTLET_DOMAINS.extend(domains)
    else:
        for token in args.prefer.split(","):
            token = token.strip().lower()
            if not token:
                continue
            if token in COMMON_OUTLETS:
                PREFERRED_OUTLET_DOMAINS.extend(COMMON_OUTLETS[token])
            else:
                PREFERRED_OUTLET_DOMAINS.append(token)

# Domains that are never a news article (social media, shorteners-to-self, junk, crypto, adult).
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

# Domains that consistently fail raw scraping due to paywalls, cloudflare blocks, etc.
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
SCRAPING_WHITELIST = {
    'bbc.com', 'bbc.co.uk', 'bbci.co.uk',
    'abc.net.au',
    'thesaturdaypaper.com.au', 'saturdaypaper.com.au',
    'smh.com.au',
    'techcrunch.com',
    'npr.org',
    'goodnewsnetwork.org',
    'positive.news',
    'optimistdaily.com',
    'squirrel-news.net'
}

# Category filter keywords
CATEGORY_KEYWORDS = {
    "tech": ["tech", "technology", "software", "hardware", "chip", "artificial intelligence", "ai ", "startup", "apple", "google", "microsoft", "nvidia", "cyber", "crypto", "telecom"],
    "business": ["business", "economy", "market", "inflation", "stock", "trade", "profit", "revenue", "export", "import", "tariff", "bank", "finance", "merger", "acquisition"],
    "politics": ["politics", "government", "parliament", "senate", "congress", "election", "senator", "president", "prime minister", "sanctions", "treaty", "legislation", "bill", "democrat", "republican", "minister", "policy", "veto"],
    "science": ["science", "space", "nasa", "research", "study", "scientist", "discover", "physics", "biology", "chemistry", "climate", "medicine", "planet", "vaccine"],
    "world": ["world", "international", "global", "foreign", "un ", "united nations", "treaty"],
    "uplifting": ["uplifting", "good news", "optimism", "happy news", "inspiring", "feel good", "hopeful", "positive news"]
}

def is_domain_whitelisted(domain):
    d = domain.strip().lower()
    return any(d == wl or d.endswith('.' + wl) for wl in SCRAPING_WHITELIST)

def load_dynamic_banned_domains():
    global DYNAMIC_BANNED_DOMAINS
    path = os.path.join(bot_dir, "unscrapable_domains.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    DYNAMIC_BANNED_DOMAINS.update(data)
        except Exception as e:
            print(f"Warning: Failed to load dynamic banned domains: {e}")

def save_dynamic_banned_domains():
    path = os.path.join(bot_dir, "unscrapable_domains.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sorted(list(DYNAMIC_BANNED_DOMAINS)), f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Failed to save dynamic banned domains: {e}")

def is_news_url(url):
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
    if any(host == bad or host.endswith('.' + bad) for bad in NON_NEWS_DOMAINS):
        return False
    if any(host == bad or host.endswith('.' + bad) for bad in DYNAMIC_BANNED_DOMAINS):
        return False
    return True

def is_banned(text, url, banned_keywords):
    if not banned_keywords:
        return False
    text_lower = text.lower()
    url_lower = url.lower() if url else ""
    for bk in banned_keywords:
        if bk in text_lower or (url_lower and bk in url_lower):
            return True
        if " " in bk:
            variants = [bk.replace(" ", "-"), bk.replace(" ", "_"), bk.replace(" ", "")]
            for var in variants:
                if var in text_lower or (url_lower and var in url_lower):
                    return True
    return False

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

def matches_category(text, url, feed_categories, requested_categories):
    if "all" in requested_categories or "general" in requested_categories:
        return True
    for cat in requested_categories:
        if cat in feed_categories:
            return True
    text_lower = text.lower()
    for cat in requested_categories:
        if cat in CATEGORY_KEYWORDS:
            for kw in CATEGORY_KEYWORDS[cat]:
                if kw in text_lower:
                    return True
    return False

def normalize_url(url):
    if not url:
        return ""
    url = url.strip()
    if "?" in url:
        url = url.split("?")[0]
    if "#" in url:
        url = url.split("#")[0]
    return url.lower().strip()

load_dynamic_banned_domains()

# --- 0. LOAD HISTORICAL EVALUATIONS (PREVENT DUPLICATE JUDGEMENTS) ---
print("Loading historical evaluations database to prevent duplicate judgements...")
seen_historical_urls = set()
seen_historical_ids = set()
seen_historical_subjects = set()
historical_domain_counts = {}

# Load persistent harvested history file
harvested_history_path = os.path.join(bot_dir, 'harvested_history.json')
if os.path.exists(harvested_history_path):
    try:
        with open(harvested_history_path, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
            if isinstance(history_data, list):
                for url in history_data:
                    seen_historical_urls.add(normalize_url(url))
                print(f"Loaded {len(history_data)} URLs from persistent harvested history.")
    except Exception as e:
        print(f"Warning: Failed to load harvested history: {e}")

seen_evaluated_urls = set()

bot_stories_dir = os.path.join(bot_dir, 'stories')
scan_dirs = [
    bot_stories_dir,
    os.path.join(bot_stories_dir, 'live'),
    os.path.join(bot_stories_dir, 'darkroom')
]
for scan_dir in scan_dirs:
    if os.path.exists(scan_dir):
        try:
            story_files = [f for f in os.listdir(scan_dir) if f.startswith('factcheck_') and f.endswith('.json')]
            for sf in story_files:
                filepath = os.path.join(scan_dir, sf)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                config = data[0] if isinstance(data, list) else data
                
                url = config.get("link") or config.get("target_url")
                if url:
                    url_clean = normalize_url(url)
                    seen_historical_urls.add(url_clean)
                    seen_evaluated_urls.add(url_clean)
                    try:
                        host = urllib.parse.urlparse(url_clean).hostname
                        if host:
                            host = host.replace("www.", "")
                            historical_domain_counts[host] = historical_domain_counts.get(host, 0) + 1
                    except Exception:
                        pass
                    
                story_id = config.get("id")
                if story_id:
                    seen_historical_ids.add(story_id.strip().lower())
                subject = config.get("subject")
                if subject:
                    seen_historical_subjects.add(subject.strip().lower())
        except Exception as e:
            print(f"Warning: Failed to load historical evaluations from {scan_dir}: {e}")

print(f"Loaded {len(seen_historical_urls)} historical URLs and {len(seen_historical_ids)} historical story IDs.")

# --- 0.5 LOAD EXISTING PENDING QUEUE ---
existing_queue = []
existing_queue_urls = set()
existing_queue_ids = set()
existing_queue_subjects = set()

queue_path = os.path.join(bot_dir, 'harvested_candidates.json')
if os.path.exists(queue_path):
    try:
        with open(queue_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for c in data:
                    url = c.get("url")
                    if url and normalize_url(url) in seen_evaluated_urls:
                        continue
                    existing_queue.append(c)
                    if url:
                        existing_queue_urls.add(normalize_url(url))
                    
                    text = c.get("text", "")
                    if text:
                        if "Stated Claim / Post Context:\n" in text:
                            claim_part = text.split("\n\nActual Article Body:\n")[0]
                            claim_part = claim_part.replace("Stated Claim / Post Context:\n", "")
                            subj = claim_part[:30]
                            title = claim_part.strip().lower()
                        else:
                            subj = text[:30]
                            title = text.split("\n\n")[0].strip().lower()
                        existing_queue_ids.add(subj.lower().replace(" ", "_").replace("/", "_"))
                        existing_queue_subjects.add(title)
                        
        print(f"Loaded {len(existing_queue)} existing pending candidates from queue.")
    except Exception as e:
        print(f"Warning: Failed to load existing queue: {e}")

existing_rss_count = sum(1 for c in existing_queue if "bsky.app" not in c.get("url", "") and "bsky.app" not in c.get("target_url", ""))
existing_bsky_count = len(existing_queue) - existing_rss_count

# Adjust targets based on existing queue size to top-up
# Prioritize clearing the existing queue first: if queue is non-empty, bypass scraping new ones.
if len(existing_queue) > 0:
    print(f"Queue is not empty ({len(existing_queue)} items). Bypassing new harvesting to clear queue first.")
    TARGET_RSS = 0
    TARGET_BSKY = 0
else:
    TARGET_RSS = max(0, TARGET_RSS - existing_rss_count)
    TARGET_BSKY = max(0, TARGET_BSKY - existing_bsky_count)
print(f"Top-up targets: RSS={TARGET_RSS} (needed), Bluesky={TARGET_BSKY} (needed)")

# --- 1. DYNAMIC STORY-LEVEL DE-DUPLICATION HEURISTIC ---
# Deduplication at harvest is intentionally narrow: only blocks the exact same article
# from being evaluated twice (same URL, same title, same slug). Topic-level grouping
# of different outlets covering the same event is handled downstream by consolidate_roundups.py.
seen_stories_keywords_list = []

def is_duplicate_story(text, url, check_batch=True):
    text_lower = text.lower()
    url_lower = normalize_url(url)

    if url_lower in seen_historical_urls:
        print(f"  -> Historical duplicate URL detected! Skipping: {url}")
        return True

    # Title deduplication: split text body (starts with the title) to check duplicate subjects
    title = text.split("\n\n")[0].strip().lower()
    if "stated claim / post context:\n" in title:
        title = title.replace("stated claim / post context:\n", "").strip()

    if title in seen_historical_subjects:
        print(f"  -> Historical duplicate subject/title detected! Skipping: {title}")
        return True
    if title in existing_queue_subjects:
        print(f"  -> Duplicate subject/title in pending queue detected! Skipping: {title}")
        return True

    subject_approx = text[:30].lower().replace(" ", "_").replace("/", "_")
    if subject_approx in seen_historical_ids:
        print(f"  -> Historical duplicate Story ID detected! Skipping: {subject_approx}")
        return True

    if url_lower in existing_queue_urls:
        print(f"  -> Duplicate in pending queue detected! Skipping: {url}")
        return True
    if subject_approx in existing_queue_ids:
        print(f"  -> Duplicate Story ID in pending queue detected! Skipping: {subject_approx}")
        return True

    # Mark as seen in this run to prevent the same story from different feeds being queued twice
    seen_historical_urls.add(url_lower)
    seen_historical_subjects.add(title)

    return False

# --- 2. EXTRACT EXTERNAL ARTICLE URL FROM BLUESKY POST ---
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
        
    domain_match = re.search(r'\b([a-z0-9-]+\.[a-z]{2,}/[^\s]+)', text, re.IGNORECASE)
    if domain_match:
        return "https://" + domain_match.group(1)
        
    return None

# --- PREFERRED OUTLETS CONFIGURATION ---
def get_historical_count(url):
    if not url:
        return 0
    try:
        host = urllib.parse.urlparse(url).hostname
        if host:
            host = host.replace("www.", "")
            return historical_domain_counts.get(host, 0)
    except Exception:
        pass
    return 0

def is_preferred_outlet(url):
    if not url or not PREFERRED_OUTLET_DOMAINS:
        return False
    u = url.strip().lower()
    try:
        host = urllib.parse.urlparse(u).hostname or ""
    except Exception:
        host = ""
    if not host:
        host = u
    return any(host == pref or host.endswith('.' + pref) for pref in PREFERRED_OUTLET_DOMAINS)

def get_sort_key(c):
    count = get_historical_count(c.get("url"))
    if PREFERRED_OUTLET_DOMAINS:
        pref = 0 if is_preferred_outlet(c.get("url")) else 1
        return (pref, count)
    return (0, count)

# --- 3. HARVEST FROM RSS FEEDS ---
print(f"\nHarvesting normal news from RSS feeds (Target: {TARGET_RSS})...")
rss_feeds = [
    # General & World News
    {"name": "ABC News Australia", "url": "https://www.abc.net.au/news/feed/2942460/rss.xml", "categories": ["general", "world"]},
    {"name": "9News Australia", "url": "https://www.9news.com.au/rss", "categories": ["general"]},
    {"name": "SBS News", "url": "https://www.sbs.com.au/news/feed", "categories": ["general", "world"]},
    {"name": "Sydney Morning Herald", "url": "https://www.smh.com.au/rss/feed.xml", "categories": ["general"]},
    {"name": "Perth Now", "url": "https://www.perthnow.com.au/feed", "categories": ["general"]},
    {"name": "The Age", "url": "https://www.theage.com.au/rss/feed.xml", "categories": ["general"]},
    {"name": "Brisbane Times", "url": "https://www.brisbanetimes.com.au/rss/feed.xml", "categories": ["general"]},
    {"name": "WA Today", "url": "https://www.watoday.com.au/rss/feed.xml", "categories": ["general"]},
    {"name": "Canberra Times", "url": "https://www.canberratimes.com.au/rss.xml", "categories": ["general"]},
    {"name": "BBC News", "url": "http://feeds.bbci.co.uk/news/rss.xml", "categories": ["general", "world"]},
    {"name": "NYT Home", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "categories": ["general", "world"]},
    {"name": "The Guardian World", "url": "https://www.theguardian.com/world/rss", "categories": ["world", "general"]},
    {"name": "The Guardian UK", "url": "https://www.theguardian.com/uk/rss", "categories": ["general"]},
    {"name": "NPR News", "url": "https://feeds.npr.org/1001/rss.xml", "categories": ["general", "world"]},
    {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "categories": ["world", "general"]},
    {"name": "DW News World", "url": "https://rss.dw.com/xml/rss-en-all", "categories": ["world", "general"]},
    {"name": "France 24", "url": "https://www.france24.com/en/rss", "categories": ["world", "general"]},
    {"name": "CBC News", "url": "https://rss.cbc.ca/lineup/topstories.xml", "categories": ["world", "general"]},
    {"name": "UPI News", "url": "https://rss.upi.com/news/news.rss", "categories": ["world", "general"]},
    {"name": "Google News World", "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en", "categories": ["world", "general"]},
    {"name": "Google News Australia", "url": "https://news.google.com/rss?hl=en-AU&gl=AU&ceid=AU:en", "categories": ["general"]},

    # Tech
    {"name": "BBC Tech", "url": "http://feeds.bbci.co.uk/news/technology/rss.xml", "categories": ["tech"]},
    {"name": "NYT Tech", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "categories": ["tech"]},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "categories": ["tech"]},
    {"name": "The Guardian Tech", "url": "https://www.theguardian.com/technology/rss", "categories": ["tech"]},

    # Business
    {"name": "BBC Business", "url": "http://feeds.bbci.co.uk/news/business/rss.xml", "categories": ["business"]},
    {"name": "NYT Business", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "categories": ["business"]},
    {"name": "CNBC Business", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147", "categories": ["business"]},
    {"name": "The Guardian Business", "url": "https://www.theguardian.com/business/rss", "categories": ["business"]},
    {"name": "DW Business", "url": "https://rss.dw.com/xml/rss-en-bus", "categories": ["business"]},

    # Politics
    {"name": "BBC Politics", "url": "http://feeds.bbci.co.uk/news/politics/rss.xml", "categories": ["politics"]},
    {"name": "NYT Politics", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "categories": ["politics"]},
    {"name": "NPR Politics", "url": "https://feeds.npr.org/1014/rss.xml", "categories": ["politics"]},
    {"name": "The Guardian Politics", "url": "https://www.theguardian.com/politics/rss", "categories": ["politics"]},

    # Science
    {"name": "BBC Science", "url": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml", "categories": ["science"]},
    {"name": "NYT Science", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml", "categories": ["science"]},
    {"name": "The Guardian Science", "url": "https://www.theguardian.com/science/rss", "categories": ["science"]},
    {"name": "DW Science", "url": "https://rss.dw.com/xml/rss-en-science", "categories": ["science"]},

    # Uplifting / Good News
    {"name": "Good News Network", "url": "https://www.goodnewsnetwork.org/feed/", "categories": ["uplifting", "general"]},
    {"name": "Positive News", "url": "https://www.positive.news/feed/", "categories": ["uplifting"]},
    {"name": "Optimist Daily", "url": "https://www.optimistdaily.com/feed/", "categories": ["uplifting"]},
    {"name": "Squirrel News", "url": "https://squirrel-news.net/feed/", "categories": ["uplifting"]},
    {"name": "ABC News Australia Good News", "url": "https://www.abc.net.au/news/feed/101830674/rss.xml", "categories": ["uplifting", "general"]},
    {"name": "HuffPost Good News", "url": "https://www.huffpost.com/section/good-news/feed", "categories": ["uplifting", "general"]}
]

if getattr(args, 'enabled_feeds', None):
    enabled_names = [f.strip().lower() for f in args.enabled_feeds.split(",") if f.strip()]
    filtered_feeds = []
    for feed in rss_feeds:
        if feed["name"].lower() in enabled_names or feed["url"].lower() in enabled_names:
            filtered_feeds.append(feed)
    rss_feeds = filtered_feeds

rss_candidates = []

requested_categories = [c.strip().lower() for c in (args.category or "all").split(",") if c.strip()]
keywords = [k.strip().lower() for k in args.topic.split(",") if k.strip()] if args.topic else []
banned_keywords = [k.strip().lower() for k in args.banned_topic.split(",") if k.strip()] if args.banned_topic else []

if TARGET_RSS > 0:
    for feed in rss_feeds:
        print(f"Fetching from {feed['name']} RSS feed: {feed['url']}...")
        req = urllib.request.Request(feed['url'], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
            root = ET.fromstring(content)
            items = root.findall('.//item')
            print(f"Found {len(items)} raw items in {feed['name']}.")
            
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
                if normalize_url(link_text) in seen_historical_urls:
                    continue
                
                # Filter by Category
                if not matches_category(text_body, link_text, feed.get("categories", []), requested_categories):
                    continue
                
                # Filter by Topic
                if keywords:
                    if not any(k in title_text.lower() or k in desc_cleaned.lower() for k in keywords):
                        continue
                        
                # Banned topic filtering
                if is_banned(title_text + "\n" + desc_cleaned, link_text, banned_keywords):
                    continue
                
                if is_duplicate_story(text_body, link_text):
                    continue
                    
                # Parse publication date
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
                                    pub_date = email.utils.parsedate_to_datetime(val)
                                if pub_date.tzinfo is None:
                                    pub_date = pub_date.replace(tzinfo=datetime.timezone.utc)
                                break
                            except Exception:
                                pass
    
                rss_candidates.append({
                    "url": link_text,
                    "target_url": "",
                    "mode": "root",
                    "text": text_body,
                    "subject": title_text[:30].strip() + "...",
                    "pub_date": pub_date
                })
                
        except Exception as e:
            print(f"Warning: Failed to fetch {feed['name']} RSS: {e}")
else:
    print("RSS target already satisfied. Skipping RSS harvesting.")

# Sort all RSS candidates by pub_date descending (newest first)
rss_candidates = sorted(
    rss_candidates,
    key=lambda c: c.get("pub_date", datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)),
    reverse=True
)

# Apply preference and target limits to the chronological list
preferred_rss = [c for c in rss_candidates if is_preferred_outlet(c["url"])]
regular_rss = [c for c in rss_candidates if not is_preferred_outlet(c["url"])]
rss_candidates = (preferred_rss + regular_rss)[:TARGET_RSS]

# Convert pub_date to string for JSON serialization
for c in rss_candidates:
    if "pub_date" in c and isinstance(c["pub_date"], datetime.datetime):
        c["pub_date"] = c["pub_date"].isoformat()

print(f"Harvested exactly {len(rss_candidates)} RSS candidates.")

# --- 4. HARVEST FROM BLUESKY FEEDS ---
bsky_candidates = []
seen_bsky_authors = set()

def harvest_bsky_search(client, topic, target, seen_urls, seen_ids, seen_targets, banned_keywords, requested_categories):
    cands = []
    keywords = [k.strip() for k in topic.split(",") if k.strip()] if topic else []
    if not keywords:
        return cands

    print(f"\nOpen-searching Bluesky network for topic(s): {keywords} (Target: {target})...")

    for kw in keywords:
        if len(cands) >= target:
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
            if len(cands) >= target:
                break
            text = getattr(post.record, 'text', '').strip()
            author_handle = post.author.handle
            rkey = post.uri.split('/')[-1]
            post_url = f"https://bsky.app/profile/{author_handle}/post/{rkey}"

            if len(text) < 45 or text.startswith('@') or text.startswith('Alethekanon'):
                continue
            if getattr(post.record, 'reply', None) is not None:
                continue

            article_url = extract_external_link(post)
            if not is_news_url(article_url):
                continue

            if is_banned(text, article_url, banned_keywords):
                continue

            # Filter by Category
            if not matches_category(text, article_url, [], requested_categories):
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

            cands.append({
                "url": article_url,
                "target_url": post_url,
                "mode": "root",
                "text": text,
                "subject": text[:30].strip() + "..."
            })
            seen_urls.add(normalized)
            seen_targets.add(post_rkey)

    print(f"Open search yielded {len(cands)} news-linked candidate(s).")
    return cands

if TARGET_BSKY > 0:
    print(f"\nHarvesting news from Bluesky feeds (Target: {TARGET_BSKY})...")
    handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
    password = os.environ.get('BSKY_PASSWORD')
    
    if password:
        client = Client()
        try:
            client.login(handle, password)
            resolver = IdResolver()
            
            # If topic/keywords defined, run network search first
            if keywords:
                bsky_candidates.extend(harvest_bsky_search(
                    client, args.topic, TARGET_BSKY, existing_queue_urls, existing_queue_ids, seen_historical_ids, banned_keywords, requested_categories
                ))
            
            bsky_feeds = [
                "https://bsky.app/profile/nickevershed.bsky.social/feed/aaaluca6lksmc",
                "https://bsky.app/profile/aendra.com/feed/verified-news",
                "https://bsky.app/profile/aendra.com/feed/news-2-0"
            ]
            
            # Fetch from feeds to top up target
            for feed_url in bsky_feeds:
                if len(bsky_candidates) >= TARGET_BSKY:
                    break
                print(f"Fetching from feed: {feed_url}...")
                try:
                    parts = feed_url.strip("/").split("/")
                    feed_handle, feed_rkey = parts[parts.index("profile")+1], parts[parts.index("feed")+1]
                    feed_did = resolver.handle.resolve(feed_handle)
                    feed_uri = f"at://{feed_did}/app.bsky.feed.generator/{feed_rkey}"
                    
                    feed_data = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 60})
                    for item in feed_data.feed:
                        if len(bsky_candidates) >= TARGET_BSKY:
                            break
                        record = getattr(item.post, 'record', None)
                        if record and getattr(record, 'reply', None) is not None:
                            continue
                        if getattr(item, 'reply', None) is not None:
                            continue
                            
                        text = getattr(item.post.record, 'text', '').strip()
                        author_handle = item.post.author.handle
                        rkey = item.post.uri.split('/')[-1]
                        post_url = f"https://bsky.app/profile/{author_handle}/post/{rkey}"
                        
                        if len(text) < 45 or text.startswith('@') or text.startswith('Alethekanon'):
                            continue
                        if "PINNED POST" in text or "News feeds" in text or "Every feed I run" in text:
                            continue
                        if any(domain in post_url for domain in ['zeit.de', 'tijd.be', 'sapo.pt', 'demorgen.be', 'folha.com', 'nu.nl', 'gazeteoksijen.com', 'graze.social']) or "graze.social" in text.lower():
                            continue
                        if not is_english(text):
                            continue
                        if post_url in existing_queue_urls:
                            continue
                            
                        article_url = extract_external_link(item.post)
                        if not is_news_url(article_url):
                            continue
                            
                        if is_banned(text, article_url, banned_keywords):
                            continue
                            
                        # Filter by Category
                        if not matches_category(text, article_url, [], requested_categories):
                            continue
                            
                        if is_duplicate_story(text, article_url, check_batch=False):
                            continue
                            
                        if author_handle in seen_bsky_authors:
                            continue
                            
                        bsky_candidates.append({
                            "url": article_url,
                            "target_url": post_url,
                            "mode": "root",
                            "text": text,
                            "subject": text[:30].strip() + "..."
                        })
                        seen_bsky_authors.add(author_handle)
                except Exception as ex:
                    print(f"Warning: Failed to fetch feed '{feed_url}': {ex}")
                    
            # Relaxation pass if slots still needed
            if len(bsky_candidates) < TARGET_BSKY:
                print(f"Retrying Bluesky feeds with relaxed author constraints to fill slots (Currently have {len(bsky_candidates)})...")
                for feed_url in bsky_feeds:
                    if len(bsky_candidates) >= TARGET_BSKY:
                        break
                    try:
                        parts = feed_url.strip("/").split("/")
                        feed_handle, feed_rkey = parts[parts.index("profile")+1], parts[parts.index("feed")+1]
                        feed_did = resolver.handle.resolve(feed_handle)
                        feed_uri = f"at://{feed_did}/app.bsky.feed.generator/{feed_rkey}"
                        feed_data = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 50})
                        for item in feed_data.feed:
                            if len(bsky_candidates) >= TARGET_BSKY:
                                break
                            record = getattr(item.post, 'record', None)
                            if record and getattr(record, 'reply', None) is not None:
                                continue
                            if getattr(item, 'reply', None) is not None:
                                continue
                                
                            text = getattr(item.post.record, 'text', '').strip()
                            author_handle = item.post.author.handle
                            rkey = item.post.uri.split('/')[-1]
                            post_url = f"https://bsky.app/profile/{author_handle}/post/{rkey}"
                            article_url = extract_external_link(item.post)
                            if not is_news_url(article_url):
                                continue
                            if article_url in existing_queue_urls or "graze.social" in article_url.lower() or "graze.social" in post_url.lower() or "graze.social" in text.lower():
                                continue
                            if len(text) < 45 or text.startswith('@') or text.startswith('Alethekanon'):
                                continue
                            if not is_english(text):
                                continue
                            if is_banned(text, article_url, banned_keywords):
                                continue
                            if not matches_category(text, article_url, [], requested_categories):
                                continue
                            if is_duplicate_story(text, article_url, check_batch=False):
                                continue
                                
                            bsky_candidates.append({
                                "url": article_url,
                                "target_url": post_url,
                                "mode": "root",
                                "text": text,
                                "subject": text[:30].strip() + "..."
                            })
                    except Exception as ex:
                        print(f"Warning: Relaxed feed fetch failed: {ex}")
            
            # Sort Bluesky candidates
            bsky_candidates.sort(key=get_sort_key)
            
            if bsky_candidates:
                print("\nBluesky Harvest Prioritization (least chosen outlets first):")
                for idx, c in enumerate(bsky_candidates[:15], 1):
                    url = c.get("url")
                    try:
                        host = urllib.parse.urlparse(url).hostname or url
                    except Exception:
                        host = url
                    print(f"  [{idx}] {host} (historical count: {get_historical_count(url)})")
                    
            bsky_candidates = bsky_candidates[:TARGET_BSKY]
                    
        except Exception as e:
            print(f"Warning: Bluesky login or retrieval failed: {e}")
    else:
        if not password:
            print("Warning: BSKY_PASSWORD not found in env. Skipping Bluesky harvesting.")
        else:
            print("Bluesky target already satisfied. Skipping Bluesky harvesting.")

print(f"Harvested and prioritized exactly {len(bsky_candidates)} Bluesky candidates.")

# --- 5. MERGE AND SAVE PREMIUM STORIES ---
combined_candidates = []
max_len = max(len(rss_candidates), len(bsky_candidates))
for i in range(max_len):
    if i < len(rss_candidates):
        combined_candidates.append(rss_candidates[i])
    if i < len(bsky_candidates):
        combined_candidates.append(bsky_candidates[i])

all_final = combined_candidates[:TARGET_RSS + TARGET_BSKY]
all_final.sort(key=get_sort_key)

print("\nScraping article bodies for final candidates...")
successful_final = []
dynamic_banlist_changed = False

for idx, c in enumerate(all_final, 1):
    url = c.get("url")
    if url:
        print(f"[{idx}/{len(all_final)}] Scraping content from: {url}")
        article_text = scrape_article_text(url)
        if article_text and not article_text.startswith("Error") and len(article_text.strip()) >= 200:
            article_text_clean = article_text[:4000]
            orig_text = c.get("text", "")
            c["text"] = f"Stated Claim / Post Context:\n{orig_text}\n\nActual Article Body:\n{article_text_clean}"
            print(f"  Scraped successfully ({len(article_text_clean)} chars).")
            successful_final.append(c)
        else:
            print(f"  Scrape failed, returned empty, or had insufficient content (length: {len(article_text) if article_text else 0} chars). Skipping candidate.")
            try:
                host = urllib.parse.urlparse(url.strip().lower()).hostname
                if host:
                    domain = host
                    if domain.startswith("www."):
                        domain = domain[4:]
                    if domain and domain not in DYNAMIC_BANNED_DOMAINS and not is_domain_whitelisted(domain) and domain not in NON_NEWS_DOMAINS:
                        DYNAMIC_BANNED_DOMAINS.add(domain)
                        dynamic_banlist_changed = True
                        print(f"  Added domain '{domain}' to dynamic scraping banlist.")
            except Exception as ex:
                print(f"  Warning: Failed to extract domain for banlist: {ex}")
    else:
        print(f"[{idx}/{len(all_final)}] Candidate has no URL. Skipping candidate.")

if dynamic_banlist_changed:
    save_dynamic_banned_domains()

final_candidates = existing_queue + successful_final

output_path = os.path.join(bot_dir, 'harvested_candidates.json')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(final_candidates, f, indent=2, ensure_ascii=False)
print(f"Candidates successfully saved to: {output_path}")

# Append newly harvested URLs to persistent history
if successful_final:
    history_urls = []
    if os.path.exists(harvested_history_path):
        try:
            with open(harvested_history_path, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                if isinstance(history_data, list):
                    history_urls = history_data
        except Exception:
            pass
            
    existing_history_set = set(normalize_url(u) for u in history_urls)
    new_added_count = 0
    for c in successful_final:
        url = c.get("url")
        if url and normalize_url(url) not in existing_history_set:
            history_urls.append(url)
            new_added_count += 1
            
    try:
        with open(harvested_history_path, 'w', encoding='utf-8') as f:
            json.dump(history_urls, f, indent=2, ensure_ascii=False)
        print(f"Appended {new_added_count} URLs to persistent history: {harvested_history_path}")
    except Exception as e:
        print(f"Warning: Failed to save harvested history: {e}")

print(f"\nFinal combined premium candidates count: {len(final_candidates)}")
for idx, c in enumerate(final_candidates, 1):
    source = "Bluesky" if "bsky.app" in c["url"] else "RSS"
    try:
        print(f"[{idx}] [{source}] {c['url']} -> {c['text'][:80].replace('\n', ' ')}...")
    except Exception:
        try:
            print(f"[{idx}] [{source}] {c['url']} -> [Unicode Content]")
        except Exception:
            pass
