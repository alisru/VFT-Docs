---
name: task
description: Manage project tasks, desires, and anti-desires using the Semantic Gluon 8-Vertex Modal Topology engine. Automatically tracks goals, anchors comparative improvements ('better'), enforces boundary defense, and cancels unviable paths.
allowed-tools: call_mcp_tool execute_bash view_file write_to_file
---
# Semantic Gluon Task & Project Manager

The `/task` workflow coordinates autonomous task execution, desire tracking, and topological boundary defense using the **Semantic Gluon 8-Vertex Topology Engine** (`semantic-gluon` MCP).

---

## Quick Command Guide

When the user types `/task` or asks to track progress, interpret their intent using the Gluon engine:

| User Input | Action / MCP Tool Call |
| :--- | :--- |
| `/task` (or `/task board`, `/task status`) | Call `gluon_render_board` to display the active 8-vertex project board. |
| `/task list` | Call `gluon_list_projects` to see all tracked projects. |
| `/task add <goal>` | Identify if it is a desire or anti-desire and call `gluon_add_desire` or `gluon_add_anti_desire`. |
| `/task todo <task desc>` | Call `gluon_add_task` to attach an actionable step under the active desire. |
| `/task done <task_id>` | Call `gluon_update_task` with `status: "completed"`. |
| `/task start <task_id>` | Call `gluon_update_task` with `status: "in_progress"`. |
| `/task avoid <boundary/taboo>` | Call `gluon_add_anti_desire` at vertex `is_not` or `cant_be`. |
| `/task better <metric/goal>` | Call `gluon_anchor_comparative` to ground "better" against a baseline and taboo ceiling. |
| `/task verify <comp_id>` | Call `gluon_verify_comparative` with empirical measurements. |
| `/task supersede <old> <new>` | Call `gluon_supersede_desire` to retire the old desire into `was_like` history. |
| `/task conflicts` | Call `gluon_detect_conflicts` to audit opposition lines. |
| `/task process <type> <item_id>` | Call `gluon_run_process` (`productive`, `reductive`, `constructive`, `regressive`). |

---

## Automated Desire & Anti-Desire Tracking

During normal conversation (even without `/task`), the AI actively:
1. **Identifies Positive Goals (Desires)**:
   - Committed target futures $\to$ `will_be`
   - Active feasible steps $\to$ `can_be`
   - Speculative ideas $\to$ `may_be`
   - Proven patterns/templates $\to$ `is_like`
2. **Identifies Hard Limits & Taboos (Anti-Desires)**:
   - Forbidden side effects / taboos $\to$ `is_not`
   - Physical or architectural limits $\to$ `cant_be`
   - Pruned or rejected scope $\to$ `wont_be`
   - Obsolete legacy to avoid duplicating $\to$ `was_like`
3. **Synchronizes State**:
   - Saves relational data to `semantic_project.db` and exports real-time JSON to `project_desires.json`.

---

## Topological Contradiction Opposition Lines

When desires or anti-desires are registered, the engine audits the 4 cross-opposition vectors:

1. **`will_be` vs `cant_be` (Red Primary - Fatal Contradiction)**:
   - Target Goal breaches an Invariant Constraint.
   - *Engine Action*: The desire and attached tasks are **automatically cancelled** and logged with the reason.
2. **`can_be` vs `is_not` (Green Primary - Boundary Violation)**:
   - Active step enters a taboo boundary.
   - *Engine Action*: Desires/tasks are marked `conflicted` and paused immediately.
3. **`is_like` vs `wont_be` (Red Secondary - False Analogy)**:
   - Mimicking a rejected pattern.
4. **`may_be` vs `was_like` (Green Secondary - Regression Risk)**:
   - Hypothesis duplicates an obsolete legacy failure.

---

## The 4 Dynamic Laws of Action

1. **Reductive Process** (`cant_be` $\to$ `is_not`):
   - Collapses an impossibility into a hard boundary invariant using `was_like` and `can_be` opposing `is_like`.
2. **Productive Process** (`can_be` $\to$ `will_be`):
   - Elevates a feasible capability into a definitive target goal using `is_not` and `is_like` opposing `was_like`.
3. **Regressive Process** (`wont_be` $\to$ `was_like`):
   - Retires rejected scope or superseded architecture into historical precedent using `is_not` and `is_like` to oppose `can_be`.
4. **Constructive Process** (`may_be` $\to$ `is_like`):
   - Crystallizes a hypothesis into a validated working template using `can_be` and `was_like`.
