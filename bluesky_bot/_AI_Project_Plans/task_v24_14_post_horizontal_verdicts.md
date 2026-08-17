# Task List - 14-Post Multi-Aspect Audits Mode

- [x] Update `google_ai_studio_one_shot.py` to output 14 posts in multi-aspect mode, setting Post 5 (index 4) as the sub-audits breakdown.
- [x] Update `transpose_flat_to_json()` in `google_ai_studio_one_shot.py` to handle 14 posts and parse aspects.
- [x] Update validation checks in `post_batch.py` and `aletheia_bot.py` to allow 14 posts in multi-aspect mode.
- [x] Update `image_card_generator.py` sections mapping to dynamically shift indices if `len(posts) == 14`.
- [x] Update `_generate_verdict_card()` in `image_card_generator.py` to draw the 5th section as a horizontal full-width box beneath the 2x2 grid.
- [x] Run a batch run and verify the generated infographic card visually.
