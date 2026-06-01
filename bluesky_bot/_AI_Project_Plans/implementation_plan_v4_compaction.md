# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 4 (Active): Consolidation of Graph PNGs into graph_png/ Subdirectories

We are consolidating all Bluesky trajectory vector graph `.png` files into dedicated `graph_png/` subfolders inside both `bluesky_bot/` and `_Generated_Content/`. We will also update all system directives to save newly generated graphs directly inside these subfolders and update the HTML viewer to automatically handle the prepended paths.

### User Review Required

> [!IMPORTANT]
> - All trajectory vector graphs must reside in `graph_png/` subdirectories. No loose `.png` files should reside in `bluesky_bot/` or `_Generated_Content/`.
> - All bot directives (`aletheia_bot.py`, `orchestrate_batch.py`, `bluesky_bot_instructions.md`) must be programmatically updated to target `graph_png/` folders automatically.
> - The HTML Viewer (`control_panel.html`) in both places must auto-prepend `graph_png/` to graph image keys when missing to ensure backward compatibility with older configurations.

### Proposed Changes

#### File Consolidation & Relocation
* Relocate all loose graph images under `bluesky_bot/` and `_Generated_Content/` to their respective `graph_png/` subfolders.
* Clean loose files to ensure zero duplicate clutter.

#### System Directives Patches

##### [MODIFY] [aletheia_bot.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/aletheia_bot.py)
* Dynamically resolve `graph_png/` folder path.
* Save generated graphs inside the subfolder.
* Synchronize copies to `_Generated_Content/graph_png/`.
* Prefix registry `graph_img` elements with `graph_png/` when compiling the stories registry.

##### [MODIFY] [orchestrate_batch.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/orchestrate_batch.py)
* Programmatically point batch graph generation to `graph_png/` directory.
* Ensure copies are synced to `_Generated_Content/graph_png/`.

##### [MODIFY] [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)
* Document `graph_png/` subdirectory usage for future developers/subagents.

#### Frontend Viewer Patches

##### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/control_panel.html)
* Automatically check if `graph_img` contains `graph_png/` prefix.
* If not, prepend `graph_png/` programmatically to prevent broken link indicators.

### Verification Plan
* Validate registry compilation by running `rebuild_registries.py` and checking `stories_registry.js`.
* Start a local Python HTTP server and verify that all graphs render flawlessly on the control panel dashboard without console warnings.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Reasoning: Cleansing directories, structuring graph assets, and making system directives self-documenting minimizes friction and prevents layout regressions.

---

## Plan 3 (Completed): Workspace Root Consolidation

We consolidated all Bluesky-bot related files from the workspace root directory into the dedicated `bluesky_bot` folder to ensure directory hygiene, resolve file clutter, and keep all components perfectly isolated.

### Proposed Changes

### Workspace Cleaning

#### [NEW] [cleanup_root_bskybot.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/cleanup_root_bskybot.py)
* Identify all `*_graph.png` files and Bluesky bot evaluation outputs scattered in the root directory.
* Safely move them to the `bluesky_bot/` directory.
* Purge duplicate files from the root.

### Verification Plan
* Execute the cleanup script and verify in the terminal that the root directory is clean of Bluesky bot related `.png` or `.json` files.
* Confirm that the files now reside correctly under the `bluesky_bot` directory.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Reasoning: Cleansing workspace directories and keeping them perfectly organized reduces clutter and confusion for the user.

---

## Plan 2 (Completed): True Directory Separation and Programmatic Indexing

We resolved the folder pollution and dynamic indexing bugs in the Aletheia Bot system. Currently, live story files are scattered across root folders and the stories/ root folder, and `control_panel.html` fails to load live posts dynamically because it only indexes `stories/index.json` and fetches from the wrong paths.

This plan details how we established a strict separation between dry-runs (`stories/`) and live runs (`stories/live/`), cleaned all duplicate files, and updated the programmatic folder loader to index both directories side-by-side.

### Proposed Changes

#### Clean-up & Re-Structuring

