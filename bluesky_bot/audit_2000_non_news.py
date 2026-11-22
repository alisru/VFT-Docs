import os
import json
import re
import urllib.parse

script_dir = os.path.dirname(os.path.abspath(__file__))
live_dir = os.path.join(script_dir, "stories", "live")

NON_NEWS_DOMAINS = {
    'tavily.com', 'api.tavily.com', 'britannica.com', 'dictionary.com', 'merriam-webster.com',
    'wikipedia.org', 'wikimedia.org', 'wiktionary.org', 'wikiquote.org', 'wikinews.org', 'wikidata.org', 'fandom.com', 'wikia.com',
    'bsky.app', 'bsky.social', 'graze.social', 'twitter.com', 'x.com', 't.co',
    'youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com', 'facebook.com', 'fb.watch', 'threads.net',
    'reddit.com', 'redd.it', 'twitch.tv', 'discord.gg', 'discord.com',
    'linktr.ee', 'patreon.com', 'ko-fi.com', 'onlyfans.com', 'fansly.com',
    'amazon.com', 'amzn.to', 'etsy.com', 'shopify.com', 'gofundme.com',
    'pinterest.com', 'tumblr.com', 'mastodon.social', 'snapchat.com',
    'coinbase.com', 'binance.com', 'pump.fun', 'opensea.io',
    'arxiv.org', 'biorxiv.org', 'medrxiv.org', 'ssrn.com',
    'researchgate.net', 'academia.edu', 'semanticscholar.org',
    'doi.org', 'osf.io', 'philpapers.org', 'chemrxiv.org', 'techrxiv.org',
    'prnewswire.com', 'businesswire.com', 'globenewswire.com', 'prweb.com',
    'accesswire.com', 'marketwired.com', 'openpr.com', 'newswire.com',
    'einpresswire.com', 'prlog.org', 'issuewire.com', '24-7pressrelease.com',
    'slickdeals.net', 'dealnews.com', 'coupons.com', 'retailmenot.com',
    'producthunt.com', 'kickstarter.com', 'indiegogo.com'
}

CORPORATE_OR_NON_NEWS_PATHS = {'about', 'pricing', 'careers', 'terms', 'privacy', 'login', 'product', 'docs', 'help', 'contact', 'legal', 'faq'}

files = []
for f in os.listdir(live_dir):
    if f.startswith('factcheck_') and f.endswith('.json'):
        fp = os.path.join(live_dir, f)
        try:
            mt = os.path.getmtime(fp)
            files.append((mt, fp, f))
        except Exception:
            pass

files.sort(key=lambda x: x[0], reverse=True)
last_2000 = files[:2000]

violations = []
for mt, fp, fname in last_2000:
    try:
        data = json.load(open(fp, encoding='utf-8', errors='ignore'))
        s = data[0] if isinstance(data, list) and data else data
        link = (s.get('link') or '').strip()
        parsed = urllib.parse.urlparse(link)
        host = parsed.netloc.lower().split(':')[0]
        if host.startswith('www.'):
            host = host[4:]
        path = parsed.path.lower().strip()
        path_parts = [p.strip() for p in path.split('/') if p.strip()]

        reason = None
        if not link:
            reason = 'Empty Link'
        elif any(host == bad or host.endswith('.' + bad) for bad in NON_NEWS_DOMAINS):
            reason = f'Banned Non-News Domain: {host}'
        elif not path_parts or path in ('', '/', '/index.html', '/index.php'):
            reason = f'Bare Root Domain: {link}'
        elif any(part in CORPORATE_OR_NON_NEWS_PATHS for part in path_parts):
            reason = f'Corporate/Non-News Path: {path}'

        if reason:
            violations.append({
                'id': s.get('id', fname),
                'subject': s.get('subject', ''),
                'link': link,
                'reason': reason,
                'file': fname,
                'rkeys': len(s.get('rkeys', []))
            })
    except Exception as ex:
        pass

print(f"Total scanned: {len(last_2000)}")
print(f"Total violations found: {len(violations)}")

out_path = os.path.join(script_dir, "non_news_violations_last_2000.json")
with open(out_path, "w", encoding="utf-8") as out_f:
    json.dump(violations, out_f, indent=2, ensure_ascii=False)

for v in violations:
    print(f"[{v['reason']}] | id: {v['id']} | rkeys: {v['rkeys']} | link: {v['link']}")
