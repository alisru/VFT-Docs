import os
import json
import re
import urllib.parse
from dotenv import load_dotenv
from google import genai
from google.genai import types

script_dir = os.path.dirname(os.path.abspath(__file__))
stories_dir = os.path.join(script_dir, "stories")

load_dotenv(os.path.join(script_dir, ".env"))
gemini_api_key = os.environ.get("GEMINI_API_KEY")

genai_client = None
if gemini_api_key:
    genai_client = genai.Client(api_key=gemini_api_key, http_options=types.HttpOptions(timeout=90000))

def clean_url(url):
    try:
        parsed = urllib.parse.urlparse(url)
        # Strip query parameters and fragment
        return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    except Exception:
        return url

def get_outlet_name(url):
    from consolidate_roundups import _outlet_name
    return _outlet_name(url)

def get_zone_label(u, psi):
    from consolidate_roundups import _zone_label
    return _zone_label(u, psi)

def get_coord_str(u, psi):
    from consolidate_roundups import _coord_str
    return _coord_str(u, psi)

def strip_numbering(post):
    post = post.strip()
    # Strip things like "1/14 ", "1/ ", "Step 1: ", "1. "
    post = re.sub(r'^\d+/\d+\s*', '', post)
    post = re.sub(r'^Step\s+\d+:\s*', '', post)
    post = re.sub(r'^\d+\.\s*', '', post)
    return post.strip()

