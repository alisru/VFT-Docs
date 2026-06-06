import os
import sys
import json
import re
import time
import argparse
import urllib.request
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from atproto import Client, IdResolver

# Resolve workspace directory
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(script_dir)
sys.path.append(script_dir)

from generate_graph import draw_graph
from aletheia_bot import save_and_sync_story

# Import rebuild_registries logic
from rebuild_registries import rebuild_registries

# Load environment variables
bot_env_path = os.path.join(script_dir, ".env")
load_dotenv(bot_env_path)

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# --- 0. HELPER FUNCTIONS FOR TOKEN MINIFICATION & ALTERNATIVE API ---
def minify_markdown(text):
    # Remove markdown link references e.g. [name](url) -> name
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove markdown alerts (e.g. > [!NOTE])
    text = re.sub(r'>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', '', text)
    
    # Process lines
    lines = [line.strip() for line in text.split('\n')]
    filtered_lines = []
    
    for line in lines:
        # Strip HTML/Markdown comments
        if line.startswith('<!--') or line.endswith('-->'):
            continue
        # Remove pure dividers
        if line.replace('-', '').strip() == '':
            continue
        # Skip empty lines
        if not line:
            continue
        
        filtered_lines.append(line)
        
    return '\n'.join(filtered_lines)

def call_agnes_api(api_key, system_prompt, user_content, model="agnes-2.0-flash"):
    url = "https://apihub.agnes-ai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.15
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        print(f"Posting request to Agnes AI API endpoint with model: {model}...")
        with urllib.request.urlopen(req, timeout=180) as response:
            res_data = json.loads(response.read().decode("utf-8"))
        print("Agnes AI API call successful!")
        return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling Agnes AI API: {e}")
        raise e

def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY environment variable not found. Gemini models will be unavailable.")
        return None
    if genai is None:
        print("Warning: Google Generative AI SDK is not installed. Gemini models will be unavailable.")
        return None
    genai.configure(api_key=api_key)
    return genai

# --- 1. HISTORICAL STORIES LOADING & DEDUPLICATION ---
def load_historical_evaluations():
    seen_urls = set()
    seen_ids = set()
    bot_stories_dir = os.path.join(script_dir, "stories")
    
    if os.path.exists(bot_stories_dir):
        try:
            story_files = [f for f in os.listdir(bot_stories_dir) if f.startswith('factcheck_') and f.endswith('.json')]
            for sf in story_files:
                filepath = os.path.join(bot_stories_dir, sf)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                config = data[0] if isinstance(data, list) else data
                
                url = config.get("link") or config.get("target_url")
                if url:
                    seen_urls.add(url.strip().lower())
                story_id = config.get("id")
                if story_id:
                    seen_ids.add(story_id.strip().lower())
            print(f"Loaded {len(seen_urls)} historical URLs and {len(seen_ids)} historical story IDs.")
        except Exception as e:
            print(f"Warning: Failed to load historical evaluations: {e}")
    return seen_urls, seen_ids

def extract_external_link(post):
    record = getattr(post, 'record', None)
    if record:
        embed = getattr(record, 'embed', None)
        if embed and hasattr(embed, 'external'):
            ext = getattr(embed, 'external', None)
            if ext and hasattr(ext, 'uri'):
                return ext.uri
    facets = getattr(record, 'facets', None) or []
    for facet in facets:
        features = getattr(facet, 'features', [])
        for feature in features:
            if hasattr(feature, 'uri'):
                return feature.uri
    embed_view = getattr(post, 'embed', None)
    if embed_view and hasattr(embed_view, 'external'):
        ext = getattr(embed_view, 'external', None)
        if ext and hasattr(ext, 'uri'):
            return ext.uri
    text = getattr(record, 'text', '') if record else ""
    url_match = re.search(r'(https?://[^\s]+)', text)
    if url_match:
        return url_match.group(1)
    return None

