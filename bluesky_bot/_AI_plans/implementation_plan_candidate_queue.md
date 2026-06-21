# Implementation Plan: Stateful Candidate Queue & History Index (Non-Scratch Edition)

This plan details the implementation of a stateful, persistent news candidate queue and historical harvest index, relocating all data files out of the `scratch/` directory and directly into `bluesky_bot/`.

## Proposed Changes

### 1. File Path Relocations (Avoiding the Scratch Folder)
We will relocate all transient and test data files into the `bluesky_bot/` project directories:
- **Candidate Queue**: Moved from `scratch/harvested_candidates.json` to `bluesky_bot/harvested_candidates.json`.
- **Vertex Test Outputs**: Moved from `scratch/vertex_test_outputs/` to `bluesky_bot/tests/vertex_test_outputs/`.

---

### 2. Historical Candidate Indexing

#### [NEW] [harvested_history.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvested_history.json)
- A history index file that stores all URLs that have ever been harvested. This ensures that even if a candidate fails evaluation or is skipped/removed from the queue, it will not be harvested again on future runs.

---

### 3. Core Logic Modifications

#### [MODIFY] [harvest_candidates.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvest_candidates.py)
- **Startup Queue Loading**: 
  - Load existing queue from `bluesky_bot/harvested_candidates.json`.
  - Filter out any that have since been completed (matching `seen_historical_urls`).
- **Startup History Loading**:
  - Load `bluesky_bot/harvested_history.json` and add these URLs to `seen_historical_urls` to prevent re-harvesting historically attempted candidates.
- **Top-up Harvesting**:
  - Fetch new candidates, de-duplicating against completed history, harvested history, and the current pending queue.
  - Append newly harvested URLs to `bluesky_bot/harvested_history.json`.
- **Scrape & Merge**:
  - Perform article scraping *only* on newly harvested candidates.
  - Merge the existing pending queue with the new successfully scraped candidates, capped at `TARGET_RSS + TARGET_BSKY`.
  - Save the merged queue to `bluesky_bot/harvested_candidates.json`.

#### [MODIFY] [google_ai_studio_one_shot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
- Update candidate path references to `bluesky_bot/harvested_candidates.json`.
- **Immediate Deletion on Success**:
  - Inside the chunk evaluation loop, once evaluations are successfully staged via `process_evaluations`:
    1. Load `bluesky_bot/harvested_candidates.json`.
    2. Filter out candidates whose URLs match the processed chunk evaluations.
    3. Save the updated list back to `bluesky_bot/harvested_candidates.json`.

---

## Verification Plan

### Manual Verification
1. Run candidate harvest:
   ```powershell
   .venv\Scripts\python.exe bluesky_bot/harvest_candidates.py --bsky-target 5
   ```
   - Verify `bluesky_bot/harvested_candidates.json` is created with 5 candidates.
   - Verify `bluesky_bot/harvested_history.json` records these 5 URLs.
2. Run evaluation (dry-run on a single candidate or chunk):
   - Interrupt/stop after a candidate is completed.
   - Verify the evaluated candidate is removed from `bluesky_bot/harvested_candidates.json`, leaving the remaining candidates in the file.
3. Run candidate harvest again:
   ```powershell
   .venv\Scripts\python.exe bluesky_bot/harvest_candidates.py --bsky-target 5
   ```
   - Verify the harvester loads the remaining pending candidates, fetches new ones, and tops up `bluesky_bot/harvested_candidates.json` to 5 candidates without duplicates.
