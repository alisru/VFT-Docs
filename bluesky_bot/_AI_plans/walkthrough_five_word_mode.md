# Walkthrough - Five-Word Judgement Mode & Terminal Info Card

We have successfully implemented the new **5-Word Judgement Mode** and its high-contrast terminal-style infographic card layout.

## Changes Made

### 1. GUI Launcher Checkbox (`AletheiaLauncher.pyw`)
* Added a new `"Enable 5-Word Mode"` checkbox (`chk_five_word`) alongside `"Enable Compact Mode"`.
* Configured the GUI command-builder to automatically append `--five-word` when running harvesting or posting pipelines.

### 2. LLM Instruction Overrides (`google_ai_studio_one_shot.py`)
* Implemented CLI `--five-word` argument mapping.
* Intercepted formatting instructions to force the model into 5-word limits for each of the 13 posts.
* Formatted the Verdict post (post 4) to output exactly: `stated [stated_u/psi] actual [real_u/psi] [verdict]`.
* Excluded adding the grounding source URL directly to the post texts to preserve the strict 5-word boundary; instead, it is set directly in the JSON configuration's `"grounding_url"` metadata key.

### 3. Terminal-Style Info Card (`image_card_generator.py`)
* Implemented `_generate_five_word_card` to layout all 13 micro-steps in a single terminal-style layout.
* Cleaned up raw persona prefixes systematically from generated lines.
* Included vertical divider at `x = 780` with right-side diagnostic logs (Status, Mode, Verdict outcome) and scanner instructions for the verified source QR code.
* Defined `_generate_qr_code` using the standard `qrcode` library to render a high-contrast themed QR code.

### 4. Dynamic Packing and Posting (`aletheia_bot.py`)
* Added `pack_5word_posts(posts)` to optimally pack the 13 lines into ~2 posts of under 300 characters using newlines (`\n`).
* Configured image uploader and posting logic to route five-word card outputs (`*_info_card_five_word.png`) to the first thread post.

### 5. Scheduling and Validation checks (`validate_batch.py` & `post_batch.py`)
* Integrated `--five-word` validation check ensuring normal stories are not posted/validated under five-word flags and vice-versa.
* Verified info card rendering on-the-fly during validation phases.

## Testing and Verification
1. **Pre-flight Validation**: Validated `factcheck_test-five-word.json` with the `--five-word` flag successfully.
2. **On-the-fly Generation**: Successfully rendered the unified terminal-style info card image `test-five-word_info_card_five_word.png` (copied to your artifact folder for review).
3. **Dry-Run Scheduler**: Executed mock posting scheduler, verifying that the 13 posts are packed into exactly 2 posts under 300 characters, containing the graph and terminal card attachments.