# --- 2. CANDIDATE HARVESTING ---
def harvest_news(target_rss, target_bsky, seen_urls, seen_ids):
    candidates = []
    
    # Harvest RSS
    if target_rss > 0:
        print(f"\nHarvesting from RSS feeds (Target: {target_rss})...")
        rss_feeds = [
            {"name": "BBC News", "url": "http://feeds.bbci.co.uk/news/rss.xml"},
            {"name": "NYT Home", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"}
        ]
        
        for feed in rss_feeds:
            if len([c for c in candidates if c["mode"] == "root"]) >= target_rss:
                break
            print(f"Fetching from {feed['name']} RSS feed: {feed['url']}...")
            req = urllib.request.Request(feed['url'], headers={'User-Agent': 'Mozilla/5.0'})
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    content = response.read()
                root = ET.fromstring(content)
                items = root.findall('.//item')
                print(f"Found {len(items)} items in {feed['name']}.")
                
                for item in items:
                    if len([c for c in candidates if c["mode"] == "root"]) >= target_rss:
                        break
                    title = item.find('title')
                    desc = item.find('description')
                    link = item.find('link')
                    
                    title_text = title.text.strip() if title is not None and title.text else ""
                    desc_text = desc.text.strip() if desc is not None and desc.text else ""
                    link_text = link.text.strip() if link is not None and link.text else ""
                    
                    if not title_text or not link_text:
                        continue
                        
                    desc_cleaned = re.sub(r'<[^>]*>', '', desc_text)
                    text_body = f"{title_text}\n\n{desc_cleaned}"
                    
                    if len(text_body) < 45:
                        continue
                    if link_text.strip().lower() in seen_urls:
                        continue
                    subject_approx = title_text[:30].lower().replace(" ", "_").replace("/", "_")
                    if subject_approx in seen_ids:
                        continue
                        
                    candidates.append({
                        "url": link_text,
                        "target_url": "",
                        "mode": "root",
                        "text": text_body,
                        "subject": title_text
                    })
                    seen_urls.add(link_text.strip().lower())
            except Exception as e:
                print(f"Warning: Failed to fetch {feed['name']} RSS: {e}")

    # Harvest Bluesky
    if target_bsky > 0:
        print(f"\nHarvesting from Bluesky feeds (Target: {target_bsky})...")
        handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
        password = os.environ.get('BSKY_PASSWORD')
        
        if password:
            client = Client()
            try:
                client.login(handle, password)
                resolver = IdResolver()
                
                bsky_feeds = [
                    "https://bsky.app/profile/aendra.com/feed/verified-news",
                    "https://bsky.app/profile/aendra.com/feed/news-2-0"
                ]
                
                english_words = re.compile(r'\b(the|with|they|have|what|which|there|their|about|would|could)\b', re.IGNORECASE)
                
                for feed_url in bsky_feeds:
                    if len([c for c in candidates if c["mode"] == "reply"]) >= target_bsky:
                        break
                    print(f"Fetching from feed: {feed_url}...")
                    parts = feed_url.strip("/").split("/")
                    feed_handle, feed_rkey = parts[parts.index("profile")+1], parts[parts.index("feed")+1]
                    feed_did = resolver.handle.resolve(feed_handle)
                    feed_uri = f"at://{feed_did}/app.bsky.feed.generator/{feed_rkey}"
                    
                    feed_data = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 60})
                    
                    for item in feed_data.feed:
                        if len([c for c in candidates if c["mode"] == "reply"]) >= target_bsky:
                            break
                        text = getattr(item.post.record, 'text', '').strip()
                        author_handle = item.post.author.handle
                        rkey = item.post.uri.split('/')[-1]
                        post_url = f"https://bsky.app/profile/{author_handle}/post/{rkey}"
                        
                        if len(text) < 45 or text.startswith('@') or text.startswith('Alethekanon'):
                            continue
                        if "PINNED POST" in text or "News feeds" in text or "Every feed I run" in text:
                            continue
                        if any(domain in post_url for domain in ['zeit.de', 'tijd.be', 'sapo.pt', 'demorgen.be', 'folha.com', 'nu.nl', 'gazeteoksijen.com', 'graze.social']):
                            continue
                        if not english_words.search(text):
                            continue
                            
                        article_url = extract_external_link(item.post) or post_url
                        
                        if article_url.strip().lower() in seen_urls:
                            continue
                        subject_approx = text[:30].lower().replace(" ", "_").replace("/", "_")
                        if subject_approx in seen_ids:
                            continue
                            
                        candidates.append({
                            "url": article_url,
                            "target_url": post_url,
                            "mode": "reply",
                            "text": text,
                            "subject": text[:80] + "..."
                        })
                        seen_urls.add(article_url.strip().lower())
            except Exception as e:
                print(f"Warning: Bluesky login or retrieval failed: {e}")
        else:
            print("Warning: BSKY_PASSWORD not found. Skipping Bluesky harvesting.")
            
    return candidates

