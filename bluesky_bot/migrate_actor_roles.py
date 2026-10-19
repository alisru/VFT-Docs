"""Batch migration script to classify existing actors into the 7-Role Taxonomy.

Runs offline and deterministically across all stories in `stories/` and `stories/live/`.
Parses existing sub-audits in Post 5 when available to ground roles and individual verdicts.
"""
import os
import glob
import json
import re
from actor_extract import classify_actor_role, clean_roundup_subject

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STORIES_DIR = os.path.join(SCRIPT_DIR, "stories")

SUB_AUDIT_PATTERN = re.compile(r'-\s*([^:]+):\s*(PASS|FAIL|COND)\s*\(([^)]+)\)', re.IGNORECASE)


def parse_sub_audits(posts):
    """Extract explicit entity sub-audits from Post 5 (index 4) if present."""
    if not posts or len(posts) < 5:
        return {}
    post5 = posts[4]
    if "Sub-Audits Breakdown:" not in post5:
        return {}
    
    results = {}
    matches = SUB_AUDIT_PATTERN.findall(post5)
    for entity, verdict, coords in matches:
        ent_clean = entity.strip()
        v_clean = verdict.strip().upper()
        # Parse coordinates if present: e.g. "+0.9, +0.8"
        try:
            parts = [float(p.strip()) for p in coords.split(",")]
            u = parts[0] if len(parts) > 0 else None
            psi = parts[1] if len(parts) > 1 else None
        except Exception:
            u, psi = None, None
        results[ent_clean.lower()] = {
            "entity": ent_clean,
            "verdict": v_clean,
            "u": u,
            "psi": psi
        }
    return results


def migrate_story_actor_roles(file_path, dry_run=False):
    """Reads a story file, classifies its actors, and appends actor_roles."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return None, f"Read error: {e}"

    cfg = None
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        cfg = data[0]
    elif isinstance(data, dict):
        cfg = data.get("story", data)

    if not cfg:
        return None, "Invalid story JSON format"

    actors = cfg.get("actors", [])
    subject = cfg.get("subject", "")
    posts = cfg.get("posts", [])
    sub_audits = parse_sub_audits(posts)

    new_roles = []
    cleaned_actors = []

    for act in actors:
        if not act or len(str(act).strip()) < 2:
            continue
        act_str = str(act).strip()
        act_lower = act_str.lower()
        
        # Check if entity was specifically sub-audited
        sub_info = None
        for sa_key, sa_val in sub_audits.items():
            if sa_key in act_lower or act_lower in sa_key:
                sub_info = sa_val
                break

        role = classify_actor_role(act_str, story_context=subject)
        
        # Refine role based on sub-audit evidence
        if sub_info:
            if sub_info["verdict"] == "PASS" and role == "instigator":
                # If an entity was audited with PASS for investigating/reporting, mark as author or regulator
                if any(w in act_lower for w in ["investigation", "report", "journalism", "propublica", "monitor"]):
                    role = "author"
                elif any(w in act_lower for w in ["court", "sentencing", "judge", "audit", "science"]):
                    role = "regulator"
            elif sub_info["verdict"] == "FAIL" and role != "instigator":
                # If an entity was audited with FAIL for committing abuses, ensure it's marked as instigator
                role = "instigator"

        entry = {"name": act_str, "role": role}
        if sub_info and sub_info.get("u") is not None:
            entry["sub_u"] = sub_info["u"]
            entry["sub_psi"] = sub_info["psi"]
            entry["sub_verdict"] = sub_info["verdict"]

        new_roles.append(entry)
        cleaned_actors.append(act_str)

    cfg["actors"] = cleaned_actors
    cfg["actor_roles"] = new_roles

    if not dry_run:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            return None, f"Write error: {e}"

    return new_roles, None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Migrate stories to 7-Role Actor Taxonomy")
    parser.add_argument("--dry-run", action="store_true", help="Print sample changes without writing to disk")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of stories processed (0 for all)")
    args = parser.parse_args()

    # Collect files from stories/ and stories/live/
    live_files = glob.glob(os.path.join(STORIES_DIR, "live", "*.json"))
    root_files = glob.glob(os.path.join(STORIES_DIR, "*.json"))
    all_files = [f for f in (live_files + root_files) if not f.endswith("index.json")]

    if args.limit > 0:
        all_files = all_files[:args.limit]

    print(f"Total story files to process: {len(all_files)}")
    
    role_counts = {}
    modified = 0
    errors = 0

    for i, fpath in enumerate(all_files):
        roles, err = migrate_story_actor_roles(fpath, dry_run=args.dry_run)
        if err:
            errors += 1
            continue
        modified += 1
        for r in roles:
            rk = r["role"]
            role_counts[rk] = role_counts.get(rk, 0) + 1
            
        if args.dry_run and i < 10:
            fname = os.path.basename(fpath)
            print(f"[{fname}] -> {roles}")

    print("\n" + "="*50)
    print(f"Migration Complete: {modified} files processed, {errors} errors.")
    print("Role Distribution:")
    for rk, count in sorted(role_counts.items(), key=lambda x: -x[1]):
        print(f"  {rk:12}: {count}")
    print("="*50)


if __name__ == '__main__':
    main()
