# Implementation Plan 004: Vocal Stream Syllable Stretch & Sampler Architecture

**Date:** 2026-10-17  
**Target:** `e:\Vector Field Theory\VFT Docs\semantic_sheet_music_studio.html`  
**Parent Plans:** [plan_001](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_semantic_sheet_music_plans/plan_001_music_theory_song_engine_20261017.md), [plan_002](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_semantic_sheet_music_plans/plan_002_two_layer_music_and_vocal_engine_20261017.md), [plan_003](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_semantic_sheet_music_plans/plan_003_measure_boundary_and_abc_duration_integrity_20261017.md)

---

## 1. Core Architectural Separation: Two Independent Streams

### Stream 1: The Music Stream (The Backing Track / Sampler Loop)
- **Role**: Steady, continuous diatonic harmonic foundation ($4/4$ or $3/4$ meter grid).
- **Instruments**: Drums (steady beat / metronome), Bass (downbeat groove on 1 and 3), and optional backing Pad/Organ.
- **Rests & Breaks**: The music stream keeps the pulse moving through breath pauses and stanza turnarounds without stopping.

### Stream 2: The Vocal Stream (The Singer & Strum Hits)
- **Role**: Word-driven vocal chops with keyed chord strums matching speech and singing duration.
- **Instruments**: Vocal Lead + Strum Comping (acoustic guitar, piano, or harp).
- **The Golden Invariant**: **Zero strumming without singing.**
  - On breath rests and stanza breaks, the Strum track is **completely silent** (`z` in the score, no audio triggers).
  - Strums only strike when an actual syllable is uttered.

---

## 2. Syllable Stretch Engine (From Spoken Speech to Slow Singing)

### The Problem
- Currently, words with more than 2 syllables (e.g. *Hallelujah* $\to$ `Hal-le-lu-jah`) force interior syllables into rigid $0.5$ eighth notes ($16^{\text{th}}$ notes $= 125\text{ms}$ at 120 BPM).
- Words that should feel slow, emotional, or sung fly by like a rapid auctioneer.

### The Solution: 3-Tier Syllable Stretch Model

1. **Delivery Style Selector (UI Control)**:
   - **`Spoken Prosody`**: Snappy speech cadence ($0.5$ to $1$ eighth note per syllable). Good for rhythmic poetry, rap, or conversational text.
   - **`Lyrical Sing` (Default)**: Normal song phrasing. Syllables default to $1$ eighth note; strong action/stress words receive $2$ eighths (quarter notes).
   - **`Ballad / Gospel Stretch`**: Wide, expressive singing. Syllables get $2$ eighths (quarter notes); cadence notes get $4$ eighths (half notes). *Hal-le-lu-jah* unfolds as `2 - 2 - 2 - 4` across two full measures!
   - **`Chant / Hymn`**: Sustained sacred/ambient pacing ($2$ to $4$ eighths per syllable).

2. **Phonetic & Punctuation Vowel Weighting**:
   - Vowel openness: Diphthongs and open vowels (`ah`, `oh`, `oo`, `ee`, `lu`, `jah`, `high`, `free`) receive an automatic $+1$ stretch boost over clipped consonant endings (`bit`, `it`, `up`).
   - Punctuation / Capitalization: Exclamation marks (`!`) and expressive words get held.

3. **Inline Text Stretch Syntax (`~` or `_`)**:
   - Users can write `Hallelujah~` or `Hal~le~lu~jah~~` in the source text to manually stretch specific syllables or words to whole beats.

4. **Sampler Gate Synchronization**:
   - The strumming instrument's envelope and audio duration lock directly to the stretched syllable duration:
     - $1$ eighth note $\to$ crisp strum chop ($250\text{ms}$).
     - $2$ eighth notes $\to$ sustained acoustic ring ($500\text{ms}$).
     - $4$ eighth notes $\to$ blooming chord with harmonic decay ($1000\text{ms}$).

---

## 3. Implementation Steps

1. **Silence Strums on Rests**:
   - In `compiledTokens.forEach`: When `tok.isRest`, engrave `formatAbcRestUnits(tok.eighths)` for Strum instead of comping chords.
   - In `playBreakGroovePocket`: Remove `spec.bandRole === 'STRUM'` trigger so only Drums/Bass keep the pocket.
2. **Add Vocal Delivery / Stretch Control to UI**:
   - Add `<select id="vocal-stretch-select">` with options:
     - `spoken` (Speech Pace)
     - `lyrical` (Lyrical Sing)
     - `ballad` (Gospel / Ballad Stretch)
     - `hymn` (Sustained Chant)
3. **Implement Dynamic Syllable Duration Calculator**:
   - Replace the hardcoded `eighths = lt.sylCount > 2 ? 0.5 : 1` with a context-aware function `computeSyllableDuration(lt, deliveryMode, lineEighthsUsed, beatsPerBar)`.
4. **Update Sampler Strum Triggering**:
   - Set strum envelope release and duration proportionally to the stretched syllable.
5. **Verify in Node & Browser**:
   - Run verification test with *"Hallelujah"* in `test_engine.js` to ensure clean measure boundaries and natural song pacing.
