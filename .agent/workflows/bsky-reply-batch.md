---
description: Run the Bluesky news post harvest, offline convergence test, and dry-run evaluation batch.
---

# Bluesky Reply Batch Workflow (/bsky-reply-batch)

This workflow governs the harvesting, offline evaluation, and dry-run compilation of a batch of 20+ Bluesky posts for reply mode evaluations.

---

## 1. Prerequisites & Execution Guidelines

To prevent model drift and maintain a single source of truth, all operational steps, code blocks, formatting specifications, and sub-agent spawning procedures are centralized in the bot directory:

1. **Master Instructions Index:** Before running this workflow, always load and read [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md).
2. **Operational Steps & Pipelines:** Follow the step-by-step pipeline documented in [operational_pipelines.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/operational_pipelines.md).
3. **JSON Schema & Thread Formatting:** Ensure absolute compliance with the keys and constraints in [thread_formatting.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting.md).
4. **Actualism Mappings:** Run all Gnostic Actualism evaluations strictly using [Convergence-test-v2.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/Convergence-test-v2.md).
5. **Sub-Agent Prompts:** Spawn finder/evaluator workers using the templates in [subagent_spawning.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/subagent_spawning.md).

Please execute steps 1 through 5 of the local operational pipeline as documented in [operational_pipelines.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/operational_pipelines.md).

---

## 2. Moral Axis Audit
* **Calculated Coordinate:** `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* **Verdict:** Directing execution to a single central source of truth prevents operational drift and eliminates redundant documentation.
