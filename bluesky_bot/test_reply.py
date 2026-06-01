import os
import sys
from dotenv import load_dotenv
from atproto import Client, models, IdResolver

load_dotenv()

TARGET_POST_URL = "https://bsky.app/profile/alisru.bsky.social/post/3mmg7utugzk2o"
handle_env = os.environ.get('BSKY_HANDLE', 'alethekanon.bsky.social')
password = os.environ.get('BSKY_PASSWORD')

if not password:
    print("ERROR: BSKY_PASSWORD not found.")
    sys.exit(1)

print(f"Authenticating as {handle_env}...")
client = Client()
try:
    client.login(handle_env, password)
    print("Successfully logged in!")
    print(f"Logged in DID: {client.me.did}")
except Exception as e:
    print(f"Login failed: {e}")
    sys.exit(1)

# Let's try to update the profile bio as requested in instructions
bio_text = (
    "Hegemonic Analyst running 5-Phase Convergence Tests on reality.\n"
    "Alethekanon = Uncompromising logic & truth.\n"
    "Awwthekanon = Empathy, human cost & healing.\n"
    "Brothekanon = Pointing out the sheer absurdity of it all.\n"
    "(Truth is a vector, not a list.)"
)

print("Updating profile bio...")
try:
    # Get current profile first to avoid overwriting other fields like display name
    profile = client.get_profile(client.me.did)
    
    # Update profile description
    client.com.atproto.repo.put_record(
        models.ComAtprotoRepoPutRecord.Data(
            repo=client.me.did,
            collection='app.bsky.actor.profile',
            rkey='self',
            record=models.AppBskyActorProfile.Record(
                description=bio_text,
                display_name=profile.display_name,
                avatar=profile.avatar
            )
        )
    )
    print("Profile bio updated successfully!")
except Exception as e:
    print(f"Warning: Failed to update profile bio: {e}")
    # If put_record fails, let's try direct update if available, or just log it
    try:
        # Some versions have client.update_profile
        if hasattr(client, 'update_profile'):
            client.update_profile(description=bio_text)
            print("Profile bio updated via update_profile helper!")
    except Exception as e2:
        print(f"Direct update also failed: {e2}")

# Parse the target post URL
def parse_bsky_url(url):
    parts = url.strip("/").split("/")
    if "profile" not in parts or "post" not in parts:
        raise ValueError("Invalid Bluesky post URL format.")
    handle_idx = parts.index("profile") + 1
    post_idx = parts.index("post") + 1
    return parts[handle_idx], parts[post_idx]

try:
    target_handle, rkey = parse_bsky_url(TARGET_POST_URL)
    print(f"Resolving DID for target handle: {target_handle}")
    resolver = IdResolver()
    target_did = resolver.handle.resolve(target_handle)
    
    uri = f"at://{target_did}/app.bsky.feed.post/{rkey}"
    print(f"Fetching target post: {uri}")
    
    response = client.com.atproto.repo.get_record(
        models.ComAtprotoRepoGetRecord.Params(
            repo=target_did,
            collection='app.bsky.feed.post',
            rkey=rkey
        )
    )
    
    target_cid = response.cid
    target_uri = response.uri
    target_record = response.value
    
    if hasattr(target_record, 'reply') and target_record.reply:
        root_ref = target_record.reply.root
    else:
        root_ref = models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)
        
    parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)
    
    test_reply_text = (
        "Alethekanon Bot Initialization: SUCCESS.\n\n"
        "Connection verified. Protocol channels established.\n"
        "Alethekanon: Standing by for analysis. Coordinates calibrated.\n"
        "Awwthekanon: Warm greetings! Ready to support and connect.\n"
        "Brothekanon: We're live, bro! Let's do this."
    )
    
    print("Posting verification reply...")
    reply = client.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=client.me.did,
            collection=models.ids.AppBskyFeedPost,
            record=models.AppBskyFeedPost.Record(
                created_at=client.get_current_time_iso(),
                text=test_reply_text,
                reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref)
            )
        )
    )
    print(f"Success! Reply posted! URI: {reply.uri}")
    
except Exception as e:
    print(f"Failed to post reply: {e}")
