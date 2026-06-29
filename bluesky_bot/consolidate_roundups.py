"""
consolidate_roundups.py — Post-generation roundup consolidation + thread generation.

Run AFTER google_ai_studio_one_shot.py has evaluated all candidates and
rebuild_registries.py has promoted them to stories/.

For every group of 2–4 draft stories in stories/ that share the same event
(detected via macro_event label, actor overlap, or headline keyword overlap),
this script:

  1. Groups constituent factcheck_*.json files by topic/event
  2. Moves them into  stories/roundup_<slug>/   (companion folder)
  3. Calls the AI to write the unified 13-post roundup thread
  4. Writes  stories/roundup_<slug>.json         (the postable roundup)

The roundup thread is ONE unified story covering the event — not a list of
article summaries — with a dedicated "Outlet Judgements" post formatted as:
    BBC (υ+0.8, ψ+0.8) Trustworthy  https://...
    Guardian (υ+0.4, ψ+0.6) Partially Distorted  https://...

Usage:
    python consolidate_roundups.py [--dry-run] [--min-outlets 2] [--max-outlets 4]
                                   [--model gemini-2.5-flash] [--son]
"""

import os
import sys
import json
import re
import shutil
import argparse
import datetime
import urllib.request
import urllib.parse

# ── paths ─────────────────────────────────────────────────────────────────────
script_dir  = os.path.dirname(os.path.abspath(__file__))
stories_dir = os.path.join(script_dir, "stories")

# ── grouping tunables ─────────────────────────────────────────────────────────
ACTOR_WINDOW_HOURS   = 72
KEYWORD_WINDOW_HOURS = 48
KEYWORD_MIN_MATCH    = 2
MIN_OUTLETS_DEFAULT  = 2
MAX_OUTLETS_DEFAULT  = 4

_STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'has', 'have', 'had', 'that', 'this', 'it', 'he', 'she', 'they', 'we',
    'its', 'his', 'her', 'their', 'our', 'says', 'say', 'said', 'will',
    'after', 'over', 'about', 'into', 'than', 'more', 'new', 'up', 'out',
    'no', 'not', 'all', 'also', 'who', 'how', 'what', 'why', 'when',
    'should', 'could', 'would', 'may', 'can', 'just', 'first', 'last',
    # Additional generic keywords to ignore
    'uk', 'us', 'next', 'year', 'years', 'day', 'days', 'week', 'weeks', 
    'month', 'months', 'time', 'times', 'people', 'country', 'world', 
    'today', 'yesterday', 'tomorrow', 'one', 'two', 'three', 'four', 'five',
    'would', 'could', 'should', 'get', 'got', 'make', 'makes', 'made', 'take',
    'takes', 'took', 'go', 'goes', 'went', 'like', 'look', 'looks', 'back', 'backs'
}

