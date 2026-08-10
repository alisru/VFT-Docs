# Implementation Plan - Dynamic Topic Banlist and Regex Matching

Implement a robust, regex-based topic banlist system that loads from a local configuration file `banned_topics.json`. This fixes false-positive matches (such as `"sport"` blocking `"transportation"`) by using word boundaries (`\b`) and adds comprehensive default keywords for sport, travel, entertainment, and obituaries.

## User Review Required

> [!NOTE]
> We will create a local configuration file `banned_topics.json` in the `bluesky_bot` directory. If it doesn't exist, it will auto-populate with our comprehensive defaults so you can easily edit it going forward.
>
> We will use regular expression word boundary matching (`\bkeyword\b`) to prevent substring collisions, which was previously a major source of false-positive filtering.

## Proposed Changes

### Bluesky Bot

#### [NEW] [banned_topics.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/banned_topics.json)
Create the new JSON file containing the default banned keywords for sport, travel, entertainment, and obituaries.

#### [MODIFY] [harvest_candidates.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvest_candidates.py)
- Replace the static CLI default string for `--banned-topic` with `None`.
- Implement `load_banned_topics()` to dynamically read from `banned_topics.json` or write defaults if it doesn't exist.
- Modify `is_banned()` to perform regular-expression-based word boundary checks (`\b`) rather than substring matching.
- Update the initialization of `banned_keywords` to load from the file and merge any optional CLI `--banned-topic` overrides.

#### [MODIFY] [google_ai_studio_one_shot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
- Replace the static CLI default string for `--banned-topic` with `None`.
- Update `harvest_news()` and `is_banned()` functions inside this file to match the new dynamic loading and regex word boundary behavior.
- Ensure that if `args.banned_topic` is not provided on CLI, it retrieves topics from the same `banned_topics.json`.

---

## Verification Plan

### Manual Verification
- Run a dry-run test check on `is_banned` logic to verify that:
  - `"transportation"` is **NOT** blocked by the `"sport"` or `"sports"` keyword.
  - `"sports"` or `"sport"` is blocked.
  - Obituaries containing `"dies at"` or `"obituary"` are blocked.
  - Travel or entertainment keywords are blocked.
- Verify `banned_topics.json` is successfully written upon first execution of `harvest_candidates.py`.
