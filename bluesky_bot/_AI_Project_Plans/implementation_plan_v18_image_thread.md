# Compact Posting Mode (Post 4+ Image Summary)

This plan introduces a new, optional compact posting path to the Bluesky posting engine. Rather than publishing all 13 posts in a long text thread, this path posts the first 4 posts (Hook, Claim, Reality, Verdict) as native text, and renders the remaining 9 posts (Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, and the three persona reactions) into a single, high-fidelity dark-mode infographic card. This image is attached to the 4th post (Verdict), resulting in a clean, professional, and visually stunning 4-post thread on the timeline.

## Proposed Changes

### 1. API Prompt Adaptations

When `--compact` is passed to `google_ai_studio_one_shot.py`:
1.  **System Instruction Modification**:
    *   We will modify the hard limit text. Instead of enforcing 270 characters on all posts, we instruct the model:
        `"CRITICAL: Posts 1 to 4 (items 0 to 3 in the posts array) MUST be under 260 characters (hard limit) as they are posted as text. Posts 5 to 13 (items 4 to 12 in the posts array) have NO character limits and should be highly verbose, comprehensive, and detailed (typically 400-800 characters each) because they will be rendered into a high-fidelity visual image card."`
2.  **Formatting Rules Prepending**:
    *   We will dynamically prepended a `COMPACT MODE DIRECTIVE` block to the top of `formatting_rules` at runtime:
        ```markdown
        === COMPACT MODE DIRECTIVE ===
        - Posts 1 to 4 (indices 0 to 3: Hook, Claim, Reality, Verdict) will be posted as standard text on Bluesky. They MUST be kept strictly under 260 characters each.
        - Posts 5 to 13 (indices 4 to 12: Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Alethekanon, Awwthekanon, Brothekanon) will be rendered into an image. They have NO character limits. They MUST be highly verbose, comprehensive, and detailed (typically 400-800 characters each) to explain the concepts fully. DO NOT compress or shorten them.
        ```
3.  **JSON Dictionary Entry**:
    *   We will add `"compact": true` to the dictionary written to disk. This flags the file as a compact thread configuration throughout the remaining pipeline.

---

### 2. Infographic Card Design System

 we will implement a custom rendering engine using the `Pillow` library in Python to build a vertically structured dark-mode infographic card.

*   **File**: [NEW] [image_card_generator.py](file:///E:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/image_card_generator.py)
*   **Dimensions**: Width 1000px, Height dynamically computed via a two-pass layout engine.
*   **Aesthetics**:
    *   *Canvas Background*: Dark Slate (`#0B0F19`)
    *   *Card Background*: Slate Navy (`#141D2F`)
    *   *Borders / Accents*: Dark Gray (`#25354F`)
    *   *Accent Strips*: Soft Teal (`#38BDF8`) for Context, Emerald (`#10B981`) or Rose (`#EF4444`) for Nuance, Purple (`#C084FC`) for Breakdown, Light Blue (`#60A5FA`) for Social Physics, Magenta (`#F472B6`) for Trajectory, Orange (`#F59E0B`) for Unavoidables.
    *   *Persona Boxes*: High-contrast card panels for Alethekanon, Awwthekanon, and Brothekanon with branded borders.
*   **Typography**: Loads Segoe UI (`segoeui.ttf`) or Arial (`arial.ttf`) for body text, Consolas (`consola.ttf`) for code/verdict lines.

---

### 3. Pipeline Integrations

#### [MODIFY] [rebuild_registries.py](file:///E:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/rebuild_registries.py) & [rebuild_registries_son.py](file:///E:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/rebuild_registries_son.py)
*   Detect `"compact": true` in the staging story config dictionary.
*   If true, invoke `image_card_generator.generate_compact_info_card(...)` to render and save `{slug}_info_card.png` to `graph_png/` before promoting the JSON to the `stories/` directory.

#### [MODIFY] [validate_batch.py](file:///E:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/validate_batch.py)
*   Parse `"compact"` key from story JSON.
*   If `"compact"` is True:
    *   Run `pack_posts` and the character limit check (`len(post) > 299`) **only** for the first 4 posts (`posts[0:4]`). Skip limit validation for posts 4 to 12.
    *   Validate that *both* `{slug}_graph.png` and `{slug}_info_card.png` exist in `graph_png/`.

#### [MODIFY] [aletheia_bot.py](file:///E:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/aletheia_bot.py)
*   Read `"compact"` parameter from story configuration.
*   In `post_thread`:
    *   If `compact` is active:
        *   Upload the staging `{slug}_info_card.png` from `graph_png/` as an image embed.
        *   Slice the published `final_posts` list to only the first 4 posts.
        *   Attach the info card embed to the 4th post (Part 4, Verdict, index 3).
        *   Concatenate posts 4-12 as the image's Alt Text to ensure searchability and accessibility.

#### [MODIFY] [post_batch.py](file:///E:/Vector%20Field%20Theory%20VFT%20Docs/bluesky_bot/post_batch.py)
*   Forward the `--compact` flag during watch processing, though it will resolve automatically from the config JSON.

---

## Verification Plan

### Automated / Local Rendering Tests
*   We will write a test runner `bluesky_bot/tests/test_info_card.py` that reads `factcheck_andy_burnham_dog.json`, artificially sets `"compact": true`, generates the infographic card, and saves it.
*   We will visually inspect the output PNG to verify typography and panel styles.

### Dry-Run Verification
*   Execute `google_ai_studio_one_shot.py --compact --rss 1` to generate a new verbose candidate, compile it, stage its graph/card, promote it, and verify that validation passes and a dry-run post outputs a 4-post text thread with the card attached.
