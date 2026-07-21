# Implementation Plan: Simplify Macro Framing out of Posting Engine

This plan simplifies the posting engine by removing the unused and redundant dual (micro-macro) framing prompt instructions and output matrix elements, resulting in significant input/output token savings and reducing structural reasoning confusion for the LLM. 

## Proposed Changes

We will remove the macro elements from the LLM prompt and output format list, shift the subsequent SON evaluation indexes in `google_ai_studio_one_shot.py`, and clean up the schema instruction files. To ensure 100% backward compatibility for downstream scripts, the parsed story dictionaries will still populate `"macro_event": ""`, and all macro coordinates to `None` by default in python before writing JSON stories.

---

### Bluesky Bot Prompt and Schema Cleanup

#### [MODIFY] [google_ai_studio_one_shot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
* Update `expected_len` variable definition to `20 if use_son else 12` (instead of `25 if use_son else 17`).
* Remove items 12 through 16 (`macro_event`, `macro_claim_u`, `macro_claim_psi`, `macro_real_u`, `macro_real_psi`) from the system prompt `output_format` structure.
* Shift subsequent SON indices in `output_format` prompt (claim_rnet, real_rnet, etc.) to start at 12 instead of 17.
* Remove macro elements from the response example in the prompt and shift the SON example fields.
* Update `run_one_shot_evaluations` parser loop:
  * Remove extraction of `macro_event`, `macro_claim_u`, `macro_claim_psi`, `macro_real_u`, `macro_real_psi` from incoming `item` slices.
  * Hardcode macro coordinates and names in the constructed `story` dict:
    ```python
    "macro_event": "",
    "macro_claim_u": None,
    "macro_claim_psi": None,
    "macro_real_u": None,
    "macro_real_psi": None,
    ```
  * Update SON parser indices (12 to 19 instead of 17 to 24) to map `claim_rnet`, `real_rnet`, etc. correctly.

#### [MODIFY] [thread_formatting_son.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting_son.md)
* Remove keys 17 to 21 (`macro_event`, `macro_claim_u`, `macro_claim_psi`, `macro_real_u`, `macro_real_psi`) from section 1 JSON blueprint structure and adjust numbers of subsequent keys.
* Update the bottom example JSON block to remove the macro keys (retaining standard SON keys).

#### [MODIFY] [subagent_spawning_son.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/subagent_spawning_son.md)
* Remove `Phase 6: Macro Context Scan` from the instructions.
* Remove `macro_event`, `macro_claim_u`, `macro_claim_psi`, `macro_real_u`, `macro_real_psi` from the list of expected keys in step 3.

---

## Verification Plan

### Automated Tests
* Run `validate_batch.py` or run a dry-run invocation of `google_ai_studio_one_shot.py` on a sample candidate using a dry-run flag to verify the JSON structure parses cleanly and produces correct output files with standard fields.
* Run `rebuild_registries_son.py` to verify that existing files and newly written files integrate seamlessly into the story registries.
