import os
import sys
import json
import shutil

# Ensure UTF-8 output encoding to prevent Unicode/Cp1252 printing errors on Windows
if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr and sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add script's directory to path to allow importing from aletheia_bot
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

try:
    from aletheia_bot import pack_posts
except ImportError as ie:
    print(f"ERROR: Failed to import pack_posts from aletheia_bot: {ie}")
    sys.exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch Pre-Flight Validator")
    parser.add_argument("--compact", action="store_true", help="Validate in compact thread mode")
    parser.add_argument("--compact-single", action="store_true", help="Validate in compact single-post mode")
    parser.add_argument("--five-word", action="store_true", help="Validate in 5-Word Mode")
    args = parser.parse_args()

    stories_dir = os.path.join(script_dir, "stories")
    graph_dir = os.path.join(script_dir, "graph_png")
    fail_dir = os.path.join(stories_dir, "fail")

    if not os.path.exists(stories_dir):
        print(f"ERROR: Stories folder not found at: {stories_dir}")
        sys.exit(1)

    print("--- STARTING BATCH PRE-FLIGHT VALIDATION ---")
    print("(Failing stories will be automatically quarantined in stories/fail/)")

    files_to_check = []
    for f in sorted(os.listdir(stories_dir)):
        if f.startswith("factcheck_") and f.endswith(".json"):
            files_to_check.append(os.path.join(stories_dir, f))

    if not files_to_check:
        print("No draft story JSON files found to validate.")
        sys.exit(0)

    print(f"Found {len(files_to_check)} draft files to validate.")
    failed = False
    skipped_count = 0

    for path in files_to_check:
        filename = os.path.basename(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = data[0] if isinstance(data, list) else data

            # Exclusivity Filter:
            config_five_word = cfg.get("five_word") is True
            exec_five_word = args.five_word is True
            if exec_five_word and not config_five_word:
                continue
            if config_five_word and not exec_five_word:
                continue

            # Skip if already posted live
            status = cfg.get("status", "")
            if status and (status.startswith("LIVE") or "LIVE POSTED" in status):
                print(f"  [SKIP] {filename} (Already posted live)")
                continue


            # Validate complete JSON Schema
            required_keys = ["id", "subject", "link", "claim_u", "claim_psi", "real_u", "real_psi", "mode", "status", "posts"]
            missing_keys = [k for k in required_keys if k not in cfg]
            if missing_keys:
                raise ValueError(f"Missing required JSON schema keys: {missing_keys}")

            # Validate types
            if not isinstance(cfg["id"], str) or not cfg["id"].strip():
                raise ValueError("Key 'id' must be a non-empty string.")
            if not isinstance(cfg["subject"], str) or not cfg["subject"].strip():
                raise ValueError("Key 'subject' must be a non-empty string.")
            if not isinstance(cfg["posts"], list):
                raise ValueError("Key 'posts' must be a list.")
            is_multi_aspect = cfg.get("multiAspect") is True
            is_spiritual = cfg.get("spiritual") is True or any(
                isinstance(p, str) and p.strip().startswith("Spirithekanon:") for p in cfg["posts"]
            )
            # Auto-repair Spirithekanon prefix if missing from the final post
            if is_spiritual and cfg["posts"]:
                last_p = str(cfg["posts"][-1]).strip()
                if not last_p.startswith("Spirithekanon:") and ('"' in last_p or 'PASS' in last_p or 'FAIL' in last_p or 'HIT' in last_p):
                    cfg["posts"][-1] = f"Spirithekanon:\n{last_p}"

            if not isinstance(cfg["posts"], list) or len(cfg["posts"]) == 0:
                raise ValueError("Key 'posts' must be a non-empty list.")
            if is_spiritual:
                spiritual_post = next((p for p in cfg["posts"] if isinstance(p, str) and p.strip().startswith("Spirithekanon:")), None)
                if not spiritual_post:
                    raise ValueError("is_spiritual is true but no post starts with 'Spirithekanon:'")
                text_to_check = spiritual_post.replace("Spirithekanon:", "").strip()
                import re
                match = re.search(r'"([^"]+)"', text_to_check)
                if not match:
                    # Attempt auto-repair of quotation marks around passage
                    lines = spiritual_post.split("\n")
                    if len(lines) >= 2:
                        quote_idx = 1 if lines[0].startswith("Spirithekanon:") else 0
                        quote_line = lines[quote_idx]
                        q_match = re.search(r'(\[?[0-9A-Za-z\s]+(?::|\s)\d+[^\]]*\]?\s*(?:PASS|FAIL|HIT|COND)?)', quote_line)
                        if q_match:
                            cite_part = q_match.group(1)
                            passage_part = quote_line[:q_match.start()].strip()
                            lines[quote_idx] = f'"{passage_part}" {cite_part}'.strip()
                            spiritual_post = "\n".join(lines)
                            cfg["posts"][-1] = spiritual_post
                            text_to_check = spiritual_post.replace("Spirithekanon:", "").strip()
                            match = re.search(r'"([^"]+)"', text_to_check)
                if not match:
                    raise ValueError(
                        f"Spirithekanon post must contain a quotation with canonical citation.\n"
                        f"Expected format: Spirithekanon:\n\"[Quote]\" [Source Text] [Verdict]\n"
                        f"Got: {spiritual_post}"
                    )
            for num_k in ["claim_u", "claim_psi", "real_u", "real_psi"]:
                if not isinstance(cfg[num_k], (int, float)):
                    raise ValueError(f"Key '{num_k}' must be a number (got type {type(cfg[num_k]).__name__}).")

            subject = cfg["subject"]
            posts = cfg["posts"]
            link = cfg["link"]
            if link and not link.startswith("http://") and not link.startswith("https://"):
                raise ValueError(f"Key 'link' must be an HTTP/HTTPS URL or empty string (got '{link}').")
            mode = cfg["mode"].lower()
            target_url = cfg.get("target_url", "")

            # 1. Pack posts and length validation
            # Auto-detect mode from story config, falling back to command-line flags
            config_five_word = cfg.get("five_word") is True
            config_compact = cfg.get("compact")
            has_config_compact = config_compact is True or config_compact == "single"

            is_five_word = config_five_word or args.five_word
            is_compact_single = (config_compact == "single" or args.compact_single) and not is_five_word
            is_compact_thread = (config_compact is True or args.compact) and not is_five_word
            is_compact = is_compact_single or is_compact_thread
            limit = 300

            if is_five_word:
                from aletheia_bot import pack_5word_posts
                final_posts = pack_5word_posts(posts, max_len=limit)
            elif is_compact_single:
                final_posts = posts[:1]
            elif is_compact_thread:
                if is_spiritual:
                    spiritual_post = None
                    for p in reversed(posts):
                        if isinstance(p, str) and p.strip().startswith("Spirithekanon:"):
                            spiritual_post = p
                            break
                    if spiritual_post:
                        final_posts = pack_posts(posts[:4] + [spiritual_post])
                    else:
                        final_posts = pack_posts(posts[:4])
                else:
                    final_posts = pack_posts(posts[:4])
            else:
                final_posts = pack_posts(posts)

            for idx, post in enumerate(final_posts, 1):
                if len(post) > limit:
                    raise ValueError(f"Packed post {idx} exceeds {limit} characters ({len(post)} chars):\n{post}")


            # 2. Graph Check (Generate on-the-fly if missing)
            story_id = cfg["id"]
            for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
                story_id = story_id.replace(char, '')
            graph_base_filename = f"{story_id}_graph.png"
            graph_filename = os.path.join(graph_dir, graph_base_filename)
            if not os.path.exists(graph_filename):
                print(f"  Trajectory graph not found for {story_id}. Generating on-the-fly...")
                try:
                    from generate_graph import draw_graph
                    draw_graph(
                        cfg.get("claim_u", 0.0), cfg.get("claim_psi", 0.0),
                        cfg.get("real_u",   0.0), cfg.get("real_psi",  0.0),
                        cfg.get("subject", "Story"),
                        graph_filename,
                        macro_event=cfg.get("macro_event", ""),
                        macro_claim_u=cfg.get("macro_claim_u"),
                        macro_claim_psi=cfg.get("macro_claim_psi"),
                        macro_real_u=cfg.get("macro_real_u"),
                        macro_real_psi=cfg.get("macro_real_psi")
                    )
                except Exception as ge:
                    raise RuntimeError(f"Failed to generate trajectory graph: {ge}")

            # 2b. Info Card Check (Generate on-the-fly if missing)
            if is_five_word:
                five_word_card_path = os.path.join(graph_dir, f"{story_id}_info_card_five_word.png")
                if not os.path.exists(five_word_card_path):
                    print(f"  Five-word info card not found for {story_id}. Generating on-the-fly...")
                    try:
                        from image_card_generator import generate_compact_info_card
                        base_path = os.path.join(graph_dir, f"{story_id}_info_card.png")
                        generate_compact_info_card(cfg, base_path)
                    except Exception as ice:
                        raise RuntimeError(f"Failed to generate five-word info card: {ice}")
            else:
                v_card_path = os.path.join(graph_dir, f"{story_id}_info_card_verdict.png")
                a_card_path = os.path.join(graph_dir, f"{story_id}_info_card_analysis.png")
                if not os.path.exists(v_card_path) or not os.path.exists(a_card_path):
                    print(f"  Split info cards not found for {story_id}. Generating on-the-fly...")
                    try:
                        from image_card_generator import generate_compact_info_card
                        base_path = os.path.join(graph_dir, f"{story_id}_info_card.png")
                        generate_compact_info_card(cfg, base_path)
                    except Exception as ice:
                        raise RuntimeError(f"Failed to generate split info cards: {ice}")



            # 3. Mode reply check
            if mode == "reply" and not target_url:
                raise ValueError("target_url is required when mode is 'reply'.")

            print(f"  [PASS] {filename} (validated successfully)")

        except Exception as e:
            print(f"  [FAIL] {filename}: {e}")
            try:
                os.makedirs(fail_dir, exist_ok=True)
                dest_path = os.path.join(fail_dir, filename)
                shutil.move(path, dest_path)
                print(f"         Moved failed draft to {dest_path}")
                skipped_count += 1
            except Exception as move_err:
                print(f"         ERROR moving failed draft to fail folder: {move_err}")
                failed = True

    if failed:
        print("\n--- VALIDATION RESULT: FAILED ---")
        sys.exit(1)
    else:
        if skipped_count > 0:
            print(f"\n--- VALIDATION RESULT: PASSED ({skipped_count} failed stories moved to fail/) ---")
        else:
            print("\n--- VALIDATION RESULT: ALL DRAFTS PASSED ---")
        sys.exit(0)

if __name__ == "__main__":
    main()
