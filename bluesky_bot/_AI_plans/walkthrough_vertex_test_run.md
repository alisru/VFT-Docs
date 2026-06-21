# Walkthrough: Vertex AI Model Test Verification & Comparison

This document summarizes the changes, execution metrics, and qualitative comparison of the test runs conducted for **Gemini 2.5 Flash** and **Gemini 3.1 Flash-Lite** on Vertex AI under the **SON + Search** configuration.

## Changes Made
- Modified [scratch/run_gemma_model_test.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/run_gemma_model_test.py):
  1. Updated the target candidate to the new JD Vance ABC News story.
  2. Replaced the `transpose_flat_to_json` call in SON mode with a direct JSON array/dictionary parser that handles markdown code fences and cleans brackets.
  3. Added auto-incrementing file saving logic so that runs are saved sequentially as `gemini_X_run_N.json` inside `scratch/vertex_test_outputs/`.

---

## Performance Comparison (JD Vance Story)

| Metric | Vertex: Gemini 2.5 Flash (Run 1) | Vertex: Gemini 3.1 Flash-Lite (Run 1) |
| :--- | :--- | :--- |
| **Elapsed Time** | 60.0 seconds | **8.05 seconds** (7.5x faster) |
| **Token Count** | Prompt: 6,143 \| Output: 1,514 \| Total: 7,657 | Prompt: 6,143 \| Output: 1,265 \| Total: 7,408 |
| **Saved File** | [vertex_gemini_2.5_flash_run_1.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/vertex_test_outputs/vertex_gemini_2.5_flash_run_1.json) | [vertex_gemini_3.1_flash_lite_run_1.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/vertex_test_outputs/vertex_gemini_3.1_flash_lite_run_1.json) |
| **Character Caps** | ❌ **FAILED**. Post 2 (305 chars), Post 10 (300 chars), and Post 11 (367 chars) all exceeded 299-character limit. | ✅ **PASSED**. Max post length was 257 characters. Zero limit warnings. |
| **Context Integrity** | ❌ **FAILED**. Suffered from context contamination. The `posts` array evaluated the Vance story, but the metadata keys (`id`, `subject`, `link`, `stated_forces`, `actual_forces`) were hallucinated from the **ACT budget story** from the previous session. | ✅ **PASSED**. Both metadata fields and posts were 100% correct, coherent, and aligned to the target Vance story. |

---

## Qualitative Highlights (Gemini 3.1 Flash-Lite)

*   **Coordinate mapping**: Puts the Stated Judgement at `(+1.0, +1.0) — Greater Good` (the framing of helping an ally for their own good) and the Actual Judgement at `(-1.0, -1.0) — Greater Evil` (the reality of publicly humiliating an ally for a transactional pivot to Iran).
*   **Plain English style**: The generated posts flow organically without numbering and capture the nuance:
    *   *First post*: "Public loyalty masks a fracturing alliance as the White House turns on its closest partner. From a White House podium, Vance delivers 'stunning development' on Israel."
    *   *Brothekanon*: "Calling your best friend a 'scumbag' on the world stage is definitely one way to handle a breakup. This is going to get a lot messier before it gets better."