# ── generic words in news filenames ───────────────────────────────────────────
GENERIC_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'has', 'have', 'had', 'that', 'this', 'it', 'he', 'she', 'they', 'we',
    'its', 'his', 'her', 'their', 'our', 'says', 'say', 'said', 'will',
    'after', 'over', 'about', 'into', 'than', 'more', 'new', 'up', 'out',
    'no', 'not', 'all', 'also', 'who', 'how', 'what', 'why', 'when',
    'should', 'could', 'would', 'may', 'can', 'just', 'first', 'last',
    'uk', 'us', 'next', 'year', 'years', 'day', 'days', 'week', 'weeks', 
    'month', 'months', 'time', 'times', 'people', 'country', 'world', 
    'today', 'yesterday', 'tomorrow', 'one', 'two', 'three', 'four', 'five',
    'would', 'could', 'should', 'get', 'got', 'make', 'makes', 'made', 'take',
    'takes', 'took', 'go', 'goes', 'went', 'like', 'look', 'looks', 'back', 'backs',
    'factcheck', 'economic', 'challenges', 'leader', 'leadership', 'pm', 'prime', 
    'minister', 'speculation', 'ruling', 'rises', 'rules', 'court', 'course', 
    'ban', 'bill', 'debt', 'debts', 'plan', 'plans', 'special', 'support', 
    'education', 'school', 'schools', 'reform', 'reforms', 'proposal', 'proposals', 
    'official', 'officials', 'council', 'councils', 'local', 'government', 'state', 
    'states', 'election', 'elections', 'candidate', 'candidates', 'party', 'parties', 
    'national', 'public', 'business', 'news', 'article', 'video', 'analysis', 'speech', 
    'full', 'transition', 'orderly', 'talks', 'seeks', 'wants', 'ambition', 'future',
    'potential', 'policies', 'power', 'chancellor', 'race', 'team', 'who', 'how', 'why',
    'what', 'where', 'when', 'which', 'many', 'much', 'more', 'less', 'most', 'least',
    'clearer', 'becoming', 'clash', 'row', 'scandal', 'charge', 'charges', 'trial',
    'case', 'court', 'judge', 'judges', 'verdict', 'sentence', 'sentencing', 'jail',
    'jailed', 'prison', 'police', 'inquiry', 'investigation', 'probe', 'report',
    'reports', 'finding', 'findings', 'reveals', 'revealed', 'shows', 'shown', 'showed',
    'tax', 'aid', 'gift', 'spending', 'details', 'funds', 'fund', 'oath', 'vows', 'serve'
}

def clean_filename_tokens(filename):
    name = filename[len("factcheck_"):-len(".json")]
    tokens = re.split(r'[-_]', name.lower())
    return {t for t in tokens if t not in GENERIC_WORDS and len(t) >= 3}


# ── VFT integrity tier labels (mirrors google_ai_studio_one_shot.py) ──────────
def _integrity_label(rnet):
    if rnet is None:
        return ""
    if rnet == 1.0:
        return "Absolute Truth"
    if rnet <= 1.5:
        return "Trustworthy"
    if rnet <= 2.0:
        return "Conditionally Sound"
    if rnet <= 5.0:
        return "Partially Distorted"
    if rnet <= 10.0:
        return "Meaningful Distortion"
    if rnet <= 100.0:
        return "Severe Deception"
    return "Baseless Lies"

def _zone_label(u, psi):
    """Return nearest named zone for a (υ, ψ) coordinate."""
    if u is None or psi is None:
        return "Unknown"
    if u >= 0.5 and psi >= 0.5:
        return "Greater Good"
    if u >= 0.5 and psi < 0:
        return "Lesser Good"
    if u < 0 and psi >= 0.5:
        return "Greatest Lie"
    if u < 0 and psi < 0:
        return "Greater Evil"
    return "Neutral"

def _coord_str(u, psi):
    """Format a VFT coordinate pair for display in a post."""
    if u is None or psi is None:
        return "(n/a)"
    sign_u   = "+" if u >= 0 else ""
    sign_psi = "+" if psi >= 0 else ""
    return f"(υ{sign_u}{u:.1f}, ψ{sign_psi}{psi:.1f})"


# ── helpers ───────────────────────────────────────────────────────────────────
def _stem(word):
    w = word.lower().strip()
    # Strip common suffixes
    for suffix in ['ations', 'ation', 'ership', 'ship', 'ings', 'ing', 'eds', 'ed', 's', 'es', 'ly']:
        if w.endswith(suffix) and len(w) - len(suffix) >= 4:
            return w[:-len(suffix)]
    return w

def _anchors(text):
    words = re.findall(r'[a-z0-9]{2,}', text.lower())
    return [_stem(w) for w in words if _stem(w) not in _STOPWORDS]


def _normalize_slug(text):
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')[:80]


