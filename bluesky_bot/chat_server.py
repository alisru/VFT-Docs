"""chat_server.py — Local AI Chatbot Server for Aletheia Bot & VFT Ecosystem.

Provides multi-model inference (Google Cloud Vertex AI default & Gemini API),
hierarchical topic threading (conversation branching with parent inheritance),
dual-track infinite context assembly (Narrative Spine + SQLite archive search),
and full thinking/output controls.

Port: 8766
"""
import os
import sys
import glob
import json
import uuid
import datetime
import urllib.parse
import re
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(script_dir)
SCRIPT_DIR = script_dir
load_dotenv(os.path.join(script_dir, ".env"))

# Import local SQLite memory engine
sys.path.insert(0, script_dir)
try:
    import memory_store
    memory_store.init_database()
except Exception as e:
    memory_store = None
    print(f"Warning: memory_store failed to initialize: {e}")

# Try importing the official google-genai SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    print("Warning: 'google-genai' SDK is not installed. Live LLM calls will fail. Run: pip install google-genai", file=sys.stderr)

PORT = 8766
STORIES_DIR = os.path.join(script_dir, "stories")
LIVE_DIR = os.path.join(STORIES_DIR, "live")
DARKROOM_DIR = os.path.join(STORIES_DIR, "darkroom")
POLICY_LEDGER_PATH = os.path.join(script_dir, "policy_ledger.json")
SESSIONS_DIR = os.path.join(script_dir, "chat_sessions")
MEMORY_PROFILE_PATH = os.path.join(SESSIONS_DIR, "memory_profile.json")
ARCHIVE_SESSIONS_DIR = os.path.join(script_dir, "archive_sessions_json")
UPLOADS_DIR = os.path.join(script_dir, "chat_uploads")
ARTICLES_DIR = os.path.join(script_dir, "News", "articles")

