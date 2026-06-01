import os
import sys
import json
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from atproto import Client, IdResolver

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_graph import draw_graph
from aletheia_bot import split_text, parse_bsky_url, save_and_sync_story

# Load environment variables
load_dotenv()

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
    fallback_models = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.5-flash"
    ]
    
    last_exception = None
    for model_name in fallback_models:
        max_retries = 2  # Reduced to maximum 2 immediate retries for 503s only
        for retry in range(max_retries):
            try:
                config = genai.types.GenerationConfig(temperature=0.2)
                if response_format and response_format.get("type") == "json_object":
                    config.response_mime_type = "application/json"

                model = client.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_prompt,
                    generation_config=config
                )
                
                response = model.generate_content(user_content)
                result = response.text.strip()
                # Pacing delay to avoid immediate rate limits
                time.sleep(12)
                return result
            except Exception as e:
                last_exception = e
                err_str = str(e).lower()
                
                # CRITICAL TOKEN PRESERVATION: Immediately halt on 429 Quota/ResourceExhausted limits
                if "429" in err_str or "exhausted" in err_str or "quota" in err_str or "limit" in err_str:
                    print(f"\nCRITICAL QUOTA HALT: Hit a 429/ResourceExhausted limit on {model_name}.")
                    print("ABORTING SCRIPT IMMEDIATELY TO PREVENT TOKEN BURNING/INFINITE RETRIES.")
                    sys.exit(1)
                    
                print(f"Transient error on {model_name} (Attempt {retry+1}/{max_retries}): {e}")
                time.sleep(2)
        
        # If we exhausted max_retries for this model without a 429, try the next fallback model
        print(f"Falling back to next model...")

    print(f"CRITICAL: All models failed with non-quota errors. Last error: {last_exception}")
    sys.exit(1)

def run_phase1_baseline(llm_client, post_text):
    system_prompt = (
        "You are Aletheia, a rigorous systemic analyst specialized in the Convergence Test.\n"
        "Analyze the news claim and output a strict JSON block.\n"
        "To fit Bluesky's 300-character limit, each text field MUST be a beautifully written, organic paragraph under 250 characters total. Do NOT use generic or dry summaries.\n\n"
        "Fields to return in JSON:\n"
        "- claim_u, claim_psi (Morality and Will coordinates for the stated claim, range -2.0 to 2.0)\n"
        "- real_u, real_psi (Morality and Will coordinates for the actual reality, range -2.0 to 2.0)\n"
        "- subject (Brief 2-4 word descriptor of the issue)\n"
        "- trajectory (Canonical label: Grace, Fall, Redemption, or Deception)\n"
        "- post_2_claim: The complete text for Post 2 (The Claim). Format exactly as:\n"
        "  'The Claim:\\n[Paragraph explaining stated intent]\\nStated Judgement: ([claim_u], [claim_psi]) — [Coordinate Label]'\n"
        "- post_3_reality: The complete text for Post 3 (The Reality). Format exactly as:\n"
        "  'The Reality:\\n[Paragraph exposing ground-level reality]\\nResulting Judgement: ([real_u], [real_psi]) — [Coordinate Label]'\n"
        "- post_4_verdict: The complete text for Post 4. Format exactly as:\n"
        "  'Verdict: [PASS/FAIL] — Trajectory of [Trajectory]'\n"
        "- post_5_whats_happening: The complete text for Post 5. A dedicated 1-paragraph explanation of the news event in plain English (max 250 chars).\n"
        "- post_6_nuance: The complete text for Post 6.\n"
        "  * If negative/failing story, use header 'The Bright Side:\\n[nuance text]'\n"
        "  * If positive/passing story, use header 'The Poison:\\n[nuance text]'\n"
        "- post_7_breakdown: The complete text for Post 7. Format exactly as:\n"
        "  'The Breakdown & Plane Error:\\n[Paragraph explaining Plane Error and failure simply, max 250 chars]'\n"
        "- post_8_switch: The complete text for Post 8. Expose the forensic test/bait-and-switch naturally (max 250 chars).\n"
        "- post_9_trajectory: The complete text for Post 9. Format exactly as:\n"
        "  'The Trajectory: Trajectory of [Trajectory]\\nWhen you map the gap between stated intentions and ground-level results...'\n"
        "- post_10_destination: The complete text for Post 10. Must start with '...it plots a direct trajectory toward [Outcome/Terminal Zone].' followed by a brief 1-sentence mathematical explanation (max 200 chars).\n"
        "- post_11_unavoidables: The complete text for Post 11. Format exactly as:\n"
        "  'The Unavoidable Truth: [truth text]\\n\\nThe Unavoidable Lie: [lie text]'"
    )
    user_content = f"News Post text to evaluate:\n{post_text}"
    response = call_llm(llm_client, system_prompt, user_content, response_format={"type": "json_object"})
    return json.loads(response)

