import json
import os

def load_story(fn):
    p = f'bluesky_bot/stories/{fn}'
    if not os.path.exists(p):
        p = f'bluesky_bot/stories/drafts/{fn}'
    d = json.load(open(p, encoding='utf-8'))
    return d[0] if isinstance(d, list) else d

# Check bill-maher, cdc-measles, cranbury-nj
for fn in ['factcheck_bill-maher-la-mayor.json', 'factcheck_cdc-measles-5000-2026.json', 'factcheck_cranbury-nj-wire-fraud-election-delay.json']:
    s = load_story(fn)
    print(f"=== {fn} ===")
    for idx, p in enumerate(s.get('posts', [])):
        print(f"[{idx}] {p[:60]}... ({len(p)} chars)")
