# Implementation Plan - Multi-Aspect Convergence Test Audits (14-Post Edition with Horizontal Card Layout)

The goal is to implement multi-aspect and multi-actor audits as a **new, optional 14-post mode** (`--multi-aspect`). When enabled, a new step (Post 5) is inserted into the thread detailing the sub-audits breakdown with at least a line of reasoning and coordinates for each. In compact mode, this new step is rendered on the first info card (Verdict Card) as a **full-width horizontal section spanning both columns directly beneath the 2x2 grid**, keeping the visual design balanced.

## User Review Required

> [!IMPORTANT]
> - **14-Post Thread length**: When `--multi-aspect` is active, the thread length is exactly **14 posts** (Post 5 is the Sub-Audits Breakdown). When disabled, standard threads remain exactly 13 posts.
> - **Horizontal Sub-Audits Section**: On the Verdict Card, the standard Hook/Claim/Reality/Verdict sections will render in their balanced 2x2 layout. Underneath them, the Sub-Audits Breakdown will draw as a full-width horizontal block spanning the entire width of the card.

---

## Proposed Changes

### 1. Bot Command Line Evaluator

#### [MODIFY] [`google_ai_studio_one_shot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
- Pass `use_multi_aspect` flag into `run_one_shot_evaluations()`.
- Update `expected_len` to `28` and total posts to `14` if both `use_son` and `use_multi_aspect` are True.
- Update `output_format` instructions:
  - Define Post 5 (index 4) as the new dedicated **Sub-Audits Breakdown** post with at least a line of explanation for each aspect.
  - Exclude character limit check for Post 5 in compact mode.
  - Update example JSON to have 14 posts, inserting the sub-audits post.
- Update `transpose_flat_to_json()` to support 14 posts and parse the aspects array.

### 2. Validation & Scheduler

#### [MODIFY] [`post_batch.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/post_batch.py)
- Update validation checks (`validate_story_file`) to allow exactly 14 posts if `"aspects"` is present in the configuration.
- Pack the first 4 posts (`posts[:4]`) as standard text for posting to Bluesky.

#### [MODIFY] [`aletheia_bot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aletheia_bot.py)
- Allow `len(posts) == 14` if `multi_aspect` is enabled in `post_thread()`.

### 3. Image Card Generator

#### [MODIFY] [`image_card_generator.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/image_card_generator.py)
- Support `len(posts) < 13` check to allow 14 posts.
- If `len(posts) == 14`, dynamically shift sections 5-10 and personas 11-13 indices by +1.
- In `_generate_verdict_card()`:
  - If a 5th section is present (the Sub-Audits Breakdown), wrap its text to full-width (`drawable_w - 40`).
  - Calculate its height `sub_audits_h`.
  - Draw it as a rounded rectangle spanning from `x_left` to `x_right` directly under the 2x2 grid (at `y = grid_start_y + grid_h + card_gap`).
  - Offset the footer position and adjust final image height accordingly.

### 4. Launcher Console GUI

#### [MODIFY] [`AletheiaLauncher.pyw`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/AletheiaLauncher.pyw)
- Ensure the checkbox maps correctly and passes `--multi-aspect` to the subprocess run args.

---

## Verification Plan

### Automated Tests
- Run `tests/test_banlist.py` to confirm compile safety.
- Run a dry-run batch call with `--multi-aspect` enabled on the OpenAI cyber model story.
- Verify that the generated image card `factcheck_openai_daybreak_cyber_model_2026_info_card_verdict.png` draws the horizontal sub-audits block underneath the 2x2 grid.
