# Implementation Plan - Refined Trajectory Path Logic

Update the programmatic trajectory path name determination (`get_path_name` in python files) and align all Gnostic Actualism convergence test instructions to match the updated rules.

## User Review Required

> [!IMPORTANT]
> The path name calculation rules are updated as follows for same-zone alignments:
> 1. If both stated and actual are in the **Greater Good** (`+u, +will` quadrant):
>    - If actual is equal to or greater than stated: returns `"Grace"`.
>    - If actual is less than stated on either coordinate (`real_u < claim_u` or `real_psi < claim_psi`), it represents a downward shift (fall):
>      - If the Euclidean distance between coordinates is $\le 1.0$, it returns `"Small Fall from Grace"`.
>      - Otherwise, it returns `"Fall from Grace"`.
> 2. If both stated and actual are in any other quadrant, the path returns the specific zone's entry name (instead of a generic `"Stasis"`):
>    - **Greatest Lie**: `"Deception"`
>    - **Lesser Good**: `"Redemption"`
>    - **Greater Evil**: `"Destruction"`
> 3. If stated and actual are in different quadrants, it continues to return `"{exit_name} into {entry_name}"` (e.g. `"Revelation into Grace"`).

## Proposed Changes

### Python Trajectory Engine

#### [MODIFY] [generate_graph.py](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/generate_graph.py)
* Refactor `get_path_name` to calculate paths with the new same-zone rules, including distance-based magnitude qualifiers for falls from Grace.

#### [MODIFY] [test_slew.py](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/tests/test_slew.py)
* Sync the copy of `get_path_name` in `test_slew.py` with the updated algorithm in `generate_graph.py` to ensure test assertions pass.

---

### Convergence Test Instructions

#### [MODIFY] [Convergence-test-v2.md](file:///E:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/Convergence-test-v2.md)
* Update Phase 5 description and path/trajectory sections to specify the new same-zone logic so that LLMs during deep audits align with the new naming logic.

#### [MODIFY] [convergence_lite.md](file:///E:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/convergence_lite.md)
* Update Section 5 (Path Names) to detail the new same-zone logic, including `"Grace"`, `"Small Fall from Grace"`, `"Fall from Grace"`, `"Deception"`, `"Redemption"`, and `"Destruction"`.

#### [MODIFY] [convergence_son.md](file:///E:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/convergence_son.md)
* Update same-zone trajectory definitions in the path names section.

#### [MODIFY] [convergence_son_lite.md](file:///E:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/convergence_son_lite.md)
* Update Section 5 (Output Trajectory (Path Names)) with the same specifications.

## Verification Plan

### Automated Tests
* Run `pytest` or run `python tests/test_slew.py` to verify path calculations work correctly.
* Run a dry run to verify story evaluation results compile with the correct path strings:
  `python bluesky_bot/google_ai_studio_one_shot.py --url https://example.com --dry-run`
