import os
import sys
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
import argparse
from dotenv import load_dotenv
from atproto import Client, IdResolver

script_dir = os.path.dirname(os.path.abspath(__file__))  # e:\Vector Field Theory\VFT Docs\bluesky_bot
root_dir = os.path.dirname(script_dir)                  # e:\Vector Field Theory\VFT Docs
bot_dir = script_dir                                    # e:\Vector Field Theory\VFT Docs\bluesky_bot
env_path = os.path.join(bot_dir, '.env')

# --- ARGUMENT PARSING ---
COMMON_OUTLETS = {
    "1": ["bloomberg.com"],
    "2": ["nytimes.com"],
    "3": ["thesaturdaypaper.com.au"],
    "4": ["reuters.com"],
    "5": ["bbc.com", "bbc.co.uk"],
    "6": ["smh.com.au"],
    "7": ["abc.net.au"],
    "8": ["techcrunch.com"],
    "9": ["washingtonpost.com"],
    "10": ["npr.org"]
}

parser = argparse.ArgumentParser(description="Harvest news candidates from RSS and Bluesky feeds.")
parser.add_argument("--rss-target", type=int, default=0, help="Target count for RSS feeds (default: 0)")
parser.add_argument("--bsky-target", type=int, default=40, help="Target count for Bluesky feeds (default: 40)")
parser.add_argument("--prefer", type=str, default="", help=(
    "Preferred outlets to prioritize. Comma-separated list of domains or numbers:\n"
    "1: Bloomberg, 2: NY Times, 3: The Saturday Paper, 4: Reuters, 5: BBC News,\n"
    "6: SMH, 7: ABC News AU, 8: TechCrunch, 9: Washington Post, 10: NPR.\n"
    "E.g., --prefer '1,2,5,theguardian.com'"
))
args = parser.parse_args()

TARGET_RSS = args.rss_target
TARGET_BSKY = args.bsky_target

# Parse preferred outlets from arguments if provided
PREFERRED_OUTLET_DOMAINS = []
if args.prefer:
    for token in args.prefer.split(","):
        token = token.strip().lower()
        if not token:
            continue
        if token in COMMON_OUTLETS:
            PREFERRED_OUTLET_DOMAINS.extend(COMMON_OUTLETS[token])
        else:
            PREFERRED_OUTLET_DOMAINS.append(token)

# --- 0. LOAD HISTORICAL EVALUATIONS (PREVENT DUPLICATE JUDGEMENTS) ---
print("Loading historical evaluations database to prevent duplicate judgements...")
seen_historical_urls = set()
seen_historical_ids = set()
historical_domain_counts = {}

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
                
                # Record historical URL and ID
                url = config.get("link") or config.get("target_url")
                if url:
                    url_clean = url.strip().lower()
                    seen_historical_urls.add(url_clean)
                    try:
                        import urllib.parse
                        host = urllib.parse.urlparse(url_clean).hostname
                        if host:
                            host = host.replace("www.", "")
                            historical_domain_counts[host] = historical_domain_counts.get(host, 0) + 1
                    except Exception:
                        pass
                    
                story_id = config.get("id")
                if story_id:
                    seen_historical_ids.add(story_id.strip().lower())
        except Exception as e:
            print(f"Warning: Failed to load historical evaluations from {scan_dir}: {e}")

print(f"Loaded {len(seen_historical_urls)} historical URLs and {len(seen_historical_ids)} historical story IDs.")


# --- 1. DYNAMIC STORY-LEVEL DE-DUPLICATION HEURISTIC ---
seen_story_keywords = set()

