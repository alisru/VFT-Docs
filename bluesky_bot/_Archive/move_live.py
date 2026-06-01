import os
import sys
import json
import shutil

def move_all_live_to_subfolder():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    dirs = [
        os.path.join(parent_dir, "bluesky_bot", "stories"),
        os.path.join(parent_dir, "_Generated_Content", "stories")
    ]
    
    moved_count = 0
    
    for s_dir in dirs:
        if not os.path.exists(s_dir):
            continue
            
        live_dir = os.path.join(s_dir, "live")
        os.makedirs(live_dir, exist_ok=True)
        
        # Scan root files in this stories folder
        for filename in os.listdir(s_dir):
            filepath = os.path.join(s_dir, filename)
            if not os.path.isfile(filepath) or not filename.endswith(".json") or filename == "index.json":
                continue
                
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cfg = data[0] if isinstance(data, list) else data
                
                status = cfg.get("status", "")
                is_live = status and (status.startswith("LIVE") or "LIVE POSTED" in status)
                
                if is_live:
                    dest_path = os.path.join(live_dir, filename)
                    shutil.move(filepath, dest_path)
                    print(f"Moved live file from {filepath} to {dest_path}")
                    moved_count += 1
            except Exception as e:
                print(f"Error checking/moving {filepath}: {e}")
                
    print(f"Successfully moved {moved_count} historically live files into their respective stories/live/ subfolders!")

if __name__ == '__main__':
    move_all_live_to_subfolder()
