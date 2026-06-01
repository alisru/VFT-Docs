# Goal: Optimize Orchestrator Token Burn

The current workflow is highly inefficient and burns through API requests rapidly, leading to the quota exhaustion (429 errors) you experienced. The goal is to restructure the logic to slash the token consumption and API request count by 80% per story.

## The Current Workflow (5 Requests / Story)
Currently, evaluating a single story requires 5 separate trips to the LLM API:
1. **Phase 1 Baseline (1 Call):** Parses the claim, reality, and writes Posts 2-11.
2. **Phase 2 Concurrent (3 Calls):** Spawns separate prompts for Awwthekanon, Brothekanon, and Alethekanon to get their individual perspectives and solutions.
3. **Phase 3 Audit (1 Call):** Feeds the results from Phases 1 & 2 back into the LLM to synthesize the final coordinates and write Posts 12-14.

*Impact: You can only evaluate 4 stories before hitting the 20 Requests-Per-Day Gemini Free Tier limit.*

## Proposed Optimized Workflow (1 Request / Story)
Modern Gemini models have massive context windows and excel at multi-persona simulation and Chain-of-Thought reasoning. We don't need 5 separate calls. 

I propose condensing the entire pipeline into a **Single-Shot Evaluation Request**:
1. **Unified Prompt:** We rewrite the system prompt into a master instruction manual that tells the LLM to internally execute all 3 phases sequentially.
2. **Internal Persona Simulation:** The LLM will simulate the Aww/Bro/Ale reactions internally (we can have it output their thoughts into hidden JSON fields for its own context).
3. **Single Output Payload:** The LLM returns the full, finalized JSON block containing all 14 posts, coordinates, and trajectories at once.

*Impact: 1 Request / Story. We cut API usage by 80%, meaning we can evaluate 20 stories per day on the free tier instead of 4, saving vast amounts of tokens and dramatically speeding up the cron script.*

## Proposed Changes

### `bluesky_bot/orchestrator.py`
- [MODIFY] `orchestrator.py`: Remove `run_phase1`, `run_phase2`, and `run_phase3`. Replace with a single `run_unified_evaluation` function.
- [MODIFY] `orchestrate_batch.py`: Apply the same unified function if we want to batch process using the API in the future.

## User Review Required
> [!IMPORTANT]
> Merging these prompts means the LLM will generate the whole thread at once. It might lose a tiny fraction of the "independent distinctness" that separate API calls provide to Aww/Bro/Ale, but with a strong prompt, it should be highly comparable while saving 80% of your tokens. Do you approve of collapsing the 3 phases into a single LLM request?
