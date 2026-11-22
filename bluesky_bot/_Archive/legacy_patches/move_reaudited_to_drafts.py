import os
import sys
import json
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

import reaudit_live_batch

live_dir = os.path.join(script_dir, "stories", "live")
drafts_dir = os.path.join(script_dir, "stories")
drafts_index_path = os.path.join(drafts_dir, "index.json")
live_index_path = os.path.join(live_dir, "index.json")

with open(drafts_index_path, "r", encoding="utf-8") as f:
    drafts_index = json.load(f)

with open(live_index_path, "r", encoding="utf-8") as f:
    live_index = json.load(f)

moved_count = 0
specs = reaudit_live_batch.REAUDIT_SPECS

for fn in specs.keys():
    src_fp = os.path.join(live_dir, fn)
    dst_fp = os.path.join(drafts_dir, fn)

    if not os.path.exists(src_fp):
        print(f"[SKIP] Not in live: {fn}")
        continue

    with open(src_fp, "r", encoding="utf-8") as f:
        data = json.load(f)

    story = data[0] if isinstance(data, list) else data
    story["status"] = "DRAFT (CORRECTION)"
    # Clear out live post flags so it behaves as an unposted draft
    story["is_correction"] = True
    
    # Save into drafts directory
    out_data = [story] if isinstance(data, list) else story
    with open(dst_fp, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)

    # Remove from live directory
    try:
        os.remove(src_fp)
    except Exception as e:
        print(f"[WARN] Could not remove {src_fp}: {e}")

    # Add to drafts index if not already present
    if fn not in drafts_index:
        drafts_index.append(fn)

    # Remove from live index
    if fn in live_index:
        live_index.remove(fn)

    moved_count += 1
    print(f"[MOVED] {fn} -> stories/ (Draft)")

# Save updated index files
with open(drafts_index_path, "w", encoding="utf-8") as f:
    json.dump(drafts_index, f, indent=2, ensure_ascii=False)

with open(live_index_path, "w", encoding="utf-8") as f:
    json.dump(live_index, f, indent=2, ensure_ascii=False)

print("\n========================================================")
print(f"Successfully moved {moved_count} stories to drafts ({drafts_dir})")
print(f"Drafts index total: {len(drafts_index)}")
print(f"Live index total: {len(live_index)}")
print("========================================================")
