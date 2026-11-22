import os
import sys
import json
import time
from dotenv import load_dotenv
from atproto import Client, models, IdResolver

load_dotenv('e:/Vector Field Theory/VFT Docs/bluesky_bot/.env')

TARGET_ROOT_URL = "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecae7q7r2e"

CORRECTION_TEXT = (
    "CORRECTION & AUDIT RE-ANCHOR:\n\n"
    "Our initial audit fell for a tabloid rage-bait trap—treating 3 anonymous Twitter trolls cited by Fox News as material proof of \"deception.\"\n\n"
    "Ground Truth: Fox News manufactured a smear out of tweets. Amanda Seyfried did not commit fraud.\n"
    "Revised: FAIL (-0.75, +0.65)"
)

STORY_PATH = "e:/Vector Field Theory/VFT Docs/bluesky_bot/stories/live/factcheck_amanda-seyfried-elizabeth-holmes-doc.json"
GRAPH_IMG = "e:/Vector Field Theory/VFT Docs/bluesky_bot/graph_png/amanda-seyfried-elizabeth-holmes-doc_graph.png"
VERDICT_IMG = "e:/Vector Field Theory/VFT Docs/bluesky_bot/graph_png/amanda-seyfried-elizabeth-holmes-doc_info_card_verdict.png"
ANALYSIS_IMG = "e:/Vector Field Theory/VFT Docs/bluesky_bot/graph_png/amanda-seyfried-elizabeth-holmes-doc_info_card_analysis.png"

def parse_bsky_url(url):
    parts = url.strip("/").split("/")
    handle_idx = parts.index("profile") + 1
    post_idx = parts.index("post") + 1
    return parts[handle_idx], parts[post_idx]

def upload_img(client, path, alt="Card"):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        up = client.com.atproto.repo.upload_blob(data)
        return models.AppBskyEmbedImages.Main(
            images=[models.AppBskyEmbedImages.Image(alt=alt, image=up.blob)]
        )
    return None

def main():
    handle = os.environ.get("BSKY_HANDLE", "judgement-bot.bsky.social")
    password = os.environ.get("BSKY_PASSWORD")
    if not password:
        print("ERROR: BSKY_PASSWORD not found.")
        sys.exit(1)

    with open(STORY_PATH, "r", encoding="utf-8") as f:
        story = json.load(f)[0]

    posts = story.get("posts", [])
    if not posts:
        print("ERROR: No posts found in story.")
        sys.exit(1)

    print(f"Authenticating as {handle}...")
    client = Client()
    client.login(handle, password)

    print(f"Resolving target root post: {TARGET_ROOT_URL}...")
    t_handle, t_rkey = parse_bsky_url(TARGET_ROOT_URL)
    resolver = IdResolver()
    did = resolver.handle.resolve(t_handle)

    resp = client.com.atproto.repo.get_record(
        models.ComAtprotoRepoGetRecord.Params(
            repo=did,
            collection="app.bsky.feed.post",
            rkey=t_rkey
        )
    )
    root_cid = resp.cid
    root_uri = resp.uri
    root_ref = models.ComAtprotoRepoStrongRef.Main(cid=root_cid, uri=root_uri)

    # 1. Post Correction Reply directly under the target root post
    print("Posting Correction Reply with Verdict Card...")
    verdict_embed = upload_img(client, VERDICT_IMG, "Audit Verdict Card")
    corr_record = models.AppBskyFeedPost.Record(
        created_at=client.get_current_time_iso(),
        text=CORRECTION_TEXT,
        reply=models.AppBskyFeedPost.ReplyRef(parent=root_ref, root=root_ref),
        embed=verdict_embed
    )
    corr_res = client.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=client.me.did,
            collection=models.ids.AppBskyFeedPost,
            record=corr_record
        )
    )
    corr_rkey = corr_res.uri.split("/")[-1]
    corr_url = f"https://bsky.app/profile/{client.me.handle}/post/{corr_rkey}"
    print(f"  -> Correction posted! URL: {corr_url}")

    # 2. Chain the full 15-post redone thread under the correction post
    parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=corr_res.cid, uri=corr_res.uri)

    print(f"\nPosting full 15-post redone thread chained under correction...")
    for idx, text in enumerate(posts):
        print(f"Posting element {idx+1}/{len(posts)} ({len(text)} chars)...")
        embed = None
        if idx == 0 and os.path.exists(GRAPH_IMG):
            embed = upload_img(client, GRAPH_IMG, "Trajectory Graph")
        elif idx == 3 and os.path.exists(VERDICT_IMG):
            embed = upload_img(client, VERDICT_IMG, "Verdict Card")
        elif idx == 11 and os.path.exists(ANALYSIS_IMG):
            embed = upload_img(client, ANALYSIS_IMG, "Analysis & Perspectives Card")

        post_record = models.AppBskyFeedPost.Record(
            created_at=client.get_current_time_iso(),
            text=text,
            reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref),
            embed=embed
        )
        res = client.com.atproto.repo.create_record(
            models.ComAtprotoRepoCreateRecord.Data(
                repo=client.me.did,
                collection=models.ids.AppBskyFeedPost,
                record=post_record
            )
        )
        parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=res.cid, uri=res.uri)
        rkey = res.uri.split("/")[-1]
        print(f"  -> Posted {idx+1}: https://bsky.app/profile/{client.me.handle}/post/{rkey}")
        time.sleep(2.0)

    print("\nAll correction posts and thread successfully published!")

if __name__ == "__main__":
    main()
