# Beehive Turn-Based Evaluation Workflow: Architectural Design Report

We analyze the transition from the legacy parallel batch evaluation model to the turn-based "beehive" model. This document details how direct worker file-writing and parent-level bulk validation yield a robust, failure-tolerant pipeline.

---

## 1. Synthesis: The Structural Failure of Parallel Batches

The current system relies on parallel batch execution. In this model, the parent agent harvests candidate stories and partitions them across six concurrently spawned subagents. Each subagent must evaluate five stories and return a massive combined JSON block. 

This architecture fails under load. 

A 14-post thread for a single story requires approximately 2,800 characters of formatted JSON text. Multiplying this by five stories yields an output payload of nearly 14,000 characters (approximately 3,500 to 4,000 tokens). This exceeds the maximum response limit of standard model generation windows. 

The result is truncation. 

The subagent runs out of output tokens mid-sentence. The JSON array remains open and corrupted. When the parent attempts to parse the response, it crashes due to a syntax error or is left with half-formed drafts lacking posts. 

Furthermore, parallel agent spawning introduces concurrency issues. Running six subagents simultaneously triggers API rate limits and creates massive, uncoordinated token spikes. A single failure in one worker corrupts a fifth of the harvested batch, offering no recovery path.

---

## 2. Mechanics: The Sequential "Bee" Pool Model

The beehive model resolves this by delegating file persistence directly to the child agents (bees) and centralizing the validation gate at the parent (Queen) level.

```
+-------------------------------------------------------+
|                 Parent Agent (Queen)                  |
|  - Controls queue state & Git staging                  |
|  - Manages active worker lifecycle                    |
|  - Executes bulk validation at end of batch           |
+-------------------------------------------------------+
                           |
            (Feeds 1 candidate at a time)
                           |
                           v
+-------------------------------------------------------+
|                 Active Worker (Bee)                   |
|  - Reads instructions (reused in history)             |
|  - Evaluates single candidate                         |
|  - Writes draft JSON directly to stories/             |
|  - Returns simple 'done' status to parent             |
+-------------------------------------------------------+
```

### Protocol Steps:
1. **Queue Initialization:** The parent loads the harvested candidate list.
2. **Worker Spawning:** The parent spawns a single worker bee with the evaluation system prompt.
3. **Sequential Stepping:** The parent feeds candidates one-by-one to the active bee using the `send_message` tool.
4. **Isolated Evaluation & Write:** The bee evaluates a single story, writes the completed `factcheck_*.json` file directly to `stories/` on disk, and returns a simple status response (e.g., "done") to the parent.
5. **Bulk Validation (End of Batch):** Once the queue is exhausted, the parent runs the new validator script `validate_batch.py` in bulk. This scans the folder, validates all generated JSON files, and automatically quarantines any failed configurations to `stories/fail/` for manual remediation or disposal.
6. **Pruned Retirement:** After ten evaluations, the parent kills the active bee using `manage_subagents` to prevent history-based context bloat, resetting the cycle with a fresh worker.

---

## 3. Implication: Performance, Security, and State Continuity

This shift improves execution safety across three core areas:

### Payload Integrity
By writing the file directly to disk, the bee does not need to output large JSON blocks back in the chat history. The response message is a simple, lightweight status code. Truncation and history bloat are completely eliminated.

### Fault Tolerance (Incremental Saves)
Because file writing is completed by the worker immediately after each evaluation, every successful draft is instantly committed to disk. If the network drops or a crash occurs, all previously completed stories remain saved. The run can resume exactly where it stopped.

### Token Conservation
We only pay the 3,000-token worker initialization fee once per ten stories. Retiring the bee at ten evaluations limits the input history size. This prevents the exponential cost growth associated with sending a massive conversation history on every turn.

### Structural Comparison

| Metric | Parallel Batch (Legacy) | Beehive Turn-Loop (Revised) |
| :--- | :--- | :--- |
| **Active Subagents** | 6 concurrent | 1 active at a time |
| **Output Token Load** | ~14,000 (Exceeds limits) | Minimal (Returns 'done' status) |
| **Rate Limit Risk** | High | Extremely Low |
| **Crash Recovery** | Zero (Lose entire batch) | Incremental (Resume from last save) |
| **File Writing** | Attempted by child / Parent block | Handled directly by child per turn |
| **Validation Gate** | Parsed in-memory per turn | Bulk verified at end via validate_batch |
