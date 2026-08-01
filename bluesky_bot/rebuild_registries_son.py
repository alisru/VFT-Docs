import json
import glob
import os
import sys
import datetime

ATTRACTORS = {
    'GG': (1.0, 1.0),
    'GE': (-1.0, -1.0),
    'LG': (1.0, -1.0),
    'LE': (-1.0, 1.0),
    'GP': (1.0, 0.0),
    'BP': (-1.0, 0.0)
}

ATTRACTORS_PERP = {
    'GG': (-1.0, 1.0),
    'GE': (1.0, -1.0),
    'LG': (1.0, 1.0),
    'LE': (-1.0, -1.0),
    'GP': (0.0, 1.0),
    'BP': (0.0, -1.0)
}

def calculate_son_coordinates(forces_dict):
    """
    Calculates (u, psi) from a dictionary containing forces for attractors:
    forces_dict: {'GG': {'S': s, 'O': o, 'N': n}, ...}
    """
    F_u = {}
    F_psi = {}
    total_weight = 0.0
    
    for i in ['GG', 'GE', 'LG', 'LE', 'GP', 'BP']:
        if i not in forces_dict:
            continue
        scores = forces_dict[i]
        s = float(scores.get('S', 0.0))
        o = float(scores.get('O', 0.0))
        n = float(scores.get('N', 0.0))
        
        if i == 'GP':
            # GP: Support has neutral Will, Oppose drives Will negative (suppression). Neutral is pure weight dilution.
            f_u = s - o
            f_psi = -o
        elif i == 'BP':
            # BP: Support has neutral Will, Oppose drives Will positive (correction). Neutral is pure weight dilution.
            f_u = -s + o
            f_psi = o
        else:
            a_u, a_psi = ATTRACTORS[i]
            ap_u, ap_psi = ATTRACTORS_PERP[i]
            
            # Net force components
            f_u = s * a_u - o * a_u + n * ap_u
            f_psi = s * a_psi - o * a_psi + n * ap_psi
        
        F_u[i] = f_u
        F_psi[i] = f_psi
        total_weight += (s + o + n)
        
    if total_weight == 0.0:
        return 0.0, 0.0
        
    # 1. Morality Coordinate (u)
    sum_F_u = sum(F_u.values())
    u = sum_F_u / total_weight
    
    # 2. Will Coordinate (psi) using Separated Will (Like-Type) Protocol
    pos_forces = {}
    neg_forces = {}
    pos_weight = 0.0
    neg_weight = 0.0
    
    for i in ['GG', 'GE', 'LG', 'LE', 'GP', 'BP']:
        if i not in forces_dict:
            continue
        scores = forces_dict[i]
        s = float(scores.get('S', 0.0))
        o = float(scores.get('O', 0.0))
        n = float(scores.get('N', 0.0))
        w = s + o + n
        
        f_psi = F_psi.get(i, 0.0)
        if f_psi > 0.0:
            pos_forces[i] = f_psi
            pos_weight += w
        elif f_psi < 0.0:
            neg_forces[i] = f_psi
            neg_weight += w
            
    sum_pos_psi = sum(pos_forces.values())
    sum_neg_psi = sum(neg_forces.values())
    
    abs_pos_psi = abs(sum_pos_psi)
    abs_neg_psi = abs(sum_neg_psi)
    
    if abs_pos_psi == 0.0 and abs_neg_psi == 0.0:
        psi = 0.0
    elif abs_pos_psi >= abs_neg_psi:
        # positive is dominant
        psi = sum_pos_psi / pos_weight if pos_weight > 0.0 else 0.0
    else:
        # negative is dominant
        psi = sum_neg_psi / neg_weight if neg_weight > 0.0 else 0.0
        
    return round(u, 2), round(psi, 2)

