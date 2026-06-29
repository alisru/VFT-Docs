# Topic-Level Deduplication for Harvest Pipeline

## Goal
Prevent the bot from flooding the timeline with a dozen stories all about the same event at the same moment in time. Allow legitimate developing-story coverage where new angles emerge over time, but suppress near-identical "same event, same day" coverage.

## The Problem Illustrated
Currently, `burnham_makerfield_win.json`, `burnham_makerfield_departure.json`, `burnham_makerfield_audit.json`, `burnham_manchester_exit.json`, `burnham_labour_leadership.json`, etc. — all on the same 2-3 day window — pass deduplication because their URLs are different. The URL-level check is necessary but not sufficient.

## Design Principle
**Same event + same 48hr window + same lead actors → skip.**
**Same event + 7+ days later + meaningfully new angle → allow.**

This is a time-windowed actor/topic frequency throttle, not a hard duplicate block.

---

## What We're Building

### 1. `build_actor_topic_index()` (in `harvest_candidates.py`)
Load all live + draft stories sorted by `mtime`. Build an in-memory index:

```python
topic_event_history = [
    {
        "actors": ["Andy Burnham", "Keir Starmer"],
        "macro_event": "Makerfield By-election",
        "topic": "UKPol",
        "mtime": 1719000000.0,
    },
    ...
]
```

### 2. `is_topic_saturated(text, title, actors_hint=None)` (new function)
Given a candidate's title/text and optionally its known actors (e.g. extracted from the post text), check:

1. **Actor overlap + recency throttle**: If ≥2 known actors appear in any existing story from the last 48 hours → soft block (skip).
2. **Macro-event saturation**: If a macro_event string appears verbatim in the last 5 stories AND the most recent was < 72 hours ago → soft block.
3. **Title keyword overlap**: Extract top 3-4 "anchor words" (non-stopwords ≥6 chars) from the headline. If ≥3 of them appear in any story headline from the last 48 hours → soft block.

If none of those trigger → allow.

### 3. Integration in `is_duplicate_story()`
After the existing checks (URL, exact title, ID), add:
```python
if is_topic_saturated(text, title):
    print(f"  -> Topic/actor saturation detected! Skipping...")
    return True
```

---

## Time Windows
| Check | Window | Threshold |
|-------|--------|-----------|
| Actor overlap | 48 hours | ≥2 shared actors |
| Macro-event count | 5 stories in 72 hours | ≥5 same macro_event label |
| Headline keyword overlap | 48 hours | ≥3 of top 4 anchor words match |

These are conservative to avoid false positives. The 48hr window means developing stories (new angle next day) are still caught, but a story with 3 new developments across a week all pass cleanly.

---

## What This Does NOT Do
- Does not block breaking news on a topic that hasn't been covered recently (e.g. first Burnham story after a week gap → always allowed)
- Does not require AI to classify topic similarity
- Does not delete existing stories

---

## Files Changed
- `harvest_candidates.py`:
  - Add `build_actor_topic_index()` (runs once at startup)
  - Add `is_topic_saturated(text, title)` helper
  - Add call to `is_topic_saturated()` inside `is_duplicate_story()`

---

## Open Questions
None — the logic is purely local and deterministic.

## Verification
Run `harvest_candidates.py --bsky 10` in dry mode, confirm suppression messages appear for duplicated topic/actor combos, confirm new-angle stories still pass.
