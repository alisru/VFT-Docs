import os
import sys
import json
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from generate_graph import enforce_deterministic_trajectory
from rebuild_registries_son import get_zone_label

quarantine_dir = os.path.join(script_dir, "stories", "quarantine")
manifest_path = os.path.join(quarantine_dir, "all_rkeys_to_delete.json")
drafts_dir = os.path.join(script_dir, "stories", "drafts")
os.makedirs(drafts_dir, exist_ok=True)

if not os.path.exists(manifest_path):
    print(f"ERROR: Manifest not found at {manifest_path}")
    sys.exit(1)

with open(manifest_path, "r", encoding="utf-8") as f:
    stories = json.load(f)

print(f"Restoring coordinates and moving {len(stories)} stories from live to drafts...\n")

moved_count = 0
for story in stories:
    f_path = story.get("file")
    if not f_path or not os.path.exists(f_path):
        continue
    try:
        with open(f_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        s = data[0] if isinstance(data, list) else data
        
        # Reset Bluesky live state
        s["rkeys"] = []
        s["post_urls"] = []
        s["status"] = "DRAFT"

        # Preserve original coordinates and posts without aspect averaging
        s = enforce_deterministic_trajectory(s)
        data = [s] if isinstance(data, list) else s

        dest_path = os.path.join(drafts_dir, os.path.basename(f_path))
        with open(dest_path, "w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2)

        os.remove(f_path)
        moved_count += 1
        print(f"  [{moved_count}/{len(stories)}] Restored to draft: {os.path.basename(f_path)} -> ({s.get('claim_u')}, {s.get('real_u')})")
    except Exception as me:
        print(f"  Error returning {f_path} to draft: {me}")

print(f"\nSuccessfully returned {moved_count}/{len(stories)} stories to stories/drafts with restored coordinates.")
