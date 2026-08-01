import os
import sys

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

import json
import re
import argparse
import time
from dotenv import load_dotenv
from atproto import Client, models, IdResolver
import shutil

# Load environment variables
load_dotenv()

def parse_bsky_url(url):
    """Parses a bsky.app URL to extract the handle and the record key (rkey)."""
    parts = url.strip("/").split("/")
    if "profile" not in parts or "post" not in parts:
        raise ValueError("Invalid Bluesky post URL format. Must contain '/profile/<handle>/post/<rkey>'")

    handle_idx = parts.index("profile") + 1
    post_idx = parts.index("post") + 1

    return parts[handle_idx], parts[post_idx]

def split_text(text, max_len=299):
    """Splits text dynamically at the last newline or space before max_len.
    Avoids orphaning short header lines (e.g. 'Brothekanon:') by only
    splitting at a newline if the chunk before it is at least 80 chars.
    Ensures that we don't leave a tiny orphaned tail (less than 25 chars)
    by walking back to split at a previous space if needed.
    """
    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break

        split_idx = text.rfind('\n', 0, max_len)
        # Only split at newline if the chunk before it is substantive (>=80 chars)
        # This prevents short label lines like 'Brothekanon:' becoming orphan posts
        if split_idx != -1 and split_idx < 80:
            split_idx = -1

        if split_idx == -1:
            split_idx = text.rfind(' ', 0, max_len)
            if split_idx != -1:
                # If splitting here leaves an orphaned word/tail of less than 25 chars,
                # walk back to find a previous space that leaves a larger, readable tail.
                while split_idx != -1 and (len(text) - split_idx) < 25:
                    prev_space = text.rfind(' ', 0, split_idx)
                    if prev_space == -1:
                        break
                    split_idx = prev_space

        if split_idx == -1:
            # Force split if no space or newline
            split_idx = max_len

        chunks.append(text[:split_idx].strip())
        text = text[split_idx:].strip()

    return chunks

def pack_posts(posts, max_len=299):
    """
    Packs a list of strings into final posts.
    If a string splits and leaves a tail (carry_over), the tail is merged with the next string 
    so we don't waste an entire Bluesky post on an orphaned 1 or 2 words.
    """
    final_posts = []
    carry_over = ""
    
    for p in posts:
        current = (carry_over + " " + p).strip() if carry_over else p.strip()
        carry_over = ""
            
        if len(current) <= max_len:
            final_posts.append(current)
        else:
            chunks = split_text(current, max_len)
            final_posts.extend(chunks[:-1])
            carry_over = chunks[-1]
            
    if carry_over:
        final_posts.append(carry_over)
        
    return final_posts

# Cache of target_urls we already have a story for. Built once per process by
# scanning stories/ (+ subdirs); kept current by save_and_sync_story. The old
# inline scan re-read every story JSON on disk for EVERY thread posted.
_REPLIED_TARGETS = None

def _target_already_replied(target_url):
    global _REPLIED_TARGETS
    if _REPLIED_TARGETS is None:
        _REPLIED_TARGETS = set()
        stories_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stories")
        scan_dirs = [stories_root] + [
            os.path.join(stories_root, d)
            for d in (os.listdir(stories_root) if os.path.isdir(stories_root) else [])
            if os.path.isdir(os.path.join(stories_root, d))
        ]
        for scan_dir in scan_dirs:
            for fname in os.listdir(scan_dir) if os.path.isdir(scan_dir) else []:
                if not fname.endswith(".json"):
                    continue
                try:
                    with open(os.path.join(scan_dir, fname), "r", encoding="utf-8") as f:
                        d = json.load(f)
                    cfg = d[0] if isinstance(d, list) else d
                    t = (cfg.get("target_url") or "").strip().lower()
                    if t:
                        status = cfg.get("status", "").upper()
                        is_live = "LIVE" in status or len(cfg.get("rkeys", [])) > 0 or len(cfg.get("post_urls", [])) > 0
                        if is_live:
                            rkey = t.strip("/").split("/")[-1].split("?")[0].split("#")[0].strip()
                            if rkey:
                                _REPLIED_TARGETS.add(rkey)
                except Exception:
                    continue
        print(f"Loaded {len(_REPLIED_TARGETS)} existing reply target rkeys for duplicate check.")
    
    target_rkey = target_url.strip().lower().strip("/").split("/")[-1].split("?")[0].split("#")[0].strip()
    return target_rkey in _REPLIED_TARGETS