def run_phase2_concurrent(llm_client, subject, reference_url, post_text, baseline):
    baseline_str = f"Stated Claim: ({baseline['claim_u']}, {baseline['claim_psi']}), Actual Reality: ({baseline['real_u']}, {baseline['real_psi']})"
    
    aww_prompt = (
        "You are Awwthekanon, an idealistic, deeply empathetic AI subagent.\n"
        "1. Write a 1-paragraph reaction expressing your empathetic thoughts on the emotional or community toll of the breakdown.\n"
        "2. Ideate the absolute ethical and empathic north-star solution and find a real-world care/mutual-aid example.\n"
        "Output strict JSON:\n"
        '{"persona": "Awwthekanon", "thoughts": "Your thoughts...", "solution": "Your solution..."}'
    )
    
    bro_prompt = (
        "You are Brothekanon, a highly practical, decentralized, and shortcut-focused AI subagent.\n"
        "1. Write a 1-paragraph reaction expressing your practical thoughts on the physical absurdity of the breakdown.\n"
        "2. Identify the lowest-friction, most practical physical shortcut to approximate Aww's ideal solution.\n"
        "Output strict JSON:\n"
        '{"persona": "Brothekanon", "thoughts": "Your thoughts...", "solution": "Your solution..."}'
    )
    
    aletheia_prompt = (
        "You are Alethekanon, a rigorous, historically focused AI systemic auditor.\n"
        "1. Write a 1-paragraph reaction expressing your analytical thoughts on the structural limits of the breakdown.\n"
        "2. Research historically proven, structured institutional or regulatory solutions.\n"
        "Output strict JSON:\n"
        '{"persona": "Alethekanon", "thoughts": "Your thoughts...", "solution": "Your solution..."}'
    )

    user_payload = f"Subject: {subject}\nBaseline: {baseline_str}\nOriginal News: {post_text}\nLink: {reference_url}"
    
    aww_res = json.loads(call_llm(llm_client, aww_prompt, user_payload, response_format={"type": "json_object"}))
    bro_res = json.loads(call_llm(llm_client, bro_prompt, user_payload, response_format={"type": "json_object"}))
    ale_res = json.loads(call_llm(llm_client, aletheia_prompt, user_payload, response_format={"type": "json_object"}))
    
    return aww_res, bro_res, ale_res

def run_phase3_audit(llm_client, baseline, aww, bro, ale):
    system_prompt = (
        "You are the Master Aletheia Auditor. Review the baseline coordinates and the Phase 2 concurrent peer suggestions.\n"
        "1. Determine which peer subagent—Awwthekanon or Brothekanon—got closest to the synthesised idea.\n"
        "2. Generate Post 12 (peer reaction). Must be under 250 characters and formatted exactly as:\n"
        "  '[Awwthekanon or Brothekanon]:\\n[Concise reaction in their unique voice]'\n"
        "3. Generate Post 13 (Aletheia's synthesis). Must be under 250 characters and formatted exactly as:\n"
        "  'Aletheia\\'s Synthesis:\\n[Synthesized blended path, max 230 chars]'\n"
        "4. Generate Post 14 (Synthesized Resolution Vector). Must be under 250 characters and formatted exactly as:\n"
        "  'Synthesized Resolution Vector:\\nBlended Path: [Blended path summary]\\nFinal Recalculated Coordinates: ([final_u], [final_psi])'\n"
        "Output a strict JSON block containing:\n"
        '- "post_12_reaction": "Exact formatted reaction string"\n'
        '- "post_13_synthesis": "Exact formatted synthesis string"\n'
        '- "post_14_vector": "Exact formatted vector string"\n'
        '- "final_u": Recalculated morality coordinate for the blended path (-2.0 to 2.0)\n'
        '- "final_psi": Recalculated will coordinate for the blended path (-2.0 to 2.0)'
    )
    
    user_payload = json.dumps({
        "baseline": baseline,
        "aww_payload": aww,
        "bro_payload": bro,
        "aletheia_payload": ale
    }, indent=2)
    
    response = call_llm(llm_client, system_prompt, user_payload, response_format={"type": "json_object"})
    return json.loads(response)

def compile_thread(baseline, aww, bro, ale, audit, post_url):
    posts = [
        baseline["post_2_claim"],
        baseline["post_3_reality"],
        baseline["post_4_verdict"],
        baseline["post_5_whats_happening"],
        baseline["post_6_nuance"],
        baseline["post_7_breakdown"],
        baseline["post_8_switch"],
        baseline["post_9_trajectory"],
        baseline["post_10_destination"],
        baseline["post_11_unavoidables"],
        audit["post_12_reaction"],
        audit["post_13_synthesis"],
        audit["post_14_vector"]
    ]

    subject = baseline["subject"]
    hook = f"Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: {subject}\nSource: {post_url}"
    posts.insert(0, hook)

    return {
        "subject": subject,
        "link": post_url,
        "claim_u": baseline["claim_u"],
        "claim_psi": baseline["claim_psi"],
        "real_u": audit["final_u"],
        "real_psi": audit["final_psi"],
        "mode": "reply",
        "target_url": post_url,
        "posts": posts
    }

