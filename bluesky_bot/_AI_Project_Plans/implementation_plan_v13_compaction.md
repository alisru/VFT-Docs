# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 13 (Active): Actor Leaderboard Dropdowns and Automatic Registry Actor Tagging

### Goal Description
Improve the control panel's actor hypocrisy leaderboard by enabling dropdown lists on actor names that display their related stories. Ensure that all stories (in both `stories/` and `stories/live/`) are processed for actors, automatically extracting actors using the deterministic `actor_extract.py` utility for files missing them during `rebuild_registries.py` compilation.

### User Review Required
> [!NOTE]
> Running `rebuild_registries.py` will automatically backfill `actors` tags for approximately 1,240 stories currently missing them and write those tags back to their respective JSON files.

### Proposed Changes

#### [MODIFY] [rebuild_registries.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/rebuild_registries.py)
* Import `extract_actors` from `actor_extract`.
* During story scanning, check if `actors` is in `cfg` or is empty.
* If missing/empty, call `extract_actors(cfg.get("subject", ""))`.
* Persist the newly extracted `actors` list back to the source JSON file on disk.
* Compile these actors into `stories_registry.js`.

#### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/control_panel.html)
* Add a `toggleActorDropdown(actorId)` helper function in the scripts section.
* Update `auditActorLeaderboard(stories)` to wrap the actor's name in a clickable element with a toggle arrow.
* Render a hidden dropdown row using `grid-column: span 4` for each actor containing a sub-list of their associated stories.
* Ensure clicking on these sub-list stories selects them in the emulator.

### Verification Plan
* Run `rebuild_registries.py` and verify it automatically identifies stories missing actors, extracts them, and writes them back to disk.
* Check git diff to ensure JSON files were modified with expected `actors` lists.
* Open `control_panel.html` in the browser, check the Actor Hypocrisy Leaderboard, and verify that clicking actor names expands dropdown lists of related stories.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Automating actor extraction fixes incomplete metrics for 1200+ stories, and the hierarchical leaderboard dropdowns make structural data navigation significantly faster and cleaner.

---
