import os
import json
import glob
import re

def normalize_url(u):
    if not u:
        return ""
    u = u.split("?")[0].split("#")[0].rstrip("/").lower().strip()
    return u

def normalize_text(t):
    if not t:
        return ""
    return re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()

def check_draft_duplicates():
    base_dir = "e:/Vector Field Theory/VFT Docs/bluesky_bot/stories"
    drafts_dir = base_dir
    live_dir = os.path.join(base_dir, "live")
    darkroom_dir = os.path.join(base_dir, "darkroom")
    quarantine_dir = os.path.join(base_dir, "quarantine")
    
    dirs = {
        "drafts": drafts_dir,
        "live": live_dir,
        "darkroom": darkroom_dir,
        "quarantine": quarantine_dir
    }
    
    all_stories = []
    
    for label, dpath in dirs.items():
        if not os.path.exists(dpath):
            continue
        for fname in os.listdir(dpath):
            if not (fname.startswith("factcheck_") and fname.endswith(".json")):
                continue
            fpath = os.path.join(dpath, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cfg = data[0] if isinstance(data, list) and len(data) > 0 else data
                all_stories.append({
                    "dir": label,
                    "filename": fname,
                    "filepath": fpath,
                    "id": cfg.get("id", ""),
                    "subject": cfg.get("subject", ""),
                    "link": cfg.get("link", "") or cfg.get("url", ""),
                    "grounding_url": cfg.get("grounding_url", ""),
                    "target_url": cfg.get("target_url", ""),
                    "status": cfg.get("status", ""),
                    "size": os.path.getsize(fpath),
                    "posts_len": len(cfg.get("posts", [])) if isinstance(cfg.get("posts"), list) else 0,
                    "claim_u": cfg.get("claim_u"),
                    "claim_psi": cfg.get("claim_psi"),
                    "real_u": cfg.get("real_u"),
                    "real_psi": cfg.get("real_psi"),
                    "posts": cfg.get("posts", []),
                    "data": cfg
                })
            except Exception as e:
                print(f"Error reading {label}/{fname}: {e}")

    print(f"Total stories scanned across all dirs: {len(all_stories)}")
    for l in dirs:
        count = sum(1 for s in all_stories if s["dir"] == l)
        print(f"  - {l}: {count}")

    # Check duplicates by normalized link
    link_map = {}
    for s in all_stories:
        nlink = normalize_url(s["link"])
        if nlink:
            link_map.setdefault(nlink, []).append(s)

    dup_links = {k: v for k, v in link_map.items() if len(v) > 1}
    print(f"\n=== DUPLICATE NORMALIZED LINKS ({len(dup_links)}) ===")
    for k, v in dup_links.items():
        print(f"\nLink: {k}")
        for item in v:
            print(f"  [{item['dir']}] {item['filename']} (posts: {item['posts_len']}, status: '{item['status']}', size: {item['size']}b)")

    # Check duplicates by normalized subject
    subj_map = {}
    for s in all_stories:
        nsubj = normalize_text(s["subject"])
        if nsubj and len(nsubj) > 10:
            subj_map.setdefault(nsubj, []).append(s)

    dup_subjs = {k: v for k, v in subj_map.items() if len(v) > 1}
    print(f"\n=== DUPLICATE NORMALIZED SUBJECTS ({len(dup_subjs)}) ===")
    for k, v in dup_subjs.items():
        print(f"\nSubject: {k}")
        for item in v:
            print(f"  [{item['dir']}] {item['filename']} (posts: {item['posts_len']}, status: '{item['status']}', size: {item['size']}b)")

    # Check duplicates by ID
    id_map = {}
    for s in all_stories:
        sid = s["id"].strip()
        if sid:
            id_map.setdefault(sid, []).append(s)

    dup_ids = {k: v for k, v in id_map.items() if len(v) > 1}
    print(f"\n=== DUPLICATE IDS ({len(dup_ids)}) ===")
    for k, v in dup_ids.items():
        print(f"\nID: {k}")
        for item in v:
            print(f"  [{item['dir']}] {item['filename']} (posts: {item['posts_len']}, status: '{item['status']}', size: {item['size']}b)")

    # Check coordinate desyncs in drafts
    print(f"\n=== DRAFT STORIES COORDINATE / INVARIANT AUDIT ===")
    desync_count = 0
    import re
    from generate_graph import get_path_name

    for s in all_stories:
        if s["dir"] != "drafts":
            continue
        posts = s["posts"]
        if not posts or len(posts) < 3:
            print(f"  [MALFORMED POSTS] {s['filename']}: only {len(posts)} posts")
            desync_count += 1
            continue
        
        # Check Post 2 coords
        p1 = posts[1]
        p2 = posts[2]
        mc = re.search(r'Stated\s+Judg[e]?ment:\s*\([ \t]*([+\-\u2212]?\d+(?:\.\d+)?)[ \t]*,[ \t]*([+\-\u2212]?\d+(?:\.\d+)?)[ \t]*\)', p1, re.IGNORECASE)
        mr = re.search(r'Resulting\s+Judg[e]?ment:\s*\([ \t]*([+\-\u2212]?\d+(?:\.\d+)?)[ \t]*,[ \t]*([+\-\u2212]?\d+(?:\.\d+)?)[ \t]*\)', p2, re.IGNORECASE)
        
        p1_coords = (float(mc.group(1).replace('\u2212', '-')), float(mc.group(2).replace('\u2212', '-'))) if mc else None
        p2_coords = (float(mr.group(1).replace('\u2212', '-')), float(mr.group(2).replace('\u2212', '-'))) if mr else None
        
        root_coords = (s["claim_u"], s["claim_psi"], s["real_u"], s["real_psi"])
        
        issues = []
        if not p1_coords:
            issues.append("Post 2 missing Stated Judgement coordinates")
        elif (round(p1_coords[0], 2), round(p1_coords[1], 2)) != (round(float(s["claim_u"] or 0), 2), round(float(s["claim_psi"] or 0), 2)):
            issues.append(f"Post 2 {p1_coords} != root ({s['claim_u']}, {s['claim_psi']})")
            
        if not p2_coords:
            issues.append("Post 3 missing Resulting Judgement coordinates")
        elif (round(p2_coords[0], 2), round(p2_coords[1], 2)) != (round(float(s["real_u"] or 0), 2), round(float(s["real_psi"] or 0), 2)):
            issues.append(f"Post 3 {p2_coords} != root ({s['real_u']}, {s['real_psi']})")
            
        if issues:
            print(f"  {s['filename']}: {'; '.join(issues)}")
            desync_count += 1

    print(f"\nTotal draft stories with coordinate desyncs/issues: {desync_count}")

if __name__ == "__main__":
    check_draft_duplicates()
