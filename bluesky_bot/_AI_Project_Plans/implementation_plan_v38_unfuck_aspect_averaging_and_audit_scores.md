# Implementation Plan v38: Unfuck Aspect Averaging and Restore Audit Integrity

**Date:** 2026-11-09  
**Objective:** Eliminate naive arithmetic averaging of multi-aspect vectors, stop registry mutations that clobber post text with averaged coordinates, introduce origin deadband to prevent neutral stories from auto-failing to "Greater Evil", and identify draft stories needing correction.

## Root Cause Summary
1. `google_ai_studio_one_shot.py` and `rebuild_registries_son.py` overwrote top-level `(claim_u, claim_psi)` and `(real_u, real_psi)` with `sum(aspects) / len(aspects)`.
2. When aspects had opposing signs (e.g. failing government at -0.85 and democratic voters at +0.70), averaging washed them out to -0.08, erasing the actual signal.
3. `get_zone_label()` had no origin deadband, defaulting any negative coordinate (even -0.01) to "Greater Evil".
4. `rebuild_registries_son.py` actively mutated `posts[1]` and `posts[2]` on disk, clobbering post prose with the averaged coordinates and "Greater Evil" text label.

## Changes Required
1. `bluesky_bot/google_ai_studio_one_shot.py`:
   - Remove `if story.get("aspects") ...:` coordinate averaging block in both dict and list parsing branches.
   - Preserve top-level coordinates evaluated by the model or calculated via SON attractor forces.
2. `bluesky_bot/rebuild_registries_son.py`:
   - Remove `if "aspects" in cfg ...:` coordinate averaging and post text rewriting block from `process_and_update_coordinates()`.
   - Update `get_zone_label(u, psi)` to include a deadband around origin ($|u| \le 0.15, |\psi| \le 0.15 \to$ "Neutral / Stasis").
3. `bluesky_bot/delete_quarantined_bluesky_posts.py` & `bluesky_bot/restore_corrupted_to_drafts.py`:
   - Remove the copy-pasted aspect averaging logic.
4. Story inspection:
   - Identify all draft stories currently in `stories/drafts/` or `stories/darkroom/` to check which ones were corrupted by aspect averaging.
   - Fix `stories/live/factcheck_anc-election-defeat-2026.json`.
