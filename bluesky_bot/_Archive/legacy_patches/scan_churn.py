import os
import glob
import json

live_dir = 'e:/Vector Field Theory/VFT Docs/bluesky_bot/stories/live'
files = glob.glob(os.path.join(live_dir, 'factcheck_*.json'))
files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

CHURN_DOMAINS = ['foxnews.com', 'nypost.com', 'breitbart.com', 'theblaze.com', 'thefederalist.com', 'dailycaller.com']
NON_CRIME_KEYWORDS = ['view', 'clashes', 'slams', 'rips', 'blasts', 'hosts', 'celebrity', 'trolls', 'backlash', 'interview', 'dinner', 'panel', 'outrage', 'grilled', 'claims', 'warns', 'calls for', 'defends']

pure_churn_traps = []

for p in files[:200]:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)[0]
        link = (d.get('link') or '').lower()
        subj = (d.get('subject') or '').lower()
        posts = d.get('posts', [])
        ru = d.get('real_u', 0)
        
        if any(cd in link for cd in CHURN_DOMAINS) and any(kw in subj for kw in NON_CRIME_KEYWORDS):
            if not any(cw in subj for cw in ['murder', 'killed', 'overdose', 'fatal', 'arson', 'rape', 'charged in', 'indicted']):
                pure_churn_traps.append({
                    'id': d.get('id'),
                    'subject': d.get('subject'),
                    'link': d.get('link'),
                    'ru': ru,
                    'rpsi': d.get('real_psi'),
                    'mode': d.get('mode', 'root'),
                    'sub_audits': posts[4] if len(posts) > 4 else ''
                })
    except Exception:
        pass

print(f"Identified {len(pure_churn_traps)} Pure Tabloid/Punditry Churn Traps out of 200:\n")
for c in pure_churn_traps:
    print(f"- ID: {c['id']}")
    print(f"  Title: {c['subject']}")
    print(f"  URL: {c['link']}")
    print(f"  Result: ({c['ru']}, {c['rpsi']}) | Mode: {c['mode']}")
    print(f"  Sub-Audits: {c['sub_audits'][:120]}...\n")