def process_and_update_coordinates(cfg, file_path):
    """
    Checks if stated_forces or actual_forces exists, recalculates claim/real u/psi,
    updates them in cfg, and returns True if any change occurred.
    """
    updated = False
    
    # Recalculate Stated
    if "stated_forces" in cfg:
        claim_u, claim_psi = calculate_son_coordinates(cfg["stated_forces"])
        if cfg.get("claim_u") != claim_u or cfg.get("claim_psi") != claim_psi:
            print(f"[{cfg.get('id')}] Updating stated coordinates: ({cfg.get('claim_u')}, {cfg.get('claim_psi')}) -> ({claim_u}, {claim_psi})")
            cfg["claim_u"] = claim_u
            cfg["claim_psi"] = claim_psi
            
            # Also update Stated Judgement string in posts[1] if present
            if len(cfg.get("posts", [])) > 1:
                post = cfg["posts"][1]
                if "Stated Judgement:" in post:
                    label = post.split("—")[-1].strip() if "—" in post else "Good Preference"
                    sgn_u = "+" if claim_u >= 0 else ""
                    sgn_psi = "+" if claim_psi >= 0 else ""
                    cfg["posts"][1] = post.split("Stated Judgement:")[0] + f"Stated Judgement: ({sgn_u}{claim_u:.2f}, {sgn_psi}{claim_psi:.2f}) — {label}"
            updated = True
            
    # Recalculate Actual
    if "actual_forces" in cfg:
        real_u, real_psi = calculate_son_coordinates(cfg["actual_forces"])
        if cfg.get("real_u") != real_u or cfg.get("real_psi") != real_psi:
            print(f"[{cfg.get('id')}] Updating actual coordinates: ({cfg.get('real_u')}, {cfg.get('real_psi')}) -> ({real_u}, {real_psi})")
            cfg["real_u"] = real_u
            cfg["real_psi"] = real_psi
            
            # Also update Resulting Judgement string in posts[2] if present
            if len(cfg.get("posts", [])) > 2:
                post = cfg["posts"][2]
                if "Resulting Judgement:" in post:
                    label = post.split("—")[-1].strip() if "—" in post else "Greater Evil"
                    sgn_u = "+" if real_u >= 0 else ""
                    sgn_psi = "+" if real_psi >= 0 else ""
                    cfg["posts"][2] = post.split("Resulting Judgement:")[0] + f"Resulting Judgement: ({sgn_u}{real_u:.2f}, {sgn_psi}{real_psi:.2f}) — {label}"
            updated = True
            
    return updated

