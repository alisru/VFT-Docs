import os
import sys
import json
import argparse
import time
from dotenv import load_dotenv
from atproto import Client, models, IdResolver
from generate_graph import draw_graph
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

def split_text(text, max_len=300):
    """Splits text dynamically at the last newline or space before max_len.
    Avoids orphaning short header lines (e.g. 'Brothekanon:') by only
    splitting at a newline if the chunk before it is at least 80 chars.
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

        if split_idx == -1:
            split_idx = max_len

        chunks.append(text[:split_idx].strip())
        text = text[split_idx:].strip()

    return chunks

def save_and_sync_story(thread_config):
    """Saves the thread config as an individual JSON and updates the registry in both workspace folders."""
    subject = thread_config.get("subject", "assessment")
    story_id = thread_config.get("id") or subject.lower().replace(" ", "_").replace("/", "_")
    thread_config["id"] = story_id
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    # Paths in bluesky_bot/
    bot_stories_dir = os.path.join(script_dir, "stories")
    bot_registry_path = os.path.join(script_dir, "stories_registry.js")
    
    # Paths in _Generated_Content/
    gen_stories_dir = os.path.join(root_dir, "_Generated_Content", "stories")
    gen_registry_path = os.path.join(root_dir, "_Generated_Content", "stories_registry.js")
    
    status = thread_config.get("status", "").upper()
    is_live = "LIVE" in status or len(thread_config.get("rkeys", [])) > 0 or len(thread_config.get("post_urls", [])) > 0
    
    # Save individual JSON files to both directories
    for s_dir in [bot_stories_dir, gen_stories_dir]:
        target_dir = os.path.join(s_dir, "live") if is_live else s_dir
        os.makedirs(target_dir, exist_ok=True)
        filename = f"factcheck_{story_id}.json"
        filepath = os.path.join(target_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([thread_config], f, indent=2, ensure_ascii=False)
            print(f"Saved JSON config to {filepath}")
        except Exception as e:
            print(f"Warning: Failed to save JSON file to {filepath}: {e}")
            
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

    # Update stories_registry.js in both directories
    for r_path in [bot_registry_path, gen_registry_path]:
        try:
            if not os.path.exists(r_path):
                registry_data = []
            else:
                with open(r_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                
                prefix = "window.ALETHEIA_STORIES_REGISTRY = "
                suffix = ";"
                if content.startswith(prefix):
                    json_str = content[len(prefix):]
                    if json_str.endswith(suffix):
                        json_str = json_str[:-len(suffix)]
                    registry_data = json.loads(json_str)
                else:
                    registry_data = []
            
            # Ensure graph_img path points into graph_png/ folder
            graph_img = thread_config.get("graph_img") or f"{story_id}_graph.png"
            if graph_img and not graph_img.startswith("graph_png/"):
                graph_img = f"graph_png/{graph_img}"
                
            # Formulate the updated registry element
            registry_story = {
                "id": story_id,
                "subject": thread_config.get("subject"),
                "link": thread_config.get("link"),
                "claim_u": thread_config.get("claim_u"),
                "claim_psi": thread_config.get("claim_psi"),
                "real_u": thread_config.get("real_u"),
                "real_psi": thread_config.get("real_psi"),
                "mode": thread_config.get("mode", "root"),
                "status": thread_config.get("status", "COMPLETED DRY RUN"),
                "verdict": thread_config.get("verdict") or (thread_config.get("posts", ["", "", "", ""])[3].replace("Verdict: ", "") if len(thread_config.get("posts", [])) > 3 else "FAIL — The Path of Deception"),
                "graph_img": graph_img,
                "posts": thread_config.get("posts")
            }
            if "target_url" in thread_config:
                registry_story["target_url"] = thread_config["target_url"]
            if "rkeys" in thread_config:
                registry_story["rkeys"] = thread_config["rkeys"]
            if "post_urls" in thread_config:
                registry_story["post_urls"] = thread_config["post_urls"]
                
            # Update or insert
            found_idx = -1
            for idx, item in enumerate(registry_data):
                if item.get("subject") == registry_story["subject"] or item.get("id") == registry_story["id"]:
                    found_idx = idx
                    break
                    
            if found_idx != -1:
                for k, v in registry_story.items():
                    registry_data[found_idx][k] = v
            else:
                registry_data.insert(0, registry_story)
                
            # Write back JS file
            new_content = f"window.ALETHEIA_STORIES_REGISTRY = {json.dumps(registry_data, indent=2, ensure_ascii=False)};\n"
            with open(r_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated stories_registry.js at {r_path}")
        except Exception as e:
            print(f"Warning: Failed to update stories_registry.js at {r_path}: {e}")

def post_thread(client, thread_config, live=False):
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
    final_posts = []
    for post in posts:
        final_posts.extend(split_text(post))
        
    for idx, post in enumerate(final_posts, 1):
        if len(post) > 300:
            raise ValueError(f"Post {idx} exceeds 300 characters ({len(post)} chars) after splitting:\n{post}")
    print(f"All posts successfully split and validated. Thread post count: {len(final_posts)}")

    # 2. Graph Generation
    # Ensure graph_png/ folder exists in workspace
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bot_graph_dir = os.path.join(script_dir, "graph_png")
    os.makedirs(bot_graph_dir, exist_ok=True)
    
    graph_base_filename = f"{subject.lower().replace(' ', '_').replace('/', '_')}_graph.png"
    graph_filename = os.path.join(bot_graph_dir, graph_base_filename)
    
    print(f"Generating trajectory graph: {graph_filename}...")
    try:
        draw_graph(claim_u, claim_psi, real_u, real_psi, f"Assessment: {subject}", graph_filename)
        print("Graph generated successfully.")
        
        # Sync graph image to _Generated_Content/graph_png/
        root_dir = os.path.dirname(script_dir)
        gen_graph_dir = os.path.join(root_dir, "_Generated_Content", "graph_png")
        os.makedirs(gen_graph_dir, exist_ok=True)
        shutil.copy2(graph_filename, os.path.join(gen_graph_dir, graph_base_filename))
        print("Graph image synchronized to _Generated_Content/graph_png/")
        
        # Keep config graph_img updated
        thread_config["graph_img"] = f"graph_png/{graph_base_filename}"
    except Exception as e:
        raise RuntimeError(f"Failed to generate trajectory graph: {e}") from e

    post_rkeys = []

    if not live:
        print("\n--- DRY-RUN OUTPUT (No posts sent to Bluesky) ---")
        for idx, post in enumerate(final_posts, 1):
            embed_info = ""
            if idx == 1:
                embed_info = f" [Embed: Trajectory Graph]"
            elif idx == 2 and link:
                embed_info = f" [Embed: Link Card -> {link}]"
            print(f"\n[Post {idx}/{len(final_posts)}]{embed_info} ({len(post)} chars):\n{post}")
        print("\nTrajectory graph generated locally. Live posting skipped because --live was not set.")
        thread_config["status"] = "COMPLETED DRY RUN"
    else:
        # --- LIVE POSTING CORE ---
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

        # first_post_embed always gets the trajectory graph_embed
        first_post_embed = graph_embed

        # 4. Resolve Links for facets (only on the first/root post)
        facets = []
        if link:
            text_bytes = final_posts[0].encode('utf-8')
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

        # 5. Determine Posting References based on Mode
        is_reply = False
        if mode == "reply":
            if not target_url:
                raise ValueError("target_url is required when mode is 'reply'.")

            print(f"Resolving target post: {target_url}...")
            try:
                target_handle, rkey = parse_bsky_url(target_url)
                resolver = IdResolver()
                target_did = resolver.handle.resolve(target_handle)

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
                print("Resolved target reference correctly.")
                is_reply = True
            except Exception as e:
                print(f"Warning: Failed to resolve reply target ({e}). Falling back to root thread mode on our timeline...")
                is_reply = False

        if is_reply:
            # Post first reply
            print("Posting Part 1 (Reply with Link Preview or Graph Embed)...")
            try:
                reply = client.com.atproto.repo.create_record(
                    models.ComAtprotoRepoCreateRecord.Data(
                        repo=client.me.did,
                        collection=models.ids.AppBskyFeedPost,
                        record=models.AppBskyFeedPost.Record(
                            created_at=client.get_current_time_iso(),
                            text=final_posts[0],
                            reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref),
                            embed=first_post_embed,
                            facets=facets
                        )
                    )
                )
                parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=reply.cid, uri=reply.uri)
                post_rkeys.append(reply.uri.split('/')[-1])
            except Exception as e:
                raise RuntimeError(f"Failed to post root reply: {e}") from e

        else:
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
                            facets=facets
                        )
                    )
                )
                root_ref = models.ComAtprotoRepoStrongRef.Main(cid=root_post.cid, uri=root_post.uri)
                parent_ref = root_ref
                post_rkeys.append(root_post.uri.split('/')[-1])
            except Exception as e:
                raise RuntimeError(f"Failed to post root thread: {e}") from e

        # 6. Post subsequent thread parts sequentially
        for i, text in enumerate(final_posts[1:], start=2):
            print(f"Posting Part {i}/{len(final_posts)}...")
            current_embed = None
            if i == 2 and link_embed is not None:
                # Attach the link preview card embed to the second post of the thread
                current_embed = link_embed
                print("Attaching link preview card embed to Part 2...")
            try:
                reply = client.com.atproto.repo.create_record(
                    models.ComAtprotoRepoCreateRecord.Data(
                        repo=client.me.did,
                        collection=models.ids.AppBskyFeedPost,
                        record=models.AppBskyFeedPost.Record(
                            created_at=client.get_current_time_iso(),
                            text=text,
                            reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref),
                            embed=current_embed
                        )
                    )
                )
                parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=reply.cid, uri=reply.uri)
                post_rkeys.append(reply.uri.split('/')[-1])
                time.sleep(1) # Slight pause to ensure strict chronologic ordering in API database
            except Exception as e:
                raise RuntimeError(f"Failed to post part {i}: {e}") from e

        handle = client.me.handle
        thread_config["rkeys"] = post_rkeys
        thread_config["post_urls"] = [f"https://bsky.app/profile/{handle}/post/{rkey}" for rkey in post_rkeys]
        thread_config["status"] = "LIVE POSTED (judgement-bot.bsky.social)"
        print(f"Thread for '{subject}' successfully posted live to Bluesky!")

    # 7. Save and Sync across directories
    save_and_sync_story(thread_config)

def main():
    parser = argparse.ArgumentParser(description="Unified Aletheia Bot CLI Engine")
    parser.add_argument("--config", required=True, help="Path to the JSON configuration file containing thread details.")
    
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

    # Process all threads
    for thread in threads:
        try:
            post_thread(client, thread, live=args.live)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)

    print("\nAll threads processed successfully!")

if __name__ == "__main__":
    main()
