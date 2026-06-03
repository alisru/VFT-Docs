import json
import glob
import os
import sys

def rebuild_registries():
    # Make sure we import save_and_sync_story correctly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(script_dir) # Since we are in bluesky_bot/ now
    
    from aletheia_bot import save_and_sync_story
    from generate_graph import draw_graph
    
    # We want to completely clear the existing registry files and rebuild them from all JSON files in bluesky_bot/stories/
    bot_stories_dir = os.path.join(script_dir, "stories")
    gen_stories_dir = os.path.join(parent_dir, "_Generated_Content", "stories")
    
    # Let's delete the old registry files so save_and_sync_story starts fresh!
    bot_registry_path = os.path.join(script_dir, "stories_registry.js")
    gen_registry_path = os.path.join(parent_dir, "_Generated_Content", "stories_registry.js")
    
    # Delete index.json and live/index.json files so save_and_sync_story regenerates them cleanly
    for s_dir in [bot_stories_dir, gen_stories_dir]:
        for idx_file in ["index.json", os.path.join("live", "index.json")]:
            ip = os.path.join(s_dir, idx_file)
            if os.path.exists(ip):
                try:
                    os.remove(ip)
                    print(f"Removed old index file {ip}")
                except Exception as e:
                    print(f"Warning: Could not remove index file {ip} ({e}). Attempting to clear it...")
                    try:
                        with open(ip, "w", encoding="utf-8") as f:
                            json.dump([], f, indent=2)
                        print(f"Cleared index file {ip}")
                    except Exception as e2:
                        print(f"Error: Failed to clear index file {ip} ({e2}). Skipping.")
                
    for r_path in [bot_registry_path, gen_registry_path]:
        if os.path.exists(r_path):
            try:
                os.remove(r_path)
                print(f"Removed old registry {r_path}")
            except Exception as e:
                print(f"Warning: Could not remove registry file {r_path} ({e}). Attempting to clear it...")
                try:
                    with open(r_path, "w", encoding="utf-8") as f:
                        f.write("window.ALETHEIA_STORIES_REGISTRY = [];\n")
                    print(f"Cleared registry file {r_path}")
                except Exception as e2:
                    print(f"Error: Failed to clear registry file {r_path} ({e2}). Skipping.")
            
    # Load all factcheck JSON files recursively
    search_pattern = os.path.join(script_dir, "stories", "**", "factcheck_*.json")
    json_files = glob.glob(search_pattern, recursive=True)
    # Sort files chronologically by modification time (oldest first)
    json_files.sort(key=os.path.getmtime)
    print(f"Found {len(json_files)} story configurations to register.")
    
    for fp in json_files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = data[0] if isinstance(data, list) else data
            
            # Generate graph if it doesn't exist
            slug = cfg.get("id")
            if slug:
                import shutil
                graph_filename = f"{slug}_graph.png"
                bot_graph_path = os.path.join(script_dir, "graph_png", graph_filename)
                gen_graph_path = os.path.join(parent_dir, "_Generated_Content", "graph_png", graph_filename)
                
                if not os.path.exists(bot_graph_path) or not os.path.exists(gen_graph_path):
                    try:
                        print(f"Generating graph for {slug}...")
                        draw_graph(
                            cfg.get("claim_u", 0.0), cfg.get("claim_psi", 0.0),
                            cfg.get("real_u", 0.0), cfg.get("real_psi", 0.0),
                            cfg.get("subject", "Story"),
                            bot_graph_path
                        )
                        os.makedirs(os.path.dirname(gen_graph_path), exist_ok=True)
                        shutil.copy2(bot_graph_path, gen_graph_path)
                    except Exception as ge:
                        print(f"Error generating graph for {slug}: {ge}")

            # Sync!
            save_and_sync_story(cfg)
        except Exception as e:
            print(f"Error syncing {fp}: {e}")
            
    print("Rebuilding complete!")

if __name__ == '__main__':
    rebuild_registries()
