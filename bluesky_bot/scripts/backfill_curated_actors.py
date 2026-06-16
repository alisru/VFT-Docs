import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
import json
import os

# Include parent directory to import actor_extract
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from actor_extract import extract_actors

stories_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paths = (
    glob.glob(os.path.join(stories_dir, "stories", "factcheck_*.json"))
    + glob.glob(os.path.join(stories_dir, "stories", "live", "factcheck_*.json"))
    + glob.glob(os.path.join(stories_dir, "stories", "darkroom", "factcheck_*.json"))
)

print(f"Found {len(paths)} stories to backfill.")

updated_count = 0
for p in paths:
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Determine if it's a list or dict
        is_list = isinstance(data, list)
        cfg = data[0] if is_list else data
        
        subject = cfg.get("subject", "")
        old_actors = cfg.get("actors", [])
        
        new_actors = extract_actors(subject)
        
        # Update config
        cfg["actors"] = new_actors
        
        # Save back to file
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        if old_actors != new_actors:
            print(f"  {os.path.basename(p)}: {old_actors} -> {new_actors}")
            updated_count += 1
            
    except Exception as e:
        print(f"Error processing {p}: {e}")

print(f"Backfill complete. Updated {updated_count} files.")
