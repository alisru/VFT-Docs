import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
stories_dir = os.path.join(script_dir, "stories")

def list_drafts():
    files = [f for f in os.listdir(stories_dir) if f.startswith("factcheck_") and f.endswith(".json")]
    print(f"Total drafts: {len(files)}")
    for f in files:
        path = os.path.join(stories_dir, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            cfg = data[0] if isinstance(data, list) else data
            print(f"- {f}:")
            print(f"  Subject: {cfg.get('subject')}")
            print(f"  Link:    {cfg.get('link')}")
            print(f"  Actors:  {cfg.get('actors', [])}")
            print(f"  Macro:   {cfg.get('macro_event')}")
        except Exception as e:
            print(f"  Error loading {f}: {e}")

if __name__ == "__main__":
    list_drafts()
