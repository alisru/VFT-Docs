import os
import sys
import re
import json
import time
import glob
import random
from datetime import datetime

try:
    from atproto import Client, models
except ImportError:
    Client = None
    models = None

def publish_story(story, graph_path=None, card_path=None, live=False, handle=None, password=None):
    """
    Publishes an evaluated story thread to Bluesky (or prints dry run) and archives it to stories/live/.
    """
    subject = story.get("subject", "Assessment")
    slug = story.get("id") or "story"
    posts = story.get("posts", [])
    link = story.get("link", "")
    grounding_url = story.get("grounding_url", "")
    if not grounding_url and len(posts) > 2:
        m = re.search(r'(https?://[^\s]+)', posts[2])
        if m:
            grounding_url = m.group(1).rstrip('.,;:)')
            posts[2] = posts[2].replace(m.group(1), '').strip()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    live_dir = os.path.join(script_dir, "stories", "live")
    os.makedirs(live_dir, exist_ok=True)
    out_json = os.path.join(live_dir, f"factcheck_{slug}.json")

    print(f"\n{'='*70}\nPUBLISHING AUDIT: {subject}\n{'='*70}")

    if not live:
        print("[DRY RUN MODE] Simulating Bluesky Thread:\n")
        embed_map = {
            1: f"[Embed: Trajectory Graph -> {graph_path}]" if graph_path else "[No Embed]",
            2: f"[Embed: Primary Story Card -> {link}]" if link else "[No Embed]",
            3: f"[Embed: Verification Card -> {grounding_url}]" if grounding_url else "[No Embed]",
            4: f"[Embed: Deep-Dive Analysis Card -> {card_path}]" if card_path else "[No Embed]"
        }

        for idx, text in enumerate(posts, start=1):
            embed_label = embed_map.get(idx, "")
            print(f"--- Post {idx}/{len(posts)} {embed_label} ({len(text)} chars) ---\n{text}\n")

        story["status"] = "COMPLETED DRY RUN"
        story["published_at"] = datetime.now().isoformat()
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump([story], f, indent=2, ensure_ascii=False)
        print(f"Dry run archived to: {out_json}")
        return True

    # --- LIVE PUBLISHING ---
    b_handle = handle or os.environ.get("BSKY_HANDLE")
    b_pass = password or os.environ.get("BSKY_PASSWORD")
    if not b_handle or not b_pass:
        raise ValueError("BSKY_HANDLE or BSKY_PASSWORD environment variable is missing for live posting.")

    if Client is None:
        raise ImportError("atproto library is required for live Bluesky posting. Install with: pip install atproto")

    print(f"Logging into Bluesky as @{b_handle}...")
    client = Client()
    client.login(b_handle, b_pass)

    # 1. Upload Graph Image
    graph_embed = None
    if graph_path and os.path.exists(graph_path):
        print(f"Uploading graph image: {graph_path}...")
        with open(graph_path, "rb") as f:
            blob = client.upload_blob(f.read())
        graph_embed = models.AppBskyEmbedImages.Main(
            images=[models.AppBskyEmbedImages.Image(alt=f"Psochic Hegemony Assessment Graph for {subject}", image=blob.blob)]
        )

    # 2. Upload Deep-Dive Analysis Card
    card_embed = None
    if card_path and os.path.exists(card_path):
        print(f"Uploading analysis card: {card_path}...")
        with open(card_path, "rb") as f:
            blob = client.upload_blob(f.read())
        card_embed = models.AppBskyEmbedImages.Main(
            images=[models.AppBskyEmbedImages.Image(alt=f"Deep-Dive Forensic Analysis Card for {subject}", image=blob.blob)]
        )

    # 3. Create Link Preview Embeds
    link_embed = None
    if link and link.startswith("http"):
        link_embed = models.AppBskyEmbedExternal.Main(
            external=models.AppBskyEmbedExternal.External(
                title=f"Source Article | {subject[:40]}",
                description=f"Primary reported news event: {subject}",
                uri=link
            )
        )

    grounding_embed = None
    if grounding_url and grounding_url.startswith("http"):
        grounding_embed = models.AppBskyEmbedExternal.Main(
            external=models.AppBskyEmbedExternal.External(
                title=f"Verification Evidence | {subject[:40]}",
                description="Empirical documentation, official filings, and verified reporting",
                uri=grounding_url
            )
        )

    # 4. Post Thread Sequentially
    post_uris = []
    root_ref = None
    parent_ref = None

    for idx, text in enumerate(posts, start=1):
        print(f"Posting Part {idx}/{len(posts)} to Bluesky...")
        cur_embed = None
        if idx == 1:
            cur_embed = graph_embed
        elif idx == 2:
            cur_embed = link_embed
        elif idx == 3:
            cur_embed = grounding_embed
        elif idx == len(posts) and card_embed:
            cur_embed = card_embed

        record_data = {
            "repo": client.me.did,
            "collection": models.ids.AppBskyFeedPost,
            "record": models.AppBskyFeedPost.Record(
                created_at=client.get_current_time_iso(),
                text=text,
                embed=cur_embed,
                langs=["en"]
            )
        }

        if idx > 1 and parent_ref and root_ref:
            record_data["record"].reply = models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref)

        resp = client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(**record_data))
        post_uris.append(resp.uri)

        ref = models.ComAtprotoRepoStrongRef.Main(cid=resp.cid, uri=resp.uri)
        if idx == 1:
            root_ref = ref
        parent_ref = ref

    story["status"] = f"LIVE POSTED ({b_handle})"
    story["published_at"] = datetime.now().isoformat()
    story["post_uris"] = post_uris
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump([story], f, indent=2, ensure_ascii=False)

    print(f"Successfully posted live thread ({len(post_uris)} parts)! Archived to: {out_json}")
    return True

