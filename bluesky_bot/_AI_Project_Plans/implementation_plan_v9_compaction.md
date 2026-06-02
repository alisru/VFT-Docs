# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 9 (Active): OOP-Style Instructions Split with Master Index linking to Convergence Test Tool

We are splitting the consolidated `bluesky_bot_instructions.md` into modular OOP-style instructions under a dedicated `bluesky_bot/instructions/` directory. `bluesky_bot_instructions.md` will serve as the Master Index and Entry Point, linking directly to the official `.agent/tools/convergence-test/Convergence-test-v2.md` specification for all coordinate, math, and actualism engine calculations to highlight alignment and prevent model drift.

### Proposed Changes

#### [MODIFY] [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)
* Convert this file into a Master Index.
* Link directly to the official [Convergence-test-v2.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/Convergence-test-v2.md) for Gnostic Actualism math and rules.
* Link to the new modular files under `bluesky_bot/instructions/`.

#### [NEW] [thread_formatting.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting.md)
* Details output format, JSON schema keys, canonical 14 logical steps mapping (Multi-Persona Sequence), and canonical example JSON block.

#### [NEW] [operational_pipelines.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/operational_pipelines.md)
* Details Finder vs. Evaluator division of labor, batch concurrency bounds, and local python orchestration flow steps.

#### [NEW] [subagent_spawning.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/subagent_spawning.md)
* Details `Batch Finder Worker` and `Batch Evaluator Worker` prompt templates, mandatory initialization checks (`view_file` calls), and context passing parameters.

### Verification Plan
* Validate that all markdown links in `bluesky_bot_instructions.md` compile and load cleanly.
* Ensure sub-agent prompt templates explicitly force reading the master index and sub-files before starting work.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Structuring the instructions into OOP-style modular components with direct links to the official convergence test tool prevents coordinate math drift, improves readability for sub-agents, and conserves token budget.

---

## Plan 8 (Completed): Consolidation of Sub-Agent Prompt Instructions into Master Instructions

We consolidated the newly created sub-agent prompt templates directly into the master `bluesky_bot_instructions.md` file (as Section 7) to keep the documentation unified in a single, comprehensive source of truth. We archived the standalone `subagent_instructions.md` file by renaming and moving it.

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
