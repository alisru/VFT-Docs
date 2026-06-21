# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 17 (Active): Intelligent Actor Extraction via LLM

### Goal Description
The current deterministic script (`actor_extract.py`) uses naive Title Case regex and hardcoded wordlists, which leads to garbage extractions like "Trump Torched" or "Trump Administration", missing the actual actor entirely. The goal is to identify actors (individuals and groups) accurately "during the processing" without relying on pre-loaded identity lists.

### User Review Required
> [!IMPORTANT]  
> Please review the proposed approach and answer the open question regarding the historical backfill.

### Proposed Changes

#### 1. Pipeline Upgrade (Future Stories)
**[MODIFY]** [google_ai_studio_one_shot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
* Update the prompt and output JSON schema sent to the Gemini API. 
* We will instruct the LLM to natively identify the core `actors` (individuals and organizations) while it processes the story and generates the posts. 
* Since the LLM already deeply understands the text, it will perfectly extract "Donald Trump" instead of "Trump Torched". This requires zero additional API calls because it rides on the existing harvest generation call.

#### 2. Deprecate the Deterministic Script
**[DELETE]** [actor_extract.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/actor_extract.py)
* The script is obsolete once the LLM handles extraction natively.

### Open Questions
> [!CAUTION]  
> **Explicit Permission Required for Historical Data**  
> We have ~1,565 historical stories that I just backfilled using the bad deterministic script. They are currently tagged with garbage actors.
> Because your global rule states: *"NEVER run scripts with api calls to AI studio unless I explicitly say to do so"*, I cannot fix these files without your consent. 
> 
> **Do I have your explicit permission to write and run a one-time backfill script that uses the Gemini API to scan the historical JSONs and fix their `actors` tags?**

---

## Plan 16 (Active): Unlimited Hypocrisy Leaderboards Scroll Lists

### Goal Description
Modify the hypocrisy leaderboards (for both Actors and Outlets) to remove the threshold filtering (`minN = 2` stories) and max row limits (`maxRows = 60` rows). Render them inside scroll containers with sticky headers so that the user can browse every tracked actor/outlet.

### User Review Required
> [!NOTE]
> Leaderboards will now list one-off entries (n=1) and will have scroll bars inside their respective panel frames.

### Proposed Changes

#### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/control_panel.html)
* Updated `_hypocrisyTable` to remove the story count threshold (`minN`) filter and display all rows.
* Wrapped the grid table in a `.scroll-container` style div block with `max-height: 400px; overflow-y: auto`.
* Styled table column headers as `position: sticky; top: 0; background: var(--panel-bg); z-index: 2` to keep them visible while scrolling.
* Cleaned up footer limits summary text blocks.

### Verification Plan
* Open the control panel, go to the Trends/Audit tab, and confirm that both the Actor and Outlet leaderboards show a scrollbar and list all actors/outlets (including single-story entries) with sticky headers.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Complete and unrestricted view of the entities database improves auditing efficiency.

---


## Plan 15 (Active): Calibration Drift Graph Axis Correction

### Goal Description
Correct the axis mapping inside the `auditCalibration(stories)` function on the trends dashboard. The original implementation plotted Stated Judgement vs Reality using Will ($\psi$) on the horizontal axis and Morality ($u$) on the vertical axis. This has been flipped to align with standard convention (Morality $u$ horizontal, Will $\psi$ vertical).

### User Review Required
> [!NOTE]
> This is a client-side layout correction for SVG coordinate plotting. No file structures or backend databases are affected.

### Proposed Changes

#### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/control_panel.html)
* Swapped variables in `auditCalibration` so `x1` and `x2` calculate based on morality values (`s.claim_u`, `s.real_u`), and `y1`/`y2` calculate based on will values (`s.claim_psi`, `s.real_psi`).
* Corrected vertical labels to read `+ψ` and `−ψ`, and horizontal label to read `u →`.

### Verification Plan
* Open the control panel, navigate to the Trends/Audit tab, scroll to the **Calibration Drift** graph, and confirm that the X axis represents morality ($u$) and the Y axis represents will ($\psi$).

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.0)` -> Greater Good & Productive Action.
* Verdict: Ensures that the user dashboard graphs show correct, standard coordinates, avoiding any user confusion.

---


## Plan 14 (Active): Enhanced Interactive Controls for Trend Over Time Graph

### Goal Description
Improve the control panel's "Trend Over Time" graph by adding standard interactive controls. These include interval settings (Daily, Weekly, Monthly), metric toggle options to show/hide lines (`reality_u`, `Δu`), and an interactive SVG hover vertical guide line and tooltip tracker.

### User Review Required
> [!NOTE]
> This updates the client-side JavaScript rendering of the trends graph. No database files or server scripts are altered.

### Proposed Changes

#### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/control_panel.html)
* Define global state variables `_trendInterval = 'week'`, `_showRealityU = true`, `_showDeltaU = true`.
* Add `setTrendInterval(interval)` and `toggleTrendLine(line, visible)` functions to handle interactions.
* Implement `handleTrendHover(evt, svg)` and `handleTrendLeave(svg)` to draw the guide line, render the indicators, and position a dynamic HTML tooltip element.
* Update `auditTimeSeries(stories)` to support interval calculations (Daily, Weekly, Monthly), generate dynamic legend control checkboxes and interval pill buttons, and render interactive hooks inside the SVG element.

### Verification Plan
* Open the control panel, navigate to the Trends tab, and confirm that:
  - Toggling intervals (Daily, Weekly, Monthly) rebuilds the trend bins correctly.
  - Checkboxes for `reality_u` and `Δu` immediately toggle line and dot visibility.
  - Hovering the mouse over the chart displays a vertical guide line and a rich tooltip with bin date ranges, story count, and averages.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Interactive telemetry makes temporal analysis significantly more readable and accessible for operators.

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
