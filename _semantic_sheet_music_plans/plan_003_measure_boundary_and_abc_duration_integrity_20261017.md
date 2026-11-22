# Implementation Plan 003: Measure Boundary & ABC Duration Integrity Verification

**Date:** 2026-10-17  
**Target:** `e:\Vector Field Theory\VFT Docs\semantic_sheet_music_studio.html`  
**Parent Plans:** [plan_001_music_theory_song_engine_20261017.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_semantic_sheet_music_plans/plan_001_music_theory_song_engine_20261017.md), [plan_002_two_layer_music_and_vocal_engine_20261017.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_semantic_sheet_music_plans/plan_002_two_layer_music_and_vocal_engine_20261017.md)

---

## 1. Problem Statement
1. **Meter Spills & Bar Distortions**:
   - In 4/4 meter (`beatsPerBar = 8`), when syllables near the end of a measure were assigned quarter-note durations (duration 2) on strong accents or cadence notes, they spilled 1 eighth note over the barline without an ABC tie.
   - This caused measures to contain 9 eighth notes instead of 8, pushing the next measure out of alignment with the 4/4 pulse.
2. **Decimal ABC Duration Tokens**:
   - In multi-syllable words where unstressed syllables received half-eighth durations (`eighths = 0.5`), phrases ending with an odd half-eighth resulted in fractional rest durations like `closeRem = 1.5` or `2.5`.
   - The engraving loop directly appended `tok.abcDurStr` (`"1.5"`, `"2.5"`), producing invalid ABC tokens like `z1.5`, `[CEG]1.5`, and `C,1.5`.

---

## 2. Solutions Implemented

### A. Strict Measure Boundary Clamping for Syllables
- Added a measure remainder boundary check before assigning syllable durations:
  ```javascript
  const remInMeasure = beatsPerBar - (lineEighthsUsed % beatsPerBar);
  if (eighths > remInMeasure && remInMeasure > 0) {
      eighths = remInMeasure === 0.5 ? 0.5 : (remInMeasure >= 1 ? Math.floor(remInMeasure) : remInMeasure);
      abcDurStr = eighths === 0.5 ? '/2' : (eighths === 1 ? '1' : String(eighths));
  }
  ```
- **Musical Effect**: Syllables cleanly align to measure boundaries. Strong words in the following measure land directly on downbeats (Beat 1), preserving natural poetic and metric pulse.

### B. Unit Duration Formatters for ABC Rests & Chords
- Created `formatAbcRestUnits(eighths)`:
  - Decomposes any fractional duration into standard ABC rest tokens (e.g., `1.5` -> `"z1 z/2"`, `0.5` -> `"z/2"`, `2.5` -> `"z2 z/2"`).
- Created `formatAbcChordUnits(chordPrefix, eighths)`:
  - Decomposes any fractional duration into valid ABC note/chord tokens (e.g., `[CEG]` for `1.5` -> `"[CEG]1 [CEG]/2"`, `C,` for `1.5` -> `"C,1 C,/2"`).
- Updated turnaround rests and breath rests across all staves (`Lead`, `Strum`, `Bass`) to use these unit formatters.

### C. Metric Adaptation for Turnaround Comping
- Dynamically split turnaround comping measures based on `beatsPerBar`:
  - 4/4 meter: two 4-eighth chords (`[chord]4 [chord]4 |`) and bass root/fifth (`rb0 4 rb5 4 |`).
  - 3/4 meter: two 3-eighth chords (`[chord]3 [chord]3 |`) and bass root/fifth (`rb0 3 rb5 3 |`).

---

## 3. Node.js Verification Results
- Executed `test_engine.js` across challenging inputs:
  1. Standard poem (*"Where the mind is without fear..."*): All measures verified at exactly 8.0 eighths.
  2. Edge case multisyllabic stress test (*"Unbelievable extraordinarily complicated philosophical contemplation..."*): All measures verified at exactly 8.0 eighths.
  3. Metric change to 3/4 time: All measures verified at exactly 6.0 eighths.
- Zero decimal ABC tokens detected.
