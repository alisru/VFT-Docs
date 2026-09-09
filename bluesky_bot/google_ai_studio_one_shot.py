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
try:
    import matplotlib
    matplotlib.use('Agg')
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

def promote_and_register_selector(use_son=False):
    if use_son:
        from rebuild_registries_son import promote_and_register_incremental as promote_son
        return promote_son()
    else:
        from rebuild_registries import promote_and_register_incremental as promote_std
        return promote_std()

# Deterministic actor extraction for the live pipeline (LLM backfill handles history)
from actor_extract import extract_actors

# Load environment variables
bot_env_path = os.path.join(script_dir, ".env")
load_dotenv(bot_env_path)

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

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

def extract_thread_content_rules(text):
    """
    Strips on-disk storage dictionary schemas and obsolete canonical JSON examples from thread formatting rules,
    retaining only conversational formatting rules, ELI18 reading level standards, character budgets,
    and the logical thread steps mapping.
    """
    lines = text.split('\n')
    clean_lines = []
    skip = False
    
    for line in lines:
        stripped = line.strip()
        # Skip on-disk storage schema sections that contradict list-of-lists format
        if (stripped.startswith("## 1. The") and "JSON Schema" in stripped) or stripped.startswith("## 2. Attractor Forces Schema"):
            skip = True
            continue
        # Resume when reaching conversational formatting or logical steps
        if (stripped.startswith("## 2. Conversational Formatting") or 
            stripped.startswith("## 3. Conversational Formatting") or 
            stripped.startswith("## 3. The 13 Logical Steps") or 
            stripped.startswith("## 4. The Logical Steps")):
            skip = False
        # Skip canonical on-disk JSON example
        if (stripped.startswith("## 4. Canonical Example JSON") or 
            stripped.startswith("## 5. Canonical Example JSON") or 
            stripped.startswith("## Canonical Example JSON")):
            skip = True
            continue
            
        if not skip:
            clean_lines.append(line)
            
    return '\n'.join(clean_lines).strip()

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
        print("Warning: google-genai SDK is not installed. Gemini models will be unavailable.")
        return None
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        print(f"Warning: Failed to initialize genai.Client: {e}")
        return None

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

