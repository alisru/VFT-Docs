import os
import shutil
import json
import sys

bot_dir = os.path.dirname(os.path.abspath(__file__))
stories_dir = os.path.join(bot_dir, "stories")
quarantine_dir = os.path.join(stories_dir, "quarantine")

RIGHT_WING_DOMAINS = [
    'foxnews.com', 'nypost.com', 'breitbart.com', 'washingtonexaminer.com',
    'dailywire.com', 'freebeacon.com', 'thefederalist.com', 'theblaze.com',
    'newsmax.com', 'oann.com', 'dailycaller.com', 'westernjournal.com'
]

def is_rw(url):
    u = (url or '').lower()
    return any(d in u for d in RIGHT_WING_DOMAINS)

def main():
    os.makedirs(quarantine_dir, exist_ok=True)
    staged_files = [f for f in os.listdir(stories_dir) if f.startswith("factcheck_") and f.endswith(".json")]

    quarantined = []
    for sf in staged_files:
        filepath = os.path.join(stories_dir, sf)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)[0]
            url = data.get("link") or data.get("url") or ""
            if is_rw(url):
                dest = os.path.join(quarantine_dir, sf)
                shutil.move(filepath, dest)
                quarantined.append((sf, data.get("subject", ""), url))
        except Exception as e:
            print(f"Error checking {sf}: {e}")

    print(f"Successfully quarantined {len(quarantined)} staged right-wing media stories to stories/quarantine/:\n")
    for idx, (sf, subj, url) in enumerate(quarantined, 1):
        print(f"{idx}. {sf} | {subj} | {url[:60]}...")

    # Rebuild registries to reflect the clean queue
    print("\nRebuilding registries...")
    import subprocess
    subprocess.run([sys.executable, os.path.join(bot_dir, "rebuild_registries_son.py")], check=True)
    print("Registries updated.")

if __name__ == "__main__":
    main()
