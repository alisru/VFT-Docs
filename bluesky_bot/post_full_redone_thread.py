import os
import sys
import json
import time
from dotenv import load_dotenv
from atproto import Client, models, IdResolver

load_dotenv()

CORRECTION_POST_URL = "https://bsky.app/profile/judgement-bot.bsky.social/post/3mxc6wstme22s"
STORY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "stories",
    "factcheck_nyt-columnist-blames-trump-cornell.json"
)

GRAPH_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph_png", "nyt-columnist-blames-trump-cornell_graph.png")
VERDICT_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph_png", "nyt-columnist-blames-trump-cornell_info_card_verdict.png")
ANALYSIS_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph_png", "nyt-columnist-blames-trump-cornell_info_card_analysis.png")

def parse_bsky_url(url):
    parts = url.strip("/").split("/")
    handle_idx = parts.index("profile") + 1
    post_idx = parts.index("post") + 1
    return parts[handle_idx], parts[post_idx]

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

    print(f"Resolving correction post target: {CORRECTION_POST_URL}...")
    t_handle, t_rkey = parse_bsky_url(CORRECTION_POST_URL)
    resolver = IdResolver()
    did = resolver.handle.resolve(t_handle)

    target_res = client.com.atproto.repo.get_record(
        models.ComAtprotoRepoGetRecord.Params(
            repo=did,
            collection="app.bsky.feed.post",
            rkey=t_rkey
        )
    )

    t_val = target_res.value
    t_cid = target_res.cid
    t_uri = target_res.uri

    if hasattr(t_val, "reply") and t_val.reply:
        root_ref = t_val.reply.root
    else:
        root_ref = models.ComAtprotoRepoStrongRef.Main(cid=t_cid, uri=t_uri)

    parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=t_cid, uri=t_uri)

    # 1. Upload Images for Post 0 (Graph + Verdict Card + Analysis Card)
    embed_images = []
    image_paths = [
        (GRAPH_IMG, "Aletheia Trajectory Graph: Stated Claim vs Ground Reality"),
        (VERDICT_IMG, "Verdict Summary Card: Claim, Reality, and Revised Verdict"),
        (ANALYSIS_IMG, "Deep Analysis Card: Social Physics, Context, and Trajectory")
    ]

    for img_path, alt in image_paths:
        if os.path.exists(img_path):
            print(f"Uploading image embed from {os.path.basename(img_path)}...")
            with open(img_path, "rb") as f:
                blob = client.com.atproto.repo.upload_blob(f.read())
            embed_images.append(models.AppBskyEmbedImages.Image(alt=alt, image=blob.blob))
        else:
            print(f"Warning: Image file not found: {img_path}")

    first_embed = models.AppBskyEmbedImages.Main(images=embed_images) if embed_images else None

    published_rkeys = []
    published_urls = []

    print(f"\nPublishing full {len(posts)}-post re-audited thread...")

    for idx, text in enumerate(posts):
        print(f"Posting Part {idx + 1}/{len(posts)} ({len(text)} chars)...")
        embed = first_embed if idx == 0 else None

        record_data = models.AppBskyFeedPost.Record(
            created_at=client.get_current_time_iso(),
            text=text,
            reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref),
            embed=embed,
            langs=["en"]
        )

        reply = client.com.atproto.repo.create_record(
            models.ComAtprotoRepoCreateRecord.Data(
                repo=client.me.did,
                collection=models.ids.AppBskyFeedPost,
                record=record_data
            )
        )

        rkey_new = reply.uri.split("/")[-1]
        url_new = f"https://bsky.app/profile/{client.me.handle}/post/{rkey_new}"
        published_rkeys.append(rkey_new)
        published_urls.append(url_new)
        print(f"  -> Part {idx + 1} published: {url_new}")

        parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=reply.cid, uri=reply.uri)
        time.sleep(1.0)

    print("\n--- ALL 15 POSTS PUBLISHED SUCCESSFULLY ---")
    print(f"Thread Head URL: {published_urls[0]}")

    # Update story JSON in live/
    live_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "stories",
        "live",
        "factcheck_nyt-columnist-blames-trump-cornell.json"
    )
    if os.path.exists(live_path):
        with open(live_path, "r", encoding="utf-8") as f:
            live_data = json.load(f)
        live_story = live_data[0]
        live_story.setdefault("amendment", {})
        live_story["amendment"]["redone_thread_head_url"] = published_urls[0]
        live_story["amendment"]["redone_thread_post_urls"] = published_urls
        live_story["amendment"]["redone_thread_rkeys"] = published_rkeys
        
        # Also append to main post_urls / rkeys
        for rk in published_rkeys:
            if rk not in live_story.get("rkeys", []):
                live_story.setdefault("rkeys", []).append(rk)
        for u in published_urls:
            if u not in live_story.get("post_urls", []):
                live_story.setdefault("post_urls", []).append(u)

        with open(live_path, "w", encoding="utf-8") as f:
            json.dump(live_data, f, indent=2, ensure_ascii=False)
        print("Updated stories/live/factcheck_nyt-columnist-blames-trump-cornell.json with new thread URLs.")

if __name__ == "__main__":
    main()
