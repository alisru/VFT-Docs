import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('stories_registry.js', 'r', encoding='utf-8') as f:
    text = f.read()[len('window.ALETHEIA_STORIES_REGISTRY = '):].rstrip(';\n')

data = json.loads(text)

commentary_cues = [
    'the article', 'the piece', 'the essay', 'the commentary', 'partisan commentary', 
    'the op-ed', 'this piece', 'the headline', 'partisan media', 'media framing',
    'media weaponized', 'punditry', 'culture war', 'weaponizing', 'romanticizing', 
    'cherry-pick', 'fearmonger', 'manufacture outrage', 'manufacture existential', 
    'manufacture an election crisis', 'sensationalist', 'stoking panic', 'stoke outrage'
]

def get_outlet(link):
    try:
        host = link.split('/')[2].replace('www.', '').lower()
        return host
    except:
        return 'unknown'

def is_article_failing(s):
    posts = s.get('posts', [])
    p3 = (posts[3] if len(posts) > 3 else '').lower()
    return any(c in p3 for c in commentary_cues)

outlets = ['propublica.org', 'thefederalist.com', 'breitbart.com', 'abc.net.au', 'nytimes.com', 'npr.org', 'foxnews.com']

header = f"{'OUTLET':<20} | {'TOTAL':<5} | {'ARTICLE BLAMED':<18} | {'INSTITUTION BLAMED':<18}"
print(header)
print('-'*len(header))

for out in outlets:
    stories = [s for s in data if get_outlet(s.get('link', '')) == out]
    art_blamed = sum(1 for s in stories if is_article_failing(s))
    total = len(stories)
    inst_blamed = total - art_blamed
    pct = (art_blamed / total * 100) if total > 0 else 0
    print(f"{out:<20} | {total:<5} | {art_blamed:<5} ({pct:4.1f}%)    | {inst_blamed:<5}")