def rebuild_registries():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(script_dir)

    from generate_graph import draw_graph
    from image_card_generator import generate_compact_info_card

    stories_dir = os.path.join(script_dir, "stories")
    live_dir    = os.path.join(stories_dir, "live")
    darkroom_dir = os.path.join(stories_dir, "darkroom")
    graph_png_dir = os.path.join(script_dir, "graph_png")

    os.makedirs(darkroom_dir, exist_ok=True)
    os.makedirs(graph_png_dir, exist_ok=True)

    def slug_from_path(p):
        b = os.path.basename(p)
        if b.startswith("factcheck_") and b.endswith(".json"):
            return b[len("factcheck_"):-len(".json")]
        return None

    def safe_getmtime(p):
        try:
            return os.path.getmtime(p)
        except OSError:
            return 0.0

    # 0. Staging/Darkroom Promotion Gate
    darkroom_paths = glob.glob(os.path.join(darkroom_dir, "factcheck_*.json"))
    if darkroom_paths:
        print(f"Found {len(darkroom_paths)} stories in darkroom. Generating graphs and promoting...")
        for p in darkroom_paths:
            slug = slug_from_path(p)
            if not slug:
                continue
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cfg = data[0] if isinstance(data, list) else data
            except Exception as e:
                print(f"Error reading darkroom file {p}: {e}")
                continue

            # Update coordinates deterministically if raw forces are defined
            if process_and_update_coordinates(cfg, p):
                try:
                    with open(p, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                except Exception as we:
                    print(f"Warning: Failed to save updated darkroom file {p}: {we}")

            # Generate graph
            graph_filename = f"{slug}_graph.png"
            graph_path = os.path.join(graph_png_dir, graph_filename)
            try:
                print(f"Generating staging graph for {slug}...")
                draw_graph(
                    cfg.get("claim_u", 0.0), cfg.get("claim_psi", 0.0),
                    cfg.get("real_u",   0.0), cfg.get("real_psi",  0.0),
                    cfg.get("subject", "Story"),
                    graph_path,
                    macro_event=cfg.get("macro_event", ""),
                    macro_claim_u=cfg.get("macro_claim_u"),
                    macro_claim_psi=cfg.get("macro_claim_psi"),
                    macro_real_u=cfg.get("macro_real_u"),
                    macro_real_psi=cfg.get("macro_real_psi")
                )
            except Exception as ge:
                print(f"Error generating graph for {slug} in darkroom: {ge}")

            # Generate compact summary card if compact mode is enabled
            if cfg.get("compact", False):
                info_card_filename = f"{slug}_info_card.png"
                info_card_path = os.path.join(graph_png_dir, info_card_filename)
                try:
                    print(f"Generating compact summary info card for {slug}...")
                    generate_compact_info_card(cfg, info_card_path)
                except Exception as ice:
                    print(f"Error generating compact info card for {slug} in darkroom: {ice}")

            # Promote config to stories/
            dest_path = os.path.join(stories_dir, os.path.basename(p))
            try:
                with open(dest_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                os.remove(p)
                print(f"Promoted {slug} from darkroom to stories/")
            except Exception as e:
                print(f"Error promoting {slug} from darkroom: {e}")

    # 1. Scan stories/ and stories/live/
    draft_paths = glob.glob(os.path.join(stories_dir, "factcheck_*.json"))
    live_paths  = glob.glob(os.path.join(live_dir,    "factcheck_*.json"))

    draft_filenames = [os.path.basename(p) for p in sorted(draft_paths, key=safe_getmtime)]
    live_filenames  = [os.path.basename(p) for p in sorted(live_paths,  key=safe_getmtime)]

    # 2. Write index files
    try:
        with open(os.path.join(stories_dir, "index.json"), "w", encoding="utf-8") as f:
            json.dump(draft_filenames, f, indent=2, ensure_ascii=False)
        print(f"Compiled stories/index.json ({len(draft_filenames)} entries)")
    except Exception as e:
        print(f"Warning: Failed to write stories/index.json: {e}")

    try:
        os.makedirs(live_dir, exist_ok=True)
        with open(os.path.join(live_dir, "index.json"), "w", encoding="utf-8") as f:
            json.dump(live_filenames, f, indent=2, ensure_ascii=False)
        print(f"Compiled stories/live/index.json ({len(live_filenames)} entries)")
    except Exception as e:
        print(f"Warning: Failed to write stories/live/index.json: {e}")

    # 3. Build story map — newest file wins for a given slug
    story_map = {}
    for p in live_paths:
        s = slug_from_path(p)
        if s:
            story_map[s] = (p, True)

    for p in draft_paths:
        s = slug_from_path(p)
        if s:
            if s not in story_map or safe_getmtime(p) > safe_getmtime(story_map[s][0]):
                story_map[s] = (p, False)

    print(f"Scanning stories registry: found {len(story_map)} unique story IDs.")

    # 4. Build registry entries
    active_story_ids  = set()
    active_stories      = []
    active_live_stories = []

    sorted_slugs = sorted(
        story_map.keys(),
        key=lambda s: safe_getmtime(story_map[s][0])
    )

    for slug in sorted_slugs:
        authoritative_file, is_live = story_map[slug]

        try:
            with open(authoritative_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = data[0] if isinstance(data, list) else data
        except Exception as e:
            print(f"Error reading {authoritative_file}: {e}")
            continue

        # Recalculate coordinates deterministically if raw forces are defined
        coords_changed = process_and_update_coordinates(cfg, authoritative_file)
        if coords_changed:
            try:
                with open(authoritative_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            except Exception as we:
                print(f"Warning: Failed to save updated config {authoritative_file}: {we}")

        # Auto-backfill missing/empty actors using the deterministic actor_extract utility
        if "actors" not in cfg:
            from actor_extract import extract_actors
            inferred = extract_actors(cfg.get("subject", ""))
            cfg["actors"] = inferred
            try:
                with open(authoritative_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"Auto-tagged missing actors for {slug}: {inferred}")
            except Exception as we:
                print(f"Warning: Failed to write back auto-tagged actors to {authoritative_file}: {we}")

        active_story_ids.add(slug)

        # Generate graph if missing or if coordinates changed
        graph_filename = f"{slug}_graph.png"
        graph_path = os.path.join(graph_png_dir, graph_filename)
        
        # If coordinates changed, we must regenerate the graph!
        # So we force regeneration if coordinates were updated or if the graph is missing
        if coords_changed or not os.path.exists(graph_path):
            try:
                print(f"Generating graph for {slug}...")
                draw_graph(
                    cfg.get("claim_u", 0.0), cfg.get("claim_psi", 0.0),
                    cfg.get("real_u",   0.0), cfg.get("real_psi",  0.0),
                    cfg.get("subject", "Story"),
                    graph_path,
                    macro_event=cfg.get("macro_event", ""),
                    macro_claim_u=cfg.get("macro_claim_u"),
                    macro_claim_psi=cfg.get("macro_claim_psi"),
                    macro_real_u=cfg.get("macro_real_u"),
                    macro_real_psi=cfg.get("macro_real_psi")
                )
            except Exception as ge:
                print(f"Error generating graph for {slug}: {ge}")

        # Normalise graph_img key
        graph_img = cfg.get("graph_img") or graph_filename
        if not graph_img.startswith("graph_png/"):
            graph_img = f"graph_png/{graph_img}"

        # Verdict
        verdict = cfg.get("verdict")
        if not verdict and len(cfg.get("posts", [])) > 3:
            verdict = cfg["posts"][3].replace("Verdict: ", "")
        if not verdict:
            verdict = "FAIL — The Path of Deception"

        status = cfg.get("status", "")

        mtime = safe_getmtime(authoritative_file)
        created_at = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

        registry_story = {
            "id":        slug,
            "subject":   cfg.get("subject"),
            "link":      cfg.get("link"),
            "claim_u":   cfg.get("claim_u"),
            "claim_psi": cfg.get("claim_psi"),
            "real_u":    cfg.get("real_u"),
            "real_psi":  cfg.get("real_psi"),
            "mode":      cfg.get("mode", "root"),
            "status":    status or "COMPLETED DRY RUN",
            "verdict":   verdict,
            "graph_img": graph_img,
            "posts":     cfg.get("posts"),
            "created_at": created_at,
        }
        # CRITICAL WARNING: DO NOT remove "posts" or other metadata from this list to optimize file size.
        # The control panel UI relies entirely on "posts" to render the thread emulator.
        for k in ["target_url", "rkeys", "post_urls", "posts", "actors", "category", "topic", "event",
                  "macro_event", "macro_claim_u", "macro_claim_psi", "macro_real_u", "macro_real_psi",
                  "stated_forces", "actual_forces", "grounding_url", "claim_rnet", "real_rnet",
                  "claim_z", "real_z", "claim_z_profile", "real_z_profile", "claim_integrity", "real_integrity"]:
            if k in cfg:
                registry_story[k] = cfg[k]

        if is_live:
            if not ("LIVE" in status.upper() or cfg.get("rkeys") or cfg.get("post_urls")):
                registry_story["status"] = "LIVE POSTED"
            active_live_stories.append(registry_story)
        else:
            if "LIVE" in status.upper() or cfg.get("rkeys") or cfg.get("post_urls"):
                registry_story["status"] = "COMPLETED DRY RUN"
            active_stories.append(registry_story)

    # 5. Write stories_registry.js (single file, next to control_panel.html)
    combined = active_live_stories + active_stories
    combined.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    registry_js = f"window.ALETHEIA_STORIES_REGISTRY = {json.dumps(combined, indent=2, ensure_ascii=False)};\n"
    registry_path = os.path.join(script_dir, "stories_registry.js")
    try:
        with open(registry_path, "w", encoding="utf-8") as f:
            f.write(registry_js)
        print(f"Compiled stories_registry.js ({len(combined)} stories, {len(active_live_stories)} live)")
        
        # Log how many stories are in the harvested stories buffer (queue)
        queue_path = os.path.join(script_dir, "harvested_candidates.json")
        pending_count = 0
        if os.path.exists(queue_path):
            try:
                with open(queue_path, 'r', encoding='utf-8') as f:
                    q_data = json.load(f)
                    if isinstance(q_data, list):
                        pending_count = len(q_data)
            except Exception:
                pass
        print(f"Pending candidates in harvested stories buffer: {pending_count}")
    except Exception as e:
        print(f"Warning: Failed to write stories_registry.js: {e}")

    # 6. Clean up orphan graph images
    for f in os.listdir(graph_png_dir):
        if f.endswith("_graph.png"):
            sid = f[:-len("_graph.png")]
            if sid not in active_story_ids:
                gp = os.path.join(graph_png_dir, f)
                try:
                    os.remove(gp)
                    print(f"[CLEANUP] Deleted orphan graph: {gp}")
                except Exception as e:
                    print(f"Warning: Could not delete orphan graph {gp}: {e}")

    print("Rebuilding complete!")

if __name__ == '__main__':
    rebuild_registries()
