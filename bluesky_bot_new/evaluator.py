import os
import sys
import json
import re
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from renderer import get_path_name

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

def load_convergence_spec():
    vft_root = os.path.abspath(os.path.join(script_dir, ".."))
    path = os.path.join(vft_root, ".agent", "tools", "convergence-test", "convergence_son_potential.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

DEFAULT_FALLBACKS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
    "vertex:gemini-3.8-flash",
    "vertex:gemini-3.7-flash",
    "vertex:gemini-3.1-flash-lite",
    "gemini-3-flash-preview",
    "gemma-4-31b-it",
    "gemma-4-26b-a4b-it",
    "agnes-2.0-flash",
]

SPIRITUAL_TRADITIONS = """Allowed Traditions:
- Christian / Abrahamic (Gospels, Epistles, Hebrew Prophets like Isaiah/Amos, Psalms, Proverbs, Ecclesiastes)
- Hindu / Vedic (Bhagavad Gita, Upanishads, Mahabharata, Vedas — Dharma, Karma, Rita)
- Buddhist / Dharmic (Dhammapada, Pali Canon, Sutta Nipata, Heart Sutra, Zen Koans — Ahimsa, Interdependence)
- Taoist / Eastern Metaphysics (Tao Te Ching, Zhuangzi, I Ching — Wu Wei, natural harmony)
- Islamic & Sufi (Quran, Hadith, Rumi's Masnavi, Attar, Saadi — Social equity, Sacred Trust/Amanah)
- Indigenous & Custodial Lore (First Nations / Alcheringa Dreaming Law, Haudenosaunee Great Law, Ubuntu)
- Stoic & Classical Philosophy (Marcus Aurelius' Meditations, Epictetus, Seneca, Platonic dialogues)"""

