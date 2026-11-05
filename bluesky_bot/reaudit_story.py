#!/usr/bin/env python3
"""
Aletheia Story Re-Audit & Correction Engine

Re-evaluates an existing story or Bluesky post by:
1. Actively retrieving fresh multi-source search grounding (counter-perspectives + wire sources)
2. Re-running the convergence audit with explicit editorial focus
3. Programmatically enforcing the deterministic trajectory invariant
4. Re-rendering graphs and visual evidence cards
5. Posting a linked Errata reply thread directly under the root Bluesky post (when --live is passed)

Usage:
  python bluesky_bot/reaudit_story.py --target dems_flips_iowa_senate_thune_vow --reason "Initial audit conflated partisan social media rhetoric with objective voting event"
  python bluesky_bot/reaudit_story.py --target "https://bsky.app/profile/judgement-bot.bsky.social/post/3mzjpogathm2h" --reason "Rebalance with wire sources and correct trajectory" --live
"""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('MPLCONFIGDIR', os.path.join(script_dir, '.mpl_cache'))
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

import json
import argparse
import datetime
import urllib.parse
from dotenv import load_dotenv

# Ensure UTF-8 output encoding on Windows
if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
load_dotenv(os.path.join(script_dir, ".env"))

from generate_graph import get_path_name, enforce_deterministic_trajectory
from harvest_candidates import (
    search_counter_sources_tavily,
    get_outlet_bias_family,
    get_outlet_bias,
    scrape_article_content
)

