# Agentic Operational Process & Pipelines

This document outlines the pipeline process and execution steps for harvesting, evaluating, and publishing news story threads in the Aletheia Bot ecosystem.

---

## 1. Division of Labor (Finder vs. Evaluator Subagents)

To preserve API token budget and isolate context bloat, candidate harvesting is strictly separated from actualism evaluation:

* **Finder Subagents (Search & Extract)**: Scrape raw news candidates from feeds/searches. They are permitted to run high-volume web searches and scraping tools. Their output is limited to a clean JSON candidate list (`{ "subject", "link", "text" }`) after which they terminate, discarding high-volume context bloat.
* **Evaluator Subagents (Actualism Evaluation)**: Perform convergence tests and draft the threads. They do not perform any web searches or external browsing, operating strictly on the clean input texts and system instructions.

---

## 2. Mathematical Bounds & Batch Sweet Spot

To prevent file-write collisions and token accumulation, candidates are processed in parallel batches rather than a single monolithic run.
* **5 stories per evaluator** is the baseline allocation, balancing token efficiency with thread/file safety.

---

## 3. Local Operational Pipeline (Bot 2 Mode)

All evaluations run locally in the workspace to ensure safety, security, and manual gatekeeping. The pipeline executes as follows:

### Step 1: Harvest Candidates
Run the harvesting scripts locally inside the virtual environment to pull candidates from Bluesky verified news feeds and search endpoints:
```bash
.venv\Scripts\python.exe scratch/harvest_candidates_script.py
```
This writes the raw candidate feeds to `scratch/harvested_candidates.json`.

### Step 2: Local Evaluation (Dry Run)
The main AI agent in the chat workspace reads the harvested candidates from `scratch/harvested_candidates.json` and spawns 4 concurrent sub-agents using the native workspace tool `invoke_subagent` (with roles `Batch Evaluator Worker 1` to `4`, delegating index ranges 0-4, 5-9, 10-14, 15-19).


Each spawned evaluator sub-agent:
1. Reads `bluesky_bot_instructions.md` and `Convergence-test-v2.md` to load the exact guidelines and schemas.
2. Performs the Gnostic Convergence Test on their assigned 5 stories natively in the workspace (consuming 0 external LLM API tokens).
3. Compiles a 14-step JSON factcheck file (status set to `"COMPLETED DRY RUN"`) saved inside `bluesky_bot/stories/`.
4. Runs a Python command locally calling `draw_graph` from `generate_graph.py` to output trajectory graph images inside `bluesky_bot/graph_png/` and sync them to `_Generated_Content/graph_png/`.


### Step 3: Registry Rebuild
Recompile the indexes and registry database so they sync with the HTML control panel:
```bash
.venv\Scripts\python.exe scratch/rebuild_registries.py
```

### Step 4: User Review (Safety Gate)
Open `control_panel.html` locally in a browser:
1. Verify that all newly harvested stories render in the sidebar.
2. Inspect the 14 steps for each thread (verify they are unnumbered and under 250 characters).
3. Validate the plotted Matplotlib trajectory graphs.

### Step 5: Live Posting
Once approved, execute the live publishing script to post the dry runs sequentially and store the retrieved `rkeys` and `post_urls` back in the registry files:
```bash
.venv\Scripts\python.exe bluesky_bot/post_batch.py
```
