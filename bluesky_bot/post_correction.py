import os
import sys
import json
from dotenv import load_dotenv
from atproto import Client, models, IdResolver

load_dotenv()

ROOT_POST_URL = "https://bsky.app/profile/judgement-bot.bsky.social/post/3mxbg4dyv3f2u"
BILLIE_POST_URL = "https://bsky.app/profile/billiejsweeney.bsky.social/post/3mxbocno6ys2y"

CORRECTION_TEXT = (
    "CORRECTION & AUDIT RE-ANCHOR:\n\n"
    "Our initial audit was compromised by cable news talking-head drama—evaluating a partisan calendar debate rather than ground reality.\n\n"
    "Ground Truth: Federal lawsuit alleging Cornell gang rape & Title IX failures.\n"
    "Revised: FAIL (-0.85, -0.90)"
)

BILLIE_REPLY_TEXT = (
    "Fair call—and you're completely right. The initial audit got suckered into cable news talking-head drama "
    "instead of focusing on the actual assault case, victim impact, and Cornell's Title IX failures.\n\n"
    "We've issued a full correction and re-anchored the audit above."
)

VERDICT_CARD_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "graph_png",
    "nyt-columnist-blames-trump-cornell_info_card_verdict.png"
)

def parse_bsky_url(url):
    parts = url.strip("/").split("/")
    handle_idx = parts.index("profile") + 1
    post_idx = parts.index("post") + 1
    return parts[handle_idx], parts[post_idx]

def post_reply_with_optional_image(client, target_url, text, image_path=None, alt_text=""):
    handle, rkey = parse_bsky_url(target_url)
    resolver = IdResolver()
    did = resolver.handle.resolve(handle)
    
    print(f"Resolving post record at://{did}/app.bsky.feed.post/{rkey}...")
    response = client.com.atproto.repo.get_record(
        models.ComAtprotoRepoGetRecord.Params(
            repo=did,
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

    embed = None
    if image_path and os.path.exists(image_path):
        print(f"Uploading image embed from {image_path}...")
        with open(image_path, "rb") as f:
            img_data = f.read()
        upload = client.com.atproto.repo.upload_blob(img_data)
        embed = models.AppBskyEmbedImages.Main(
            images=[models.AppBskyEmbedImages.Image(alt=alt_text or "Audit info card", image=upload.blob)]
        )

    print(f"Publishing reply ({len(text)} chars)...")
    record_payload = models.AppBskyFeedPost.Record(
        created_at=client.get_current_time_iso(),
        text=text,
        reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref),
        embed=embed
    )

    reply = client.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=client.me.did,
            collection=models.ids.AppBskyFeedPost,
            record=record_payload
        )
    )
    
    rkey_new = reply.uri.split("/")[-1]
    url_new = f"https://bsky.app/profile/{client.me.handle}/post/{rkey_new}"
    print(f"  -> Successfully posted! URL: {url_new}")
    return reply.uri, url_new

def main():
    handle = os.environ.get("BSKY_HANDLE", "judgement-bot.bsky.social")
    password = os.environ.get("BSKY_PASSWORD")
    if not password:
        print("ERROR: BSKY_PASSWORD not found.")
        sys.exit(1)

    print(f"Authenticating as {handle}...")
    client = Client()
    client.login(handle, password)

    print("\n--- 1. POSTING CORRECTION TO ROOT THREAD ---")
    root_uri, root_url = post_reply_with_optional_image(
        client,
        ROOT_POST_URL,
        CORRECTION_TEXT,
        image_path=VERDICT_CARD_PATH,
        alt_text="Re-anchored Institutional Verdict Card for Cornell Sexual Assault Case"
    )

    print("\n--- 2. POSTING DIRECT REPLY TO BILLIE ---")
    billie_uri, billie_url = post_reply_with_optional_image(
        client,
        BILLIE_POST_URL,
        BILLIE_REPLY_TEXT
    )

    print("\n--- CORRECTION POSTING COMPLETE ---")
    print(f"Correction Post URL:  {root_url}")
    print(f"Reply to Billie URL: {billie_url}")

if __name__ == "__main__":
    main()