def validate_draft(story):
    """
    Validates a story draft before live posting (checks character lengths and post sequence).
    """
    posts = story.get("posts", [])
    if not posts:
        return False, "Story has no posts."
    for idx, p in enumerate(posts, start=1):
        if len(p) > 280:
            return False, f"Post {idx} exceeds 280 chars ({len(p)} chars): {p[:40]}..."
    return True, f"Validation passed ({len(posts)} posts)."

def post_batch_drafts(live=False, min_delay=10, max_delay=30, watch=False):
    """
    Batch poster / scheduler:
    Scans stories/ for pending factcheck_*.json drafts, validates them, posts them sequentially
    with delays, and archives to stories/live/.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    drafts_dir = os.path.join(script_dir, "stories")
    live_dir = os.path.join(drafts_dir, "live")
    os.makedirs(live_dir, exist_ok=True)

    print(f"\n{'='*70}\nSTARTING POSTER / SCHEDULER (Live: {live}, Delay: {min_delay}-{max_delay}s, Watch: {watch})\n{'='*70}")

    while True:
        # Find drafts in stories/ directly (not in live/)
        pattern = os.path.join(drafts_dir, "factcheck_*.json")
        candidates = [f for f in glob.glob(pattern) if not os.path.commonpath([f, live_dir]) == live_dir]

        if not candidates:
            if watch:
                print("No pending drafts found. Watching for new stories (checking every 10s)...")
                time.sleep(10)
                continue
            else:
                print("No pending drafts found in stories/ to post.")
                break

        print(f"Found {len(candidates)} pending draft(s) to process.")

        for path in candidates:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                story = data[0] if isinstance(data, list) and len(data) > 0 else data

                valid, msg = validate_draft(story)
                if not valid:
                    print(f"Skipping invalid draft {os.path.basename(path)}: {msg}")
                    continue

                slug = story.get("id") or "story"
                # Locate graphs and cards
                graph_path = os.path.join(script_dir, "graph_png", f"graph_{slug}.png")
                if not os.path.exists(graph_path):
                    graph_path = story.get("graph_path")

                card_path = os.path.join(script_dir, "card_png", f"card_{slug}.png")
                if not os.path.exists(card_path):
                    card_path = story.get("card_path")

                print(f"\nProcessing draft: {story.get('subject', slug)}...")
                success = publish_story(story, graph_path=graph_path, card_path=card_path, live=live)

                if success and live:
                    # Remove the unposted draft file now that it's published to stories/live/
                    if os.path.exists(path) and os.path.abspath(path) != os.path.abspath(os.path.join(live_dir, os.path.basename(path))):
                        os.remove(path)

                # Delay before next post
                delay = random.uniform(float(min_delay), float(max_delay))
                print(f"Waiting {delay:.1f}s before next post...")
                time.sleep(delay)

            except Exception as e:
                print(f"Error processing draft {path}: {e}")

        if not watch:
            break

    print("\n--- Poster / Scheduler Completed ---")

