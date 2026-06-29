import os
import json

def normalize_url(url):
    if not url:
        return ""
    url = url.strip()
    if "?" in url:
        url = url.split("?")[0]
    if "#" in url:
        url = url.split("#")[0]
    return url.lower().strip()

def get_file_metadata(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cfg = data[0] if isinstance(data, list) else data
        posts = cfg.get("posts", [])
        post_count = len(posts)
        char_violations = sum(1 for p in posts if len(p) > 299)
        subject = cfg.get("subject", "")
        link = cfg.get("link", "")
        mode = cfg.get("mode", "")
        mtime = os.path.getmtime(filepath)
        return {
            "path": filepath,
            "filename": os.path.basename(filepath),
            "post_count": post_count,
            "char_violations": char_violations,
            "subject": subject,
            "link": link,
            "mode": mode,
            "mtime": mtime,
            "error": None
        }
    except Exception as e:
        return {
            "path": filepath,
            "filename": os.path.basename(filepath),
            "post_count": 0,
            "char_violations": 0,
            "subject": "",
            "link": "",
            "mode": "",
            "mtime": 0,
            "error": str(e)
        }

def resolve_duplicates():
    stories_dir = "e:/Vector Field Theory/VFT Docs/bluesky_bot/stories"
    
    # First, harvest all file metadatas
    files = []
    for filename in os.listdir(stories_dir):
        if filename.startswith("factcheck_") and filename.endswith(".json"):
            filepath = os.path.join(stories_dir, filename)
            files.append(get_file_metadata(filepath))
            
    # Group by normalized link
    groups = {}
    for f in files:
        if f["error"]:
            continue
        norm_url = normalize_url(f["link"])
        if norm_url:
            groups.setdefault(norm_url, []).append(f)
            
    # Print comparison and remove the least valid
    for url, grp in groups.items():
        if len(grp) < 2:
            continue
            
        print(f"\nDuplicate group for URL: {url}")
        # Sort group by validity:
        # 1. Post count should be exactly 13 (a perfect thread)
        # 2. Fewer character violations
        # 3. Mode should be 'root' (as requested recently)
        # 4. More detailed subject/descriptive filename (longer length)
        # 5. Newer modified time
        
        def score_file(item):
            # Perfect post count is 13
            post_count_score = 10 if item["post_count"] == 13 else item["post_count"]
            # Fewer char violations is better
            char_violation_penalty = -5 * item["char_violations"]
            # Mode 'root' is preferred
            mode_score = 2 if item["mode"] == "root" else 0
            # Descriptiveness / clean naming
            desc_score = len(item["filename"]) / 100.0
            
            return (post_count_score, char_violation_penalty, mode_score, desc_score, item["mtime"])
            
        sorted_grp = sorted(grp, key=score_file, reverse=True)
        keep = sorted_grp[0]
        to_delete = sorted_grp[1:]
        
        print(f"  KEEPING: {keep['filename']}")
        print(f"    - Subject: {keep['subject']}")
        print(f"    - Posts: {keep['post_count']}, Char Violations: {keep['char_violations']}, Mode: {keep['mode']}")
        
        for item in to_delete:
            print(f"  DELETING: {item['filename']}")
            print(f"    - Subject: {item['subject']}")
            print(f"    - Posts: {item['post_count']}, Char Violations: {item['char_violations']}, Mode: {item['mode']}")
            try:
                os.remove(item["path"])
                print("      Successfully deleted.")
            except Exception as e:
                print(f"      Error deleting: {e}")

if __name__ == "__main__":
    resolve_duplicates()
