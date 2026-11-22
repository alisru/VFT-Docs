# Implementation Plan v39: Simplified Multi-Source Harvest & Objective Vector Scoring

## Goal Description
Strip away overengineered rules and fix the two core issues:
1. **Harvester**: Stop throwing away alternative coverage. When multiple RSS or Bluesky feeds report on the same event, combine their text into the story candidate so the AI has the full context.
2. **Evaluator**: Tell the AI to stop cheerleading articles and judge them objectively per the Vector Field Theory coordinates $(\upsilon, \psi)$:
   - Axis $\upsilon$ (Morality): Who actually benefits? (+2 Systemic Good to -2 Pure Extraction)
   - Axis $\psi$ (Will): What is the energy physically doing? (+2 Creation to -2 Destruction)
   - Do not accept partisan spin as reality. Score the physical facts on the ground.

---

## Proposed Changes

### 1. Harvester (`bluesky_bot/harvest_candidates.py`)
- When clustering candidates, keep all articles covering the same event together into `cross_source_dossier`.
- Do not drop alternative outlet coverage as "duplicates".

### 2. Evaluator Prompt (`bluesky_bot/google_ai_studio_one_shot.py`)
- Simple, direct prompt instruction:
  - *"Judge the story objectively using the $(\upsilon, \psi)$ vectors based on physical actions and ground reality, not the outlet's political spin or cheerleading."*

---

## Verification
- Run a test candidate through evaluation and verify the AI scores the vectors objectively against real-world impact.
