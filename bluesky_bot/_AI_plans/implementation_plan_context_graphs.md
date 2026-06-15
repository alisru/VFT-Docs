# Implementation Plan: Nested Context-in-Context Graphs

Introduce a nested, multi-layered coordinate system to visually display a micro-event's evaluation inside its overarching macro-context event (e.g. evaluating a sports title win within the context of a political photo-op event).

## Proposed Changes

### 1. Evaluator Prompt & Schema Changes
#### [MODIFY] [google_ai_studio_one_shot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
* Update system prompts and examples to instruct the model to identify and evaluate the **macro-context event** if the story contains one.
* Expand the JSON output list schema from 11 items to 16 items by appending:
  * `item[11]`: `macro_event` (string; name of the overarching context/venue, or `""` if none)
  * `item[12]`: `macro_claim_u` (float or `null`)
  * `item[13]`: `macro_claim_psi` (float or `null`)
  * `item[14]`: `macro_real_u` (float or `null`)
  * `item[15]`: `macro_real_psi` (float or `null`)
* Update `transpose_flat_to_json` to parse these 5 new elements if they exist (gracefully defaulting to `""` and `None` for backward compatibility with older 11-element JSONs).

### 2. Validation & Registry Processing
#### [MODIFY] [post_batch.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/post_batch.py) and [validate_batch.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/validate_batch.py)
* Ensure validation does not fail if new optional macro keys (`macro_event`, `macro_claim_u`, etc.) are present in the JSON story configs.

#### [MODIFY] [rebuild_registries.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/rebuild_registries.py)
* Update calls to `draw_graph` to pass the new macro parameters from the config dictionary if present.

### 3. Graph Generation Logic
#### [MODIFY] [generate_graph.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/generate_graph.py)
* Update `draw_graph` signature to accept optional macro parameters:
  ```python
  def draw_graph(claim_u, claim_psi, real_u, real_psi, title, filename,
                 macro_event="", macro_claim_u=None, macro_claim_psi=None, macro_real_u=None, macro_real_psi=None)
  ```
* If `macro_event` is present:
  1. Plot the **macro-event** coordinates `(macro_claim_u, macro_claim_psi)` and `(macro_real_u, macro_real_psi)` on the outer axes as standard Stated (yellow circle) and Actual (red star) points.
  2. Draw an **inner nested box** centered at `(0, 0)` spanning `[-0.5, 0.5]` on both outer axes.
  3. Determine if the macro-context is **selfish** (`macro_real_u < 0`). If so, **mirror the inner coordinate space horizontally (flipped on the vertical y-axis)** (`is_mirrored = True`).
  4. Write inner quadrant labels (`The Greater Good`, `The Greatest Lie`, etc.) and corner tags (`JUSTICE`, `TYRANNY`, etc.) inside the inner box, mirrored horizontally using `scale(-1, 1)` transform if mirrored.
  5. Plot the **micro-event** coordinates `(claim_u, claim_psi)` to `(real_u, real_psi)` inside the inner box. The plot coordinates are scaled by `0.25` and the morality coordinate (u) is negated if mirrored:
     * `u_plot = (-claim_u if is_mirrored else claim_u) * 0.25`
     * `psi_plot = claim_psi * 0.25`
  6. Draw dashed connection projection lines from the outer macro points to the corresponding inner box corners in the same quadrant.

---

## Verification Plan

### Automated Tests
1. Create a verification script `scratch/test_context_graph.py` that calls the updated `draw_graph` using the exact UFC / White House event parameters:
   * **Macro**: Stated `(1.0, 1.0)`, Actual `(-1.0, -1.0)` ("White House promotional event")
   * **Micro**: Stated `(0.0, 0.0)`, Actual `(-0.5, 0.5)`
2. Run the script and output the graph to `scratch/test_context_graph.png`.
3. Check that the inner box is correctly rotated 180 degrees, points are scaled, and dashed projection lines connect the outer points to the inner corners.
