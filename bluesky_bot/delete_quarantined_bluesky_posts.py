import os
import sys
import json
import time

sys.stdout.reconfigure(line_buffering=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from dotenv import load_dotenv
load_dotenv(os.path.join(script_dir, ".env"))

from atproto import Client

handle = os.environ.get("BSKY_HANDLE", "judgement-bot.bsky.social")
password = os.environ.get("BSKY_PASSWORD")

if not password:
    print("ERROR: BSKY_PASSWORD not found in .env")
    sys.exit(1)

print(f"Connecting to Bluesky as {handle}...")
client = Client()
try:
    client.login(handle, password)
    my_did = client.me.did
    print(f"Logged in successfully! DID: {my_did}")
except Exception as e:
    print(f"Failed to login to Bluesky: {e}")
    sys.exit(1)

quarantine_dir = os.path.join(script_dir, "stories", "quarantine")
manifest_path = os.path.join(quarantine_dir, "all_rkeys_to_delete.json")

if not os.path.exists(manifest_path):
    print(f"ERROR: Manifest not found at {manifest_path}")
    sys.exit(1)

with open(manifest_path, "r", encoding="utf-8") as f:
    stories = json.load(f)

total_stories = len(stories)
total_rkeys = sum(len(s["rkeys"]) for s in stories)
print(f"Ready to delete {total_rkeys} posts across {total_stories} quarantined stories.\n")

deleted_count = 0
not_found_count = 0
failed_count = 0

start_time = time.time()

for s_idx, story in enumerate(stories, 1):
    subject = story.get("subject", story.get("file", ""))
    rkeys = story.get("rkeys", [])
    print(f"[{s_idx}/{total_stories}] Deleting: {subject[:45]} ({len(rkeys)} posts)")
    
    # Delete in reverse order (replies first, then root)
    for rkey in reversed(rkeys):
        uri = f"at://{my_did}/app.bsky.feed.post/{rkey}"
        try:
            client.delete_post(uri)
            deleted_count += 1
            print(f"  Deleted: {rkey}")
            time.sleep(0.08) # Rate limit protection
        except Exception as e:
            err_str = str(e)
            if "Could not find record" in err_str or "NotFound" in err_str or "RecordNotFound" in err_str:
                not_found_count += 1
                print(f"  Already gone: {rkey}")
            else:
                failed_count += 1
                print(f"  Error on {rkey}: {err_str[:60]}")

elapsed = time.time() - start_time
print(f"\n==========================================")
print(f"BLUESKY DELETION COMPLETE in {elapsed:.1f}s:")
print(f"Successfully deleted: {deleted_count}")
print(f"Already gone/not found: {not_found_count}")
print(f"Failed: {failed_count}")
print(f"Total processed: {deleted_count + not_found_count + failed_count}/{total_rkeys}")
print(f"==========================================\n")

# Now move each story to its target destination (drafts or quarantine)
print("Moving stories to target folders (drafts or quarantine)...")
import shutil
drafts_dir = os.path.join(script_dir, "stories", "drafts")
quarantine_dir = os.path.join(script_dir, "stories", "quarantine")
os.makedirs(drafts_dir, exist_ok=True)
os.makedirs(quarantine_dir, exist_ok=True)

from generate_graph import enforce_deterministic_trajectory
from rebuild_registries_son import get_zone_label

moved_count = 0
for story in stories:
    raw_path = story.get("file", "")
    target_dest = story.get("destination", "drafts")
    base = os.path.basename(raw_path)
    
    candidates = [
        raw_path,
        os.path.join(script_dir, "stories", "live", base),
        os.path.join(script_dir, "stories", "quarantine", base),
        os.path.join(script_dir, "stories", "drafts", base),
        os.path.join(os.path.dirname(script_dir), raw_path)
    ]
    f_path = None
    for c in candidates:
        if c and os.path.exists(c):
            f_path = c
            break

    if not f_path:
        print(f"  Warning: file not found on disk for story {story.get('id')}: {raw_path}")
        continue

    try:
        with open(f_path, "r", encoding="utf-8") as fp_in:
            data = json.load(fp_in)
        s = data[0] if isinstance(data, list) else data
        
        # Reset Bluesky live state
        s["rkeys"] = []
        s["post_urls"] = []

        if target_dest == "quarantine":
            s["status"] = f"QUARANTINED ({story.get('reason', 'Policy violation')})"
            dest_folder = quarantine_dir
        else:
            s["status"] = "DRAFT"
            s = enforce_deterministic_trajectory(s)
            dest_folder = drafts_dir

        data = [s] if isinstance(data, list) else s

        dest_path = os.path.join(dest_folder, base)
        with open(dest_path, "w", encoding="utf-8") as fp_out:
            json.dump(data, fp_out, indent=2)

        if os.path.abspath(f_path) != os.path.abspath(dest_path):
            os.remove(f_path)
            
        moved_count += 1
        print(f"  Moved to {target_dest}: {base}")
    except Exception as me:
        print(f"  Error moving {f_path}: {me}")

print(f"\nSuccessfully processed and moved {moved_count}/{len(stories)} stories.")
