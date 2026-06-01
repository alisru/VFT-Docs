import json
import os
import sys

def mark_live_and_sync():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Define the updates
    live_stories = {
        "noah's_kitchen": {
            "rkey": "3mn4gsuxdmf2d",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mn4gsuxdmf2d"
        },
        "noahs_kitchen": {
            "rkey": "3mn4gsuxdmf2d",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mn4gsuxdmf2d"
        },
        "reclaimed_coal_mine": {
            "rkey": "3mn4gtfv2rr2x",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mn4gtfv2rr2x"
        },
        "reclaimed_mine": {
            "rkey": "3mn4gtfv2rr2x",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mn4gtfv2rr2x"
        },
        "volvo": {
            "rkey": "3mn4pnkrees2y",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mn4pnkrees2y"
        },
        "volvo_ev_target_retreat": {
            "rkey": "3mn4pnkrees2y",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mn4pnkrees2y"
        },
        "sodium_batteries": {
            "rkey": "3mn4gsdyqrq2z",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mn4gsdyqrq2z"
        },
        "sodium": {
            "rkey": "3mn4gsdyqrq2z",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mn4gsdyqrq2z"
        },
        "trump_freedom_250_cancel": {
            "rkey": "3mmzxflgtss2i",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mmzxflgtss2i"
        },
        "trump_freedom_250": {
            "rkey": "3mmzxflgtss2i",
            "url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3mmzxflgtss2i"
        }
    }
    
    updated_files = 0
    
    # Scan stories directories
    dirs = [
        os.path.join(parent_dir, "bluesky_bot", "stories"),
        os.path.join(parent_dir, "_Generated_Content", "stories")
    ]
    
    for s_dir in dirs:
        if not os.path.exists(s_dir):
            continue
        for filename in os.listdir(s_dir):
            if not filename.endswith(".json") or filename == "index.json":
                continue
                
            story_id = filename.replace("factcheck_", "").replace("story_", "").replace(".json", "")
            if story_id in live_stories:
                filepath = os.path.join(s_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    cfg = data[0] if isinstance(data, list) else data
                    
                    # Update fields!
                    cfg["status"] = "LIVE"
                    cfg["post_urls"] = [live_stories[story_id]["url"]]
                    cfg["rkeys"] = [live_stories[story_id]["rkey"]]
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump([cfg], f, indent=2, ensure_ascii=False)
                        
                    print(f"Updated live status for {filepath}")
                    updated_files += 1
                except Exception as e:
                    print(f"Error updating {filepath}: {e}")
                    
    print(f"Successfully marked {updated_files} files as live!")

if __name__ == '__main__':
    mark_live_and_sync()
