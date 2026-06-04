import json
import glob
import os
import sys
import shutil

def rebuild_registries():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(script_dir)
    
    from generate_graph import draw_graph
    
    bot_stories_dir = os.path.join(script_dir, "stories")
    gen_stories_dir = os.path.join(parent_dir, "_Generated_Content", "stories")
    
    # 1. Scan bot_stories_dir
    bot_search_draft = os.path.join(bot_stories_dir, "factcheck_*.json")
    bot_search_live = os.path.join(bot_stories_dir, "live", "factcheck_*.json")
    
    bot_draft_paths = glob.glob(bot_search_draft)
    bot_live_paths = glob.glob(bot_search_live)
    
    # Sort files by mtime (newest first)
    bot_draft_paths_sorted = sorted(bot_draft_paths, key=os.path.getmtime)
    bot_draft_filenames = [os.path.basename(p) for p in bot_draft_paths_sorted]
    
    bot_live_paths_sorted = sorted(bot_live_paths, key=os.path.getmtime)
    bot_live_filenames = [os.path.basename(p) for p in bot_live_paths_sorted]
    
    # Write index.json in bot_stories_dir
    try:
        dry_index_path = os.path.join(bot_stories_dir, "index.json")
        with open(dry_index_path, "w", encoding="utf-8") as out:
            json.dump(bot_draft_filenames, out, indent=2, ensure_ascii=False)
        print(f"Compiled index.json at {dry_index_path}")
    except Exception as e:
        print(f"Warning: Failed to compile index.json at {dry_index_path}: {e}")
        
    try:
        live_index_path = os.path.join(bot_stories_dir, "live", "index.json")
        os.makedirs(os.path.dirname(live_index_path), exist_ok=True)
        with open(live_index_path, "w", encoding="utf-8") as out:
            json.dump(bot_live_filenames, out, indent=2, ensure_ascii=False)
        print(f"Compiled live index.json at {live_index_path}")
    except Exception as e:
        print(f"Warning: Failed to compile live index.json at {live_index_path}: {e}")

    # 2. Scan gen_stories_dir
    gen_search_draft = os.path.join(gen_stories_dir, "factcheck_*.json")
    gen_search_live = os.path.join(gen_stories_dir, "live", "factcheck_*.json")
    
    gen_draft_paths = glob.glob(gen_search_draft)
    gen_live_paths = glob.glob(gen_search_live)
    
    gen_draft_paths_sorted = sorted(gen_draft_paths, key=os.path.getmtime)
    gen_draft_filenames = [os.path.basename(p) for p in gen_draft_paths_sorted]
    
    gen_live_paths_sorted = sorted(gen_live_paths, key=os.path.getmtime)
    gen_live_filenames = [os.path.basename(p) for p in gen_live_paths_sorted]
    
    # Write index.json in gen_stories_dir
    try:
        dry_index_path_gen = os.path.join(gen_stories_dir, "index.json")
        os.makedirs(os.path.dirname(dry_index_path_gen), exist_ok=True)
        with open(dry_index_path_gen, "w", encoding="utf-8") as out:
            json.dump(gen_draft_filenames, out, indent=2, ensure_ascii=False)
        print(f"Compiled index.json at {dry_index_path_gen}")
    except Exception as e:
        print(f"Warning: Failed to compile index.json at {dry_index_path_gen}: {e}")
        
    try:
        live_index_path_gen = os.path.join(gen_stories_dir, "live", "index.json")
        os.makedirs(os.path.dirname(live_index_path_gen), exist_ok=True)
        with open(live_index_path_gen, "w", encoding="utf-8") as out:
            json.dump(gen_live_filenames, out, indent=2, ensure_ascii=False)
        print(f"Compiled live index.json at {live_index_path_gen}")
    except Exception as e:
        print(f"Warning: Failed to compile live index.json at {live_index_path_gen}: {e}")

    # 3. Collect unique stories to build stories_registry.js
    all_json_files = (
        bot_draft_paths + bot_live_paths +
        gen_draft_paths + gen_live_paths
    )
    
    def extract_story_id(filepath):
        basename = os.path.basename(filepath)
        if basename.startswith("factcheck_") and basename.endswith(".json"):
            return basename[len("factcheck_"):-len(".json")]
        return None

    story_map = {}
    for p in all_json_files:
        sid = extract_story_id(p)
        if sid:
            story_map.setdefault(sid, []).append(p)
            
    print(f"Scanning stories registry: found {len(story_map)} unique story IDs.")
    
    active_story_ids = set()
    active_stories = []
    active_live_stories = []
    
    story_newest_mtimes = {}
    for sid, paths in story_map.items():
        story_newest_mtimes[sid] = max(os.path.getmtime(p) for p in paths)
        
    sorted_story_ids = sorted(story_map.keys(), key=lambda sid: story_newest_mtimes[sid])
    
    for slug in sorted_story_ids:
        paths = story_map[slug]
        newest_file = max(paths, key=os.path.getmtime)
        
        try:
            with open(newest_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = data[0] if isinstance(data, list) else data
            
            active_story_ids.add(slug)
            
            graph_filename = f"{slug}_graph.png"
            bot_graph_path = os.path.join(script_dir, "graph_png", graph_filename)
            gen_graph_path = os.path.join(parent_dir, "_Generated_Content", "graph_png", graph_filename)
            
            # Draw graph if missing
            if not os.path.exists(bot_graph_path) or not os.path.exists(gen_graph_path):
                try:
                    print(f"Generating graph for {slug}...")
                    os.makedirs(os.path.dirname(bot_graph_path), exist_ok=True)
                    draw_graph(
                        cfg.get("claim_u", 0.0), cfg.get("claim_psi", 0.0),
                        cfg.get("real_u", 0.0), cfg.get("real_psi", 0.0),
                        cfg.get("subject", "Story"),
                        bot_graph_path
                    )
                    os.makedirs(os.path.dirname(gen_graph_path), exist_ok=True)
                    shutil.copy2(bot_graph_path, gen_graph_path)
                except Exception as ge:
                    print(f"Error generating graph for {slug}: {ge}")
                    
            # Format registry entry
            graph_img = cfg.get("graph_img") or f"{slug}_graph.png"
            if graph_img and not graph_img.startswith("graph_png/"):
                graph_img = f"graph_png/{graph_img}"
                
            verdict = cfg.get("verdict")
            if not verdict and len(cfg.get("posts", [])) > 3:
                verdict = cfg["posts"][3].replace("Verdict: ", "")
            if not verdict:
                verdict = "FAIL — The Path of Deception"
                
            registry_story = {
                "id": slug,
                "subject": cfg.get("subject"),
                "link": cfg.get("link"),
                "claim_u": cfg.get("claim_u"),
                "claim_psi": cfg.get("claim_psi"),
                "real_u": cfg.get("real_u"),
                "real_psi": cfg.get("real_psi"),
                "mode": cfg.get("mode", "root"),
                "status": cfg.get("status", "COMPLETED DRY RUN"),
                "verdict": verdict,
                "graph_img": graph_img,
                "posts": cfg.get("posts")
            }
            for k in ["target_url", "rkeys", "post_urls"]:
                if k in cfg:
                    registry_story[k] = cfg[k]
            
            status = cfg.get("status", "")
            is_live = "LIVE" in status.upper() or len(cfg.get("rkeys", [])) > 0 or len(cfg.get("post_urls", [])) > 0
            
            if is_live:
                active_live_stories.append(registry_story)
            else:
                active_stories.append(registry_story)
                
        except Exception as e:
            print(f"Error reading configuration {newest_file}: {e}")

    # 4. Write final stories_registry.js files
    combined_registry = active_live_stories + active_stories
    registry_content = f"window.ALETHEIA_STORIES_REGISTRY = {json.dumps(combined_registry, indent=2, ensure_ascii=False)};\n"
    
    bot_registry_path = os.path.join(script_dir, "stories_registry.js")
    gen_registry_path = os.path.join(parent_dir, "_Generated_Content", "stories_registry.js")
    
    for r_path in [bot_registry_path, gen_registry_path]:
        try:
            with open(r_path, "w", encoding="utf-8") as out:
                out.write(registry_content)
            print(f"Compiled stories_registry.js at {r_path}")
        except Exception as e:
            print(f"Warning: Failed to compile stories_registry.js at {r_path}: {e}")

    # 5. Clean up orphan graph images not associated with any active story ID
    for g_dir in [os.path.join(script_dir, "graph_png"), os.path.join(parent_dir, "_Generated_Content", "graph_png")]:
        if os.path.exists(g_dir):
            for f in os.listdir(g_dir):
                if f.endswith("_graph.png"):
                    sid = f[:-len("_graph.png")]
                    if sid not in active_story_ids:
                        gp = os.path.join(g_dir, f)
                        try:
                            os.remove(gp)
                            print(f"[CLEANUP] Deleted orphan graph image: {gp}")
                        except Exception as e:
                            print(f"Warning: Could not delete orphan graph {gp}: {e}")
                            
    print("Rebuilding complete!")

if __name__ == '__main__':
    rebuild_registries()
