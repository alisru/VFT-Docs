import os

fp = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\google_ai_studio_one_shot.py"
with open(fp, "r", encoding="utf-8") as f:
    content = f.read()

calibration_block = '''COORDINATE_SCALE_CALIBRATION = """=== COORDINATE SCALE CALIBRATION ANCHORS (CANONICAL VFT HORIZONS) ===
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
  * (+2, +2) Salk polio vaccine, Universal Human Rights, municipal water sanitation.
  * (-2, +2) Atlantic slave trade, WMD war pretext, Big Tobacco 50-yr cancer coverup.
  * (-2, -2) Holocaust, Chernobyl coverup, Holodomor famine, nuclear war.
  * (+2, -2) Montreal Protocol (banning CFCs), Cuban Missile Crisis de-escalation.
- Ring 1.0 (Individual / Human / National — Affects Millions & Legal Architecture):
  * (+1, +1) Civil Rights Act, Medicare, Apollo program, Robodebt Royal Commission.
  * (-1, +1) Enron, 2008 subprime mortgage fraud, Watergate, partisan gerrymandering.
  * (-1, -1) Flint water poisoning, Texas 2021 grid freeze, systemic police corruption.
  * (+1, -1) Antitrust breakup, peaceful election concession, emergency public health pause.
- Ring 0.5 (Perceptual Inversion Zone / Local Events / Everyday Civic & Commercial):
  * (+0.5, +0.5) Local school bond, community clinic, open-sourcing useful software.
  * (-0.5, +0.5) Misleading campaign ad, corporate astroturfing, hidden junk fees.
  * (-0.5, -0.5) Fatal 143mph crash, postal ballot theft, localized shelter neglect.
  * (+0.5, -0.5) Postponing event for weather/safety, temporary union strike / collective bargaining.
- Neutral Horizon (0.0):
  * Procedural court scheduling, neutral parliamentary rulings, routine commercial litigation.

MANDATORY CALIBRATION BOUNDS:
Before scoring any event <= -0.7 or >= +0.7, verify the blast radius against these benchmarks. Is the event structurally comparable to Flint, Michigan (-1.0), Enron (-1.0), or Chernobyl (-2.0)?
Routine strikes, union protests, campaign debates, and commercial lawsuits belong strictly in the local/civic scale ([-0.3, +0.4]), NOT civilizational catastrophe (<= -0.8).
"""
'''

target = """_RULES_CACHE = {}

def _load_rules(use_son=False, use_potential=False):"""

replacement = f"""{calibration_block}
_RULES_CACHE = {{}}

def _load_rules(use_son=False, use_potential=False):"""

if target in content and "COORDINATE_SCALE_CALIBRATION =" not in content:
    content = content.replace(target, replacement)
    
    # Also update where convergence is minified and stored in cache:
    old_cache = """        with open(convergence_path, "r", encoding="utf-8") as f:
            _RULES_CACHE[f"{cache_key}_convergence"] = minify_markdown(f.read())"""
            
    new_cache = """        with open(convergence_path, "r", encoding="utf-8") as f:
            _RULES_CACHE[f"{cache_key}_convergence"] = COORDINATE_SCALE_CALIBRATION + "\\n\\n" + minify_markdown(f.read())"""
            
    if old_cache in content:
        content = content.replace(old_cache, new_cache)
        print("Updated convergence cache to prepend calibration block.")
    else:
        print("old_cache target not found, searching alternative...")
        
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully patched google_ai_studio_one_shot.py with calibration block before convergence tests.")
else:
    print("Target already present or not found.")