def load_banned_topics():
    default_categories = {
        "sport": [
            "sport", "sports", "football", "soccer", "basketball", "baseball", "tennis",
            "golf", "olympics", "nfl", "nba", "mlb", "nhl", "premier league", "afl",
            "rugby", "cricket", "formula 1", "f1", "athlete", "championship", "tournament",
            "race", "racing", "boxing", "ufc", "mma", "tour de france"
        ],
        "travel": [
            "travel", "tourism", "cruise", "vacation", "flight", "hotel", "resort",
            "hostel", "packing list", "travel guide", "wanderlust", "sightseeing", "itinerary"
        ],
        "entertainment": [
            "movie", "movies", "music", "song", "songs", "album", "concert", "gaming",
            "actor", "actress", "hollywood", "cinema", "box office", "festival", "nintendo",
            "playstation", "xbox", "tv show", "television", "celebrity", "celebrities",
            "gossip", "kardashian", "pop star", "rapper", "theatre", "playbill", "netflix",
            "hulu", "disney+", "streaming", "review"
        ],
        "obituaries": [
            "obituary", "obituaries", "dies at", "passed away at", "death notice", "in memoriam",
            "tribute to"
        ],
        "gardening": [
            "gardening", "garden", "recipe", "recipes", "cooking", "fashion", "style", "runway"
        ]
    }
    path = os.path.join(script_dir, "banned_topics.json")
    if not os.path.exists(path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default_categories, f, indent=2, ensure_ascii=False)
            print(f"Created default topic banlist map at {path}")
        except Exception as e:
            print(f"Warning: Failed to create default banned_topics.json: {e}")
        return default_categories
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                elif isinstance(data, list):
                    return {"custom": data}
        except Exception as e:
            print(f"Warning: Failed to load banned_topics.json: {e}")
    return default_categories

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
        pattern = rf"\b{re.escape(bk)}\b"
        if re.search(pattern, text_lower) or (url_lower and re.search(pattern, url_lower)):
            return True
        if " " in bk:
            variants = [bk.replace(" ", "-"), bk.replace(" ", "_"), bk.replace(" ", "")]
            for var in variants:
                var_pattern = rf"\b{re.escape(var)}\b"
                if re.search(var_pattern, text_lower) or (url_lower and re.search(var_pattern, url_lower)):
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
    "9": ["npr.org"],
    "10": ["scmp.com"],
    "11": ["sixthtone.com"],
    "12": ["hongkongfp.com"],
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
        "china": [
            {"name": "SCMP China", "url": "https://www.scmp.com/rss/4/feed"},
            {"name": "SCMP Asia & World", "url": "https://www.scmp.com/rss/92/feed"},
            {"name": "SCMP Economy", "url": "https://www.scmp.com/rss/96/feed"},
            {"name": "SCMP Tech", "url": "https://www.scmp.com/rss/318206/feed"},
            {"name": "Sixth Tone", "url": "https://www.sixthtone.com/rss"},
            {"name": "Hong Kong Free Press", "url": "https://hongkongfp.com/feed/"},
            {"name": "China Daily News", "url": "http://www.chinadaily.com.cn/rss/china_rss.xml"},
            {"name": "China Daily Biz", "url": "http://www.chinadaily.com.cn/rss/bizchina_rss.xml"},
            {"name": "Google News China", "url": "https://news.google.com/rss/search?q=China+when:2d&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News China Tech/Economy", "url": "https://news.google.com/rss/search?q=China+(economy+OR+tech+OR+diplomacy)+when:2d&hl=en-US&gl=US&ceid=US:en"},
        ],
        "asia": [
            {"name": "SCMP Asia & World", "url": "https://www.scmp.com/rss/92/feed"},
            {"name": "SCMP China", "url": "https://www.scmp.com/rss/4/feed"},
            {"name": "Hong Kong Free Press", "url": "https://hongkongfp.com/feed/"},
            {"name": "Sixth Tone", "url": "https://www.sixthtone.com/rss"},
            {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
            {"name": "Google News Asia", "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en"},
        ],
        "tech": [
            {"name": "BBC Tech", "url": "http://feeds.bbci.co.uk/news/technology/rss.xml"},
            {"name": "NYT Tech", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"},
            {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
            {"name": "The Guardian Tech", "url": "https://www.theguardian.com/technology/rss"},
            {"name": "SCMP Tech", "url": "https://www.scmp.com/rss/318206/feed"},
        ],
        "business": [
            {"name": "BBC Business", "url": "http://feeds.bbci.co.uk/news/business/rss.xml"},
            {"name": "NYT Business", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"},
            {"name": "CNBC Business", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147"},
            {"name": "The Guardian Business", "url": "https://www.theguardian.com/business/rss"},
            {"name": "DW Business", "url": "https://rss.dw.com/xml/rss-en-bus"},
            {"name": "SCMP Economy", "url": "https://www.scmp.com/rss/96/feed"},
        ],
        "politics": [
            {"name": "BBC Politics", "url": "http://feeds.bbci.co.uk/news/politics/rss.xml"},
            {"name": "NYT Politics", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml"},
            {"name": "Fox News Politics", "url": "http://feeds.foxnews.com/foxnews/politics"},
            {"name": "Washington Examiner", "url": "https://www.washingtonexaminer.com/feed/"},
            {"name": "The Federalist", "url": "https://thefederalist.com/feed/"},
            {"name": "Washington Times", "url": "https://www.washingtontimes.com/rss/headlines/news/politics/"},
            {"name": "Daily Caller", "url": "https://dailycaller.com/feed/"},
            {"name": "Breitbart", "url": "https://feeds.feedburner.com/breitbart"},
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
            {"name": "Fox News Latest", "url": "http://feeds.foxnews.com/foxnews/latest"},
            {"name": "New York Post", "url": "https://nypost.com/news/feed/"},
            {"name": "The Guardian World", "url": "https://www.theguardian.com/world/rss"},
            {"name": "NPR World", "url": "https://feeds.npr.org/1004/rss.xml"},
            {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
            {"name": "DW News World", "url": "https://rss.dw.com/xml/rss-en-all"},
            {"name": "France 24", "url": "https://www.france24.com/en/rss"},
            {"name": "CBC News", "url": "https://rss.cbc.ca/lineup/topstories.xml"},
            {"name": "UPI News", "url": "https://rss.upi.com/news/news.rss"},
            {"name": "SCMP China", "url": "https://www.scmp.com/rss/4/feed"},
            {"name": "Google News World", "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en"},
        ],
        "general": [
            {"name": "ABC News Australia", "url": "https://www.abc.net.au/news/feed/2942460/rss.xml"},
            {"name": "9News Australia", "url": "https://www.9news.com.au/rss"},
            {"name": "SBS News", "url": "https://www.sbs.com.au/news/feed"},
            {"name": "Sydney Morning Herald", "url": "https://www.smh.com.au/rss/feed.xml"},
            {"name": "Perth Now", "url": "https://www.perthnow.com.au/feed"},
            {"name": "Daily Mail Australia", "url": "https://www.dailymail.co.uk/auhome/index.rss"},
            {"name": "The Age", "url": "https://www.theage.com.au/rss/feed.xml"},
            {"name": "Brisbane Times", "url": "https://www.brisbanetimes.com.au/rss/feed.xml"},
            {"name": "WA Today", "url": "https://www.watoday.com.au/rss/feed.xml"},
            {"name": "Canberra Times", "url": "https://www.canberratimes.com.au/rss.xml"},
            {"name": "BBC News", "url": "http://feeds.bbci.co.uk/news/rss.xml"},
            {"name": "NYT Home", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"},
            {"name": "Fox News Latest", "url": "http://feeds.foxnews.com/foxnews/latest"},
            {"name": "New York Post", "url": "https://nypost.com/news/feed/"},
            {"name": "Washington Examiner", "url": "https://www.washingtonexaminer.com/feed/"},
            {"name": "The Federalist", "url": "https://thefederalist.com/feed/"},
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
        
    banned_map = load_banned_topics()
    banned_keywords = []
    if banned_topic:
        user_banned = [k.strip().lower() for k in banned_topic.split(",") if k.strip()]
        for item in user_banned:
            if item in banned_map:
                banned_keywords.extend(banned_map[item])
            else:
                banned_keywords.append(item)
    else:
        for cat, kws in banned_map.items():
            banned_keywords.extend(kws)
    banned_keywords = list(dict.fromkeys([kw.lower() for kw in banned_keywords]))
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
    "gemini-3.7-flash",
    "gemini-2.5-flash",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "vertex:gemini-3.7-flash",
    "vertex:gemini-3.1-flash-lite",
    "gemini-3-flash-preview",
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
            raw_fmt = f.read()
            clean_fmt = extract_thread_content_rules(raw_fmt)
            _RULES_CACHE[f"{cache_key}_formatting"] = minify_markdown(clean_fmt)
    return _RULES_CACHE[f"{cache_key}_convergence"], _RULES_CACHE[f"{cache_key}_formatting"]

SPIRITUAL_TRADITIONS_MAP = {
    "christianity": "Christian / Abrahamic (Gospels, Epistles, Hebrew Prophets like Isaiah/Amos, Psalms, Proverbs, Ecclesiastes)",
    "hinduism": "Hindu / Vedic (Bhagavad Gita, Upanishads, Mahabharata, Vedas — Dharma, Karma, Rita)",
    "buddhism": "Buddhist / Dharmic (Dhammapada, Pali Canon, Sutta Nipata, Heart Sutra, Zen Koans — Ahimsa, Interdependence)",
    "taoism": "Taoist / Eastern Metaphysics (Tao Te Ching, Zhuangzi, I Ching — Wu Wei, natural harmony)",
    "islam": "Islamic & Sufi (Quran, Hadith, Rumi's Masnavi, Attar, Saadi — Social equity, Sacred Trust/Amanah, Divine Mercy)",
    "indigenous": "Indigenous & Custodial Lore (First Nations / Alcheringa Dreaming Law, Haudenosaunee Great Law, Ubuntu, Kaitiakitanga)",
    "stoicism": "Stoic & Classical Philosophy (Marcus Aurelius' Meditations, Epictetus, Seneca, Platonic dialogues)",
    "other": "Universal & Metaphysical Canon (Martin Buber's I and Thou, Hermeticism, universal philosophical ethics)",
}

def resolve_spiritual_traditions(traditions_arg):
    if not traditions_arg or str(traditions_arg).lower().strip() in ("all", "any", "everything", "none"):
        return list(SPIRITUAL_TRADITIONS_MAP.keys())
    
    selected = []
    aliases = {
        "christian": "christianity",
        "bible": "christianity",
        "hindu": "hinduism",
        "vedic": "hinduism",
        "gita": "hinduism",
        "buddhist": "buddhism",
        "dharmic": "buddhism",
        "taoist": "taoism",
        "daoist": "taoism",
        "daoism": "taoism",
        "sufi": "islam",
        "muslim": "islam",
        "islamic": "islam",
        "first_nations": "indigenous",
        "aboriginal": "indigenous",
        "custodial": "indigenous",
        "stoic": "stoicism",
        "greek": "stoicism",
        "philosophy": "stoicism",
        "universal": "other",
        "everything_else": "other",
        "else": "other",
    }
    
    for item in str(traditions_arg).split(","):
        key = item.strip().lower().replace(" ", "_").replace("-", "_")
        key = aliases.get(key, key)
        if key in SPIRITUAL_TRADITIONS_MAP and key not in selected:
            selected.append(key)
    
    return selected if selected else list(SPIRITUAL_TRADITIONS_MAP.keys())

def build_spiritual_directive(traditions_arg="all"):
    active_keys = resolve_spiritual_traditions(traditions_arg)
    active_desc = "\n".join(f"  - {SPIRITUAL_TRADITIONS_MAP[k]}" for k in active_keys)
    
    return (
        "=== SPIRITUAL AUDIT DIRECTIVE ===\n"
        "- The final post in the posts array MUST be a Spirithekanon post.\n"
        "- Active Allowed Traditions / Canons:\n"
        f"{active_desc}\n"
        "- CRITICAL DIRECTIVE: You MUST evaluate the story's core dilemma and select the single most structurally and philosophically appropriate passage STRICTLY from the allowed traditions listed above.\n"
        "- DO NOT default to any single religion (e.g. Christian/Bible verses) unless it is genuinely the sharpest philosophical fit among the active traditions.\n"
        "- STRICT VERBATIM & CANONICAL ACCURACY (ZERO-HALLUCINATION RULE):\n"
        "  1. VERBATIM PASSAGE MANDATE: The quoted text inside quotation marks MUST be a real, authentic, historically established canonical passage or recognized standard translation. You are STRICTLY FORBIDDEN from inventing, improvising, synthesizing, or writing fake 'fortune cookie' aphorisms.\n"
        "  2. EXACT CITATION ACCURACY: The citation (e.g. Tao Te Ching 64, Bhagavad Gita 3.21, Dhammapada 103, Quran 31:17, 1 Timothy 6:10, Meditations 4.3) MUST match the exact book, chapter, and verse/section of the quote. NEVER attribute a quote to the wrong chapter, verse, or book.\n"
        "  3. NO IDIOMS AS SCRIPTURE: NEVER cite English proverbs, colloquial idioms, or secular folk sayings (e.g. 'Cleanliness is next to godliness' or 'Honesty is the best policy') as scripture.\n"
        "  4. NO META-COMMENTARY IN QUOTES: NEVER insert editorial commentary, internal hesitation, or conversational remarks inside the quotation marks.\n"
        "  5. MULTI-PHASE LENGTH & DE-ARCHAIC FALLBACK RULE:\n"
        "     - The entire Spirithekanon post MUST be kept strictly under 280 characters total.\n"
        "     - Format: Strip all unnecessary characters (NO parentheses around citation, NO em-dash, NO plane name suffixes). Example: \"[Quote]\" Isaiah 24:4-5 FAIL\n"
        "     - If a passage is long and approaches character limits, de-archaic verbose setup phrasing into concise modern language while preserving all core theological/philosophical beats, the operative dilemma, and the exact citation.\n"
        "- Format it exactly as:\n"
        "  Spirithekanon:\n"
        "  \"[Canonical Quote or De-archaiced Passage]\" [Source Text Chapter:Verse or Section] [PASS/FAIL/HIT]\n"
        "  [1 concise sentence of deep ethical/philosophical reflection on the actors' actions relative to this quote].\n"
        "  *Note: The entire Spirithekanon post must be kept under 280 characters total.\n\n"
    )

def build_formatting_rules(use_son=False, compact=False, five_word=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all"):
    convergence_rules, formatting_rules = _load_rules(use_son=use_son)
        
    if five_word:
        formatting_rules = (
            "CRITICAL DIRECTIVE FOR FIVE-WORD MODE:\n"
            "You are in FIVE-WORD MODE. Every single element/string in the 'posts' array MUST be exactly 5 words long. "
            "No element may exceed 5 words. Plan your word selection meticulously.\n"
            "Format of posts[3] (the Verdict post) MUST be exactly: 'stated [stated_u/psi] actual [real_u/psi] [pass/fail/neutral]'\n"
            "Example of posts[3]: 'stated (+1.0, +1.0) actual (-0.5, -0.5) fail'\n"
            "This counts as exactly 5 words: 'stated' (1), '(+1.0, +1.0)' (2), 'actual' (3), '(-0.5, -0.5)' (4), 'fail' (5).\n"
            "Keep posts[4] as the 5-word Context post. Keep all other posts under 5 words too.\n"
        )
    elif compact:
        override_text = (
            "=== COMPACT MODE DIRECTIVE ===\n"
            "- Posts 1 to 4 (indices 0 to 3 in the posts array: Hook, Claim, Reality, Verdict) will be posted as standard text on Bluesky. They MUST be kept strictly under 260 characters each.\n"
            "- Posts 5+ (indices 4+ in the posts array: Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Personas) will be rendered into a graphical image card. They have NO character limits. They MUST be highly verbose, comprehensive, and detailed (typically 400-800 characters each) to explain the concepts fully. DO NOT compress or shorten them.\n\n"
        )
        formatting_rules = override_text + formatting_rules
        formatting_rules = formatting_rules.replace("Keep every single step strictly under **275 characters**", "Keep the first 4 steps under **275 characters** (subsequent image card steps have no character limits, 400-800 chars)")
        formatting_rules = formatting_rules.replace("Keep each individual post strictly under 280 characters (hard max 290)", "Keep the first 4 steps strictly under 260 characters (subsequent image card steps have no character limits, 400-800 chars)")

    if use_son and use_multi_aspect:
        multi_aspect_text = (
            "=== MULTI-ASPECT & MULTI-SOURCE DIRECTIVE ===\n"
            "- Post 4 (index 3 in the posts array: The Verdict) is the OVERALL verdict only. It evaluates the REAL-WORLD EVENT and ACTORS themselves. Format it as:\n"
            "  Verdict: [PASS/FAIL] — [Path Name]. [1-2 sentence explanation of the trajectory's cause].\n"
            "  Integrity: [real_integrity] (Hypocrisy: [real_rnet], z: [real_z])\n"
            "  DO NOT include any sub-audit or Subs: summary in this post.\n"
            "  *Note: Post 4 MUST be kept strictly under 260 characters total.\n"
            "- Post 5 (index 4 in the posts array: Source Quality Scorecard / Sub-Audits Breakdown) is the dedicated aspect & source breakdown. Format DIRECTLY as concise bullet points (NO header prefix). Each bullet must be 1 short line under 60 chars:\n"
            "  - [Outlet / Aspect A]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Brief 1-line framing/omission reason under 60 chars].\n"
            "  - [Outlet / Aspect B]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Brief 1-line framing/omission reason under 60 chars].\n"
            "  *Note: If the story contains multiple reporting sources in the dossier, evaluate each news outlet's editorial integrity and framing bias as individual aspects. Keep the ENTIRE combined Post 5 strictly under 260 characters total.\n"
            "- Post 6 (index 5) is the Context post. Keep it to 1-2 concise sentences under 260 characters.\n"
            "- The Unavoidables post MUST have exactly 1 concise sentence for The Unavoidable Truth and 1 concise sentence for The Unavoidable Lie (under 260 chars total).\n"
            "- The Alethekanon post MUST be at most 2 concise sentences (under 260 chars total).\n\n"
        )
        formatting_rules = multi_aspect_text + formatting_rules

    if use_spiritual:
        spiritual_text = build_spiritual_directive(spiritual_traditions)
        formatting_rules = spiritual_text + formatting_rules

    return convergence_rules, formatting_rules

SOCIAL_PHYSICS_DIRECTIVE = (
    "=== SOCIAL PHYSICS ENGINE ('THE 42') ===\n"
    "AUDIT DIRECTIVE FOR 'Social Physics Analysis:' POST:\n"
    "Analyze the real-world actors and events using the 4 axes (Power vs. Empowerment, Justification vs. Transparency, Projection vs. Empathy, Manufactured Problems vs. Solutions) and actor loops (Smart Selfish vs. Smart Altruistic) defined in the convergence rules.\n"
    "Cut through stated pretexts to reveal whether actors are running a Smart Selfish Maneuver (hidden extraction behind manufactured crises and projected blame) or acting towards genuine systemic empowerment."
)

def build_system_instruction(use_son=False, compact=False, five_word=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all", extra_context=None):
    import datetime
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    core_concept_directive = (
        f"Today's reference date is {today_str}.\n"
        "CONCEPTUAL DIRECTIVE: You must always evaluate the REAL-WORLD EVENT and ACTORS themselves, rather than auditing the journalist's reporting or news outlet. "
        "Stated claims/ideals and actual realities must reflect the actions, intentions, and outcomes of the actors involved in the event itself. "
        "After evaluating the event, you can optionally analyze the reporting's accuracy or framing relative to the event in the Alethekanon analysis."
    )

    if five_word:
        instruction = (
            "You are the Master Aletheia Auditor in Five-Word Mode. Respond ONLY with the exact delimited data rows requested. No commentary, no markdown, no preamble, no explanation. "
            "Use Google Search ONLY to fact-check names, dates, and medical/legal claims from the article. "
            "Every single post in the 'posts' array MUST be exactly 5 words long. No more, no less. "
            "CRITICAL: The 'subject' field (item[2]) must be the full, non-truncated title/subject of the story based on the context. Never end the subject with '...' (ellipses) or truncate it. Reconstruct the full correct title if the input title is truncated.\n\n"
            f"{core_concept_directive}"
        )
    elif compact:
        instruction = (
            "You are the Master Aletheia Auditor in Compact Mode. Respond ONLY with the exact delimited data rows requested. No commentary, no markdown, no preamble, no explanation. "
            "Use Google Search ONLY to fact-check names, dates, and medical/legal claims from the article. Do NOT use search results to alter your structural analysis or your Alethekanon persona. "
            "You are strictly forbidden from inventing, guessing, or inferring specific details not explicitly written in the text or verified by search. "
            "Adhere to a strict budget of AT MOST 1 search query per story to stay within API quota limits. "
            "If you used Google Search to verify any information in your response for a candidate, you MUST append the emoji 🌐 at the end of the first post (post 1) of that candidate's thread. "
            "CRITICAL: You are strictly forbidden from writing robotic bracket tags like [Verified: ...], 'Verified:', or raw URLs in the Alethekanon post. Alethekanon MUST always speak purely in authentic, sharp analytical prose. "
            "CRITICAL: Posts 1 to 4 (items 0 to 3 in the posts array: Hook, Claim, Reality, Verdict) MUST be under 260 characters (hard limit) as they are posted as text on Bluesky. "
            "Posts 5+ (items 4+ in the posts array: Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Personas) have NO character limits and should be highly verbose, comprehensive, and detailed (typically 400-800 characters each) because they will be rendered into a high-fidelity visual image card.\n\n"
            f"{core_concept_directive}"
        )
    else:
        instruction = (
            "You are the Master Aletheia Auditor. Respond ONLY with the exact delimited data rows requested. No commentary, no markdown, no preamble, no explanation. "
            "Use Google Search ONLY to fact-check names, dates, and medical/legal claims from the article. Do NOT use search results to alter your structural analysis or your Alethekanon persona. "
            "You are strictly forbidden from inventing, guessing, or inferring specific details not explicitly written in the text or verified by search. "
            "Adhere to a strict budget of AT MOST 1 search query per story to stay within API quota limits. "
            "If you used Google Search to verify any information in your response for a candidate, you MUST append the emoji 🌐 at the end of the first post (post 1) of that candidate's thread. "
            "CRITICAL: You are strictly forbidden from writing robotic bracket tags like [Verified: ...], 'Verified:', or raw URLs in the Alethekanon post. Alethekanon MUST always speak purely in authentic, sharp analytical prose. "
            "CRITICAL: In standard mode, each post must be kept strictly under 280 characters to fit Bluesky limits (thread_formatting_son standard). Aim for 250-275 characters. BE CONCISE.\n\n"
            f"{core_concept_directive}"
        )
    if not five_word:
        instruction += f"\n\n{SOCIAL_PHYSICS_DIRECTIVE}"
    if extra_context:
        instruction += f"\n\nCRITICAL: You must actively incorporate the following background knowledge and additional context when performing the audits:\n{extra_context}"
    return instruction

def build_output_format(n, use_son=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all"):
    expected_len = 28 if (use_son and use_multi_aspect) else (27 if use_son else 17)
    
    example_posts_list = [
        '"Hook text here.\\nEvidence: a, b, c\\n#Aletheia #Topic"',
        '"Claim text.\\nStated Judgement: (+1.0, 0.0) — Good Preference"',
        '"Reality text.\\nResulting Judgement: (-1.0, -1.0) — Greater Evil"',
        '"Verdict: FAIL — The Path of Deception.\\nExplanation.\\n\\nIntegrity: Severe Deception (Hypocrisy: 12.5, z: 4)"',
        '"Context paragraph."',
        '"The Bright Side:\\nNuance."',
        '"The Breakdown & Plane Error:\\nExplanation."',
        '"**Social Physics Analysis:**\\nDirect, conversational analysis in plain English detailing selfishness, pretexts, and projection."',
        '"The Trajectory: The Path of Deception.\\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward Greater Evil. Explanatory mathematical sentence."',
        '"The Unavoidable Truth: truth in 1 sentence.\\n\\nThe Unavoidable Lie: lie in 1 sentence."',
        '"Alethekanon:\\nStructural analysis in 1-2 concise sentences."',
        '"Awwthekanon:\\nEmpathy."',
        '"Brothekanon:\\nCasual take."'
    ]
    if use_son and use_multi_aspect:
        example_posts_list.insert(4, '"- Nigel Farage: FAIL (-0.94, -0.87) — Prioritizes political capital over truth.\\n- Electoral Messaging: FAIL (-0.94, -0.88) — Disinformation exposed."')
    
    if use_spiritual:
        example_posts_list.append('"Spirithekanon:\\n\\"Universal wisdom quote...\\" (Source Chapter/Section) — PASS (Spiritual Vector)\\nSpiritual evaluation in 1-2 sentences."')
    
    example_posts_str = ",\n      ".join(example_posts_list)

    output_format = (
        f"OUTPUT FORMAT — YOUR ENTIRE RESPONSE MUST BE A SINGLE VALID JSON LIST OF LISTS. NO commentary, NO markdown formatting (other than JSON code fences if desired), NO explanation.\n"
        f"The JSON array must contain exactly {n} elements (one per candidate, in the same order). Each element must be a list of exactly {expected_len} items representing the evaluation of that candidate in this specific structure:\n"
        "[\n"
        "  [\n"
        '    "thinking",                                // item[0]: detailed thinking block. You MUST write down the full 6-Phase Convergence scan here, including scoring the 18 variables of the 6 attractors with high-resolution decimals, and detailing your coordinate equations (u, psi), hypocrisy delta, and trajectory calculations step-by-step before outputting the rest of the array.\n'
        '    "id",                                      // item[1]: clean story id slug\n'
        '    "subject",                                 // item[2]: story subject\n'
        '    "link",                                    // item[3]: story link (or "")\n'
        '    "target_url",                              // item[4]: target post url (or "")\n'
        "    0.5,                                       // item[5]: stated morality (claim_u, float)\n"
        "    0.0,                                       // item[6]: stated will (claim_psi, float)\n"
        "    -0.8,                                      // item[7]: actual morality (real_u, float)\n"
        "    -0.9,                                      // item[8]: actual will (real_psi, float)\n"
        '    "root",                                    // item[9]: mode ("root" or "reply")\n'
        "    [\n"
        f"      {example_posts_str}\n"
        f"    ],                                         // item[10]: posts array (logical thread sequence: Hook, Claim, Reality, Verdict, Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Personas...)\n"
        '    ["Actor / Org / Geopolitical tag", ...],  // item[11]: actors array\n'
        '    "macro_event",                             // item[12]: overarching context name or "" if none\n'
        "    null,                                      // item[13]: macro stated morality, null if none\n"
        "    null,                                      // item[14]: macro stated will, null if none\n"
        "    null,                                      // item[15]: macro actual morality, null if none\n"
        "    null                                       // item[16]: macro actual will, null if none\n"
    )
    if use_son:
        if use_multi_aspect:
            output_format += (
                ",\n"
                "    1.0,                                       // item[17]: stated R_net integrity score\n"
                "    12.5,                                      // item[18]: actual R_net integrity score\n"
                "    0,                                         // item[19]: stated uncertainty score (claim_z)\n"
                "    4,                                         // item[20]: actual uncertainty score (real_z)\n"
                "    [0, 0, 0, 0, 0, 0, 0],                     // item[21]: stated blank profile [B_Q1..B_Q7]\n"
                "    [1, 0, 0, 2, 1, 0, 0],                     // item[22]: actual blank profile\n"
                '    "Absolute Truth",                          // item[23]: stated integrity label\n'
                '    "Severe Deception",                        // item[24]: actual integrity label\n'
                '    {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}}, // item[25]: stated forces\n'
                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}, // item[26]: actual forces\n'
                '    [{"aspect": "Aspect Name", "claim_u": 0.5, "claim_psi": 0.0, "real_u": -0.9, "real_psi": -0.8, "verdict": "FAIL", "reason": "1-line reason under 60 chars"}] // item[27]: aspects breakdown\n'
            )
        else:
            output_format += (
                ",\n"
                "    1.0,                                       // item[17]: stated R_net integrity score\n"
                "    12.5,                                      // item[18]: actual R_net integrity score\n"
                "    0,                                         // item[19]: stated uncertainty score (claim_z)\n"
                "    4,                                         // item[20]: actual uncertainty score (real_z)\n"
                "    [0, 0, 0, 0, 0, 0, 0],                     // item[21]: stated blank profile [B_Q1..B_Q7]\n"
                "    [1, 0, 0, 2, 1, 0, 0],                     // item[22]: actual blank profile\n"
                '    "Absolute Truth",                          // item[23]: stated integrity label\n'
                '    "Severe Deception",                        // item[24]: actual integrity label\n'
                '    {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}}, // item[25]: stated forces\n'
                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}  // item[26]: actual forces\n'
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
            "FORCE SCORING GRANULARITY CRITICAL RULES:\n"
            "- You MUST score the [S, O, N] force magnitudes for the 6 attractors as granular decimals (e.g. 0.2, 0.5, 0.8, 1.2, 1.5, 1.8) based on specific evidence in the text. Do NOT default to binary 0.0 or 1.0 values, as this causes coordinate collapse and loses analytical resolution.\n"
            "- Ensure that the forces you output in items[25] and [26] are highly granular and match the math you write down in your thinking block (item[0]).\n\n"
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
        "    1.0,\n"
        "    -0.89,\n"
        "    -0.87,\n"
        '    "root",\n'
        "    [\n"
        f"      {example_posts_str}\n"
        "    ],\n"
        '    ["Nigel Farage", "Reform UK", "United Kingdom"],\n'
        '    "",\n'
        "    null,\n"
        "    null,\n"
        "    null,\n"
        "    null"
    )
    if use_son:
        if use_multi_aspect:
            output_format += (
                ",\n"
                "    1.0,\n"
                "    12.5,\n"
                "    0,\n"
                "    4,\n"
                "    [0, 0, 0, 0, 0, 0, 0],\n"
                "    [1, 0, 0, 2, 1, 0, 0],\n"
                '    "Absolute Truth",\n'
                '    "Severe Deception",\n'
                '    {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}},\n'
                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}},\n'
                '    [\n'
                '      {\n'
                '        "name": "Nigel Farage Political Intervention",\n'
                '        "type": "actor",\n'
                '        "stated_forces": {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}},\n'
                '        "actual_forces": {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\n'
                '      },\n'
                '      {\n'
                '        "name": "Electoral Messaging Integrity",\n'
                '        "type": "aspect",\n'
                '        "stated_forces": {"GG": {"S": 1.0, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.0, "N": 0.0}, "LG": {"S": 0.0, "O": 0.0, "N": 0.5}, "LE": {"S": 0.0, "O": 0.0, "N": 0.5}, "GP": {"S": 1.0, "O": 0.0, "N": 0.0}, "BP": {"S": 1.0, "O": 1.0, "N": 0.0}},\n'
                '        "actual_forces": {"GG": {"S": 0.0, "O": 1.5, "N": 0.0}, "GE": {"S": 1.0, "O": 0.0, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\n'
                '      }\n'
                '    ]\n'
            )
        else:
            output_format += (
                ",\n"
                "    1.0,\n"
                "    12.5,\n"
                "    0,\n"
                "    4,\n"
                "    [0, 0, 0, 0, 0, 0, 0],\n"
                "    [1, 0, 0, 2, 1, 0, 0],\n"
                '    "Absolute Truth",\n'
                '    "Severe Deception",\n'
                '    {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}},\n'
                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\n'
            )
    output_format += (
        "\n"
        "  ]\n"
        "]"
    )
    return output_format

def harvest_search_grounding(genai_client, candidates):
    """
    Stage 1 Grounding Harvester:
    Uses gemini-2.5-flash (with fallback to gemini-2.5-flash-lite) with Google Search Grounding
    to fetch verified facts, official data, and resolve HTTP 200 URLs.
    Batches all candidates in the chunk into a single search grounding request.
    """
    if not genai_client or not candidates:
        return "", []
    
    # Safety guard: Never exceed 5 candidates per search grounding call to prevent Google Search fan-out 503 timeouts
    if len(candidates) > 5:
        all_dossiers = []
        all_urls = []
        for i in range(0, len(candidates), 5):
            sub_batch = candidates[i:i+5]
            sub_dossier, sub_urls = harvest_search_grounding(genai_client, sub_batch)
            if sub_dossier:
                all_dossiers.append(sub_dossier)
            for u in sub_urls:
                if u not in all_urls:
                    all_urls.append(u)
        return "\n\n".join(all_dossiers), all_urls
    
    import datetime, requests
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    queries = []
    for c in candidates:
        title = c.get("title") or c.get("subject") or ""
        link = c.get("link") or c.get("url") or ""
        publisher = c.get("publisher") or c.get("author") or ""
        if not publisher and link:
            try:
                host = urllib.parse.urlparse(link).hostname or ""
                publisher = host.replace("www.", "")
            except Exception:
                publisher = ""
        body = c.get("body") or c.get("summary") or c.get("text") or ""
        body_snippet = body[:400].strip()
        
        parts = [f"- Headline: {title}"]
        if publisher:
            parts.append(f"Publisher: {publisher}")
        if link:
            parts.append(f"Original Story URL: {link}")
        if body_snippet:
            parts.append(f"Summary/Snippet: {body_snippet}")
            
        queries.append(" | ".join(parts))
    
    prompt = (
        f"You are a Real-Time Fact-Checking Grounding Engine. Today's reference date is {today_str}.\n"
        f"Search Google for current external news, official reports, data figures, and verified developments for each of the {len(candidates)} stories below:\n\n"
        + "\n\n".join(queries) +
        "\n\nProvide a concise Grounding Dossier for each story:\n"
        "1. Verified numbers / official statistics (e.g. criminal vs non-criminal breakdown, economic metrics, quotes).\n"
        "2. Counter-claims, retractions, or omitted collateral details.\n"
        "3. Timeline and recent official developments."
    )
    
    grounding_models = ["gemini-2.5-flash-lite", "gemini-2.5-flash"]
    last_err = None
    
    for g_model in grounding_models:
        try:
            print(f"  [Stage 1 Grounding] Pre-harvesting search facts for {len(candidates)} candidate(s) via {g_model} (Ref Date: {today_str})...")
            resp = genai_client.models.generate_content(
                model=g_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=16384,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )
            dossier = resp.text.strip() if resp and hasattr(resp, "text") and resp.text else ""
            
            resolved_urls = []
            if resp.candidates and resp.candidates[0].grounding_metadata:
                chunks = resp.candidates[0].grounding_metadata.grounding_chunks
                if chunks:
                    for c in chunks:
                        if c.web and c.web.uri:
                            raw_url = c.web.uri
                            try:
                                r = requests.get(raw_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5, allow_redirects=True)
                                if r.status_code == 200 and r.url not in resolved_urls:
                                    resolved_urls.append(r.url)
                            except Exception:
                                pass
            print(f"  [Stage 1 Grounding] Harvested successfully via {g_model} ({len(resolved_urls)} verified HTTP 200 URLs).")
            return dossier, resolved_urls
        except Exception as e:
            last_err = e
            print(f"  [Stage 1 Grounding] Warning: Grounding attempt on {g_model} failed ({e}). Trying fallback...")
            
    print(f"  [Stage 1 Grounding] All grounding models failed ({last_err}). Proceeding with ungrounded context.")
    return "", []

def run_one_shot_evaluations(genai_client, candidates, model_name, agnes_api_key=None, use_son=False, use_search=False, extra_context=None, model_sequence=None, compact=False, five_word=False, thinking_level="MEDIUM", use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all", pre_grounded_dossier=None, pre_harvested_urls=None):
    if pre_harvested_urls is None:
        pre_harvested_urls = []
    
    # Stage 1: Attach pre-grounded dossier or run fallback grounding on 2.5/2.5-lite
    if pre_grounded_dossier:
        extra_context = (extra_context + "\n\n" if extra_context else "") + f"=== VERIFIED REAL-TIME SEARCH GROUNDING DOSSIER ===\n{pre_grounded_dossier}"
    elif use_search and genai_client:
        grounded_dossier, pre_harvested_urls = harvest_search_grounding(genai_client, candidates)
        if grounded_dossier:
            extra_context = (extra_context + "\n\n" if extra_context else "") + f"=== VERIFIED REAL-TIME SEARCH GROUNDING DOSSIER ===\n{grounded_dossier}"

    convergence_rules, formatting_rules = build_formatting_rules(use_son=use_son, compact=compact, five_word=five_word, use_multi_aspect=use_multi_aspect, use_spiritual=use_spiritual, spiritual_traditions=spiritual_traditions)
    system_instruction = build_system_instruction(use_son=use_son, compact=compact, five_word=five_word, use_multi_aspect=use_multi_aspect, use_spiritual=use_spiritual, spiritual_traditions=spiritual_traditions, extra_context=extra_context)
    
    n = len(candidates)
    output_format = build_output_format(n, use_son=use_son, use_multi_aspect=use_multi_aspect, use_spiritual=use_spiritual, spiritual_traditions=spiritual_traditions)
    
    # Prune duplicate payload fields from candidates before passing to LLM to save tokens
    clean_candidates = []
    for c in candidates:
        cand_entry = {
            "subject": c.get("subject") or c.get("title") or "",
            "url": c.get("url") or c.get("link") or "",
            "target_url": c.get("target_url") or "",
            "mode": c.get("mode") or "root",
            "text": c.get("text") or c.get("body") or "",
        }
        if c.get("id"):
            cand_entry["id"] = c.get("id")
        if c.get("pub_date"):
            cand_entry["pub_date"] = str(c.get("pub_date"))
        clean_candidates.append(cand_entry)

    user_payload = [
        f"=== CONVERGENCE TEST RULES ===\n{convergence_rules}\n\n",
        f"=== THREAD FORMATTING & SCHEMAS ===\n{formatting_rules}\n\n",
        f"You are evaluating a batch of {n} candidate news items simultaneously.\n\n"
    ]
    if extra_context:
        user_payload.append(f"=== ADDITIONAL CONTEXT / BACKGROUND TO CONSIDER ===\n{extra_context}\n\n")
    user_payload.extend([
        f"=== CANDIDATES TO EVALUATE ({n} total) ===\n{json.dumps(clean_candidates, separators=(',', ':'), ensure_ascii=False)}\n\n",
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
                return call_agnes_api(key, system_instruction, user_payload_str, model=model), pre_harvested_urls
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
                
                v_safety_settings = [
                    vertex_types.SafetySetting(
                        category=vertex_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=vertex_types.HarmBlockThreshold.BLOCK_NONE
                    ),
                    vertex_types.SafetySetting(
                        category=vertex_types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=vertex_types.HarmBlockThreshold.BLOCK_NONE
                    ),
                    vertex_types.SafetySetting(
                        category=vertex_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=vertex_types.HarmBlockThreshold.BLOCK_NONE
                    ),
                    vertex_types.SafetySetting(
                        category=vertex_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=vertex_types.HarmBlockThreshold.BLOCK_NONE
                    ),
                ]
                
                v_tools_list = None
                if use_search:
                    v_tools_list = [vertex_types.Tool(google_search=vertex_types.GoogleSearch())]
                    
                v_thinking_config = None
                if thinking_level != "OFF":
                    model_lower = base_model.lower()
                    if "gemini-3." in model_lower or "gemini-3-" in model_lower:
                        v_thinking_config = vertex_types.ThinkingConfig(
                            thinking_level=thinking_level.upper()
                        )
                    elif "gemini-2.5" in model_lower:
                        budget_map = {"LOW": 1024, "MEDIUM": 2048, "HIGH": 4096}
                        v_thinking_config = vertex_types.ThinkingConfig(
                            thinking_budget=budget_map.get(thinking_level.upper(), 2048)
                        )
                
                v_config = vertex_types.GenerateContentConfig(
                    temperature=0.15,
                    max_output_tokens=32768,
                    system_instruction=system_instruction,
                    safety_settings=v_safety_settings,
                    tools=v_tools_list,
                    thinking_config=v_thinking_config
                )
                
                response = v_client.models.generate_content(
                    model=base_model,
                    contents=user_payload_str,
                    config=v_config
                )
                
                result_text = ""
                if hasattr(response, 'candidates') and response.candidates:
                    cand = response.candidates[0]
                    if hasattr(cand, 'content') and cand.content and hasattr(cand.content, 'parts') and cand.content.parts:
                        non_thought_parts = []
                        for part in cand.content.parts:
                            if getattr(part, 'thought', False):
                                continue
                            if hasattr(part, 'text') and part.text:
                                non_thought_parts.append(part.text)
                        result_text = "".join(non_thought_parts).strip()
                
                if not result_text and hasattr(response, 'text') and response.text:
                    result_text = response.text.strip()
            else:
                if not genai_client:
                    raise ValueError("Gemini API client not initialized.")
                
                safety_settings = [
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE
                    ),
                ]
                
                # Only pass direct tools_list to models with active grounding quota (e.g. 2.5) if Stage 1 did not pre-ground
                tools_list = None
                if use_search and "gemini-2.5" in model.lower() and not pre_harvested_urls:
                    tools_list = [types.Tool(google_search=types.GoogleSearch())]
                
                thinking_config = None
                if thinking_level != "OFF":
                    model_lower = model.lower()
                    if "gemini-3." in model_lower or "gemini-3-" in model_lower:
                        thinking_config = types.ThinkingConfig(
                            thinking_level=thinking_level.upper()
                        )
                    elif "gemini-2.5" in model_lower:
                        budget_map = {"LOW": 1024, "MEDIUM": 2048, "HIGH": 4096}
                        thinking_config = types.ThinkingConfig(
                            thinking_budget=budget_map.get(thinking_level.upper(), 2048)
                        )

                config = types.GenerateContentConfig(
                    temperature=0.15,
                    max_output_tokens=65536,
                    system_instruction=system_instruction,
                    safety_settings=safety_settings,
                    tools=tools_list,
                    thinking_config=thinking_config
                )
                
                response = genai_client.models.generate_content(
                    model=model,
                    contents=user_payload_str,
                    config=config
                )
                
                result_text = ""
                if hasattr(response, 'candidates') and response.candidates:
                    cand = response.candidates[0]
                    if hasattr(cand, 'content') and cand.content and hasattr(cand.content, 'parts') and cand.content.parts:
                        non_thought_parts = []
                        for part in cand.content.parts:
                            if getattr(part, 'thought', False):
                                continue
                            if hasattr(part, 'text') and part.text:
                                non_thought_parts.append(part.text)
                        result_text = "".join(non_thought_parts).strip()
                
                if not result_text and hasattr(response, 'text') and response.text:
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
                                        raw_url = chunk.web.uri
                                        # Follow Google redirect to get the true destination URL and verify HTTP 200
                                        resolved_url = raw_url
                                        try:
                                            resp_check = requests.get(raw_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=6, allow_redirects=True)
                                            if resp_check.status_code == 200 and resp_check.url:
                                                resolved_url = resp_check.url
                                            else:
                                                continue # Skip dead/broken links
                                        except Exception:
                                            pass

                                        if resolved_url not in grounding_urls:
                                            grounding_urls.append(resolved_url)
                except Exception as ge:
                    print(f"  Warning checking grounding chunks: {ge}")

            return result_text, grounding_urls
        except Exception as e:
            err_str = str(e).lower()
            if "503" in err_str or "unavailable" in err_str or "high demand" in err_str:
                print(f"Server capacity spike (503 Unavailable) on model {model}. Trying fallback...")
            elif "429" in err_str or "exhausted" in err_str or "quota" in err_str:
                print(f"Rate limited or quota exhausted (429) on model {model}. Trying fallback...")
            elif "deadline" in err_str or "timeout" in err_str or "504" in err_str:
                print(f"Model {model} timed out after {GEMINI_TIMEOUT_SECS}s. Trying fallback...")
            else:
                print(f"Warning: Model {model} failed ({e}). Trying fallback...")
            last_exception = e
            time.sleep(1)
            
    print(f"CRITICAL: All models failed in one-shot batch evaluation. Last error: {last_exception}")
    sys.exit(1)

def sanitize_story_posts(posts, use_spiritual=False):
    import re
    clean = []
    for p in posts:
        p_str = str(p).strip()
        if p_str.startswith("Alethekanon:"):
            body = p_str.replace("Alethekanon:", "", 1).strip()
            body = re.sub(r"^\[Verified:[^\]]+\]\.?\s*", "", body, flags=re.IGNORECASE)
            body = re.sub(r"^Verified:\s*[^.\n]+\.?\s*", "", body, flags=re.IGNORECASE)
            body = re.sub(r"\n\nSource:\s*https?://\S+", "", body, flags=re.IGNORECASE).strip()
            p_str = f"Alethekanon:\n{body}"
        clean.append(p_str)
        
    if use_spiritual and clean:
        last_p = clean[-1]
        if not last_p.startswith("Spirithekanon:"):
            clean[-1] = f"Spirithekanon:\n{last_p}"
            
        # Ensure quotation marks around the passage
        lines = clean[-1].split("\n")
        if len(lines) >= 2:
            quote_idx = 1 if lines[0].startswith("Spirithekanon:") else 0
            quote_line = lines[quote_idx]
            if '"' not in quote_line:
                match = re.search(r'(\[?[0-9A-Za-z\s]+(?::|\s)\d+[^\]]*\]?\s*(?:PASS|FAIL|HIT|COND)?)', quote_line)
                if match:
                    cite_part = match.group(1)
                    passage_part = quote_line[:match.start()].strip()
                    lines[quote_idx] = f'"{passage_part}" {cite_part}'.strip()
                    clean[-1] = "\n".join(lines)
                
    # Auto-fit raw text posts destined for Bluesky under 280 chars
    for i in range(min(4, len(clean))):
        if len(clean[i]) > 280:
            lines = clean[i].split("\n")
            while len("\n".join(lines)) > 280 and len(lines) > 1:
                lines.pop()
            trimmed = "\n".join(lines).strip()
            if len(trimmed) > 280:
                trimmed = trimmed[:277] + "..."
            clean[i] = trimmed
            
    if use_spiritual and clean and len(clean[-1]) > 280:
        sp_text = clean[-1]
        if "\n" in sp_text:
            parts = sp_text.split("\n")
            header_quote = "\n".join(parts[:-1])
            reflection = parts[-1]
            avail = 280 - len(header_quote) - 1
            if avail > 20:
                reflection = reflection[:avail-3].strip() + "..."
                clean[-1] = f"{header_quote}\n{reflection}"
            else:
                clean[-1] = sp_text[:277] + "..."
        else:
            clean[-1] = sp_text[:277] + "..."
            
    return clean

def transpose_flat_to_json(flat_text, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all"):
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
        # 1. Handle dictionary item returned by model
        if isinstance(item, dict):
            try:
                posts_raw = item.get("posts") or []
                clean_posts = sanitize_story_posts(posts_raw, use_spiritual=use_spiritual)
                
                story = {
                    "thinking": str(item.get("thinking", "")).strip(),
                    "id": str(item.get("id", "")).strip(),
                    "subject": str(item.get("subject", "")).strip(),
                    "link": str(item.get("link", "")).strip(),
                    "target_url": str(item.get("target_url", "")).strip(),
                    "claim_u": float(item.get("claim_u", 0.0)),
                    "claim_psi": float(item.get("claim_psi", 0.0)),
                    "real_u": float(item.get("real_u", 0.0)),
                    "real_psi": float(item.get("real_psi", 0.0)),
                    "mode": str(item.get("mode", "root")).strip(),
                    "posts": clean_posts,
                    "actors": item.get("actors", []),
                    "macro_event": str(item.get("macro_event", "")).strip(),
                    "macro_claim_u": item.get("macro_claim_u"),
                    "macro_claim_psi": item.get("macro_claim_psi"),
                    "macro_real_u": item.get("macro_real_u"),
                    "macro_real_psi": item.get("macro_real_psi"),
                    "status": "COMPLETED DRY RUN"
                }
                if "claim_rnet" in item and item["claim_rnet"] is not None:
                    story["claim_rnet"] = float(item["claim_rnet"])
                if "real_rnet" in item and item["real_rnet"] is not None:
                    story["real_rnet"] = float(item["real_rnet"])
                if "claim_z" in item and item["claim_z"] is not None:
                    story["claim_z"] = int(item["claim_z"])
                if "real_z" in item and item["real_z"] is not None:
                    story["real_z"] = int(item["real_z"])
                if "claim_z_profile" in item and isinstance(item["claim_z_profile"], list):
                    story["claim_z_profile"] = list(item["claim_z_profile"])
                if "real_z_profile" in item and isinstance(item["real_z_profile"], list):
                    story["real_z_profile"] = list(item["real_z_profile"])
                if "claim_integrity" in item and item["claim_integrity"] is not None:
                    story["claim_integrity"] = str(item["claim_integrity"]).strip()
                if "real_integrity" in item and item["real_integrity"] is not None:
                    story["real_integrity"] = str(item["real_integrity"]).strip()
                if "stated_forces" in item and isinstance(item["stated_forces"], dict):
                    story["stated_forces"] = item["stated_forces"]
                if "actual_forces" in item and isinstance(item["actual_forces"], dict):
                    story["actual_forces"] = item["actual_forces"]
                if "aspects" in item and isinstance(item["aspects"], list):
                    story["aspects"] = item["aspects"]
                    story["multiAspect"] = True
                elif use_multi_aspect:
                    story["multiAspect"] = True
                if use_spiritual:
                    story["spiritual"] = True
                    story["spiritual_traditions"] = resolve_spiritual_traditions(spiritual_traditions)
                evaluations.append(story)
                continue
            except Exception as e:
                print(f"Warning: Failed to parse dict item {idx}: {e}")
                continue

        # 2. Handle list item returned by model
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

            clean_posts = sanitize_story_posts(item[10], use_spiritual=use_spiritual)

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
                "posts": clean_posts,
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
            if len(item) >= 26 and isinstance(item[25], dict):
                story["stated_forces"] = item[25]
            if len(item) >= 27 and isinstance(item[26], dict):
                story["actual_forces"] = item[26]
            if len(item) >= 28 and isinstance(item[27], list):
                story["aspects"] = item[27]
                story["multiAspect"] = True
            elif use_multi_aspect:
                story["multiAspect"] = True
            
            if use_spiritual:
                story["spiritual"] = True
                story["spiritual_traditions"] = resolve_spiritual_traditions(spiritual_traditions)

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
            if not isinstance(posts, list) or len(posts) == 0:
                print(f"ERROR: Story '{story.get('subject')}' has empty or invalid posts. Skipping.")
                continue

            # Character limit warnings (only check first 4 posts for compact mode)
            is_compact = story.get("compact") is True or story.get("compact") == "single"
            posts_to_check = posts[:4] if is_compact else posts
            violations = [(i, len(p)) for i, p in enumerate(posts_to_check) if len(p) > 299]
            if violations:
                print(f"WARNING: '{story.get('subject')}' has char violations at posts {violations}")
            story["posts"] = posts

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
    parser.add_argument("--multi-aspect", action="store_true", help="Enable Multi-Aspect and Multi-Actor convergence test audits")
    parser.add_argument("--spiritual", action="store_true", help="Enable spiritual/scriptural optional audit mode")
    parser.add_argument("--spiritual-traditions", type=str, default="all", help="Comma-separated spiritual/scriptural traditions to draw from (e.g. 'christianity,hinduism,buddhism,taoism,other', default: 'all')")
    parser.add_argument("--five-word", action="store_true", help="Enable 5-word limit mode")
    parser.add_argument("--rss", type=int_or_default(0), default=5, help="Number of RSS stories to harvest (default: 5)")
    parser.add_argument("--bsky", type=int_or_default(0), default=15, help="Number of Bluesky stories to harvest (default: 15)")
    parser.add_argument("--model", type=str, default="gemini-3.5-flash", help="Generative model to use (default: gemini-3.5-flash)")
    parser.add_argument("--context", type=str, default=None, help="Additional context/background knowledge to send to the evaluator model")
    parser.add_argument("--model-sequence", type=str, default=None, help="Comma-separated list of models to try in sequence (overriding default fallbacks)")
    parser.add_argument("--chunk-size", type=int_or_default(1), default=1, help="Number of stories to process per API call (default: 1)")
    parser.add_argument("--category", type=str, default="all", help="Category (or comma-separated categories) of news to harvest (default: all). E.g. 'politics,tech'")
    parser.add_argument("--topic", type=str, default=None, help="Specific topic query to filter/search for (e.g. 'Ukraine', 'Trump')")
    parser.add_argument("--banned-topic", type=str, default=None, help="Comma-separated topics/keywords to exclude from harvesting (overrides/extends local banlist)")
    parser.add_argument("--thinking-level", type=str, default="MEDIUM", choices=["OFF", "LOW", "MEDIUM", "HIGH"], help="Gemini API thinking level/mode (default: MEDIUM)")
    parser.add_argument("--roundup", action="store_true", help="After evaluation, run consolidate_roundups to group overlapping stories into roundup threads (default: False)")
    parser.add_argument("--prefer", type=str, default="", help=(
        "Preferred outlets to prioritize. Comma-separated list of domains or numbers:\n"
        "1: Bloomberg, 2: NY Times, 3: The Saturday Paper, 4: Reuters, 5: BBC News,\n"
        "6: SMH, 7: TechCrunch, 8: Washington Post, 9: NPR.\n"
        "E.g., --prefer '1,2,5,theguardian.com'"
    ))
    parser.add_argument("--enabled-feeds", type=str, default=None, help="Comma-separated feed names (or URLs) to enable for harvesting.")
    parser.add_argument("--probe", type=str, default=None, help="Trigger Research Probe mode: query historical events or specific topics (e.g. 'Hitler 1933', 'Albanese housing policy')")
    parser.add_argument("--candidates", type=str, default=None, help="Path to existing candidate JSON file to evaluate directly (skips harvesting)")
    parser.add_argument("--policy-report", action="store_true", help="Print a formatted policy tracking report from policy_ledger.json and exit")
    args = parser.parse_args()
    
    if args.policy_report:
        try:
            from policy_extract import DEFAULT_LEDGER_PATH
            if os.path.exists(DEFAULT_LEDGER_PATH):
                with open(DEFAULT_LEDGER_PATH, "r", encoding="utf-8") as f:
                    ledger_data = json.load(f)
                policies = ledger_data.get("policies", {})
                print("=" * 60)
                print("ALETHEIA POLICY LEDGER REPORT")
                print(f"Last updated: {ledger_data.get('last_updated', 'N/A')}")
                print("=" * 60)
                for slug, p in sorted(policies.items(), key=lambda x: x[1].get("story_count", 0), reverse=True):
                    print(f"\n• {p.get('name')} ({slug})")
                    print(f"  Stories: {p.get('story_count')} | Pass: {p.get('pass_count', 0)} | Fail: {p.get('fail_count', 0)}")
                    print(f"  Avg Coords (υ, ψ): ({p.get('avg_real_u')}, {p.get('avg_real_psi')})")
                    print(f"  Timeline: {p.get('first_seen')} -> {p.get('last_updated')}")
            else:
                print("No policy ledger found at policy_ledger.json.")
        except Exception as pe:
            print(f"Error reading policy ledger: {pe}")
        sys.exit(0)

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
    
    if args.candidates:
        scratch_candidates_path = os.path.abspath(args.candidates)
        print(f"Using pre-existing candidates file: {scratch_candidates_path}")
    elif args.probe:
        probe_script = os.path.join(script_dir, "research_probe.py")
        limit = (args.rss or 0) + (args.bsky or 0)
        if limit <= 0:
            limit = 5
        cmd = [
            sys.executable,
            probe_script,
            "--probe", args.probe,
            "--limit", str(limit)
        ]
        if args.probe_year:
            cmd.extend(["--year", str(args.probe_year)])
        # Provide contextual prompt note
        probe_note = f"This is a historical/thematic research probe on: '{args.probe}'. Evaluate the actor's stated vs actual alignment in historical/policy context."
        if args.context:
            args.context = f"{args.context}\n{probe_note}"
        else:
            args.context = probe_note
            
        print(f"Executing: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Probe script failed with exit code {e.returncode}")
            sys.exit(1)
        scratch_candidates_path = os.path.join(script_dir, "harvested_candidates.json")
    else:
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
    min_tf = len(minify_markdown(extract_thread_content_rules(open(formatting_path, "r", encoding="utf-8").read())))
    
    raw_total_chars = raw_ct + raw_tf
    min_total_chars = min_ct + min_tf
    percent_saved = (1.0 - (min_total_chars / raw_total_chars)) * 100
    
    print(f"\n--- PROMPT TOKENS MINIFICATION ---")
    print(f"Raw instructions size:      {raw_total_chars} characters (~{int(raw_total_chars/4)} tokens)")
    print(f"Minified instructions size: {min_total_chars} characters (~{int(min_total_chars/4)} tokens)")
    print(f"Total instructions token budget saved: {percent_saved:.1f}%")
    print(f"----------------------------------\n")
    
    # Process candidates: Grounding in batches of max 5, Auditing in chunks of args.chunk_size
    chunk_size = args.chunk_size
    all_evaluations = []
    MAX_RETRIES_PER_CHUNK = 2

    # 1. Partition search grounding batches (always batches of up to 5)
    GROUNDING_BATCH_SIZE = 5
    grounding_batches = [candidates[i:i + GROUNDING_BATCH_SIZE] for i in range(0, len(candidates), GROUNDING_BATCH_SIZE)]
    total_g_batches = len(grounding_batches)

    # 2. Partition audit chunks (user-configured manual chunk size)
    chunks = [candidates[i:i + chunk_size] for i in range(0, len(candidates), chunk_size)]
    total_chunks = len(chunks)
    
    from concurrent.futures import ThreadPoolExecutor
    grounding_executor = ThreadPoolExecutor(max_workers=2)
    pre_grounding_futures = {}
    pre_grounded_batches = {}

    # Sequential first grounding batch to guarantee grounded facts before initial audit begins
    if args.search and genai_client and total_g_batches > 0:
        first_count = len(grounding_batches[0])
        print(f"\n[Pipeline Init] Grounding Batch 1/{total_g_batches} (stories 1-{first_count}) sequentially before initial audit launch...")
        dossier_0, urls_0 = harvest_search_grounding(genai_client, grounding_batches[0])
        pre_grounded_batches[0] = (dossier_0, urls_0)
        
        # Start pre-fetching Grounding Batch 2 in background while Chunk 1 audits
        if total_g_batches > 1:
            second_count = len(grounding_batches[1])
            print(f"[Pipeline Prefetch] Launching background grounding for Batch 2/{total_g_batches} (stories {first_count+1}-{first_count+second_count})...")
            pre_grounding_futures[1] = grounding_executor.submit(harvest_search_grounding, genai_client, grounding_batches[1])

    for chunk_idx, chunk in enumerate(chunks):
        chunk_num = chunk_idx + 1
        print(f"\nEvaluating chunk {chunk_num}/{total_chunks} ({len(chunk)} candidates)...")

        # Retrieve pre-grounded dossier covering the candidates in this chunk
        cur_dossier_parts = []
        cur_urls = []
        if args.search:
            start_cand_idx = chunk_idx * chunk_size
            end_cand_idx = start_cand_idx + len(chunk)
            
            start_g_batch = start_cand_idx // GROUNDING_BATCH_SIZE
            end_g_batch = (end_cand_idx - 1) // GROUNDING_BATCH_SIZE
            
            for g_idx in range(start_g_batch, end_g_batch + 1):
                if g_idx in pre_grounded_batches:
                    g_dossier, g_urls = pre_grounded_batches[g_idx]
                elif g_idx in pre_grounding_futures:
                    try:
                        g_dossier, g_urls = pre_grounding_futures[g_idx].result()
                        pre_grounded_batches[g_idx] = (g_dossier, g_urls)
                    except Exception as ex:
                        print(f"  Warning: Prefetched grounding batch {g_idx+1} failed ({ex}). Retrying synchronously...")
                        g_dossier, g_urls = harvest_search_grounding(genai_client, grounding_batches[g_idx])
                        pre_grounded_batches[g_idx] = (g_dossier, g_urls)
                else:
                    g_dossier, g_urls = harvest_search_grounding(genai_client, grounding_batches[g_idx])
                    pre_grounded_batches[g_idx] = (g_dossier, g_urls)
                    
                if g_dossier:
                    cur_dossier_parts.append(g_dossier)
                for u in g_urls:
                    if u not in cur_urls:
                        cur_urls.append(u)
                        
            # Prefetch next grounding batch ahead of time if not already started
            next_g_batch = end_g_batch + 1
            if next_g_batch < total_g_batches and next_g_batch not in pre_grounding_futures and next_g_batch not in pre_grounded_batches:
                print(f"[Pipeline Prefetch] Launching background grounding for Batch {next_g_batch + 1}/{total_g_batches}...")
                pre_grounding_futures[next_g_batch] = grounding_executor.submit(harvest_search_grounding, genai_client, grounding_batches[next_g_batch])

        cur_dossier = "\n\n".join(cur_dossier_parts)

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
                is_spiritual_active = args.spiritual or (args.spiritual_traditions and args.spiritual_traditions.lower().strip() != "all")
                is_multi_aspect_active = args.multi_aspect or any(c.get("is_multi_source") for c in remaining)
                raw_text, grounding_urls = run_one_shot_evaluations(
                    genai_client, remaining, args.model, agnes_api_key=agnes_api_key, 
                    use_son=args.son, use_search=args.search,
                    extra_context=args.context, model_sequence=model_seq,
                    compact=compact_val, five_word=args.five_word,
                    thinking_level=args.thinking_level,
                    use_multi_aspect=is_multi_aspect_active,
                    use_spiritual=is_spiritual_active,
                    spiritual_traditions=args.spiritual_traditions,
                    pre_grounded_dossier=cur_dossier,
                    pre_harvested_urls=cur_urls
                )
                parsed = transpose_flat_to_json(raw_text, use_multi_aspect=is_multi_aspect_active, use_spiritual=is_spiritual_active, spiritual_traditions=args.spiritual_traditions)

                # Attach multi-source metadata from candidate objects
                cand_map = {normalize_url(c.get("url", "")): c for c in remaining if c.get("url")}
                for it in parsed:
                    if isinstance(it, dict):
                        cand_match = cand_map.get(normalize_url(it.get("link", "")))
                        if cand_match:
                            if cand_match.get("cluster_sources"):
                                it["cluster_sources"] = cand_match["cluster_sources"]
                            if cand_match.get("is_multi_source"):
                                it["is_multi_source"] = True
                            if cand_match.get("cross_source_dossier"):
                                it["cross_source_dossier"] = cand_match["cross_source_dossier"]

                # Conditional Second-Pass Fact-Checking Reflection for High Hypocrisy/Distortion
                if args.search:
                    reflected_parsed = []
                    for idx, item in enumerate(parsed):
                        trigger_reflection = False
                        claim_rnet = 0.0
                        real_rnet = 0.0
                        hypocrisy = 0.0

                        if args.son and isinstance(item, list) and len(item) >= 25:
                            try:
                                claim_rnet = float(item[17]) if item[17] is not None else 0.0
                                real_rnet = float(item[18]) if item[18] is not None else 0.0
                                hypocrisy = abs(real_rnet - claim_rnet)
                            except (ValueError, TypeError):
                                pass
                            # Trigger if real R_net > 2.0 (distorted/deception) or delta > 2.0
                            if real_rnet > 2.0 or hypocrisy > 2.0:
                                trigger_reflection = True
                        elif not args.son and isinstance(item, list) and len(item) >= 9:
                            try:
                                claim_u = float(item[5])
                                claim_psi = float(item[6])
                                real_u = float(item[7])
                                real_psi = float(item[8])
                                hypocrisy = abs(real_u - claim_u) + abs(real_psi - claim_psi)
                            except (ValueError, TypeError):
                                pass
                            if hypocrisy > 1.5:
                                trigger_reflection = True

                        if trigger_reflection:
                            desc = f"R_net={real_rnet:.2f}, delta={hypocrisy:.2f}" if args.son else f"hypocrisy={hypocrisy:.2f}"
                            print(f"  [REFLECT] High hypocrisy/distortion detected ({desc}) for item {idx}: {item[2]}")
                            print("  Executing second-pass fact-checking search grounding reflection...")

                            orig_cand = None
                            if idx < len(chunk):
                                orig_cand = chunk[idx]
                            else:
                                url_clean = normalize_url(item[3])
                                for c in chunk:
                                    if normalize_url(c.get("url", "")) == url_clean:
                                        orig_cand = c
                                        break

                            if orig_cand:
                                reflection_context = (args.context or "") + (
                                    f"\n\n[HYPOCRISY ALERT - REFLECTION REQUIRED]\n"
                                    f"Your initial analysis detected high hypocrisy/distortion ({desc}).\n"
                                    f"You MUST use Google Search Grounding to perform a deep fact-checking reflection. Search for concrete evidence about the actors' claims vs. actual outcomes. "
                                    f"Ensure that all 13 posts are thoroughly grounded in these verified facts, exposing any deceit or empty rhetoric."
                                )
                                try:
                                    ref_raw, ref_grounding = run_one_shot_evaluations(
                                        genai_client, [orig_cand], args.model, agnes_api_key=agnes_api_key,
                                        use_son=args.son, use_search=True, # Force search grounding ON
                                        extra_context=reflection_context, model_sequence=model_seq,
                                        compact=compact_val, five_word=args.five_word,
                                        thinking_level=args.thinking_level,
                                        use_multi_aspect=args.multi_aspect,
                                        use_spiritual=is_spiritual_active,
                                        spiritual_traditions=args.spiritual_traditions
                                    )
                                    ref_parsed = transpose_flat_to_json(ref_raw, use_multi_aspect=args.multi_aspect, use_spiritual=is_spiritual_active, spiritual_traditions=args.spiritual_traditions)
                                    if ref_parsed and len(ref_parsed) > 0:
                                        item = ref_parsed[0]
                                        print(f"  [REFLECT SUCCESS] Successfully updated story '{item[2]}' with grounded facts.")
                                        if ref_grounding:
                                            if not grounding_urls:
                                                grounding_urls = []
                                            for u in ref_grounding:
                                                if u not in grounding_urls:
                                                    grounding_urls.append(u)
                                except Exception as re:
                                    print(f"  Warning: Reflection API call failed: {re}. Falling back to initial evaluation.")
                        reflected_parsed.append(item)
                    parsed = reflected_parsed

                
                # If search was actually used, append 🌐 to post 1 and record grounding URL as metadata
                if grounding_urls:
                    print(f"  Google Search grounding detected with {len(grounding_urls)} source(s).")
                    primary_url = grounding_urls[0]
                    # Strip tracking parameters to save character space
                    if "?" in primary_url:
                        primary_url = primary_url.split("?")[0]
                    primary_url = primary_url.strip()
                    
                    for item in parsed:
                        if isinstance(item, dict):
                            item["grounding_url"] = primary_url
                            posts = item.get("posts", [])
                            if posts and len(posts) > 0:
                                first_post = posts[0]
                                if "🌐" not in first_post:
                                    posts[0] = first_post.rstrip() + " 🌐"
                        elif isinstance(item, list) and len(item) > 10:
                            if isinstance(item[10], list) and len(item[10]) > 0:
                                first_post = item[10][0]
                                if "🌐" not in first_post:
                                    item[10][0] = first_post.rstrip() + " 🌐"

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
            print("  Promoting, generating graphs, and fast-registering immediately...")
            promote_and_register_selector(args.son)
            print("  Chunk successfully promoted and registered.")
            
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

    print("\nBatch evaluation finished. Synchronizing final registries...")
    rebuild_registries_selector(args.son)
    print("\nOne-Shot Batch Evaluation Pipeline Completed Successfully!")

if __name__ == "__main__":
    main()
