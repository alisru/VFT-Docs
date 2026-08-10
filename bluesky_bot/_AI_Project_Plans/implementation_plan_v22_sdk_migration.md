# Implementation Plan - Google Gen AI SDK Migration, Model Upgrades & UI Thinking Controls

Migrate the Bluesky bot's API calls from the deprecated `google-generativeai` SDK to the modern `google-genai` SDK. Add `gemini-3.5-flash-lite` and `gemini-3.6-flash` to the available model registries, and add a **Thinking Level** selector directly to the Aletheia operator console UI to configure thinking mode dynamically.

## Proposed Changes

### Operator Console GUI

#### [MODIFY] [AletheiaLauncher.pyw](file:///e:/Vector Field Theory/VFT Docs/AletheiaLauncher.pyw)
- Add a dropdown combobox for **Thinking Level** (`combo_thinking`) next to the "Prioritize Outlets" row in the grid layout.
- Options: `"OFF"`, `"LOW"`, `"MEDIUM"` (default), `"HIGH"`.
- Forward the selected value to the backend python process via the new `--thinking-level` argument.
- Add `"gemini-3.5-flash-lite"` and `"gemini-3.6-flash"` to the fallback lists.

### Bluesky Bot Backend

#### [MODIFY] [google_ai_studio_one_shot.py](file:///e:/Vector Field Theory/VFT Docs/bluesky_bot/google_ai_studio_one_shot.py)
- Import `from google import genai` and `from google.genai import types`.
- Update `DEFAULT_FALLBACKS` list to include `"gemini-3.5-flash-lite"` and `"gemini-3.6-flash"`.
- Add `--thinking-level` argument parser parameter.
- Refactor `get_gemini_client()` to return `genai.Client(api_key=api_key)`.
- Refactor `run_one_shot_evaluations` to accept `thinking_level` parameter.
- Build `types.ThinkingConfig` dynamically based on selection:
  - If `thinking_level == "OFF"`: Disable thinking config (set `thinking_budget=0` for Gemini 2.5, omit or set `thinking_budget=0` for Gemini 3.x).
  - If `thinking_level` is `LOW`, `MEDIUM`, or `HIGH`:
    - **Gemini 3.x models**: Use `thinking_level` string mapping.
    - **Gemini 2.5 models**: Map to `thinking_budget` tokens (`LOW` = 1024, `MEDIUM` = 2048, `HIGH` = 4096).
- Use `genai_client.models.generate_content()` with `types.GenerateContentConfig`.

#### [MODIFY] [consolidate_roundups.py](file:///e:/Vector Field Theory/VFT Docs/bluesky_bot/consolidate_roundups.py)
- Refactor legacy `google.generativeai` code to use `google-genai` SDK and client call conventions (e.g. `client.models.generate_content`).

#### [MODIFY] [fix_roundups.py](file:///e:/Vector Field Theory/VFT Docs/bluesky_bot/fix_roundups.py)
- Refactor legacy generative model calls in the manual regeneration block to use `google-genai` client model calls.

---

## Verification Plan

### Manual Verification
- Launch the operator console and confirm the "Thinking Level" dropdown is rendered with "MEDIUM" pre-selected.
- Select "LOW", "HIGH", or "OFF" and run a dry-run evaluation. Verify that the CLI command logs the correct `--thinking-level` argument.
- Run `tests/test_banlist.py` and a dry-run batch call to confirm it initializes the new client without any syntax or type validation errors.
