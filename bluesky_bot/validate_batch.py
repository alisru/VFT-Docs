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
            if len(cfg["posts"]) != 13:
                raise ValueError(f"Key 'posts' must contain exactly 13 elements (got {len(cfg['posts'])}).")
            for num_k in ["claim_u", "claim_psi", "real_u", "real_psi"]:
                if not isinstance(cfg[num_k], (int, float)):
                    raise ValueError(f"Key '{num_k}' must be a number (got type {type(cfg[num_k]).__name__}).")

            subject = cfg["subject"]
            posts = cfg["posts"]
            link = cfg["link"]
            mode = cfg["mode"].lower()
            target_url = cfg.get("target_url", "")

            # 1. Pack posts and length validation
            final_posts = pack_posts(posts)

            for idx, post in enumerate(final_posts, 1):
                if len(post) > 299:
                    raise ValueError(f"Post {idx} exceeds 299 characters ({len(post)} chars):\n{post}")

            # 2. Graph Check
            story_id = cfg["id"]
            for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
                story_id = story_id.replace(char, '')
            graph_base_filename = f"{story_id}_graph.png"
            graph_filename = os.path.join(graph_dir, graph_base_filename)
            if not os.path.exists(graph_filename):
                raise FileNotFoundError(f"Required trajectory graph image not found: {graph_filename}. Graphs must be pre-generated.")

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
