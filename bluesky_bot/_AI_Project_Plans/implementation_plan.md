# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 12 (Active): Enhanced Trajectory Graphs and Change-Tracking Push Flag Script

### Goal Description
Modify the Matplotlib trajectory graphs to display a highly precise, labeled two-axis coordinate system. Update the evaluative instructions to formalize these scales. Provide a local git change-tracking and verification script to automate the flow of verifying and staging stories prior to pushing.

### User Review Required
> [!NOTE]
> All 90 story graph images will be programmatically regenerated to reflect the new axis scales, and the stories registry will be rebuilt.

### Proposed Changes

#### [MODIFY] [generate_graph.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/generate_graph.py)
* Add explicit tick labels on the X-axis for Morality (υ):
  - `+2.0` -> "Everyone\n(+2.0)"
  - `+1.0` -> "Others\n(+1.0)"
  - `+0.5` -> "Other\n(+0.5)"
  - `0.0`   -> "No One\n(0.0)"
  - `-1.0`  -> "My Group\n(-1.0)"
  - `-1.5`  -> "Me\n(-1.5)"
  - `-2.0`  -> "Only Me\n(-2.0)"
* Add explicit tick labels on the Y-axis for Will (ψ):
  - `+2.0` -> "Active-Active (+2.0)"
  - `+1.0` -> "Passive-Active (+1.0)"
  - `0.0`   -> "Neutral (0.0)"
  - `-1.0`  -> "Passive-Passive (-1.0)"
  - `-2.0`  -> "Active-Passive (-2.0)"
* Remove hardcoded text labels `Good Preference` and `Bad Preference` from the middle of the plot area to prevent overlap/clutter.

#### [MODIFY] [Convergence-test-v2.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/Convergence-test-v2.md)
* Update Section "Phase 2 — Vector Verification" to document the continuous (υ, ψ) morality-will coordinate system ticks and their precise semantic definitions.

#### [NEW] [track_changes.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/track_changes.py)
* Create a change-tracking Python script that:
  - Validates all JSON configs under `stories/` and `stories/live/` for schema completeness, status flags, character lengths (<250 per post), and matching graph images.
  - Compiles a summary of modified and ready-to-push files via Git status.
  - Warns if there are any validation failures.
  - Offers to run `rebuild_registries.py` and stage files (`git add`) to prepare them for a push.

#### [MODIFY] [running_dialogue.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/running_dialogue.md)
* Document Intent 25 in the intentions log tracking this trajectory scale and change tracking script implementation.

### Verification Plan
* Run `generate_graph.py` to generate a test graph and inspect it visually.
* Run batch regeneration script to update all 90 story graph images.
* Run the new change-tracking script to confirm all stories validate successfully and are marked ready to stage.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Precise visualization of the (υ, ψ) coordinates makes the AI's moral judgments fully transparent, and automated change-tracking prevents regression errors.

---

## Plan 11 (Active): Scripts & Utilities Index in Master Instructions

To reduce token usage and prevent agents from loading large python script files just to understand pipeline flow, we are adding a "Scripts & Utilities Directory" to the Master Index ([bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)). This section will provide a high-level summary of the files in `bluesky_bot/` and `scratch/` that handle harvesting, evaluation, registries, and posting.

### User Review Required
> [!NOTE]
> This change is documentation-only, adding metadata to the master index to prevent context-bloat for subsequent AI turns. No operational scripts are altered.

### Proposed Changes

### [Documentation Component]

#### [MODIFY] [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)
* Prepend or append a new section: `## 4. Scripts & Utilities Directory` outlining:
  * `scratch/harvest_candidates_script.py` (candidate retrieval & de-duplication)
  * `bluesky_bot/orchestrate_batch.py` (Gemini API pipeline wrapper — legacy/locked)
  * `bluesky_bot/aletheia_bot.py` (the core posting CLI engine)
  * `scratch/rebuild_registries.py` (registry compiler & visual control panel indexer)
  * `bluesky_bot/generate_graph.py` (the Matplotlib trajectory graph plotter)

#### [MODIFY] [running_dialogue.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/running_dialogue.md)
* Document Intent 24 in the intentions log tracking this token optimization update.

### Verification Plan
* Verify that all links in the modified [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md) resolve correctly.
* Run git diff to confirm only clean, expected markdown modifications have occurred.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Providing a script registry in the instructions prevents incoming agents from having to open the code files, drastically reducing token consumption and processing time.

---

## Plan 10 (Completed): Aligning /bsky-reply-batch Workflow with OOP Instructions

We updated the system workflow `/bsky-reply-batch` ([bsky-reply-batch.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/workflows/bsky-reply-batch.md)) to align with the new OOP-style modular bot instructions directory. This ensures that any agent executing this workflow is explicitly directed to the Master Index ([bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)) and its modular components, preventing model drift or incorrect JSON schema generations.