##### [MODIFY] [rebuild_registries.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/rebuild_registries.py)
* Update `rebuild_registries.py` to delete `index.json` and `live/index.json` before rebuild to ensure a clean slate.
* Re-build separate indices for `stories/` and `stories/live/` based on their actual location on disk.
* Correctly call `save_and_sync_story` to sync them to the `stories_registry.js` bundle.

##### [NEW] [clean_stories_duplicates.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/clean_stories_duplicates.py)
* Copy the 5 dry-run files from `_Generated_Content/stories/` to `bluesky_bot/stories/` (restoring them).
* Delete any live JSON files (`factcheck_*.json`, `boots_amika_bundle.json`, `india_good_samaritan.json`, etc.) from the roots of `bluesky_bot/`, `_Generated_Content/`, `bluesky_bot/stories/`, and `_Generated_Content/stories/` where they do not belong.
* Keep live files strictly inside `stories/live/`.

#### Frontend (HTML Viewer)

##### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/control_panel.html)
* Update the programmatic loader:
  * Fetch `stories/index.json` (dry-runs) and load files from `stories/[filename]`.
  * Fetch `stories/live/index.json` (live posts) and load files from `stories/live/[filename]`.
  * Merge both arrays and sort them dynamically (newest first).
  * Set status correctly (dry-runs as "COMPLETED DRY RUN", live runs as "LIVE POSTED").

### Verification Plan
* Run `clean_stories_duplicates.py` to purge all duplicates and restore dry-runs.
* Run `rebuild_registries.py` to generate clean `index.json` files and `stories_registry.js`.
* Run a local HTTP server: `python -m http.server` and verify in the browser that both folders load seamlessly.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+2.0, ψ=+2.0)` -> Systemic Justice & Productive Value.
* Reasoning: Organizing workspace directories, preventing resource duplication, and fixing programmatic APIs benefit all users and systems involved.

---

## Plan 1 (Completed): Restoring HTML Viewer & High-Fidelity Candidate Regeneration

We remediated the catastrophic failure from the previous subagent run. The previous worker agents produced malformed and corrupted JSON structures containing mismatched coordinate keys (e.g. `stated_u`, `stated_coords`, etc. instead of `claim_u` and `claim_psi`), which broke the `control_panel.html` viewer.

To resolve this permanently and ensure this NEVER happens again, we executed a strict three-phase recovery plan.

### 1. Clean-Up and Restoration (completed)
* **Delete Corrupted Files:** Identify and delete all 21 corrupted `factcheck_*.json` files inside `bluesky_bot/stories/`.
* **Clean Duplicates:** Traverse the workspace and delete root-level `factcheck_*.json` copies, and resolve any name clashes between live and dry-run subdirectories.
* **Registry Reset:** Re-run `scratch/rebuild_registries.py` to compile `stories_registry.js` from ONLY 100% valid files.

### 2. High-Fidelity Offline Regeneration (completed)
Instead of relying on subagents with ad-hoc prompts that hallucinate schemas, we did the evaluation programmatically using our own native model capabilities to guarantee 100% schema alignment:
* **Strict Schema Enforcement:** Use the exact keys required by `aletheia_bot.py` and `orchestrator.py` (`claim_u`, `claim_psi`, `real_u`, `real_psi`, `posts` containing exactly 14 elements).
* **Automatic Geodesic Plotting:** Generate corresponding trajectory vector graphs (`[subject_slug]_graph.png`) using the local `matplotlib` script and sync them to `bluesky_bot/` and `_Generated_Content/`.
* **Registry Integration:** Sequentially sync all 16 regenerated files into indices and JS registries to restore the portfolio.

### 3. Verification & Safety Safeguards
* **Validation Script:** Run `scratch/inspect_factchecks.py` to ensure that the file counts and structures are completely healthy.
* **Model Selection Lockdown:** Explicitly acknowledge the shift from Pro (Low) to Flash (Medium) to ensure fast, robust execution.

### Morality and Will Audit
* Calculated Coordinate: `(υ=+2.0, ψ=+2.0)` -> Systemic Justice & Productive Value Creation.
* Reasoning: Resolving structural bugs, recovering the integrity of the user's workspace, and restoring public visibility metrics without wasting paid resources.
