"""direct_reply_dispatcher.py — Direct Target Post & Reply Dispatcher for Aletheia Bot Ecosystem.

Allows manual target post replies by taking a Bluesky post URL, resolving its ATProto thread
references, selecting a specific bot persona and skill, cross-referencing against the 10,800+
Audit Database, generating an official Archival Badge card, and posting threaded replies.
"""

import os
import sys
import json
import re
import argparse
import urllib.request
import urllib.parse
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows terminals
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from aletheia_bot import parse_bsky_url, resolve_facets_and_tags
from audit_crossref import (
    search_audit_archive,
    format_archive_reply,
    extract_search_terms_from_post,
    get_audit_by_id,
    crossref_factcheck_claim
)
from image_card_generator import generate_audit_archive_card, generate_audit_factcheck_card

GRAPH_PNG_DIR = os.path.join(SCRIPT_DIR, "graph_png")
os.makedirs(GRAPH_PNG_DIR, exist_ok=True)

# Bot Personas mapping
BOT_PERSONAS = {
    "aletheia": {
        "name": "Aletheia Bot ⚖️",
        "handle_env": "BSKY_HANDLE",
        "pass_env": "BSKY_PASSWORD",
        "default_handle": "judgement-bot.bsky.social"
    },
    "brothekanon": {
        "name": "Brothekanon 🛹",
        "handle_env": "BROTHEKANON_HANDLE",
        "pass_env": "BROTHEKANON_PASSWORD",
        "default_handle": "brothekanon.bsky.social"
    },
    "awwthekanon": {
        "name": "Awwthekanon 🧸",
        "handle_env": "AWWTHEKANON_HANDLE",
        "pass_env": "AWWTHEKANON_PASSWORD",
        "default_handle": "awwthekanon.bsky.social"
    },
    "spirithekanon": {
        "name": "Spirithekanon 🕊️",
        "handle_env": "SPIRITHEKANON_HANDLE",
        "pass_env": "SPIRITHEKANON_PASSWORD",
        "default_handle": "spirithekanon.bsky.social"
    }
}


