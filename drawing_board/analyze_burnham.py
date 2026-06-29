import os
import json

stories_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\stories"
files = [f for f in os.listdir(stories_dir) if f.endswith(".json") and f.startswith("factcheck_")]

target_files = [f for f in files if "burnham" in f.lower() or "brexit" in f.lower()]

for fn in sorted(target_files):
    path = os.path.join(stories_dir, fn)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cfg = data[0] if isinstance(data, list) else data
    print(f"File: {fn}")
    print(f"  Subject:     {cfg.get('subject')}")
    print(f"  Macro Event: {cfg.get('macro_event')}")
    print(f"  Actors:      {cfg.get('actors')}")
    print(f"  Link:        {cfg.get('link')}")
    print(f"  Topic:       {cfg.get('topic')}")
    print(f"  Category:    {cfg.get('category')}")
    print("-" * 50)
