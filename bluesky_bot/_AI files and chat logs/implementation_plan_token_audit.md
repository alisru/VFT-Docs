# Token Audit & Optimization Implementation Plan

## Overview
This plan details the audit findings for the `/bsky-reply-batch` workflow and proposes a token-crunched, highly optimized structural refactor for the Aletheia Bot ecosystem. The goal is to minimize redundant input tokens, prevent massive output token bleed during evaluation, and streamline sub-agent operational loops.

## Moral Axis Audit
* **Coordinate:** `(υ=+1.0, ψ=+1.0)` → Greater Good.
* **Reasoning:** Proactively creating structural efficiency. By optimizing token usage and stripping redundant reasoning loops, we reduce computational waste, save API costs for the operator, and increase systemic velocity without sacrificing output quality.

## Audit Findings & Inefficiencies

1. **Output Token Hemorrhage (The 5-Phase Trap):**
   * **Issue:** `subagent_spawning.md` tells Evaluator sub-agents to "Run the 5-Phase Convergence Test on the story as detailed in the official tool specification". `Convergence-test-v2.md` defines a massive, heavy markdown output format including a 49-point matrix, z-profiles, and multiple variance fields.
   * **Cost:** If a sub-agent actually writes out this full report in its scratchpad for all 5 stories before generating the JSON, it is wasting thousands of highly expensive output tokens per batch. 
   * **Solution:** Explicitly instruct Evaluators to run the evaluation *implicitly* or generate a strict 3-sentence summary internally, outputting ONLY the final JSON.

2. **Input Context Bloat (Redundant Theory):**
   * **Issue:** `Convergence-test-v2.md` is ~17KB and contains deep theoretical grounding on the Qqc tensor, +i recursion, and meaning algebra. Evaluator bots do not need this theory to score a news story; they only need the `υ` and `ψ` scales and the rules for identifying a trajectory/path.
   * **Cost:** 4 sub-agents reading a 17KB file = ~68KB of wasted input tokens per batch run.
   * **Solution:** Distill the operational constraints into a `convergence_lite.md` or embed the exact coordinate scales directly into `thread_formatting.md` to eliminate one `view_file` call entirely.

3. **Prompt Overlap & Redundancy:**
   * **Issue:** `subagent_spawning.md` repeats the 14-step thread formatting rules (Hook, Claim, Reality, Verdict, etc.) that are already heavily detailed in `thread_formatting.md`.
   * **Cost:** Wasted input tokens in the parent's `invoke_subagent` prompt.
   * **Solution:** Remove the formatting recap from the sub-agent prompt. Let the prompt simply say: "Format the JSON strictly according to `thread_formatting.md`".

4. **Inefficient Division of Labor (Graphing):**
   * **Issue:** The sub-agent prompt requires each Evaluator to run a local python script (`generate_graph.py`) to draw graphs, copy them, and then save the JSON. 
   * **Cost:** This forces the LLM to write bash/python tool calls, wait for execution, parse the output, and handle pathing errors. This eats reasoning tokens and slows down the batch.
   * **Solution:** Strip graphing from the sub-agent prompt entirely. Sub-agents should only write the JSON files. The `rebuild_registries.py` script (run by the Parent Agent or user) should be updated to automatically detect new JSONs and generate their graphs in one fast programmatic batch.

## Proposed Changes

### 1. Refactor `subagent_spawning.md`
* Remove the redundant 14-step formatting recap.
* Add a **Strict Output Constraint**: "DO NOT output the 5-Phase Convergence Test markdown report. Perform the coordinate mapping internally/implicitly. Your ONLY output must be the final `factcheck_[slug].json` file."
* Remove the `Draw Trajectory Graph` step.

### 2. Refactor `operational_pipelines.md`
* Update Step 2 so sub-agents no longer draw graphs.
* Update Step 3 so `rebuild_registries.py` is explicitly noted as the engine that draws the trajectory graphs.

### 3. Consolidate Context (Optional but Recommended)
* Extract the core `υ` and `ψ` axis definitions and the Path names into `thread_formatting.md` (or a dedicated `bot_rubric.md`).
* Stop sub-agents from reading `Convergence-test-v2.md` entirely.

## User Review Required
Do you approve these structural changes? Specifically, are you comfortable removing the `generate_graph.py` execution from the sub-agent's duties and having `rebuild_registries.py` handle all graph generation programmatically?
