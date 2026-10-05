# Implementation Plan - Fix Stuck Harvested Story Queue Pruning & Deduplication

## Problem
A single story ("Australia Considers Smart Glasses Ban in Government Workplaces...") remains persistently stuck in `bluesky_bot/harvested_candidates.json`, resulting in `📥 Queue: 1` in the AletheiaLauncher HUD.
Although the story was evaluated and published to `stories/live/`, it could not be popped or deduplicated because:
1. `google_ai_studio_one_shot.py` compares candidate `url` against evaluated `link`. For bridged/feed candidates, candidate `url` is the ActivityPub link, evaluated `link` is the primary article link (e.g. Slashdot), and `target_url` is the Bluesky post. Since neither `target_url` nor multiple URL aliases are cross-matched, the candidate is never pruned.
2. `harvest_candidates.py` short-circuits on `config.get("link") or config.get("target_url")`, omitting `target_url` from `seen_evaluated_urls`. When reading the queue, it also only checks `c.get("url")` against `seen_evaluated_urls`, causing the candidate to be preserved on every subsequent harvest run.

## Proposed Changes
1. **Clear Stuck Queue**:
   - Overwrite `bluesky_bot/harvested_candidates.json` with `[]`.
2. **Patch `google_ai_studio_one_shot.py`**:
   - In chunk evaluation result deduction (around line 2499 and line 2524), index all URL fields (`link`, `target_url`, `grounding_url`, `url`) from evaluated stories.
   - Match candidate using any of its URL fields (`url`, `target_url`) against evaluated URLs so bridged / multi-source candidates are accurately recognized and deducted.
3. **Patch `harvest_candidates.py`**:
   - In historical/live story scanning (around lines 560-571), register both `link` and `target_url` (and `grounding_url`) into `seen_historical_urls` and `seen_evaluated_urls`.
   - In queue loading (around lines 596-602), check both candidate `url` and `target_url` against `seen_evaluated_urls` so already evaluated stories are pruned upon loading.

## Verification
- Confirm `harvested_candidates.json` is empty `[]`.
- Verify `python -c "import json; ..."` runs without syntax errors on both modified scripts.
- Note: Do NOT restart or close any running AletheiaLauncher process.
