#!/usr/bin/env python3
"""
Aletheia Retraction & Errata CLI Tool

Usage:
  python bluesky_bot/retract_story.py --story-id dems_flips_iowa_senate_thune_vow --reason "Original audit conflated partisan social media rhetoric with objective voting participation; corrected trajectory to reflect democratic process." --new-real-u 0.2 --new-real-psi 0.2
"""

import os
import sys
import json
import argparse
import datetime
import re

# Ensure UTF-8 output encoding on Windows
if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from generate_graph import get_path_name, enforce_deterministic_trajectory

def find_story_file(story_id):
    candidates = [
        os.path.join(script_dir, "stories", "live", f"factcheck_{story_id}.json"),
        os.path.join(script_dir, "stories", f"factcheck_{story_id}.json"),
        os.path.join(script_dir, "stories", "quarantine", f"factcheck_{story_id}.json"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def retract_or_amend_story(story_id, reason, new_coords=None, live=False, mark_retracted=False):
    filepath = find_story_file(story_id)
    if not filepath:
        print(f"ERROR: Could not find story JSON file for '{story_id}'.")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    story = data[0] if isinstance(data, list) and len(data) > 0 else data

    old_claim_u = story.get("claim_u", 0.0)
    old_claim_psi = story.get("claim_psi", 0.0)
    old_real_u = story.get("real_u", 0.0)
    old_real_psi = story.get("real_psi", 0.0)

    print(f"Target Story: '{story.get('subject')}' ({story_id})")
    print(f"Current Coords: Claim=({old_claim_u}, {old_claim_psi}), Real=({old_real_u}, {old_real_psi})")
    print(f"Current Status: {story.get('status')}")

    status_label = "RETRACTED" if mark_retracted else "AMENDED"

    if new_coords:
        if "claim_u" in new_coords:
            story["claim_u"] = float(new_coords["claim_u"])
        if "claim_psi" in new_coords:
            story["claim_psi"] = float(new_coords["claim_psi"])
        if "real_u" in new_coords:
            story["real_u"] = float(new_coords["real_u"])
        if "real_psi" in new_coords:
            story["real_psi"] = float(new_coords["real_psi"])

        print(f"Updated Coords: Claim=({story['claim_u']}, {story['claim_psi']}), Real=({story['real_u']}, {story['real_psi']})")

    # Recalculate deterministic trajectory
    story = enforce_deterministic_trajectory(story)

    # Record retraction / amendment metadata
    story["status"] = f"{status_label} (Aletheia Editorial Audit)"
    story["retraction"] = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "type": status_label,
        "reason": reason,
        "previous_coords": {
            "claim": [old_claim_u, old_claim_psi],
            "real": [old_real_u, old_real_psi]
        },
        "new_coords": {
            "claim": [story["claim_u"], story["claim_psi"]],
            "real": [story["real_u"], story["real_psi"]]
        }
    }

    # Prepend Errata Notice to Post 0
    posts = story.get("posts", [])
    if posts:
        errata_prefix = f"[{status_label} / CORRECTION]\n"
        if not posts[0].startswith(f"[{status_label}"):
            posts[0] = errata_prefix + posts[0]
            if len(posts[0]) > 300:
                posts[0] = posts[0][:297] + "..."
    story["posts"] = posts

    # Save updated story JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([story], f, indent=2, ensure_ascii=False)
    print(f"Updated story saved to: {filepath}")

    # Post Errata reply to live Bluesky thread if requested
    if live:
        handle = os.environ.get("BSKY_HANDLE", "judgement-bot.bsky.social")
        password = os.environ.get("BSKY_PASSWORD")
        if not password:
            print("Warning: BSKY_PASSWORD not set. Skipping live Bluesky reply.")
        else:
            try:
                from atproto import Client, models
                client = Client()
                client.login(handle, password)

                target_post_url = story.get("target_url") or story.get("link")
                print(f"Connecting to Bluesky to post errata reply under target post...")
                # Compose concise errata post
                math_path = get_path_name(story["claim_u"], story["claim_psi"], story["real_u"], story["real_psi"])
                errata_text = (
                    f"[{status_label} AUDIT]\n"
                    f"Reason: {reason}\n"
                    f"Corrected Judgement: ({story['real_u']:+.1f}, {story['real_psi']:+.1f}) — {math_path}\n"
                    f"#Aletheia #Errata"
                )
                if len(errata_text) > 300:
                    errata_text = errata_text[:297] + "..."

                # Post to Bluesky as a threaded reply
                parent_ref = None
                root_ref = None

                # 1. Try to thread under the story's first posted post (rkeys[0])
                rkeys = story.get("rkeys") or []
                if rkeys and len(rkeys) > 0:
                    first_rkey = rkeys[0]
                    try:
                        res_post = client.com.atproto.repo.get_record(
                            models.ComAtprotoRepoGetRecord.Params(
                                repo=client.me.did,
                                collection='app.bsky.feed.post',
                                rkey=first_rkey
                            )
                        )
                        target_cid = res_post.cid
                        target_uri = res_post.uri
                        target_rec = res_post.value
                        root_ref = target_rec.reply.root if (hasattr(target_rec, 'reply') and target_rec.reply) else models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)
                        parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)
                    except Exception as rk_err:
                        print(f"Notice: Could not resolve rkey '{first_rkey}' on bot profile: {rk_err}")

                # 2. Fall back to target_url if rkeys[0] didn't resolve
                if not parent_ref and target_post_url:
                    try:
                        from atproto import IdResolver
                        parts = target_post_url.strip("/").split("/")
                        if "profile" in parts and "post" in parts:
                            author_handle = parts[parts.index("profile") + 1]
                            rkey = parts[parts.index("post") + 1].split("?")[0].split("#")[0]
                            resolver = IdResolver()
                            did = resolver.handle.resolve(author_handle)
                            res_post = client.com.atproto.repo.get_record(
                                models.ComAtprotoRepoGetRecord.Params(
                                    repo=did,
                                    collection='app.bsky.feed.post',
                                    rkey=rkey
                                )
                            )
                            target_cid = res_post.cid
                            target_uri = res_post.uri
                            target_rec = res_post.value
                            root_ref = target_rec.reply.root if (hasattr(target_rec, 'reply') and target_rec.reply) else models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)
                            parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=target_cid, uri=target_uri)
                    except Exception as url_err:
                        print(f"Notice: Could not resolve target URL '{target_post_url}': {url_err}")

                if parent_ref and root_ref:
                    reply_ref = models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref)
                    reply_rec = models.AppBskyFeedPost.Record(
                        created_at=client.get_current_time_iso(),
                        text=errata_text,
                        reply=reply_ref
                    )
                    post_res = client.com.atproto.repo.create_record(
                        models.ComAtprotoRepoCreateRecord.Data(
                            repo=client.me.did,
                            collection='app.bsky.feed.post',
                            record=reply_rec
                        )
                    )
                    print(f"Live errata reply posted successfully as thread: {post_res.uri}")
                else:
                    print("Warning: Could not resolve thread parent; posting errata as fallback top-level post...")
                    post_res = client.send_post(text=errata_text)
                    print(f"Live errata posted successfully: {post_res.uri}")
            except Exception as bsky_err:
                print(f"Warning: Failed to post live errata to Bluesky: {bsky_err}")

    # Rebuild registries to re-generate graph and update registry index
    try:
        from rebuild_registries_son import rebuild_registries
        rebuild_registries()
        print("Registries successfully rebuilt.")
    except Exception as re_err:
        print(f"Warning: Failed to rebuild registries: {re_err}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Aletheia Story Retraction & Errata CLI")
    parser.add_argument("--story-id", required=True, help="Story slug ID (e.g. dems_flips_iowa_senate_thune_vow)")
    parser.add_argument("--reason", required=True, help="Detailed reason for retraction or amendment")
    parser.add_argument("--retract", action="store_true", help="Mark as fully RETRACTED instead of AMENDED")
    parser.add_argument("--new-claim-u", type=float, help="Revised claim u coordinate")
    parser.add_argument("--new-claim-psi", type=float, help="Revised claim psi coordinate")
    parser.add_argument("--new-real-u", type=float, help="Revised real u coordinate")
    parser.add_argument("--new-real-psi", type=float, help="Revised real psi coordinate")
    parser.add_argument("--live", action="store_true", help="Post an errata reply directly to Bluesky")

    args = parser.parse_args()

    new_coords = {}
    if args.new_claim_u is not None:
        new_coords["claim_u"] = args.new_claim_u
    if args.new_claim_psi is not None:
        new_coords["claim_psi"] = args.new_claim_psi
    if args.new_real_u is not None:
        new_coords["real_u"] = args.new_real_u
    if args.new_real_psi is not None:
        new_coords["real_psi"] = args.new_real_psi

    success = retract_or_amend_story(
        story_id=args.story_id,
        reason=args.reason,
        new_coords=new_coords if new_coords else None,
        live=args.live,
        mark_retracted=args.retract
    )

    if success:
        print("\nRetraction / amendment pipeline completed successfully.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