def is_duplicate_story(text, url):
    text_lower = text.lower()
    url_lower = url.strip().lower()
    
    # 1. Historical Check
    if url_lower in seen_historical_urls:
        print(f"  -> Historical duplicate URL detected! Skipping: {url}")
        return True
        
    subject_approx = text[:30].lower().replace(" ", "_").replace("/", "_")
    if subject_approx in seen_historical_ids:
        print(f"  -> Historical duplicate Story ID detected! Skipping: {subject_approx}")
        return True

    # 2. Batch-level conceptual check
    words = set(re.findall(r'\b[a-z]{5,}\b', text_lower))
    stopwords = {
        'about', 'after', 'again', 'against', 'almost', 'already', 'being', 'between', 
        'could', 'first', 'found', 'great', 'hours', 'house', 'under', 'would', 'years',
        'their', 'there', 'these', 'those', 'which', 'where', 'while', 'people', 'latest',
        'episode', 'today', 'report', 'called', 'officials', 'confirmed', 'court', 'state'
    }
    high_value_keywords = words - stopwords
    overlap = high_value_keywords & seen_story_keywords
    
    if overlap:
        print(f"  -> Batch-level conceptual duplicate detected! Skipping due to overlap of: {overlap}")
        return True
        
    seen_story_keywords.update(high_value_keywords)
    return False


# --- 2. EXTRACT EXTERNAL ARTICLE URL FROM BLUESKY POST ---
def extract_external_link(post):
    """Robustly extracts the actual external news story/article URL linked in a Bluesky post."""
    record = getattr(post, 'record', None)
    
    # A. Check record embed for external URI cards
    if record:
        embed = getattr(record, 'embed', None)
        if embed and hasattr(embed, 'external'):
            ext = getattr(embed, 'external', None)
            if ext and hasattr(ext, 'uri'):
                return ext.uri
                
    # B. Check record facets for link features
    facets = getattr(record, 'facets', None) or []
    for facet in facets:
        features = getattr(facet, 'features', [])
        for feature in features:
            if hasattr(feature, 'uri'):
                return feature.uri
                
    # C. Check post view embed
    embed_view = getattr(post, 'embed', None)
    if embed_view and hasattr(embed_view, 'external'):
        ext = getattr(embed_view, 'external', None)
        if ext and hasattr(ext, 'uri'):
            return ext.uri
            
    # D. Fallback to regex search in post text
    text = getattr(record, 'text', '') if record else ""
    url_match = re.search(r'(https?://[^\s]+)', text)
    if url_match:
        return url_match.group(1)
        
    # E. Check for domain abbreviations
    domain_match = re.search(r'\b([a-z0-9-]+\.[a-z]{2,}/[^\s]+)', text, re.IGNORECASE)
    if domain_match:
        return "https://" + domain_match.group(1)
        
    return None


# --- PREFERRED OUTLETS CONFIGURATION ---
def is_preferred_outlet(url):
    if not url or not PREFERRED_OUTLET_DOMAINS:
        return False
    u = url.strip().lower()
    try:
        import urllib.parse
        host = urllib.parse.urlparse(u).hostname or ""
    except Exception:
        host = ""
    if not host:
        host = u
    host = host.replace("www.", "")
    return any(host == pref or host.endswith('.' + pref) for pref in PREFERRED_OUTLET_DOMAINS)

def get_historical_count(url):
    if not url:
        return 999999
    u = url.strip().lower()
    try:
        import urllib.parse
        host = urllib.parse.urlparse(u).hostname or ""
    except Exception:
        host = ""
    if not host:
        host = u
    host = host.replace("www.", "")
    return historical_domain_counts.get(host, 0)

def get_sort_key(c):
    count = get_historical_count(c.get("url"))
    if PREFERRED_OUTLET_DOMAINS:
        pref = 0 if is_preferred_outlet(c.get("url")) else 1
        return (pref, count)
    return (0, count)


