# Beehive Turn-Based Evaluation Workflow: Architectural Design Report

This report analyzes the transition from the legacy parallel batch evaluation model to the turn-based "beehive" model. It identifies structural failures in the current design and details how the new sequential pool model achieves stability.

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

The beehive model resolves this by centralizing state management in the parent (Queen) and treating child agents (bees) as stateless, turn-based reasoning loops.

```
+-------------------------------------------------------+
|                 Parent Agent (Queen)                  |
|  - Controls queue state & Git staging                  |
|  - Manages active worker lifecycle                    |
|  - Validates and writes draft JSONs                   |
+-------------------------------------------------------+
                           |
            (Feeds 1 candidate at a time)
                           |
                           v
+-------------------------------------------------------+
|                 Active Worker (Bee)                   |
|  - Reads instructions (reused in history)             |
|  - Evaluates single candidate                         |
|  - Returns single JSON thread (~2,800 chars)          |
+-------------------------------------------------------+
```

### Protocol Steps:
1. **Queue Initialization:** The parent loads the harvested candidate list.
2. **Worker Spawning:** The parent spawns a single worker bee with the evaluation system prompt.
3. **Sequential Stepping:** The parent feeds candidates one-by-one to the active bee using the `send_message` tool.
4. **Isolated Evaluation:** The bee evaluates a single story, returns the JSON block, and awaits the next input.
5. **Immediate Validation & Quarantine:** The parent receives the JSON, checks it against the strict 14-post schema, and writes it directly to disk (moving failures immediately to `stories/fail/`).
6. **Pruned Retirement:** After ten evaluations, the parent kills the active bee using `manage_subagents` to prevent history-based context bloat, resetting the cycle with a fresh worker.

---

## 3. Implication: Performance, Security, and State Continuity

This shift improves execution safety across three core areas:

### Payload Integrity
A single-story evaluation fits comfortably within the model's output generation limits. The JSON payloads are short and concise. Truncation is eliminated.

### Fault Tolerance (Incremental Saves)
Because file writing is managed by the parent after each turn, every successful evaluation is instantly committed to disk. If the network drops or a crash occurs on story #15, the first 14 stories remain saved. The run can resume exactly where it stopped.

### Token Conservation
We only pay the 3,000-token worker initialization fee once per ten stories. Retiring the bee at ten evaluations limits the input history size. This prevents the exponential cost growth associated with sending a massive conversation history on every turn.

### Structural Comparison

| Metric | Parallel Batch (Legacy) | Beehive Turn-Loop (Proposed) |
| :--- | :--- | :--- |
| **Active Subagents** | 6 concurrent | 1 active at a time |
| **Output Token Load** | ~14,000 (Exceeds limits) | ~2,800 (Safe) |
| **Rate Limit Risk** | High | Extremely Low |
| **Crash Recovery** | Zero (Loose entire batch) | Incremental (Resume from last save) |
| **File Writing** | Attempted by child / Parent block | Handled strictly by Parent |