def process_roundups():
    for fn in os.listdir(stories_dir):
        if not (fn.startswith("roundup_") and fn.endswith(".json")):
            continue
        path = os.path.join(stories_dir, fn)
        print(f"Processing {fn}...")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cfg = data[0] if isinstance(data, list) else data
        
        # 1. Clean up individual outlet URLs in the config structure
        for o in cfg.get("outlets", []):
            o["url"] = clean_url(o["url"])
            
        posts = cfg.get("posts") or []
        
        # 2. If posts are empty, let's regenerate using Gemini
        if not posts:
            print(f"  Thread is empty. Regenerating via Gemini...")
            if not gemini_api_key:
                print("  ERROR: GEMINI_API_KEY not configured. Skipping regeneration.")
                continue
            
            # Re-build user prompt with cleaned URLs
            outlet_lines = []
            for o in cfg["outlets"]:
                coord = get_coord_str(o["claim_u"], o["claim_psi"])
                real_coord = get_coord_str(o["real_u"], o["real_psi"])
                outlet_lines.append({
                    "outlet": o["name"],
                    "url": o["url"],
                    "subject": o["subject"],
                    "stated_coord": coord,
                    "stated_zone": get_zone_label(o["claim_u"], o["claim_psi"]),
                    "actual_coord": real_coord,
                    "actual_zone": get_zone_label(o["real_u"], o["real_psi"]),
                    "context": o["context_post"],
                })

            claim_coord = get_coord_str(cfg["claim_u"], cfg["claim_psi"])
            real_coord  = get_coord_str(cfg["real_u"], cfg["real_psi"])
            claim_zone  = get_zone_label(cfg["claim_u"], cfg["claim_psi"])
            real_zone   = get_zone_label(cfg["real_u"], cfg["real_psi"])
            verdict     = "PASS" if (cfg["real_u"] or 0) >= 0 else "FAIL"

            outlet_block_desc = "\n".join(
                f'  {o["outlet"]} {o["actual_coord"]} {o["actual_zone"]}  {o["url"]}'
                for o in outlet_lines
            )

            prompt = f"""Write a 14-step Bluesky thread for a Media Roundup covering this event.

EVENT: {cfg['subject']}
OUTLETS COVERED ({len(outlet_lines)} total):
{json.dumps(outlet_lines, indent=2, ensure_ascii=False)}

PACK META-COORDINATES:
  Stated (collective framing): {claim_coord} — {claim_zone}
  Actual (ground reality):     {real_coord}  — {real_zone}
  Verdict: {verdict}

THREAD STRUCTURE — write exactly 14 steps. Call them "steps", not "posts".
CRITICAL RULES:
* NEVER prefix any step with "1/14", "1/", "Step 1:", or any numerical indices. The thread must read as a seamless, organic story.
* Every single string MUST be under 265 characters. Be ruthlessly concise.

Step 1 (Hook): Open with what happened — tell the story as ONE unified event, not N articles. End with 1-2 hashtags. Under 265 chars.

Step 2 (Outlet Judgements): List each outlet with its actual VFT coordinate and URL.
Format each line as: [OutletName] [actual_coord] [zone_label]  [url]
Keep each line short. Under 265 chars total for the whole step.
Example format:
{outlet_block_desc}

Step 3 (Stated Claim): What was the collective media framing? End with: Stated Judgement: {claim_coord} — {claim_zone}

Step 4 (Actual Reality): What is the ground truth of the event? End with: Resulting Judgement: {real_coord} — {real_zone}

Step 5 (Verdict): {verdict} — one punchy sentence explaining the gap between framing and reality.

Step 6 (Context): The full factual context of what happened — unified from all sources, no duplication.

Step 7 (Bright Side): The most accurate or honest element of the coverage — what good journalism looked like here.

Step 8 (Breakdown & Plane Error): Which outlet skewed hardest, how, and why that framing fails the VFT test.

Step 9 (Social Physics Analysis): Direct, plain-English analysis of pack dynamics — why did multiple outlets converge on this framing?

Step 10 (Trajectory): The path this media pack is on. End with the meta-coordinate and zone.

Step 11 (Unavoidable Truth/Lie): Two lines — "The Unavoidable Truth: ..." and "The Unavoidable Lie: ..."

Step 12 (Alethekanon): Formal VFT verdict. Analytical tone.

Step 13 (Awwthekanon): Empathetic take. Start with "Awwthekanon:"

Step 14 (Brothekanon): Casual, blunt take. Start with "Brothekanon:"

OUTPUT: Return only a JSON array of 14 strings. No other text.
"""
            system_prompt = (
                "You are the Master Aletheia Auditor writing a consolidated Media Roundup thread. "
                "Respond ONLY with valid JSON — a single list of exactly 14 strings (one per step). "
                "No commentary, no markdown wrapper, no preamble. "
                "CRITICAL: DO NOT use any numbering like '1/14' or 'Step 1:' at the beginning of posts. "
                "CRITICAL: every string MUST be under 265 characters. Be ruthlessly concise."
            )
            
            try:
                if not genai_client:
                    raise ValueError("Gemini API client not initialized.")
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                )
                response = genai_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=config
                )
                raw = response.text.strip()
                cleaned = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw, flags=re.MULTILINE).strip()
                parsed = json.loads(cleaned)
                if isinstance(parsed, list) and len(parsed) == 14:
                    posts = parsed
                    print("  Regeneration successful!")
                else:
                    print(f"  Regeneration failed: AI returned list of length {len(parsed) if isinstance(parsed, list) else 'N/A'}")
                    continue
            except Exception as e:
                print(f"  Regeneration failed with exception: {e}")
                continue
        
        # 3. Clean up formatting (numbering & URL query params in Step 2)
        cleaned_posts = []
        for i, post in enumerate(posts):
            p = strip_numbering(post)
            if i == 1:
                # Step 2: Outlet Judgements. Let's make sure URLs are cleaned up and formatted nicely.
                lines = []
                # Try to parse individual lines from Step 2
                for line in p.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    # Extract the URL from the line if present
                    url_match = re.search(r'https?://\S+', line)
                    if url_match:
                        full_url = url_match.group(0)
                        clean_u = clean_url(full_url)
                        line = line.replace(full_url, clean_u)
                    lines.append(line)
                p = "\n".join(lines)
            cleaned_posts.append(p)
            
        # Verify post lengths and print warnings
        for idx, cp in enumerate(cleaned_posts):
            if len(cp) > 270:
                print(f"  WARNING: Post {idx+1} is {len(cp)} characters long!")
                
        cfg["posts"] = cleaned_posts
        cfg["status"] = "COMPLETED DRY RUN"
        
        # Write back updated JSON
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Saved updated {fn}")

if __name__ == "__main__":
    process_roundups()
