# Implementation Plan 001: Music Theory Song Construction Engine

**Date:** 2026-10-17  
**File Under Work:** [`semantic_sheet_music_studio.html`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/semantic_sheet_music_studio.html)  
**Location:** `e:\Vector Field Theory\VFT Docs\_semantic_sheet_music_plans\plan_001_music_theory_song_engine_20261017.md`

---

## 1. Context & Objectives
The semantic sheet music studio translates text into musical scores and audio using Vector Field Theory (Qqci 7-planes and AEC action/effect grammar). While the basic voice-leading smoothing and single master clock are in place, the composition engine currently violates foundational principles of song construction:
1. **Harmonic Rhythm**: Chords change randomly on every syllable/word.
2. **Tonal Center**: No stable home key; modes and roots hop erratically.
3. **Metric Prosody**: Syllable lengths are chained serially without aligning stressed syllables to downbeats.
4. **Phrase Structure & Cadences**: Lines end arbitrarily without call-and-response or cadential resolution.
5. **Harmonic Consonance**: Melodic notes clash dissonantly with chords on strong beats.
6. **Voice Leading**: Accompaniment jumps in parallel block triads.
7. **Mixer Controls**: Band instruments lack independent channel strips (volume, mute, solo).

This plan fixes these violations in sequential order.

---

## 2. Sequence of Implementation Phases

### Phase 1: Phrase-Level Harmonic Rhythm & Chord Progressions
- **Tonal Center**: Establish a stable piece-wide tonic key ($I$) anchored in the document's dominant plane, with a standard diatonic scale ($I, ii, iii, IV, V, vi, vii^\circ$).
- **Harmonic Rhythm**: Fix chord changes to musical measure boundaries (1 chord per 2 beats or 1 chord per bar in 4/4).
- **Functional Progressions**: Build 2-bar or 4-bar phrase progressions derived from the poetic line's planes (e.g. $I - V - vi - IV$, $I - IV - V - I$, $vi - IV - I - V$).
- **Coloring**: Individual semantic word planes tint or modify the underlying chord (7ths, 9ths, sus4) instead of destroying the root.

### Phase 2: Metric Prosody & Downbeat Alignment
- **Stress-to-Meter Mapping**: Align content words (verbs, nouns, stressed syllables) to primary metric downbeats (beats 1 & 3).
- **Pickups (Anacrusis)**: Place unstressed function words (*the, of, to, in, and*) on weak upbeat eighths (beat 4&).
- **Bar Completion**: Each line of poetry rounds out to an integer number of measures (e.g., 2 or 4 bars = 8 or 16 eighths) with a breath rest filling remaining beats.

### Phase 3: Phrase Structure & Cadences (Call & Response)
- **Antecedent Phrases (Calls)**: Odd lines (1, 3) end on an open half cadence (scale degree 2 or 5, over $V$ or $ii$).
- **Consequent Phrases (Responses)**: Even lines (2, 4) end on an authentic cadence (scale degree 1 or 3, over $I$).
- **Stanza Breaks**: Full tonic resolution and extended resting space.

### Phase 4: Melody-to-Harmony Consonance on Strong Beats
- On beats 1 and 3, snap or attract the melody note from `computeFlowingStep` to the nearest chord tone (root, 3rd, 5th) of the currently sounding harmony.
- On weak off-beats, permit passing tones, suspensions, and expressive tensions that resolve into the next beat.

### Phase 5: Smooth Accompaniment Voice Leading
- Replace parallel root-position triad leaps with inverted voicings (root, 1st inversion, 2nd inversion) that minimize voice motion between consecutive chords.
- Bass line plays root on downbeat, 5th or passing tones on secondary beats, moving in contrary motion to the melody.

### Phase 6: Multi-Track Mixer & Channel Controls
- Add a dedicated Mixer strip in the Band Conductor toolbar:
  - Lead Vocal / Solo: Volume Slider (0-100%), Mute, Solo.
  - Rhythm Strum (Piano/Guitar): Volume Slider, Mute, Solo.
  - Bass (Cello/Bass): Volume Slider, Mute, Solo.
  - Drums & Percussion: Volume Slider, Mute, Solo.
- Connect each channel's gain and mute state directly into the Web Audio audio bus routing.

---

## 3. Verification & Validation Steps
1. **Compilation Validation**: Ensure ABC score compiles cleanly without measure overflows or bar-line mismatches.
2. **Harmonic Consistency Check**: Verify chords change on bar/half-bar boundaries and voice leading remains within vocal/instrument ranges.
3. **Audio Playback Test**: Verify the Web Audio graph plays lead, strum, bass, and drums with independent volume/mute controls.
4. **Browser Syntax & Runtime Check**: Run headless Node syntax and logic check with mock DOM.
