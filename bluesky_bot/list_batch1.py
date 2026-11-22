import json
import os

batch = json.load(open('bluesky_bot/batch_agent1.json', encoding='utf-8'))
for i, fn in enumerate(batch):
    p = f'bluesky_bot/stories/{fn}'
    in_drafts = False
    if not os.path.exists(p):
        p = f'bluesky_bot/stories/drafts/{fn}'
        in_drafts = True
    d = json.load(open(p, encoding='utf-8'))
    s = d[0] if isinstance(d, list) else d
    posts = s.get('posts', [])
    aspects = s.get('aspects', [])
    
    # check post personas
    has_aww = any('Awwthekanon:' in p for p in posts)
    has_bro = any('Brothekanon:' in p for p in posts)
    has_alethe = any('Alethekanon:' in p for p in posts)
    has_spirit = any('Spirithekanon:' in p for p in posts)
    
    # max length
    max_len = max([len(p) for p in posts]) if posts else 0
    
    print(f"[{i+1:02d}] {fn} | posts={len(posts)} | asp={len(aspects)} | aww={has_aww} bro={has_bro} | max_len={max_len} | drafts={in_drafts} | status={s.get('status')}")
