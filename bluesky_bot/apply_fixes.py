import os
import re

bot_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Update harvest_candidates.py
harvest_path = os.path.join(bot_dir, "harvest_candidates.py")
with open(harvest_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    # 1. scrape_via_tavily
    (
        '''            if results:
                raw_content = results[0].get("raw_content", "") or ""
                return "Article", "", raw_content''',
        '''            if results:
                raw_content = results[0].get("raw_content", "") or ""
                path_slug = urllib.parse.urlparse(url).path.strip('/').split('/')[-1]
                slug_title = re.sub(r'[-_]+', ' ', path_slug).title()
                return (slug_title or "News Report"), "", raw_content'''
    ),
    # 2. search_counter_sources_tavily
    (
        '''        for r in results:
            r_url = r.get("url", "")
            r_title = r.get("title", "")
            r_content = r.get("content", "").strip()
            if not r_url or not r_content or len(r_content) < 150:
                continue

            try:
                r_host = urllib.parse.urlparse(r_url).hostname or ""
                if r_host.startswith("www."):
                    r_host = r_host[4:]
            except Exception:
                continue

            if not r_host or r_host in seen_domains:
                continue''',
        '''        for r in results:
            r_url = r.get("url", "")
            r_title = r.get("title", "")
            r_content = r.get("content", "").strip()
            if not r_url or not r_content or len(r_content) < 150:
                continue

            if "tavily.com" in r_url:
                continue

            try:
                r_host = urllib.parse.urlparse(r_url).hostname or ""
                if r_host.startswith("www."):
                    r_host = r_host[4:]
            except Exception:
                continue

            if not r_host or "tavily.com" in r_host or r_host in seen_domains:
                continue

            if not is_news_url(r_url):
                continue'''
    ),
    # 3. cluster_candidate_stories
    (
        '''            if jaccard >= similarity_threshold or len(intersection) >= 2:
                cluster.append(c)
                placed = True
                break''',
        '''            if jaccard >= similarity_threshold:
                cluster.append(c)
                placed = True
                break'''
    ),
    # 4. NON_NEWS_DOMAINS
    (
        '''NON_NEWS_DOMAINS = {
    'bsky.app', 'bsky.social', 'graze.social',''',
        '''NON_NEWS_DOMAINS = {
    'tavily.com', 'api.tavily.com',
    'bsky.app', 'bsky.social', 'graze.social','''
    ),
    # 5. UNSCRAPABLE_DOMAINS
    (
        '''UNSCRAPABLE_DOMAINS = {
    'pbs.org', 'reut.rs', 'reuters.com',
    'on.wsj.com', 'wsj.com',
    'bloom.bg', 'bloomberg.com',
    'nyti.ms', 'nytimes.com',
    'washingtonpost.com', 'wapo.st',
    'ft.com', 'economist.com', 'afr.com'
}''',
        '''UNSCRAPABLE_DOMAINS = {
    'pbs.org', 'reut.rs',
    'on.wsj.com',
    'bloom.bg',
    'nyti.ms',
    'washingtonpost.com', 'wapo.st',
    'afr.com'
}'''
    ),
    # 6. is_news_url
    (
        '''AD_OR_LIFESTYLE_PATH_SEGMENTS = {
    'lifestyle', 'tvshowbiz', 'femail', 'shopping', 'deals', 'coupons',
    'promotions', 'sponsored', 'advertisement', 'native-content',
    'partner-content', 'affiliate', 'horoscopes', 'puzzles', 'recipes',
    'advertisements', 'ad', 'ads', 'sponsored-content', 'commercial', 'brand-spotlight'
}

def is_news_url(url):
    if not url:
        return False
    u = url.strip().lower()
    if not u.startswith(('http://', 'https://')):
        return False
    try:
        parsed = urllib.parse.urlparse(u)
        host = parsed.hostname or ""
        path = parsed.path.lower()
    except Exception:
        return False
    if not host:
        return False
    if any(host == bad or host.endswith('.' + bad) for bad in NON_NEWS_DOMAINS):
        return False
    if any(host == bad or host.endswith('.' + bad) for bad in DYNAMIC_BANNED_DOMAINS):
        return False
    # Filter out lifestyle, celebrity showbiz, deals, shopping, and sponsored sections
    path_parts = [p.strip() for p in path.split('/') if p.strip()]
    if any(part in AD_OR_LIFESTYLE_PATH_SEGMENTS for part in path_parts):
        return False
    return True''',
        '''AD_OR_LIFESTYLE_PATH_SEGMENTS = {
    'lifestyle', 'tvshowbiz', 'femail', 'shopping', 'deals', 'coupons',
    'promotions', 'sponsored', 'advertisement', 'native-content',
    'partner-content', 'affiliate', 'horoscopes', 'puzzles', 'recipes',
    'advertisements', 'ad', 'ads', 'sponsored-content', 'commercial', 'brand-spotlight'
}

CORPORATE_OR_NON_NEWS_PATHS = {
    'about', 'about-us', 'pricing', 'plans', 'login', 'signin', 'signup',
    'register', 'terms', 'privacy', 'careers', 'jobs', 'team', 'features',
    'product', 'solutions', 'docs', 'documentation', 'knowledge', 'help',
    'faq', 'support'
}

def is_news_url(url):
    if not url:
        return False
    u = url.strip().lower()
    if not u.startswith(('http://', 'https://')):
        return False
    try:
        parsed = urllib.parse.urlparse(u)
        host = parsed.hostname or ""
        path = parsed.path.lower()
    except Exception:
        return False
    if not host:
        return False
    if any(host == bad or host.endswith('.' + bad) for bad in NON_NEWS_DOMAINS):
        return False
    if not is_domain_whitelisted(host):
        if any(host == bad or host.endswith('.' + bad) for bad in DYNAMIC_BANNED_DOMAINS):
            return False
    # Reject bare root homepages and empty paths
    path_parts = [p.strip() for p in path.split('/') if p.strip()]
    if not path_parts or path in ('', '/', '/index.html', '/index.php'):
        return False
    # Filter out corporate / non-news paths
    if any(part in CORPORATE_OR_NON_NEWS_PATHS for part in path_parts):
        return False
    # Filter out lifestyle, celebrity showbiz, deals, shopping, and sponsored sections
    if any(part in AD_OR_LIFESTYLE_PATH_SEGMENTS for part in path_parts):
        return False
    if len(path_parts) == 1 and len(path_parts[0]) < 8 and not re.search(r'\\d+', path_parts[0]):
        return False
    return True'''
    ),
    # 7. is_banned
    (
        '''def is_banned(text, url, banned_keywords):
    if is_ad_text(text):
        return True
    if not banned_keywords:
        return False
    text_lower = text.lower()
    url_lower = url.lower() if url else ""
    for bk in banned_keywords:
        pattern = rf"\\b{re.escape(bk)}\\b"
        if re.search(pattern, text_lower) or (url_lower and re.search(pattern, url_lower)):
            return True
        if " " in bk:
            variants = [bk.replace(" ", "-"), bk.replace(" ", "_"), bk.replace(" ", "")]
            for var in variants:
                var_pattern = rf"\\b{re.escape(var)}\\b"
                if re.search(var_pattern, text_lower) or (url_lower and re.search(var_pattern, url_lower)):
                    return True
    return False''',
        '''def is_banned(text, url, banned_keywords):
    if is_ad_text(text):
        return True
    if not banned_keywords:
        return False
    text_lower = text.lower()
    url_lower = url.lower() if url else ""
    for bk in banned_keywords:
        pattern = rf"(?<!\\w){re.escape(bk)}(?!\\w)"
        if re.search(pattern, text_lower) or (url_lower and re.search(pattern, url_lower)):
            return True
        if " " in bk:
            variants = [bk.replace(" ", "-"), bk.replace(" ", "_"), bk.replace(" ", "")]
            for var in variants:
                var_pattern = rf"(?<!\\w){re.escape(var)}(?!\\w)"
                if re.search(var_pattern, text_lower) or (url_lower and re.search(var_pattern, url_lower)):
                    return True
    return False'''
    ),
    # 8. is_english
    (
        '''    non_eng_chars = re.compile(r'[áéíóúñ¿¡àèùçâêîôûëïüöäüß]', re.IGNORECASE)''',
        '''    non_eng_chars = re.compile(r'[áéíóúñ¿¡àèùçâêîôûëïüöäß]', re.IGNORECASE)'''
    )
]