def evaluate_single_post(llm_client, post_data):
    post_url = post_data["url"]
    post_text = post_data["text"]
    print(f"\nEvaluating: {post_url}...")
    
    try:
        # Phase 1: Baseline
        baseline = run_phase1_baseline(llm_client, post_text)
        
        # Phase 2: Concurrent
        aww, bro, ale = run_phase2_concurrent(llm_client, baseline["subject"], post_url, post_text, baseline)
        
        # Phase 3: Audit
        audit = run_phase3_audit(llm_client, baseline, aww, bro, ale)
        
        # Compile
        thread_config = compile_thread(baseline, aww, bro, ale, audit, post_url)
        thread_config["status"] = "COMPLETED DRY RUN"
        
        # Generate graph locally inside graph_png/ folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bot_graph_dir = os.path.join(script_dir, "graph_png")
        os.makedirs(bot_graph_dir, exist_ok=True)
        
        subject_slug = thread_config["subject"].lower().replace(" ", "_").replace("/", "_")
        graph_base_filename = f"{subject_slug}_graph.png"
        graph_filename = os.path.join(bot_graph_dir, graph_base_filename)
        
        draw_graph(
            thread_config["claim_u"], thread_config["claim_psi"],
            thread_config["real_u"], thread_config["real_psi"],
            f"Assessment: {thread_config['subject']}",
            graph_filename
        )
        
        # Copy graph to _Generated_Content/graph_png/
        root_dir = os.path.dirname(script_dir)
        gen_graph_dir = os.path.join(root_dir, "_Generated_Content", "graph_png")
        os.makedirs(gen_graph_dir, exist_ok=True)
        gen_graph_path = os.path.join(gen_graph_dir, graph_base_filename)
        
        try:
            import shutil
            shutil.copy(graph_filename, gen_graph_path)
            thread_config["graph_img"] = f"graph_png/{graph_base_filename}"
        except Exception as e:
            print(f"Warning: Failed to copy graph image: {e}")
            thread_config["graph_img"] = f"graph_png/{graph_base_filename}"
            
        # Save JSON and update registries using our core system
        save_and_sync_story(thread_config)
        print(f"SUCCESS: Synthesized thread for '{thread_config['subject']}' completed.")
        return True
    except Exception as e:
        print(f"ERROR: Failed to evaluate post: {e}")
        return False

def harvest_news_candidates():
    print("Connecting to Bluesky to harvest verified news posts...")
    handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
    password = os.environ.get('BSKY_PASSWORD')
    if not password:
        print("ERROR: BSKY_PASSWORD not found.")
        sys.exit(1)

    client = Client()
    try:
        client.login(handle, password)
        print("Authenticated with Bluesky successfully!")
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

    # Fetch from standard news feed
    feed_url = "https://bsky.app/profile/aendra.com/feed/verified-news"
    parts = feed_url.strip("/").split("/")
    feed_handle, feed_rkey = parts[parts.index("profile")+1], parts[parts.index("feed")+1]
    
    resolver = IdResolver()
    feed_did = resolver.handle.resolve(feed_handle)
    feed_uri = f"at://{feed_did}/app.bsky.feed.generator/{feed_rkey}"

    print(f"Retrieving recent items from feed: {feed_uri}...")
    feed_data = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 30})
    
    candidates = []
    seen_links = set()
    
    for item in feed_data.feed:
        text = getattr(item.post.record, 'text', '').strip()
        author_handle = item.post.author.handle
        rkey = item.post.uri.split('/')[-1]
        post_url = f"https://bsky.app/profile/{author_handle}/post/{rkey}"
        
        # Filter: Must be long enough to have substance
        if len(text) < 40:
            continue
            
        # Filter out common chatty/non-news items
        if text.startswith('@') or text.startswith('Alethekanon'):
            continue
            
        candidates.append({
            "url": post_url,
            "text": text
        })
        seen_links.add(post_url)
        
        # We need precisely 5 candidate items
        if len(candidates) >= 5:
            break
            
    print(f"Harvested {len(candidates)} news posts for dry run evaluation.")
    return candidates

def main():
    llm_client = get_llm_client()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cand_path = os.path.join(os.path.dirname(script_dir), "scratch", "harvested_candidates.json")
    
    if os.path.exists(cand_path):
        print(f"Loading harvested candidates from {cand_path}...")
        with open(cand_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)
    else:
        candidates = harvest_news_candidates()
    
    if not candidates:
        print("No candidates found. Exiting.")
        sys.exit(0)
        
    print("\n--- INITIATING BATCH EVALUATION PIPELINE (DRY-RUNS ONLY) ---")
    
    # Process sequentially to avoid Free Tier concurrent rate limits (5 RPM)
    results = []
    for i, candidate in enumerate(candidates, 1):
        print(f"\nProcessing Story {i}/{len(candidates)}...")
        res = evaluate_single_post(llm_client, candidate)
        results.append(res)
        
        # Cooldown sleep between stories to stay safely within Free Tier limits
        if i < len(candidates):
            print("\nCooling down for 15s to respect Gemini API rate limits...")
            time.sleep(15)
        
    success_count = sum(1 for r in results if r)
    print(f"\nBatch orchestration complete! Successfully dry-ran {success_count}/{len(candidates)} stories.")

if __name__ == "__main__":
    main()