def find_local_story(target):
    target_clean = target.strip()
    # Check if target is a file path
    if os.path.exists(target_clean) and target_clean.endswith(".json"):
        return target_clean

    slug = target_clean
    if "/" in slug:
        slug = slug.rstrip("/").split("/")[-1].split("?")[0]

    # Search in stories/live/, stories/, stories/darkroom/
    candidates = [
        os.path.join(script_dir, "stories", "live", f"factcheck_{slug}.json"),
        os.path.join(script_dir, "stories", "live", f"{slug}.json"),
        os.path.join(script_dir, "stories", f"factcheck_{slug}.json"),
        os.path.join(script_dir, "stories", f"{slug}.json"),
        os.path.join(script_dir, "stories", "darkroom", f"factcheck_{slug}.json"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c

    # Search by target_url matching in stories/live/
    live_dir = os.path.join(script_dir, "stories", "live")
    if os.path.exists(live_dir) and "bsky.app" in target_clean:
        for fname in os.listdir(live_dir):
            if fname.endswith(".json"):
                fpath = os.path.join(live_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    item = data[0] if isinstance(data, list) else data
                    t_url = item.get("target_url") or ""
                    link = item.get("link") or ""
                    if slug in t_url or slug in link:
                        return fpath
                except Exception:
                    pass

    return None

def resolve_bsky_post(post_url):
    from atproto import Client, IdResolver
    handle = os.environ.get("BSKY_HANDLE", "judgement-bot.bsky.social")
    password = os.environ.get("BSKY_PASSWORD")
    
    parts = post_url.strip("/").split("/")
    author_handle = parts[parts.index("profile") + 1]
    rkey = parts[parts.index("post") + 1].split("?")[0]

    resolver = IdResolver()
    did = resolver.handle.resolve(author_handle)

    client = Client()
    if password:
        client.login(handle, password)

    from atproto import models
    res = client.com.atproto.repo.get_record(
        models.ComAtprotoRepoGetRecord.Params(
            repo=did,
            collection='app.bsky.feed.post',
            rkey=rkey
        )
    )
    return {
        "did": did,
        "rkey": rkey,
        "uri": res.uri,
        "cid": res.cid,
        "record": res.value,
        "text": getattr(res.value, "text", ""),
        "created_at": getattr(res.value, "created_at", None)
    }

def run_reaudit(target, reason="", model="gemini-3.8-flash", use_son=True, use_potential=False, live=False):
    print(f"\n=======================================================")
    print(f"🔄 ALETHEIA RE-AUDIT & CORRECTION DISPATCHER")
    print(f"=======================================================")
    print(f"Target: {target}")
    print(f"Editorial Correction Focus: {reason or 'General multi-source balance'}")
    print(f"Mode: {'SON (6-Attractor)' if use_son else 'Standard'}")
    print(f"Generative Model: {model}")
    print(f"Live Bluesky Reply: {'YES (LIVE POSTING)' if live else 'NO (DRY RUN)'}")
    print(f"-------------------------------------------------------\n")

    local_path = find_local_story(target)
    story_data = None
    target_bsky_info = None

    if local_path:
        print(f"Found local story record: {local_path}")
        with open(local_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        story_data = raw[0] if isinstance(raw, list) and len(raw) > 0 else raw
    elif "bsky.app" in target:
        print(f"Resolving live Bluesky post from AT Protocol...")
        try:
            target_bsky_info = resolve_bsky_post(target)
            print(f"Resolved Bluesky post URI: {target_bsky_info['uri']}")
        except Exception as ex:
            print(f"ERROR: Could not resolve Bluesky post ({ex}).")
            return False
    else:
        print(f"ERROR: Could not locate story or post for '{target}'.")
        return False

    # 1. Determine Subject, Primary Link, and Target URL
    if story_data:
        subject = story_data.get("subject") or story_data.get("id")
        primary_link = story_data.get("link") or ""
        target_post_url = story_data.get("target_url") or target if "bsky.app" in target else story_data.get("target_url", "")
        slug = story_data.get("id") or "reaudit_story"
    else:
        text = target_bsky_info.get("text", "")
        subject = text[:60].strip() + "..."
        primary_link = ""
        target_post_url = target
        slug = f"bsky_post_{target_bsky_info['rkey']}"

    print(f"\n[1/5] Target Subject: '{subject}'")
    print(f"Primary Link: {primary_link or '(none)'}")
    print(f"Target Post URL: {target_post_url or '(none)'}")

    # 2. Multi-Source Active Perspective Search
    print(f"\n[2/5] Running Active Counter-Perspective Search via Tavily/Exa...")
    host = ""
    if primary_link:
        try:
            host = urllib.parse.urlparse(primary_link).hostname or ""
            if host.startswith("www."):
                host = host[4:]
        except Exception:
            pass
    primary_bias = get_outlet_bias_family(host)

    counter_sources = search_counter_sources_tavily(
        title=subject,
        primary_url=primary_link,
        primary_bias_family=primary_bias,
        max_results=5
    )
    print(f"Retrieved {len(counter_sources)} balanced counter/wire source(s).")

    # Scrape primary link if missing
    dossier_entries = []
    if primary_link:
        _, _, p_body = scrape_article_content(primary_link)
        if p_body and not p_body.startswith("Error"):
            clean_p = p_body.strip()[:2500]
            dossier_entries.append(f"[Source 1 (Primary) — {host} (Bias: {get_outlet_bias(host)})] (URL: {primary_link}):\n{clean_p}")

    for idx, cs in enumerate(counter_sources, len(dossier_entries) + 1):
        cs_pub = cs.get("publisher", "")
        cs_url = cs.get("url", "")
        cs_bias = cs.get("editorial_bias", "")
        cs_text = cs.get("snippet", "")
        # Scrape full text if snippet is short
        _, _, s_body = scrape_article_content(cs_url)
        if s_body and not s_body.startswith("Error") and len(s_body.strip()) > len(cs_text):
            cs_text = s_body.strip()[:1500]
        else:
            cs_text = cs_text[:1200]
        dossier_entries.append(f"[Source {idx} — {cs_pub} (Bias: {cs_bias})] (URL: {cs_url}):\n{cs_text}")

    cross_source_dossier = "\n\n".join(dossier_entries)
    print(f"Compiled balanced cross-source dossier with {len(dossier_entries)} perspectives.")

    # 3. Build Re-Audit Candidate Payload
    correction_prompt = (
        f"EDITORIAL RE-AUDIT INSTRUCTION:\n"
        f"You are issuing a formal re-audit and correction. {reason}\n"
        f"Ground your evaluation strictly in the verified real-world event and actions across the multi-source dossier, "
        f"NOT partisan social media rhetoric or cable news punditry.\n\n"
        f"=== MULTI-SOURCE BALANCED DOSSIER ===\n"
        f"{cross_source_dossier}"
    )

    candidate_payload = [{
        "url": primary_link or (counter_sources[0]["url"] if counter_sources else ""),
        "target_url": target_post_url,
        "mode": "reply" if target_post_url else "root",
        "text": f"Stated Claim / Post Context:\n{subject}\n\n{correction_prompt}",
        "subject": subject
    }]

    # Save to temporary candidates file for one-shot evaluator
    temp_cand_path = os.path.join(script_dir, f"temp_reaudit_candidate_{slug}.json")
    with open(temp_cand_path, "w", encoding="utf-8") as f:
        json.dump(candidate_payload, f, indent=2, ensure_ascii=False)

    # 4. Run Convergence Evaluation via google_ai_studio_one_shot
    print(f"\n[3/5] Running Convergence Evaluation via {model}...")
    import subprocess
    cmd = [
        sys.executable, "-u",
        os.path.join(script_dir, "google_ai_studio_one_shot.py"),
        "--candidates", temp_cand_path,
        "--model", model,
        "--compact"
    ]
    if use_potential:
        cmd.append("--potential")
    elif use_son:
        cmd.append("--son")

    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.stderr:
        print(f"Stderr: {res.stderr}")

    # Remove temporary candidate file
    try:
        os.remove(temp_cand_path)
    except Exception:
        pass

    # 5. Inspect Evaluated Story in Darkroom & Apply Retraction Metadata
    darkroom_file = os.path.join(script_dir, "stories", "darkroom", f"factcheck_{slug}.json")
    if not os.path.exists(darkroom_file):
        # Look for the newest file in darkroom
        dark_dir = os.path.join(script_dir, "stories", "darkroom")
        files = [os.path.join(dark_dir, f) for f in os.listdir(dark_dir) if f.startswith("factcheck_") and f.endswith(".json")]
        if files:
            files.sort(key=os.path.getmtime, reverse=True)
            darkroom_file = files[0]

    if not os.path.exists(darkroom_file):
        print(f"ERROR: Re-audited story JSON not found in darkroom.")
        return False

    with open(darkroom_file, "r", encoding="utf-8") as f:
        re_data = json.load(f)
    re_story = re_data[0] if isinstance(re_data, list) else re_data

    # Enforce Deterministic Trajectory
    re_story = enforce_deterministic_trajectory(re_story)

    # Prepend Errata Badge to Post 0
    posts = re_story.get("posts", [])
    if posts:
        errata_prefix = "[CORRECTION & RE-AUDIT]\n"
        if not posts[0].startswith("[CORRECTION"):
            posts[0] = errata_prefix + posts[0]
            if len(posts[0]) > 300:
                posts[0] = posts[0][:297] + "..."
    re_story["posts"] = posts
    re_story["status"] = "AMENDED (Re-Audited)"
    re_story["retraction"] = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "type": "AMENDED",
        "reason": reason,
        "new_coords": [re_story.get("real_u"), re_story.get("real_psi")]
    }

    # Save to live destination
    dest_path = local_path if local_path else os.path.join(script_dir, "stories", "live", f"factcheck_{slug}.json")
    with open(dest_path, "w", encoding="utf-8") as f:
        json.dump([re_story], f, indent=2, ensure_ascii=False)
    print(f"\n[4/5] Re-audited story saved to: {dest_path}")

    # Rebuild registries
    print(f"Rebuilding registries and generating evidence cards...")
    try:
        from rebuild_registries_son import rebuild_registries
        rebuild_registries()
    except Exception as rb_ex:
        print(f"Warning: Rebuild registries failed: {rb_ex}")

    # 6. Post Live Correction Reply to Bluesky (if live)
    if live and target_post_url and "bsky.app" in target_post_url:
        print(f"\n[5/5] Posting Live Errata Reply directly under root thread...")
        try:
            from atproto import Client, models, IdResolver
            handle = os.environ.get("BSKY_HANDLE", "judgement-bot.bsky.social")
            password = os.environ.get("BSKY_PASSWORD")
            client = Client()
            client.login(handle, password)

            parts = target_post_url.strip("/").split("/")
            author_handle = parts[parts.index("profile") + 1]
            rkey = parts[parts.index("post") + 1].split("?")[0]

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

            # Upload verdict card image
            img_path = os.path.join(script_dir, "graph_png", f"{slug}_info_card_verdict.png")
            if not os.path.exists(img_path):
                img_path = os.path.join(script_dir, "graph_png", f"{slug}_graph.png")

            embed = None
            if os.path.exists(img_path):
                with open(img_path, "rb") as img_f:
                    up_blob = client.com.atproto.repo.upload_blob(img_f.read())
                embed = models.AppBskyEmbedImages.Main(
                    images=[models.AppBskyEmbedImages.Image(alt="Re-Audited Verdict Card", image=up_blob.blob)]
                )

            math_path = get_path_name(re_story["claim_u"], re_story["claim_psi"], re_story["real_u"], re_story["real_psi"])
            errata_msg = (
                f"[CORRECTION & AUDIT RE-ANCHOR]\n\n"
                f"{reason or 'Rebalanced with multi-source wire coverage.'}\n\n"
                f"Revised Judgement: ({re_story['real_u']:+.1f}, {re_story['real_psi']:+.1f}) — {math_path}\n"
                f"#Aletheia #Errata"
            )
            if len(errata_msg) > 300:
                errata_msg = errata_msg[:297] + "..."

            reply_rec = models.AppBskyFeedPost.Record(
                created_at=client.get_current_time_iso(),
                text=errata_msg,
                reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref),
                embed=embed
            )
            reply_res = client.com.atproto.repo.create_record(
                models.ComAtprotoRepoCreateRecord.Data(
                    repo=client.me.did,
                    collection='app.bsky.feed.post',
                    record=reply_rec
                )
            )
            print(f"SUCCESS: Live Errata reply posted to Bluesky: {reply_res.uri}")
        except Exception as post_err:
            print(f"Warning: Failed to publish live errata to Bluesky: {post_err}")
    else:
        print(f"\n[5/5] Re-Audit complete. Preview available in Darkroom / Control Panel. (Dry run mode - no live posts made).")

    print(f"\n=======================================================")
    print(f"✅ RE-AUDIT PIPELINE COMPLETED")
    print(f"=======================================================\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="Aletheia Story Re-Audit & Correction Dispatcher")
    parser.add_argument("--target", required=True, help="Story slug ID (e.g. dems_flips_iowa_senate_thune_vow) or Bluesky post URL")
    parser.add_argument("--reason", default="", help="Editorial correction focus and reason for re-audit")
    parser.add_argument("--model", default="gemini-3.8-flash", help="Generative model for re-audit (default: gemini-3.8-flash)")
    parser.add_argument("--son", action="store_true", default=True, help="Use 6-Attractor SON convergence model (default: True)")
    parser.add_argument("--potential", action="store_true", help="Use 9-Node Modal Potential convergence model")
    parser.add_argument("--live", action="store_true", help="Post live Errata reply directly to Bluesky")

    args = parser.parse_args()
    success = run_reaudit(
        target=args.target,
        reason=args.reason,
        model=args.model,
        use_son=not args.potential,
        use_potential=args.potential,
        live=args.live
    )
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
