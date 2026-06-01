import os
import sys
import json
import shutil

# Resolve relative paths
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
bot_dir = os.path.join(root_dir, 'bluesky_bot')

# Add bot_dir to system path to import save_and_sync_story
sys.path.append(bot_dir)
from aletheia_bot import save_and_sync_story

print("Starting Sequential Consolidation of the 20 Evaluated Stories...")

# 1. Gather all fact-check JSON files from scratch
scratch_files = [f for f in os.listdir(script_dir) if f.startswith('factcheck_') and f.endswith('.json')]
print(f"Found {len(scratch_files)} story configs in scratch/ to synchronize.")

success_count = 0
for sf in scratch_files:
    filepath = os.path.join(script_dir, sf)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # The subagent writes the config as an object or a 1-item array
        if isinstance(data, list):
            thread_config = data[0]
        else:
            thread_config = data
            
        # Ensure status is COMPLETED DRY RUN
        thread_config["status"] = "COMPLETED DRY RUN"
        
        # Save and synchronize using the official bot registry system
        save_and_sync_story(thread_config)
        
        # 2. Copy the corresponding graph image if it exists
        subject_slug = thread_config["subject"].lower().replace(" ", "_").replace("/", "_")
        graph_src_name = f"{subject_slug}_graph.png"
        
        # Sometimes there's minor naming differences, let's also guess the filename from story id
        story_id = thread_config.get("id") or subject_slug
        possible_names = [graph_src_name, f"{story_id}_graph.png", sf.replace('factcheck_', '').replace('.json', '_graph.png')]
        
        src_graph_path = None
        for name in possible_names:
            p = os.path.join(script_dir, name)
            if os.path.exists(p):
                src_graph_path = p
                break
                
        if src_graph_path:
            # Targets: bluesky_bot/ and _Generated_Content/
            dest_bot_graph = os.path.join(bot_dir, os.path.basename(src_graph_path))
            dest_gen_graph = os.path.join(root_dir, "_Generated_Content", os.path.basename(src_graph_path))
            
            shutil.copy(src_graph_path, dest_bot_graph)
            shutil.copy(src_graph_path, dest_gen_graph)
            print(f"  -> Graph copied to {dest_bot_graph} and {dest_gen_graph}")
        else:
            print(f"  -> Warning: No graph image found for {sf} (checked names: {possible_names})")
            
        success_count += 1
    except Exception as e:
        print(f"Error processing {sf}: {e}")

print(f"\nSequential sync complete! Successfully compiled and synced {success_count}/{len(scratch_files)} stories.")
