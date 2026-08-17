import os
import json

log_path = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\harvested_stories_log.jsonl"
stories_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\stories"

# 1. Build map of story_id -> original_posts from harvested_stories_log.jsonl
original_posts_map = {}
if os.path.exists(log_path):
    print("Loading original posts from log...")
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                story_id = item.get("id")
                posts = item.get("posts")
                if story_id and posts:
                    # Keep the latest evaluation posts for this id
                    original_posts_map[story_id] = posts
            except Exception as e:
                pass
    print(f"Loaded {len(original_posts_map)} historical story definitions.")

def trim_post_clean(post, limit=300):
    if len(post) <= limit:
        return post
    
    # Try removing the hashtags line at the end
    lines = post.split('\n')
    if lines:
        last_line = lines[-1].strip()
        # If the last line is purely hashtags, remove it
        if last_line.startswith('#') or (last_line and all(word.startswith('#') for word in last_line.split())):
            post_no_tags = '\n'.join(lines[:-1]).strip()
            if len(post_no_tags) <= limit:
                print(f"    Optimized by removing hashtags line (len {len(post)} -> {len(post_no_tags)}): {last_line}")
                return post_no_tags
            post = post_no_tags
            
    # Crop exactly at limit without adding '...'
    cropped = post[:limit].strip()
    print(f"    Cropped post to {limit} chars without adding '...'")
    return cropped

# 2. Scan stories/ directory for JSON files and restore/clean-trim them
corrected_count = 0
for filename in os.listdir(stories_dir):
    if not filename.endswith(".json") or not filename.startswith("factcheck_"):
        continue
        
    filepath = os.path.join(stories_dir, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        cfg = data[0] if isinstance(data, list) else data
        
        story_id = cfg.get("id")
        if not story_id:
            continue
            
        # Try to restore original posts from the map
        orig_posts = original_posts_map.get(story_id)
        if orig_posts:
            cfg["posts"] = list(orig_posts)
            print(f"Restored original posts for {filename}")
        else:
            print(f"Warning: No log entry found for {story_id}, cleaning existing posts.")
            
        # Apply clean trimming
        posts = cfg["posts"]
        limit = 300 if cfg.get("compact") or cfg.get("multiAspect") else 299
        posts_to_check = posts[:4] if cfg.get("compact") else posts
        
        for i, post in enumerate(posts):
            if i < len(posts_to_check) and len(post) > limit:
                print(f"  Trimming post {i+1} of {filename} (current len: {len(post)})...")
                posts[i] = trim_post_clean(post, limit)
                
        cfg["posts"] = posts
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        corrected_count += 1
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print(f"\nSuccessfully restored and clean-trimmed {corrected_count} stories.")