OUTLET_MAP = {
    "bbc.co.uk": "BBC", "bbc.com": "BBC",
    "theguardian.com": "The Guardian",
    "guardian.com": "The Guardian",
    "dailymail.co.uk": "Daily Mail",
    "mirror.co.uk": "Daily Mirror",
    "thetimes.co.uk": "The Times",
    "telegraph.co.uk": "The Telegraph",
    "independent.co.uk": "The Independent",
    "sky.com": "Sky News", "news.sky.com": "Sky News",
    "abc.net.au": "ABC Australia",
    "smh.com.au": "SMH",
    "theage.com.au": "The Age",
    "washingtonpost.com": "WaPo",
    "nytimes.com": "NY Times",
    "apnews.com": "AP News",
    "reuters.com": "Reuters",
    "cnn.com": "CNN",
    "foxnews.com": "Fox News",
    "npr.org": "NPR",
    "politico.com": "Politico",
    "theatlantic.com": "The Atlantic",
    "techcrunch.com": "TechCrunch",
    "ft.com": "Financial Times",
    "economist.com": "The Economist",
    "bloomberg.com": "Bloomberg",
    "axios.com": "Axios",
    "vox.com": "Vox",
    "thehill.com": "The Hill",
    "newsweek.com": "Newsweek",
    "time.com": "Time",
}

def _outlet_name(link):
    try:
        host = urllib.parse.urlparse(link).hostname or ""
        host = host.replace("www.", "")
        return OUTLET_MAP.get(host, host.split(".")[0].title())
    except Exception:
        return "Unknown"


def sort_priority(r):
    fn = r["filename"].lower()
    score = 0
    if "resignation" in fn or "resign" in fn:
        score += 10
    if "speech" in fn:
        score += 5
    return (score, r["mtime"])


# ── load & group ──────────────────────────────────────────────────────────────
def load_drafts():
    records = []
    for fn in os.listdir(stories_dir):
        if not (fn.startswith("factcheck_") and fn.endswith(".json")):
            continue
        path = os.path.join(stories_dir, fn)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cfg = data[0] if isinstance(data, list) else data
            posts = cfg.get("posts") or []
            records.append({
                "filename":     fn,
                "path":         path,
                "data":         data,
                "cfg":          cfg,
                "subject":      (cfg.get("subject") or "").strip(),
                "actors":       [a.lower() for a in (cfg.get("actors") or [])],
                "macro":        (cfg.get("macro_event") or "").strip().lower(),
                "mtime":        os.path.getmtime(path),
                "claim_u":      cfg.get("claim_u"),
                "claim_psi":    cfg.get("claim_psi"),
                "real_u":       cfg.get("real_u"),
                "real_psi":     cfg.get("real_psi"),
                "macro_claim_u":   cfg.get("macro_claim_u"),
                "macro_claim_psi": cfg.get("macro_claim_psi"),
                "macro_real_u":    cfg.get("macro_real_u"),
                "macro_real_psi":  cfg.get("macro_real_psi"),
                # post 5 (index 4) = context paragraph; post 6 (index 5) = bright side
                "context_post": posts[4] if len(posts) > 4 else "",
                "link":         cfg.get("link", ""),
                "category":     cfg.get("category", "general"),
                "topic":        cfg.get("topic", ""),
            })
        except Exception as e:
            print(f"  Warning: could not load {fn}: {e}")
    return records