os.makedirs(SESSIONS_DIR, exist_ok=True)
os.makedirs(ARCHIVE_SESSIONS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(ARTICLES_DIR, exist_ok=True)

# Global in-memory registries
STORY_REGISTRY = {}
POLICY_LEDGER = {}


def render_news_article_html(title, lede, body_html, coordinates_info=None, timestamp=None, slug=""):
    """Render a standalone, responsive news story article HTML page."""
    import datetime
    if not timestamp:
        timestamp = datetime.datetime.now().strftime("%B %d, %Y")
        
    coords_box = ""
    if coordinates_info and isinstance(coordinates_info, dict):
        claim_u = coordinates_info.get("claim_u", 0.0)
        claim_psi = coordinates_info.get("claim_psi", 0.0)
        real_u = coordinates_info.get("real_u", 0.0)
        real_psi = coordinates_info.get("real_psi", 0.0)
        verdict = coordinates_info.get("verdict", "AUDIT")
        path = coordinates_info.get("path", "Geodesic")
        
        coords_box = f"""
        <div class="audit-meta-card">
          <div class="audit-badge">{verdict} · {path}</div>
          <div class="coords-row">
            <span><strong>Stated Claim:</strong> ({claim_u:+.2f}, {claim_psi:+.2f})</span>
            <span><strong>Ground Reality:</strong> ({real_u:+.2f}, {real_psi:+.2f})</span>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Aletheia Dispatch</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: #131b2e;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
      --accent-cyan: #06b6d4;
      --accent-gold: #f59e0b;
      --border: rgba(255, 255, 255, 0.1);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Newsreader', Georgia, serif;
      font-size: 1.18rem;
      line-height: 1.75;
      padding: 40px 20px;
    }}
    .article-container {{
      max-width: 780px;
      margin: 0 auto;
    }}
    .header-tag {{
      font-family: 'Inter', sans-serif;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--accent-cyan);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    h1 {{
      font-size: 2.3rem;
      font-weight: 700;
      line-height: 1.25;
      color: #ffffff;
      margin-bottom: 16px;
      letter-spacing: -0.01em;
    }}
    .byline-bar {{
      font-family: 'Inter', sans-serif;
      font-size: 0.85rem;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      padding: 12px 0;
      margin-bottom: 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .lede {{
      font-size: 1.35rem;
      font-weight: 500;
      color: #f8fafc;
      line-height: 1.6;
      margin-bottom: 24px;
    }}
    .audit-meta-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent-cyan);
      border-radius: 8px;
      padding: 16px 20px;
      margin: 28px 0;
      font-family: 'Inter', sans-serif;
    }}
    .audit-badge {{
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--accent-cyan);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }}
    .coords-row {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      color: var(--text-muted);
      display: flex;
      gap: 24px;
      flex-wrap: wrap;
    }}
    .article-body p {{
      margin-bottom: 22px;
    }}
    .article-body h2 {{
      font-family: 'Inter', sans-serif;
      font-size: 1.4rem;
      font-weight: 700;
      color: #ffffff;
      margin-top: 36px;
      margin-bottom: 16px;
    }}
    .article-body blockquote {{
      border-left: 3px solid var(--accent-gold);
      padding-left: 18px;
      margin: 24px 0;
      font-style: italic;
      color: #cbd5e1;
    }}
    footer {{
      margin-top: 60px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
      font-family: 'Inter', sans-serif;
      font-size: 0.8rem;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    a {{ color: var(--accent-cyan); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <article class="article-container">
    <div class="header-tag">⚡ Aletheia Actualism Dispatch · Source Article</div>
    <h1>{title}</h1>
    <div class="byline-bar">
      <span>By Aletheia Investigation Desk</span>
      <span>Published {timestamp}</span>
    </div>
    {f'<p class="lede">{lede}</p>' if lede else ''}
    {coords_box}
    <div class="article-body">
      {body_html}
    </div>
    <footer>
      <span>Generated by Aletheia Actualism Intelligence</span>
      <a href="http://localhost:8766/">← Open Aletheia Chat & Controls</a>
    </footer>
  </article>
</body>
</html>"""
    return html


def load_data():
    """Load all factcheck JSON files and policy ledger into memory."""
    global STORY_REGISTRY, POLICY_LEDGER
    STORY_REGISTRY.clear()

    search_dirs = [LIVE_DIR, DARKROOM_DIR, STORIES_DIR]
    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        for p in glob.glob(os.path.join(sdir, "factcheck_*.json")):
            slug = os.path.basename(p)[len("factcheck_"):-len(".json")]
            if slug in STORY_REGISTRY:
                continue
            try:
                mtime = os.path.getmtime(p)
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cfg = data[0] if isinstance(data, list) and len(data) > 0 else (data if isinstance(data, dict) else {})
                cfg["_mtime"] = mtime
                cfg["_filepath"] = p
                if "id" not in cfg:
                    cfg["id"] = slug
                STORY_REGISTRY[slug] = cfg
            except Exception:
                pass

    if os.path.exists(POLICY_LEDGER_PATH):
        try:
            with open(POLICY_LEDGER_PATH, "r", encoding="utf-8") as f:
                POLICY_LEDGER = json.load(f)
        except Exception:
            POLICY_LEDGER = {"policies": {}}
    else:
        POLICY_LEDGER = {"policies": {}}

    print(f"[Chat Server] Loaded {len(STORY_REGISTRY)} stories and {len(POLICY_LEDGER.get('policies', {}))} tracked policies.")


load_data()


# ── Audit Data Retriever ──────────────────────────────────────────────────────
def retrieve_relevant_audits(query_text, max_results=4):
    """Search story registry for stories matching keywords in the query."""
    if not query_text or len(query_text.strip()) < 3:
        return []

    tokens = [t.lower() for t in re.findall(r"\b\w{3,}\b", query_text) if t.lower() not in {"what", "when", "where", "how", "the", "and", "for", "with", "this", "that", "show", "tell", "audit", "judge"}]
    if not tokens:
        return []

    scored = []
    for s in STORY_REGISTRY.values():
        subj = s.get("subject", "").lower()
        actors = [a.lower() for a in s.get("actors", [])]
        policies = [p.lower() for p in s.get("policies", [])]
        posts_text = " ".join(s.get("posts", [])[:4]).lower()

        match_score = 0
        for token in tokens:
            if token in subj:
                match_score += 4
            if any(token in a for a in actors):
                match_score += 5
            if any(token in p for p in policies):
                match_score += 3
            if token in posts_text:
                match_score += 1

        if match_score > 0:
            scored.append((match_score, s))

    scored.sort(key=lambda x: (x[0], x[1].get("_mtime", 0)), reverse=True)
    return [s for _, s in scored[:max_results]]


# ── Session & Topic Thread Management ─────────────────────────────────────────
def get_memory_profile():
    if os.path.exists(MEMORY_PROFILE_PATH):
        try:
            with open(MEMORY_PROFILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "operator_notes": "Operator focuses on high-precision Actualism, policy analysis, and historical audits.",
        "key_preferences": ["Default to Vertex AI endpoints", "Use decimal coordinates (υ, ψ)", "Provide nuance: bright side / poison", "Ground claims in database or live search"]
    }


def save_memory_profile(profile):
    try:
        with open(MEMORY_PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Failed to save memory profile: {e}")


def list_sessions():
    sessions = []
    for p in glob.glob(os.path.join(SESSIONS_DIR, "session_*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                s = json.load(f)
                
                # Compute total message count across threads
                msg_count = 0
                if "threads" in s:
                    for t in s["threads"].values():
                        msg_count += len(t.get("messages", []))
                else:
                    msg_count = len(s.get("messages", []))

                threads_meta = []
                if "threads" in s:
                    for tid, t in s["threads"].items():
                        threads_meta.append({
                            "id": tid,
                            "name": t.get("name", "Thread"),
                            "parent_id": t.get("parent_thread_id"),
                            "msg_count": len(t.get("messages", []))
                        })

                sessions.append({
                    "id": s.get("id"),
                    "title": s.get("title", "Untitled Conversation"),
                    "created_at": s.get("created_at", ""),
                    "updated_at": s.get("updated_at", ""),
                    "message_count": msg_count,
                    "active_thread_id": s.get("active_thread_id", "main"),
                    "threads": threads_meta
                })
        except Exception:
            pass
    sessions.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return sessions


def load_session(session_id):
    path = os.path.join(SESSIONS_DIR, f"session_{session_id}.json")
    if not os.path.exists(path):
        archive_path = os.path.join(ARCHIVE_SESSIONS_DIR, f"session_{session_id}.json")
        if os.path.exists(archive_path):
            path = archive_path

    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                s = json.load(f)
                # Auto-migrate legacy flat session to multi-thread hierarchy
                if "threads" not in s:
                    legacy_msgs = s.get("messages", [])
                    s["threads"] = {
                        "main": {
                            "id": "main",
                            "name": "Main Trunk",
                            "parent_thread_id": None,
                            "fork_message_index": 0,
                            "created_at": s.get("created_at", datetime.datetime.now().isoformat()),
                            "messages": legacy_msgs
                        }
                    }
                    s["active_thread_id"] = "main"
                    if "narrative_spine" not in s:
                        s["narrative_spine"] = []
                    save_session(s)
                return s
        except Exception as e:
            return {"error": str(e)}
            
    now = datetime.datetime.now().isoformat()
    return {
        "id": session_id,
        "title": "New Conversation",
        "created_at": now,
        "updated_at": now,
        "active_thread_id": "main",
        "narrative_spine": [],
        "threads": {
            "main": {
                "id": "main",
                "name": "Main Trunk",
                "parent_thread_id": None,
                "fork_message_index": 0,
                "created_at": now,
                "messages": []
            }
        }
    }


def save_session(session_data):
    session_id = session_data.get("id") or str(uuid.uuid4())[:8]
    session_data["id"] = session_id
    session_data["updated_at"] = datetime.datetime.now().isoformat()
    if "created_at" not in session_data:
        session_data["created_at"] = session_data["updated_at"]

    # Ensure threads structure exists
    if "threads" not in session_data:
        session_data["threads"] = {
            "main": {
                "id": "main",
                "name": "Main Trunk",
                "parent_thread_id": None,
                "fork_message_index": 0,
                "created_at": session_data["created_at"],
                "messages": session_data.get("messages", [])
            }
        }
        session_data["active_thread_id"] = "main"

    if "narrative_spine" not in session_data:
        session_data["narrative_spine"] = []

    # Derive dynamic title if default
    main_msgs = session_data["threads"].get("main", {}).get("messages", [])
    if session_data.get("title") in ("New Conversation", "Untitled Conversation", "") and main_msgs:
        first_msg = main_msgs[0].get("content", "")
        title = first_msg[:35] + ("..." if len(first_msg) > 35 else "")
        session_data["title"] = title

    path = os.path.join(SESSIONS_DIR, f"session_{session_id}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        return session_data
    except Exception as e:
        print(f"Error saving session: {e}")
        return session_data


# ── Client & Prompt Builder ───────────────────────────────────────────────────
def get_gemini_client(use_vertex=True):
    if not genai:
        raise ImportError("google-genai SDK is not installed. Run: pip install google-genai")
    
    if use_vertex:
        vertex_key = os.environ.get("VERTEX_API_KEY")
        project_id = os.environ.get("VERTEX_PROJECT_ID", "alethekanon")
        location = os.environ.get("VERTEX_LOCATION", "us-central1")
        client_args = {"vertexai": True}
        if vertex_key:
            client_args["api_key"] = vertex_key
        else:
            client_args["project"] = project_id
            client_args["location"] = location
        return genai.Client(**client_args)
    else:
        gemini_key = os.environ.get("GEMINI_API_KEY")
        return genai.Client(api_key=gemini_key)


def classify_archive_file(filename, content_sample=""):
    """Categorize an archive log file into clean semantic groups."""
    fn = filename.lower()
    sample = content_sample.lower()
    
    if any(k in fn for k in ["math", "infinity", "tensor", "physics", "quantum", "cosmology", "dimension", "geometry", "duality of time", "6d memory"]):
        return "🌌 Physics & Cosmology"
    if any(k in fn for k in ["hegemon", "trump", "russia", "china", "iran", "catholic", "balaam", "policy", "srl", "strategic", "trade"]):
        return "🏛️ Politics & Hegemony"
    if any(k in fn for k in ["mbti", "epistemic", "faith", "belief", "greek", "deleuze", "perception", "consciousness", "fear"]):
        return "🧠 Epistemology & Mind"
    if any(k in fn for k in ["tautonic", "axiom", "kanon", "objective truth", "framework"]):
        return "📜 Axioms & Tautonics"
    return "💬 Discussion Transcripts"


def load_convergence_son_instructions():
    """Dynamically load the authoritative Convergence SON protocol directly from the workspace tool directory."""
    candidates = [
        os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son.md"),
        os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son_lite.md"),
        os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "Convergence-test-v2.md")
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception:
                pass
    return ""


def load_thread_formatting_instructions():
    """Dynamically load the authoritative Thread Formatting protocol from instructions/."""
    candidates = [
        os.path.join(script_dir, "instructions", "thread_formatting_son.md"),
        os.path.join(script_dir, "instructions", "thread_formatting.md")
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception:
                pass
    return ""


def build_system_prompt(custom_instructions="", retrieved_audits=None, retrieved_archives=None, narrative_spine=None, canvas_story=None):
    profile = get_memory_profile()
    notes = profile.get("operator_notes", "")
    prefs = "\n".join(f"- {p}" for p in profile.get("key_preferences", []))
    
    audits_block = ""
    if retrieved_audits:
        lines = ["\n### RELEVANT DATABASE AUDITS (8,651 Corpus Grounding):"]
        for s in retrieved_audits:
            lines.append(f"- **{s.get('subject')}**")
            lines.append(f"  Claimed: ({s.get('claim_u')}, {s.get('claim_psi')}) | Actual Reality: ({s.get('real_u')}, {s.get('real_psi')}) [{s.get('verdict')}]")
            if s.get("posts"):
                lines.append(f"  Summary: {s.get('posts')[0]}")
        audits_block = "\n".join(lines) + "\n"

    archive_block = ""
    if retrieved_archives:
        lines = ["\n### RECALLED ARCHIVE DISCUSSION CHUNKS ('_AI files and chat logs/'):"]
        for a in retrieved_archives:
            lines.append(f"--- SOURCE: {a.get('filename')} ---")
            lines.append(a.get("content", "").strip())
        archive_block = "\n".join(lines) + "\n"

    spine_block = ""
    if narrative_spine and isinstance(narrative_spine, list) and len(narrative_spine) > 0:
        lines = ["\n### SESSION NARRATIVE SPINE (Chronological Topic Timeline):"]
        for idx, entry in enumerate(narrative_spine):
            lines.append(f"{idx+1}. {entry}")
        spine_block = "\n".join(lines) + "\n"

    custom_block = f"\n### OPERATOR CUSTOM INSTRUCTIONS:\n{custom_instructions}\n" if custom_instructions else ""

    canvas_block = ""
    if canvas_story and isinstance(canvas_story, dict) and canvas_story.get("subject"):
        posts_str = "\n".join([f"Post {idx+1}: {p}" for idx, p in enumerate(canvas_story.get("posts", []))])
        canvas_block = f"""
### ACTIVE STORY DRAFT IN OPERATOR'S CANVAS:
- **Slug / ID:** {canvas_story.get('id', '')}
- **Subject:** {canvas_story.get('subject', '')}
- **Link:** {canvas_story.get('link', '')}
- **Stated Claim:** ({canvas_story.get('claim_u', 0.0)}, {canvas_story.get('claim_psi', 0.0)})
- **Empirical Reality:** ({canvas_story.get('real_u', 0.0)}, {canvas_story.get('real_psi', 0.0)})
- **Actors:** {', '.join(canvas_story.get('actors', []))}
- **Posts (1-14):**
{posts_str}

CRITICAL STORY EDITING INSTRUCTION:
If the operator asks to edit, revise, rewrite, refine, or recalculate this story or any of its posts (e.g. "make post 14 punchier", "recalculate coords", "edit post 1 to add hashtags", "fix the plane error in post 8", "shorten post 3"), you MUST provide your concise explanation in markdown AND output the complete revised story JSON in a code block tagged:
```json:story_update
{{
  "id": "{canvas_story.get('id', '')}",
  "subject": "...",
  "link": "...",
  "claim_u": ...,
  "claim_psi": ...,
  "real_u": ...,
  "real_psi": ...,
  "actors": [...],
  "posts": [
    "Clean hook prose without Post 1 prefix...",
    ...
    "Clean Brothekanon prose without Post 14 prefix..."
  ]
}}
```
The operator's interactive UI will automatically catch this ````json:story_update```` block and update their Story Canvas live!
"""

    formatting_spec = load_thread_formatting_instructions()

    story_synthesis_rules = f"""
### STORY SYNTHESIS & OFFICIAL BLUESKY BOT THREAD STANDARDS (14-POST MULTI-ASPECT SON PROTOCOL):
If the user asks you to:
- "Make a story about the things we're talking about" or "Draft a story from our discussion"
- "Make a story about [topic / event / actor]"
- "Turn these selected points into a story"
You MUST:
1. Extract the primary stated intent vs empirical reality and compute the two-axis coordinates:
   - Stated Claim: (claim_u, claim_psi)
   - Empirical Reality: (real_u, real_psi)
2. Generate EXACTLY 14 sequential Aletheia thread posts (strictly under 280 characters each, hard max 290) mapped strictly to Elements 0 through 13.
3. **STRICT BAN ON NUMBERED PREFIXES**: NEVER start post strings with "Post 1:", "Post 2:", "1. Hook:", etc. Each array element MUST be pure, conversational editorial text conforming to the 14-step standard below:
   - Element 0 (The Hook): Custom punchy scene-setter one-liner + News Subject title + Evidence line (Evidence: [Stated Ideal in 2-5 words], [Actual Effect in 2-5 words], [Actual Ideal in 2-5 words]) + 1-2 #hashtags. (Max 260 chars).
   - Element 1 (The Claim): Natural claim paragraph ending with: Stated Judgement: ([claim_u], [claim_psi]) — [Coordinate Label]
   - Element 2 (The Reality): Ground reality paragraph ending with: Resulting Judgement: ([real_u], [real_psi]) — [Coordinate Label]
   - Element 3 (The Verdict): Verdict: [PASS/FAIL] — [Path Name]. Explanatory summary.\n\nIntegrity: [Label] (Hypocrisy: [R_net], Uncertainty z: [z])
   - Element 4 (Sub-Audits Breakdown): Sub-Audits Breakdown:\n- [Aspect A]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Takeaway under 60 chars].\n- [Aspect B]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Takeaway under 60 chars].
   - Element 5 (What's Happening / Context): Clear, non-technical context paragraph explaining the news event in 1-2 concise sentences.
   - Element 6 (The Nuance): The Bright Side:\n[Nuance] OR The Poison:\n[Nuance]
   - Element 7 (The Breakdown & Plane Error): The Breakdown & Plane Error:\n[Plain language explanation of WHAT vs WHO and forensic bait-and-switch]
   - Element 8 (Social Physics Analysis): Social Physics Analysis:\n[Plain-English dynamics without jargon loops]
   - Element 9 (The Trajectory & Destination): The Trajectory: The Path of [Path Name].\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward [Outcome/Terminal Zone]. [Mathematical explanation]
   - Element 10 (The Unavoidables): The Unavoidable Truth: [1 concise sentence]\n\nThe Unavoidable Lie: [1 concise sentence]
   - Element 11 (Alethekanon): Alethekanon:\n[Analytical Persona reaction]
   - Element 12 (Awwthekanon): Awwthekanon:\n[Empathetic Persona reaction]
   - Element 13 (Brothekanon): Brothekanon:\n[Casual, sharp observer persona reaction]
4. Output the complete revised story JSON in a ```json:story_update``` code block matching:
```json:story_update
{{
  "id": "kebab-case-slug",
  "subject": "Compelling thread headline",
  "link": "http://localhost:8766/articles/kebab-case-slug.html",
  "claim_u": 0.8,
  "claim_psi": 0.9,
  "real_u": -0.5,
  "real_psi": -0.3,
  "actors": ["Actor 1"],
  "posts": [
    "Clean hook prose without Post 1 prefix...",
    ...
  ]
}}
```
"""

    son_spec = load_convergence_son_instructions()
    son_block = f"\n### AUTHORITATIVE CONVERGENCE TEST (SON PROTOCOL LOADED FROM DISK):\n{son_spec}\n" if son_spec else ""
    format_block = f"\n### OFFICIAL BLUESKY BOT THREAD FORMATTING INSTRUCTIONS (LOADED FROM DISK):\n{formatting_spec}\n" if formatting_spec else ""

    return f"""You are Aletheia, an advanced Actualism intelligence engine and high-precision reasoning partner for Vector Field Theory (VFT) and Hegemonic Audits.

### OPERATOR PROFILE & RULES:
{notes}
{prefs}
{custom_block}
{spine_block}
{canvas_block}
{story_synthesis_rules}
{son_block}
{audits_block}
{archive_block}
### ELI18 READING LEVEL & VOICE DIRECTIVE:
- Maintain an **ELI18 reading level** across all chat responses, analytical audits, and story drafts.
- **ELI18 Definition**: Articulate, sharp, undergraduate / senior-high school clarity.
- **No Point Loss**: Never dumb down or omit rigorous math, two-axis coordinates (υ, ψ), empirical evidence, or structural dynamics—instead, explain them in lucid, accessible language.
- **Anti-Jargon & Anti-Gatekeeping**: Strictly avoid impenetrable academic jargon, circular abstractions, or opaque Latinisms. Ground every insight in real-world human dynamics (who benefits, who pays, and how the incentives function).

### OUTPUT EXPECTATIONS:
- Present clear, rigorous structural analysis without moralizing or preachiness.
- When evaluating a claim, event, actor, or policy, execute the 7 Planes and 6-Attractor SON Protocol from the specification above and explicitly label:
  - **Decimal Coordinates:** `(υ, ψ)`
  - **Nearest Zone Anchor:** [Anchor Name]
  - **Trajectory Geodesic:** [Path of Grace / Path of Fall / Path of Redemption / Path of Deception / Path of Compromise]
  - **Hypocrisy Gap (ΔH):** [Value + Verdict]
  - **Plain Language Verdict:** [Direct structural summary]
  - **Nuance (Bright Side / Poison):** [Counter-perspective]
"""


def call_llm_chat(message, history=None, model="vertex:gemini-3.7-flash", use_search=True, attachments=None,
                  thinking_level="MEDIUM", temperature=0.3, max_tokens=8192, custom_instructions="",
                  narrative_spine=None, ancestral_history=None, canvas_story=None):
    """Execute live LLM call using Google GenAI SDK with Dual-Track Context Assembly & Automatic Fallback Cascades."""
    if not genai:
        raise ImportError("google-genai SDK not available.")

    # Parse requested model or sequence
    candidates = []
    if isinstance(model, list):
        candidates = [str(m).strip() for m in model if str(m).strip()]
    elif isinstance(model, str):
        if "," in model:
            candidates = [m.strip() for m in model.split(",") if m.strip()]
        elif model.strip():
            candidates = [model.strip()]

    # Append standard zero-downtime fallback cascade
    default_cascade = [
        "vertex:gemini-3.7-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-3.1-flash-lite",
        "gemma-4-31b-it"
    ]
    for df in default_cascade:
        if df not in candidates:
            candidates.append(df)
    
    # 1. Retrieve relevant audits from 8,651 story store
    retrieved_audits = retrieve_relevant_audits(message)

    # 2. Retrieve relevant archive discussion chunks from SQLite FTS5
    retrieved_archives = []
    if memory_store:
        try:
            retrieved_archives = memory_store.search_archive_logs(message, limit=2)
        except Exception:
            pass

    system_instruction = build_system_prompt(
        custom_instructions=custom_instructions,
        retrieved_audits=retrieved_audits,
        retrieved_archives=retrieved_archives,
        narrative_spine=narrative_spine,
        canvas_story=canvas_story
    )

    contents = []

    # Insert ancestral parent turns if this is a sub-thread
    if ancestral_history and isinstance(ancestral_history, list):
        for turn in ancestral_history:
            role = "user" if turn.get("role") == "user" else "model"
            turn_text = turn.get("content", "")
            if turn_text:
                prefix = "[Parent Context] " if role == "user" else ""
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=f"{prefix}{turn_text}")]
                ))

    # Insert active thread history
    if history and isinstance(history, list):
        for turn in history:
            role = "user" if turn.get("role") == "user" else "model"
            turn_text = turn.get("content", "")
            if turn_text:
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=turn_text)]
                ))
    
    # Build current user parts
    current_parts = []
    if message:
        current_parts.append(types.Part.from_text(text=message))
    
    # Process attachments
    if attachments and isinstance(attachments, list):
        for att in attachments:
            fname = att.get("name", "file")
            ftype = att.get("type", "application/octet-stream")
            b64data = att.get("data", "")
            if b64data:
                try:
                    raw_bytes = base64.b64decode(b64data)
                    if ftype.startswith("image/"):
                        current_parts.append(types.Part.from_bytes(data=raw_bytes, mime_type=ftype))
                    else:
                        try:
                            text_content = raw_bytes.decode("utf-8")
                            current_parts.append(types.Part.from_text(text=f"\n--- ATTACHED FILE: {fname} ---\n{text_content[:25000]}\n--- END FILE ---\n"))
                        except Exception:
                            current_parts.append(types.Part.from_bytes(data=raw_bytes, mime_type=ftype))
                except Exception as e:
                    print(f"Failed to attach file {fname}: {e}")

    if not current_parts:
        current_parts = [types.Part.from_text(text="Hello")]

    contents.append(types.Content(
        role="user",
        parts=current_parts
    ))

    tools = None
    if use_search:
        tools = [types.Tool(google_search=types.GoogleSearch())]

    safety = [
        types.SafetySetting(category='HARM_CATEGORY_HATE_SPEECH', threshold='BLOCK_NONE'),
        types.SafetySetting(category='HARM_CATEGORY_HARASSMENT', threshold='BLOCK_NONE'),
        types.SafetySetting(category='HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold='BLOCK_NONE'),
        types.SafetySetting(category='HARM_CATEGORY_DANGEROUS_CONTENT', threshold='BLOCK_NONE'),
    ]

    last_err = None
    successful_model = None
    response = None

    # Cascade through candidate models until one succeeds
    for target_model in candidates:
        use_vertex = target_model.startswith("vertex:")
        actual_model = target_model.split(":", 1)[1] if use_vertex else target_model

        try:
            client = get_gemini_client(use_vertex=use_vertex)

            # Dynamic Thinking Config
            thinking_config = None
            if thinking_level and thinking_level != "OFF":
                model_lower = actual_model.lower()
                if "gemini-3." in model_lower or "gemini-3-" in model_lower:
                    thinking_config = types.ThinkingConfig(thinking_level=thinking_level.upper())
                elif "gemini-2.5" in model_lower:
                    budget_map = {"LOW": 1024, "MEDIUM": 2048, "HIGH": 4096}
                    thinking_config = types.ThinkingConfig(thinking_budget=budget_map.get(thinking_level.upper(), 2048))

            config = types.GenerateContentConfig(
                temperature=float(temperature),
                max_output_tokens=int(max_tokens),
                system_instruction=system_instruction,
                tools=tools,
                safety_settings=safety,
                thinking_config=thinking_config
            )

            response = client.models.generate_content(
                model=actual_model,
                contents=contents,
                config=config
            )
            successful_model = target_model
            break
        except Exception as e:
            print(f"[Chat Server] Model '{target_model}' encountered error ({e}). Cascading to next fallback...", file=sys.stderr)
            last_err = e
            import time
            time.sleep(0.3)

    if response is None:
        raise RuntimeError(f"All models in fallback chain failed. Last error: {last_err}")

    result_text = ""
    thought_text = ""
    if hasattr(response, 'candidates') and response.candidates:
        cand = response.candidates[0]
        if hasattr(cand, 'content') and cand.content and hasattr(cand.content, 'parts') and cand.content.parts:
            non_thought_parts = []
            thought_parts = []
            for part in cand.content.parts:
                if getattr(part, 'thought', False):
                    if hasattr(part, 'text') and part.text:
                        thought_parts.append(part.text)
                else:
                    if hasattr(part, 'text') and part.text:
                        non_thought_parts.append(part.text)
            result_text = "".join(non_thought_parts).strip()
            thought_text = "".join(thought_parts).strip()

    if not result_text and hasattr(response, 'text') and response.text:
        result_text = response.text.strip()

    # Extract coordinates specifically if the model labeled them
    coords_match = re.search(
        r"(?:Coordinates|Decimal Coordinates|Verdict Coordinates|\(υ,\s*ψ\))\s*[:*]*\s*\(([+-]?[0-2](?:\.\d+)?),\s*([+-]?[0-2](?:\.\d+)?)\)",
        result_text,
        re.IGNORECASE
    )
    detected_coords = None
    if coords_match:
        detected_coords = {
            "u": float(coords_match.group(1)),
            "psi": float(coords_match.group(2))
        }

    # Extract token usage and cost
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    if hasattr(response, 'usage_metadata') and response.usage_metadata:
        prompt_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0) or 0
        completion_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0) or 0
        total_tokens = getattr(response.usage_metadata, 'total_token_count', 0) or (prompt_tokens + completion_tokens)

    cost_info = calculate_token_cost(successful_model or model, prompt_tokens, completion_tokens)

    return {
        "text": result_text,
        "thought": thought_text,
        "coords": detected_coords,
        "model": model,
        "model_used": successful_model or model,
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost_info["total_cost_usd"],
            "input_cost_usd": cost_info["input_cost_usd"],
            "output_cost_usd": cost_info["output_cost_usd"],
            "rates": cost_info["rates"]
        },
        "retrieved_audits": len(retrieved_audits),
        "retrieved_archives": len(retrieved_archives)
    }


