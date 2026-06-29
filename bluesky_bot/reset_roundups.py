import os
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
stories_dir = os.path.join(script_dir, "stories")

def reset():
    print("Resetting roundups...")
    for fn in os.listdir(stories_dir):
        path = os.path.join(stories_dir, fn)
        if os.path.isdir(path) and fn.startswith("roundup_"):
            print(f"Restoring files from companion directory: {fn}")
            for sub_fn in os.listdir(path):
                if sub_fn.startswith("factcheck_") and sub_fn.endswith(".json"):
                    shutil.move(os.path.join(path, sub_fn), os.path.join(stories_dir, sub_fn))
                    print(f"  Restored {sub_fn} to stories/")
            shutil.rmtree(path)
            print(f"  Deleted companion directory {fn}")
        elif os.path.isfile(path) and fn.startswith("roundup_") and fn.endswith(".json"):
            os.remove(path)
            print(f"  Deleted roundup config file {fn}")
            
    # Restore duplicate_discard
    discard_dir = os.path.join(stories_dir, "duplicate_discard")
    if os.path.isdir(discard_dir):
        print("Restoring files from duplicate_discard...")
        for sub_fn in os.listdir(discard_dir):
            if sub_fn.startswith("factcheck_") and sub_fn.endswith(".json"):
                shutil.move(os.path.join(discard_dir, sub_fn), os.path.join(stories_dir, sub_fn))
                print(f"  Restored {sub_fn} to stories/")
        shutil.rmtree(discard_dir)
        print("  Deleted duplicate_discard folder.")
        
    print("Reset complete!")

if __name__ == "__main__":
    reset()