def save_and_sync_story(thread_config, write_json=True):
    """Saves the thread config as an individual JSON and updates the registry in the bluesky_bot/ folder."""
    subject = thread_config.get("subject", "assessment")
    story_id = thread_config.get("id") or subject.lower().replace(" ", "_").replace("/", "_")
    # Sanitize story_id to remove forbidden characters for Windows paths
    for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
        story_id = story_id.replace(char, '')
    thread_config["id"] = story_id
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths in bluesky_bot/
    bot_stories_dir = os.path.join(script_dir, "stories")
    bot_registry_path = os.path.join(script_dir, "stories_registry.js")
    
    status = thread_config.get("status", "").upper()
    is_live = "LIVE" in status or len(thread_config.get("rkeys", [])) > 0 or len(thread_config.get("post_urls", [])) > 0

    # Keep the duplicate-reply cache current within this process.
    _t = (thread_config.get("target_url") or "").strip().lower()
    if _t and _REPLIED_TARGETS is not None:
        _REPLIED_TARGETS.add(_t)

    # Save individual JSON files to bot directory
    s_dir = bot_stories_dir
    target_dir = os.path.join(s_dir, "live") if is_live else s_dir
    os.makedirs(target_dir, exist_ok=True)
    filename = f"factcheck_{story_id}.json"
    filepath = os.path.join(target_dir, filename)
    if write_json:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([thread_config], f, indent=2, ensure_ascii=False)
            print(f"Saved JSON config to {filepath}")
            
            # If we are writing to live, remove the draft file from the parent directory if it exists
            if is_live:
                draft_path = os.path.join(s_dir, filename)
                if os.path.exists(draft_path):
                    os.remove(draft_path)
                    print(f"Cleaned up draft file: {draft_path}")
        except Exception as e:
            print(f"Warning: Failed to save JSON file to {filepath}: {e}")
        
    # Clean up draft index if we moved to live
    if is_live:
        draft_index_path = os.path.join(s_dir, "index.json")
        if os.path.exists(draft_index_path):
            try:
                with open(draft_index_path, "r", encoding="utf-8") as f:
                    draft_index_data = json.load(f)
                if filename in draft_index_data:
                    draft_index_data.remove(filename)
                    with open(draft_index_path, "w", encoding="utf-8") as f:
                        json.dump(draft_index_data, f, indent=2, ensure_ascii=False)
                    print(f"Removed {filename} from draft index.json at {draft_index_path}")
            except Exception as e:
                print(f"Warning: Failed to update draft index.json: {e}")
        
    # Update index.json
    index_path = os.path.join(target_dir, "index.json")
    try:
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                index_data = json.load(f)
        else:
            index_data = []
        
        # Check if this filename is already in index.json, if not add it
        if filename not in index_data:
            index_data.append(filename)
            with open(index_path, "w", encoding="utf-8") as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            print(f"Updated index.json at {index_path}")
    except Exception as e:
        print(f"Warning: Failed to update index.json at {index_path}: {e}")

    # Rebuild registries using the single source of truth compiler
    try:
        from rebuild_registries import rebuild_registries
        rebuild_registries()
    except Exception as e:
        print(f"Warning: Failed to rebuild registries: {e}")

def resolve_facets_and_tags(text, link=None):
    """Parses text for hashtags and links, returning facets list and tags list."""
    facets = []
    tags_list = []
    
    # 1. Resolve Link facet if link is provided and exists in text
    if link:
        text_bytes = text.encode('utf-8')
        link_bytes = link.encode('utf-8')
        byte_start = text_bytes.find(link_bytes)
        if byte_start != -1:
            byte_end = byte_start + len(link_bytes)
            facets.append(
                models.AppBskyRichtextFacet.Main(
                    features=[models.AppBskyRichtextFacet.Link(uri=link)],
                    index=models.AppBskyRichtextFacet.ByteSlice(byte_end=byte_end, byte_start=byte_start)
                )
            )

    # 2. Parse #hashtags and build Tag facets and tags list
    for match in re.finditer(r'#(\w+)', text):
        tag = match.group(1)
        tags_list.append(tag)
        byte_start = len(text[:match.start()].encode('utf-8'))
        byte_end = len(text[:match.end()].encode('utf-8'))
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Tag(tag=tag)],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_start=byte_start, byte_end=byte_end)
            )
        )
        
    # Cap tags list at 8 items as per lexicon schema limits
    tags_list = tags_list[:8]
    
    # Sort facets by byteStart as required by AT Protocol
    facets.sort(key=lambda f: f.index.byte_start)
    
    return (facets if facets else None), (tags_list if tags_list else None)

