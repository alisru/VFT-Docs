# Semantic Gluon Project & Task Management Rule

When planning, tracking, or managing non-trivial features, refactorings, or comparative goals (e.g., "better", "faster", "cleaner"):

## 1. Always Use the Semantic Gluon Project Manager
Use the `semantic-gluon` MCP tools or `semantic_project_db.py` to record goals, track constraints, and detect contradictions.

## 2. Mandatory Comparative Goal Anchoring (Testing "Better")
Whenever the user or task introduces qualitative or comparative aims (such as *"make it faster"*, *"better search"*, *"cleaner code"*, *"lightweight"*):
- You MUST anchor the predicate using `gluon_anchor_comparative`:
  - **`predicate`**: The claim (`better`, `faster`, `simpler`).
  - **`target_dimension`**: The metric (`latency_ms`, `memory_mb`, `loc`, `token_cost`).
  - **`baseline_was_like`**: The previously accepted benchmark.
  - **`boundary_is_not`**: The taboo ceiling / side-effect constraint that invalidates the improvement if breached.
- After implementation, test and record the outcome with `gluon_verify_comparative`. Never declare success without verifying that the `is_not` boundary was respected.

## 3. Strict Topological Boundary Defense
- Map goals to positive vertices:
  - `will_be`: Committed target outcome.
  - `can_be`: Feasible actionable next step.
  - `may_be`: Speculative hypothesis.
  - `is_like`: Validated architectural pattern/exemplar.
- Map boundaries to negative vertices:
  - `is_not`: Hard taboo / forbidden side effect.
  - `cant_be`: Physical, structural, or architectural impossibility.
  - `wont_be`: Pruned or explicitly rejected scope.
  - `was_like`: Deprecated or superseded legacy.
- **Auto-Cancellation**: If a collision occurs between `will_be` and `cant_be` (Fatal Contradiction), treat the goal as neutralized and refactor the architecture rather than pushing invalid code.
- If `can_be` breaches `is_not` (Boundary Violation), immediately pause and resolve the conflict.

## 4. Dual Persistence & Board Visibility
- Every project state is recorded in `semantic_project.db` and synchronized to `project_desires.json`.
- When reporting project status, use `gluon_render_board` to provide a clear Markdown overview of the 8-vertex topology.
