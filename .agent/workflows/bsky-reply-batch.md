---
description: How to harvest 20+ new Bluesky news posts, execute high-fidelity convergence tests locally, and generate complete dry runs with trajectory graphs.
---

# Bluesky Reply Batch Workflow (/bsky-reply-batch)

This workflow governs the harvesting, offline evaluation, and dry-run compilation of a batch of 20+ Bluesky posts for reply mode evaluations.

---

## 1. Prerequisites & Safety Safeguards
* **Bot 1 Locked:** Always perform evaluations using the Local Agent-Interactive Bot (Bot 2) native reasoning. Never run or trigger background API evaluation processes.
* **Environment Setup:** Ensure `BSKY_HANDLE` and `BSKY_PASSWORD` are loaded inside `bluesky_bot/.env`.

---

## 2. Step-by-Step Pipeline

### Phase 1: Harvesting Candidates
To harvest 20+ fresh news posts from Bluesky's verified news feeds, run the RSS/BSKY hybrid harvester:
```powershell
.venv\Scripts\python scratch\harvest_candidates_script.py
```
* **Target:** This command connects to Bluesky, fetches verified news items from Aendra's feeds, extracts external link cards, de-duplicates them against all historical stories, and writes a clean array to [scratch/harvested_candidates.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/harvested_candidates.json).
* **If less than 20 candidates:** Modify `TARGET_BSKY` inside `scratch/harvest_candidates_script.py` to a higher number (e.g., 40), or manually append new external article targets to the candidates array.

### Phase 2: High-Fidelity Convergence Tests
For each harvested post in the candidates JSON:
1. **Convergence Analysis:** Run the 5-Phase Convergence Test under the Actualism Framework.
2. **Character Count Strict Check:** Ensure each of the 14 posts is strictly under 250 characters.
3. **No Numbering:** Ensure thread posts contain zero prefixes (`1/`, `2/`, etc.) and read as organic, standalone paragraphs.
4. **Link Rules:** Set `"link"` to the actual news article URL and `"target_url"` to the original Bluesky post URL. Set `"mode"` to `"reply"`.

### Phase 3: Trajectory Graph Drawing
For each evaluated story:
1. Programmatically call `draw_graph` from `generate_graph.py` to draw the trajectory.
2. Save the graph inside `bluesky_bot/graph_png/` as `[subject_slug]_graph.png`.
3. Copy the graph to `_Generated_Content/graph_png/`.

### Phase 4: Registry Update & Indexing
Run the recompiler script to clean up `index.json` files and regenerate the registry:
```powershell
.venv\Scripts\python scratch\rebuild_registries.py
```
* This populates `stories_registry.js` with the correct `graph_png/` prefixes in both workspace locations.

### Phase 5: Verification & Safety Audit
1. Open the [control_panel.html](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/control_panel.html) in your browser.
2. Verify that all 20+ stories render flawlessly with correct paths, and confirm that there are zero console exceptions or broken images.

---

## 3. Moral Axis Audit
* **Calculated Coordinate:** `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* **Verdict:** Standardizing harvesting workflows and automating offline convergence testing builds structured quality safeguards into the research pipeline.