SYSTEM_INSTRUCTION = """Today's reference date is {today_str}.
You are the Master Aletheia News Auditor. You evaluate real-world news events strictly according to the **Convergence Test (SON Potential) — Modal & Temporal Topology of the Hegemony** detailed below.

=== THE AUTHORITATIVE CONVERGENCE TEST (SON POTENTIAL) ===
{convergence_spec}

GROUND TRUTH & INSTITUTIONAL ANCHORING DIRECTIVE:
You must always anchor your audit in the real-world event and its primary actors, NOT in media punditry or talking heads.
Evaluate three core pillars:
1. Institutional Actions: What did the institutions involved (universities, courts, police, government bodies, corporations) actually do, fail to do, or try to hide?
2. Empirical Evidence: What do documented records, official filings, timelines, and physical facts prove actually happened?
3. Human Impacts: Who suffered real harm, trauma, financial loss, or danger, and who protected or failed them?

STATED CLAIM DEFINITION ACROSS ALL NEWS & ABSOLUTE BAN ON AUDITING REPORTING:
- The Stated Claim (Element 1 / Post 2) is the substantive real-world assertion of the event being reported in the headline and article.
- ABSOLUTE BAN ON AUDITING NEWS REPORTING: You are strictly forbidden from writing 'News coverage presents objective reporting...', 'The article reports...', or evaluating the journalist/outlet as the Stated Claim. The reporting outlet is an observer ('author'), NOT the audited actor!
- CONVERGENCE = PASS: If the headline/article asserts that an event occurred, and empirical evidence (police reports, court filings, official records, hospital releases) confirms that event occurred, the claim CONVERGES with physical reality -> PASS. Both the claim and the reality reflect the physical event.
- Hypocrisy / FAIL only exists when there is an empirical DIVERGENCE between what was claimed and what actually happened (e.g. claiming an accidental fire when evidence proves deliberate arson; or claiming a policy saves taxpayer money when it secretly extracts billions).

MEDIA PUNDITRY & ANTI-GOTCHA RULE:
- Never allow the audit to be tricked or hijacked by partisan media arguments or columnist commentary. Cut straight to the underlying crime, event, or institutional failure.

THE 15-POST THREAD SEQUENCE:
Your response must provide exactly 15 sequential posts in the 'posts' array.
CRITICAL: Every single post MUST be strictly under 280 characters to fit Bluesky limits (target 230-265 characters). No post may exceed 280 characters.

Post 1 (Hook): Scene setting one-liner exposing structural irony + clean title + 'Evidence: [Stated], [Actual], [Actual Ideal] #Aletheia #[Topic]'. (Append 🌐 at the very end if verified with grounding source).
Post 2 (Claim): Explains substantive claim organically. Ends with 'Stated Judgement: ([claim_u], [claim_psi]) — [Coordinate Label]'.
Post 3 (Reality): Exposes ground reality organically. Ends with 'Resulting Judgement: ([real_u], [real_psi]) — [Coordinate Label]'.
Post 4 (Verdict): Overall verdict line: 'Verdict: [PASS/FAIL] — [Path Name]. [1-2 sentence explanation of trajectory cause]. Integrity: [Absolute Truth / Trustworthy / Meaningful Distortion / Severe Deception] (Hypocrisy: [delta], z: [uncertainty])'.
Post 5 (Multi-Aspect Breakdown): Dedicated sub-audits of the physical event's constituent actors/aspects (Instigator, Regulator, Acted-upon target). Bullet points under 60 chars each:
  - [Actor / Aspect A]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Brief action reason].
  - [Actor / Aspect B]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Brief action reason].
Post 6 (Context): Clear, non-technical context paragraph explaining the event and its background.
Post 7 (Nuance): 'The Bright Side:\\n[nuance]' (if negative) or 'The Poison:\\n[nuance]' (if positive).
Post 8 (Breakdown & Plane Error): Expose the Plane Error in plain English (e.g. WHAT vs WHO, Physical vs Will) and the structural bait-and-switch.
Post 9 (Social Physics Analysis): 'Social Physics Analysis:\\n' Grounded in The 42 of Social Physics: audit actors across the 4 axes (Power vs Empowerment, Justification vs Transparency, Projection vs Empathy, Manufactured Problems vs Solutions) exposing Smart Selfish vs Smart Altruistic maneuvers.
Post 10 (The Trajectory): 'The Trajectory: The Path of [Path Name].\\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward [Outcome Zone]. [1-sentence explanation]'.
Post 11 (The Unavoidables):
  The Unavoidable Truth: [1 concise sentence]
  The Unavoidable Lie: [1 concise sentence]
Post 12 (Alethekanon): Uncompromising structural analysis, pure logic, max signal, zero noise. 'Alethekanon:\\n[Paragraph]'.
Post 13 (Awwthekanon): Empathy, human cost, somatic reaction, healing. 'Awwthekanon:\\n[Paragraph]'.
Post 14 (Brothekanon): Casual observer, humor, pointing out the sheer absurdity/pub test. 'Brothekanon:\\n[Paragraph]'.
Post 15 (Spirithekanon): Authentic canonical scriptural/philosophical passage with exact source citation and ethical reflection:
  Spirithekanon:
  \"[Verbatim Canonical Quote]\" [Source Book Chapter:Verse or Section] [PASS/FAIL/HIT]
  [1 concise sentence of deep ethical/philosophical reflection].

{spiritual_traditions}

POTENTIAL MODE SPECIFICATION:
- modal_claim: Stated claim Modal node string ("is", "will be", "is like", "was like", "can be", "can't be", "May be", "Won't be", "is not")
- modal_real: Actual ground reality Modal node string ("is", "will be", "is like", "was like", "can be", "can't be", "May be", "Won't be", "is not")
- modal_vector: Quadrant transition or trajectory description (e.g. "Top-Right to Bottom-Left Inversion")
- geodesic: Dynamic Geodesic name (e.g. "Red Top (The Imperial Trap)", "Red Bottom (The PR Shield)", "Pretext Tether", "Grace")
- central_is_barrier_crossed: boolean (true if trajectory crossed central IS barrier from +u to -u, else false)

ACTOR ENTITIES & 7-ROLE CLASSIFICATION DIRECTIVE:
Classify key entities in the 'actors' array: 'acted_upon', 'regulator', 'instigator', 'beneficiary', 'author', 'context', 'misc'.
"""

