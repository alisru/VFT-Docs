import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
import json
import re
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from actor_extract import extract_actors

stories = glob.glob('stories/factcheck_*.json') + glob.glob('stories/live/factcheck_*.json')

results = []
for p in stories:
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
        cfg = d[0] if isinstance(d, list) else d
        subject = cfg.get("subject", "")
        actors = extract_actors(subject)
        results.append((subject, actors))

# Print first 100 results to see what's being extracted
for i, (sub, act) in enumerate(results[:300]):
    print(f"SUBJ: {repr(sub)}")
    print(f"ACTS: {repr(act)}")
    print("-" * 40)
