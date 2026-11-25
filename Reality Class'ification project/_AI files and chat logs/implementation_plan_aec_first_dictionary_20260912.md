# Implementation Plan: AEC-First Dynamic Dictionary & 100-Word Epistemic Ingestion

Invert the QQCI Semantic Dictionary architecture from **word-first** to **AEC-first (Action-Strain-Effect as primary keys)**, source a standard 100-word seed dictionary, and build a processing pipeline using the `epistemic-primitive-hunter` skill to dynamically discover, cluster, and link words to their underlying information-action primitives.

---

## 1. Architectural Inversion: Word-First ➔ AEC-First

### Current Architecture (Word-Centric)
* Primary keys are English words (`"store": { ... }`, `"know": { ... }`).
* Traps semantics in language-specific vocabulary tokens.
* Obscures that multiple words across different contexts are expressions of the exact same invariant force vector.

### New Architecture (AEC-First / Invariant-Centric)
* Primary keys are **AEC Invariant Signatures** (or canonical action-strain-effect IDs).
* An AEC node defines the **pure information-action potential and boundary dynamics**.
* **Words are applied/attached to AEC forms** to describe how that invariant manifests across contexts and planes.
* Multiple words cluster into the same AEC primitive (e.g. *store, cache, reservoir, hoard* are all surface expressions of the same containment-retention lifecycle).

```json
{
  "version": "3.0.0",
  "format": "aec_first",
  "primitives": {
    "put_in__keep_organized__take_out": {
      "id": "AEC-001",
      "action": "put in, keep organized, take out",
      "strain": "exposed, cluttered, inaccessible",
      "effect": "safe, ordered, ready to use",
      "definitive_meaning": "to keep things in an organized place for later retrieval",
      "topology": {
        "closure_level": 3,
        "boundary_type": "enclosure_chamber",
        "operations": ["in", "hold", "out"],
        "glyph": "⪽"
      },
      "surface_words": {
        "canonical": "store",
        "synonyms_and_aliases": ["cache", "stock", "hoard", "bank"],
        "plane_manifestations": {
          "Q1": ["steward", "keeper", "reserve"],
          "Q2": ["inventory", "capacity", "margin"],
          "Q3": ["storehouse", "warehouse", "vault"],
          "Q4": ["foresight", "core values", "preservation"],
          "Q5": ["database", "buffer", "index"],
          "Q6": ["surplus", "heritage", "legacy"],
          "Q7": ["readiness", "security", "peace of mind"]
        }
      },
      "planes": {
        "Q1": { "interrogative": "Who", "answer": "...", "word_in_context_of_plane": "..." },
        "Q2": { "interrogative": "What", "answer": "...", "word_in_context_of_plane": "..." },
        "Q3": { "interrogative": "Where", "answer": "...", "word_in_context_of_plane": "..." },
        "Q4": { "interrogative": "Why", "answer": "...", "word_in_context_of_plane": "..." },
        "Q5": { "interrogative": "How", "answer": "...", "word_in_context_of_plane": "..." },
        "Q6": { "interrogative": "Cause", "answer": "...", "word_in_context_of_plane": "..." },
        "Q7": { "interrogative": "Effect", "answer": "...", "word_in_context_of_plane": "..." }
      }
    }
  },
  "word_index": {
    "store": "put_in__keep_organized__take_out",
    "cache": "put_in__keep_organized__take_out",
    "warehouse": { "primitive_id": "put_in__keep_organized__take_out", "context_plane": "Q3" }
  }
}
```

---

## 2. Phase Breakdown

### Phase 1: Source & Download 100-Word Seed Dictionary
* Create a clean downloader/ingestion script (`download_seed_dictionary.py`) in `Reality Class'ification project/_AI files and chat logs/`.
* Source 100 core foundational English words (covering core physical actions, perception, boundary operations, state transitions, social exchange, and containment).
* Sources: Combine foundational Swadesh/Leipzig core vocabularies + standard WordNet/GCIDE definitions into `Reality Class'ification project/source_dictionary_100.json`.
* Structure each entry with orthodox definitions, part of speech, and usage examples.

### Phase 2: Design the Inverted AEC-First Schema & Migration
* Define the JSON schema for `qqci_aec_dictionary.json`:
  * `primitives`: Map of unique AEC triad keys to their full invariant data.
  * `word_index`: Inverted lookup index mapping any surface word to its corresponding AEC primitive and relevant Q-plane.
* Migrate our existing 44 calibrated words into this AEC-first format so zero existing work is lost.

### Phase 3: Epistemic Primitive Hunting Pipeline
* Implement the 5-stage hunter protocol from `.agents/skills/epistemic-primitive-hunter/SKILL.md`:
  1. Substrate Evacuation (remove biology, Earth gravity, IT jargon).
  2. Q2 Potential State Space (uncommitted distinctions and latent gradients).
  3. Q2 ➔ Q3 Collapse (boundary crossing, force application, localization).
  4. 3-Step Pairwise Triad extraction (`Action` ➔ `Strain` ➔ `Effect`).
  5. 7-Plane Rotation Test.
* Create an automated/interactive hunter orchestrator script (`hunt_aec_primitives.py`) that:
  * Reads candidate words from `source_dictionary_100.json`.
  * Runs the de-substrating sieve.
  * **Dynamic Clustering**: Compares extracted triad against existing AEC primitives.
    * If identical or congruent: Appends the word to the existing AEC primitive's alias/plane list.
    * If novel: Mints a new AEC primitive entry.
    * If composite phenotype: Marks parent AEC primitive and topological closure coordinates.

### Phase 4: Validation & Visualization
* Update `validate_dictionary.py` to validate the new AEC-first schema and invariant invariants.
* Update `qqci_dictionary_viewer.html` (or create `qqci_aec_viewer.html`) to support browsing by:
  1. Primary AEC Primitive (Action-Strain-Effect).
  2. Boundary Closure Level (Wall, Pocket, Enclosure).
  3. Surface Word Search (auto-resolving to its AEC primitive and plane projection).

---

## 3. Verification Plan

### Automated Tests
1. `validate_aec_dictionary.py`:
   * Check 1-to-1 lockstep for all action-strain-effect triads.
   * Verify plane-collapse ban on all root definitive meanings.
   * Verify all 7 planes exist per primitive.
   * Ensure word_index maps 100% of surface words back to valid AEC keys.
2. Ingestion Run:
   * Process 10 words as a pilot batch to verify clustering and schema integrity before running all 100 words.

### Manual Verification
* Inspect extracted triads in `qqci_aec_dictionary.json` against the Periodic Table of Boundary Closure.
* Confirm that words like *cache, vault, store* correctly cluster under the same AEC primitive rather than creating redundant duplicates.
