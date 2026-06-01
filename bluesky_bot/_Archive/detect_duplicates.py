import os
import json
import glob

def find_duplicates():
    stories_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\stories"
    pattern = os.path.join(stories_dir, "**", "factcheck_*.json")
    files = glob.glob(pattern, recursive=True)
    
    url_map = {}
    subject_map = {}
    
    for f_path in files:
        try:
            with open(f_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = data[0] if isinstance(data, list) else data
            
            link = cfg.get("link")
            subject = cfg.get("subject", "").lower().strip()
            
            if link:
                url_map.setdefault(link, []).append(f_path)
            if subject:
                subject_map.setdefault(subject, []).append(f_path)
        except Exception as e:
            print(f"Error reading {f_path}: {e}")
            
    print("--- DUPLICATE BY URL/LINK ---")
    duplicate_urls = {k: v for k, v in url_map.items() if len(v) > 1}
    for url, paths in duplicate_urls.items():
        print(f"URL: {url}")
        for p in paths:
            print(f"  - {os.path.basename(p)}")
            
    print("\n--- DUPLICATE BY SUBJECT ---")
    duplicate_subjects = {k: v for k, v in subject_map.items() if len(v) > 1}
    for sub, paths in duplicate_subjects.items():
        print(f"Subject: '{sub}'")
        for p in paths:
            print(f"  - {os.path.basename(p)}")

if __name__ == "__main__":
    find_duplicates()
