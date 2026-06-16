import os
import sys
import json
from dotenv import load_dotenv
from atproto import Client

# Setup path
script_dir = os.path.dirname(os.path.abspath(__file__))
bot_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(bot_dir)

load_dotenv(os.path.join(bot_dir, ".env"))

def main():
    handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
    password = os.environ.get('BSKY_PASSWORD')
    if not password:
        print("ERROR: BSKY_PASSWORD not found in environment.")
        return

    # Load rkeys from live story file
    story_path = os.path.join(bot_dir, "stories", "live", "factcheck_bolton_imam_home.json")
    if not os.path.exists(story_path):
        print(f"ERROR: Story file not found at {story_path}")
        return

    with open(story_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cfg = data[0] if isinstance(data, list) else data

    rkeys = cfg.get("rkeys", [])
    if not rkeys:
        print("No rkeys found in story config. It may not be live posted.")
        return

    print(f"Connecting to Bluesky as {handle}...")
    client = Client()
    client.login(handle, password)
    print("Logged in successfully.")

    me_did = client.me.did
    print(f"My DID: {me_did}")

    # Delete posts in reverse order to clean up replies first
    print(f"Deleting {len(rkeys)} posts...")
    for rkey in reversed(rkeys):
        uri = f"at://{me_did}/app.bsky.feed.post/{rkey}"
        print(f"Deleting post: {uri}")
        try:
            client.delete_post(uri)
            print(f"  Successfully deleted {rkey}")
        except Exception as e:
            print(f"  Failed to delete {rkey}: {e}")

    # Clean up local config to change status and remove live URLs
    print("\nUpdating local configuration...")
    if "rkeys" in cfg:
        del cfg["rkeys"]
    if "post_urls" in cfg:
        del cfg["post_urls"]
    cfg["status"] = "COMPLETED DRY RUN"

    # Move file from stories/live/ to stories/
    new_story_path = os.path.join(bot_dir, "stories", "factcheck_bolton_imam_home.json")
    with open(new_story_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    if os.path.exists(story_path):
        os.remove(story_path)
    print(f"Moved story config to {new_story_path} and set status to COMPLETED DRY RUN.")

    # Rebuild registries to update stories_registry.js
    print("\nRebuilding registries...")
    from rebuild_registries import rebuild_registries
    rebuild_registries()
    print("Registries successfully rebuilt.")

if __name__ == "__main__":
    main()
