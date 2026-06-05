---
description: Run the Bluesky news post harvest, offline convergence test, and dry-run evaluation batch.
---

# Bluesky Reply Batch Workflow (/bsky-reply-batch)

This workflow governs the harvesting, offline evaluation, and dry-run compilation of a batch of Bluesky posts for reply mode evaluations. Evaluation runs via the **Beehive turn-based loop** — one bee, one story at a time, writing directly to disk.

---

## 1. Prerequisites & Execution Guidelines

To prevent model context bloat and token wastage, the parent orchestrator is strictly separated from the heavy evaluation modules. **Do NOT open the thread formatting or convergence test modules.**

1. **Master Instructions Index:** First, read [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md) to load the operational rules and script locations.
2. **Operational Pipeline:** Read [operational_pipelines.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/operational_pipelines.md) to understand the step-by-step batch execution process.
3. **Sub-Agent Prompts:** When it is time to spawn the Evaluator workers in Step 2, open [subagent_spawning.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/subagent_spawning.md) to get their prompt templates.

Please execute steps 1 through 5 of the local operational pipeline as documented in [operational_pipelines.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/operational_pipelines.md).

---

## 2. Moral Axis Audit
* **Calculated Coordinate:** `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* **Verdict:** Directing execution to a single central source of truth prevents operational drift and eliminates redundant documentation.
