import os
import sys
from dotenv import load_dotenv
from atproto import Client, models, IdResolver

load_dotenv()

TARGET_POST_URL = "https://bsky.app/profile/alisru.bsky.social/post/3mmg7utugzk2o"
handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
password = os.environ.get('BSKY_PASSWORD')

if not password:
    print("ERROR: BSKY_PASSWORD not found.")
    sys.exit(1)

client = Client()
try:
    client.login(handle, password)
except Exception as e:
    print(f"Login failed: {e}")
    sys.exit(1)

def parse_bsky_url(url):
    parts = url.strip("/").split("/")
    if "profile" not in parts or "post" not in parts:
        raise ValueError("Invalid Bluesky post URL format.")
    handle_idx = parts.index("profile") + 1
    post_idx = parts.index("post") + 1
    return parts[handle_idx], parts[post_idx]

try:
    target_handle, rkey = parse_bsky_url(TARGET_POST_URL)
    resolver = IdResolver()
    target_did = resolver.handle.resolve(target_handle)
    
    response = client.com.atproto.repo.get_record(
        models.ComAtprotoRepoGetRecord.Params(
            repo=target_did,
            collection='app.bsky.feed.post',
            rkey=rkey
        )
    )
    
    target_record = response.value
    print("--- TARGET POST CONTENT ---")
    print(f"Author: {target_handle} ({target_did})")
    print(f"Text: {target_record.text}")
    print("---------------------------")
    
except Exception as e:
    print(f"Failed to fetch post: {e}")
