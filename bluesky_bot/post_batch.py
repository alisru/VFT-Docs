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

from aletheia_bot import post_thread
from atproto import Client

def main():
    parser = argparse.ArgumentParser(description="Aletheia Bot Batch Posting Scheduler")
    parser.add_argument("--files", nargs="+", help="List of factcheck JSON filenames to post (e.g., factcheck_volvo.json)")
    parser.add_argument("--folder", type=str, help="Path to folder containing JSON files to post (e.g. bluesky_bot/stories/ready)")
    parser.add_argument("--min-delay", type=int, default=10, help="Minimum delay between different threads in seconds (default: 10)")
    parser.add_argument("--max-delay", type=int, default=30, help="Maximum delay between different threads in seconds (default: 30)")
    parser.add_argument("--live", action="store_true", help="Set to actually post live (dry-run by default)")
    parser.add_argument("--move-to", type=str, help="Folder to move successfully posted files to (e.g. bluesky_bot/stories/live)")
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

    # 1. Resolve files
    files_to_post = []
    if args.folder:
        if not os.path.exists(args.folder):
            print(f"ERROR: Folder not found: {args.folder}")
            sys.exit(1)
        for f in sorted(os.listdir(args.folder)):
            if f.endswith(".json") and f != "index.json":
                files_to_post.append(os.path.join(args.folder, f))
        print(f"Found {len(files_to_post)} JSON files in folder '{args.folder}'.")
    elif args.files:
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
            def custom_sleep(seconds):
                original_sleep(2.0 if seconds == 1 else seconds)
            time.sleep = custom_sleep
            
            post_thread(client, cfg, live=args.live)
            
            # Restore sleep
            time.sleep = original_sleep
            success = True
            
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            continue
            
        # Move successfully posted files if live and destination folder is provided
        if success and args.live and args.move_to:
            try:
                os.makedirs(args.move_to, exist_ok=True)
                dest_path = os.path.join(args.move_to, filename)
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
