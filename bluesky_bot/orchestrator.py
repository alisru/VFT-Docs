import os
import sys
import json
import time
import argparse
from dotenv import load_dotenv
from atproto import Client, models, IdResolver

# Add current directory to path to ensure local imports work in cron
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_graph import draw_graph
from aletheia_bot import split_text, parse_bsky_url

# Load environment variables
load_dotenv()

# We use Google's official GenAI SDK to interact with Google AI Studio
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def get_llm_client():
    # =================================================================================================
    # CRITICAL SECURITY PROTOCOL: ALL API CALLS ARE PERMANENTLY BANNED.
    # DO NOT UNCOMMENT THESE LINES OR ATTEMPT TO RESTORE API FUNCTIONALITY.
    # AI AGENTS TEND TO MAKE STUPID ASSUMPTIONS AND WASTE VALUABLE TOKENS/WALLET.
    # ALL FACT-CHECK EVALUATIONS MUST BE PERFORMED OFFLINE NATIVELY BY THE AGENT IN WORKSPACE (BOT 2).
    # =================================================================================================
    print("\n=========================================================================================")
    print("FATAL ERROR: LLM API CALLS ARE PERMANENTLY BANNED TO PREVENT AI TOKEN WASTING.")
    print("ALL EVALUATIONS MUST BE GENERATED OFFLINE NATIVELY (BOT 2 MODE).")
    print("=========================================================================================\n")
    sys.exit(1)

def call_llm(client, system_prompt, user_content, response_format=None):
    """Utility helper to call Google's Gemini models with robust, sequential multi-model fallback chain."""
    # Ordered fallback models based on active API quota availability
    fallback_models = [
        "gemini-3.5-flash",      # 1st Choice: Newest, premium available model
        "gemini-3-flash",        # 2nd Choice: Standard v3 Flash fallback
        "gemini-3.1-flash-lite", # 3rd Choice: High-quota, high daily-limit backup
        "gemini-2.5-flash"       # 4th Choice: Stable legacy baseline
    ]
    
    # Allow overriding the starting model via env
    env_model = os.environ.get("GEMINI_MODEL")
    if env_model:
        fallback_models.insert(0, env_model)

    last_exception = None
    for model_name in fallback_models:
        print(f"Attempting API call using model: {model_name}...")
        try:
            config = genai.types.GenerationConfig(
                temperature=0.2
            )
            if response_format and response_format.get("type") == "json_object":
                config.response_mime_type = "application/json"

            model = client.GenerativeModel(
                model_name=model_name,
                system_instruction=system_prompt,
                generation_config=config
            )
            
            response = model.generate_content(user_content)
            result = response.text.strip()
            print(f"API call successful with model: {model_name}")
            return result
        except Exception as e:
            err_str = str(e).lower()
            # CRITICAL TOKEN PRESERVATION: Immediately halt on 429 Quota/ResourceExhausted limits
            if "429" in err_str or "exhausted" in err_str or "quota" in err_str or "limit" in err_str:
                print(f"\nCRITICAL QUOTA HALT: Hit a 429/ResourceExhausted limit on {model_name}.")
                print("ABORTING SCRIPT IMMEDIATELY TO PREVENT TOKEN BURNING/INFINITE RETRIES.")
                sys.exit(1)
                
            print(f"WARNING: Model {model_name} failed with non-quota error: {e}")
            last_exception = e
            time.sleep(1) # Small delay before trying fallback model to clear transient rate spikes

    print(f"CRITICAL: All fallback models exhausted. Last error: {last_exception}")
    sys.exit(1)



