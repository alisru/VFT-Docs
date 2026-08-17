# Walkthrough - Multi-Aspect and Multi-Actor Convergence Test Audits Mode

I have successfully implemented the new optional **Multi-Aspect and Multi-Actor Convergence Test** mode. This allows the bot to evaluate multiple sub-aspects/actors of a story independently, aggregate their attractor forces, and compute highly granular overall coordinates.

## Changes Made

### 1. Evaluator CLI argument and Schema
- Added `--multi-aspect` CLI flag to [`google_ai_studio_one_shot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py).
- Programmed conditional expected output array length:
  - Default/Standard: `17` items
  - Standard SON: `27` items
  - Multi-Aspect SON: `28` items
- Updated the system prompt and instructions in `google_ai_studio_one_shot.py` to prompt the model to identify 2-4 key actors/aspects, perform separate convergence calculations in its thinking block, and output their details in Item 27.
- Updated the example JSON response in the prompt to illustrate the aspects format with realistic granular decimals.

### 2. Evaluator Parser
- Updated `transpose_flat_to_json()` in `google_ai_studio_one_shot.py` to parse Item 27 as `"aspects"` if present, saving it into the darkroom stage file.

### 3. Registry Rebuilder
- Added `calculate_aggregated_forces()` in [`rebuild_registries_son.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/rebuild_registries_son.py) to compute average forces across all sub-aspects.
- Updated `process_and_update_coordinates()` in `rebuild_registries_son.py` to:
  - If aspects are present, calculate coordinates for each aspect individually.
  - Average the sub-aspect forces to populate the parent story's `stated_forces` and `actual_forces`.
  - Recalculate overall coordinates dynamically using the net averaged forces.

### 4. Launcher UI
- Added the "Enable Multi-Aspect Audit" checkbutton on Row 7 of [`AletheiaLauncher.pyw`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/AletheiaLauncher.pyw) (symmetrically aligned next to 5-Word Mode and Compact Mode).
- Configured the subprocess argument construction to pass `--multi-aspect` to the execution command when checked.

---

## Verification Results

- **Syntax & Compilation Validation**: Running `tests/test_banlist.py` passed with code 0.
- **Aspect Integration dry-run**: Evaluated `https://www.techdirt.com/2026/08/10/spacexs-earnings-show-elon-wiped-out-two-thirds-of-twitters-ad-business/` in `--multi-aspect` mode.
  - The model returned two aspects: `"Elon Musk's Business Acumen"` and `"X (Twitter) Ad Revenue Performance"`.
  - Aspect 2 returned granular forces: `GG: O: 1.8`, `GE: S: 1.8`, `LG: O: 1.2`, etc.
  - The rebuilder calculated coordinates for both aspects individually, averaged their forces, and updated the parent story configuration successfully.
