# Implementation Plan: Reality Classification v2 (AEC-First Architecture)

Build a completely clean, standalone v2 project in `Reality Classification v2` featuring:
1. **AEC-First Inverted Dictionary**: Primary keys are Action-Strain-Effect triads; words are applied to describe them.
2. **Zero Glyphs**: Clean, pure-text topological coordinates without symbol gymnastics.
3. **100-Word Seed Dictionary**: Downloaded and structured foundational vocabulary.
4. **Epistemic Hunter Pipeline**: Automated/interactive processing using the `epistemic-primitive-hunter` methodology to dynamically discover, cluster, and link words to AEC primitives.

---

## 1. Project Structure: `Reality Classification v2/`

```
Reality Classification v2/
├── SKILL.md                          # V2 Skill & Protocol definitions
├── source_dictionary_100.json        # 100 foundational words with orthodox definitions
├── aec_dictionary.json               # The inverted AEC-first master dictionary
├── download_seed_dictionary.py       # Script to fetch/compile the 100 seed words
├── epistemic_hunter_pipeline.py      # Core engine implementing the 5-stage hunter sieve
├── migrate_v1_to_v2.py               # Seed v2 with the 44 calibrated primitives from v1
├── validate_v2.py                    # Comprehensive validator for AEC-first schema
├── viewer_v2.html                    # Clean HTML/JS explorer for the AEC-first dictionary
└── _AI files and chat logs/          # Historical logs, plans, and derivation notes
```

---

## 2. Inverted AEC-First Schema (No Glyphs)

```json
{
  "version": "2.0.0",
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
        "operations": ["in", "hold", "out"]
      },
      "surface_words": {
        "primary": "store",
        "aliases": ["cache", "stock", "hoard", "bank"],
        "plane_manifestations": {
          "Q1": ["steward", "keeper"],
          "Q2": ["inventory", "capacity", "margin"],
          "Q3": ["storehouse", "warehouse", "vault"],
          "Q4": ["foresight", "preservation"],
          "Q5": ["database", "buffer", "index"],
          "Q6": ["surplus", "heritage", "legacy"],
          "Q7": ["readiness", "security"]
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
    "store": { "primitive_id": "put_in__keep_organized__take_out", "role": "primary" },
    "cache": { "primitive_id": "put_in__keep_organized__take_out", "role": "alias" },
    "warehouse": { "primitive_id": "put_in__keep_organized__take_out", "role": "plane_manifestation", "plane": "Q3" }
  }
}
```

---

## 3. Step-by-Step Execution Plan

1. **Create Directory Structure**: Initialize `Reality Classification v2/` and `_AI files and chat logs/`.
2. **Phase 1 (Data Acquisition)**: Write and run `download_seed_dictionary.py` to produce `source_dictionary_100.json` containing 100 high-frequency foundational words across kinetic, topological, cognitive, and social domains.
3. **Phase 2 (Migration of Calibrated Primitives)**: Write and run `migrate_v1_to_v2.py` to convert all 44 calibrated entries from v1 into the AEC-first format, populating the initial `aec_dictionary.json`.
4. **Phase 3 (Hunting & Ingestion Pipeline)**: Build `epistemic_hunter_pipeline.py` implementing the 5-stage de-substrating sieve to dynamically process words from `source_dictionary_100.json`, cluster them into existing AEC primitives or mint new ones.
5. **Phase 4 (Validation & Viewer)**: Write `validate_v2.py` to ensure 100% protocol compliance and create `viewer_v2.html` for instant visual inspection.