def post_thread(client, thread_config, live=False, compact=False):
    """Processes a single thread configuration (generating graph, validating, and posting)."""
    subject = thread_config.get("subject", "Assessment")
    posts = thread_config.get("posts", [])
    link = thread_config.get("link", "")
    claim_u = thread_config.get("claim_u", 0.0)
    claim_psi = thread_config.get("claim_psi", 0.0)
    real_u = thread_config.get("real_u", 0.0)
    real_psi = thread_config.get("real_psi", 0.0)
    mode = thread_config.get("mode", "root").lower()
    target_url = thread_config.get("target_url", "")

    print(f"\n==================================================")
    print(f"PROCESSING SUBJECT: {subject}")
    print(f"Mode: {mode.upper()}")
    print(f"==================================================")

    # 1. Split posts dynamically and validate
    print("Performing dynamic splitting and pre-flight size validation...")
    if not posts:
        raise ValueError("Thread configuration contains no posts.")
        
    is_compact_single = thread_config.get("compact") == "single" or compact == "single"
    is_compact_thread = thread_config.get("compact") is True or compact is True
    is_compact = is_compact_single or is_compact_thread

    if is_compact_single:
        final_posts = posts[:1]
        if link:
            ref_suffix = f"\n\nReference: {link}"
            if len(final_posts[0]) + len(ref_suffix) <= 299:
                final_posts[0] += ref_suffix
            else:
                ref_suffix = f"\n\n{link}"
                if len(final_posts[0]) + len(ref_suffix) <= 299:
                    final_posts[0] += ref_suffix
    elif is_compact_thread:
        final_posts = posts[:4]
    else:
        final_posts = pack_posts(posts, max_len=299)
        
    for idx, post in enumerate(final_posts, 1):
        if len(post) > 299:
            raise ValueError(f"Post {idx} exceeds 299 characters ({len(post)} chars) after splitting:\n{post}")
    print(f"All posts successfully split and validated. Thread post count: {len(final_posts)}")

    # 2. Graph Check (No generation in posting script)
    # Ensure graph_png/ folder exists in workspace
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bot_graph_dir = os.path.join(script_dir, "graph_png")
    os.makedirs(bot_graph_dir, exist_ok=True)
    
    story_id = thread_config.get("id") or subject.lower().replace(" ", "_").replace("/", "_")
    # Sanitize story_id to remove forbidden characters for Windows paths
    for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
        story_id = story_id.replace(char, '')
    thread_config["id"] = story_id

    graph_base_filename = f"{story_id}_graph.png"
    graph_filename = os.path.join(bot_graph_dir, graph_base_filename)
    
    # Verify the graph already exists. We do not generate graphs in the posting script.
    if os.path.exists(graph_filename):
        print(f"Using existing pre-generated trajectory graph: {graph_filename}")
        thread_config["graph_img"] = f"graph_png/{graph_base_filename}"
    else:
        raise FileNotFoundError(f"Required trajectory graph image not found: {graph_filename}. Graphs must be pre-generated.")

    post_rkeys = []
    post_uris = []

    if target_url:
        if _target_already_replied(target_url):
            print(f"SKIP: Already have a story for this target post ({target_url}). Skipping.")
            raise RuntimeError("ALREADY_REPLIED")

    if not live:
        print("\n--- DRY-RUN OUTPUT (No posts sent to Bluesky) ---")
        for idx, post in enumerate(final_posts, 1):
            embed_info = ""
            if idx == 1:
                if is_compact_single:
                    embed_info = " [Embed: Trajectory Graph & Compact Summary Card]"
                else:
                    embed_info = " [Embed: Trajectory Graph]"
            elif idx == 2 and link:
                embed_info = f" [Embed: Link Card -> {link}]"
            elif idx == 4 and is_compact_thread:
                embed_info = f" [Embed: Compact Summary Card]"
            elif "Source: " in post and thread_config.get("grounding_url"):
                embed_info = f" [Embed: Grounding Card -> {thread_config.get('grounding_url')}]"
            print(f"\n[Post {idx}/{len(final_posts)}]{embed_info} ({len(post)} chars):\n{post}")
        thread_config["status"] = "COMPLETED DRY RUN"
    else:
        # --- LIVE POSTING CORE ---
        try:
            # 3. Upload Graph Image
            print("Uploading trajectory graph to Bluesky...")
            try:
                with open(graph_filename, "rb") as f:
                    img_data = f.read()
                upload = client.com.atproto.repo.upload_blob(img_data)
                images = [models.AppBskyEmbedImages.Image(alt=f"Alethekanon Psochic Hegemony Assessment Graph for {subject}", image=upload.blob)]
                graph_embed = models.AppBskyEmbedImages.Main(images=images)
                print("Graph uploaded successfully.")
            except Exception as e:
                raise RuntimeError(f"Failed to upload graph: {e}") from e

            # Create Compact Mode Info Card Embed
            info_card_embed = None
            if is_compact:
                info_card_filename = os.path.join(bot_graph_dir, f"{story_id}_info_card.png")
                if not os.path.exists(info_card_filename):
                    print(f"Compact mode info card not found at {info_card_filename}. Generating on-the-fly...")
                    try:
                        from image_card_generator import generate_compact_info_card
                        generate_compact_info_card(thread_config, info_card_filename)
                    except Exception as e:
                        raise RuntimeError(f"Failed to generate compact info card on-the-fly: {e}") from e
                print("Uploading compact summary info card to Bluesky...")
                try:
                    with open(info_card_filename, "rb") as f:
                        card_img_data = f.read()
                    card_upload = client.com.atproto.repo.upload_blob(card_img_data)
                    
                    # Construct alt text containing details of posts 4 to 12
                    alt_parts = [
                        "Aletheia Assessment Summary Details:",
                        f"Context: {posts[4].replace('What\'s happening:\\n', '').replace('Context:\\n', '').strip()}",
                        f"Nuance: {posts[5]}",
                        f"Breakdown: {posts[6]}",
                        f"Social Physics: {posts[7]}",
                        f"Trajectory: {posts[8]}",
                        f"The Unavoidables: {posts[9]}",
                        f"Alethekanon: {posts[10]}",
                        f"Awwthekanon: {posts[11]}",
                        f"Brothekanon: {posts[12]}"
                    ]
                    card_alt = "\n\n".join(alt_parts)
                    if len(card_alt) > 9900:
                        card_alt = card_alt[:9897] + "..."
                        
                    card_images = [models.AppBskyEmbedImages.Image(alt=card_alt, image=card_upload.blob)]
                    info_card_embed = models.AppBskyEmbedImages.Main(images=card_images)
                    print("Compact summary info card uploaded successfully.")
                except Exception as e:
                    raise RuntimeError(f"Failed to upload compact info card: {e}") from e

            # Create External Link Preview Card
            link_embed = None
            if link:
                try:
                    desc_text = ""
                    if len(final_posts) > 4:
                        desc_text = final_posts[4].replace("What's happening:\n", "").strip()
                    else:
                        desc_text = f"Alethekanon Psochic Hegemony Assessment for {subject}"
                    if len(desc_text) > 200:
                        desc_text = desc_text[:197] + "..."
                    link_embed = models.AppBskyEmbedExternal.Main(
                        external=models.AppBskyEmbedExternal.External(
                            title=subject,
                            description=desc_text,
                            uri=link
                        )
                    )
                    print(f"Created link preview card embed for: {link}")
                except Exception as ex:
                    print(f"Warning: Failed to create external link embed card: {ex}")

            # Create Grounding Link Preview Card (if grounding_url is present)
            grounding_url = thread_config.get("grounding_url", "")
            grounding_embed = None
            if grounding_url:
                try:
                    desc_text = f"Fact-check verification source for {subject}"
                    grounding_embed = models.AppBskyEmbedExternal.Main(
                        external=models.AppBskyEmbedExternal.External(
                            title="Verification Source | Aletheia Bot",
                            description=desc_text,
                            uri=grounding_url
                        )
                    )
                    print(f"Created grounding link preview card embed for: {grounding_url}")
                except Exception as ex:
                    print(f"Warning: Failed to create grounding external link embed card: {ex}")

            # first_post_embed gets the trajectory graph, and in compact-single mode, also gets the summary card
            first_post_embed = graph_embed
            if is_compact_single and info_card_embed is not None:
                joint_images = []
                if graph_embed is not None and hasattr(graph_embed, "images"):
                    joint_images.extend(graph_embed.images)
                if info_card_embed is not None and hasattr(info_card_embed, "images"):
                    joint_images.extend(info_card_embed.images)
                first_post_embed = models.AppBskyEmbedImages.Main(images=joint_images)

            # 4. Resolve Links and Hashtags for facets (only on the first/root post)
            facets, tags_list = resolve_facets_and_tags(final_posts[0], link=link)

            # 5. Determine Posting References based on Mode
            is_reply = False
            # Commented out reply-to-user logic to avoid spam/ban issues. We always post to our feed/timeline.
            # if mode == "reply":
            #     print(f"Resolving target post: {target_url}...")
            #     try:
            #         target_handle, rkey = parse_bsky_url(target_url)
            #         resolver = IdResolver()
            #         target_did = resolver.handle.resolve(target_handle)
            # 
            #         response = client.com.atproto.repo.get_record(
            #             models.ComAtprotoRepoGetRecord.Params(
            #                 repo=target_did,
            #                 collection='app.bsky.feed.post',
            #                 rkey=rkey
            #             )
            #         )
            #         target_cid = response.cid
            #         target_uri = response.uri
            #         target_record = response.value
            # 
            #         if hasattr(target_record, 'reply') and target_record.reply:
            #             root_ref = target_record.reply.root
            #         else:
            #             root_ref = models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)
            # 
            #         parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)
            # 
            #         print("Resolved target reference correctly.")
            #         is_reply = True
            #     except Exception as e:
            #         print(f"Warning: Failed to resolve reply target ({e}). Falling back to root thread mode on our timeline...")
            #         is_reply = False
            # 
            # if is_reply:
            #     # Post first reply
            #     print("Posting Part 1 (Reply with Link Preview or Graph Embed)...")
            #     try:
            #         reply = client.com.atproto.repo.create_record(
            #             models.ComAtprotoRepoCreateRecord.Data(
            #                 repo=client.me.did,
            #                 collection=models.ids.AppBskyFeedPost,
            #                 record=models.AppBskyFeedPost.Record(
            #                     created_at=client.get_current_time_iso(),
            #                     text=final_posts[0],
            #                     reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref),
            #                     embed=first_post_embed,
            #                     facets=facets,
            #                     tags=tags_list,
            #                     langs=["en"]
            #                 )
            #             )
            #         )
            #         parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=reply.cid, uri=reply.uri)
            #         post_uris.append(reply.uri)
            #         post_rkeys.append(reply.uri.split('/')[-1])
            #     except Exception as e:
            #         raise RuntimeError(f"Failed to post root reply: {e}") from e

            # Root Mode: Post standard new stand-alone post on profile timeline
            print("Posting Part 1 (New Root Thread with Link Preview or Graph Embed)...")
            try:
                root_post = client.com.atproto.repo.create_record(
                    models.ComAtprotoRepoCreateRecord.Data(
                        repo=client.me.did,
                        collection=models.ids.AppBskyFeedPost,
                        record=models.AppBskyFeedPost.Record(
                            created_at=client.get_current_time_iso(),
                            text=final_posts[0],
                            embed=first_post_embed,
                            facets=facets,
                            tags=tags_list,
                            langs=["en"]
                        )
                    )
                )
                root_ref = models.ComAtprotoRepoStrongRef.Main(cid=root_post.cid, uri=root_post.uri)
                parent_ref = root_ref
                post_uris.append(root_post.uri)
                post_rkeys.append(root_post.uri.split('/')[-1])
            except Exception as e:
                raise RuntimeError(f"Failed to post root thread: {e}") from e

            # 6. Post subsequent thread parts sequentially
            for i, text in enumerate(final_posts[1:], start=2):
                print(f"Posting Part {i}/{len(final_posts)}...")
                current_embed = None
                if is_compact and i == 4 and info_card_embed is not None:
                    # Attach the compact summary card image embed to the fourth post of the thread
                    current_embed = info_card_embed
                    print("Attaching compact summary card embed to Part 4...")
                elif i == 2 and link_embed is not None:
                    # Attach the link preview card embed to the second post of the thread
                    current_embed = link_embed
                    print("Attaching link preview card embed to Part 2...")
                elif "Source: " in text and grounding_embed is not None:
                    current_embed = grounding_embed
                    print(f"Attaching grounding link preview card embed to Part {i}...")
                sub_facets, sub_tags = resolve_facets_and_tags(text)
                try:
                    reply = client.com.atproto.repo.create_record(
                        models.ComAtprotoRepoCreateRecord.Data(
                            repo=client.me.did,
                            collection=models.ids.AppBskyFeedPost,
                            record=models.AppBskyFeedPost.Record(
                                created_at=client.get_current_time_iso(),
                                text=text,
                                reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref),
                                embed=current_embed,
                                facets=sub_facets,
                                tags=sub_tags,
                                langs=["en"]
                            )
                        )
                    )
                    parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=reply.cid, uri=reply.uri)
                    post_uris.append(reply.uri)
                    post_rkeys.append(reply.uri.split('/')[-1])
                    time.sleep(1) # Slight pause to ensure strict chronologic ordering in API database
                except Exception as e:
                    raise RuntimeError(f"Failed to post part {i}: {e}") from e

            handle = client.me.handle
            thread_config["rkeys"] = post_rkeys
            thread_config["post_urls"] = [f"https://bsky.app/profile/{handle}/post/{rkey}" for rkey in post_rkeys]
            thread_config["status"] = "LIVE POSTED (judgement-bot.bsky.social)"
            
            # Save parsed tags to the config
            all_tags = []
            for post_text in final_posts:
                _, post_tags = resolve_facets_and_tags(post_text)
                if post_tags:
                    for t in post_tags:
                        if t not in all_tags:
                            all_tags.append(t)
            if all_tags:
                thread_config["tags"] = all_tags
                
            print(f"Thread for '{subject}' successfully posted live to Bluesky!")

        except Exception as e:
            if post_uris:
                print(f"\nERROR ENCOUNTERED during live posting: {e}")
                print(f"Rollback: Deleting {len(post_uris)} partially-posted thread items...")
                for uri in reversed(post_uris):
                    try:
                        client.delete_post(uri)
                        print(f"  Deleted partially-posted post: {uri}")
                    except Exception as del_err:
                        print(f"  Warning: Failed to delete {uri}: {del_err}")
            raise e

    # 7. Save and Sync across directories
    save_and_sync_story(thread_config)