# --- 3. EXECUTE SINGLE-SHOT BATCH EVALUATION VIA GOOGLE AI STUDIO API ---
def run_one_shot_evaluations(genai_client, candidates, model_name, agnes_api_key=None):
    # Load rules and guidelines
    convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_lite.md")
    formatting_path = os.path.join(script_dir, "instructions", "thread_formatting.md")
    
    with open(convergence_path, "r", encoding="utf-8") as f:
        convergence_rules = minify_markdown(f.read())
    with open(formatting_path, "r", encoding="utf-8") as f:
        formatting_rules = minify_markdown(f.read())
        
    # System prompt: pure role declaration only
    system_instruction = "You are the Master Aletheia Auditor. Respond ONLY with the exact delimited data rows requested. No commentary, no markdown, no preamble, no explanation."

    # Build the full user message: rules + candidates + strict output demand
    output_format = (
        "OUTPUT FORMAT — YOUR ENTIRE RESPONSE MUST BE ONLY THIS, NOTHING ELSE:\n"
        "Line 1 (header, exact):\n"
        "idþsubjectþlinkþtarget_urlþclaim_uþclaim_psiþreal_uþreal_psiþmodeþposts\n"
        "Then one line per story. Rules:\n"
        "- Columns separated by þ (Thorn U+00FE). NEVER use þ inside column text.\n"
        "- 'posts' column = exactly 14 post strings joined by ¶ (Pilcrow U+00B6). NEVER use ¶ inside post text.\n"
        "- Escape ALL real newlines inside posts as the two characters \\n so each story fits on ONE output line.\n"
        "- Every post must be under 250 characters.\n"
        "- Do NOT output blank lines, bullet points, character counts, commentary, markdown, or any text that is not a data row.\n\n"
        "EXAMPLE (one story, shortened):\n"
        "my_slug_idþStory TitleþhttpsURLþþ1.0þ0.0þ-1.0þ-1.0þrootþHook text here.\\nEvidence: a, b, c¶Claim text.\\nStated Judgement: (+1.0, 0.0) — Good Preference¶Reality text.\\nResulting Judgement: (-1.0, -1.0) — Greater Evil¶Verdict: FAIL — The Path of Deception.\\nExplanation.¶Context paragraph.¶The Bright Side:\\nNuance.¶The Breakdown & Plane Error:\\nExplanation.¶The Trajectory: The Path of Deception.\\nWhen you map the gap...¶...it plots a direct trajectory toward Greater Evil.¶The Unavoidable Truth: truth.\\n\\nThe Unavoidable Lie: lie.¶Alethekanon:\\nAnalysis.¶Awwthekanon:\\nEmpathy.¶Brothekanon:\\nCasual take.¶Synthesized Resolution Vector:\\nBlended Path: summary.\\nFinal Recalculated Coordinates: (-1.0, -1.0)\n"
    )

    user_payload_str = (
        f"=== CONVERGENCE TEST RULES ===\n{convergence_rules}\n\n"
        f"=== THREAD FORMATTING & SCHEMAS ===\n{formatting_rules}\n\n"
        f"=== CANDIDATES TO EVALUATE ===\n{json.dumps(candidates, indent=2)}\n\n"
        f"{output_format}"
    )
    
    # Try the specified model, fallback if rate-limited or fails
    default_fallbacks = [
        "gemini-3.5-flash",
        "gemini-3-flash",
        "gemini-3.1-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash"
    ]
    # Keep unique order, trying model_name first
    fallback_models = []
    for m in [model_name] + default_fallbacks:
        if m not in fallback_models:
            fallback_models.append(m)
            
    # Append Agnes AI at the very end of fallback list if key exists
    if agnes_api_key or os.environ.get("AGNES_API_KEY"):
        fallback_models.append("agnes-2.0-flash")
        
    last_exception = None
    
    for model in fallback_models:
        print(f"Attempting batch evaluation call using model: {model}...")
        try:
            if model.startswith("agnes"):
                key = agnes_api_key or os.environ.get("AGNES_API_KEY")
                return call_agnes_api(key, system_instruction, user_payload_str, model=model)
            else:
                if not genai_client:
                    raise ValueError("Gemini API client not initialized.")
                config = genai_client.types.GenerationConfig(
                    temperature=0.15,
                    max_output_tokens=8192
                )
                model_instance = genai_client.GenerativeModel(
                    model_name=model,
                    system_instruction=system_instruction,
                    generation_config=config
                )
                response = model_instance.generate_content(user_payload_str)
                result_text = response.text.strip()
                print(f"API call successful with model: {model}")
                return result_text
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "exhausted" in err_str or "quota" in err_str:
                print(f"Rate limited or quota exhausted on model {model}. Trying fallback...")
            else:
                print(f"Warning: Model {model} failed: {e}")
            last_exception = e
            time.sleep(2)
            
    print(f"CRITICAL: All models failed in one-shot batch evaluation. Last error: {last_exception}")
    sys.exit(1)

