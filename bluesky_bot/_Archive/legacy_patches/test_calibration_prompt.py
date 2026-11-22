import os
import sys
import json
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
load_dotenv(os.path.join(script_dir, ".env"))

import google_ai_studio_one_shot as bot_engine
from generate_graph import enforce_deterministic_trajectory

# 1. Target story for comparison
target_fn = "factcheck_france_nationwide_strikes_2026.json"
target_fp = os.path.join(script_dir, "stories", target_fn)

with open(target_fp, "r", encoding="utf-8") as f:
    old_data = json.load(f)
old_story = old_data[0] if isinstance(old_data, list) else old_data

candidate = {
    "subject": old_story.get("subject"),
    "url": old_story.get("link") or old_story.get("url"),
    "target_url": old_story.get("target_url", ""),
    "mode": "root",
    "text": old_story.get("scraped_text", "")
}

print("=================================================================")
print("RUNNING CALIBRATION BENCHMARK TEST")
print(f"Target: {candidate['subject']}")
print(f"URL: {candidate['url']}")
print(f"OLD AUDIT (Uncalibrated): Stated ({old_story.get('claim_u')}, {old_story.get('claim_psi')}) -> Actual ({old_story.get('real_u')}, {old_story.get('real_psi')})")
print("=================================================================\n")

# 2. Calibration block to inject
CALIBRATION_DIRECTIVE = """
COORDINATE SCALE CALIBRATION DIRECTIVE (VFT CANONICAL HORIZONS):
When judging the morality (υ) and will (ψ) of any action, claim, or policy, you must map the coordinates strictly against the following concentric horizons. Do not moralize — map and calculate:

AXIS υ (Morality) — Who does this benefit?
  +2 Everyone / All beings (Systemic Justice)
  +1 Other people (Greater Good)
  +0 No one / Neutral
  -1 My group only (Lesser Evil)
  -2 Only me (Tyranny / Pure Extraction)
  (Spectrum: Everyone -> Other Beings -> A Being -> No One -> My Group -> Me -> Only Me)

AXIS ψ (Will) — What is the energy doing?
  +2 Actively creating systemic value for all (Productive Justice)
  +1 Proactive — creating, building, acting
  +0 Neutral — no meaningful force applied
  -1 Passive — allowing, suppressing, withholding
  -2 Actively destroying or extracting value (Chaos / Collapse)

CANONICAL BENCHMARK HORIZONS:
- Ring 2.0 (Systemic / Civilizational — Structural Shift across Humanity / Species):
  * (+2, +2) Salk polio vaccine, Universal Human Rights, municipal sanitation.
  * (-2, +2) Atlantic slave trade, WMD war pretext, Big Tobacco 50-yr coverup.
  * (-2, -2) Holocaust, Chernobyl coverup, Holodomor famine, nuclear war.
  * (+2, -2) Montreal Protocol (banning CFCs), Cuban Missile Crisis de-escalation.
- Ring 1.0 (Individual / Human / National — Affects Millions & Legal Architecture):
  * (+1, +1) Civil Rights Act, Medicare, Apollo program, Robodebt Royal Commission.
  * (-1, +1) Enron, 2008 subprime mortgage fraud, Watergate, gerrymandering.
  * (-1, -1) Flint water poisoning, Texas 2021 grid freeze, systemic corruption.
  * (+1, -1) Antitrust breakup, peaceful election concession, public health pause.
- Ring 0.5 (Perceptual Inversion Zone / Local Events / Everyday Civic & Commercial):
  * (+0.5, +0.5) Local school bond, community clinic, open-sourcing useful software.
  * (-0.5, +0.5) Misleading campaign ad, corporate astroturfing, hidden junk fees.
  * (-0.5, -0.5) Fatal 143mph crash, postal ballot theft, localized shelter neglect.
  * (+0.5, -0.5) Postponing event for weather/safety, temporary union strike / collective bargaining.
- Neutral Horizon (0.0):
  * Procedural court scheduling, neutral parliamentary rulings, routine commercial litigation.

MANDATORY CALIBRATION BOUNDS:
Before scoring any event <= -0.7 or >= +0.7, verify the blast radius. Is this event structurally comparable to Flint, Michigan (-1.0), Enron (-1.0), or Chernobyl (-2.0)?
Routine strikes, union protests, campaign debates, and commercial lawsuits belong in the local/civic scale ([-0.3, +0.4]), NOT civilizational catastrophe (<= -0.8).
"""

