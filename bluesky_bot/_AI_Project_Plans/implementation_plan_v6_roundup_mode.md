# Roundup Mode: Multi-Outlet Coverage Audit
## v2 — Post-Generation Consolidation Architecture

## Goal
When multiple outlets cover the same macro-event, post **one** roundup thread that judges each outlet's framing separately, rather than either flooding the feed with duplicates or silently dropping them.

---

## Pipeline (Revised)

```
1. harvest_candidates.py       Exact-match dedup only (URL / title / slug)
                               Different outlets on same event → all queued ✓
                               Same article seen twice → blocked ✗

2. google_ai_studio_one_shot.py  Evaluates each candidate individually
                               → individual factcheck_*.json in stories/darkroom/
                               → rebuild_registries promotes to stories/

3. [NEW] consolidate_roundups.py  Post-generation pass on stories/ (draft folder)
                               Groups stories by macro_event / actor overlap
                               If ≥2 stories in a group → merge into roundup_*.json
                               Archives individual stories to stories/consolidated/

4. rebuild_registries.py       Picks up roundup_*.json alongside normal factcheck_*.json
                               Roundup stories have identical structure → no changes needed

5. post_batch.py               Posts everything as usual
```

---

## consolidate_roundups.py — Design

### Grouping Logic
Three signals, checked in priority order:

1. **macro_event match** (exact, normalised): Stories sharing the same non-empty `macro_event` label → same group
2. **Actor overlap**: Stories sharing ≥2 actors (within 72 hours) → same group
3. **Keyword overlap**: Stories whose subject shares ≥3 anchor words (≥5 chars, non-stopword) AND were filed within 48 hours → same group

### What Happens to Individual Stories
- Stories that get **consolidated** → moved to `stories/consolidated/` (not deleted, archived)
- The individual stories' VFT coordinates are preserved in the roundup's `outlets[]` array
- If a group has only 1 story → leave it alone, post individually as normal

### Roundup Story JSON Structure
```json
[{
  "id": "roundup_burnham-makerfield-byelection",
  "subject": "Media Roundup: Burnham wins Makerfield by-election",
  "roundup": true,
  "outlets": [
    {
      "name": "BBC",
      "url": "https://bbc.co.uk/...",
      "subject": "Burnham romps to victory...",
      "claim_u": 1.0, "claim_psi": 1.0,
      "real_u": 0.8, "real_psi": 0.8,
      "context_post": "post 5 text from individual story (context paragraph)"
    },
    ...
  ],
  "claim_u": ...,   "claim_psi": ...,   // pack meta-verdict
  "real_u":  ...,   "real_psi":  ...,
  "macro_event": "Makerfield By-election",
  "actors": [...],  // union of all outlet actors
  "mode": "root",
  "posts": [...],   // 13 posts — written by AI call
  "status": "COMPLETED DRY RUN",
  ...
}]
```

### Thread Format (13 posts)
| Posts | Content |
|-------|---------|
| 1 | Hook: "N outlets covered [EVENT]. Their framings diverge." + hashtags |
| 2–(N+1) | Per-outlet block: outlet name, stated claim, VFT coordinate (max 4 outlets) |
| N+2 | Context: what actually happened |
| N+3 | Synthesis verdict: who was closest to reality |
| N+4 | Bright Side / what good coverage looked like |
| N+5 | Breakdown & Plane Error — framing errors across the pack |
| N+6 | Social Physics Analysis — pack dynamics |
| N+7 | Trajectory (meta-coordinate of the whole pack) |
| N+8 | Unavoidable Truth/Lie |
| 13 | Alethekanon / Awwthekanon / Brothekanon |

For 2 outlets (posts 2–3): 11 analysis posts remain → fits exactly.
For 4 outlets (posts 2–5): 8 analysis posts remain → still fits.

### AI Call for Roundup Thread
- Input: structured JSON with per-outlet coordinates + subjects (NOT raw article text)
- Much smaller prompt than a regular evaluation
- Uses existing `call_agnes_api` or `genai_client`
- Single call produces 13 posts

---

## Files

| File | Action |
|------|--------|
| `consolidate_roundups.py` | NEW — main consolidation script |
| `instructions/thread_formatting_roundup.md` | NEW — 13-post roundup format spec |
| `harvest_candidates.py` | DONE — topic saturation removed, exact dedup only |
| `rebuild_registries.py` | No change — already handles any `factcheck_*.json` |
| `post_batch.py` | No change — roundup is just another story |

---

## Open Questions (resolved)
- ✅ Dedup strategy: exact-only at harvest, topic grouping post-generation
- ✅ Individual stories that get consolidated → archived not deleted
- Min outlets to trigger roundup: **2** (any 2 outlets = roundup)
- Max outlets per roundup: **4** (fits in 13 posts)
- Lonely single-outlet stories: **posted individually** as before
- Pipeline step: **manual CLI call** (`python consolidate_roundups.py`) between step 2 and step 4
