import json
import glob
import os
import sys

def rebuild_registries():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(script_dir)

    from generate_graph import draw_graph

    stories_dir = os.path.join(script_dir, "stories")
    live_dir    = os.path.join(stories_dir, "live")

    # 1. Scan stories/ and stories/live/
    draft_paths = glob.glob(os.path.join(stories_dir, "factcheck_*.json"))
    live_paths  = glob.glob(os.path.join(live_dir,    "factcheck_*.json"))

    draft_filenames = [os.path.basename(p) for p in sorted(draft_paths, key=os.path.getmtime)]
    live_filenames  = [os.path.basename(p) for p in sorted(live_paths,  key=os.path.getmtime)]

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

    # 3. Build story map — live/ is always authoritative for a given slug
    def slug_from_path(p):
        b = os.path.basename(p)
        if b.startswith("factcheck_") and b.endswith(".json"):
            return b[len("factcheck_"):-len(".json")]
        return None

    # Map slug -> (authoritative_path, is_live)
    story_map = {}
    for p in live_paths:
        s = slug_from_path(p)
        if s:
            story_map[s] = (p, True)

    for p in draft_paths:
        s = slug_from_path(p)
        if s and s not in story_map:   # live already wins — don't overwrite
            story_map[s] = (p, False)

    print(f"Scanning stories registry: found {len(story_map)} unique story IDs.")

    # 4. Build registry entries
    active_story_ids  = set()
    active_stories      = []
    active_live_stories = []

    graph_png_dir = os.path.join(script_dir, "graph_png")
    os.makedirs(graph_png_dir, exist_ok=True)

    sorted_slugs = sorted(
        story_map.keys(),
        key=lambda s: os.path.getmtime(story_map[s][0])
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

        active_story_ids.add(slug)

        # Generate graph if missing
        graph_filename = f"{slug}_graph.png"
        graph_path = os.path.join(graph_png_dir, graph_filename)
        if not os.path.exists(graph_path):
            try:
                print(f"Generating graph for {slug}...")
                draw_graph(
                    cfg.get("claim_u", 0.0), cfg.get("claim_psi", 0.0),
                    cfg.get("real_u",   0.0), cfg.get("real_psi",  0.0),
                    cfg.get("subject", "Story"),
                    graph_path
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
        }
        for k in ["target_url", "rkeys", "post_urls"]:
            if k in cfg:
                registry_story[k] = cfg[k]

        if is_live:
            # File is in live/ — force status to LIVE POSTED if not already marked
            if not ("LIVE" in status.upper() or cfg.get("rkeys") or cfg.get("post_urls")):
                registry_story["status"] = "LIVE POSTED"
            active_live_stories.append(registry_story)
        else:
            # File is in stories/ root — it's a dry run, strip any accidental LIVE status
            if "LIVE" in status.upper() or cfg.get("rkeys") or cfg.get("post_urls"):
                registry_story["status"] = "COMPLETED DRY RUN"
            active_stories.append(registry_story)

    # 5. Write stories_registry.js (single file, next to control_panel.html)
    combined = active_live_stories + active_stories
    registry_js = f"window.ALETHEIA_STORIES_REGISTRY = {json.dumps(combined, indent=2, ensure_ascii=False)};\n"
    registry_path = os.path.join(script_dir, "stories_registry.js")
    try:
        with open(registry_path, "w", encoding="utf-8") as f:
            f.write(registry_js)
        print(f"Compiled stories_registry.js ({len(combined)} stories, {len(active_live_stories)} live)")
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
