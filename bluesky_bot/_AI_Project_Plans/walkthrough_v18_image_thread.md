# Compact Posting Mode & On-The-Fly Conversion Walkthrough

We have successfully implemented and verified **Compact Posting Mode** with **On-the-Fly Image Conversion** across the entire Bluesky bot pipeline. Rather than publishing a long 13-post text thread, this mode publishes exactly 4 posts (Hook, Claim, Reality, Verdict) as native text, and packages the remaining 9 details (Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Alethe, Aww, and Bro) into a single, high-fidelity dark-mode infographic card PNG. This image is attached to the 4th post (Verdict) with the full summaries contained in its Alt Text.

Importantly, **this works for both native compact stories and regular 13-post format stories**. If you run the posting scheduler with the `--compact` flag, it will automatically detect any missing visual card images and generate them *on-the-fly* before validation and posting.

---

## Changes Made

1.  **On-the-Fly Card Rendering Integration**:
    *   **`aletheia_bot.py`**: In `post_thread()`, if `compact` mode is active, the engine checks for the `{story_id}_info_card.png` image on disk. If it's missing (which occurs when posting a regular 13-post JSON story in compact mode), it automatically imports and invokes the visual rendering engine to generate the PNG on-the-fly.
    *   **`validate_batch.py`**: Added a `--compact` CLI argument. If validation is run in compact mode, and a story's card image does not exist, the validator generates it on-the-fly so the validation checklist passes cleanly.
    *   **`post_batch.py`**: Updated `validate_story_file()` to accept the `compact` flag, resolving the status from the CLI command and generating missing card images at validation time.
2.  **Live Post Scheduler GUI Option (`AletheiaLauncher.pyw`)**:
    *   Added a "Post in Compact Mode" checkbox to the **Live Post Scheduler** (the second card in the GUI layout) next to the "Continuous Watch Mode" toggle.
    *   When checked, the GUI automatically appends the `--compact` argument to the `validate_batch.py` and `post_batch.py` subprocess calls.

---

## Verification Results

### 1. On-the-Fly Conversion & Slicing Test
We tested this with a regular 13-post format JSON story `factcheck_bill_wilson_obituary.json` which did not have any pre-generated visual cards in `graph_png/`:
```powershell
.venv\Scripts\python.exe bluesky_bot/aletheia_bot.py --config bluesky_bot/stories/factcheck_bill_wilson_obituary.json --compact --dry-run
```
*   **Result**: 
    *   The posting engine correctly reported that the info card was missing and successfully logged: `Compact mode info card not found at ... Generating on-the-fly...`
    *   The card was dynamically generated and written to `graph_png/bill_wilson_obituary_info_card.png`.
    *   The output thread was successfully sliced to exactly **4 posts** (Post 1: Graph embed, Post 2: Link card embed, Post 3: standard text, Post 4: Compact summary card image embed).

### 2. Batch Validation Success
We ran the batch validator `bluesky_bot/validate_batch.py` inside the virtual environment:
*   **Result**: All 88 story configs in the workspace passed validation, confirming that compact stories bypass the character limit on verbose sections and compile cleanly.
