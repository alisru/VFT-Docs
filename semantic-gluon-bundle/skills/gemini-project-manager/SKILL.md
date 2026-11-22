---
name: gemini-project-manager
description: Coordinate autonomous task execution, desire tracking, comparative goal verification ('better' testing), and anti-desire contradiction cancellation using the Semantic Gluon Project Management MCP Server and SQLite engine.
allowed-tools: execute_bash view_file write_to_file call_mcp_tool
---
# Gemini Project Manager (Semantic Gluon Engine)

Coordinate autonomous task execution, desire tracking, comparative goal verification, and topological boundary defense.

## Summary

The Gemini Project Manager integrates the 8-vertex Semantic Gluon topology into task execution workflows. It allows the agent to:
- **Ground Subjective Claims**: Transform vague descriptors like *"make it better"*, *"faster"*, *"cleaner"* into rigorous, falsifiable criteria.
- **Topological Boundary Defense**: Automatically neutralize and cancel desires that collide with invariant constraints along opposition vectors (`will_be` vs `cant_be`, `can_be` vs `is_not`, etc.).
- **Dual Persistence**: High-integrity SQLite database (`semantic_project.db`) with real-time JSON sync (`project_desires.json`).
- **Evolutionary Lineage**: Track desire supersession and task retirement into historical precedent (`was_like`).
- **Production MCP Server**: Native integration via stdio JSON-RPC 2.0 (`semantic-gluon` server).

---

## The 8-Vertex Modal Topology

| Vertex | Semiotic Role | Space |
| :--- | :--- | :--- |
| **`is`** | Ground Truth Reality / Baseline State | Center Axis |
| **`will_be`** | Target Goal / Committed Definitive Future | Solution Outer |
| **`can_be`** | Active Capability / Feasible Next Action | Solution Inner |
| **`may_be`** | Hypothesis Probe / Speculative Exploration | Constructive Inner |
| **`is_like`** | Working Precedent / Validated Pattern | Constructive Outer |
| **`is_not`** | Hard Taboo Boundary / Anti-Goal Ceiling | Problem Outer |
| **`cant_be`** | Invariant Constraint / Physical Impossibility | Problem Inner |
| **`wont_be`** | Explicitly Rejected Scope / Pruned Path | Regressive Inner |
| **`was_like`** | Obsolete Legacy / Deprecated Benchmark | Regressive Outer |

---

## Comparative Goal Anchoring Protocol (Testing "Better")

Whenever a vague or qualitative goal is introduced (e.g., *"improve search speed"*, *"clean up architecture"*):

### 1. Extract the 4-Point Anchor
- **Predicate**: The comparative claim (`better`, `faster`, `cleaner`, `more scalable`).
- **Target Dimension**: The measurable variable (`latency_ms`, `memory_mb`, `loc_count`, `test_coverage`).
- **Baseline (`was_like`)**: The previously accepted benchmark or metric.
- **Boundary Guardrail (`is_not`)**: The taboo threshold that immediately refutes the claim if breached.
- **Exemplar Template (`is_like`)**: Optional proven architectural pattern.

### 2. Register Anchor via MCP Tool
Call `gluon_anchor_comparative`:
```json
{
  "project_id": "PRJ-001",
  "desire_id": "DES-001",
  "predicate": "better",
  "target_dimension": "latency",
  "baseline_was_like": "Linear scan took 350ms",
  "boundary_is_not": "Memory usage must not exceed 50MB and zero cloud API reliance"
}
```

### 3. Verify Against Reality
After execution, call `gluon_verify_comparative`:
- If the boundary was breached: Status becomes `invalidated_by_boundary` and the desire is marked `conflicted`. (A feature cannot be "better" if it violates an explicit anti-desire).
- If it beat the baseline without breaching boundaries: Status becomes `verified_true`.
- If it failed to beat the baseline: Status becomes `refuted_false`.

---

## Tool Reference (Semantic Gluon MCP)

| Tool Name | Purpose |
| :--- | :--- |
| `gluon_init_project` | Initialize a new project with ID, name, description, and ground truth (`is`). |
| `gluon_list_projects` | List all tracked projects in the database. |
| `gluon_add_desire` | Register a target goal or capability (`will_be`, `can_be`, `may_be`, `is_like`). |
| `gluon_add_anti_desire` | Register an invariant, taboo, or boundary (`is_not`, `cant_be`, `wont_be`, `was_like`). |
| `gluon_anchor_comparative` | Ground comparative claims into falsifiable metrics against baselines and boundaries. |
| `gluon_verify_comparative` | Record empirical measurements and verify if the comparative goal held true. |
| `gluon_add_task` | Attach an executable sub-task to an active desire. |
| `gluon_update_task` | Update task status (`pending`, `in_progress`, `completed`, `cancelled`, `blocked`). |
| `gluon_supersede_desire` | Retire an old desire into `was_like` history and link its replacement. |
| `gluon_detect_conflicts` | Run collision checks across opposition vectors and auto-cancel invalid goals. |
| `gluon_run_process` | Execute Parables dynamic operations (`productive`, `reductive`, `constructive`, `regressive`). |
| `gluon_render_board` | Generate a complete, scannable Markdown status board. |
| `gluon_export_json` | Export database state to portable `project_desires.json`. |

---

## Natural Contradiction Opposition Lines

1. **`will_be` vs `cant_be` (Red Primary - Fatal Contradiction)**:
   - Target Goal breaches an Invariant Constraint.
   - *Action*: Automatic cancellation of the desire and its subtasks.
2. **`can_be` vs `is_not` (Green Primary - Boundary Violation)**:
   - Active action breaches an Anti-Goal Boundary.
   - *Action*: Flagged as `conflicted`, task execution halted.
3. **`is_like` vs `wont_be` (Red Secondary - False Analogy)**:
   - Solution mimics a pattern that was explicitly rejected.
4. **`may_be` vs `was_like` (Green Secondary - Regression Risk)**:
   - Speculative probe duplicates an obsolete legacy failure.
