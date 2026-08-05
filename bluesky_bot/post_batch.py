import os
import sys
import json
import time
import random
import shutil
import argparse
import datetime

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

# Add bluesky_bot to path if run from root
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from aletheia_bot import post_thread, pack_posts
from atproto import Client

def is_five_word_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cfg = data[0] if isinstance(data, list) else data
        return cfg.get("five_word") is True
    except Exception:
        return False



def safe_getmtime(p):
    try:
        return os.path.getmtime(p)
    except OSError:
        return 0.0

def wait_for_rate_limit(exc: Exception) -> bool:
    """If exc looks like a Bluesky 429, sleep until the reset time and return True.
    Returns False if it isn't a rate-limit error (caller should re-raise).

    Bluesky sends:
        HTTP 429  +  ratelimit-reset: <unix timestamp>
    The atproto client wraps this as a RequestException whose .response carries
    status_code and headers. post_thread re-wraps that in a RuntimeError, so we
    walk the __cause__/__context__ chain to find the response.
    """
    response = None
    seen = set()
    cursor = exc
    while cursor is not None and id(cursor) not in seen:
        seen.add(id(cursor))
        response = getattr(cursor, "response", None)
        if response is not None:
            break
        cursor = cursor.__cause__ or cursor.__context__
    if response is None:
        # Some wrappers stringify the error — check message text as fallback.
        # Match deliberately narrow phrases: a bare "rate" would catch
        # "generate"/"moderate" and stall the bot an hour on unrelated errors.
        msg = str(exc).lower()
        if not any(tok in msg for tok in ("429", "rate limit", "ratelimit", "too many requests")):
            return False
        # No header info available; sleep until the top of the next hour.
        now = datetime.datetime.now()
        next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=5, microsecond=0)
        wait = max(0, (next_hour - now).total_seconds())
        print(f"\n[RATE LIMIT] No reset header found. Sleeping until next hour ({next_hour.strftime('%H:%M:%S')}) — {int(wait)}s.")
        _sleep_with_countdown(int(wait))
        return True

    status = getattr(response, "status_code", 0)
    if status != 429:
        return False

    headers = getattr(response, "headers", {}) or {}
    reset_ts = headers.get("ratelimit-reset") or headers.get("x-ratelimit-reset")
    remaining = headers.get("ratelimit-remaining", "?")

    if reset_ts:
        try:
            reset_dt = datetime.datetime.fromtimestamp(int(reset_ts))
            wait = max(5, (reset_dt - datetime.datetime.now()).total_seconds())
            print(f"\n[RATE LIMIT] remaining={remaining}  reset={reset_dt.strftime('%H:%M:%S')}  sleeping {int(wait)}s...")
            _sleep_with_countdown(int(wait))
            return True
        except (ValueError, OSError):
            pass

    # Header present but unparseable — sleep 15 min as safe default.
    print(f"\n[RATE LIMIT] 429 received but could not parse reset time. Sleeping 15 minutes.")
    _sleep_with_countdown(900)
    return True


def _safe_to_retry(exc: Exception) -> bool:
    """post_thread has no resume: retrying after a mid-thread failure would
    re-post the parts that already landed. Only the root post (part 1) failing
    means nothing went out, so only that case is safe to retry."""
    return "Failed to post part" not in str(exc)


def _sleep_with_countdown(seconds: int):
    """Sleep with a live countdown so the terminal isn't silent."""
    try:
        for remaining in range(seconds, 0, -10):
            sys.stdout.write(f"\r[RATE LIMIT] Resuming in {remaining}s ...   ")
            sys.stdout.flush()
            time.sleep(min(10, remaining))
        print("\r[RATE LIMIT] Rate limit window passed. Resuming.              ")
    except KeyboardInterrupt:
        print("\n[RATE LIMIT] Sleep interrupted by user.")
        raise

