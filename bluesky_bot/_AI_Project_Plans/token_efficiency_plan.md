# Token Efficiency Improvements for `/bsky-reply-batch` Workflow

This plan outlines the specific file modifications required to resolve the 7 token inefficiencies identified in the recent audit.

## Proposed Changes

### Workflows & Master Index

#### [MODIFY] [bsky-reply-batch.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/workflows/bsky-reply-batch.md)
*   **Remove Step 2** (`operational_pipelines.md` reference) from the Prerequisites & Execution Guidelines.
*   **Update Step numbering** so the parent agent is instructed to jump directly from reading the master index/running the harvest script to spawning the subagents via `subagent_spawning.md`.

#### [MODIFY] [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)
*   **Remove Section 4 (Bluesky Profile Bio & Custom Persona Text)** entirely from this file. This reduces context bloat for the parent orchestrator. (This information will be relocated to a separate `persona.md` file if needed, or left in the live posting scripts where it actually matters).

---

### Subagent Spawning Templates

#### [MODIFY] [subagent_spawning.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/subagent_spawning.md)
*   **Fix Index Notation (FIND-04):** Change `Batch [Batch ID] (Stories [Start Index] to [End Index], which are indices [Start Index - 1] to [End Index - 1])` to a clean, array-index-only format: `Batch [Batch ID] (evaluating array indices [Start Index] through [End Index] from harvested_candidates.json)`.
*   **Strengthen Constraint (FIND-07):** Update the "No File Writing" constraint to explicitly state the consequence: `Any file write tool call will cause your output to be discarded. Output JSON in your final message only.`
*   **Update File References:** Update the mandatory initialization section to point to the newly created "lite" files (`convergence_batch.md` and `thread_formatting_lite.md`) instead of the full versions.

---

### Evaluation Modules

#### [NEW] [thread_formatting_lite.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting_lite.md)
*   Create a stripped-down version of `thread_formatting.md` specifically for batch evaluators.
*   Retain the 13-key JSON schema definition and the rules for the 14 logical steps.
*   **Remove the canonical JSON example** at the end.
*   **Remove the verbose quoted examples** for each of the 14 elements, keeping only the instructional wording and formatting rules.

#### [NEW] [convergence_batch.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/convergence_batch.md)
*   Create a streamlined version of `convergence_lite.md` for batch mode.
*   Retain the core tables: The 7 Planes, Phase 1 pass/fail conditions, the υ and ψ scoring tables, and Path Names.
*   **Remove Phase 4** (Fake Maximiser / Helxis stress tests).
*   **Remove the mathematical derivation prose** surrounding the `p·t` primitive, keeping only the actionable scoring rules.

---

## Future Optimization (FIND-06)

> [!NOTE]
> The highest-payoff optimization (FIND-06: eliminating the 8 subagent warm-up turns by inlining the lite module content directly into `subagent_spawning.md`) is complex and makes the spawning template very large. 
> 
> For this first pass, we will implement the lightweight changes and the creation of the `lite` files. Once these are stable, we can move to inline the content.

## User Review Required

Does this plan accurately capture how you want to address the audit findings? If you approve, I will proceed with creating the new lite files and updating the existing instructions.