ATTRACTOR_SON_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "S": {"type": "NUMBER", "description": "Support force (0.0 to 2.0)"},
        "O": {"type": "NUMBER", "description": "Oppose force (0.0 to 2.0)"},
        "N": {"type": "NUMBER", "description": "Neutral force (0.0 to 2.0)"}
    },
    "required": ["S", "O", "N"]
}

FORCES_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "GG": ATTRACTOR_SON_SCHEMA,
        "GE": ATTRACTOR_SON_SCHEMA,
        "LG": ATTRACTOR_SON_SCHEMA,
        "LE": ATTRACTOR_SON_SCHEMA,
        "GP": ATTRACTOR_SON_SCHEMA,
        "BP": ATTRACTOR_SON_SCHEMA
    },
    "required": ["GG", "GE", "LG", "LE", "GP", "BP"]
}

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "thinking": {"type": "STRING", "description": "Phase 1 to 5 calculations, 18-variable attractor scoring, and modal proofs"},
        "id": {"type": "STRING", "description": "Clean lowercase hyphenated slug (e.g. waterford-family-tragedy)"},
        "subject": {"type": "STRING", "description": "Full, non-truncated subject headline"},
        "claim_u": {"type": "NUMBER", "description": "Stated morality (-2.0 to +2.0)"},
        "claim_psi": {"type": "NUMBER", "description": "Stated will (-2.0 to +2.0)"},
        "real_u": {"type": "NUMBER", "description": "Actual morality (-2.0 to +2.0)"},
        "real_psi": {"type": "NUMBER", "description": "Actual will (-2.0 to +2.0)"},
        "stated_forces": FORCES_SCHEMA,
        "actual_forces": FORCES_SCHEMA,
        "verdict": {"type": "STRING", "enum": ["PASS", "FAIL", "CONDITIONAL"]},
        "grounding_url": {"type": "STRING", "description": "URL of secondary verification source or official documentation if available, otherwise empty string"},
        "modal_claim": {"type": "STRING", "description": "Potential mode stated modal node"},
        "modal_real": {"type": "STRING", "description": "Potential mode actual ground reality modal node"},
        "modal_vector": {"type": "STRING", "description": "Quadrant transition description"},
        "geodesic": {"type": "STRING", "description": "Dynamic geodesic name"},
        "central_is_barrier_crossed": {"type": "BOOLEAN", "description": "Whether central IS barrier was crossed"},
        "aspects": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "aspect": {"type": "STRING"},
                    "claim_u": {"type": "NUMBER"},
                    "claim_psi": {"type": "NUMBER"},
                    "real_u": {"type": "NUMBER"},
                    "real_psi": {"type": "NUMBER"},
                    "verdict": {"type": "STRING", "enum": ["PASS", "FAIL", "CONDITIONAL"]},
                    "reason": {"type": "STRING"}
                },
                "required": ["aspect", "real_u", "real_psi", "verdict", "reason"]
            }
        },
        "posts": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Exactly 15 posts under 280 chars each: Hook, Claim, Reality, Verdict, Multi-Aspect, Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Alethekanon, Awwthekanon, Brothekanon, Spirithekanon"
        },
        "actors": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "role": {"type": "STRING", "enum": ["acted_upon", "regulator", "instigator", "beneficiary", "author", "context", "misc"]}
                },
                "required": ["name", "role"]
            }
        }
    },
    "required": [
        "thinking", "id", "subject", "claim_u", "claim_psi", "real_u", "real_psi",
        "stated_forces", "actual_forces", "verdict",
        "modal_claim", "modal_real", "modal_vector", "geodesic", "central_is_barrier_crossed",
        "aspects", "posts", "actors"
    ]
}

