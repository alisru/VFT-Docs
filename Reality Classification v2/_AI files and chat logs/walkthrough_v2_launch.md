# Walkthrough: Reality Classification v2 (AEC-First Architecture)

## Overview
Reality Classification v2 has been launched in a completely new, dedicated workspace: `Reality Classification v2/`.
All glyph gymnastics were eliminated in favor of clean topological closure levels, and the dictionary architecture was inverted so that **Action-Strain-Effect triads are the primary invariant keys**, with words attached to describe them.

---

## 1. Key Accomplishments

### A. Dedicated New Workspace
* Initialized `Reality Classification v2/` with its own `_AI files and chat logs/` directory.
* Established v2 `SKILL.md` enforcing the AEC-first architecture and the 5-stage epistemic primitive hunter protocol.

### B. Architectural Inversion (AEC-First)
* **Old Structure (v1)**: Keyed by English word (`"store": { ... }`).
* **New Structure (v2)**: Keyed by canonical Action-Strain-Effect triad:
  `"put in, keep organized, take out -> exposed, cluttered, inaccessible -> safe, ordered, ready to use": { ... }`
* Words are now classified under `surface_words`:
  * `primary`: The canonical anchor word.
  * `aliases`: Alternative words expressing the same invariant (e.g. *run* and *walk* as velocity variants of *move*).
  * `plane_manifestations`: Contextual surface words across $Q_1 \dots Q_7$.
* `word_index`: High-speed reverse lookup mapping any surface word directly to its AEC primitive key.

### C. 100-Word Foundational Seed Dictionary
* Built and executed `download_seed_dictionary.py`.
* Produced `source_dictionary_100.json` containing 100 core English words across kinetic, force, boundary, custodial, assembly, aggregation, state, and perception domains.

### D. Epistemic Primitive Hunter Pipeline
* Built and executed `epistemic_hunter_pipeline.py` implementing the 5-stage de-substrating sieve ($Q_2$ potential space ➔ $Q_3$ bounded collapse).
* **Pipeline Results**:
  * Migrated 44 calibrated entries from v1.
  * Minted **12 new irreducible AEC primitives**:
    * `push` (`AEC-045`), `pull` (`AEC-046`)
    * `rise` (`AEC-047`), `fall` (`AEC-048`)
    * `open` (`AEC-049`), `close` (`AEC-050`)
    * `enter` (`AEC-051`), `leave` (`AEC-052`)
    * `gather` (`AEC-053`), `scatter` (`AEC-054`)
    * `join` (`AEC-055`), `split` (`AEC-056`)
  * Dynamically linked **9 surface aliases**:
    * `run` & `walk` ➔ `move` (`AEC-041`)
    * `travel` ➔ `go` (`AEC-030`)
    * `drop` ➔ `fall` (`AEC-048`)
    * `contain` ➔ `have` (`AEC-024`)
    * `grab` ➔ `take` (`AEC-029`)
    * `keep` ➔ `hold` (`AEC-040`)
    * `collect` ➔ `gather` (`AEC-053`)
    * `look` ➔ `see` (`AEC-026`)
  * **Current Totals**: **56 AEC Invariant Primitives**, **65 Words Indexed**.

---

## 2. Validation & Verification

* Created `validate_v2.py` auditing:
  * 1-to-1 Triad lockstep matching.
  * Plane-collapse ban on all root definitions.
  * Banned academic/IT jargon.
  * Strict plane separation (telos in $Q_4$ only).
  * Topological closure consistency.
  * Word index integrity.
* **Result**: **`100% PASS`** (0 errors).

---

## 3. Interactive Web Viewer

* Built `viewer_v2.html`:
  * Filter by Topological Closure: Level 0 (Open Axis), Level 1 (Wall), Level 2 (Joint), Level 3 (Pocket), Level 4 (Enclosure).
  * Real-time search across words, aliases, IDs, and triad definitions.
  * Complete 7-Plane reality breakdown matrix per primitive.