def main():
    parser = argparse.ArgumentParser(description="Unified Aletheia Bot CLI Engine")
    parser.add_argument("--config", required=True, help="Path to the JSON configuration file containing thread details.")
    parser.add_argument("--compact", action="store_true", help="Force compact thread posting mode (posts 1-4 as text, posts 5+ as summary card image)")
    parser.add_argument("--compact-single", action="store_true", help="Force compact single-post mode (only post 1 with graph and card images)")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Run in validation and dry-run mode (local graph, console logging).")
    group.add_argument("--live", action="store_true", help="Post the threads live on Bluesky timeline/replies.")

    args = parser.parse_args()

    # Load thread configuration
    if not os.path.exists(args.config):
        print(f"ERROR: Configuration file not found at '{args.config}'")
        sys.exit(1)

    try:
        with open(args.config, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse JSON configuration file: {e}")
        sys.exit(1)

    # Standardize data to a list of thread objects
    if isinstance(data, dict):
        threads = [data]
    elif isinstance(data, list):
        threads = data
    else:
        print("ERROR: Config file must be a JSON object or a list of JSON objects.")
        sys.exit(1)

    client = None
    if args.live:
        handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
        password = os.environ.get('BSKY_PASSWORD')
        if not password:
            print("ERROR: BSKY_PASSWORD environment variable not found in .env. Cannot post live.")
            sys.exit(1)

        print(f"Authenticating with Bluesky as {handle}...")
        try:
            client = Client()
            client.login(handle, password)
            print("Authentication successful!")
        except Exception as e:
            print(f"Authentication failed: {e}")
            sys.exit(1)

    compact_val = False
    if args.compact_single:
        compact_val = "single"
    elif args.compact:
        compact_val = True

    # Process all threads
    for thread in threads:
        try:
            post_thread(client, thread, live=args.live, compact=compact_val)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)

    try:
        print("\nRebuilding registries to update live and drafts counts...")
        from rebuild_registries import rebuild_registries
        rebuild_registries()
    except Exception as e:
        print(f"Warning: Failed to rebuild registries: {e}")

    print("\nAll threads processed successfully!")

if __name__ == "__main__":
    main()