def evaluate_candidate(candidate, model_name="gemini-2.5-flash", model_sequence=None, api_key=None):
    """
    Evaluates a single news candidate using Gemini with native structured JSON output.
    Ensures 1:1 synchronization between coordinates, posts, and canonical path names.
    Supports graceful model fallback across an ordered sequence of Gemini models.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    client = genai.Client(api_key=key)
    today_str = datetime.now().strftime("%Y-%m-%d")
    conv_spec = load_convergence_spec()
    sys_inst = SYSTEM_INSTRUCTION.format(
        today_str=today_str,
        spiritual_traditions=SPIRITUAL_TRADITIONS,
        convergence_spec=conv_spec
    )

    user_prompt = f"""EVALUATE THIS NEWS EVENT USING THE 6-ATTRACTOR SON POTENTIAL CONVERGENCE TEST:
Subject: {candidate.get('subject') or candidate.get('title')}
URL: {candidate.get('url') or candidate.get('link')}

Article Content:
{candidate.get('body') or candidate.get('text') or 'No body provided.'}
"""

    config = types.GenerateContentConfig(
        system_instruction=sys_inst,
        response_mime_type="application/json",
        response_schema=RESPONSE_SCHEMA,
        temperature=0.2,
    )

    # Build unique fallback model list
    models_to_try = []
    if model_sequence:
        for m in model_sequence:
            if m and m not in models_to_try:
                models_to_try.append(m)
    elif model_name:
        models_to_try.append(model_name)
        for m in DEFAULT_FALLBACKS:
            if m not in models_to_try:
                models_to_try.append(m)
    else:
        models_to_try = list(DEFAULT_FALLBACKS)

    last_error = None
    response = None
    used_model = None

    for model in models_to_try:
        print(f"Attempting evaluation with model: {model}...")
        try:
            response = client.models.generate_content(
                model=model,
                contents=user_prompt,
                config=config
            )
            used_model = model
            print(f"Successfully evaluated candidate using {model}!")
            break
        except Exception as e:
            last_error = e
            print(f"Warning: Model {model} failed: {e}. Falling back to next model in sequence...")

    if response is None:
        raise RuntimeError(f"All models in fallback sequence failed. Last error: {last_error}")

    parsed = json.loads(response.text)
    parsed["evaluated_by_model"] = used_model

    # 1. Authoritative Coordinate Extraction & Canonical Geodesic Binding
    claim_u = float(parsed["claim_u"])
    claim_psi = float(parsed["claim_psi"])
    real_u = float(parsed["real_u"])
    real_psi = float(parsed["real_psi"])
    
    math_path = get_path_name(claim_u, claim_psi, real_u, real_psi)
    parsed["path_name"] = math_path

    # 2. Synchronize Post 4 (The Verdict line)
    verdict = parsed["verdict"]
    posts = parsed.get("posts", [])
    if len(posts) >= 4:
        if not posts[3].startswith("Verdict:"):
            posts[3] = f"Verdict: {verdict} — {math_path}."
        elif math_path not in posts[3]:
            posts[3] = re.sub(r'Verdict:\s*[A-Z]+\s*—\s*[^.]+\.', f"Verdict: {verdict} — {math_path}.", posts[3])

    # 3. Grounding URL & Emoji synchronization in Post 1
    grounding_url = parsed.get("grounding_url", "").strip()
    if grounding_url and len(posts) > 0 and not posts[0].endswith("🌐"):
        posts[0] = f"{posts[0].rstrip()} 🌐"

    parsed["posts"] = posts
    parsed["link"] = candidate.get("url") or candidate.get("link") or ""
    parsed["created_at"] = today_str

    return parsed
