"""
backfill_harvested_history.py

Scans all factcheck_*.json files in stories/live/, extracts their "link" URLs,
and appends any that are missing from harvested_history.json.
"""
import os
import json
import glob

script_dir   = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(script_dir, "harvested_history.json")
LIVE_DIR     = os.path.join(script_dir, "stories", "live")

# --- 1. Load existing history ---
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        existing = json.load(f)
else:
    existing = []

existing_set = {u.strip().lower() for u in existing if u.strip()}
print(f"harvested_history.json has {len(existing)} URLs.")

# --- 2. Scan all live factcheck JSONs ---
pattern = os.path.join(LIVE_DIR, "factcheck_*.json")
files   = glob.glob(pattern)
print(f"Found {len(files)} factcheck files in stories/live/.")

added   = []
skipped = 0
errors  = 0

for filepath in files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        story = data[0] if isinstance(data, list) else data
        url   = (story.get("link") or story.get("url") or "").strip()
        if not url:
            skipped += 1
            continue
        if url.lower() in existing_set:
            skipped += 1
            continue
        added.append(url)
        existing_set.add(url.lower())
    except Exception as e:
        print(f"  Warning: {os.path.basename(filepath)}: {e}")
        errors += 1

# --- 3. Write back ---
if added:
    updated = existing + added
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
    print(f"\nAdded {len(added)} missing URLs to harvested_history.json.")
    print(f"Total URLs now: {len(updated)}")
else:
    print("\nNothing to add — all story URLs are already in harvested_history.json.")

print(f"Skipped (already present or no URL): {skipped} | Errors: {errors}")
