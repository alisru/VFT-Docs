# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 6 (Active): Process Integration and Batch Plan Archival

We are merging the agentic operational process instructions from `subagent_batch_plan.md` into `bluesky_bot_instructions.md` and archiving `subagent_batch_plan.md` to keep all bot instructions consolidated in a single file.

### Proposed Changes

#### [MODIFY] [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)
* Append new section **Section 6: Agentic Operational Process & Pipelines**.
* Incorporate the Finder vs. Evaluator subagent structure.
* Document the mathematical bounds for batch allocation (5 stories per evaluator).
* Detail the local pipeline execution workflow (harvesting, offline evaluations, index rebuild, review, publishing).

#### [ARCHIVE] [subagent_batch_plan.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/subagent_batch_plan.md)
* Move the current contents of `subagent_batch_plan.md` to `e:\Vector Field Theory\VFT Docs\bluesky_bot\_Archive\subagent_batch_plan_archive_20260602.md`.
* Remove `subagent_batch_plan.md` from the `bluesky_bot/` root folder.

### Verification Plan
* Ensure `bluesky_bot_instructions.md` has no markdown issues.
* Verify the archive file is correctly written and the original file is deleted in accordance with the no-delete archive rule.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Consolidating bot documentation into a single master instruction file eliminates layout discrepancies and ensures future agent runs do not split focus between multiple outdated specification files.

---

## Plan 5 (Completed): Automated Reply Harvesting & Batch Evaluation Workflow

We implemented the automated reply mode harvesting process to identify exactly 20+ fresh news posts from Bluesky feeds and standard search queries, perform programmatic convergence evaluations offline, compile character-bounded dry-run configs, generate trajectory graphs, and register them cleanly inside the HTML Portfolio control panel. We also introduced the `/bsky-reply-batch` system workflow to standardise this pipeline.

---

## Plan 4 (Completed): Consolidation of Graph PNGs into graph_png/ Subdirectories

We consolidated all Bluesky trajectory vector graph `.png` files into dedicated `graph_png/` subfolders inside both `bluesky_bot/` and `_Generated_Content/`. We also updated all system directives to save newly generated graphs directly inside these subfolders and updated the HTML viewer to automatically handle the prepended paths.

---

## Plan 3 (Completed): Workspace Root Consolidation

We consolidated all Bluesky-bot related files from the workspace root directory into the dedicated `bluesky_bot` folder to ensure directory hygiene, resolve file clutter, and keep all components perfectly isolated.

---

## Plan 2 (Completed): True Directory Separation and Programmatic Indexing

We resolved the folder pollution and dynamic indexing bugs in the Aletheia Bot system. Currently, live story files are scattered across root folders and the stories/ root folder, and `control_panel.html` fails to load live posts dynamically because it only indexes `stories/index.json` and fetches from the wrong paths.

---

## Plan 1 (Completed): Restoring HTML Viewer & High-Fidelity Candidate Regeneration

We remediated the catastrophic failure from the previous subagent run. The previous worker agents produced malformed and corrupted JSON structures containing mismatched coordinate keys, which broke the `control_panel.html` viewer.
