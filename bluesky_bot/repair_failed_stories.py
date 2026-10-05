import os
import sys
import json
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from validate_batch import repair_spirithekanon_post

def repair_stories():
    stories_dir = os.path.join(script_dir, "stories")
    fail_dir = os.path.join(stories_dir, "fail")
    
    if not os.path.exists(fail_dir):
        print("No fail directory found. Nothing to repair.")
        return

    for filename in sorted(os.listdir(fail_dir)):
        if filename.endswith(".json"):
            fail_path = os.path.join(fail_dir, filename)
            try:
                with open(fail_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                story = data[0] if isinstance(data, list) else data
                posts = story.get("posts", [])
                modified = False
                
                # 1. Repair Spirithekanon post
                for idx, post in enumerate(posts):
                    if isinstance(post, str) and post.strip().startswith("Spirithekanon:"):
                        repaired = repair_spirithekanon_post(post)
                        if repaired != post:
                            posts[idx] = repaired
                            modified = True
                            print(f"  Repaired Spirithekanon post in {filename}")

                # 2. Trim posts exceeding character limit
                for idx, post in enumerate(posts):
                    if len(post) > 300:
                        truncated = post[:295]
                        last_period = truncated.rfind(".")
                        if last_period > 150:
                            trimmed = truncated[:last_period+1]
                        else:
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
                    json.dump([story] if isinstance(data, list) else story, f, indent=2, ensure_ascii=False)
                
                # Safely remove old copy from fail_dir since it has been restored to stories/
                if os.path.exists(fail_path) and os.path.abspath(fail_path) != os.path.abspath(dest_path):
                    os.remove(fail_path)
                print(f"Successfully repaired and restored {filename} to stories/")
            except Exception as e:
                print(f"Error repairing {filename}: {e}")

if __name__ == "__main__":
    repair_stories()
