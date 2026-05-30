import os
import sys
from dotenv import load_dotenv
from atproto import Client, models, IdResolver

load_dotenv()

# Example: https://bsky.app/profile/motherjones.com/post/3mn3fzc3oau2d
TARGET_POST_URL = "https://bsky.app/profile/motherjones.com/post/3mn3fzc3oau2d"

def parse_bsky_url(url):
    """Parses a bsky.app URL to extract the handle and the record key (rkey)."""
    parts = url.strip("/").split("/")
    if "profile" not in parts or "post" not in parts:
        raise ValueError("Invalid Bluesky post URL format.")

    handle_idx = parts.index("profile") + 1
    post_idx = parts.index("post") + 1

    handle = parts[handle_idx]
    rkey = parts[post_idx]

    return handle, rkey

def reply_to_post(client, handle, rkey, text):
    """Fetches the target post and replies to it."""
    print(f"Resolving DID for handle: {handle}")
    resolver = IdResolver()
    did = resolver.handle.resolve(handle)

    print(f"Fetching post record: {rkey}")
    # We need the CID and URI of the post to reply to it
    uri = f"at://{did}/app.bsky.feed.post/{rkey}"

    try:
        # Get the target post data
        response = client.com.atproto.repo.get_record(
            models.ComAtprotoRepoGetRecord.Params(
                repo=did,
                collection='app.bsky.feed.post',
                rkey=rkey
            )
        )

        target_cid = response.cid
        target_uri = response.uri

        # Determine root and parent references
        # If the target post is already a reply, its root is the root of the thread.
        # Otherwise, the target post itself is the root.
        target_record = response.value

        if hasattr(target_record, 'reply') and target_record.reply:
            root_ref = target_record.reply.root
        else:
            root_ref = models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)

        parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)

        print("Constructing reply...")
        reply = client.com.atproto.repo.create_record(
            models.ComAtprotoRepoCreateRecord.Data(
                repo=client.me.did,
                collection=models.ids.AppBskyFeedPost,
                record=models.AppBskyFeedPost.Record(
                    created_at=client.get_current_time_iso(),
                    text=text,
                    reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref)
                )
            )
        )
        print(f"Successfully replied! Reply URI: {reply.uri}")
        return True

    except Exception as e:
        print(f"Failed to fetch or reply to post: {e}")
        return False

if __name__ == "__main__":
    password = os.environ.get('BSKY_PASSWORD')
    if not password:
        print("ERROR: BSKY_PASSWORD not found.")
        sys.exit(1)

    print("Authenticating...")
    client = Client()
    try:
        client.login('judgement-bot.bsky.social', password)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    try:
        handle, rkey = parse_bsky_url(TARGET_POST_URL)
        print(f"Target Handle: {handle}, Record Key: {rkey}")

        # DO NOT EXECUTE LIVE POST AUTOMATICALLY IN THIS PROOF OF CONCEPT
        print("\n--- DRY RUN ---")
        print("This script is configured to parse the URL and demonstrate how the reply references are built.")
        print("To actually post, you would call `reply_to_post(client, handle, rkey, 'Your text here')`.")

    except ValueError as e:
        print(e)