def group_stories(records, actor_win_h, keyword_win_h):
    groups   = []
    assigned = set()

    # Pass 1: exact macro_event match
    macro_buckets = {}
    for r in records:
        if r["macro"] and r["filename"] not in assigned:
            macro_buckets.setdefault(r["macro"], []).append(r)
    for macro, bucket in macro_buckets.items():
        if len(bucket) >= 2:
            group = {r["filename"] for r in bucket}
            groups.append(group)
            assigned.update(group)

    # Pass 2: Shared specific filename tokens
    unassigned = [r for r in records if r["filename"] not in assigned]
    for i, a in enumerate(unassigned):
        if a["filename"] in assigned:
            continue
        tokens_a = clean_filename_tokens(a["filename"])
        if not tokens_a:
            continue
        group = {a["filename"]}
        for b in unassigned[i+1:]:
            if b["filename"] in assigned or b["filename"] in group:
                continue
            tokens_b = clean_filename_tokens(b["filename"])
            common_tokens = tokens_a & tokens_b
            if common_tokens:
                group.add(b["filename"])
        if len(group) >= 2:
            groups.append(group)
            assigned.update(group)

    fn_map = {r["filename"]: r for r in records}
    return [[fn_map[fn] for fn in g] for g in groups]


def derive_slug(group):
    macros = [r["macro"] for r in group if r["macro"]]
    if macros:
        from collections import Counter
        label = Counter(macros).most_common(1)[0][0]
        return "roundup_" + _normalize_slug(label)
    
    # Try to find common anchors
    anchors = None
    for r in group:
        a = set(_anchors(r["subject"]))
        anchors = a if anchors is None else anchors & a
        
    if anchors:
        # Sort by length descending (longest descriptive words first)
        sorted_anchors = sorted(list(anchors), key=len, reverse=True)
        return "roundup_" + _normalize_slug("-".join(sorted_anchors[:3]))
        
    fallback_subj = _normalize_slug(group[0]["subject"])
    return "roundup_" + fallback_subj[:50]


def _unique_slug(base_slug):
    """Return a collision-free slug (appending -2, -3 if necessary)."""
    candidate = base_slug
    counter = 2
    while os.path.exists(os.path.join(stories_dir, f"{candidate}.json")):
        candidate = f"{base_slug}-{counter}"
        counter += 1
    return candidate


# ── AI call ───────────────────────────────────────────────────────────────────
ROUNDUP_SYSTEM_PROMPT = (
    "You are the Master Aletheia Auditor writing a consolidated Media Roundup thread. "
    "Respond ONLY with valid JSON — a single list of exactly 14 strings (one per step). "
    "No commentary, no markdown wrapper, no preamble. "
    "CRITICAL: every string MUST be under 270 characters. Be ruthlessly concise."
)

