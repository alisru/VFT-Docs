import os
import sys
import json

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

script_dir = os.path.dirname(os.path.abspath(__file__))
live_dir = os.path.join(script_dir, 'stories', 'live')
index_path = os.path.join(live_dir, 'index.json')

with open(index_path, 'r', encoding='utf-8') as f:
    files = json.load(f)

last_100 = files[-100:]

violations = []
extreme_neg = []
tabloid_echo = []
sound_audits = []

for idx, fn in enumerate(last_100, 1):
    fp = os.path.join(live_dir, fn)
    if not os.path.exists(fp):
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        d = json.load(f)
    s = d[0] if isinstance(d, list) else d

    cu = float(s.get('claim_u', 0.0))
    cp = float(s.get('claim_psi', 0.0))
    ru = float(s.get('real_u', 0.0))
    rp = float(s.get('real_psi', 0.0))
    posts = s.get('posts', [])
    p3 = posts[3] if len(posts) > 3 else ''
    v_line = p3.split('\n')[0]
    sub = s.get('subject', '')
    url = s.get('link') or s.get('url') or s.get('source_url') or ''

    # Invariant check: (+,+) -> (-,-) must be Fall into Destruction
    is_viol = False
    if cu >= 0 and cp >= 0 and ru <= 0 and rp <= 0:
        if 'Deception' in v_line or 'Redemption' in v_line or 'Awakening' in v_line:
            is_viol = True
    elif cu >= 0 and cp >= 0 and ru <= 0 and rp >= 0:
        if 'Destruction' in v_line or 'Redemption' in v_line:
            is_viol = True

    if is_viol:
        violations.append((fn, sub, f"({cu},{cp})->({ru},{rp})", v_line))

    if ru <= -0.7 or rp <= -0.7:
        extreme_neg.append((fn, sub, f"({cu},{cp})->({ru},{rp})", url))

    any_tabloid = any(t in url for t in ['foxnews', 'nypost', 'dailymail', 'breitbart', 'dailycaller', 'thefederalist', 'washingtonexaminer'])
    if any_tabloid:
        tabloid_echo.append((fn, sub, url))
    else:
        sound_audits.append((fn, sub, url))

print(f"Total Analyzed: {len(last_100)}")
print(f"Deterministic Trajectory Invariant Violations: {len(violations)}")
print(f"Extreme Negative Judgements (<= -0.7): {len(extreme_neg)}")
print(f"Tabloid / Partisan Source Stories: {len(tabloid_echo)}")
print(f"Independent / Broadcaster / Sound Sources: {len(sound_audits)}")

print("\n--- SAMPLE OF TRAJECTORY VIOLATIONS ---")
for fn, sub, coords, v in violations[:8]:
    print(f"  * {fn}: {coords} | {v}")

print("\n--- SAMPLE OF EXTREME NEGATIVE OUTLIERS ---")
for fn, sub, coords, u in extreme_neg[:8]:
    print(f"  * {fn}: {coords} | {sub[:50]}... | {u[:50]}...")
