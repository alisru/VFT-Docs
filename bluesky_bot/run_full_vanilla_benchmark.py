import os, sys, json, time, urllib.request, re
from html import unescape
from google import genai

# Load .env
env_file = os.path.join("bluesky_bot", ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

vertex_key = os.environ.get("VERTEX_API_KEY")
project_id = os.environ.get("VERTEX_PROJECT_ID", "alethekanon")
location = os.environ.get("VERTEX_LOCATION", "us-central1")

client_args = {"vertexai": True}
if vertex_key:
    client_args["api_key"] = vertex_key
else:
    client_args["project"] = project_id
    client_args["location"] = location

client = genai.Client(**client_args)

def extract_full_clean_article(html):
    html = re.sub(r'<(script|style|head|nav|footer|header|svg|noscript|form|aside)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<(p|br|div|h[1-6]|li|article|section)[^>]*>', '\n', html, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = unescape(text)
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 25]
    clean_lines = []
    for l in lines:
        l_lower = l.lower()
        if any(skip in l_lower for skip in ['skip to news navigation', 'skip to navigation', 'cookie policy', 'privacy policy', 'terms of service', 'sign up for our newsletter', 'all rights reserved']):
            continue
        clean_lines.append(l)
    return '\n\n'.join(clean_lines)

target_files = [
    'factcheck_ai_police_face_screening_trial_sparks_privacy_concern_107009644.json',
    'factcheck_amazon_deforestation_hits_13_year_low.json',
    'factcheck_apple-external-link-commission.json',
    'factcheck_act-recriminalising-methamphetamine-ignores-evidence-advocates.json',
    'factcheck_ai_store_manager_fires_employee.json',
    'factcheck_aukus_sovereignty_audit.json',
    'factcheck_anthropic-export-ban.json',
    'factcheck_alzheimers-sleep-restoration-breakthrough.json',
    'factcheck_aluminium_smelter_bailout_2026.json',
    'factcheck_aipac-didnt-always-spend-on-campaigns-now-it-faces-criticism-over-money-in-politics.json'
]

results = []
print(f"Starting 100% FULL UNTRUNCATED benchmark on Vertex Gemini 3.7 Flash...")

for idx, fname in enumerate(target_files, 1):
    fpath = os.path.join("bluesky_bot", "stories", "live", fname)
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
        d = data[0] if isinstance(data, list) else data

    story_id = d.get("id", fname)
    url = d.get("link", "")
    subject = d.get("subject", "")
    structured_real_u = d.get("real_u")
    structured_real_psi = d.get("real_psi")
    structured_real_z = d.get("real_z")
    structured_real_rnet = d.get("real_rnet")
    structured_posts = d.get("posts", [])

    print(f"[{idx}/10] Extracting FULL text for: {story_id[:35]}...")
    full_article_text = ""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            full_article_text = extract_full_clean_article(html)
    except Exception as e:
        print(f"      Scrape error ({e})")

    print(f"      Full Article Length: {len(full_article_text)} characters")

    # The 100% pure vanilla prompt with FULL untruncated article text
    full_prompt = f"Judge this story:\n\nURL: {url}\nTitle: {subject}\n\n{full_article_text}"

    t0 = time.time()
    try:
        resp = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=full_prompt
        )
        vanilla_response = resp.text
        latency = round(time.time() - t0, 2)
        print(f"      API Completed ({latency}s, {len(vanilla_response)} chars response)")
    except Exception as api_err:
        print(f"      API Error: {api_err}")
        vanilla_response = f"ERROR: {api_err}"
        latency = 0.0

    results.append({
        "index": idx,
        "id": story_id,
        "filename": fname,
        "title": subject,
        "url": url,
        "full_article_char_count": len(full_article_text),
        "vft_framework_audit": {
            "real_u": structured_real_u,
            "real_psi": structured_real_psi,
            "real_z": structured_real_z,
            "real_rnet": structured_real_rnet,
            "posts": structured_posts[:4]
        },
        "vanilla_gemini_3_7_flash": {
            "prompt_sent": full_prompt,
            "raw_judgment": vanilla_response,
            "latency_sec": latency
        }
    })
    time.sleep(1)

out_file = os.path.join("bluesky_bot", "tests", "vanilla_benchmark_10_stories.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nAll 10 FULL UNTRUNCATED benchmark stories saved to {out_file}!")