for idx, (target, repl) in enumerate(replacements, 1):
    c_target = target.replace('\r\n', '\n')
    c_content = content.replace('\r\n', '\n')
    if c_target not in c_content:
        raise ValueError(f"Replacement {idx} target not found in harvest_candidates.py!")
    c_content = c_content.replace(c_target, repl.replace('\r\n', '\n'), 1)
    content = c_content

with open(harvest_path, "w", encoding="utf-8", newline="\r\n") as f:
    f.write(content)

print("harvest_candidates.py successfully updated.")

# 2. Update scraped_cache.py
cache_path = os.path.join(bot_dir, "scraped_cache.py")
with open(cache_path, "r", encoding="utf-8") as f:
    cache_content = f.read()

target_cache = '''def normalize_url(url):
    if not url:
        return ""
    url = sanitize_url(url)
    if "?" in url:
        url = url.split("?")[0]
    if "#" in url:
        url = url.split("#")[0]
    return url.lower().rstrip("/").strip()'''

repl_cache = '''def normalize_url(url):
    if not url:
        return ""
    url = sanitize_url(url)
    if "?" in url:
        url = url.split("?")[0]
    if "#" in url:
        url = url.split("#")[0]
    return url.lower().strip()'''

c_target_cache = target_cache.replace('\r\n', '\n')
c_cache_content = cache_content.replace('\r\n', '\n')
if c_target_cache not in c_cache_content:
    raise ValueError("Target not found in scraped_cache.py!")
c_cache_content = c_cache_content.replace(c_target_cache, repl_cache.replace('\r\n', '\n'), 1)

with open(cache_path, "w", encoding="utf-8", newline="\r\n") as f:
    f.write(c_cache_content)

print("scraped_cache.py successfully updated.")
