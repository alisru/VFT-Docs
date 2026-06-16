# Implementation Plan: Context Inversion Logic Correction

This plan outlines the correction of the programmatic detection and plotting of **perceptual inversions** inside context-in-context graphs. We use the coordinates of the story `gaethje-ufc-white-house-show` as our primary research reference.

---

## 1. Research Reference: `gaethje-ufc-white-house-show`

The core reference values are:
*   **Micro Event (UFC Victory)**:
    *   Stated Claim: $claim\_u = 1.0, claim\_\psi = 0.0$
    *   Actual Reality: $real\_u = 1.0, real\_\psi = 1.0$ (athletic achievement in isolation)
*   **Macro Context (White House Event / Birthday Ball)**:
    *   Stated Claim: $m\_claim\_u = 1.0, m\_claim\_\psi = 0.0$
    *   Actual Reality: $m\_real\_u = -1.0, m\_real\_\psi = -1.0$ (bad containing frame)

Using these reference coordinates, we distinguish two different systemic cases:

### Case A: The Micro Event is a Genuine Good Act (Subversive)
*   **Concept**: A positive action that challenges, subverts, or exposes the bad containing frame (e.g. Whistleblower, Volunteer).
*   **Mathematical Mapping**:
    *   Actual morality coordinate remains positive: $real\_u = 1.0$ (exposing truth/helping others).
    *   Because the containing frame is bad ($m\_real\_u = -1.0 < 0$), the inner box's perception grid is inverted (`is_inverted = True`).
    *   We plot the micro-point at its actual coordinate: $u\_ac\_plot = real\_u \times 0.5 = +0.5$ (left side).
    *   Because the inner box is inverted, the label on the left side is **Perceived Evil / Threat**.
    *   **Result**: The graph correctly shows a positive actual outcome ($+0.5$ on the outer axis) that is perceived/treated as an evil threat by the bad containing system.

### Case B: The Micro Event is Co-opted (Supportive)
*   **Concept**: An action that is celebrated as good by the system, but structurally supports, maintains, or promotes the bad containing frame (e.g. commercial victory co-opted by a dictator).
*   **Mathematical Mapping**:
    *   Because the action supports the bad containing frame, its actual moral value in this context is negative: $real\_u = -1.0$ (reinforcing the bad frame).
    *   Because the containing frame is bad ($m\_real\_u < 0$), the inner box's perception grid is inverted (`is_inverted = True`).
    *   We plot the micro-point at its actual coordinate: $u\_ac\_plot = real\_u \times 0.5 = -0.5$ (right side).
    *   Because the inner box is inverted, the label on the right side is **Perceived Good**.
    *   **Result**: The graph correctly shows a negative actual outcome ($-0.5$ on the outer axis) that is perceived/celebrated as good by the containing system.

---

## 2. Proposed Code Changes

### Graph Generation Script
#### [MODIFY] [generate_graph.py](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/generate_graph.py)
*   Update `is_inverted` to depend solely on whether the macro context is bad:
    ```python
    is_inverted = (m_real_u < 0)
    ```
*   Remove coordinate flipping for micro-points (plot them exactly where they belong on the outer axes):
    ```python
    u_st_plot = claim_u * 0.5
    psi_st_plot = claim_psi * 0.5
    u_ac_plot = real_u * 0.5
    psi_ac_plot = real_psi * 0.5
    ```

### Test Suite Script
#### [MODIFY] [test_slew.py](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/tests/test_slew.py)
*   Apply the identical `is_inverted` and plotting updates to the test graphing function `draw_test_graph`.
*   Ensure that test cases with co-opted micro-actions (e.g., dedicated team leader supporting a corrupt merger) have their actual morality coordinates input as negative ($real\_u < 0$) to reflect their actual systemic effect, while genuine good acts (e.g., whistleblowers) remain positive ($real\_u > 0$).

### Research File
#### [MODIFY] [table_of_inversions.md](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/_AI_plans/table_of_inversions.md)
*   Update section 2 and Case Gaethje description to document the `gaethje-ufc-white-house-show` values under both interpretations (Subversive vs Co-opted) as the primary research reference.

---

## 3. Verification Plan

### Automated Tests
*   Run the test script to regenerate the 32 test cases and check that their layouts are visually correct:
    ```powershell
    python "E:/Vector Field Theory/VFT Docs/bluesky_bot/tests/test_slew.py"
    ```
*   Ensure all regenerated PNGs in `_AI files and chat logs/test_runs` align with the corrected grid.
