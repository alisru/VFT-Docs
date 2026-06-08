import os
import sys
import json
import time
import random
import shutil
import argparse

# Add bluesky_bot to path if run from root
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from aletheia_bot import post_thread, split_text
from atproto import Client

def validate_story_file(path):
    filename = os.path.basename(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cfg = data[0] if isinstance(data, list) else data

        # Validate JSON Schema
        required_keys = ["id", "subject", "link", "claim_u", "claim_psi", "real_u", "real_psi", "mode", "status", "posts"]
        missing_keys = [k for k in required_keys if k not in cfg]
        if missing_keys:
            raise ValueError(f"Missing required JSON schema keys: {missing_keys}")

        if len(cfg["posts"]) != 13:
            raise ValueError(f"Key 'posts' must contain exactly 13 elements (got {len(cfg['posts'])}).")

        # Split posts and length validation
        final_posts = []
        for post in cfg["posts"]:
            final_posts.extend(split_text(post))

        for idx, post in enumerate(final_posts, 1):
            if len(post) > 250:
                raise ValueError(f"Post {idx} exceeds 250 characters ({len(post)} chars):\n{post}")

        # Graph Check
        story_id = cfg["id"]
        for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
            story_id = story_id.replace(char, '')
        graph_filename = os.path.join(script_dir, "graph_png", f"{story_id}_graph.png")
        if not os.path.exists(graph_filename):
            raise FileNotFoundError(f"Required trajectory graph image not found: {graph_filename}.")

        return True, ""
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description="Aletheia Bot Batch Posting Scheduler")
    parser.add_argument("--files", nargs="+", help="List of factcheck JSON filenames to post (e.g., factcheck_volvo.json)")
    parser.add_argument("--folder", type=str, default=os.path.join(script_dir, "stories"), help="Path to folder containing JSON files to post (default: bluesky_bot/stories)")
    parser.add_argument("--min-delay", type=int, default=5, help="Minimum delay between different threads in seconds (default: 10)")
    parser.add_argument("--max-delay", type=int, default=10, help="Maximum delay between different threads in seconds (default: 30)")
    parser.add_argument("--live", action="store_true", help="Set to actually post live (dry-run by default)")
    parser.add_argument("--move-to", type=str, default=os.path.join(script_dir, "stories", "live"), help="Folder to move successfully posted files to (default: bluesky_bot/stories/live)")
    parser.add_argument("--watch", action="store_true", help="Run in continuous daemon mode, watching the folder and posting any new files (default: False)")
    args = parser.parse_args()

    from dotenv import load_dotenv
    # Check root first, then script dir (bluesky_bot/.env)
    if not load_dotenv():
        load_dotenv(os.path.join(script_dir, ".env"))
    
    username = os.getenv("BSKY_HANDLE") or os.getenv("BLUESKY_USERNAME") or "judgement-bot.bsky.social"
    password = os.getenv("BSKY_PASSWORD") or os.getenv("BLUESKY_PASSWORD")
    
    if args.live:
        if not password:
            print("ERROR: BSKY_PASSWORD environment variable is required for live posting.")
            sys.exit(1)
        print("Initializing Bluesky Client...")
        client = Client()
        client.login(username, password)
        print(f"Logged in successfully as {username}.")
    else:
        client = None
        print("--- DRY-RUN MODE ACTIVE ---")
        print("Set --live to actually post to Bluesky.")

    if args.watch:
        if not args.folder:
            print("ERROR: --folder must be specified to use --watch mode.")
            sys.exit(1)
        
        print("--------------------------------------------------")
        print(f"ALETHEIA BOT: RUNNING IN CONTINUOUS WATCH MODE")
        print(f"Watching folder: {args.folder}")
        print("--------------------------------------------------")
        
        seen_files = set()  # avoid infinite retries on permanently broken files
        
        try:
            while True:
                files_to_post = []
                for f in sorted(os.listdir(args.folder)):
                    if f.startswith("factcheck_") and f.endswith(".json"):
                        full_path = os.path.join(args.folder, f)
                        if full_path not in seen_files:
                            files_to_post.append(full_path)
                
                if files_to_post:
                    print(f"\nFound {len(files_to_post)} new story file(s) to process.")
                    for idx, path in enumerate(files_to_post, 1):
                        filename = os.path.basename(path)
                        print(f"\n[Watch] Validating and posting: {filename}")
                        
                        # Pre-flight validation
                        is_valid, err_msg = validate_story_file(path)
                        if not is_valid:
                            print(f"  [VALIDATION FAIL] {filename}: {err_msg}")
                            # Move to fail folder
                            fail_dir = os.path.join(args.folder, "fail")
                            os.makedirs(fail_dir, exist_ok=True)
                            dest_path = os.path.join(fail_dir, filename)
                            try:
                                shutil.move(path, dest_path)
                                print(f"  Moved failed file to {dest_path}")
                            except Exception as me:
                                print(f"  Error moving failed file: {me}")
                            seen_files.add(path)
                            continue
                        
                        # Read configuration
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        cfg = data[0] if isinstance(data, list) else data
                        
                        # Post thread
                        success = False
                        try:
                            # Enforce 2 second delay between individual posts within the thread
                            original_sleep = time.sleep
                            try:
                                def custom_sleep(seconds):
                                    original_sleep(2.0 if seconds == 1 else seconds)
                                time.sleep = custom_sleep
                                post_thread(client, cfg, live=args.live)
                                success = True
                            finally:
                                time.sleep = original_sleep
                        except Exception as e:
                            print(f"  [POSTING FAIL] Failed to post {filename}: {e}")
                            seen_files.add(path)
                            continue
                            
                        # Move successfully posted files
                        if success and args.live and args.move_to:
                            try:
                                os.makedirs(args.move_to, exist_ok=True)
                                dest_path = os.path.join(args.move_to, filename)
                                if os.path.exists(dest_path):
                                    os.remove(path)
                                    print(f"  Removed source file because it exists in live: {path}")
                                else:
                                    shutil.move(path, dest_path)
                                    print(f"  Moved successfully posted file to {dest_path}")
                            except Exception as e:
                                print(f"  Warning: Failed to move file to live: {e}")
                                
                        # Spacing delay between threads
                        if success and idx < len(files_to_post):
                            wait_seconds = random.randint(args.min_delay, args.max_delay)
                            print(f"  Waiting {wait_seconds} seconds before posting the next thread...")
                            time.sleep(wait_seconds)
                
                # Sleep before next scan
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nWatcher stopped by user. Exiting.")
            sys.exit(0)
    else:
        # 1. Resolve files (standard one-shot mode)
        files_to_post = []
        if args.files:
            for f in args.files:
                # Resolve path
                path = f
                if not os.path.exists(path):
                    path = os.path.join("bluesky_bot", "stories", f)
                if not os.path.exists(path):
                    path = os.path.join("scratch", f)
                
                if os.path.exists(path):
                    files_to_post.append(path)
                else:
                    print(f"Warning: File not found and skipped: {f}")
        elif args.folder:
            if not os.path.exists(args.folder):
                print(f"ERROR: Folder not found: {args.folder}")
                sys.exit(1)
            for f in sorted(os.listdir(args.folder)):
                if f.startswith("factcheck_") and f.endswith(".json"):
                    files_to_post.append(os.path.join(args.folder, f))
            print(f"Found {len(files_to_post)} JSON files in folder '{args.folder}'.")
        else:
            print("ERROR: Either --files or --folder must be specified.")
            sys.exit(1)

        total_files = len(files_to_post)
        if total_files == 0:
            print("No files found to post.")
            sys.exit(0)

        print(f"\nScheduling {total_files} threads to post.")
        print(f"Delay between threads: Randomly spaced between {args.min_delay} and {args.max_delay} seconds.")
        print("Within each thread, we will wait 2.0 seconds between posts to ensure Bluesky indexers align the thread perfectly.")
        
        for idx, path in enumerate(files_to_post, 1):
            filename = os.path.basename(path)
            print(f"\n==================================================")
            print(f"POSTING THREAD {idx}/{total_files}: {filename}")
            print(f"==================================================")
            
            success = False
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cfg = data[0] if isinstance(data, list) else data
                
                # Skip if already posted live
                status = cfg.get("status", "")
                if status and (status.startswith("LIVE") or "LIVE POSTED" in status):
                    print(f"Skipping {filename}: Already posted live (Status: {status})")
                    continue
                
                # Enforce 2 second delay between individual posts within the thread
                original_sleep = time.sleep
                try:
                    def custom_sleep(seconds):
                        original_sleep(2.0 if seconds == 1 else seconds)
                    time.sleep = custom_sleep
                    
                    post_thread(client, cfg, live=args.live)
                    success = True
                finally:
                    # Restore sleep
                    time.sleep = original_sleep
                
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
                continue
                
            # Move successfully posted files if live and destination folder is provided
            if success and args.live and args.move_to:
                try:
                    os.makedirs(args.move_to, exist_ok=True)
                    dest_path = os.path.join(args.move_to, filename)
                    if os.path.exists(dest_path):
                        os.remove(path)
                        print(f"Removed source file because it was already synchronized in live directory: {path}")
                    else:
                        shutil.move(path, dest_path)
                        print(f"Moved successfully posted file to {dest_path}")
                except Exception as e:
                    print(f"Warning: Failed to move file to {args.move_to}: {e}")
                
            # Spacing delay between threads (only if there are more files remaining)
            if idx < total_files:
                wait_seconds = random.randint(args.min_delay, args.max_delay)
                print(f"\nThread {idx} finished. Waiting {wait_seconds} seconds before posting the next thread...")
                try:
                    for remaining in range(wait_seconds, 0, -1):
                        sys.stdout.write(f"\rNext thread in {remaining} seconds...   ")
                        sys.stdout.flush()
                        time.sleep(1)
                    print("\nTimer elapsed. Starting next thread!")
                except KeyboardInterrupt:
                    print("\nScheduler paused by user. Exiting.")
                    sys.exit(0)

        print("\nAll scheduled batch threads completed successfully!")

if __name__ == "__main__":
    main()