# --- 3. HARVEST FROM RSS FEEDS ---
print(f"\nHarvesting normal news from RSS feeds (Target: {TARGET_RSS})...")
rss_feeds = [
    {"name": "BBC News", "url": "http://feeds.bbci.co.uk/news/rss.xml"},
    {"name": "NYT Home", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"}
]

rss_candidates = []
seen_urls = set()

for feed in rss_feeds:
    if len(rss_candidates) >= TARGET_RSS:
        break
        
    print(f"Fetching from {feed['name']} RSS feed: {feed['url']}...")
    req = urllib.request.Request(feed['url'], headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
        root = ET.fromstring(content)
        items = root.findall('.//item')
        print(f"Found {len(items)} raw items in {feed['name']}.")
        
        for item in items:
            if len(rss_candidates) >= TARGET_RSS:
                break
                
            title = item.find('title')
            desc = item.find('description')
            link = item.find('link')
            
            title_text = title.text.strip() if title is not None and title.text else ""
            desc_text = desc.text.strip() if desc is not None and desc.text else ""
            link_text = link.text.strip() if link is not None and link.text else ""
            
            if not title_text or not link_text:
                continue
                
            desc_cleaned = re.sub(r'<[^>]*>', '', desc_text)
            text_body = f"{title_text}\n\n{desc_cleaned}"
            
            if len(text_body) < 45:
                continue
            if link_text in seen_urls:
                continue
                
            if is_duplicate_story(text_body, link_text):
                continue
                
            rss_candidates.append({
                "url": link_text,
                "target_url": "",
                "mode": "root",
                "text": text_body,
                "subject": title_text[:30].strip() + "..."
            })
            seen_urls.add(link_text)
            
    except Exception as e:
        print(f"Warning: Failed to fetch {feed['name']} RSS: {e}")

print(f"Harvested exactly {len(rss_candidates)} RSS candidates.")

# --- 4. HARVEST FROM BLUESKY FEEDS ---
print(f"\nHarvesting news from Bluesky feeds (Target: {TARGET_BSKY})...")
load_dotenv(env_path)
handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
password = os.environ.get('BSKY_PASSWORD')

bsky_candidates = []
seen_bsky_authors = set()

if password:
    print(f"Logging in to Bluesky as {handle}...")
    client = Client()
    try:
        client.login(handle, password)
        resolver = IdResolver()
        
        bsky_feeds = [
            "https://bsky.app/profile/aendra.com/feed/verified-news",
            "https://bsky.app/profile/aendra.com/feed/news-2-0"
        ]
        
        # Use strictly English words that rarely overlap with Dutch/German/French
        english_words = re.compile(r'\b(the|with|they|have|what|which|there|their|about|would|could|this|that|from|some|more|news|study|report|said|and|for|out|but|been|has|was|were)\b', re.IGNORECASE)
        cjk_re = re.compile(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]')
        
        def is_english(text):
            cleaned_text = re.sub(r'https?://[^\s]+', '', text)
            cleaned_text = re.sub(r'\b[a-zA-Z0-9-]+\.[a-z]{2,}/[^\s]*', '', cleaned_text)
            if cjk_re.search(cleaned_text):
                return False
            matches = english_words.findall(cleaned_text)
            return len(matches) >= 1
        for feed_url in bsky_feeds:
            print(f"Fetching from feed: {feed_url}...")
            parts = feed_url.strip("/").split("/")
            feed_handle, feed_rkey = parts[parts.index("profile")+1], parts[parts.index("feed")+1]
            
            feed_did = resolver.handle.resolve(feed_handle)
            feed_uri = f"at://{feed_did}/app.bsky.feed.generator/{feed_rkey}"
            
            feed_data = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 50})
            
            for item in feed_data.feed:
                # Skip if the post is a reply to another post (ensure it is a top comment)
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
                if post_url in seen_urls:
                    continue
                    
                # Robustly extract the external news article URL card
                article_url = extract_external_link(item.post)
                if not article_url or "bsky.app" in article_url.lower():
                    continue
                    
                banned_keywords = ["nsfw", "hentai", "waifu", "r18", "ecchi", "sexyai", "r34", "illustration", "art", "イラスト", "crypto", "dumped", "token", "solana", "bitcoin", "ethereum", "linktr.ee"]
                if any(banned in text.lower() or banned in article_url.lower() for banned in banned_keywords):
                    continue
                    
                # Perform unified de-duplication check using the actual article_url
                if is_duplicate_story(text, article_url):
                    continue
                    
                if author_handle in seen_bsky_authors:
                    continue
                    
                bsky_candidates.append({
                    "url": article_url,
                    "target_url": post_url,
                    "mode": "reply",
                    "text": text,
                    "subject": text[:30].strip() + "..."
                })
                seen_urls.add(article_url)
                seen_bsky_authors.add(author_handle)
                
        # Relaxation pass if slots still needed
        if len(bsky_candidates) < TARGET_BSKY:
            print(f"Retrying Bluesky feeds with relaxed author constraints to fill slots (Currently have {len(bsky_candidates)})...")
            for feed_url in bsky_feeds:
                parts = feed_url.strip("/").split("/")
                feed_handle, feed_rkey = parts[parts.index("profile")+1], parts[parts.index("feed")+1]
                feed_did = resolver.handle.resolve(feed_handle)
                feed_uri = f"at://{feed_did}/app.bsky.feed.generator/{feed_rkey}"
                feed_data = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 50})
                for item in feed_data.feed:
                    # Skip if the post is a reply to another post (ensure it is a top comment)
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
                    if not article_url or "bsky.app" in article_url.lower():
                        continue
                    if article_url in seen_urls or "graze.social" in article_url.lower() or "graze.social" in post_url.lower() or "graze.social" in text.lower():
                        continue
                    if len(text) < 45 or text.startswith('@') or text.startswith('Alethekanon'):
                        continue
                    if not is_english(text):
                        continue
                    if is_duplicate_story(text, article_url):
                        continue
                        
                    bsky_candidates.append({
                        "url": article_url,
                        "target_url": post_url,
                        "mode": "reply",
                        "text": text,
                        "subject": text[:30].strip() + "..."
                    })
                    seen_urls.add(article_url)
        
        # Sort Bluesky candidates: prioritize preferred if defined, and sort by least chosen domain count in ascending order
        bsky_candidates.sort(key=get_sort_key)
        
        # Log sorting results for visibility
        if bsky_candidates:
            print("\nBluesky Harvest Prioritization (least chosen outlets first):")
            for idx, c in enumerate(bsky_candidates[:15], 1):
                url = c.get("url")
                try:
                    import urllib.parse
                    host = urllib.parse.urlparse(url).hostname or url
                except Exception:
                    host = url
                print(f"  [{idx}] {host} (historical count: {get_historical_count(url)})")
                
        bsky_candidates = bsky_candidates[:TARGET_BSKY]
                
    except Exception as e:
        print(f"Warning: Bluesky login or retrieval failed: {e}")
