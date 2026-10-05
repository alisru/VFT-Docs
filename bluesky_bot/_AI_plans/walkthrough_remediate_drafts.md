# Walkthrough - Manual Remediation of Draft Stories

## Summary
Remediated all 17 draft stories in `bluesky_bot/stories/` that were originally generated without Spiritual Mode or Multi-Aspect Audits.

## Remediations Applied
1. **Multi-Aspect Audits (`aspects` and Post 4 `Sub-Audits Breakdown:`)**:
   - Synthesized structured sub-audits across distinct actors/aspects for the 15 stories missing them (with precise `(u, psi)` coordinates, PASS/FAIL/COND verdicts, and concise reasons under 60 characters).
   - Formatted and inserted dedicated `Sub-Audits Breakdown:` bullet posts at index 4 of `posts`.
   - Populated the structured `"aspects"` list and set `"multiAspect": true` on each story JSON.
2. **Spiritual Audits (`Spirithekanon:`)**:
   - Evaluated the ethical and systemic tensions of each story.
   - Selected authentic, verified canonical passages (Tao Te Ching, Isaiah, Proverbs, Luke, Psalm, James, Ecclesiastes, Nehemiah, Deuteronomy, Matthew, John).
   - Appended a dedicated `Spirithekanon:` post (strictly < 280 characters) to all 17 stories.
3. **Card Generator Support**:
   - Fixed `image_card_generator.py` to properly recognize 15-post threads with both multi-aspect sub-audits and spiritual posts.
4. **Registry & Graph Synchronization**:
   - Rebuilt stories registries via `rebuild_registries_son.py`, successfully updating all indices and pre-generating trajectory graphs and split cards.

## Verification Results
- All 25 current draft stories in `bluesky_bot/stories/` now consistently have:
  - `Posts: 15`
  - `Spiritual: True`
  - `Aspects: True`
  - `SubAuditPost: True`
- Pre-flight card generation tests passed with 0 character violations.
- Running AletheiaLauncher processes were not touched or interrupted.
