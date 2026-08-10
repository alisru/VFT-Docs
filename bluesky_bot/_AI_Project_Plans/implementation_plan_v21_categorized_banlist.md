# Implementation Plan - Categorized Topic Banlist and UI Integration

Restructure the topic banlist system to support dictionary-mapped categories in `banned_topics.json`. Update the harvester's keyword resolver to parse category names (expanding them into keyword lists) and raw keywords. Integrate this dynamically into the Aletheia Launcher Tkinter console UI.

## User Review Required

> [!NOTE]
> We will update `banned_topics.json` to be a categorized map.
>
> `AletheiaLauncher.pyw` will read this file on startup and dynamically pre-populate the "Exclude Topics" field with all category names (`travel, sport, entertainment, obituaries, gardening`), allowing you to enable or disable categories by typing/removing their names.

## Proposed Changes

### Bluesky Bot

#### [MODIFY] [banned_topics.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/banned_topics.json)
Convert the flat JSON array to a category-to-keywords dictionary including `"tour de france"` under `"sport"`.

#### [MODIFY] [harvest_candidates.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvest_candidates.py)
- Refactor `load_banned_topics()` to return a dictionary of categories.
- Update the keyword initialization logic to split the input of `--banned-topic` (Exclude Topics), check if each term matches a category name (and expand it if it does), and treat non-matching terms as custom raw keywords.

#### [MODIFY] [google_ai_studio_one_shot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
- Refactor `load_banned_topics()` to match `harvest_candidates.py` returning a dictionary of categories.
- Update `harvest_news()` keyword parsing to use the categorized dual-resolver logic.

#### [MODIFY] [AletheiaLauncher.pyw](file:///e:/Vector%20Field%20Theory/VFT%20Docs/AletheiaLauncher.pyw)
- Add a helper function to read the categories from `banned_topics.json` on startup.
- Populate the `self.ent_banned` entry widget with the categories dynamically, defaulting to all of them if the file fails to load.

---

## Verification Plan

### Manual Verification
- Verify the console launcher starts up correctly and pre-populates the "Exclude Topics" field dynamically with `"travel, sport, entertainment, obituaries, gardening"`.
- Run the test suite `python tests/test_banlist.py` (which we will update to test the categorized mapping and keyword expansion resolver).
- Check that omitting `"sport"` from custom test queries leaves `"tour de france"` unblocked, while including it blocks it.
