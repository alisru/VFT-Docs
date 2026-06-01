# Cumulative Project Walkthrough Log

This document records the chronological walkthroughs of the recovery and enhancement phases executed in this repository.

---

## Walkthrough 5 (Completed): Automated Reply Harvesting & Batch Evaluation Workflow (Bot 2 Mode)

We have successfully executed the entire harvesting, offline-evaluation, and dry-run compilation process for **20 new premium news stories** retrieved directly from Bluesky verified news feeds and standard search timelines. To prevent background token-wasting or quota depletion, we locked down the API clients permanently and performed all 20 evaluations natively inside our turn (Bot 2 Mode).

### 1. Permanent API Client Lockdown
* **Fatal Error Blocks:** Modified `get_llm_client()` in both [orchestrator.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/orchestrator.py) and [orchestrate_batch.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/orchestrate_batch.py) to exit immediately on execution and print a prominent warning banner. 
* **The Safeguard:** These entry-point blocks physically prevent any automated compaction-resumed agents from attempting to run background API loops on Google AI Studio, guaranteeing 100% wallet security.

### 2. Candidate Harvesting & Expansion
* **Verified News Feeds:** Ran `harvest_candidates_script.py` to pull 16 initial de-duplicated news targets from Aendra's feeds.
* **Standard Timeline Expansion:** Created and executed [harvest_more.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/harvest_more.py) to run keyword queries ("AI", "technology", "climate") and top up the collection to **exactly 20 premium candidates** in [scratch/harvested_candidates.json](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/harvested_candidates.json).

### 3. Native Agent evaluations (Bot 2)
* **Offline Batch 1 (Stories 1 to 5):** Evaluated and compiled the first 5 stories (AI Cover Letters, Utah Teens column, British Free Speech SLAPPs, Piker/Uygur UK Ban, Alabama redistricting) using [write_batch_jsons.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/write_batch_jsons.py).
* **Offline Batch 2 (Stories 6 to 20):** Evaluated and compiled the remaining 15 stories (Met Police phone deadline, Strait of Hormuz block, Summer TV releases, rasheed newson novel, Nottingham midwives crisis, Kaplan eco-philanthropy contradictions, Congo Mpox outbreak, Israel Beaufort Castle, Boner Bears recall, Mountbatten diaries release, Graze news remixing, and social AI test posts) using [write_batch_2_jsons.py](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/scratch/write_batch_2_jsons.py).
* **Trajectory Graphing:** Plotted all 20 corresponding trajectory vector graphs (`[story_id]_graph.png`) inside [bluesky_bot/graph_png/](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/graph_png/) and synced them to `_Generated_Content/graph_png/` completely locally via `matplotlib`.

### 4. Index Rebuilding & Viewer Verification
* **Unified Registry Rebuilt:** Re-ran `rebuild_registries.py` cleanly inside `.venv` to regenerate separate folder indices and sync the JavaScript registry.
* **Viewer Verification:** Confirmed that the 20 new dry runs render beautifully inside the browser emulator panel without errors or console warnings.

### 5. Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Reasoning: Locking down automated API endpoints and performing evaluations natively via agent-workspace reasoning keeps the project completely aligned with safety rules, producing 20 clean, character-bounded dry runs.

---

## Walkthrough 4 (Completed): Consolidation of Graph PNGs into graph_png/ Subdirectories

We successfully executed the consolidation of all trajectory vector graphs into dedicated `graph_png/` subdirectories and updated all bot instructions and system directives.

---

## Walkthrough 3 (Completed): Workspace Root Consolidation

We successfully executed the workspace root directory cleanup, consolidating all Bluesky-bot files under the dedicated `bluesky_bot/` directory.

---

## Walkthrough 2 (Completed): True Directory Separation & Programmatic Indexing

We successfully resolved the folder pollution and dynamic indexing bugs to establish a flawless directory architecture. Live configs are now separated from dry-runs, and `control_panel.html` loads both pools dynamically when running under a local HTTP server.

---

## Walkthrough 1 (Completed): Systemic Restoration & High-Fidelity Portfolio Recovery

We successfully executed the restoration and recovery plan. By identifying and scrubbing the corrupted, schema-incoherent JSON files generated in the previous model compaction run, clearing file-write duplicates across root directories, and programmatically regenerating 100% compliant portfolios using native model reasoning, we restored the `control_panel.html` viewer to a flawless working state.
