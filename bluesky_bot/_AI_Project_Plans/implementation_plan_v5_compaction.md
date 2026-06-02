# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 5 (Active): Automated Reply Harvesting & Batch Evaluation Workflow

We are implementing the automated reply mode harvesting process to identify exactly 20+ fresh news posts from Bluesky feeds and standard search queries, perform programmatic convergence evaluations offline, compile character-bounded dry-run configs, generate trajectory graphs, and register them cleanly inside the HTML Portfolio control panel. We will also introduce the `/bsky-reply-batch` system workflow to standardise this pipeline.

### User Review Required

> [!IMPORTANT]
> - This execution processes exactly 20 diverse, high-quality, de-duplicated news posts retrieved from Bluesky.
> - Dry runs will be compiled programmatically, ensuring 100% schema alignment with zero rate limit or context exhaustion risks.
> - The new slash command `/bsky-reply-batch` is officially registered under `.agent/workflows/` so it is permanently available.

### Proposed Changes

### Candidate Harvesting
* Modify `scratch/harvest_candidates_script.py` to increase harvest limits to ensure robust candidates count.
* Create a dedicated top-up script `scratch/harvest_more.py` to query standard search queries ("AI", "technology", "climate", etc.) to fill slots and reach exactly 20 distinct premium candidates.

### Programmatic Offline Evaluations
* Execute `orchestrate_batch.py` to sequentially evaluate the 20 candidates, utilizing stable pacing and cooldowns to bypass Gemini API limits.
* Compile and save separate JSON factchecks under `stories/` in the COMPLETED DRY RUN status.
* Draw corresponding matplotlib trajectory graphs inside `graph_png/` subfolders.

### System Workflow Registration
* **[NEW] [bsky-reply-batch.md](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/.agent/workflows/bsky-reply-batch.md):** Define and document the `/bsky-reply-batch` workflow command.

### Verification Plan
* Recompile indices using `rebuild_registries.py`.
* Load `control_panel.html` locally and verify that all 20 new dry runs render flawlessly with their trajectory graphs.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Standardizing the harvesting and evaluation flow into a repeatable system workflow reduces developer friction and guarantees high-fidelity, schema-aligned thread generation.

---

## Plan 4 (Completed): Consolidation of Graph PNGs into graph_png/ Subdirectories

We consolidated all Bluesky trajectory vector graph `.png` files into dedicated `graph_png/` subfolders inside both `bluesky_bot/` and `_Generated_Content/`. We also updated all system directives to save newly generated graphs directly inside these subfolders and updated the HTML viewer to automatically handle the prepended paths.

### Proposed Changes

### File Consolidation & Relocation
* Relocated all loose graph images under `bluesky_bot/` and `_Generated_Content/` to their respective `graph_png/` subfolders.
* Purged loose duplicate files from the root folders.

### System Directives Patches

#### [MODIFY] [aletheia_bot.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/aletheia_bot.py)
* Dynamically resolved `graph_png/` folder path.
* Saved generated graphs inside the subfolder.
* Synchronized copies to `_Generated_Content/graph_png/`.
* Prefixed registry `graph_img` elements with `graph_png/` when compiling the stories registry.

#### [MODIFY] [orchestrate_batch.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/orchestrate_batch.py)
* Programmatically pointed batch graph generation to `graph_png/` directory.
* Ensured copies are synced to `_Generated_Content/graph_png/`.

#### [MODIFY] [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)
* Documented `graph_png/` subdirectory usage.

### Frontend Viewer Patches

#### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/control_panel.html)
* Automatically checks and prepends `graph_png/` to graph image keys when missing.

### Verification Plan
* Verified registry compilation by running `rebuild_registries.py` and checking `stories_registry.js`.
* Started a local Python HTTP server and verified that all graphs render flawlessly on the control panel dashboard without console warnings.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Reasoning: Cleansing directories, structuring graph assets, and making system directives self-documenting minimizes friction and prevents layout regressions.

---

## Plan 3 (Completed): Workspace Root Consolidation

We consolidated all Bluesky-bot related files from the workspace root directory into the dedicated `bluesky_bot` folder to ensure directory hygiene, resolve file clutter, and keep all components perfectly isolated.

---

## Plan 2 (Completed): True Directory Separation and Programmatic Indexing

We resolved the folder pollution and dynamic indexing bugs in the Aletheia Bot system. Currently, live story files are scattered across root folders and the stories/ root folder, and `control_panel.html` fails to load live posts dynamically because it only indexes `stories/index.json` and fetches from the wrong paths.

---

## Plan 1 (Completed): Restoring HTML Viewer & High-Fidelity Candidate Regeneration

We remediated the catastrophic failure from the previous subagent run. The previous worker agents produced malformed and corrupted JSON structures containing mismatched coordinate keys, which broke the `control_panel.html` viewer.
