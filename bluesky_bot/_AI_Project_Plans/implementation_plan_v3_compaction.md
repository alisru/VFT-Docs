# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 3 (Active): Workspace Root Consolidation

We are consolidating all Bluesky-bot related files from the workspace root directory into the dedicated `bluesky_bot` folder to ensure directory hygiene, resolve file clutter, and keep all components perfectly isolated.

### Proposed Changes

### Workspace Cleaning

#### [NEW] [cleanup_root_bskybot.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/cleanup_root_bskybot.py)
* Create a script to:
  * Identify all `*_graph.png` files and Bluesky bot evaluation outputs scattered in the root directory.
  * Safely move them to the `bluesky_bot/` directory (overwriting existing files to ensure the latest versions are kept).
  * Purge duplicate files from the root.

### Verification Plan
* Execute the cleanup script and verify in the terminal that the root directory is clean of Bluesky bot related `.png` or `.json` files.
* Confirm that the files now reside correctly under the `bluesky_bot` directory.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Reasoning: Cleansing workspace directories and keeping them perfectly organized reduces clutter and confusion for the user.

## Plan 2 (Active): True Directory Separation and Programmatic Indexing

We are resolving the folder pollution and dynamic indexing bugs in the Aletheia Bot system. Currently, live story files are scattered across root folders and the stories/ root folder, and `control_panel.html` fails to load live posts dynamically because it only indexes `stories/index.json` and fetches from the wrong paths.

This plan details how we will establish a strict separation between dry-runs (`stories/`) and live runs (`stories/live/`), clean all duplicate files, and update the programmatic folder loader to index both directories side-by-side.

### User Review Required

> [!IMPORTANT]
> - All live JSON files will be kept **strictly** in `stories/live/`. Any live JSON files found in `stories/` or the root `bluesky_bot/` folder will be deleted to eliminate duplicates.
> - Dry-run JSON files will be kept **strictly** in `stories/` root.
> - The programmatic loader in `control_panel.html` will be updated to fetch both `stories/index.json` (dry-runs) and `stories/live/index.json` (live stories) so they are rendered side-by-side.

### Proposed Changes

#### Clean-up & Re-Structuring

##### [MODIFY] [rebuild_registries.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/rebuild_registries.py)
* Update `rebuild_registries.py` to:
  * Delete `stories/index.json` and `stories/live/index.json` before rebuild to ensure a clean slate.
  * Re-build separate indices for `stories/` and `stories/live/` based on their actual location on disk.
  * Correctly call `save_and_sync_story` to sync them to the `stories_registry.js` bundle.

##### [NEW] [clean_stories_duplicates.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/clean_stories_duplicates.py)
* Create a dedicated cleaning script to:
  * Copy the 5 dry-run files from `_Generated_Content/stories/` to `bluesky_bot/stories/` (restoring them).
  * Delete any live JSON files (`factcheck_*.json`, `boots_amika_bundle.json`, `india_good_samaritan.json`, etc.) from the roots of `bluesky_bot/`, `_Generated_Content/`, `bluesky_bot/stories/`, and `_Generated_Content/stories/` where they do not belong.
  * Keep live files strictly inside `stories/live/`.

#### Frontend (HTML Viewer)

##### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/control_panel.html)
* Update the programmatic loader at line 1714:
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

We are remediating the catastrophic failure from the previous subagent run. The previous worker agents produced malformed and corrupted JSON structures containing mismatched coordinate keys (e.g. `stated_u`, `stated_coords`, etc. instead of `claim_u` and `claim_psi`), which broke the `control_panel.html` viewer.

To resolve this permanently and ensure this NEVER happens again, we are executing a strict three-phase recovery plan.

### 1. Clean-Up and Restoration (completed)
* **Delete Corrupted Files:** Identify and delete all 21 corrupted `factcheck_*.json` files inside `bluesky_bot/stories/`.
* **Clean Duplicates:** Traverse the workspace and delete root-level `factcheck_*.json` copies, and resolve any name clashes between live and dry-run subdirectories.
* **Registry Reset:** Re-run `scratch/rebuild_registries.py` to compile `stories_registry.js` from ONLY 100% valid files.

### 2. High-Fidelity Offline Regeneration (completed)
Instead of relying on subagents with ad-hoc prompts that hallucinate schemas, we are doing the evaluation programmatically using our own native model capabilities to guarantee 100% schema alignment:
* **Strict Schema Enforcement:** Use the exact keys required by `aletheia_bot.py` and `orchestrator.py` (`claim_u`, `claim_psi`, `real_u`, `real_psi`, `posts` containing exactly 14 elements).
* **Automatic Geodesic Plotting:** Generate corresponding trajectory vector graphs (`[subject_slug]_graph.png`) using the local `matplotlib` script and sync them to `bluesky_bot/` and `_Generated_Content/`.
* **Registry Integration:** Sequentially sync all 16 regenerated files into indices and JS registries to restore the portfolio.

### 3. Verification & Safety Safeguards
* **Validation Script:** Run `scratch/inspect_factchecks.py` to ensure that the file counts and structures are completely healthy.
* **Model Selection Lockdown:** Explicitly acknowledge the shift from Pro (Low) to Flash (Medium) to ensure fast, robust execution.

### Morality and Will Audit
* Calculated Coordinate: `(υ=+2.0, ψ=+2.0)` -> Systemic Justice & Productive Value Creation.
* Reasoning: Resolving structural bugs, recovering the integrity of the user's workspace, and restoring public visibility metrics without wasting paid resources.
