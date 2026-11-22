import os
import sys
import json
import glob
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
bot_dir = os.path.dirname(script_dir)
if bot_dir not in sys.path:
    sys.path.insert(0, bot_dir)

from generate_graph import get_path_name, enforce_deterministic_trajectory

def normalize_url(u):
    if not u:
        return ""
    return u.split("?")[0].split("#")[0].rstrip("/").lower().strip()

def normalize_text(t):
    if not t:
        return ""
    return re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()

def audit_draft_stories():
    base_dir = os.path.join(bot_dir, "stories")
    live_dir = os.path.join(base_dir, "live")
    
    draft_files = sorted(glob.glob(os.path.join(base_dir, "factcheck_*.json")))
    live_files = glob.glob(os.path.join(live_dir, "factcheck_*.json"))
    
    print(f"Total Drafts in stories/: {len(draft_files)}")
    print(f"Total Live in stories/live/: {len(live_files)}")
    
    # Map live URLs and live subjects
    live_urls = set()
    live_subjs = set()
    for lf in live_files:
        try:
            with open(lf, "r", encoding="utf-8") as f:
                d = json.load(f)
            cfg = d[0] if isinstance(d, list) and len(d) > 0 else d
            u = normalize_url(cfg.get("link") or cfg.get("url"))
            s = normalize_text(cfg.get("subject"))
            if u:
                live_urls.add(u)
            if s and len(s) > 10:
                live_subjs.add(s)
        except Exception:
            pass

    # Check drafts
    draft_entries = []
    draft_url_map = {}
    draft_subj_map = {}
    
    drafts_already_live = []
    draft_internal_dups = []
    
    for df in draft_files:
        fname = os.path.basename(df)
        try:
            with open(df, "r", encoding="utf-8") as f:
                d = json.load(f)
            cfg = d[0] if isinstance(d, list) and len(d) > 0 else d
            u = normalize_url(cfg.get("link") or cfg.get("url"))
            s = normalize_text(cfg.get("subject"))
            
            entry = {
                "file": fname,
                "path": df,
                "url": u,
                "raw_url": cfg.get("link") or cfg.get("url") or "",
                "subject": cfg.get("subject", ""),
                "norm_subj": s,
                "size": os.path.getsize(df),
                "data": cfg
            }
            draft_entries.append(entry)
            
            # Check against live
            if u and u in live_urls:
                drafts_already_live.append((fname, "URL matches live", u))
            elif s and s in live_subjs:
                drafts_already_live.append((fname, "Subject matches live", s))
                
            if u:
                draft_url_map.setdefault(u, []).append(entry)
            if s and len(s) > 10:
                draft_subj_map.setdefault(s, []).append(entry)
        except Exception as ex:
            print(f"Error reading draft {fname}: {ex}")

    # Internal draft duplicates
    for u, elist in draft_url_map.items():
        if len(elist) > 1:
            draft_internal_dups.append(("URL", u, [e["file"] for e in elist]))
            
    for s, elist in draft_subj_map.items():
        if len(elist) > 1 and not any(d[0] == "URL" and set([e["file"] for e in elist]).issubset(set(d[2])) for d in draft_internal_dups):
            draft_internal_dups.append(("Subject", s, [e["file"] for e in elist]))

    print(f"\n1. Drafts already published in live/ ({len(drafts_already_live)}):")
    for fname, reason, match in drafts_already_live:
        print(f"   - {fname} ({reason}: {match})")

    print(f"\n2. Duplicate Drafts among themselves ({len(draft_internal_dups)} clusters):")
    for dtype, key, flist in draft_internal_dups:
        print(f"   - [{dtype}] {key[:60]} -> {flist}")

    # Check coordinate desyncs and fixable issues in drafts
    print(f"\n3. Checking Coordinate and Invariant Sync across {len(draft_entries)} drafts...")
    needs_trajectory_sync = []
    
    for entry in draft_entries:
        cfg = entry["data"]
        posts = cfg.get("posts", [])
        if not posts or len(posts) < 3:
            continue
            
        # Check Post 2 coords
        p1 = posts[1]
        p2 = posts[2]
        mc = re.search(r'Stated\s+Judg[e]?ment:\s*\([ \t]*([+\-\u2212]?\d+(?:\.\d+)?)[ \t]*,[ \t]*([+\-\u2212]?\d+(?:\.\d+)?)[ \t]*\)', p1, re.IGNORECASE)
        mr = re.search(r'Resulting\s+Judg[e]?ment:\s*\([ \t]*([+\-\u2212]?\d+(?:\.\d+)?)[ \t]*,[ \t]*([+\-\u2212]?\d+(?:\.\d+)?)[ \t]*\)', p2, re.IGNORECASE)
        
        p1_u = float(mc.group(1).replace('\u2212', '-')) if mc else None
        p1_psi = float(mc.group(2).replace('\u2212', '-')) if mc else None
        p2_u = float(mr.group(1).replace('\u2212', '-')) if mr else None
        p2_psi = float(mr.group(2).replace('\u2212', '-')) if mr else None
        
        c_u = cfg.get("claim_u")
        c_psi = cfg.get("claim_psi")
        r_u = cfg.get("real_u")
        r_psi = cfg.get("real_psi")
        
        diff = False
        if p1_u is not None and (c_u is None or round(p1_u, 2) != round(float(c_u), 2)):
            diff = True
        if p1_psi is not None and (c_psi is None or round(p1_psi, 2) != round(float(c_psi), 2)):
            diff = True
        if p2_u is not None and (r_u is None or round(p2_u, 2) != round(float(r_u), 2)):
            diff = True
        if p2_psi is not None and (r_psi is None or round(p2_psi, 2) != round(float(r_psi), 2)):
            diff = True
            
        if diff:
            needs_trajectory_sync.append((entry["file"], f"Post 2: ({p1_u}, {p1_psi}) vs Root: ({c_u}, {c_psi}) | Post 3: ({p2_u}, {p2_psi}) vs Root: ({r_u}, {r_psi})"))

    print(f"\n4. Checking requeued_to_harvest directory...")
    requeued_dir = os.path.join(base_dir, "requeued_to_harvest")
    if os.path.exists(requeued_dir):
        r_files = glob.glob(os.path.join(requeued_dir, "factcheck_*.json"))
        print(f"   requeued_to_harvest has {len(r_files)} files")
        
        # Check URLs and subjects in requeued vs drafts
        r_url_matches = []
        r_subj_matches = []
        
        draft_urls = {e["url"]: e["file"] for e in draft_entries if e["url"]}
        draft_subjs = {e["norm_subj"]: e["file"] for e in draft_entries if e["norm_subj"]}
        
        for rf in r_files:
            fname = os.path.basename(rf)
            try:
                with open(rf, "r", encoding="utf-8") as f:
                    rd = json.load(f)
                rcfg = rd[0] if isinstance(rd, list) and len(rd) > 0 else rd
                ru = normalize_url(rcfg.get("link") or rcfg.get("url"))
                rs = normalize_text(rcfg.get("subject"))
                
                if ru in draft_urls:
                    r_url_matches.append((fname, draft_urls[ru], ru))
                elif rs in draft_subjs:
                    r_subj_matches.append((fname, draft_subjs[rs], rs))
            except Exception:
                pass
                
        print(f"   URL matches between requeued and drafts: {len(r_url_matches)}")
        unmatched_r = [rf for rf in r_files if os.path.basename(rf) not in [m[0] for m in r_url_matches]]
        print(f"   Remaining {len(unmatched_r)} files in requeued not matching draft URLs:")
        for rf in unmatched_r:
            try:
                with open(rf, "r", encoding="utf-8") as f:
                    rd = json.load(f)
                rcfg = rd[0] if isinstance(rd, list) and len(rd) > 0 else rd
                print(f"      {os.path.basename(rf)} -> URL: {rcfg.get('link')} | Subj: {rcfg.get('subject')}")
            except Exception:
                pass
        print(f"   Subject matches between requeued and drafts: {len(r_subj_matches)}")
        for rf, df, s in r_subj_matches:
            print(f"      requeued: {rf} == draft: {df} (subj: {s[:40]})")

    print(f"\n5. Checking trajectory graphs for all 117 drafts...")
    graph_dir = os.path.join(bot_dir, "graph_png")
    missing_graphs = []
    for entry in draft_entries:
        cfg = entry["data"]
        sid = cfg.get("id") or entry["file"].replace("factcheck_", "").replace(".json", "")
        g_file = os.path.join(graph_dir, f"{sid}_graph.png")
        if not os.path.exists(g_file):
            missing_graphs.append((entry["file"], sid))
            
    print(f"Drafts missing trajectory graph images in graph_png/: {len(missing_graphs)}")
    for f, sid in missing_graphs[:10]:
        print(f"   - {f} (id: {sid})")

    for f in ["factcheck_6g-phones-arrive-in-2030-fight-over-airwaves.json", "factcheck_american-democracy-was-a-big-winner-in-the-midterms.json", "factcheck_anchorage-mpox-advisory-2026.json", "factcheck_armed-migrant-arrest-white-house.json"]:
        p = os.path.join(requeued_dir, f)
        try:
            with open(p, "r", encoding="utf-8") as fh:
                d = json.load(fh)
            cfg = d[0] if isinstance(d, list) and len(d) > 0 else d
            print(f"      [4 CANDIDATES] {f} -> posts: {len(cfg.get('posts', []))}, status: '{cfg.get('status')}'")
        except Exception as e:
            print(f"      [4 CANDIDATES] {f} -> Error: {e}")

    print(f"\n6. Checking candidate JSON files for duplicates...")
    for cfile in ["harvested_candidates.json", "filtered_candidates.json"]:
        cpath = os.path.join(bot_dir, cfile)
        if os.path.exists(cpath):
            try:
                with open(cpath, "r", encoding="utf-8") as f:
                    cdata = json.load(f)
                if isinstance(cdata, list):
                    urls = [c.get("url") or c.get("link") for c in cdata if isinstance(c, dict)]
                    subjs = [c.get("subject") or c.get("title") for c in cdata if isinstance(c, dict)]
                    print(f"   {cfile}: {len(cdata)} items, {len(set(urls))} unique URLs, {len(set(subjs))} unique subjects")
                    if len(cdata) != len(set(urls)):
                        print(f"      -> {len(cdata) - len(set(urls))} duplicate URLs in {cfile}!")
            except Exception as e:
                print(f"   Error reading {cfile}: {e}")

    print(f"\n5. Checking internal content of 117 draft files (duplicate posts, repeated sources, etc.)...")
    internal_issues = []
    for entry in draft_entries:
        cfg = entry["data"]
        posts = cfg.get("posts", [])
        
        # Check duplicate posts in posts array
        if len(posts) != len(set(posts)):
            internal_issues.append((entry["file"], "Duplicate post strings inside posts array!"))
            
        # Check if verification URL or link is mentioned multiple times in post texts
        g_url = cfg.get("grounding_url")
        link = cfg.get("link")
        
        source_count = 0
        for p in posts:
            if "Source:" in p or "Evidence:" in p or (g_url and g_url in p):
                source_count += 1
        if source_count > 2:
            internal_issues.append((entry["file"], f"Source/evidence mentioned in {source_count} different posts"))

    print(f"Drafts with internal post duplication/repetition: {len(internal_issues)}")
    for f, iss in internal_issues[:20]:
        print(f"   - {f}: {iss}")

if __name__ == "__main__":
    audit_draft_stories()
