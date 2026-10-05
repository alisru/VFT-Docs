# Walkthrough - Queue Deduplication & Pruning Fix

## Summary
Resolved the issue where 1 candidate story (*Australia Considers Smart Glasses Ban...*) remained permanently stuck in the harvested candidates queue (`📥 Queue: 1`).

## Changes Made
1. **`bluesky_bot/harvested_candidates.json`**:
   - Cleared the zombie candidate back to `[]` (the story had already been evaluated and is active in `stories/live/`).
2. **`bluesky_bot/google_ai_studio_one_shot.py`**:
   - Replaced single-field URL matching with symmetric multi-field matching (`link`, `target_url`, `grounding_url`, `url`).
   - Evaluated candidates and pending queue items are now matched across any available URL alias, ensuring bridged/ActivityPub feeds, Bluesky posts, and scraped article URLs properly trigger deduction from `harvested_candidates.json`.
3. **`bluesky_bot/harvest_candidates.py`**:
   - Updated the historical and live evaluation directory scanner to collect all available URL keys (`link`, `target_url`, `grounding_url`) into `seen_evaluated_urls` instead of short-circuiting on `link`.
   - Updated pending queue loading logic to check both `c["url"]` and `c["target_url"]` against `seen_evaluated_urls`.

## Verification Results
- `harvested_candidates.json` verified as `[]`.
- `py_compile` verified syntax on both modified Python scripts without errors.
- Running launcher was left untouched and its HUD will display `📥 Queue: 0` on its next tick.
