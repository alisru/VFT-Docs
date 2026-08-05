# Implementation Plan: 5-Word Judgement Mode with Terminal Info Card

We will implement a new mode called **5-Word Mode** (activated via a new `--five-word` flag). This mode runs the full Convergence SON model but restricts the generated narrative steps (the 13 posts) to exactly 5 words each, packing them dynamically into standard 300-character posts (~2 posts total) for Bluesky. 

In addition, it will generate a single unified **Five-Word Info Card** featuring all 13 steps rendered in a clean terminal-style log.

## Proposed Changes

### [Aletheia Launcher]

#### [MODIFY] [AletheiaLauncher.pyw](file:///E:/Vector%20Field%20Theory/VFT%20Docs/AletheiaLauncher.pyw)
* Add an "Enable 5-Word Mode" checkbox (`self.chk_five_word`) next to the "Enable Compact Mode" checkbox.
* Forward `--five-word` as a CLI argument if checked.

---

### [Evaluator Engine]

#### [MODIFY] [google_ai_studio_one_shot.py](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
* Add `--five-word` command line flag.
* Update `run_one_shot_evaluations` to accept a `five_word` parameter.
* If `five_word` is True:
  * Append strict directive to `formatting_rules` requiring each of the 13 posts to be exactly 5 words long.
  * Explicitly instruct Post 4 (Verdict) to be formatted as `stated [claim_coord] actual [real_coord] [pass/fail/neutral]`.
  * Inject `"five_word": true` into the generated story config JSON.

---

### [Card Generator]

#### [MODIFY] [image_card_generator.py](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/image_card_generator.py)
* Inside `generate_compact_info_card`, intercept `five_word` stories:
  ```python
  if thread_config.get("five_word") is True:
      _generate_five_word_card(subject, verdict_subtitle, posts, fonts, link, output_path.replace(".png", "_five_word.png"))
      return
  ```
* Implement `_generate_five_word_card(subject, subtitle, posts, fonts, link, output_path)`:
  * Creates a `1200 x 950` canvas.
  * Draws the header with the story title and coordinates.
  * Draws a single terminal container card with 13 vertical lines (color-coded by phase/persona).
  * Composites the QR code in the bottom right corner of the footer.

---

### [Validator & Posting Core]

#### [MODIFY] [aletheia_bot.py](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aletheia_bot.py)
* Add `pack_5word_posts(posts, max_len=300)` helper function to group 5-word lines using newlines.
* Accept `five_word=False` in `post_thread`.
* Enforce safety/isolation checks: prevent 5-word configs from being posted in normal/compact modes, and vice versa.
* If `is_five_word` is True, pack posts using `pack_5word_posts`.
* Attach BOTH the Trajectory Graph and the single Five-Word Info Card (`*_info_card_five_word.png`) to Post 1.

#### [MODIFY] [validate_batch.py](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/validate_batch.py)
* Add `--five-word` CLI argument.
* Add isolation validation: prevent mismatch between story config `"five_word"` metadata and run-time parameters.
* Use `pack_5word_posts` to group and validate character lengths when `is_five_word` is enabled.
* Verify that the unified `{story_id}_info_card_five_word.png` exists (generating it on-the-fly if missing).

#### [MODIFY] [post_batch.py](file:///E:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/post_batch.py)
* Add `--five-word` CLI argument.
* Forward `five_word` flag when invoking `post_thread`.

---

## Verification Plan

### Manual Verification
1. Open the Launcher (`AletheiaLauncher.pyw`) and verify that "Enable 5-Word Mode" appears.
2. Select a news story and run a dry-run evaluation with "Enable 5-Word Mode" and "Enable SON Mode" enabled. Verify that:
   * The generated text has exactly 13 posts, each containing exactly 5 words.
   * The draft config JSON is successfully created with `"five_word": true`.
3. Run the validator (`validate_batch.py --five-word`) to confirm it generates the unified terminal card on-the-fly.
4. Run a live post of the generated draft (`post_batch.py --live --five-word --files <file_name>`) and check the resulting Bluesky thread on the timeline to verify it formats correctly as 2 packed posts with the trajectory graph and the terminal-style info card attached to Post 1.
