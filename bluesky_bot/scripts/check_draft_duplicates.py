import os
import json

def check_draft_duplicates():
    stories_dir = "e:/Vector Field Theory/VFT Docs/bluesky_bot/stories"
    
    seen_links = {}
    seen_subjects = {}
    seen_ids = {}
    
    files_checked = 0
    
    for filename in os.listdir(stories_dir):
        if not (filename.startswith("factcheck_") and filename.endswith(".json")):
            continue
            
        filepath = os.path.join(stories_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            cfg = data[0] if isinstance(data, list) else data
            story_id = cfg.get("id")
            subject = cfg.get("subject", "").strip().lower()
            link = cfg.get("link", "").strip().lower()
            
            files_checked += 1
            
            if story_id:
                seen_ids.setdefault(story_id, []).append(filename)
            if subject:
                seen_subjects.setdefault(subject, []).append(filename)
            if link:
                seen_links.setdefault(link, []).append(filename)
                
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    print(f"Checked {files_checked} draft files.")
    
    print("\n--- DUPLICATE LINKS ---")
    dup_links_found = False
    for link, files in seen_links.items():
        if len(files) > 1:
            dup_links_found = True
            print(f"Link: {link}")
            for f in files:
                print(f"  - {f}")
    if not dup_links_found:
        print("No duplicate links found.")
        
    print("\n--- DUPLICATE SUBJECTS ---")
    dup_subs_found = False
    for sub, files in seen_subjects.items():
        if len(files) > 1:
            dup_subs_found = True
            print(f"Subject: {sub}")
            for f in files:
                print(f"  - {f}")
    if not dup_subs_found:
        print("No duplicate subjects found.")

    print("\n--- DUPLICATE IDS ---")
    dup_ids_found = False
    for story_id, files in seen_ids.items():
        if len(files) > 1:
            dup_ids_found = True
            print(f"ID: {story_id}")
            for f in files:
                print(f"  - {f}")
    if not dup_ids_found:
        print("No duplicate IDs found.")

if __name__ == "__main__":
    check_draft_duplicates()
