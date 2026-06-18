---
description: Run the Bluesky news post harvest, offline 6-Attractor SON convergence test, and dry-run evaluation batch.
---

# Bluesky Reply Batch Workflow (SON Edition) (/bsky-reply-batch-son)

This workflow governs the harvesting, offline evaluation, and dry-run compilation of a batch of Bluesky posts for reply mode evaluations using the high-precision **6-Attractor SON Convergence Test** (`convergence_son_lite.md`). Evaluation runs via the **Beehive turn-based loop** — utilizing 5 parallel bees, giving a story from the FIFO list to whichever agent finishes first until the list is exhausted, writing directly to disk.

---

## 1. Prerequisites & Execution Guidelines

To prevent model context bloat and token wastage, the parent orchestrator is strictly separated from the heavy evaluation modules. **Do NOT open the thread formatting or convergence test modules.**

1. **Master Instructions Index:** First, read [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md) to load the operational rules and script locations.
2. **Operational Pipeline:** Read [operational_pipelines.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/operational_pipelines.md) to understand the step-by-step batch execution process.
3. **Sub-Agent Prompts:** When it is time to spawn the Evaluator workers in Step 2, open [subagent_spawning_son.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/subagent_spawning_son.md) to get their prompt templates.

Please execute steps 1 through 5 of the local operational pipeline as documented in [operational_pipelines.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/operational_pipelines.md).

---

## 2. Moral Axis Audit
* **Calculated Coordinate:** `(υ=+1.8, ψ=+1.8)` -> Greater Good & Productive Justice.
* **Verdict:** Transitioning the batch processing pipeline to the 6-Attractor force balance equations maximizes the accuracy and alignment of the automated Aletheia bot ecosystem.
