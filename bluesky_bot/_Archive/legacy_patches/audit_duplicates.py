import os
import sys
import json
import argparse
from dotenv import load_dotenv
from atproto import Client

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

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

def audit_duplicates():
    parser = argparse.ArgumentParser(description="Audit and optionally delete duplicate Bluesky threads.")
    parser.add_argument("--limit", type=int, default=200, help="Number of root story replies to scan (default: 200)")
    parser.add_argument("--skip", type=int, default=0, help="Number of root story replies to skip (default: 0)")
    parser.add_argument("--delete", action="store_true", help="Actually delete the duplicate threads from Bluesky")
    args = parser.parse_args()

    handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
    password = os.environ.get('BSKY_PASSWORD')
    if not password:
        print("ERROR: BSKY_PASSWORD not found in env.")
        sys.exit(1)

    print(f"Logging in as {handle}...")
    client = Client()
    try:
        client.login(handle, password)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    print(f"Fetching up to {args.limit + args.skip} root story replies from author feed...")
    root_replies = []
    all_posts = []  # Store all posts to resolve child replies in duplicate threads
    cursor = None
    pages_fetched = 0
    
    while len(root_replies) < (args.limit + args.skip):
        params = {
            'actor': client.me.did,
            'limit': 100
        }
        if cursor:
            params['cursor'] = cursor
            
        try:
            response = client.app.bsky.feed.get_author_feed(params=params)
        except Exception as e:
            print(f"Failed to fetch author feed: {e}")
            break
            
        feed_items = response.feed
        if not feed_items:
            break
            
        for item in feed_items:
            post = item.post
            record = getattr(post, 'record', None)
            if not record:
                continue
                
            text = getattr(record, 'text', '').strip()
            created_at = getattr(record, 'created_at', '')
            
            # Check if the post is a reply
            reply_ref = getattr(record, 'reply', None)
            is_reply = reply_ref is not None
            
            parent_uri = ""
            root_uri = ""
            if is_reply:
                if hasattr(reply_ref, 'parent') and reply_ref.parent:
                    parent_uri = getattr(reply_ref.parent, 'uri', '')
                if hasattr(reply_ref, 'root') and reply_ref.root:
                    root_uri = getattr(reply_ref.root, 'uri', '')

            # Resolve public URL for the post
            rkey = post.uri.split('/')[-1]
            post_url = f"https://bsky.app/profile/{post.author.handle}/post/{rkey}"

            post_info = {
                "uri": post.uri,
                "url": post_url,
                "text": text,
                "created_at": created_at,
                "is_reply": is_reply,
                "parent_uri": parent_uri,
                "root_uri": root_uri
            }
            all_posts.append(post_info)

            # A root reply to an external post must be a reply, and parent_uri must not start with our own DID
            is_root_reply = False
            if is_reply and parent_uri:
                parts = parent_uri.replace("at://", "").split("/")
                if parts:
                    parent_did = parts[0]
                    if parent_did != client.me.did:
                        is_root_reply = True

            if is_root_reply:
                parent_url = ""
                try:
                    parent_parts = parent_uri.replace("at://", "").split("/")
                    if len(parent_parts) >= 3:
                        p_did = parent_parts[0]
                        p_rkey = parent_parts[2]
                        parent_url = f"https://bsky.app/profile/{p_did}/post/{p_rkey}"
                except Exception:
                    pass

                post_info["parent_url"] = parent_url
                root_replies.append(post_info)
                
                if len(root_replies) >= (args.limit + args.skip):
                    break
        
        pages_fetched += 1
        cursor = response.cursor
        if not cursor:
            break
            
    print(f"Retrieved {len(root_replies)} root replies total across {pages_fetched} page(s).")
    
    # Slice target replies based on skip offset
    target_replies = root_replies[args.skip:]
    print(f"Skipping first {args.skip} replies. Analyzing remaining {len(target_replies)} root replies...")

    # Group replies by target parent_uri
    parent_map = {}
    for r in target_replies:
        if r["parent_uri"]:
            parent_map.setdefault(r["parent_uri"], []).append(r)

    duplicate_groups = []
    for parent_uri, posts in parent_map.items():
        if len(posts) > 1:
            # Sort by creation time ascending so the earliest is index 0
            posts_sorted = sorted(posts, key=lambda x: x["created_at"])
            duplicate_groups.append({
                "parent_uri": parent_uri,
                "parent_url": posts[0].get("parent_url", ""),
                "original": posts_sorted[0],
                "duplicates": posts_sorted[1:]
            })

    if not duplicate_groups:
        print("No duplicate replies to the same target post found.")
        sys.exit(0)

    print(f"\nFound {len(duplicate_groups)} target posts with duplicate replies.")

    for group in duplicate_groups:
        print(f"\nTarget Post: {group['parent_url'] or group['parent_uri']}")
        print(f"  [KEEP ORIGINAL] URL: {group['original']['url']} (Created: {group['original']['created_at']})")
        print(f"      Text: \"{group['original']['text'][:100]}...\"")
        
        for idx, dup in enumerate(group["duplicates"], 1):
            print(f"  [DUPLICATE {idx}] URL: {dup['url']} (Created: {dup['created_at']})")
            print(f"      Text: \"{dup['text'][:100]}...\"")

    if not args.delete:
        print("\nDRY RUN: Run with '--delete' to execute the deletion of these duplicate threads.")
        sys.exit(0)

    print("\n--- STARTING AUTOMATED DELETION ---")
    
    for group in duplicate_groups:
        print(f"\nProcessing duplicates for target: {group['parent_url'] or group['parent_uri']}")
        
        for dup in group["duplicates"]:
            dup_root_uri = dup["uri"]
            # Find all posts in the thread (root post itself, and any reply referencing this root)
            thread_posts = []
            for p in all_posts:
                if p["uri"] == dup_root_uri or p["root_uri"] == dup_root_uri:
                    thread_posts.append(p)
            
            # Sort from leaf to root (reverse chronological or reply depth) to delete replies first
            thread_posts_sorted = sorted(thread_posts, key=lambda x: x["created_at"], reverse=True)
            
            print(f"  Deleting thread with root {dup['url']} ({len(thread_posts_sorted)} posts)...")
            for post_to_del in thread_posts_sorted:
                print(f"    Deleting post: {post_to_del['url']}")
                try:
                    client.delete_post(post_to_del["uri"])
                    print("      Success")
                except Exception as e:
                    print(f"      Failed: {e}")

    print("\nDeletion completed successfully.")

if __name__ == "__main__":
    audit_duplicates()
