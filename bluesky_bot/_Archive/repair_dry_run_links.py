import os
import sys
import json

# Resolve paths
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
bot_dir = os.path.join(root_dir, 'bluesky_bot')

# Add bot_dir to system path to import save_and_sync_story
sys.path.append(bot_dir)
from aletheia_bot import save_and_sync_story

print("Starting Link Correction on all generated dry-runs...")

# 1. Load the clean candidate harvest dataset
candidates_path = os.path.join(script_dir, 'harvested_candidates.json')
if not os.path.exists(candidates_path):
    print("ERROR: harvested_candidates.json not found in scratch/.")
    sys.exit(1)
    
with open(candidates_path, 'r', encoding='utf-8') as f:
    candidates = json.load(f)
print(f"Loaded {len(candidates)} clean candidates from harvest.")

# 2. Load all historical/batch story configs in stories/
bot_stories_dir = os.path.join(bot_dir, 'stories')
story_files = [f for f in os.listdir(bot_stories_dir) if f.startswith('factcheck_') and f.endswith('.json')]
print(f"Found {len(story_files)} story files on disk.")

corrected_count = 0
for sf in story_files:
    filepath = os.path.join(bot_stories_dir, sf)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        config = data[0] if isinstance(data, list) else data
        current_link = config.get("link", "").strip().lower()
        
        # Match candidate by checking links
        matched_candidate = None
        for c in candidates:
            c_url = c.get("url", "").strip().lower()
            c_target = c.get("target_url", "").strip().lower()
            
            # Match condition:
            # - If candidate is a reply: the config's link was set to the bsky target_url
            # - If candidate is a root: the config's link was set to the bsky/rss url
            if c_target and current_link == c_target:
                matched_candidate = c
                break
            elif not c_target and current_link == c_url:
                matched_candidate = c
                break
                
        if matched_candidate:
            target_mode = matched_candidate.get("mode", "root")
            target_article_url = matched_candidate.get("url", "")
            target_bsky_url = matched_candidate.get("target_url", "")
            
            print(f"\nMatched config '{config['subject']}' to candidate:")
            print(f"  -> Target Mode: {target_mode}")
            print(f"  -> Article Link: {target_article_url}")
            print(f"  -> Bsky Link: {target_bsky_url}")
            
            # Correct configuration fields
            config["link"] = target_article_url
            config["target_url"] = target_bsky_url
            config["mode"] = target_mode
            
            # Correct Post 1 text
            posts = config.get("posts", [])
            if len(posts) > 0:
                hook_post = posts[0]
                
                # Check for either Target Post: or Source: labels
                new_hook = hook_post
                
                # We replace the printed Bluesky post link with the actual news story article link
                if target_bsky_url and target_bsky_url in hook_post:
                    new_hook = hook_post.replace(target_bsky_url, target_article_url)
                    
                # Ensure the label matches the mode
                if target_mode == "root":
                    new_hook = new_hook.replace("Target Post:", "Source:")
                else:
                    new_hook = new_hook.replace("Source:", "Target Post:")
                    
                if new_hook != hook_post:
                    print(f"  -> Hook post link corrected!")
                    posts[0] = new_hook
                    config["posts"] = posts
            
            # Re-verify character limit compliance
            if len(posts[0]) > 300:
                print(f"  -> Warning: Post 1 exceeds 300 chars: {len(posts[0])}!")
                
            # Re-save and sync sequentially
            save_and_sync_story(config)
            corrected_count += 1
            
    except Exception as e:
        print(f"Error processing {sf}: {e}")

print(f"\nRegistry synchronization complete! Programmatically repaired and aligned {corrected_count} dry run configurations.")
