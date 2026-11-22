import os
import sys
import re
import json
import argparse
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from renderer import draw_graph, draw_card, get_path_name
from evaluator import evaluate_candidate, DEFAULT_FALLBACKS
from harvester import harvest_candidates, scrape_article_text
from publisher import publish_story, post_batch_drafts, validate_draft

def slugify(text):
    text = re.sub(r'[^a-zA-Z0-9]+', '_', text or "story")
    return text.strip('_').lower()[:40]

def run_test_graph():
    print("\n--- Running Graphics Test ---")
    graph_dir = os.path.join(script_dir, "graph_png")
    card_dir = os.path.join(script_dir, "card_png")
    os.makedirs(graph_dir, exist_ok=True)
    os.makedirs(card_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_graph_path = os.path.join(graph_dir, f"test_graph_{timestamp}.png")
    test_card_path = os.path.join(card_dir, f"test_card_{timestamp}.png")

    # 1. Test Graph
    claim_u, claim_psi = 1.8, 1.5
    real_u, real_psi = -1.2, -1.4
    title = "Test Case: Public Integrity Audit"
    print(f"Generating test graph: {test_graph_path}...")
    draw_graph(claim_u, claim_psi, real_u, real_psi, title, test_graph_path)
    print(f"Graph generated successfully: {os.path.exists(test_graph_path)} ({os.path.getsize(test_graph_path):,} bytes)")

    # 2. Test Deep-Dive Card
    path_name = get_path_name(claim_u, claim_psi, real_u, real_psi)
    card_cfg = {
        "title": title,
        "verdict": "FAIL",
        "path_name": path_name,
        "claim_coords": f"({claim_u:+.1f}, {claim_psi:+.1f})",
        "real_coords": f"({real_u:+.1f}, {real_psi:+.1f})",
        "sections": {
            "Context": "Official ministerial statement asserted that all emergency disaster relief funding reached affected flood communities with zero overhead waste.",
            "Empirical Evidence": "Independent state auditor report and bank disbursement logs confirmed 75% of allocated funds were retained by administrative consultants, leaving communities unassisted.",
            "Human Impacts": "Over 2,400 displaced residents remained in temporary shelters for 18 months without reconstructed drainage or essential infrastructure.",
            "Plane Analysis": "Q5 Logical Breakdown: Material bank transaction records directly contradict published administrative budget declarations.",
            "Social Physics": "Moral vector inverted from stated universal public protection (+1.8, +1.5) to group extraction (-1.2, -1.4)."
        },
        "personas": {
            "Alethekanon": "The ledger tells no lies; the money stopped flowing three miles outside the capital.",
            "Brothekanon": "Consultants took seventy-five cents on every dollar meant for sandbags and pumps.",
            "Awwthekanon": "Families spent another winter under blue tarps while reports were stamped complete.",
            "Spirithekanon": "A promise broken to people in need is an absolute moral failure."
        }
    }
    print(f"Generating test card: {test_card_path}...")
    draw_card(card_cfg, test_card_path)
    print(f"Card generated successfully: {os.path.exists(test_card_path)} ({os.path.getsize(test_card_path):,} bytes)")
    print("--- Graphics Test Completed ---\n")
    return test_graph_path, test_card_path

def process_candidate(candidate, model_name="gemini-2.5-flash", model_sequence=None, live=False):
    subject = candidate.get("subject") or candidate.get("title") or "News Audit"
    url = candidate.get("url") or candidate.get("link") or ""
    print(f"\nProcessing Candidate: {subject}\nURL: {url}")

    # 1. Run Structured Evaluation via Gemini with Model Fallback
    story = evaluate_candidate(candidate, model_name=model_name, model_sequence=model_sequence)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = f"{slugify(story.get('subject', 'audit'))}_{timestamp}"
    story["id"] = slug

    # 2. Render Graph
    graph_dir = os.path.join(script_dir, "graph_png")
    os.makedirs(graph_dir, exist_ok=True)
    graph_path = os.path.join(graph_dir, f"graph_{slug}.png")
    
    draw_graph(
        claim_u=story["claim_u"],
        claim_psi=story["claim_psi"],
        real_u=story["real_u"],
        real_psi=story["real_psi"],
        title=story.get("subject", subject),
        filename=graph_path
    )
    story["graph_path"] = graph_path

    # 3. Render Deep-Dive Card
    card_dir = os.path.join(script_dir, "card_png")
    os.makedirs(card_dir, exist_ok=True)
    card_path = os.path.join(card_dir, f"card_{slug}.png")

    card_cfg = {
        "subject": story.get("subject", subject),
        "id": slug,
        "verdict": story.get("verdict", "AUDIT"),
        "path_name": story.get("path_name", ""),
        "claim_coords": f"({story['claim_u']:+.1f}, {story['claim_psi']:+.1f})",
        "real_coords": f"({story['real_u']:+.1f}, {story['real_psi']:+.1f})",
        "posts": story.get("posts", [])
    }
    draw_card(card_cfg, card_path)
    story["card_path"] = card_path

    # 4. Publish / Dry-Run Thread
    publish_story(story, graph_path=graph_path, card_path=card_path, live=live)
    return story

def main():
    parser = argparse.ArgumentParser(description="Aletheia Bluesky News Factcheck Bot (Streamlined v2)")
    parser.add_argument("--test-graph", action="store_true", help="Render test graph and analysis card to verify visuals.")
    parser.add_argument("--dry-run", action="store_true", help="Harvest and simulate Bluesky threads without live posting.")
    parser.add_argument("--live", action="store_true", help="Publish evaluated threads live to Bluesky.")
    parser.add_argument("--url", type=str, default=None, help="Audit a single specific URL directly.")
    parser.add_argument("--limit", type=int, default=1, help="Max candidates to harvest and process.")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash", help="Primary Gemini model for audit.")
    parser.add_argument("--model-sequence", type=str, default=None, help="Comma-separated model fallback sequence (e.g. 'gemini-2.5-flash,gemini-2.5-flash-lite').")
    
    # Filtering & Category Arguments
    parser.add_argument("--category", type=str, default="general", help="Feed category or comma-separated categories.")
    parser.add_argument("--topic", type=str, default="", help="Keyword topic filter.")
    parser.add_argument("--exclude-topics", type=str, default="", help="Comma-separated topics to exclude.")
    
    # Poster / Scheduler Arguments
    parser.add_argument("--post-drafts", action="store_true", help="Run batch poster on pending drafts in stories/.")
    parser.add_argument("--validate-drafts", action="store_true", help="Pre-flight validation check on all drafts in stories/.")
    parser.add_argument("--min-delay", type=float, default=10.0, help="Minimum delay in seconds between scheduled posts.")
    parser.add_argument("--max-delay", type=float, default=30.0, help="Maximum delay in seconds between scheduled posts.")
    parser.add_argument("--watch", action="store_true", help="Continuously watch for new draft stories and post them.")
    args = parser.parse_args()

    if args.test_graph:
        run_test_graph()
        return

    # Poster / Scheduler Flow
    if args.validate_drafts:
        import glob
        drafts = glob.glob(os.path.join(script_dir, "stories", "factcheck_*.json"))
        print(f"Validating {len(drafts)} drafts in stories/...")
        for d in drafts:
            try:
                with open(d, "r", encoding="utf-8") as f:
                    data = json.load(f)
                s = data[0] if isinstance(data, list) and len(data) > 0 else data
                ok, msg = validate_draft(s)
                status = "PASS" if ok else "FAIL"
                print(f"[{status}] {os.path.basename(d)}: {msg}")
            except Exception as e:
                print(f"[ERROR] {os.path.basename(d)}: {e}")
        return

    if args.post_drafts:
        post_batch_drafts(live=args.live, min_delay=args.min_delay, max_delay=args.max_delay, watch=args.watch)
        return

    # Parse fallback model sequence if provided
    model_seq = None
    if args.model_sequence:
        model_seq = [m.strip() for m in args.model_sequence.split(",") if m.strip()]

    if args.url:
        print(f"Scraping direct URL: {args.url}...")
        body = scrape_article_text(args.url)
        if not body or len(body) < 100:
            print(f"Error: Unable to extract sufficient body text from URL: {args.url}")
            sys.exit(1)
        candidate = {
            "subject": args.url.split("/")[-1].replace("-", " ").title(),
            "url": args.url,
            "body": body
        }
        process_candidate(candidate, model_name=args.model, model_sequence=model_seq, live=args.live)
        return

    # Standard feed harvest workflow
    print(f"Harvesting up to {args.limit} candidates from RSS feeds...")
    candidates = harvest_candidates(max_candidates=args.limit)
    if not candidates:
        print("No new candidates harvested (all current stories may already be archived).")
        return

    for c in candidates:
        process_candidate(c, model_name=args.model, model_sequence=model_seq, live=args.live)

if __name__ == "__main__":
    main()
