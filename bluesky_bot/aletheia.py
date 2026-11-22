#!/usr/bin/env python3
"""
Aletheia Unified CLI Router (aletheia.py)
Single authoritative entrypoint for the Aletheia Bot suite.

Subcommands:
  aletheia harvest  - Ingest news candidates from RSS / Bluesky
  aletheia eval     - Evaluate candidates into dossiers with AI Studio & SON/Modal physics
  aletheia post     - Post audited dossiers to Bluesky
  aletheia render   - Render/re-render vector field graphs and visual cards
  aletheia retract  - Retract an audited story with in-thread errata
  aletheia rebuild  - Rebuild story and actor registries
  aletheia status   - Print system status and story queue metrics
"""

import sys
import os
import argparse
import subprocess

# Ensure bluesky_bot directory is on sys.path
BOT_DIR = os.path.dirname(os.path.abspath(__file__))
if BOT_DIR not in sys.path:
    sys.path.insert(0, BOT_DIR)


def get_python_exe():
    """Locate python executable in venv or default sys.executable."""
    venv_main = os.path.join(BOT_DIR, "..", ".venv", "Scripts", "python.exe")
    venv_bot = os.path.join(BOT_DIR, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_main):
        return os.path.abspath(venv_main)
    if os.path.exists(venv_bot):
        return os.path.abspath(venv_bot)
    return sys.executable


def run_pipeline_script(script_name, forwarded_args):
    """Run a pipeline script directly forwarding arguments."""
    script_path = os.path.join(BOT_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"Error: Script not found: {script_path}", file=sys.stderr)
        return 1
    
    cmd = [get_python_exe(), "-u", script_path] + forwarded_args
    try:
        proc = subprocess.run(cmd, cwd=BOT_DIR)
        return proc.returncode
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 130


def cmd_harvest(args, remaining_args):
    """Run candidate harvesting."""
    forwarded = []
    if args.rss:
        forwarded.extend(["--rss", str(args.rss)])
    if args.bsky:
        forwarded.extend(["--bsky", str(args.bsky)])
    if args.category:
        forwarded.extend(["--category", args.category])
    if args.topic:
        forwarded.extend(["--topic", args.topic])
    if args.banned_topic:
        forwarded.extend(["--banned-topic", args.banned_topic])
    if args.feeds:
        forwarded.extend(["--enabled-feeds", args.feeds])
    forwarded.extend(remaining_args)
    return run_pipeline_script("harvest_candidates.py", forwarded)


def cmd_eval(args, remaining_args):
    """Run evaluation batch (google_ai_studio_one_shot.py)."""
    forwarded = []
    if args.potential:
        forwarded.append("--potential")
    elif args.son:
        forwarded.append("--son")
    if args.spiritual:
        forwarded.append("--spiritual")
    if args.multi_aspect:
        forwarded.append("--multi-aspect")
    if args.search:
        forwarded.append("--search")
    if args.compact:
        forwarded.append("--compact")
    if args.five_word:
        forwarded.append("--five-word")
    if args.batch_size:
        forwarded.extend(["--batch-size", str(args.batch_size)])
    if args.model:
        forwarded.extend(["--model", args.model])
    if args.thinking_level:
        forwarded.extend(["--thinking-level", args.thinking_level])
    if args.rss:
        forwarded.extend(["--rss", str(args.rss)])
    if args.bsky:
        forwarded.extend(["--bsky", str(args.bsky)])
    if args.category:
        forwarded.extend(["--category", args.category])
    if args.topic:
        forwarded.extend(["--topic", args.topic])
    if args.dry_run:
        forwarded.append("--dry-run")
    forwarded.extend(remaining_args)
    return run_pipeline_script("google_ai_studio_one_shot.py", forwarded)


def cmd_post(args, remaining_args):
    """Post audited stories to Bluesky."""
    forwarded = []
    if args.live:
        forwarded.append("--live")
    if args.dry_run:
        forwarded.append("--dry-run")
    if args.single:
        forwarded.extend(["--single", args.single])
    if args.limit:
        forwarded.extend(["--limit", str(args.limit)])
    forwarded.extend(remaining_args)
    return run_pipeline_script("post_batch.py", forwarded)


def cmd_render(args, remaining_args):
    """Render graph or visual card."""
    if args.card:
        return run_pipeline_script("image_card_generator.py", remaining_args)
    return run_pipeline_script("generate_graph.py", remaining_args)


def cmd_retract(args, remaining_args):
    """Retract an audited story with errata reply."""
    forwarded = [args.story_id]
    if args.reason:
        forwarded.extend(["--reason", args.reason])
    forwarded.extend(remaining_args)
    return run_pipeline_script("retract_story.py", forwarded)


def cmd_rebuild(args, remaining_args):
    """Rebuild registries."""
    return run_pipeline_script("rebuild_registries_son.py", remaining_args)