def transpose_flat_to_json(flat_text):
    # Try to extract the block between <result> and </result>
    result_match = re.search(r'<result>(.*?)</result>', flat_text, re.DOTALL)
    if result_match:
        content_to_parse = result_match.group(1).strip()
    else:
        # Fallback to the whole text if tags are missing
        content_to_parse = flat_text.strip()
        
    lines = content_to_parse.split('\n')
    if not lines or len(lines) < 2:
        return []
        
    # Ignore any markdown fences if the model outputted them
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
        
    if not lines:
        return []
        
    # Find the header line: must contain 'idþ' AND at least 5 þ separators
    header_idx = -1
    for idx, l in enumerate(lines):
        if 'idþ' in l and l.count('þ') >= 5:
            header_idx = idx
            break

    if header_idx == -1:
        # Hard fail — don't silently assume a header and parse garbage
        print("ERROR: Could not find a valid header row (expected 'idþsubjectþ...') in model output.")
        print("--- RAW MODEL OUTPUT (first 500 chars) ---")
        print(flat_text[:500])
        print("------------------------------------------")
        return []
    else:
        header = [h.strip() for h in lines[header_idx].split('þ')]
        data_lines = lines[header_idx + 1:]
        
    evaluations = []
    for line in data_lines:
        if not line.strip():
            continue
        cols = [c.strip() for c in line.split('þ')]
        if len(cols) < len(header):
            print(f"Warning: Skipping malformed row (found {len(cols)} columns, expected {len(header)}): {line}")
            continue
            
        story = dict(zip(header, cols))
        
        try:
            story["claim_u"] = float(story["claim_u"])
            story["claim_psi"] = float(story["claim_psi"])
            story["real_u"] = float(story["real_u"])
            story["real_psi"] = float(story["real_psi"])
            
            raw_posts = story["posts"].split('¶')
            story["posts"] = [p.replace('\\n', '\n') for p in raw_posts]
            story["status"] = "COMPLETED DRY RUN"
            evaluations.append(story)
        except Exception as e:
            print(f"Warning: Failed to parse row {line}: {e}")
            continue
            
    return evaluations

# --- 4. GRAPH GENERATION AND SAVING ---
def process_evaluations(evaluations):
    success_count = 0
    os.makedirs(os.path.join(script_dir, "graph_png"), exist_ok=True)
    
    for story in evaluations:
        try:
            slug = story.get("id") or story.get("subject").lower().replace(" ", "_").replace("/", "_")
            # Sanitize slug to remove forbidden characters for Windows paths
            for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
                slug = slug.replace(char, '')
            story["id"] = slug
            story["status"] = "COMPLETED DRY RUN"
            
            # Post validation check
            posts = story.get("posts", [])
            if len(posts) != 14:
                print(f"ERROR: Story '{story.get('subject')}' has {len(posts)} posts instead of 14! Skipping.")
                continue
                
            char_violations = []
            for idx, post in enumerate(posts):
                if len(post) > 250:
                    char_violations.append((idx, len(post)))
            if char_violations:
                print(f"WARNING: Story '{story.get('subject')}' has character limit violations: {char_violations}")
                
            print(f"Processing story: {story.get('subject')} ({slug})...")
            
            # 1. Draw graph
            graph_base = f"{slug}_graph.png"
            graph_bot_path = os.path.join(script_dir, "graph_png", graph_base)
            
            title = f"Assessment: {story['subject']}"
            draw_graph(story["claim_u"], story["claim_psi"], story["real_u"], story["real_psi"], title, graph_bot_path)
            
            story["graph_img"] = f"graph_png/{graph_base}"
            
            # 2. Save JSON and sync registry
            save_and_sync_story(story)
            success_count += 1
            print(f"Successfully saved and synced story config: {slug}")
        except Exception as e:
            print(f"ERROR: Failed to process evaluation for story: {story.get('subject')}. Error: {e}")
            
    return success_count

