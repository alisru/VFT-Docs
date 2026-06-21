# Implementation Plan: Vertex AI Endpoint Integration & Verification (SON + Search)

This plan details the addition of Google Cloud's **Vertex AI** Gemini endpoints to the model fallback and rotation chain in the Bluesky bot, specifically focusing on validating **gemini-2.5-flash** and **gemini-3.1-flash-lite** under the **SON + Google Search** configuration. 

This addresses the inconsistency of Google AI Studio's free tier when running search grounding.

## User Review Required

> [!IMPORTANT]
> - Vertex AI endpoints will be prefixed with `vertex:` (e.g., `vertex:gemini-2.5-flash`, `vertex:gemini-3.1-flash-lite`) to differentiate them from AI Studio endpoints.
> - The SDK will use the `VERTEX_API_KEY`, `VERTEX_PROJECT_ID`, and `VERTEX_LOCATION` parameters from `.env`.
> - If `VERTEX_API_KEY` is not set, it will automatically fall back to standard Google Application Default Credentials (ADC).

---

## Model Pricing comparison (Vertex AI)
*Both models share extremely low pricing tiers:*

*   **Gemini 2.5 Flash**: Input: $0.075 / 1M | Output: $0.30 / 1M
*   **Gemini 3.1 Flash-Lite**: Input: $0.0375 / 1M | Output: $0.15 / 1M *(50% cheaper than 2.5 Flash)*

### Per-Batch (3 stories) Cost Projection:
*   **Gemini 2.5 Flash (SON + Search)**: ~0.13 cents per call (~0.9 cents per 21 stories)
*   **Gemini 3.1 Flash-Lite (SON + Search)**: ~0.06 cents per call (~0.4 cents per 21 stories)

---

## Proposed Changes

### Configuration

#### [MODIFY] [.env](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/.env)
- Keep current configuration parameters:
  * `VERTEX_API_KEY`: API key for calling Vertex AI APIs.
  * `VERTEX_PROJECT_ID`: The GCP project ID (default: `alethekanon`).
  * `VERTEX_LOCATION`: The GCP region/location (default: `us-central1`).

---

### Core Logic

#### [MODIFY] [google_ai_studio_one_shot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
- Update `run_one_shot_evaluations` to handle model names prefixed with `vertex:`.
- When a `vertex:` prefix is encountered:
  1. Extract the base model name (e.g., `gemini-2.5-flash` or `gemini-3.1-flash-lite`).
  2. Initialize a Vertex-enabled `genai.Client` on the fly using project credentials.
  3. Call `generate_content` using the Vertex client with safety settings, max tokens, and Google Search tool configurations.
- Update `default_fallbacks` generation:
  * Dynamically interleave the Vertex counterparts (e.g. `vertex:gemini-2.5-flash` directly after `gemini-2.5-flash`) into the fallback chain.

#### [MODIFY] [enrich_stories.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/enrich_stories.py)
- Apply the same `vertex:` prefix parsing and client initialization to the `call_model` helper in `enrich_stories.py` so that story enrichment can also leverage the Vertex AI fallback.

---

## Verification Plan

### Automated Test Runs
We will execute a dry-run test using `scratch/run_gemma_model_test.py` or a custom verification script specifically targeting Vertex AI for the SON + Search config.

1.  **Test 1 (Gemini 2.5 Flash)**:
    ```powershell
    .venv\Scripts\python.exe scratch/run_gemma_model_test.py --model vertex:gemini-2.5-flash --son --search
    ```
2.  **Test 2 (Gemini 3.1 Flash-Lite)**:
    ```powershell
    .venv\Scripts\python.exe scratch/run_gemma_model_test.py --model vertex:gemini-3.1-flash-lite --son --search
    ```

We will monitor:
- Successful compilation and injection of search results.
- Correct JSON formatting (JSON list of lists).
- Exact prompt, candidate, and output token usage.