def cmd_status(args, remaining_args):
    """Print system status."""
    stories_dir = os.path.join(BOT_DIR, "stories")
    darkroom = os.path.join(stories_dir, "darkroom")
    drafts = os.path.join(stories_dir, "drafts")
    live = os.path.join(stories_dir, "live")
    quarantine = os.path.join(stories_dir, "quarantine")

    def count_json(path):
        if not os.path.exists(path):
            return 0
        return len([f for f in os.listdir(path) if f.endswith(".json")])

    print("=" * 50)
    print("  ALETHEIA PIPELINE STATUS")
    print("=" * 50)
    print(f"  Darkroom (Candidates) : {count_json(darkroom)}")
    print(f"  Drafts (Audited)      : {count_json(drafts)}")
    print(f"  Live (Published)      : {count_json(live)}")
    print(f"  Quarantine            : {count_json(quarantine)}")
    print("-" * 50)
    
    # Check registries
    reg_path = os.path.join(BOT_DIR, "story_registry_son.json")
    if os.path.exists(reg_path):
        try:
            import json
            with open(reg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"  Story Registry Stories: {len(data.get('stories', []))}")
        except Exception:
            pass
    print("=" * 50)
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="aletheia",
        description="Aletheia Bot Suite - Unified CLI Router",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Harvest
    p_harvest = subparsers.add_parser("harvest", help="Ingest candidates from RSS/Bluesky")
    p_harvest.add_argument("--rss", type=int, default=5, help="Number of RSS items per feed")
    p_harvest.add_argument("--bsky", type=int, default=5, help="Number of Bluesky posts")
    p_harvest.add_argument("--category", type=str, default="", help="Filter category")
    p_harvest.add_argument("--topic", type=str, default="", help="Keyword filter")
    p_harvest.add_argument("--banned-topic", type=str, default="", help="Topics to exclude")
    p_harvest.add_argument("--feeds", type=str, default="", help="Comma-separated enabled feeds")

    # Eval
    p_eval = subparsers.add_parser("eval", help="Evaluate candidates with AI Studio")
    p_eval.add_argument("--potential", action="store_true", help="Enable Potential Mode (Modal)")
    p_eval.add_argument("--son", action="store_true", help="Enable SON 6-Attractor Mode")
    p_eval.add_argument("--spiritual", action="store_true", help="Enable Spiritual Mode")
    p_eval.add_argument("--multi-aspect", action="store_true", help="Enable Multi-Aspect Audit")
    p_eval.add_argument("--search", action="store_true", help="Enable Google Search Grounding")
    p_eval.add_argument("--compact", action="store_true", help="Enable Compact Mode")
    p_eval.add_argument("--five-word", action="store_true", help="Enable 5-Word Mode")
    p_eval.add_argument("--batch-size", type=int, default=2, help="Batch size (default: 2)")
    p_eval.add_argument("--model", type=str, default="", help="Override model name")
    p_eval.add_argument("--thinking-level", type=str, default="HIGH", help="Thinking level")
    p_eval.add_argument("--rss", type=int, default=5, help="RSS limit")
    p_eval.add_argument("--bsky", type=int, default=5, help="Bluesky limit")
    p_eval.add_argument("--category", type=str, default="", help="Category")
    p_eval.add_argument("--topic", type=str, default="", help="Topic")
    p_eval.add_argument("--dry-run", action="store_true", help="Dry run evaluation without saving")

    # Post
    p_post = subparsers.add_parser("post", help="Post audited stories to Bluesky")
    p_post.add_argument("--live", action="store_true", help="Post live to Bluesky (default is dry-run)")
    p_post.add_argument("--dry-run", action="store_true", help="Simulate posting without ATProto calls")
    p_post.add_argument("--single", type=str, default="", help="Post a specific story JSON file")
    p_post.add_argument("--limit", type=int, default=0, help="Max stories to post")

    # Render
    p_render = subparsers.add_parser("render", help="Render vector graphs and image cards")
    p_render.add_argument("--card", action="store_true", help="Render visual cards instead of graph")

    # Retract
    p_retract = subparsers.add_parser("retract", help="Retract an audited story")
    p_retract.add_argument("story_id", help="Story ID or filename to retract")
    p_retract.add_argument("--reason", type=str, default="", help="Retraction rationale")

    # Rebuild
    p_rebuild = subparsers.add_parser("rebuild", help="Rebuild story and actor registries")

    # Status
    p_status = subparsers.add_parser("status", help="Print pipeline status metrics")

    # Parse known args, remaining args are forwarded
    parsed, remaining = parser.parse_known_args()
    if not parsed.command:
        parser.print_help()
        return 0

    commands = {
        "harvest": (cmd_harvest, parsed, remaining),
        "eval": (cmd_eval, parsed, remaining),
        "post": (cmd_post, parsed, remaining),
        "render": (cmd_render, parsed, remaining),
        "retract": (cmd_retract, parsed, remaining),
        "rebuild": (cmd_rebuild, parsed, remaining),
        "status": (cmd_status, parsed, remaining),
    }

    fn, p, rem = commands[parsed.command]
    return fn(p, rem)


if __name__ == "__main__":
    sys.exit(main())