def main():
    parser = argparse.ArgumentParser(description="Google AI Studio One-Shot Batch Evaluator")
    parser.add_argument("--rss", type=int, default=5, help="Number of RSS stories to harvest (default: 5)")
    parser.add_argument("--bsky", type=int, default=15, help="Number of Bluesky stories to harvest (default: 15)")
    parser.add_argument("--model", type=str, default="gemini-3.5-flash", help="Generative model to use (default: gemini-3.5-flash)")
    parser.add_argument("--chunk-size", type=int, default=6, help="Number of stories to process per API call (default: 6)")
    args = parser.parse_args()
    
    print("=" * 80)
    print("GOOGLE AI STUDIO ONE-SHOT BATCH EVALUATOR")
    print("=" * 80)
    
    seen_urls, seen_ids = load_historical_evaluations()
    
    candidates = harvest_news(args.rss, args.bsky, seen_urls, seen_ids)
    if not candidates:
        print("\nNo new, non-duplicate candidates found. Exiting.")
        sys.exit(0)
        
    print(f"\nHarvested {len(candidates)} total candidates.")
    
    # Save a temporary copy of candidates for debugging/safety
    scratch_candidates_path = os.path.join(workspace_dir, "scratch", "harvested_candidates.json")
    with open(scratch_candidates_path, "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)
    print(f"Saved raw harvested candidates to {scratch_candidates_path}")
    
    genai_client = get_gemini_client()
    agnes_api_key = os.environ.get("AGNES_API_KEY")
    
    # Calculate simple token savings metrics
    convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_lite.md")
    formatting_path = os.path.join(script_dir, "instructions", "thread_formatting.md")
    with open(convergence_path, "r", encoding="utf-8") as f:
        raw_ct = len(f.read())
    with open(formatting_path, "r", encoding="utf-8") as f:
        raw_tf = len(f.read())
    
    min_ct = len(minify_markdown(open(convergence_path, "r", encoding="utf-8").read()))
    min_tf = len(minify_markdown(open(formatting_path, "r", encoding="utf-8").read()))
    
    raw_total_chars = raw_ct + raw_tf
    min_total_chars = min_ct + min_tf
    percent_saved = (1.0 - (min_total_chars / raw_total_chars)) * 100
    
    print(f"\n--- PROMPT TOKENS MINIFICATION ---")
    print(f"Raw instructions size:      {raw_total_chars} characters (~{int(raw_total_chars/4)} tokens)")
    print(f"Minified instructions size: {min_total_chars} characters (~{int(min_total_chars/4)} tokens)")
    print(f"Total instructions token budget saved: {percent_saved:.1f}%")
    print(f"----------------------------------\n")
    
    # Process candidates in chunks
    chunk_size = args.chunk_size
    all_evaluations = []
    
    for i in range(0, len(candidates), chunk_size):
        chunk = candidates[i:i + chunk_size]
        print(f"\nEvaluating chunk {i // chunk_size + 1}/{(len(candidates) + chunk_size - 1) // chunk_size} ({len(chunk)} candidates)...")
        
        try:
            raw_text = run_one_shot_evaluations(genai_client, chunk, args.model, agnes_api_key=agnes_api_key)
            chunk_evals = transpose_flat_to_json(raw_text)
            print(f"Successfully parsed {len(chunk_evals)} evaluations from chunk.")
            all_evaluations.extend(chunk_evals)
        except Exception as pe:
            print(f"Error processing chunk: {pe}")
            # Continue to next chunk to recover gracefully
            time.sleep(2)
            
    print(f"\nReceived {len(all_evaluations)} total evaluations across all chunks.")
    if not all_evaluations:
        print("ERROR: No evaluations returned across all chunks. Exiting.")
        sys.exit(1)
        
    success_count = process_evaluations(all_evaluations)
    print(f"\nSuccessfully processed {success_count}/{len(all_evaluations)} evaluations.")
    
    print("\nRebuilding registries...")
    rebuild_registries()
    print("Registries successfully rebuilt.")
    print("\nOne-Shot Batch Evaluation Pipeline Completed Successfully!")

if __name__ == "__main__":
    main()