def _build_roundup_user_prompt(capped, macro_label, avg_claim_u, avg_claim_psi, avg_real_u, avg_real_psi):
    """Build the user message for the roundup thread AI call."""
    outlet_lines = []
    
    # Simple inline clean URL to save space
    def clean_url(url):
        try:
            import urllib.parse
            parsed = urllib.parse.urlparse(url)
            # Strip www., query parameters and fragment
            netloc = parsed.netloc.replace("www.", "")
            return urllib.parse.urlunparse((parsed.scheme, netloc, parsed.path, '', '', ''))
        except Exception:
            return url

    by_outlet = {}
    for r in capped:
        name = _outlet_name(r["link"])
        u_url = clean_url(r["link"])
        coord = _coord_str(r["claim_u"], r["claim_psi"])
        real_coord = _coord_str(r["real_u"], r["real_psi"])
        
        item = {
            "outlet": name,
            "url": u_url,
            "subject": r["subject"],
            "stated_coord": coord,
            "stated_zone": _zone_label(r["claim_u"], r["claim_psi"]),
            "actual_coord": real_coord,
            "actual_zone": _zone_label(r["real_u"], r["real_psi"]),
            "context": r["context_post"],
        }
        outlet_lines.append(item)
        by_outlet.setdefault(name, []).append(item)

    claim_coord = _coord_str(avg_claim_u, avg_claim_psi)
    real_coord  = _coord_str(avg_real_u,  avg_real_psi)
    claim_zone  = _zone_label(avg_claim_u, avg_claim_psi)
    real_zone   = _zone_label(avg_real_u,  avg_real_psi)
    verdict     = "PASS" if (avg_real_u or 0) >= 0 else "FAIL"

    # Build a compact outlet judgement block for post 2 showing stated -> actual coords
    example_lines = []
    for name, items in by_outlet.items():
        stated = items[0]["stated_coord"]
        actual = items[0]["actual_coord"]
        zone = items[0]["actual_zone"]
        urls = " ".join([it["url"] for it in items[:3]])  # list up to 3 URLs
        example_lines.append(f"  {name} {stated} -> {actual} {zone}  {urls}")
    outlet_block_desc = "\n".join(example_lines)

    return f"""Write a 14-step Bluesky thread for a Media Roundup covering this event.

EVENT: {macro_label or capped[0]['subject']}
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

Step 2 (Outlet Judgements): List the audited outlets with their VFT coordinate shift from Stated to Actual (Claim -> Real) and URLs.
Format: Group by outlet to save space. For each outlet, list the name, coordinate transition (Stated -> Actual), actual zone, and a space-separated list of clean URLs (up to 3 URLs).
CRITICAL: You must keep this step under 265 characters total. Do not list duplicate URLs, and use the cleaned short URLs.
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


def call_ai_for_thread(capped, macro_label, avg_claim_u, avg_claim_psi, avg_real_u, avg_real_psi,
                        genai_client, model_name, agnes_api_key):
    """Call the AI to generate the 13-post (actually 14-step) roundup thread. Returns list of 14 strings or None."""
    import time
    user_prompt = _build_roundup_user_prompt(
        capped, macro_label, avg_claim_u, avg_claim_psi, avg_real_u, avg_real_psi
    )

    default_fallbacks = [
        "gemini-3.5-flash",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-3.1-flash-lite",
        "vertex:gemini-3.1-flash-lite",
        "gemini-3-flash-preview",
    ]
    # Keep unique order, trying model_name first
    fallback_models = []
    for m in [model_name] + default_fallbacks:
        if m not in fallback_models:
            fallback_models.append(m)

    if agnes_api_key or os.environ.get("AGNES_API_KEY"):
        fallback_models.append("agnes-2.0-flash")

    print(f"    Fallback models to try: {fallback_models}")

    raw = None
    for model in fallback_models:
        try:
            if model.startswith("agnes"):
                print(f"    Attempting thread generation using Agnes model: {model}...")
                import urllib.request as ureq
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": ROUNDUP_SYSTEM_PROMPT},
                        {"role": "user",   "content": user_prompt},
                    ],
                    "temperature": 0.2,
                }
                req = ureq.Request(
                    "https://apihub.agnes-ai.com/v1/chat/completions",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Authorization": f"Bearer {agnes_api_key}", "Content-Type": "application/json"},
                    method="POST",
                )
                with ureq.urlopen(req, timeout=120) as resp:
                    raw = json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
                print(f"    Thread generation: Agnes ({model}) call successful.")
            elif model.startswith("vertex:"):
                print(f"    Attempting thread generation using Vertex model: {model}...")
                from google import genai as vertex_genai
                from google.genai import types as vertex_types
                
                base_model = model.split(":", 1)[1]
                vertex_key = os.environ.get("VERTEX_API_KEY")
                project_id = os.environ.get("VERTEX_PROJECT_ID", "alethekanon")
                location = os.environ.get("VERTEX_LOCATION", "us-central1")
                
                client_args = {"vertexai": True}
                if vertex_key:
                    client_args["api_key"] = vertex_key
                else:
                    client_args["project"] = project_id
                    client_args["location"] = location
                
                v_client = vertex_genai.Client(**client_args)
                v_safety = [
                    vertex_types.SafetySetting(category='HARM_CATEGORY_HATE_SPEECH', threshold='BLOCK_NONE'),
                    vertex_types.SafetySetting(category='HARM_CATEGORY_HARASSMENT', threshold='BLOCK_NONE'),
                    vertex_types.SafetySetting(category='HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold='BLOCK_NONE'),
                    vertex_types.SafetySetting(category='HARM_CATEGORY_DANGEROUS_CONTENT', threshold='BLOCK_NONE'),
                ]
                config = vertex_types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=8192,
                    system_instruction=ROUNDUP_SYSTEM_PROMPT,
                    safety_settings=v_safety
                )
                response = v_client.models.generate_content(
                    model=base_model,
                    contents=user_prompt,
                    config=config
                )
                raw = response.text.strip()
                print(f"    Thread generation: Vertex ({model}) call successful.")
            else:
                print(f"    Attempting thread generation using Gemini model: {model}...")
                if not genai_client:
                    raise ValueError("Gemini API client not initialized.")
                
                try:
                    from google.generativeai.types import HarmCategory, HarmBlockThreshold
                except ImportError:
                    HarmCategory = None
                    HarmBlockThreshold = None

                safety_settings = None
                if HarmCategory and HarmBlockThreshold:
                    safety_settings = {
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    }
                
                model_instance = genai_client.GenerativeModel(
                    model_name=model,
                    system_instruction=ROUNDUP_SYSTEM_PROMPT,
                )
                response = model_instance.generate_content(
                    user_prompt,
                    request_options={"timeout": 90},
                    safety_settings=safety_settings
                )
                raw = response.text
                print(f"    Thread generation: Gemini ({model}) call successful.")

            # Parse JSON array from response
            if raw:
                cleaned = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip(), flags=re.MULTILINE).strip()
                posts = json.loads(cleaned)
                if isinstance(posts, list) and len(posts) == 14 and all(isinstance(p, str) for p in posts):
                    return posts
                else:
                    raise ValueError(f"AI returned invalid structure (len={len(posts) if isinstance(posts, list) else 'N/A'}, expected 14).")
        except Exception as e:
            print(f"    Model {model} failed: {e}")
            time.sleep(2)

    return None


# ── build roundup JSON ────────────────────────────────────────────────────────
def build_roundup_json(slug, capped, posts_or_none, macro_label):
    outlets = []
    all_actors = set()
    macro_events = set()

    for r in capped:
        outlets.append({
            "name":         _outlet_name(r["link"]),
            "url":          r["link"],
            "filename":     r["filename"],
            "subject":      r["subject"],
            "claim_u":      r["claim_u"],
            "claim_psi":    r["claim_psi"],
            "real_u":       r["real_u"],
            "real_psi":     r["real_psi"],
            "context_post": r["context_post"],
        })
        all_actors.update(r["actors"])
        if r["macro"]:
            macro_events.add(r["macro"])

    def avg(lst):
        lst = [x for x in lst if x is not None]
        return round(sum(lst) / len(lst), 2) if lst else None

    avg_claim_u   = avg(r["claim_u"]   for r in capped)
    avg_claim_psi = avg(r["claim_psi"] for r in capped)
    avg_real_u    = avg(r["real_u"]    for r in capped)
    avg_real_psi  = avg(r["real_psi"]  for r in capped)

    story_id = slug[len("roundup_"):]  # strip prefix for the id field
    subject  = f"Media Roundup: {macro_label or capped[0]['subject']}"
    status   = "COMPLETED DRY RUN" if posts_or_none else "ROUNDUP PENDING THREAD"

    return [{
        "id":           story_id,
        "subject":      subject,
        "roundup":      True,
        "outlets":      outlets,
        "link":         "",
        "target_url":   "",
        "claim_u":      avg_claim_u,
        "claim_psi":    avg_claim_psi,
        "real_u":       avg_real_u,
        "real_psi":     avg_real_psi,
        "macro_event":  macro_label,
        "actors":       sorted(all_actors),
        "category":     capped[0]["category"],
        "topic":        capped[0]["topic"],
        "mode":         "root",
        "posts":        posts_or_none or [],
        "status":       status,
    }]


# ── main consolidation pass ───────────────────────────────────────────────────
def consolidate(dry_run, min_outlets, max_outlets, actor_win, keyword_win,
                genai_client=None, model_name="gemini-3.5-flash", agnes_api_key=None):
    records = load_drafts()
    print(f"Loaded {len(records)} draft stories from stories/")

    groups = group_stories(records, actor_win, keyword_win)
    groups = [g for g in groups if len(g) >= min_outlets]

    # ── Intra-outlet Deduplication Pass ───────────────────────────────────────
    # If a group has multiple stories from the same outlet, we keep only the latest one
    # and move the others to stories/duplicate_discard/
    final_groups = []
    discard_dir = os.path.join(stories_dir, "duplicate_discard")
    
    for group in groups:
        by_outlet = {}
        for r in group:
            outlet = _outlet_name(r["link"])
            by_outlet.setdefault(outlet, []).append(r)
        
        kept_stories = []
        for outlet, stories in by_outlet.items():
            # Sort by priority and then mtime descending
            sorted_stories = sorted(stories, key=sort_priority, reverse=True)
            kept = sorted_stories[0]
            kept_stories.append(kept)
            
            # Discarded ones
            for disc in sorted_stories[1:]:
                if dry_run:
                    print(f"  [DRY RUN] Would discard duplicate intra-outlet story: {disc['filename']} ({outlet})")
                else:
                    os.makedirs(discard_dir, exist_ok=True)
                    dest = os.path.join(discard_dir, disc["filename"])
                    try:
                        shutil.move(disc["path"], dest)
                        print(f"  Discarded duplicate intra-outlet story: {disc['filename']} → duplicate_discard/ ({outlet})")
                    except Exception as de:
                        print(f"  Warning: failed to move duplicate {disc['filename']}: {de}")
        
        # If we still have at least min_outlets (2) from different outlets, keep it as a roundup
        # provided they share at least one common token (avoid transitive bridging of unrelated files)
        if len(kept_stories) >= min_outlets:
            common_tokens = clean_filename_tokens(kept_stories[0]["filename"])
            for r in kept_stories[1:]:
                common_tokens &= clean_filename_tokens(r["filename"])
            
            if common_tokens:
                final_groups.append(kept_stories)
            else:
                print(f"  Roundup dissolved: kept stories { [r['filename'] for r in kept_stories] } do not share a common filename token (transitive bridge dissolved).")
        else:
            if len(kept_stories) == 1:
                # Kept story will post individually
                print(f"  Roundup dissolved for single remaining story: {kept_stories[0]['filename']} (posts individually)")
                
    groups = final_groups

    if not groups:
        print("No roundup groups found. All stories post individually.")
        return 0

    print(f"\nFound {len(groups)} roundup group(s):\n")
    roundups_created = 0

    for gi, group in enumerate(groups, 1):
        # Sort group by priority and then mtime descending
        sorted_group = sorted(group, key=sort_priority, reverse=True)
        capped = sorted_group

        # Derive macro label
        macros = [r["macro"] for r in capped if r["macro"]]
        from collections import Counter
        macro_label = Counter(macros).most_common(1)[0][0].title() if macros else ""

        base_slug = derive_slug(capped)
        slug      = _unique_slug(base_slug)

        print(f"  Group {gi}: {slug}")
        print(f"    Outlets ({len(capped)}):")
        for r in capped:
            name = _outlet_name(r["link"])
            coord = _coord_str(r["real_u"], r["real_psi"])
            print(f"      • [{name}] {coord}  {r['subject'][:60]}")

        if dry_run:
            print(f"    [DRY RUN] Would create: {slug}.json + {slug}/\n")
            continue

        # ── Create companion folder and move constituent stories into it ──────
        companion_dir = os.path.join(stories_dir, slug)
        os.makedirs(companion_dir, exist_ok=True)
        for r in capped:
            dest = os.path.join(companion_dir, r["filename"])
            shutil.move(r["path"], dest)
            print(f"    Moved {r['filename']} → {slug}/")
        # Update paths for AI call (we need the context posts, already in memory)

        # ── Call AI for thread text ───────────────────────────────────────────
        posts = None
        if genai_client is not None or agnes_api_key:
            print(f"    Generating roundup thread via AI...")
            def _avg(lst):
                lst = [x for x in lst if x is not None]
                return round(sum(lst) / len(lst), 2) if lst else None
            avg_cu  = _avg([r["claim_u"]   for r in capped])
            avg_cpsi= _avg([r["claim_psi"] for r in capped])
            avg_ru  = _avg([r["real_u"]    for r in capped])
            avg_rpsi= _avg([r["real_psi"]  for r in capped])
            posts = call_ai_for_thread(
                capped, macro_label, avg_cu, avg_cpsi, avg_ru, avg_rpsi,
                genai_client, model_name, agnes_api_key
            )
            if posts:
                # Warn on character violations
                violations = [(i+1, len(p)) for i, p in enumerate(posts) if len(p) > 270]
                if violations:
                    print(f"    WARNING: char violations at steps {violations}")
                if len(posts) != 14:
                    print(f"    WARNING: expected 14 steps, got {len(posts)}")
            else:
                print(f"    AI thread generation failed — writing stub (posts=[]).")
        else:
            print(f"    No AI client configured — writing stub (posts=[]).")

        # ── Write roundup JSON ────────────────────────────────────────────────
        roundup_data = build_roundup_json(slug, capped, posts, macro_label)
        roundup_json_path = os.path.join(stories_dir, f"{slug}.json")
        with open(roundup_json_path, 'w', encoding='utf-8') as f:
            json.dump(roundup_data, f, indent=2, ensure_ascii=False)
        status = roundup_data[0]["status"]
        print(f"    Created {slug}.json  [{status}]\n")
        roundups_created += 1

    if not dry_run and roundups_created:
        print(f"Consolidation complete — {roundups_created} roundup(s) created.")
        print("Next: run rebuild_registries.py, then post_batch.py.")
    return roundups_created


def main():
    from dotenv import load_dotenv
    if not load_dotenv():
        load_dotenv(os.path.join(script_dir, ".env"))

    parser = argparse.ArgumentParser(description="Consolidate overlapping draft stories into roundup threads.")
    parser.add_argument("--dry-run",       action="store_true",   help="Show groups without moving files or calling AI.")
    parser.add_argument("--min-outlets",   type=int, default=MIN_OUTLETS_DEFAULT)
    parser.add_argument("--max-outlets",   type=int, default=MAX_OUTLETS_DEFAULT)
    parser.add_argument("--actor-window",  type=int, default=ACTOR_WINDOW_HOURS)
    parser.add_argument("--keyword-window",type=int, default=KEYWORD_WINDOW_HOURS)
    parser.add_argument("--model",         type=str, default="gemini-3.5-flash", help="Gemini model for roundup thread generation")
    parser.add_argument("--son",           action="store_true",   help="(reserved — SON scoring not yet implemented for roundups)")
    args = parser.parse_args()

    # Init AI clients
    genai_client   = None
    agnes_api_key  = os.environ.get("AGNES_API_KEY")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if gemini_api_key:
        try:
            import google.generativeai as genai_mod
            genai_mod.configure(api_key=gemini_api_key)
            genai_client = genai_mod
        except Exception as e:
            print(f"Warning: Could not init Gemini client: {e}")

    consolidate(
        dry_run      = args.dry_run,
        min_outlets  = args.min_outlets,
        max_outlets  = args.max_outlets,
        actor_win    = args.actor_window,
        keyword_win  = args.keyword_window,
        genai_client = genai_client,
        model_name   = args.model,
        agnes_api_key= agnes_api_key,
    )


if __name__ == "__main__":
    main()
