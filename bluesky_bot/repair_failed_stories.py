import os
import json

def repair_stories():
    fail_dir = "E:/Vector Field Theory/VFT Docs/bluesky_bot/stories/fail"
    stories_dir = "E:/Vector Field Theory/VFT Docs/bluesky_bot/stories"
    
    if not os.path.exists(fail_dir):
        print("No fail directory found. Nothing to repair.")
        return

    for filename in os.listdir(fail_dir):
        if filename.endswith(".json"):
            fail_path = os.path.join(fail_dir, filename)
            try:
                with open(fail_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                story = data[0]
                posts = story.get("posts", [])
                modified = False
                
                for idx, post in enumerate(posts):
                    if len(post) > 300:
                        # Find a clean sentence boundary before 295 characters, or fallback to word boundary
                        truncated = post[:295]
                        last_period = truncated.rfind(".")
                        if last_period > 150: # sensible sentence length
                            trimmed = truncated[:last_period+1]
                        else:
                            # Try to find a space to split on
                            last_space = truncated.rfind(" ")
                            if last_space > 150:
                                trimmed = truncated[:last_space].strip() + "..."
                            else:
                                trimmed = truncated.strip() + "..."
                        
                        posts[idx] = trimmed
                        modified = True
                        print(f"  Trimmed post {idx+1} of {filename} from {len(post)} to {len(trimmed)} chars.")
                
                dest_path = os.path.join(stories_dir, filename)
                with open(dest_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                os.remove(fail_path)
                print(f"Successfully repaired and restored {filename}")
            except Exception as e:
                print(f"Error repairing {filename}: {e}")

if __name__ == "__main__":
    repair_stories()
