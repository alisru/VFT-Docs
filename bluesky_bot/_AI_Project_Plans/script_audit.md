# Aletheia Bot Python Script Audit & Systemic Archeology

This document compiles a comprehensive audit of all Python (`.py`) scripts present in the `bluesky_bot/` and `scratch/` directories. It analyzes their original intent, categorizes them under the two active bot projects, and marks redundant files for archiving to secure clean workspaces.

---

## 1. Core Bot Architecture (To Keep Active)

These files constitute the structural backbone of the two projects. **Do NOT archive or touch these files.**

### Bot 1: The Deployment/API Bot
* **[orchestrator.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/orchestrator.py)**
  * **Purpose:** Single-shot API-driven entry point. Performs a 3-Phase Convergence Test on a target URL using direct Gemini Generative AI SDK calls, builds the 14-post thread configuration, draws the trajectory graph, and posts it live.
  * **Deployment status:** Production.
* **[orchestrate_batch.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/orchestrate_batch.py)**
  * **Purpose:** Parallel, high-throughput API batch orchestrator. Spawns stateless worker threads to evaluate stories concurrently when running in automated deployment mode.
  * **Deployment status:** Production.

### Bot 2: The Agent-Interactive/Local Bot
* **[orchestrate_batch_local.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/orchestrate_batch_local.py)**
  * **Purpose:** Serves as the template instruction manual. Safe from background token consumption; prints stories and directs the AI agent (us) to perform local evaluations.
  * **Deployment status:** Active workspace tool.
* **[post_batch.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/post_batch.py)**
  * **Purpose:** The user-facing publishing script. Takes pre-compiled local dry-run JSONs in the `stories/` folder and publishes them sequentially as live threads on Bluesky, writing back the server-returned `rkeys` and `post_urls`.
  * **Deployment status:** Active workspace tool.

### Shared Utility Foundations
* **[aletheia_bot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aletheia_bot.py)**
  * **Purpose:** Core engine of the bot. Handles Bluesky login authentication via `atproto`, provides dynamic text-splitting (`split_text()`) under the 300-char post limit, processes thread postings, and handles `save_and_sync_story()` database serializations.
* **[generate_graph.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/generate_graph.py)**
  * **Purpose:** Matplotlib trajectory plotter. Takes claim and reality coordinates, calculates the geodesic moral path, draws inverted X-axis grids, watermarks, and legends, and outputs the image as `[story_id]_graph.png`.

---

## 2. Workspace Utility Tools (To Keep Active)

These are active helper scripts in `scratch/` or `bluesky_bot/` used for index maintenance, searching, or manual validation testing.

* **[scratch/rebuild_registries.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/rebuild_registries.py)**
  * **Purpose:** Database compiler. Completely purges the compiled registries (`stories_registry.js`) and builds them fresh by recursively scanning all valid `factcheck_*.json` files.
* **[bluesky_bot/search_bsky.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/search_bsky.py)**
  * **Purpose:** Query search test. Connects to feed endpoints to verify search term matching on the feed level.
* **[bluesky_bot/post_live.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/post_live.py)** & **[bluesky_bot/post_dry_run.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/post_dry_run.py)**
  * **Purpose:** Standalone test runners for single-post experiments.

---

## 3. Audited Redundant Scripts (Marked for Archive)

These files are typical "compaction residue." Previous models generated them as single-use scratch files to work around rate limits or try to hack together batch outputs. They are now redundant and cluttering the workspace. We will move them to `bluesky_bot/_Archive/`.

### Subagent Spawners & Parallel Worker Scripts
* **`worker1_batch1_eval.py`**, **`worker3_eval.py`**, **`worker4_eval.py`**, **`worker4_eval_batch4.py`**
  * **Why generated:** Previous models spawned these scripts to run offline calculations inside separate subagent contexts concurrently.
  * **Why redundant:** Replaced by the agent's native high-fidelity evaluations.
* **`process_batch.py`**, **`process_batch_2.py`**, **`process_batch3.py`**, **`save_batch3_configs.py`**
  * **Why generated:** Used by worker subagents to try and merge/sync results of parallel batches.
  * **Why redundant:** Replaced by standard sequential imports and the `rebuild_registries.py` protocol.

### Temporary File & Graph Generators
* **`generate_jsons.py`**, **`generate_batch2_files.py`**
  * **Why generated:** Hacks written to programmatically mass-produce JSON files for specific batches.
  * **Why redundant:** Standardized evaluations must happen via the unified local bot protocol.
* **`generate_batch2_graphs.py`**, **`generate_batch4_graphs.py`**, **`generate_graphs.py`**, **`generate_graphs_for_batch.py`**
  * **Why generated:** Ad-hoc scripts written to regenerate missing PNG graphs after subagents crashed.
  * **Why redundant:** Trajectory graphs are now drawn programmatically during evaluation.

### Audited Single-Use Task Fixes
* **`repair_dry_run_links.py`**, **`mark_live.py`**, **`move_live.py`**, **`filter_candidates.py`**, **`sync_harvested_evaluations.py`**
  * **Why generated:** Written to fix modes (reply vs. root) or force-update links.
  * **Why redundant:** Standard `aletheia_bot.py` sync logic and clean generation prevent link corruption natively.
* **`generate_evaluated_json_files.py`** (Our temporary repair script)
  * **Why generated:** Used to quickly regenerate the 16 missing candidates.
  * **Why redundant:** Portfolios are now complete, and further runs will use the standardized batch local manual workflow.

---

## 4. Archiving Execution Strategy

All files listed in **Section 3** will be systematically relocated to **`bluesky_bot/_Archive/`** to isolate them from active runs. The folder structure of `stories/` remains completely pristine, keeping only the 21 valid dry-runs and `stories_registry.js` database files.