# 3. Build instructions with injected calibration
conv_rules, form_rules = bot_engine.build_formatting_rules(use_son=True, compact=False)
sys_inst = bot_engine.build_system_instruction(use_son=True, compact=False)
sys_inst_calibrated = sys_inst + "\n\n" + CALIBRATION_DIRECTIVE

output_fmt = bot_engine.build_output_format(1, use_son=True)

clean_cands = [{
    "subject": candidate["subject"],
    "url": candidate["url"],
    "target_url": candidate["target_url"],
    "mode": candidate["mode"],
    "text": candidate["text"][:2500]
}]

user_payload = (
    f"=== CONVERGENCE TEST RULES ===\n{conv_rules}\n\n"
    f"=== THREAD FORMATTING & SCHEMAS ===\n{form_rules}\n\n"
    f"=== SCALE CALIBRATION BENCHMARKS ===\n{CALIBRATION_DIRECTIVE}\n\n"
    f"You are evaluating 1 candidate news item.\n\n"
    f"=== CANDIDATES TO EVALUATE (1 total) ===\n{json.dumps(clean_cands, separators=(',', ':'), ensure_ascii=False)}\n\n"
    f"{output_fmt}"
)

# 4. Run through Gemini API client
genai_client = bot_engine.get_gemini_client()
if not genai_client:
    print("ERROR: genai_client could not be initialized.")
    sys.exit(1)

model_name = "gemini-2.5-flash"
print(f"Calling Gemini API with calibrated prompt (Model: {model_name})...")

try:
    from google.genai import types
    config = types.GenerateContentConfig(
        system_instruction=sys_inst_calibrated,
        temperature=0.2,
    )
    response = genai_client.models.generate_content(
        model=model_name,
        contents=user_payload,
        config=config
    )
    raw_output = response.text.strip()
except Exception as e:
    print(f"Primary call failed: {e}. Trying fallback...")
    raw_output = bot_engine.call_agnes_api(
        os.environ.get("AGNES_API_KEY"),
        sys_inst_calibrated,
        user_payload,
        model="agnes-2.0-flash"
    )

print("Received API response. Parsing evaluations...")
eval_dicts = bot_engine.transpose_flat_to_json(raw_output, use_potential=False)
if not eval_dicts:
    print("Could not parse output:")
    print(raw_output[:1000])
    sys.exit(1)

new_story = eval_dicts[0]
new_story = enforce_deterministic_trajectory(new_story)

print("\n" + "="*70)
print("CALIBRATION TEST COMPARISON RESULTS")
print("="*70)
print(f"STORY: {candidate['subject']}")
print("-" * 70)
print(f"BEFORE (Uncalibrated): Stated ({old_story.get('claim_u')}, {old_story.get('claim_psi')}) -> Actual ({old_story.get('real_u')}, {old_story.get('real_psi')})")
print(f"BEFORE Verdict Line: {old_story.get('posts', [])[3].splitlines()[0]}")
print("-" * 70)
print(f"AFTER (Calibrated):   Stated ({new_story.get('claim_u')}, {new_story.get('claim_psi')}) -> Actual ({new_story.get('real_u')}, {new_story.get('real_psi')})")
print(f"AFTER Verdict Line:  {new_story.get('posts', [])[3].splitlines()[0]}")
print("-" * 70)
print("AFTER Posts 0 to 4:")
for i, p in enumerate(new_story.get("posts", [])[:5]):
    print(f"  [Post {i}] {p}")
print("="*70)
