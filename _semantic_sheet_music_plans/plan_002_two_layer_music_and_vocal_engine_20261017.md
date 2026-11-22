# Implementation Plan 002: Two-Layer Music & Vocal Architecture

**Date:** 2026-10-17  
**File Under Work:** [`semantic_sheet_music_studio.html`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/semantic_sheet_music_studio.html)  
**Location:** `e:\Vector Field Theory\VFT Docs\_semantic_sheet_music_plans\plan_002_two_layer_music_and_vocal_engine_20261017.md`

---

## 1. The Core Insight
Previously, the audio engine confused the **voice** with the **instruments**. Every syllable was forcing the entire band (bass, pads, chords, drums) to start and stop at irregular speech intervals, destroying the tempo and harmony.

We are dividing the engine into two decoupled but harmonized layers:

### Layer 1: The Music Layer (The Band / Harmony & Groove)
- **Clock**: Steady, continuous metronomic bar time (4/4, 3/4, etc.).
- **Harmonic Rhythm**: Chord progressions (e.g. $I - IV - vi - V$) that change on measure or half-measure boundaries (every 2 or 4 beats), not on syllables.
- **Smooth Voicing**: Piano/guitar/strings chords voiced with close inversions (voice-leading) rather than jumping parallel blocks.
- **Rhythm Section**: Bass lands on downbeats 1 & 3; drums lock to steady kicks, snares, and hi-hats.
- **Phrasing & Cadences**: Antecedent (call) phrases end on half cadences ($V$); Consequent (response) phrases resolve on full cadences ($I$).

### Layer 2: The Vocal / Text Layer (The Singer / Strum Hits)
- **Prosody & Timing**: Keyed to how long each word takes to speak (syllable duration, word stress, legato carry across syllables).
- **Pitch & Melodic Contour**: Follows the natural voice-leading cost function (`findNaturalNextScaleIndex`), anchored to the active chord's triad notes on strong beats.
- **Expression & Dynamic Articulation**: Accents and strum chucks driven by consonant plosives and AEC semantic strain.
- **Mixer Separation**: Independent channel strips (Volume, Mute, Solo) for Lead Vocal, Rhythm Strum, Bass, and Drums.

---

## 2. Implementation Steps
1. **Mixer Console & Sub-Buses**:
   - Add 4-track mixer controls (Lead, Strum, Bass, Drums) to the Band Conductor panel.
   - Route Web Audio nodes through dedicated channel gain nodes into `masterBus`.
2. **Music Layer Harmonic Grid**:
   - Pre-calculate the measure-by-measure chord progression for the piece based on line planes and cadential functions.
   - Smooth chord inversions so accompanying instruments move smoothly between chords.
3. **Vocal Prosodic Placement**:
   - Place vocal syllables onto the metric grid: content words anchor to beats 1 & 3, pickup words land on upbeats.
   - Snap strong-beat vocal notes to the active chord's triad.
4. **Independent Playback Engine**:
   - Master sequencer runs on exact measure time.
   - Band accompaniment plays continuous, steady groove and harmony.
   - Vocal/lead layer triggers at prosodic word times over the groove.
5. **Score Engraving**:
   - Top staff: Vocal melody + lyrics.
   - Harmony staves: Multi-staff score renders clean measures with proper barlines.