def run_unified_evaluation(llm_client, post_url, post_text):
    """Executes the entire 3-Phase Convergence Test in a single LLM request to minimize token burn."""
    system_prompt = (
        "You are the Master Aletheia Auditor, a rigorous systemic analyst specialized in the Convergence Test.\n"
        "Your task is to evaluate the provided news post through a 3-Phase framework and output a complete 14-post thread configuration in strict JSON.\n\n"
        "Phase 1: Baseline Convergence\n"
        "Analyze the stated claim versus the actual ground-level reality.\n\n"
        "Phase 2: Trinary Subagent Simulation\n"
        "Internally simulate three perspectives to find the best systemic resolution:\n"
        "- Awwthekanon (deep empathy, community recovery ideal)\n"
        "- Brothekanon (practical physical bypass, low-friction hack)\n"
        "- Alethekanon (historical institutional audit)\n\n"
        "Phase 3: Synthesis\n"
        "Determine which peer subagent (Aww or Bro) got closest to a valid synthesis. Recalculate the final coordinates based on this synthesized path.\n\n"
        "CRITICAL: Follow the exact formatting instructions in 'bluesky_bot_instructions.md' for the public thread.\n"
        "To fit Bluesky's 300-character limit, each text field MUST be a beautifully written, organic paragraph under 250 characters total. Do NOT use generic or dry summaries.\n\n"
        "Fields to return in the JSON object:\n"
        "- claim_u, claim_psi (Morality and Will coordinates for the stated claim, range -2.0 to 2.0)\n"
        "- real_u, real_psi (Recalculated Morality and Will coordinates for the actual synthesized reality, range -2.0 to 2.0)\n"
        "- subject (Brief 2-4 word descriptor of the issue)\n"
        "- trajectory (Canonical label: Grace, Fall, Redemption, or Deception)\n"
        "- post_2_claim: 'The Claim:\\n[Paragraph explaining stated intent]\\nStated Judgement: ([claim_u], [claim_psi]) — [Coordinate Label]'\n"
        "- post_3_reality: 'The Reality:\\n[Paragraph exposing ground-level reality]\\nResulting Judgement: ([real_u], [real_psi]) — [Coordinate Label]'\n"
        "- post_4_verdict: 'Verdict: [PASS/FAIL] — Trajectory of [Trajectory]'\n"
        "- post_5_whats_happening: A dedicated 1-paragraph explanation of the news event (max 250 chars).\n"
        "- post_6_nuance: Identify the nuance. Use header 'The Bright Side:\\n[nuance]' or 'The Poison:\\n[nuance]'\n"
        "- post_7_breakdown: 'The Breakdown & Plane Error:\\n[Paragraph explaining Plane Error simply, max 250 chars]'\n"
        "- post_8_switch: Expose the forensic test/bait-and-switch naturally (max 250 chars).\n"
        "- post_9_trajectory: 'The Trajectory: Trajectory of [Trajectory]\\nWhen you map the gap between stated intentions and ground-level results...'\n"
        "- post_10_destination: '...it plots a direct trajectory toward [Outcome/Terminal Zone].' followed by a brief 1-sentence mathematical explanation.\n"
        "- post_11_unavoidables: 'The Unavoidable Truth: [truth text]\\n\\nThe Unavoidable Lie: [lie text]'\n"
        "- post_12_reaction: '[Awwthekanon or Brothekanon]:\\n[Concise reaction in their unique voice, under 250 chars]'\n"
        "- post_13_synthesis: 'Aletheia\\'s Synthesis:\\n[Synthesized blended path, max 230 chars]'\n"
        "- post_14_vector: 'Synthesized Resolution Vector:\\nBlended Path: [Blended path summary]\\nFinal Recalculated Coordinates: ([real_u], [real_psi])'\n"
    )
    user_content = f"News Post URL: {post_url}\nNews Post text to evaluate:\n{post_text}"
    print("Initiating Unified Single-Shot Evaluation...")
    response = call_llm(llm_client, system_prompt, user_content, response_format={"type": "json_object"})
    raw_json = json.loads(response)
    
    # Compile the final thread config format
    subject = raw_json["subject"]
    hook = f"Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: {subject}\nSource: {post_url}"
    
    posts = [
        hook,
        raw_json["post_2_claim"],
        raw_json["post_3_reality"],
        raw_json["post_4_verdict"],
        raw_json["post_5_whats_happening"],
        raw_json["post_6_nuance"],
        raw_json["post_7_breakdown"],
        raw_json["post_8_switch"],
        raw_json["post_9_trajectory"],
        raw_json["post_10_destination"],
        raw_json["post_11_unavoidables"],
        raw_json["post_12_reaction"],
        raw_json["post_13_synthesis"],
        raw_json["post_14_vector"]
    ]
    
    return {
        "subject": subject,
        "link": post_url,
        "claim_u": raw_json["claim_u"],
        "claim_psi": raw_json["claim_psi"],
        "real_u": raw_json["real_u"],
        "real_psi": raw_json["real_psi"],
        "mode": "reply",
        "target_url": post_url,
        "posts": posts
    }






def main():
    parser = argparse.ArgumentParser(description="Aletheia Cron Orchestrator Pipeline")
    parser.add_argument("--news-query", required=True, help="Keyword to search in verified feed.")
    parser.add_argument("--feed", default="https://bsky.app/profile/aendra.com/feed/verified-news", help="Custom feed URL.")
    parser.add_argument("--live", action="store_true", help="Post live to Bluesky.")
    args = parser.parse_args()

    llm_client = get_llm_client()

    print(f"Connecting to Bluesky to search feed for query '{args.news_query}'...")
    # Programmatic feed search setup (using search_bsky logic)
    handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
    password = os.environ.get('BSKY_PASSWORD')
    if not password:
        print("ERROR: BSKY_PASSWORD not found.")
        sys.exit(1)

    client = Client()
    try:
        client.login(handle, password)
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

    # 1. Resolve Feed URI
    parts = args.feed.strip("/").split("/")
    feed_handle, feed_rkey = parts[parts.index("profile")+1], parts[parts.index("feed")+1]
    resolver = IdResolver()
    feed_did = resolver.handle.resolve(feed_handle)
    feed_uri = f"at://{feed_did}/app.bsky.feed.generator/{feed_rkey}"

    print(f"Fetching posts from feed: {feed_uri}...")
    feed_data = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 20})
    
    target_post = None
    query_lower = args.news_query.lower()
    for item in feed_data.feed:
        text = getattr(item.post.record, 'text', '')
        if query_lower in text.lower():
            target_post = item.post
            break

    if not target_post:
        print(f"No posts in the feed matched '{args.news_query}'. Exiting gracefully.")
        sys.exit(0)

    author_handle = target_post.author.handle
    rkey = target_post.uri.split('/')[-1]
    post_url = f"https://bsky.app/profile/{author_handle}/post/{rkey}"
    post_text = target_post.record.text

    print(f"\nTARGET POST IDENTIFIED: {post_url}")
    print(f"Text:\n{post_text}\n")

    # 2. Execute Unified Single-Shot LLM Pipeline
    thread_config = run_unified_evaluation(llm_client, post_url, post_text)
    
    # 4. Generate Graph and Publish using functions imported from aletheia_bot.py
    from aletheia_bot import post_thread
    post_thread(client, thread_config, live=args.live)
    print("\nOrchestrator Cron completed successfully!")

if __name__ == "__main__":
    main()
