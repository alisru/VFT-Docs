import os
import sys
import json
import time
from dotenv import load_dotenv
from atproto import Client, models, IdResolver

load_dotenv()

# The specific verdict post flagged by the user
TARGET_VERDICT_POST_URL = "https://bsky.app/profile/judgement-bot.bsky.social/post/3mxebygzse426"

CORRECTION_TEXT = (
    "CORRECTION & RE-ANCHOR:\n\n"
    "Our initial audit was compromised by Fox News oppo research—evaluating an out-of-context 2020 clip instead of legislative reality.\n\n"
    "Ground Truth: Bipartisan student mental health reform (HB 18) vs chronic Texas school underfunding.\n"
    "Revised: FAIL (-0.75, -0.80)"
)

STORY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "stories",
    "factcheck_talarico-texas-schools.json"
)

GRAPH_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph_png", "talarico-texas-schools_graph.png")
VERDICT_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph_png", "talarico-texas-schools_info_card_verdict.png")
ANALYSIS_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph_png", "talarico-texas-schools_info_card_analysis.png")

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

    print(f"Resolving target post: {TARGET_VERDICT_POST_URL}...")
    t_handle, t_rkey = parse_bsky_url(TARGET_VERDICT_POST_URL)
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

    # Step 1: Post the initial Correction Notice with Verdict Card embed
    print("\n[Step 1] Posting Correction Notice...")
    corr_embed = None
    if os.path.exists(VERDICT_IMG):
        print(f"Uploading verdict card image for correction...")
        with open(VERDICT_IMG, "rb") as f:
            v_blob = client.com.atproto.repo.upload_blob(f.read())
        corr_embed = models.AppBskyEmbedImages.Main(
            images=[models.AppBskyEmbedImages.Image(alt="Aletheia Revised Verdict Card", image=v_blob.blob)]
        )

    corr_record = models.AppBskyFeedPost.Record(
        created_at=client.get_current_time_iso(),
        text=CORRECTION_TEXT,
        reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref),
        embed=corr_embed,
        langs=["en"]
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
    print(f"  -> Correction posted: {corr_url}")

    # Set parent for the thread head to the correction post
    parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=corr_res.cid, uri=corr_res.uri)

    # Step 2: Upload images for Post 1 of the redone thread (Graph + Verdict Card + Analysis Card)
    print("\n[Step 2] Uploading images for redone thread head...")
    embed_images = []
    image_paths = [
        (GRAPH_IMG, "Aletheia Trajectory Graph: Stated Claim vs Ground Reality"),
        (VERDICT_IMG, "Verdict Summary Card: Claim, Reality, and Revised Verdict"),
        (ANALYSIS_IMG, "Deep Analysis Card: Social Physics, Context, and Trajectory")
    ]

    for img_path, alt in image_paths:
        if os.path.exists(img_path):
            print(f"Uploading {os.path.basename(img_path)}...")
            with open(img_path, "rb") as f:
                blob = client.com.atproto.repo.upload_blob(f.read())
            embed_images.append(models.AppBskyEmbedImages.Image(alt=alt, image=blob.blob))

    first_embed = models.AppBskyEmbedImages.Main(images=embed_images) if embed_images else None

    published_rkeys = [corr_rkey]
    published_urls = [corr_url]

    print(f"\n[Step 3] Publishing full {len(posts)}-post redone thread...")
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

    print("\n--- ALL POSTS PUBLISHED SUCCESSFULLY ---")
    print(f"Correction Post URL: {corr_url}")
    print(f"Thread Head URL:     {published_urls[1]}")

    # Step 4: Update live story JSON in stories/live/
    live_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "stories",
        "live",
        "factcheck_talarico-texas-schools.json"
    )
    if os.path.exists(live_path):
        with open(live_path, "r", encoding="utf-8") as f:
            live_data = json.load(f)
        live_story = live_data[0]
        live_story.setdefault("amendment", {})
        live_story["amendment"]["correction_post_url"] = corr_url
        live_story["amendment"]["redone_thread_head_url"] = published_urls[1]
        live_story["amendment"]["redone_thread_post_urls"] = published_urls[1:]
        live_story["amendment"]["redone_thread_rkeys"] = published_rkeys[1:]

        # Update the live story's primary evaluation fields to the redone evaluation
        for k in ["thinking", "claim_u", "claim_psi", "real_u", "real_psi", "claim_rnet", "real_rnet",
                  "claim_z", "real_z", "claim_z_profile", "real_z_profile", "claim_integrity",
                  "real_integrity", "aspects", "multiAspect", "spiritual", "spiritual_traditions",
                  "scraped_text", "actors", "posts"]:
            if k in story:
                live_story[k] = story[k]

        with open(live_path, "w", encoding="utf-8") as f:
            json.dump(live_data, f, indent=2, ensure_ascii=False)
        print(f"Updated {live_path} with redone audit and live correction metadata.")

    # Step 5: Rebuild registries
    print("Synchronizing registries...")
    import subprocess
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "rebuild_registries_son.py")], check=True)
    print("Registry synchronization complete.")

if __name__ == "__main__":
    main()
