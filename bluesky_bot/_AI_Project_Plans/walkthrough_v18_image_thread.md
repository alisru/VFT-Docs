# Compact Posting Mode Implementation Walkthrough

We have successfully implemented a new parallel path in the Bluesky bot system to support **Compact Posting Mode**. Rather than publishing a long 13-post text thread, this path posts the first 4 posts (Hook, Claim, Reality, Verdict) as text and compiles the remaining 9 posts (Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Alethe, Aww, Bro) into a single, high-fidelity dark-mode infographic card PNG. This image is attached to the 4th post (Verdict) with the full summaries contained in its Alt Text, resulting in a premium, 4-post thread on the timeline.

## Changes Made

1.  **Image Generator Module (`image_card_generator.py`)**:
    *   Designed a visual rendering engine in Python using the `Pillow` library.
    *   Constructed a two-pass layout process: first measures text lines and container rectangles to dynamically calculate the overall canvas height, then draws the elements.
    *   Created styled slate panels with rounded corners (`#141D2F` on `#0B0F19`) and colored left borders mapping to each actualism section.
    *   Implemented separate perspective reaction boxes for Alethekanon, Awwthekanon, and Brothekanon stacked at the bottom of the card.
    *   Added robust font loading routines (Segoe UI/Arial/Consolas) with try-except fallback to the system default font.
2.  **API Prompt Adaptation (`google_ai_studio_one_shot.py`)**:
    *   Added a `--compact` CLI argument.
    *   When active, it dynamically modifies the system prompt limits and prepends a `COMPACT MODE DIRECTIVE` to the formatting rules, telling Gemini to output highly verbose, detailed narratives (400–800 characters) for posts 5–13 (indices 4–12) while keeping the first 4 posts under the 260-character limit.
    *   Tags the resulting story JSON with `"compact": true` on disk.
3.  **Staging Gate PNG Pre-generation (`rebuild_registries.py` & `rebuild_registries_son.py`)**:
    *   Modified the darkroom promotion gates to detect the `"compact": true` metadata.
    *   If active, it calls the `image_card_generator` to draw and write the visual card PNG directly to `graph_png/{slug}_info_card.png` at promotion time.
4.  **Batch Validator Bypass (`validate_batch.py`)**:
    *   Loads `"compact"` flag. If true, skips post-packing and limits length validation only to the first 4 elements (`posts[0:4]`).
    *   Validates that both the trajectory graph and the summary card PNG exist in `graph_png/`.
5.  **Thread Posting Engine (`aletheia_bot.py` & `post_batch.py`)**:
    *   Added `--compact` CLI override parameters.
    *   In `post_thread()`, if `compact` is active:
        *   Slices `final_posts` to only `posts[:4]` (Hook, Claim, Reality, Verdict) without packing.
        *   Uploads the staging `{slug}_info_card.png` to the Bluesky server.
        *   Attaches the card embed to the 4th post (Part 4, Verdict, index 3).
        *   Concatenates posts 4–12 into the image's Alt Text field (up to 10k character limits) for accessibility and search indexing.
6.  **Operator GUI Checklist Box (`AletheiaLauncher.pyw`)**:
    *   Integrated an "Enable Compact Image Mode" checkbutton in the One-Shot Batch Evaluator card.
    *   Appends the `--compact` flag when triggering the python execution process.

---

## Verification Results

### 1. Card Rendering Test
We ran `bluesky_bot/tests/test_info_card.py` to generate the card for the Larry the Cat/Andy Burnham story. It successfully wrapped lines, calculated canvas heights, and outputted the beautiful infographic PNG to `graph_png/andy_burnham_dog_info_card.png`.

### 2. Posting Slice Logic & Dry-Run Logs
We ran a local dry-run posting command inside the virtual environment:
```powershell
.venv\Scripts\python.exe bluesky_bot/aletheia_bot.py --config bluesky_bot/stories/factcheck_andy_burnham_dog.json --compact --dry-run
```
*   **Result**: The engine successfully sliced the thread count from 13 to **4 posts**.
*   *Post 1*: Hook (with Trajectory Graph Image embedded)
*   *Post 2*: Claim (with BBC article URL link card embedded)
*   *Post 3*: Reality (no embed)
*   *Post 4*: Verdict (with the new Compact Summary Card image embedded)
*   The dry-run validated and compiled successfully.

### 3. Batch Validation Check
We ran the batch validator `bluesky_bot/validate_batch.py` inside the virtual environment:
*   **Result**: All 88 story configs in the workspace passed validation, confirming that compact stories bypass the character limit on verbose sections and compile cleanly.
