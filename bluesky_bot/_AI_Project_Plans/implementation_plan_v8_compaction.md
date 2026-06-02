# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 8 (Active): Consolidation of Sub-Agent Prompt Instructions into Master Instructions

We are consolidating the newly created sub-agent prompt templates directly into the master `bluesky_bot_instructions.md` file (as Section 7) to keep the documentation unified in a single, comprehensive source of truth. We will archive the standalone `subagent_instructions.md` file by renaming and moving it.

### Proposed Changes

#### [MODIFY] [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)
* Append new section **Section 7: Sub-Agent Spawning Templates** containing the templates and rules for Finder and Evaluator sub-agents.

#### [ARCHIVE] [subagent_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/subagent_instructions.md)
* Rename and move `subagent_instructions.md` to `e:\Vector Field Theory\VFT Docs\bluesky_bot\_Archive\subagent_instructions_archive_20260602.md` via `git mv`.

### Verification Plan
* Validate that `bluesky_bot_instructions.md` reads cleanly and has no layout issues.
* Ensure the standalone file is archived by renaming and moving in accordance with the no-delete archive rule.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Keeping all documentation unified in one master instruction file prevents the context splits and coordinate drift that occur when an AI parses multiple files.

---

## Plan 7 (Completed): Formalization of Sub-Agent Prompt Instructions

We formalized the operational instructions for Finder and Evaluator sub-agents by creating a dedicated instruction file `subagent_instructions.md` within the `bluesky_bot/` directory.

---

## Plan 6 (Completed): Process Integration and Batch Plan Archival

We merged the agentic operational process instructions from `subagent_batch_plan.md` into `bluesky_bot_instructions.md` and archived `subagent_batch_plan.md` to keep all bot instructions consolidated in a single file.

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