else:
    print("Warning: BSKY_PASSWORD not found in env. Skipping Bluesky harvesting.")

print(f"Harvested and prioritized exactly {len(bsky_candidates)} Bluesky candidates.")

# --- 5. MERGE AND SAVE EXACTLY 20 DISTINCT PREMIUM STORIES ---
combined_candidates = []
max_len = max(len(rss_candidates), len(bsky_candidates))
for i in range(max_len):
    if i < len(rss_candidates):
        combined_candidates.append(rss_candidates[i])
    if i < len(bsky_candidates):
        combined_candidates.append(bsky_candidates[i])

# Ensure preferred outlets (if specified) and least-chosen outlets are placed at the absolute front of the final evaluation batch
all_final = combined_candidates[:TARGET_RSS + TARGET_BSKY]
all_final.sort(key=get_sort_key)
final_candidates = all_final

# Output path points to scratch/harvested_candidates.json relative to root workspace
output_path = os.path.join(root_dir, 'scratch', 'harvested_candidates.json')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(final_candidates, f, indent=2, ensure_ascii=False)
print(f"Candidates successfully saved to: {output_path}")

print(f"\nFinal combined premium candidates count: {len(final_candidates)}")
for idx, c in enumerate(final_candidates, 1):
    source = "Bluesky" if "bsky.app" in c["url"] else "RSS"
    try:
        print(f"[{idx}] [{source}] {c['url']} -> {c['text'][:80].replace('\n', ' ')}...")
    except Exception:
        # Fallback for Windows terminal unicode encoding errors
        try:
            print(f"[{idx}] [{source}] {c['url']} -> [Unicode Content]")
        except Exception:
            pass
