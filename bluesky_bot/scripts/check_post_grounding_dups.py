import glob
import json
import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
bot_dir = os.path.dirname(script_dir)
stories_dir = os.path.join(bot_dir, "stories")

files = sorted(glob.glob(os.path.join(stories_dir, "factcheck_*.json")))
print(f"Scanning {len(files)} draft files for duplicated URLs, grounding stories, or verification mentions in posts...\n")

issues = []
raw_url_pattern = re.compile(r'https?://[^\s)\]]+')

for f in files:
    fname = os.path.basename(f)
    try:
        with open(f, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        cfg = data[0] if isinstance(data, list) and len(data) > 0 else data
        posts = cfg.get("posts", [])
        g_url = (cfg.get("grounding_url") or "").strip()
        link = (cfg.get("link") or "").strip()
        
        # 1. Check duplicate URLs in posts
        url_locations = {}
        for idx, p in enumerate(posts):
            found_urls = raw_url_pattern.findall(p)
            for u in found_urls:
                clean_u = u.rstrip(".,;:\"'")
                url_locations.setdefault(clean_u, []).append(idx + 1)
                
        dup_urls = {u: locs for u, locs in url_locations.items() if len(locs) > 1}
        
        # 2. Check if grounding_url appears in multiple posts
        g_in_posts = []
        if g_url:
            for idx, p in enumerate(posts):
                if g_url in p:
                    g_in_posts.append(idx + 1)
                    
        # 3. Check if primary link appears in multiple posts
        l_in_posts = []
        if link:
            for idx, p in enumerate(posts):
                if link in p:
                    l_in_posts.append(idx + 1)
                    
        # 4. Check repeated "Source: ..." or "Evidence: ..." lines across posts
        source_lines = []
        for idx, p in enumerate(posts):
            for line in p.split("\n"):
                if line.strip().startswith("Source:") or line.strip().startswith("Evidence:"):
                    source_lines.append((idx + 1, line.strip()))
                    
        file_problems = []
        if dup_urls:
            file_problems.append(f"Duplicate raw URLs across posts: {dup_urls}")
        if len(g_in_posts) > 1:
            file_problems.append(f"Grounding URL repeated in posts {g_in_posts}")
        if len(l_in_posts) > 1:
            file_problems.append(f"Primary link repeated in posts {l_in_posts}")
        if len(source_lines) > 2:
            file_problems.append(f"Source/Evidence lines repeated ({len(source_lines)} times): {source_lines}")
            
        # 5. Check if the grounding story text or dossier was pasted into multiple posts
        dossier = (cfg.get("cross_source_dossier") or "").strip()
        if dossier and len(dossier) > 100:
            # check if chunks of dossier appear in multiple posts
            dossier_snippets = [line.strip() for line in dossier.split("\n") if len(line.strip()) > 50]
            repeated_snippets = []
            for s in dossier_snippets:
                matching_posts = [idx + 1 for idx, p in enumerate(posts) if s in p]
                if len(matching_posts) > 1:
                    repeated_snippets.append((s[:40], matching_posts))
            if repeated_snippets:
                file_problems.append(f"Dossier snippets repeated in multiple posts: {repeated_snippets}")
                
        if file_problems:
            issues.append((fname, file_problems))
            
    except Exception as e:
        print(f"Error reading {fname}: {e}")

print(f"Total draft stories with duplicate grounding/URLs in posts: {len(issues)}")

print("\n--- SAMPLE DRAFT POSTS AUDIT (first 5 stories) ---")
for f in files[:5]:
    fname = os.path.basename(f)
    with open(f, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    cfg = data[0] if isinstance(data, list) and len(data) > 0 else data
    posts = cfg.get("posts", [])
    print(f"\nStory: {fname} (total posts: {len(posts)})")
    print(f"  Root link: {cfg.get('link')}")
    print(f"  Grounding URL: {cfg.get('grounding_url')}")
    for idx, p in enumerate(posts):
        urls = raw_url_pattern.findall(p)
        source_mentions = [line.strip() for line in p.split("\n") if "source" in line.lower() or "evidence" in line.lower() or "http" in line.lower()]
        if urls or source_mentions:
            print(f"    Post {idx+1}: URLs={urls} | Mentions={source_mentions}")
