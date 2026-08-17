# Implementation Plan - Multi-Aspect and Multi-Actor Convergence Test Audits (New Mode Edition)

The goal is to implement multi-aspect and multi-actor audits as a **new, optional mode** (`--multi-aspect`). This ensures that all existing operational pathways (such as standard SON or regular evaluations) remain completely unchanged and safe. When `--multi-aspect` is active, the model will identify 2-4 primary actors and aspects, evaluate their individual attractor forces, and output them in the JSON schema. The rebuilder will then dynamically aggregate them to calculate the overall coordinates.

## User Review Required

> [!IMPORTANT]
> - **New CLI Option**: Added `--multi-aspect` to `google_ai_studio_one_shot.py`.
> - **New UI Option**: Added an "Enable Multi-Aspect Audit" checkbox to `AletheiaLauncher.pyw`, aligned symmetrically in the grid.
> - **Strict Pathway Isolation**:
>   - When `--multi-aspect` is **disabled** (default), the schema remains `27` items in SON mode (or `17` items in standard mode) with no alterations to inputs, parsing, or rebuilder behavior.
>   - When `--multi-aspect` is **enabled**, the schema expands to `28` items, and the aspects array is parsed and aggregated.

---

## Proposed Changes

### 1. Bot Command Line Evaluator

#### [MODIFY] [`google_ai_studio_one_shot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
- Add a new command-line argument `--multi-aspect` (store as boolean `args.multi_aspect`).
- Pass `multi_aspect` flag into `run_one_shot_evaluations()`.
- Update `expected_len`:
  ```python
  expected_len = 28 if (use_son and use_multi_aspect) else (27 if use_son else 17)
  ```
- Conditionally update `output_format` instructions:
  - If `use_multi_aspect` is True, append the aspects description (item 27) and update the example config to show aspects.
- Update `transpose_flat_to_json()` to conditionally parse item 27:
  ```python
  if len(item) >= 28 and isinstance(item[27], list):
      story["aspects"] = item[27]
  ```

### 2. Registry Rebuilder

#### [MODIFY] [`rebuild_registries_son.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/rebuild_registries_son.py)
- Implement `calculate_aggregated_forces(aspects_list, force_key)`:
  - Sums the `S`, `O`, and `N` force scores for each of the 6 attractors across the aspects and divides by the number of aspects to calculate average forces.
- Update `process_and_update_coordinates(cfg, file_path)`:
  - Only recalculate aspects and aggregate forces if `"aspects"` exists in `cfg` (which is only true when generated under `--multi-aspect` mode).
  - This ensures standard dry-run or live stories bypass aspect calculations entirely.

### 3. Launcher Console GUI

#### [MODIFY] [`AletheiaLauncher.pyw`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/AletheiaLauncher.pyw)
- Add a new BooleanVar `self.val_multi = tk.BooleanVar(value=False)`.
- Add a new Checkbutton `self.chk_multi` ("Enable Multi-Aspect Audit") placed on Row 7 next to the Compact Mode checkbox.
- Forward the `--multi-aspect` flag to the subprocess when `self.val_multi` is checked.

---

## Verification Plan

### Automated Tests
- Run `tests/test_banlist.py` to confirm compile safety.
- Run a dry-run batch call with `--multi-aspect` enabled on the Sudan story to verify correct parsing, staging, recalculation, and decimal coordination.
- Run a dry-run batch call *without* `--multi-aspect` to verify the standard path remains fully functional.
