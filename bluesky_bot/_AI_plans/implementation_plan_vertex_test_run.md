# Implementation Plan: Vertex AI Model Test Verification (SON + Search) on New Story

This plan details the steps to properly run, parse, and verify evaluations using **gemini-2.5-flash** and **gemini-3.1-flash-lite** on Vertex AI under the **6-Attractor SON + Google Search** configuration, using a **new harvested story** from the feeds.

## Target Story Candidate
We will use the following fresh news candidate harvested from the feeds:
*   **Title**: `"From a White House podium, Vance delivers 'stunning development' on Israel"`
*   **URL**: `https://www.abc.net.au/news/2026-06-19/jd-vance-unprecedented-comments-on-israel-over-iran-deal/106817622`
*   **Context**: JD Vance publicly warning Israel to accept the US-Iran deal, highlighting a deteriorating alliance and reliance on US defense aid.

---

## Proposed Changes

### Test Runner Parsing & File Hardening

#### [MODIFY] [run_gemma_model_test.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/run_gemma_model_test.py)
- **Target New Story**: Swap the default candidate definition (lines 68-72) to point to the new JD Vance story.
- **Parse SON JSON**: Update the parser block around line 208:
  - If `args.son` is enabled, do not call `transpose_flat_to_json` (which expects list of lists and throws errors for dictionaries).
  - Clean markdown code fences (```json ... ```) and extract the raw JSON structure.
  - Parse the array containing the evaluation dictionary.
  - Validate the `posts` array and print character lengths/warnings for posts exceeding 299 characters.
- **Increment Output Files**: Add logic to find the next available run number `N` (starting at 1) for the output files:
  - For `gemini-2.5-flash`: `scratch/vertex_test_outputs/gemini_2_5_flash_run_N.json`
  - For `gemini-3.1-flash-lite`: `scratch/vertex_test_outputs/gemini_3_1_flash_lite_run_N.json`
  - Save the parsed JSON to that file.

---

## Verification & Execution Plan

We will run the following two commands sequentially:

1.  **Run Gemini 2.5 Flash Test**:
    ```powershell
    .venv\Scripts\python.exe scratch/run_gemma_model_test.py --model vertex:gemini-2.5-flash --son --search
    ```
2.  **Run Gemini 3.1 Flash-Lite Test**:
    ```powershell
    .venv\Scripts\python.exe scratch/run_gemma_model_test.py --model vertex:gemini-3.1-flash-lite --son --search
    ```

For each run:
- The script will output raw token usage, elapsed time, and raw model response.
- The parsed JSON response will be saved to the next incremented file:
  - `scratch/vertex_test_outputs/gemini_2_5_flash_run_N.json`
  - `scratch/vertex_test_outputs/gemini_3_1_flash_lite_run_N.json`
- We will present a side-by-side qualitative comparison of:
  - Coordinate reasoning and alignment accuracy.
  - Plain English style flow.
  - Limit warnings (whether any posts exceed character caps).