# ── Model Pricing per 1 Million Tokens (USD) ──────────────────────────────────
MODEL_PRICING = {
    "gemini-3.7-flash": {"input": 0.75, "output": 3.75, "name": "Gemini 3.7 Flash"},
    "vertex:gemini-3.7-flash": {"input": 0.75, "output": 3.75, "name": "Vertex: Gemini 3.7 Flash"},
    "gemini-3.6-flash": {"input": 1.50, "output": 7.50, "name": "Gemini 3.6 Flash"},
    "vertex:gemini-3.6-flash": {"input": 1.50, "output": 7.50, "name": "Vertex: Gemini 3.6 Flash"},
    "gemini-3.5-flash": {"input": 1.50, "output": 9.00, "name": "Gemini 3.5 Flash"},
    "vertex:gemini-3.5-flash": {"input": 1.50, "output": 9.00, "name": "Vertex: Gemini 3.5 Flash"},
    "gemini-3.5-flash-lite": {"input": 0.25, "output": 1.50, "name": "Gemini 3.5 Flash-Lite"},
    "vertex:gemini-3.5-flash-lite": {"input": 0.25, "output": 1.50, "name": "Vertex: Gemini 3.5 Flash-Lite"},
    "gemini-3.1-flash-lite": {"input": 0.25, "output": 1.50, "name": "Gemini 3.1 Flash-Lite"},
    "vertex:gemini-3.1-flash-lite": {"input": 0.25, "output": 1.50, "name": "Vertex: Gemini 3.1 Flash-Lite"},
    "gemini-3-flash-preview": {"input": 0.50, "output": 3.00, "name": "Gemini 3 Flash Preview"},
    "gemini-2.5-flash": {"input": 0.30, "output": 2.50, "name": "Gemini 2.5 Flash"},
    "vertex:gemini-2.5-flash": {"input": 0.30, "output": 2.50, "name": "Vertex: Gemini 2.5 Flash"},
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40, "name": "Gemini 2.5 Flash-Lite"},
    "vertex:gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40, "name": "Vertex: Gemini 2.5 Flash-Lite"},
    "gemini-2.5-pro": {"input": 1.25, "output": 5.00, "name": "Gemini 2.5 Pro"},
    "vertex:gemini-2.5-pro": {"input": 1.25, "output": 5.00, "name": "Vertex: Gemini 2.5 Pro"},
    "gemma-4-31b-it": {"input": 0.20, "output": 0.40, "name": "Gemma 4 31B IT"}
}


