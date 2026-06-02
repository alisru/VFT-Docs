# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 7 (Active): Formalization of Sub-Agent Prompt Instructions

We are formalizing the operational instructions for Finder and Evaluator sub-agents by creating a dedicated instruction file `subagent_instructions.md` within the `bluesky_bot/` directory. This ensures future runs do not rely on ad-hoc instructions and stay completely aligned with constraints.

### Proposed Changes

#### [NEW] [subagent_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/subagent_instructions.md)
* Create `subagent_instructions.md` to store formal templates for:
  - **Finder Sub-agents**: Crawl limits, scraping feeds, de-duplication, format constraints, and immediate exit.
  - **Evaluator Sub-agents**: Input batch limits, Convergence Test requirements, strict 14-step JSON schema constraints, trajectory graph generation, and registry updates.

### Verification Plan
* Validate that the new file `subagent_instructions.md` compiles and reads cleanly without format issues.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Standardizing prompt templates for sub-agents ensures consistent task delegation, preventing common formatting errors, token-wasting loops, or schema drifts in parallel runs.

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
