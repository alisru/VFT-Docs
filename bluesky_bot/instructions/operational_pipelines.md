# Agentic Operational Process & Pipelines

This document outlines the pipeline process and execution steps for harvesting, evaluating, and publishing news story threads in the Aletheia Bot ecosystem.

---

## 1. Division of Labor (Finder vs. Evaluator Subagents)

To preserve API token budget and isolate context bloat, candidate harvesting is strictly separated from actualism evaluation:

* **Finder Subagents (Search & Extract)**: Scrape raw news candidates from feeds/searches. They are permitted to run high-volume web searches and scraping tools. Their output is limited to a clean JSON candidate list (`{ "subject", "link", "text" }`) after which they terminate, discarding high-volume context bloat.
* **Evaluator Subagents (Actualism Evaluation)**: Perform convergence tests and draft the threads. They do not perform any web searches or external browsing, operating strictly on the clean input texts and system instructions.

---

## 2. Beehive Model: Turn-Based Sequential Evaluation

Candidates are evaluated one-at-a-time by a single active bee. This eliminates output truncation, rate limit spikes, and parallel file-write collisions. The Queen (parent agent) manages the entire lifecycle.

**Key parameters (empirically measured):**
* Typical evaluation time per story: ~43 seconds
* Timeout cutoff per dispatch: **90 seconds** (2× buffer for model slowness)
* Bee retirement interval: **every 10 stories** (prevents context bloat)
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
The parent (Queen) runs a sequential turn-based loop:

1. Load `bluesky_bot/stories/harvested_candidates.json` and build an ordered queue.
2. Spawn **one bee** using the `Beehive Evaluator Bee` system prompt from `subagent_spawning.md`. Workspace: `inherit`.
3. Track two counters: `stories_sent_to_bee` (resets at retirement) and `completed` (total).
4. For each candidate in the queue:
   a. Send the candidate JSON object to the active bee via `send_message`.
   b. Start a `schedule` timer for **90 seconds**.
   c. **If `1` returns** before the timer: increment `completed`, cancel the timer, advance queue.
   d. **If the timer fires first**: `manage_subagents → kill` the bee, spawn a fresh one, re-dispatch the same candidate.
   e. After every **10 successful evaluations**: proactively retire the bee (`manage_subagents → kill`), spawn a fresh one.
5. Once the queue is exhausted, proceed to Step 3.

*The bee writes each `factcheck_[id].json` directly to `bluesky_bot/stories/`. The parent never parses JSON from chat.*

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
