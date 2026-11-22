import os
import glob
import json
import re

live_dir = 'e:/Vector Field Theory/VFT Docs/bluesky_bot/stories/live'
files = glob.glob(os.path.join(live_dir, 'factcheck_*.json'))
files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
past_200 = files[:200]

print(f"Scanning past {len(past_200)} stories on disk...\n")

TABLOID_DOMAINS = [
    'foxnews.com', 'nypost.com', 'dailymail.co.uk', 'breitbart.com',
    'theblaze.com', 'thefederalist.com', 'dailycaller.com', 'westernjournal.com'
]
OUTRAGE_CUES = [
    r'\brip\b', r'\brips\b', r'\bslam\b', r'\bslams\b', r'\bblast\b', r'\bblasts\b',
    r'\bfaces backlash\b', r'\bunder fire\b', r'\bfume\b', r'\bfuming\b',
    r'\bsparks outrage\b', r'\bcriticism\b', r'\bsparks fury\b', r'\bhypocrisy\b'
]

smear_suspects = []
flat_ones = []

for p in past_200:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cfg = data[0] if isinstance(data, list) else data
        sid = cfg.get('id', os.path.basename(p))
        subj = cfg.get('subject', '')
        link = cfg.get('link', '') or ''
        ru = cfg.get('real_u', 0.0)
        rpsi = cfg.get('real_psi', 0.0)
        cu = cfg.get('claim_u', 0.0)
        cpsi = cfg.get('claim_psi', 0.0)
        posts = cfg.get('posts', [])
        mode = cfg.get('mode', 'root')

        # Check flat 1's
        if (abs(ru) == 1.0 and abs(rpsi) == 1.0) or (abs(cu) == 1.0 and abs(cpsi) == 1.0):
            flat_ones.append((sid, subj, (cu, cpsi), (ru, rpsi)))

        # Check tabloid smear trap
        is_tabloid = any(d in link.lower() for d in TABLOID_DOMAINS)
        has_cue = any(re.search(cue, subj, re.IGNORECASE) for cue in OUTRAGE_CUES)

        if (is_tabloid or has_cue) and ru < -0.3:
            p2 = posts[2] if len(posts) > 2 else ''
            p3 = posts[3] if len(posts) > 3 else ''
            p4 = posts[4] if len(posts) > 4 else ''
            p8 = posts[8] if len(posts) > 8 else ''
            
            # Check if an individual was framed as the failing actor rather than the media outlet
            all_text = (p2 + " " + p3 + " " + p4 + " " + p8).lower()
            outlet_blamed = any(w in all_text for w in ['outlet', 'smear', 'media profit', 'rage clicks', 'tabloid', 'clickbait', 'launders', 'fox news'])
            
            smear_suspects.append({
                'id': sid,
                'subj': subj,
                'link': link,
                'mode': mode,
                'cu': cu,
                'cpsi': cpsi,
                'ru': ru,
                'rpsi': rpsi,
                'outlet_blamed': outlet_blamed,
                'p2': p2[:130],
                'p4': p4[:130]
            })
    except Exception as e:
        pass

print("=== AUDIT REPORT: PAST 200 LIVE STORIES ===")
print(f"Total Stories Scanned: {len(past_200)}")
print(f"Flat 1.0 Coordinates Count: {len(flat_ones)}")
print(f"Tabloid / Outrage Cues with FAIL Verdict: {len(smear_suspects)}\n")

unprotected_smears = [s for s in smear_suspects if not s['outlet_blamed']]
protected_smears = [s for s in smear_suspects if s['outlet_blamed']]

print(f"-> Protected Smears (Outlet Audited): {len(protected_smears)}")
print(f"-> Unprotected Smears (Victim/Target Blamed or Conflated): {len(unprotected_smears)}\n")

if unprotected_smears:
    print("--- UNPROTECTED TABLOID TRAPS (Target Penalized on Churn) ---")
    for s in unprotected_smears:
        print(f"ID: {s['id']}")
        print(f"  Title: {s['subj']}")
        print(f"  URL: {s['link']}")
        print(f"  Mode: {s['mode']} | Coordinates: Stated ({s['cu']}, {s['cpsi']}) -> Real ({s['ru']}, {s['rpsi']})")
        print(f"  Reality: {s['p2']}...")
        print(f"  Sub-Audits: {s['p4']}...\n")
