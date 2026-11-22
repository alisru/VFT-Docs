import json
import os

batch = json.load(open('bluesky_bot/batch_agent1.json', encoding='utf-8'))

for i, fn in enumerate(batch):
    p = f'bluesky_bot/stories/{fn}'
    src_p = p
    if not os.path.exists(p):
        src_p = f'bluesky_bot/stories/drafts/{fn}'
    d = json.load(open(src_p, encoding='utf-8'))
    s = d[0] if isinstance(d, list) else d
    
    posts = s.get('posts', [])
    aspects = s.get('aspects', [])
    
    # check structure of posts
    p3_verdict = posts[3].startswith('Verdict:') if len(posts) > 3 else False
    p4_subaudit = ('- ' in posts[4]) if len(posts) > 4 else False
    p5_context = len(posts) > 5 and not posts[5].startswith('- ') and not posts[5].startswith('The Bright Side:')
    
    issues = []
    if len(posts) != 15:
        issues.append(f"posts_len={len(posts)}")
    if len(aspects) < 2:
        issues.append(f"aspects_len={len(aspects)}")
    if any(a.get('aspect') is None or a.get('aspect') == '' for a in aspects):
        issues.append("aspect_name_none")
    if not p4_subaudit:
        issues.append("post4_not_subaudit")
    if any(len(p) > 280 for p in posts):
        issues.append(f"max_p_len={max(len(p) for p in posts)}")
    if not s.get('multiAspect'):
        issues.append("multiAspect_false")
    if not s.get('spiritual'):
        issues.append("spiritual_false")
    if not s.get('potential_audit'):
        issues.append("potential_false")
    if s.get('status') != 'DRAFT':
        issues.append(f"status_{s.get('status')}")
    if src_p.startswith('bluesky_bot/stories/drafts/'):
        issues.append("in_drafts_dir")

    print(f"[{i+1:02d}] {fn}: {', '.join(issues) if issues else 'CLEAN'}")