def fetch_target_post_public(target_url):
    """Fetches a public Bluesky post via public API (works without credentials)."""
    handle, rkey = parse_bsky_url(target_url)

    # 1. Resolve handle to DID
    resolve_url = f"https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle={urllib.parse.quote(handle)}"
    req = urllib.request.Request(resolve_url, headers={"User-Agent": "AletheiaBot/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        did = data.get("did")

    if not did:
        raise ValueError(f"Could not resolve DID for handle: {handle}")

    # 2. Fetch post record
    at_uri = f"at://{did}/app.bsky.feed.post/{rkey}"
    thread_url = f"https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?uri={urllib.parse.quote(at_uri)}&depth=0"
    treq = urllib.request.Request(thread_url, headers={"User-Agent": "AletheiaBot/1.0"})
    with urllib.request.urlopen(treq, timeout=10) as tresp:
        tdata = json.loads(tresp.read().decode("utf-8"))

    thread_obj = tdata.get("thread", {})
    post_obj = thread_obj.get("post", {})
    record = post_obj.get("record", {})

    cid = post_obj.get("cid")
    uri = post_obj.get("uri")
    text = record.get("text", "")
    author_handle = post_obj.get("author", {}).get("handle", handle)
    author_name = post_obj.get("author", {}).get("displayName", author_handle)

    # Check for existing reply root
    reply_data = record.get("reply")
    if reply_data and isinstance(reply_data, dict):
        root_ref = reply_data.get("root", {"cid": cid, "uri": uri})
    else:
        root_ref = {"cid": cid, "uri": uri}
    parent_ref = {"cid": cid, "uri": uri}

    return {
        "handle": author_handle,
        "displayName": author_name,
        "did": did,
        "rkey": rkey,
        "cid": cid,
        "uri": uri,
        "text": text,
        "root_ref": root_ref,
        "parent_ref": parent_ref
    }


def get_authenticated_client_for_bot(bot_key):
    """Logs into Bluesky using the bot's credentials, falling back to primary BSKY credentials."""
    from atproto import Client
    load_dotenv(os.path.join(SCRIPT_DIR, ".env"))
    load_dotenv()

    binfo = BOT_PERSONAS.get(bot_key, BOT_PERSONAS["aletheia"])
    handle = os.getenv(binfo["handle_env"]) or os.getenv("BSKY_HANDLE") or binfo["default_handle"]
    password = os.getenv(binfo["pass_env"]) or os.getenv("BSKY_PASSWORD")

    if not password:
        raise ValueError(f"No Bluesky password found in .env for {bot_key} (checked {binfo['pass_env']} and BSKY_PASSWORD).")

    client = Client()
    client.login(handle, password)
    return client, handle


def execute_direct_reply(target_url, bot="aletheia", skill="archive", query_override="", custom_text="", num_replies=1, live=False, use_ai=True, model_sequence=None, perspectives=None):
    """Executes or previews a targeted direct reply to a Bluesky post."""
    bot_key = bot.lower().strip()
    if bot_key not in BOT_PERSONAS:
        for k in BOT_PERSONAS:
            if k in bot_key:
                bot_key = k
                break
        else:
            bot_key = "aletheia"

    binfo = BOT_PERSONAS[bot_key]
    
    # Resolve thread length from perspectives queue if provided
    if perspectives and len(perspectives) > 0:
        perspective_queue = perspectives[:5]
        n_replies = len(perspective_queue)
    else:
        perspective_queue = None
        n_replies = max(1, min(5, int(num_replies)))

    print(f"\n==================================================")
    print(f"TARGET POST DIRECT REPLY DISPATCHER")
    print(f"Target URL: {target_url}")
    print(f"Bot Persona: {binfo['name']}")
    print(f"Skill: {skill.upper()}")
    print(f"Thread Length: {n_replies} {'reply' if n_replies == 1 else 'replies'}")
    if perspective_queue:
        print(f"Perspective Queue: {' -> '.join(perspective_queue)}")
    print(f"AI Persona Synthesis: {'ENABLED' if use_ai else 'DISABLED (COLD LEDGER)'}")
    print(f"Live Post Mode: {'LIVE (POSTING TO BLUESKY)' if live else 'DRY RUN (PREVIEW ONLY)'}")
    print(f"==================================================")

    # 1. Fetch Target Bluesky Post
    print("Resolving target Bluesky post...")
    target_info = fetch_target_post_public(target_url)
    print(f"Target Author: @{target_info['handle']} ({target_info['displayName']})")
    print(f"Target Content: \"{target_info['text'][:140]}{'...' if len(target_info['text']) > 140 else ''}\"")

    card_image_path = None
    audit_record = None
    reply_posts = []

    # 2. Skill Execution
    if skill in ["archive", "factcheck"]:
        # Full empirical fact-check across 10,800+ Audit Database Archive
        print(f"Cross-referencing claim across 10,800+ Audit Database Archive...")
        fc_data = crossref_factcheck_claim(
            claim_text=target_info["text"],
            author_handle=target_info["handle"],
            query_override=query_override,
            persona=bot_key,
            num_replies=n_replies,
            use_ai=use_ai,
            model_sequence=model_sequence,
            perspective_queue=perspective_queue
        )
        print(f"Domain Identified: {fc_data['domain_name']} ({fc_data['domain_short']})")
        print(f"Corpus Analysis: {fc_data['total_cases']:,} relevant audits analyzed")
        print(f"Empirical Skew: {fc_data['neg_pct']:.1f}% (-υ extraction) vs {fc_data['pos_pct']:.1f}% (+υ defense/clash)")
        print(f"Claim Coordinate: ({fc_data['claim_u']:+.2f}, {fc_data['claim_psi']:+.2f}) -> {fc_data['zone_anchor']}")
        print(f"Verdict: {fc_data['verdict']}")

        # Generate "From the Audit Archive · Empirical Fact Check" Badge Card
        slug = re.sub(r'[^a-zA-Z0-9_-]+', '_', target_info['handle']).strip('_')
        card_image_path = os.path.join(GRAPH_PNG_DIR, f"{slug}_{target_info['rkey']}_factcheck_card.png")
        print(f"Generating high-resolution Empirical Fact-Check Card...")
        generate_audit_factcheck_card(fc_data, card_image_path)
        print(f"Fact-Check Card ready: {card_image_path}")

        reply_posts = fc_data.get("reply_posts", [fc_data["reply_text"]])
        audit_record = fc_data

    elif skill in ["bro", "aww", "spirit"]:
        # Persona-tailored empirical reaction cross-referenced against the archive
        print(f"Running persona-tuned ({skill.upper()}) empirical analysis across Audit Database...")
        fc_data = crossref_factcheck_claim(
            claim_text=target_info["text"],
            author_handle=target_info["handle"],
            query_override=query_override,
            persona=skill,
            num_replies=n_replies,
            use_ai=use_ai,
            model_sequence=model_sequence,
            perspective_queue=perspective_queue
        )
        print(f"Domain: {fc_data['domain_short']} ({fc_data['total_cases']:,} cases) | Skew: {fc_data['neg_pct']:.1f}% (-υ) vs {fc_data['pos_pct']:.1f}% (+υ)")
        slug = re.sub(r'[^a-zA-Z0-9_-]+', '_', target_info['handle']).strip('_')
        card_image_path = os.path.join(GRAPH_PNG_DIR, f"{slug}_{target_info['rkey']}_factcheck_card.png")
        generate_audit_factcheck_card(fc_data, card_image_path)

        reply_posts = fc_data.get("reply_posts", [fc_data["persona_replies"].get(skill, fc_data["reply_text"])])
        audit_record = fc_data

    elif skill == "precedent":
        # Single Historical Audit Precedent Citation
        search_term = query_override.strip() if query_override else extract_search_terms_from_post(target_info["text"])
        if not search_term:
            search_term = target_info["handle"]
        print(f"Searching historical precedent for terms: '{search_term}'...")
        matches = search_audit_archive(search_term, limit=3)
        if not matches:
            raise RuntimeError(f"No historical precedent records found matching '{search_term}'.")
        single_record = matches[0]
        slug = single_record.get("id") or "archive_record"
        card_image_path = os.path.join(GRAPH_PNG_DIR, f"{slug}_archive_card.png")
        generate_audit_archive_card(single_record, card_image_path)
        p1_text = format_archive_reply(single_record, persona=bot_key, target_text=target_info["text"])
        reply_posts = [p1_text]
        audit_record = single_record

    elif skill == "custom":
        custom_clean = custom_text.strip()
        if not custom_clean:
            raise ValueError("Skill 'custom' requires --custom-text to be provided.")
        reply_posts = [custom_clean]

    else:
        raise ValueError(f"Unknown skill: '{skill}'. Available skills: archive, factcheck, bro, aww, spirit, precedent, custom.")

    print(f"\n--- DRAFTED THREAD ({len(reply_posts)} {'post' if len(reply_posts) == 1 else 'posts'}) ---")
    for i, p_text in enumerate(reply_posts):
        print(f"\n[Post {i+1}/{len(reply_posts)}] ({len(p_text)} chars):")
        print(p_text)
    print("--------------------------------------------------")

    reply_text = reply_posts[0] if reply_posts else ""

    # 3. Live Posting or Dry Run Return
    if not live:
        print("\n[DRY RUN COMPLETE] Replies were not sent. Pass --live to publish live on Bluesky.")
        return {
            "status": "DRY_RUN",
            "bot": bot_key,
            "handle": binfo["default_handle"],
            "reply_posts": reply_posts,
            "reply_text": reply_text,
            "card_image_path": card_image_path,
            "target_info": target_info,
            "audit_record": audit_record
        }

    # Authenticate and Post Live
    from atproto import models
    print(f"\nLogging into Bluesky as {binfo['name']}...")
    client, posting_handle = get_authenticated_client_for_bot(bot_key)
    print(f"Logged in successfully as {posting_handle}.")

    # Upload Card Image Blob if present
    embed = None
    if card_image_path and os.path.exists(card_image_path):
        print(f"Uploading Audit Archive Card to Bluesky...")
        with open(card_image_path, "rb") as f:
            img_data = f.read()
        upload = client.com.atproto.repo.upload_blob(img_data)
        subject_alt = audit_record.get('subject', 'Audit Record') if audit_record and isinstance(audit_record, dict) else 'From the Audit Archive'
        images = [models.AppBskyEmbedImages.Image(
            alt=f"Aletheia Audit Archive Record for {subject_alt}",
            image=upload.blob
        )]
        embed = models.AppBskyEmbedImages.Main(images=images)
        print("Archive Card uploaded successfully.")

    posted_records = []
    current_parent_ref = models.ComAtprotoRepoStrongRef.Main(
        cid=target_info["parent_ref"]["cid"],
        uri=target_info["parent_ref"]["uri"]
    )
    thread_root_ref = models.ComAtprotoRepoStrongRef.Main(
        cid=target_info["root_ref"]["cid"],
        uri=target_info["root_ref"]["uri"]
    )

    print(f"\nPublishing threaded reply sequence ({len(reply_posts)} posts) to {target_info['uri']}...")
    for idx, p_text in enumerate(reply_posts):
        post_num = idx + 1
        print(f"Publishing post {post_num}/{len(reply_posts)}...")
        post_embed = embed if idx == 0 else None
        facets, tags_list = resolve_facets_and_tags(p_text)

        reply_response = client.com.atproto.repo.create_record(
            models.ComAtprotoRepoCreateRecord.Data(
                repo=client.me.did,
                collection=models.ids.AppBskyFeedPost,
                record=models.AppBskyFeedPost.Record(
                    created_at=client.get_current_time_iso(),
                    text=p_text,
                    reply=models.AppBskyFeedPost.ReplyRef(parent=current_parent_ref, root=thread_root_ref),
                    embed=post_embed,
                    facets=facets,
                    tags=tags_list,
                    langs=["en"]
                )
            )
        )
        posted_rkey = reply_response.uri.split("/")[-1]
        posted_url = f"https://bsky.app/profile/{posting_handle}/post/{posted_rkey}"
        print(f"Post {post_num}/{len(reply_posts)} published: {posted_url}")

        posted_records.append({
            "uri": reply_response.uri,
            "cid": reply_response.cid,
            "rkey": posted_rkey,
            "url": posted_url,
            "text": p_text
        })

        # Subsequent posts in the thread chain onto this post
        current_parent_ref = models.ComAtprotoRepoStrongRef.Main(
            cid=reply_response.cid,
            uri=reply_response.uri
        )

    print(f"\nSUCCESS! All {len(posted_records)} posts published live:")
    for r in posted_records:
        print(f"• {r['url']}")

    return {
        "status": "LIVE_POSTED",
        "bot": bot_key,
        "handle": posting_handle,
        "reply_posts": reply_posts,
        "reply_text": reply_text,
        "card_image_path": card_image_path,
        "posted_records": posted_records,
        "posted_url": posted_records[0]["url"] if posted_records else ""
    }


def main():
    parser = argparse.ArgumentParser(description="Direct Target Post & Reply Dispatcher for Aletheia Bot")
    parser.add_argument("--target-url", type=str, required=True, help="Target Bluesky post URL to reply to")
    parser.add_argument("--bot", type=str, default="aletheia", choices=["aletheia", "brothekanon", "awwthekanon", "spirithekanon"], help="Bot persona to reply as (default: aletheia)")
    parser.add_argument("--skill", type=str, default="archive", choices=["archive", "factcheck", "bro", "aww", "spirit", "precedent", "custom"], help="Skill to execute (default: archive)")
    parser.add_argument("--num-replies", type=int, default=1, choices=[1, 2, 3, 4, 5], help="Number of threaded replies to generate with supporting detail (default: 1)")
    parser.add_argument("--query", type=str, default="", help="Optional search query override for Audit Archive search")
    parser.add_argument("--custom-text", type=str, default="", help="Custom text for reply if skill=custom")
    parser.add_argument("--live", action="store_true", help="Publish reply live to Bluesky (defaults to dry-run preview)")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI persona synthesis and output cold empirical ledger format")
    parser.add_argument("--model-sequence", type=str, default="", help="Comma-separated model fallback sequence (e.g. 'gemini-3.8-flash,gemini-3.7-flash')")
    parser.add_argument("--perspectives", type=str, default="", help="Ordered semicolon or pipe separated perspective queue (e.g. 'receipt;bro;spirit' or 'receipt;custom:media profit')")
    args = parser.parse_args()

    model_seq = [m.strip() for m in args.model_sequence.split(",") if m.strip()] if args.model_sequence else None
    persp_list = [p.strip() for p in re.split(r'[;|]', args.perspectives) if p.strip()] if args.perspectives else None

    try:
        execute_direct_reply(
            target_url=args.target_url,
            bot=args.bot,
            skill=args.skill,
            query_override=args.query,
            custom_text=args.custom_text,
            num_replies=args.num_replies,
            live=args.live,
            use_ai=not args.no_ai,
            model_sequence=model_seq,
            perspectives=persp_list
        )
    except Exception as e:
        print(f"\n[ERROR] Direct reply failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
