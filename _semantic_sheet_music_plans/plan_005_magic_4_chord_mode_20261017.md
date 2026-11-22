# Implementation Plan 005: Magic 4 Chord Mode & Harmonic Progression Engine

**Date:** 2026-10-17  
**Target:** `e:\Vector Field Theory\VFT Docs\semantic_sheet_music_studio.html`  
**Parent Plans:** [plan_001](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_semantic_sheet_music_plans/plan_001_music_theory_song_engine_20261017.md), [plan_002](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_semantic_sheet_music_plans/plan_002_two_layer_music_and_vocal_engine_20261017.md), [plan_003](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_semantic_sheet_music_plans/plan_003_measure_boundary_and_abc_duration_integrity_20261017.md), [plan_004](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_semantic_sheet_music_plans/plan_004_vocal_stretch_and_sampler_streams_20261017.md)

---

## 1. Goal
Add a dedicated **Harmonic Progression / Chord Engine** selector featuring the iconic **Magic 4 Chords** ($I - V - vi - IV$) along with classic songwriting progressions, seamlessly integrated with:
1. Smooth diatonic voice-leading triads.
2. Bass downbeat root movement ($1 \to 5 \to 6 \to 4$).
3. Vocal melody chord-gravity attraction.
4. Vocal strum synchronization.

---

## 2. Progression Modes Supported

1. **`magic-4` (★ The Magic 4 Chords)**:
   - Major: $I - V - vi - IV$ ($C - G - Am - F$)
   - Minor: $i - VI - III - VII$ ($Am - F - C - G$)
   - The most ubiquitous and emotionally resonant pop progression in history ("Axis of Awesome", Journey, Beatles, U2, Adele).

2. **`anthem-4` (Epic Melancholy Anthem)**:
   - Major: $vi - IV - I - V$ ($Am - F - C - G$)
   - Minor: $i - iv - VII - III$
   - Minor-driven anthem progression ("Zombie", "Apologize", "Despacito").

3. **`doo-wop-4` (Classic 50s Doo-Wop)**:
   - Major: $I - vi - IV - V$ ($C - Am - F - G$)
   - Minor: $i - iv - VI - VII$

4. **`blues-turn` (Blues & Folk Turnaround)**:
   - Major: $I - IV - V - I$ ($C - F - G - C$)
   - Minor: $i - iv - v - i$ ($Am - Dm - Em - Am$)

5. **`canon-8` (Pachelbel Canon Loop)**:
   - Major: $I - V - vi - iii - IV - I - IV - V$

6. **`call-response` (Dynamic Antecedent / Consequent)**:
   - Adaptive Call ($I - V$) and Response ($IV - I$).

---

## 3. Metric Mapping Logic (2-Bar vs 4-Bar Phrases)

- If `targetBars === 4`:
  - 1 chord per bar:
    - Bar 1: Chord 1 ($I$)
    - Bar 2: Chord 2 ($V$)
    - Bar 3: Chord 3 ($vi$)
    - Bar 4: Chord 4 ($IV$)
- If `targetBars === 2`:
  - Call Line (Stanza line 1): Chords 1 & 2 ($I \to V$)
  - Response Line (Stanza line 2): Chords 3 & 4 ($vi \to IV$)
  - Together, every two lines form the complete 4-chord cycle!
- If `targetBars > 4`:
  - Loops the 4 chords cyclically across measures: `[1, 5, 6, 4, 1, 5, 6, 4]`.

---

## 4. UI Integration
- Add `<select id="progression-mode-select">` to the Band Conductor panel right beside "Text Strumming / Comping".
- Trigger `compileDocument()` on change.
- Display the progression roman numerals and chord names in the live telemetry and score staves.