def calculate_token_cost(model_name, prompt_tokens, completion_tokens):
    """Compute estimated API cost in USD based on input and output tokens."""
    rates = MODEL_PRICING.get(model_name)
    if not rates:
        # Match normalized key
        norm_key = model_name.replace("vertex:", "").strip()
        rates = MODEL_PRICING.get(norm_key, {"input": 0.75, "output": 3.75, "name": model_name})

    in_cost = (prompt_tokens / 1_000_000.0) * rates["input"]
    out_cost = (completion_tokens / 1_000_000.0) * rates["output"]
    total_cost = in_cost + out_cost
    return {
        "input_cost_usd": round(in_cost, 6),
        "output_cost_usd": round(out_cost, 6),
        "total_cost_usd": round(total_cost, 6),
        "rates": rates
    }


# ── HTTP Server Request Handler ───────────────────────────────────────────────
class ChatHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/models":
            self.send_json(200, {"models": MODEL_PRICING})
            return

        if parsed.path in ["/", "/chat", "/aletheia_chat.html", "/chat.html"]:
            chat_html_path = os.path.join(SCRIPT_DIR, "aletheia_chat.html")
            if os.path.exists(chat_html_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                with open(chat_html_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        if parsed.path in ["/alethekanon.png", "/alethekanon.ico"]:
            fname = "alethekanon.png" if parsed.path.endswith(".png") else "alethekanon.ico"
            img_path = os.path.join(SCRIPT_DIR, fname)
            if os.path.exists(img_path):
                self.send_response(200)
                self.send_header("Content-Type", "image/png" if fname.endswith(".png") else "image/x-icon")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                try:
                    with open(img_path, "rb") as f:
                        self.wfile.write(f.read())
                except Exception:
                    pass
                return

        if parsed.path.startswith("/articles/"):
            art_name = parsed.path.split("/articles/", 1)[1]
            art_path = os.path.join(ARTICLES_DIR, art_name)
            if os.path.exists(art_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                try:
                    with open(art_path, "rb") as f:
                        self.wfile.write(f.read())
                except Exception:
                    pass
                return
            else:
                self.send_json(404, {"error": f"Article '{art_name}' not found"})
                return

        if parsed.path == "/health":
            self.send_json(200, {
                "status": "ok",
                "stories": len(STORY_REGISTRY),
                "policies": len(POLICY_LEDGER.get("policies", {})),
                "sessions": len(list_sessions()),
                "has_gemini": bool(os.environ.get("GEMINI_API_KEY")),
                "has_vertex": bool(os.environ.get("VERTEX_API_KEY") or os.environ.get("VERTEX_PROJECT_ID"))
            })
            return

        if parsed.path == "/sessions":
            self.send_json(200, list_sessions())
            return

        if parsed.path == "/session":
            sid = params.get("id", [""])[0].strip()
            if not sid:
                self.send_json(400, {"error": "Missing 'id' parameter"})
                return
            self.send_json(200, load_session(sid))
            return

        if parsed.path == "/audits/search":
            q = params.get("q", [""])[0].strip()
            results = retrieve_relevant_audits(q, max_results=8)
            cards = [{
                "id": s.get("id"),
                "subject": s.get("subject"),
                "claim_u": s.get("claim_u"),
                "claim_psi": s.get("claim_psi"),
                "real_u": s.get("real_u"),
                "real_psi": s.get("real_psi"),
                "verdict": s.get("verdict")
            } for s in results]
            self.send_json(200, cards)
            return

        if parsed.path == "/registry":
            self.send_json(200, list(STORY_REGISTRY.values()))
            return

        if parsed.path == "/policy-ledger":
            self.send_json(200, POLICY_LEDGER)
            return

        if parsed.path == "/story/drafts/list":
            drafts = []
            for root, dirs, files in os.walk(STORIES_DIR):
                for f in files:
                    if f.startswith("factcheck_") and f.endswith(".json"):
                        fpath = os.path.join(root, f)
                        try:
                            mtime = os.path.getmtime(fpath)
                            with open(fpath, "r", encoding="utf-8") as jf:
                                data = json.load(jf)
                                story = data[0] if isinstance(data, list) and data else data
                                drafts.append({
                                    "filename": f,
                                    "filepath": fpath,
                                    "id": story.get("id", f),
                                    "subject": story.get("subject", f),
                                    "status": story.get("status", "DRAFT"),
                                    "mtime": mtime
                                })
                        except Exception:
                            pass
            drafts.sort(key=lambda x: x["mtime"], reverse=True)
            self.send_json(200, drafts[:100])
            return

        if parsed.path == "/story/drafts/get":
            fname = params.get("filename", [""])[0].strip()
            slug = params.get("slug", [""])[0].strip()
            target_file = None
            if fname:
                target_file = os.path.join(STORIES_DIR, fname)
            elif slug:
                target_file = os.path.join(STORIES_DIR, f"factcheck_{slug}.json")

            if target_file and os.path.exists(target_file):
                try:
                    with open(target_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        story = data[0] if isinstance(data, list) and data else data
                        self.send_json(200, story)
                        return
                except Exception as e:
                    self.send_json(500, {"error": f"Failed to read file: {e}"})
                    return
            self.send_json(404, {"error": "Story file not found"})
            return

        # ── Archives Viewer Endpoints ─────────────────────────────────────────
        if parsed.path == "/archives/list":
            category_filter = params.get("category", [""])[0].strip()
            search_query = params.get("q", [""])[0].strip().lower()
            
            ai_logs_dir = os.path.join(os.path.dirname(SCRIPT_DIR), "_AI files and chat logs")
            if not os.path.exists(ai_logs_dir):
                self.send_json(200, {"archives": [], "categories": []})
                return

            archives = []
            categories_count = {}

            # Gather all .md and .txt files
            files = glob.glob(os.path.join(ai_logs_dir, "*.md")) + glob.glob(os.path.join(ai_logs_dir, "*.txt"))
            for fpath in files:
                fname = os.path.basename(fpath)
                try:
                    mtime = os.path.getmtime(fpath)
                    size = os.path.getsize(fpath)
                    cat = classify_archive_file(fname)
                    categories_count[cat] = categories_count.get(cat, 0) + 1

                    if category_filter and cat != category_filter:
                        continue
                    if search_query and (search_query not in fname.lower()):
                        continue

                    # Read first 300 chars for preview
                    preview = ""
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            preview = f.read(350).strip()
                    except Exception:
                        pass

                    clean_title = fname.replace(".txt", "").replace(".md", "").replace("_", " ").replace("-", " ")
                    slug = re.sub(r'[^a-zA-Z0-9_-]', '_', fname.replace('.txt', '').replace('.md', ''))[:48]
                    session_id = f"archive_{slug}"

                    archives.append({
                        "filename": fname,
                        "title": clean_title,
                        "slug": slug,
                        "session_id": session_id,
                        "category": cat,
                        "size_bytes": size,
                        "size_formatted": f"{round(size / 1024, 1)} KB" if size > 1024 else f"{size} B",
                        "mtime": mtime,
                        "date_formatted": datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d"),
                        "preview": preview
                    })
                except Exception:
                    pass

            archives.sort(key=lambda x: x["mtime"], reverse=True)
            self.send_json(200, {
                "archives": archives,
                "categories": [{"name": k, "count": v} for k, v in sorted(categories_count.items())],
                "total": len(files)
            })
            return

        if parsed.path == "/archives/session":
            fname = params.get("filename", [""])[0].strip()
            sid = params.get("id", [""])[0].strip()
            if not fname and not sid:
                self.send_json(400, {"error": "Missing filename or id parameter"})
                return

            if not sid and fname:
                slug = re.sub(r'[^a-zA-Z0-9_-]', '_', fname.replace('.txt', '').replace('.md', ''))[:48]
                sid = f"archive_{slug}"

            session = load_session(sid)
            self.send_json(200, session)
            return

        if parsed.path == "/archives/get":
            fname = params.get("filename", [""])[0].strip()
            if not fname:
                self.send_json(400, {"error": "Missing filename parameter"})
                return

            ai_logs_dir = os.path.join(os.path.dirname(SCRIPT_DIR), "_AI files and chat logs")
            fpath = os.path.join(ai_logs_dir, fname)
            if not os.path.exists(fpath):
                self.send_json(404, {"error": "Archive file not found"})
                return

            try:
                mtime = os.path.getmtime(fpath)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                cat = classify_archive_file(fname, content_sample=content[:1000])
                words = len(content.split())
                clean_title = fname.replace(".txt", "").replace(".md", "").replace("_", " ").replace("-", " ")
                slug = re.sub(r'[^a-zA-Z0-9_-]', '_', fname.replace('.txt', '').replace('.md', ''))[:48]
                self.send_json(200, {
                    "filename": fname,
                    "title": clean_title,
                    "slug": slug,
                    "session_id": f"archive_{slug}",
                    "category": cat,
                    "content": content,
                    "word_count": words,
                    "mtime": mtime,
                    "date_formatted": datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
                })
                return
            except Exception as e:
                self.send_json(500, {"error": f"Failed to read archive: {e}"})
                return

        self.send_json(404, {"error": "Not Found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            req_data = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except Exception as e:
            self.send_json(400, {"error": f"Invalid JSON body: {e}"})
            return

        if parsed.path == "/session/save":
            saved = save_session(req_data)
            self.send_json(200, saved)
            return

        if parsed.path == "/session/delete":
            sid = req_data.get("id") or urllib.parse.parse_qs(parsed.query).get("id", [""])[0]
            if sid:
                path = os.path.join(SESSIONS_DIR, f"session_{sid}.json")
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception:
                        pass
            self.send_json(200, {"status": "ok", "deleted": sid})
            return

        # ── Topic Thread Endpoints ────────────────────────────────────────────
        if parsed.path == "/session/thread/create":
            sid = req_data.get("session_id")
            parent_tid = req_data.get("parent_thread_id", "main")
            fork_idx = int(req_data.get("fork_message_index", 0))
            name = req_data.get("name", "Topic Branch").strip()

            session = load_session(sid)
            if "threads" not in session:
                session["threads"] = {}

            new_tid = f"thread_{uuid.uuid4().hex[:8]}"
            session["threads"][new_tid] = {
                "id": new_tid,
                "name": name,
                "parent_thread_id": parent_tid,
                "fork_message_index": fork_idx,
                "created_at": datetime.datetime.now().isoformat(),
                "messages": []
            }
            session["active_thread_id"] = new_tid
            session["narrative_spine"].append(f"Branched topic thread [{name}] from {parent_tid} at message #{fork_idx+1}.")
            saved = save_session(session)
            self.send_json(200, {"status": "ok", "thread_id": new_tid, "session": saved})
            return

        if parsed.path == "/session/thread/merge":
            sid = req_data.get("session_id")
            tid = req_data.get("thread_id")
            session = load_session(sid)
            threads = session.get("threads", {})

            if tid not in threads:
                self.send_json(404, {"error": f"Thread {tid} not found."})
                return

            target_thread = threads[tid]
            parent_tid = target_thread.get("parent_thread_id") or "main"
            parent_thread = threads.get(parent_tid, threads.get("main"))

            # Synthesize sub-thread takeaways
            t_msgs = target_thread.get("messages", [])
            synthesis_prompt = f"Synthesize this research thread '{target_thread.get('name')}' into an executive takeaway card with: (1) Core findings (2) Calculated decimal coordinates (υ, ψ) (3) 3 bullet takeaways.\n\nThread Transcript:\n"
            for m in t_msgs:
                synthesis_prompt += f"{m.get('role').upper()}: {m.get('content')}\n"

            try:
                synth_res = call_llm_chat(synthesis_prompt, model="vertex:gemini-3.7-flash", thinking_level="LOW")
                synth_text = synth_res.get("text", "")
            except Exception as e:
                synth_text = f"Summary of {target_thread.get('name')}: Completed discussion across {len(t_msgs)} turns."

            # Update Narrative Spine
            session["narrative_spine"].append(f"Merged branch [{target_thread.get('name')}] into {parent_tid}.")

            # Insert summary card into parent thread
            parent_thread["messages"].append({
                "role": "model",
                "content": f"### 📥 Synthesized Sub-Thread: {target_thread.get('name')}\n\n{synth_text}\n\n*(Branched from #{target_thread.get('fork_message_index')+1} · {len(t_msgs)} turns)*",
                "timestamp": datetime.datetime.now().isoformat(),
                "is_thread_summary": True,
                "source_thread_id": tid
            })

            session["active_thread_id"] = parent_tid
            saved = save_session(session)
            self.send_json(200, {"status": "ok", "session": saved})
            return

        if parsed.path == "/session/thread/rename":
            sid = req_data.get("session_id")
            tid = req_data.get("thread_id")
            new_name = req_data.get("name", "").strip()
            session = load_session(sid)
            if tid in session.get("threads", {}):
                session["threads"][tid]["name"] = new_name
                saved = save_session(session)
                self.send_json(200, {"status": "ok", "session": saved})
                return
            self.send_json(404, {"error": "Thread not found"})
            return

        if parsed.path == "/memory/search":
            q = req_data.get("query", "").strip()
            archives = memory_store.search_archive_logs(q, limit=5) if memory_store else []
            memories = memory_store.search_memories(q, limit=5) if memory_store else []
            self.send_json(200, {"archives": archives, "memories": memories})
            return

        # ── Story Studio & Canvas Endpoints ──────────────────────────────────
        if parsed.path == "/story/generate_from_chat":
            chat_text = req_data.get("text", "").strip()
            model_req = req_data.get("model", "vertex:gemini-3.7-flash")
            
            # Parse requested model candidates cleanly
            candidates = []
            if isinstance(model_req, list):
                candidates = [str(m).strip() for m in model_req if str(m).strip()]
            elif isinstance(model_req, str):
                if "," in model_req:
                    candidates = [m.strip() for m in model_req.split(",") if m.strip()]
                elif model_req.strip():
                    candidates = [model_req.strip()]

            default_cascade = [
                "vertex:gemini-3.7-flash",
                "gemini-3.5-flash",
                "gemini-3.5-flash-lite",
                "gemini-2.5-flash",
                "gemini-3.1-flash-lite"
            ]
            for df in default_cascade:
                if df not in candidates:
                    candidates.append(df)

            formatting_guide = load_thread_formatting_instructions()

            system_prompt = f"""You are Aletheia's thread compiler and investigative editor. Transform the user's analytical chat message into BOTH:
1. A complete, professional News Story Article (headline, lede, and rich multi-paragraph body).
2. A complete 14-post Aletheia factcheck story thread conforming strictly to the official Multi-Aspect SON formatting standards.

CRITICAL FORMATTING INSTRUCTIONS:
- ELI18 READING LEVEL: Use articulate, engaging undergraduate / senior-high level clarity across both the article and all posts. Never omit technical coordinates or empirical data, but explain them without academic pretension or circular jargon loops.
- STRICT BAN ON NUMBERED PREFIXES: NEVER write 'Post 1:', 'Post 2:', '1.', or any other numbers at the start of any post. Each array element MUST contain clean, conversational editorial prose.
- EXACTLY 14 POSTS: You MUST output exactly 14 elements in the 'posts' array (Elements 0 through 13).
- Every post MUST be strictly under 280 characters (hard max 290 chars) to fit cleanly on Bluesky.

OFFICIAL 14-STEP MULTI-ASPECT THREAD MAPPING:
Element 0 (The Hook): Custom punchy scene-setter one-liner + News Subject title + Evidence line (Evidence: [Stated Ideal in 2-5 words], [Actual Effect in 2-5 words], [Actual Ideal in 2-5 words]) + 1-2 #hashtags. (Max 260 chars).
Element 1 (The Claim): Natural claim paragraph ending with: Stated Judgement: ([claim_u], [claim_psi]) — [Coordinate Label]
Element 2 (The Reality): Ground reality paragraph ending with: Resulting Judgement: ([real_u], [real_psi]) — [Coordinate Label]
Element 3 (The Verdict): Verdict: [PASS/FAIL] — [Path Name]. Explanatory summary.\n\nIntegrity: [Label] (Hypocrisy: [R_net], Uncertainty z: [z])
Element 4 (Sub-Audits Breakdown): Sub-Audits Breakdown:\n- [Aspect A]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Takeaway under 60 chars].\n- [Aspect B]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Takeaway under 60 chars].
Element 5 (What's Happening / Context): Clear, non-technical context paragraph explaining the news event in 1-2 concise sentences.
Element 6 (The Nuance): The Bright Side:\n[Nuance] OR The Poison:\n[Nuance]
Element 7 (The Breakdown & Plane Error): The Breakdown & Plane Error:\n[Plain language explanation of WHAT vs WHO and forensic bait-and-switch]
Element 8 (Social Physics Analysis): Social Physics Analysis:\n[Plain-English dynamics without jargon loops]
Element 9 (The Trajectory & Destination): The Trajectory: The Path of [Path Name].\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward [Outcome/Terminal Zone].
Element 10 (The Unavoidables): The Unavoidable Truth: [1 concise sentence]\n\nThe Unavoidable Lie: [1 concise sentence]
Element 11 (Alethekanon): Alethekanon:\n[Analytical Persona reaction]
Element 12 (Awwthekanon): Awwthekanon:\n[Empathetic Persona reaction]
Element 13 (Brothekanon): Brothekanon:\n[Casual, sharp observer persona reaction]

You MUST return ONLY a valid JSON object matching this schema (NO markdown fences, NO extra words):
{{
  "id": "kebab-case-slug",
  "subject": "Clear descriptive headline",
  "article_title": "Full Investigative Article Headline",
  "article_lede": "Comprehensive 1-2 sentence journalistic lede paragraph setting up the story and structural stakes.",
  "article_body_html": "<p>First detailed context paragraph...</p><h2>Structural Breakdown</h2><p>Second paragraph explaining stated intentions vs actual operations...</p><blockquote>Relevant quote or key empirical evidence point.</blockquote><p>Third paragraph providing social physics analysis and systemic consequences.</p>",
  "claim_u": 0.8,
  "claim_psi": 0.9,
  "real_u": -0.6,
  "real_psi": -0.4,
  "verdict": "FAIL",
  "path": "Path of Deception",
  "actors": ["Actor 1", "Actor 2"],
  "posts": [
    "Punchy editorial hook.\\n\\nHeadline Subject\\nEvidence: stated ideal, actual effect, actual ideal #Aletheia",
    "Stated claim details explaining intent organically.\\nStated Judgement: (+1.0, +1.0) — Greater Good",
    "Actual reality details revealing structural actions.\\nResulting Judgement: (-0.6, -0.4) — Greater Evil",
    "Verdict: FAIL — The Path of Deception.\\nStructural cause summary.\\n\\nIntegrity: Severe Deception (Hypocrisy: 8.5, Uncertainty z: 3)",
    "Sub-Audits Breakdown:\\n- Aspect 1: FAIL (-0.8, -0.5) — Extractive focus.\\n- Aspect 2: COND (+0.2, -0.1) — Partial oversight.",
    "Comprehensive context paragraph detailing the real-world event and policy background.",
    "The Bright Side:\\nNuance or constructive takeaway.",
    "The Breakdown & Plane Error:\\nExplanation of the plane error (WHAT vs WHO) and bait-and-switch.",
    "Social Physics Analysis:\\nNatural human dynamics explaining institutional friction and incentives.",
    "The Trajectory: The Path of Deception.\\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward Greater Evil.",
    "The Unavoidable Truth: Core truth.\\n\\nThe Unavoidable Lie: Core lie.",
    "Alethekanon:\\nAnalytical reaction.",
    "Awwthekanon:\\nEmpathetic reaction.",
    "Brothekanon:\\nCasual reaction."
  ]
}}"""

            last_error = None
            story_obj = None

            for cand in candidates:
                try:
                    use_vertex = cand.startswith("vertex:")
                    actual_model = cand.split(":", 1)[1] if use_vertex else cand
                    client = get_gemini_client(use_vertex=use_vertex)
                    
                    config = types.GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=4096,
                        system_instruction=system_prompt,
                        response_mime_type="application/json"
                    )
                    
                    res = client.models.generate_content(
                        model=actual_model,
                        contents=[types.Content(role="user", parts=[types.Part.from_text(text=f"Create a complete news article and 14-post Multi-Aspect Aletheia thread from this discussion:\n\n{chat_text[:8000]}")]),],
                        config=config
                    )
                    raw_json = res.text.strip()
                    if raw_json.startswith("```"):
                        raw_json = re.sub(r'^```(?:json)?\s*', '', raw_json)
                        raw_json = re.sub(r'\s*```$', '', raw_json)
                    story_obj = json.loads(raw_json)
                    
                    # Sanitize any accidental numbered prefixes from posts
                    if story_obj and "posts" in story_obj and isinstance(story_obj["posts"], list):
                        clean_posts = []
                        for p in story_obj["posts"]:
                            p_clean = re.sub(r'^(?:Post\s*\d+[:.]?\s*|\d+[:.]\s*)', '', str(p)).strip()
                            clean_posts.append(p_clean)
                        story_obj["posts"] = clean_posts[:14]

                    break
                except Exception as e:
                    last_error = e
                    print(f"[Chat Server] Story generation fallback from {cand} due to error: {e}", file=sys.stderr)

            if story_obj:
                slug = story_obj.get("id") or re.sub(r'[^a-zA-Z0-9_-]', '-', story_obj.get("subject", "new_story")).lower()[:40]
                slug = slug.strip("-")
                story_obj["id"] = slug
                
                # Render and save the full news story article HTML
                art_title = story_obj.get("article_title") or story_obj.get("subject", "News Story")
                art_lede = story_obj.get("article_lede", "")
                art_body = story_obj.get("article_body_html", "<p>No body text generated.</p>")
                
                rendered_article_html = render_news_article_html(
                    title=art_title,
                    lede=art_lede,
                    body_html=art_body,
                    coordinates_info={
                        "claim_u": story_obj.get("claim_u", 0.0),
                        "claim_psi": story_obj.get("claim_psi", 0.0),
                        "real_u": story_obj.get("real_u", 0.0),
                        "real_psi": story_obj.get("real_psi", 0.0),
                        "verdict": story_obj.get("verdict", "AUDIT"),
                        "path": story_obj.get("path", "Geodesic")
                    },
                    slug=slug
                )
                
                article_filename = f"{slug}.html"
                article_path = os.path.join(ARTICLES_DIR, article_filename)
                with open(article_path, "w", encoding="utf-8") as af:
                    af.write(rendered_article_html)
                print(f"[Chat Server] Rendered source news article HTML: {article_path}")

                canonical_article_url = f"http://localhost:8766/articles/{article_filename}"
                story_obj["link"] = canonical_article_url
                story_obj["id"] = slug
                story_obj["mode"] = "root"
                story_obj["status"] = "COMPLETED DRY RUN"
                story_obj["multiAspect"] = (len(story_obj.get("posts", [])) == 14)
                
                # Also save to stories draft automatically
                target_json_path = os.path.join(STORIES_DIR, f"factcheck_{slug}.json")
                try:
                    with open(target_json_path, "w", encoding="utf-8") as sf:
                        json.dump([story_obj], sf, indent=2, ensure_ascii=False)
                    STORY_REGISTRY[slug] = story_obj
                except Exception as ex:
                    print(f"[Chat Server] Warning auto-saving draft JSON: {ex}", file=sys.stderr)

                self.send_json(200, {
                    "status": "ok",
                    "story": story_obj,
                    "article_url": canonical_article_url,
                    "article_html": rendered_article_html,
                    "article_title": art_title
                })
            else:
                self.send_json(500, {"error": f"Story generation failed across all models: {last_error}"})
            return

        if parsed.path == "/story/save_draft":
            story_data = req_data.get("story", {})
            if not story_data:
                self.send_json(400, {"error": "Missing story payload"})
                return

            slug = story_data.get("id") or re.sub(r'[^a-zA-Z0-9_-]', '-', story_data.get("subject", "new_story")).lower()[:40]
            slug = slug.strip("-")
            story_data["id"] = slug
            story_data["mode"] = story_data.get("mode") or "root"
            story_data["status"] = "COMPLETED DRY RUN"
            story_data["multiAspect"] = (len(story_data.get("posts", [])) == 14)
            story_data["_mtime"] = datetime.datetime.now().timestamp()

            target_filename = f"factcheck_{slug}.json"
            target_path = os.path.join(STORIES_DIR, target_filename)

            try:
                with open(target_path, "w", encoding="utf-8") as f:
                    json.dump([story_data], f, indent=2, ensure_ascii=False)
                
                # Update in-memory registry
                STORY_REGISTRY[slug] = story_data
                print(f"[Chat Server] Saved draft story to {target_path}")
                self.send_json(200, {
                    "status": "ok",
                    "filename": target_filename,
                    "filepath": target_path,
                    "story": story_data
                })
            except Exception as e:
                self.send_json(500, {"error": f"Failed to save file: {e}"})
            return

        if parsed.path == "/story/expand_posts":
            story_data = req_data.get("story", {})
            model = req_data.get("model", "vertex:gemini-3.7-flash")
            post_idx = req_data.get("post_index")  # optional single post index
            
            expand_prompt = """You are Aletheia's thread optimizer. Your goal is to maximize the information density, nuance, and structural precision of the posts so they fill close to the maximum 290 character limit (strictly between 270 and 292 characters).

RULES:
1. Every post MUST be between 270 and 292 characters (including spaces, emojis, hashtags).
2. NEVER exceed 295 characters (hard cutoff).
3. Deepen the social physics, empirical data, or philosophical clarity to fill the space naturally.
4. Return ONLY a JSON object matching: {"posts": ["Post 1...", ..., "Post 14..."]}"""

            try:
                use_vertex = model.startswith("vertex:")
                actual_model = model.split(":", 1)[1] if use_vertex else model
                client = get_gemini_client(use_vertex=use_vertex)
                
                config = types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=4096,
                    system_instruction=expand_prompt,
                    response_mime_type="application/json"
                )
                
                curr_posts_str = json.dumps(story_data.get("posts", []))
                prompt_content = f"Story Subject: {story_data.get('subject')}\nClaim: ({story_data.get('claim_u')}, {story_data.get('claim_psi')}) | Real: ({story_data.get('real_u')}, {story_data.get('real_psi')})\nCurrent Posts:\n{curr_posts_str}\n\nExpand each post to fill 270-292 characters:"
                
                res = client.models.generate_content(
                    model=actual_model,
                    contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt_content)])],
                    config=config
                )
                raw_json = res.text.strip()
                res_obj = json.loads(raw_json)
                new_posts = res_obj.get("posts", story_data.get("posts", []))
                
                if post_idx is not None and isinstance(post_idx, int) and 0 <= post_idx < len(new_posts):
                    story_data["posts"][post_idx] = new_posts[post_idx]
                else:
                    story_data["posts"] = new_posts
                    
                self.send_json(200, {"status": "ok", "story": story_data})
            except Exception as e:
                print(f"[Chat Server] Post expansion error: {e}", file=sys.stderr)
                self.send_json(500, {"error": f"Expansion failed: {e}"})
            return

        # ── Main Chat Endpoint ────────────────────────────────────────────────
        if parsed.path == "/chat":
            user_msg = req_data.get("message", "")
            session_id = req_data.get("session_id")
            thread_id = req_data.get("thread_id", "main")
            model = req_data.get("model", "vertex:gemini-3.7-flash")
            use_search = req_data.get("use_search", True)
            attachments = req_data.get("attachments", [])
            
            # Thinking & output controls
            thinking_level = req_data.get("thinking_level", "MEDIUM")
            temperature = req_data.get("temperature", 0.3)
            max_tokens = req_data.get("max_tokens", 8192)
            custom_instructions = req_data.get("custom_instructions", "")
            canvas_story = req_data.get("canvas_story")

            # Load active session and thread
            session = load_session(session_id) if session_id else None
            active_thread_msgs = []
            ancestral_msgs = []
            narrative_spine = []

            if session:
                threads = session.get("threads", {})
                target_thread = threads.get(thread_id, threads.get("main", {}))
                active_thread_msgs = target_thread.get("messages", [])
                narrative_spine = session.get("narrative_spine", [])

                # If sub-thread, retrieve ancestor messages up to fork index
                parent_tid = target_thread.get("parent_thread_id")
                fork_idx = target_thread.get("fork_message_index", 0)
                if parent_tid and parent_tid in threads:
                    ancestral_msgs = threads[parent_tid].get("messages", [])[:fork_idx + 1]

            try:
                llm_res = call_llm_chat(
                    user_msg,
                    history=active_thread_msgs,
                    ancestral_history=ancestral_msgs,
                    narrative_spine=narrative_spine,
                    model=model,
                    use_search=use_search,
                    attachments=attachments,
                    thinking_level=thinking_level,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    custom_instructions=custom_instructions,
                    canvas_story=canvas_story
                )
                self.send_json(200, llm_res)
            except Exception as e:
                print(f"[Chat Server] LLM Execution Error: {e}", file=sys.stderr)
                self.send_json(500, {"error": str(e)})
            return

        self.send_json(404, {"error": "Not Found"})


def run_server():
    server = HTTPServer(("localhost", PORT), ChatHandler)
    print(f"============================================================")
    print(f"ALETHEIA CHAT SERVER ONLINE ON PORT {PORT}")
    print(f"Endpoint: http://localhost:{PORT}")
    print(f"Default Model: vertex:gemini-3.7-flash")
    print(f"Hierarchical Topic Threading & Dual-Track Memory Active")
    print(f"============================================================")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
