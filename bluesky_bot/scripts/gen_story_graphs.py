"""
Generate graphs from real draft story JSONs in bluesky_bot/stories/
Outputs PNGs into bluesky_bot/scratch/test_runs/stories/
"""
import os
import json
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from generate_graph import draw_graph

STORIES_DIR = os.path.join(os.path.dirname(__file__), '..', 'stories')
OUT_DIR = r"E:\Vector Field Theory\VFT Docs\_AI files and chat logs\test_runs"
os.makedirs(OUT_DIR, exist_ok=True)

skipped = []
generated = []

for fname in sorted(f for f in os.listdir(STORIES_DIR) if f.startswith('factcheck_') and f.endswith('.json')):
    fpath = os.path.join(STORIES_DIR, fname)
    try:
        with open(fpath, encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        skipped.append((fname, f'parse error: {e}'))
        continue

    story = data[0] if isinstance(data, list) else data
    if not isinstance(story, dict):
        skipped.append((fname, 'not a dict'))
        continue

    claim_u   = story.get('claim_u')
    claim_psi = story.get('claim_psi')
    real_u    = story.get('real_u')
    real_psi  = story.get('real_psi')

    if any(v is None for v in [claim_u, claim_psi, real_u, real_psi]):
        skipped.append((fname, 'missing micro coords'))
        continue

    title = story.get('subject', fname)

    macro_event    = story.get('macro_event', '')
    macro_claim_u  = story.get('macro_claim_u')
    macro_claim_psi= story.get('macro_claim_psi')
    macro_real_u   = story.get('macro_real_u')
    macro_real_psi = story.get('macro_real_psi')

    # Only pass macro args if all four coords exist and there is a macro_event label
    has_macro = (
        macro_event and
        macro_claim_u is not None and
        macro_claim_psi is not None and
        macro_real_u is not None and
        macro_real_psi is not None
    )

    out_name = fname.replace('.json', '.png')
    out_path = os.path.join(OUT_DIR, out_name)

    try:
        if has_macro:
            draw_graph(
                claim_u=claim_u, claim_psi=claim_psi,
                real_u=real_u, real_psi=real_psi,
                title=title, filename=out_path,
                macro_event=macro_event,
                macro_claim_u=macro_claim_u, macro_claim_psi=macro_claim_psi,
                macro_real_u=macro_real_u, macro_real_psi=macro_real_psi
            )
        else:
            draw_graph(
                claim_u=claim_u, claim_psi=claim_psi,
                real_u=real_u, real_psi=real_psi,
                title=title, filename=out_path
            )
        generated.append(fname)
        print(f'OK  {out_name}{"  [macro]" if has_macro else ""}')
    except Exception as e:
        skipped.append((fname, f'draw error: {e}'))
        print(f'ERR {fname}: {e}')

print(f'\nDone. Generated: {len(generated)}  Skipped: {len(skipped)}')
if skipped:
    for s in skipped:
        print(f'  SKIP {s[0]}: {s[1]}')
