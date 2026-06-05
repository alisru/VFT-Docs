# Agentic Operational Process & Pipelines

This document outlines the pipeline process and execution steps for harvesting, evaluating, and publishing news story threads in the Aletheia Bot ecosystem.

---

## 1. Division of Labor (Finder vs. Evaluator Subagents)

To preserve API token budget and isolate context bloat, candidate harvesting is strictly separated from actualism evaluation:

* **Finder Subagents (Search & Extract)**: Scrape raw news candidates from feeds/searches. They are permitted to run high-volume web searches and scraping tools. Their output is limited to a clean JSON candidate list (`{ "subject", "link", "text" }`) after which they terminate, discarding high-volume context bloat.
* **Evaluator Subagents (Actualism Evaluation)**: Perform convergence tests and draft the threads. They do not perform any web searches or external browsing, operating strictly on the clean input texts and system instructions.

---

## 2. Beehive Model: Turn-Based Parallel FIFO Evaluation

Candidates are evaluated by 5 parallel bees, giving a story from the FIFO list to whichever agent finishes first until the list is exhausted. This maximizes throughput while avoiding parallel file-write collisions (since each story has a unique output ID). The Queen (parent agent) manages the queue dispatch and worker lifecycles.

**Key parameters (empirically measured):**
* Typical evaluation time per story: ~43 seconds
* Timeout cutoff per dispatch: **90 seconds** per worker (2× buffer for model slowness)
* Bee retirement interval: **every 10 stories** per individual bee (prevents context bloat)
* Concurrency count: **5 bees** running in parallel
* Token outage: excluded from timeout scope — if quota is exhausted the parent dies too, timeout is irrelevant

---

## 3. Local Operational Pipeline (Bot 2 Mode)

All evaluations run locally in the workspace to ensure safety, security, and manual gatekeeping. The pipeline executes as follows:

### Step 1: Harvest Candidates
Run the harvesting scripts locally inside the virtual environment to pull candidates from Bluesky verified news feeds and search endpoints:
```bash
.venv\Scripts\python.exe bluesky_bot/harvest_candidates.py --rss-target 0 --bsky-target 40
```
This writes the raw candidate feeds to `scratch/harvested_candidates.json`.

### Step 2: Beehive Evaluation Loop (Dry Run)
The parent (Queen) runs a parallel FIFO turn-based loop:

1. Load `bluesky_bot/stories/harvested_candidates.json` and build a global FIFO queue.
2. Spawn **5 parallel bees** (Bee 1 to Bee 5) using the `Beehive Evaluator Bee` system prompt from `subagent_spawning.md`. Workspace: `inherit`.
3. Track individual metrics per bee: `stories_sent_to_bee_[id]` (for retirement checks) and `completed` (total).
4. Initially pop and dispatch the first 5 stories to the 5 spawned bees respectively.
5. Whenever any bee returns `1` (indicating it has completed a story and written `factcheck_[id].json` to disk):
   a. Increment the `completed` counter.
   b. Check if the global FIFO queue has remaining stories. If yes, pop the next story and send it to that specific idle bee.
   c. Start/reset a `schedule` timer of **90 seconds** for that specific bee.
   d. If a bee reaches **10 successful evaluations**, proactively retire it (`manage_subagents → kill`), spawn a fresh replacement bee, and dispatch the next story from the queue to the replacement.
   e. If a bee's timer fires before it returns `1`, kill that specific bee, spawn a fresh replacement, and re-dispatch the failed story to the replacement.
6. Once the global queue is exhausted and all active dispatches complete, terminate all active bees and proceed to Step 3.

*Each bee writes its `factcheck_[id].json` directly to `bluesky_bot/stories/`. The parent never parses JSON from chat.*

### Step 3: Registry & Graph Rebuild
Recompile the indexes, registry database, and automatically draw missing trajectory graphs:
```bash
.venv\Scripts\python.exe bluesky_bot/rebuild_registries.py
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