def validate_story_file(path, compact=False):
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

        # Pack posts and length validation
        is_compact_single = compact == "single" or cfg.get("compact") == "single"
        is_compact_thread = compact is True or cfg.get("compact") is True
        is_compact = is_compact_single or is_compact_thread

        if is_compact_single:
            final_posts = cfg["posts"][:1]
        elif is_compact_thread:
            final_posts = cfg["posts"][:4]
        else:
            final_posts = pack_posts(cfg["posts"])

        for idx, post in enumerate(final_posts, 1):
            if len(post) > 299:
                raise ValueError(f"Post {idx} exceeds 299 characters ({len(post)} chars):\n{post}")

        # Graph Check
        story_id = cfg["id"]
        for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
            story_id = story_id.replace(char, '')
        graph_filename = os.path.join(script_dir, "graph_png", f"{story_id}_graph.png")
        if not os.path.exists(graph_filename):
            raise FileNotFoundError(f"Required trajectory graph image not found: {graph_filename}.")

        # Info Card Check (Generate on-the-fly if missing)
        if is_compact:
            v_card_path = os.path.join(script_dir, "graph_png", f"{story_id}_info_card_verdict.png")
            a_card_path = os.path.join(script_dir, "graph_png", f"{story_id}_info_card_analysis.png")
            if not os.path.exists(v_card_path) or not os.path.exists(a_card_path):
                print(f"  Info cards not found for {story_id}. Generating on-the-fly...")
                try:
                    from image_card_generator import generate_compact_info_card
                    base_path = os.path.join(script_dir, "graph_png", f"{story_id}_info_card.png")
                    generate_compact_info_card(cfg, base_path)
                except Exception as ice:
                    raise RuntimeError(f"Failed to generate compact info cards: {ice}")

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
    parser.add_argument("--compact", action="store_true", help="Post in compact thread mode (posts 1-4 as text, posts 5+ as summary card image)")
    parser.add_argument("--compact-single", action="store_true", help="Post in compact single-post mode (only post 1 with graph and card images)")
    parser.add_argument("--five-word", action="store_true", help="Post in 5-Word Mode")
    parser.add_argument("--move-to", type=str, default=os.path.join(script_dir, "stories", "live"), help="Folder to move successfully posted files to (default: bluesky_bot/stories/live)")
    parser.add_argument("--watch", action="store_true", help="Run in continuous daemon mode, watching the folder and posting any new files (default: False)")
    args = parser.parse_args()


    compact_val = False
    if args.compact_single:
        compact_val = "single"
    elif args.compact:
        compact_val = True

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
                try:
                    candidates = [
                        os.path.join(args.folder, f)
                        for f in os.listdir(args.folder)
                        if (f.startswith("factcheck_") or f.startswith("roundup_")) and f.endswith(".json")
                    ]
                    candidates = [
                        c for c in candidates
                        if is_five_word_file(c) == bool(args.five_word)
                    ]
                    candidates.sort(key=safe_getmtime)

                    for full_path in candidates:
                        if full_path not in seen_files:
                            files_to_post.append(full_path)
                except Exception as e:
                    print(f"Warning: Failed to list and sort files in watcher loop: {e}")
                
                if files_to_post:
                    print(f"\nFound {len(files_to_post)} new story file(s) to process.")
                    any_posted = False
                    for idx, path in enumerate(files_to_post, 1):
                        filename = os.path.basename(path)
                        print(f"\n[Watch] Validating and posting: {filename}")
                        
                        # Pre-flight validation
                        is_valid, err_msg = validate_story_file(path, compact=compact_val)
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
                        
                        # Post thread (retry once after rate-limit)
                        success = False
                        already_replied = False
                        for _attempt in range(2):
                            try:
                                original_sleep = time.sleep
                                try:
                                    def custom_sleep(seconds):
                                        original_sleep(2.0 if seconds == 1 else seconds)
                                    time.sleep = custom_sleep
                                    post_thread(client, cfg, live=args.live, compact=compact_val, five_word=args.five_word)

                                    success = True
                                finally:
                                    time.sleep = original_sleep
                                break
                            except Exception as e:
                                if "ALREADY_REPLIED" in str(e):
                                    print(f"  [SKIP/ALREADY REPLIED] {filename} is already live on Bluesky. Moving to live folder.")
                                    success = True
                                    already_replied = True
                                    break
                                if _attempt == 0 and wait_for_rate_limit(e):
                                    if _safe_to_retry(e):
                                        continue  # nothing posted yet — retry after sleep
                                    print(f"  [POSTING FAIL] Rate limit hit MID-THREAD on {filename}; not retrying (would duplicate posted parts). Review manually.")
                                    seen_files.add(path)
                                    break
                                print(f"  [POSTING FAIL] Failed to post {filename}: {e}")
                                seen_files.add(path)
                                break
                            
                        # Move successfully posted files
                        if success and args.live and args.move_to:
                            try:
                                os.makedirs(args.move_to, exist_ok=True)
                                dest_path = os.path.join(args.move_to, filename)
                                if os.path.exists(path):
                                    if os.path.exists(dest_path):
                                        os.remove(path)
                                        print(f"  Removed source file because it exists in live: {path}")
                                    else:
                                        shutil.move(path, dest_path)
                                        print(f"  Moved successfully posted file to {dest_path}")
                                else:
                                    print(f"  Source file was already cleaned up/moved by posting process.")
                                
                                # If this is a roundup, also move the companion folder (roundup_slug/) to live/
                                if filename.startswith("roundup_"):
                                    slug = filename[len("roundup_"):-len(".json")]
                                    companion_dir = os.path.join(os.path.dirname(path), f"roundup_{slug}")
                                    if os.path.isdir(companion_dir):
                                        dest_dir = os.path.join(args.move_to, f"roundup_{slug}")
                                        try:
                                            if os.path.exists(dest_dir):
                                                shutil.rmtree(dest_dir)
                                            shutil.move(companion_dir, dest_dir)
                                            print(f"  Moved companion folder to {dest_dir}")
                                        except Exception as ce:
                                            print(f"  Warning: Failed to move companion folder: {ce}")
                            except Exception as e:
                                print(f"  Warning: Failed to move file to live: {e}")
                                
                        if success:
                            any_posted = True

                        # Spacing delay between threads
                        if success and not already_replied and idx < len(files_to_post):
                            wait_seconds = random.randint(args.min_delay, args.max_delay)
                            print(f"  Waiting {wait_seconds} seconds before posting the next thread...")
                            time.sleep(wait_seconds)

                    if any_posted:
                        try:
                            print("\nRebuilding registries to update live and drafts counts...")
                            from rebuild_registries import rebuild_registries
                            rebuild_registries()
                        except Exception as e:
                            print(f"Warning: Failed to rebuild registries: {e}")
                
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
            files_to_post = [
                f for f in files_to_post
                if is_five_word_file(f) == bool(args.five_word)
            ]

        elif args.folder:
            if not os.path.exists(args.folder):
                print(f"ERROR: Folder not found: {args.folder}")
                sys.exit(1)
            try:
                candidates = [
                    os.path.join(args.folder, f)
                    for f in os.listdir(args.folder)
                    if (f.startswith("factcheck_") or f.startswith("roundup_")) and f.endswith(".json")
                ]
                candidates = [
                    c for c in candidates
                    if is_five_word_file(c) == bool(args.five_word)
                ]
                candidates.sort(key=safe_getmtime)
                files_to_post.extend(candidates)

            except Exception as e:
                print(f"ERROR: Failed to list and sort files in folder: {e}")
                sys.exit(1)
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
        
        any_posted = False
        for idx, path in enumerate(files_to_post, 1):
            filename = os.path.basename(path)
            print(f"\n==================================================")
            print(f"POSTING THREAD {idx}/{total_files}: {filename}")
            print(f"==================================================")
            
            success = False
            already_replied = False
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cfg = data[0] if isinstance(data, list) else data

                # Skip if already posted live
                status = cfg.get("status", "")
                if status and (status.startswith("LIVE") or "LIVE POSTED" in status):
                    print(f"Skipping {filename}: Already posted live (Status: {status})")
                    continue

                # Post thread (retry once after rate-limit)
                for _attempt in range(2):
                    try:
                        original_sleep = time.sleep
                        try:
                            def custom_sleep(seconds):
                                original_sleep(2.0 if seconds == 1 else seconds)
                            time.sleep = custom_sleep
                            post_thread(client, cfg, live=args.live, compact=compact_val, five_word=args.five_word)

                            success = True
                        finally:
                            time.sleep = original_sleep
                        break
                    except Exception as e:
                        if "ALREADY_REPLIED" in str(e):
                            print(f"  [SKIP/ALREADY REPLIED] {filename} is already live on Bluesky. Moving to live folder.")
                            success = True
                            already_replied = True
                            break
                        if _attempt == 0 and wait_for_rate_limit(e):
                            if _safe_to_retry(e):
                                continue  # nothing posted yet — retry after sleep
                            print(f"Rate limit hit MID-THREAD on {filename}; not retrying (would duplicate posted parts). Review manually.")
                        raise  # let outer handler log and move on

            except Exception as e:
                if not success:
                    print(f"Failed to process {filename}: {e}")
                    continue
                
            # Move successfully posted files if live and destination folder is provided
            if success and args.live and args.move_to:
                try:
                    os.makedirs(args.move_to, exist_ok=True)
                    dest_path = os.path.join(args.move_to, filename)
                    if os.path.exists(path):
                        if os.path.exists(dest_path):
                            os.remove(path)
                            print(f"Removed source file because it was already synchronized in live directory: {path}")
                        else:
                            shutil.move(path, dest_path)
                            print(f"Moved successfully posted file to {dest_path}")
                    else:
                        print(f"Source file was already cleaned up/moved by posting process.")
                    # If this is a roundup, also move the companion folder (roundup_slug/) to live/
                    if filename.startswith("roundup_"):
                        slug = filename[len("roundup_"):-len(".json")]
                        companion_dir = os.path.join(os.path.dirname(path), f"roundup_{slug}")
                        if os.path.isdir(companion_dir):
                            dest_dir = os.path.join(args.move_to, f"roundup_{slug}")
                            try:
                                if os.path.exists(dest_dir):
                                    shutil.rmtree(dest_dir)
                                shutil.move(companion_dir, dest_dir)
                                print(f"Moved companion folder to {dest_dir}")
                            except Exception as ce:
                                print(f"Warning: Failed to move companion folder: {ce}")
                except Exception as e:
                    print(f"Warning: Failed to move file to {args.move_to}: {e}")
                
            if success:
                any_posted = True

            # Spacing delay between threads (only if there are more files remaining)
            if success and not already_replied and idx < total_files:
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

        if any_posted:
            try:
                print("\nRebuilding registries to update live and drafts counts...")
                from rebuild_registries import rebuild_registries
                rebuild_registries()
            except Exception as e:
                print(f"Warning: Failed to rebuild registries: {e}")

        print("\nAll scheduled batch threads completed successfully!")

if __name__ == "__main__":
    main()
