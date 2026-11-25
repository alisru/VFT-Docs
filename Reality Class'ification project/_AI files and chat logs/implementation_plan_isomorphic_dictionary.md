# Implementation Plan: Dynamic Isomorphic Semantics Dictionary

## Goal
Implement a dynamically-loaded, context-aware **Isomorphic Semantics Dictionary** (in JSON format) that maps natural language words to core semantic primitives (actions, roles, modifiers) across different domain contexts. The dictionary will be loaded into a **globally shared static registry** (`SaelIsomorphicRegistry`), allowing all parser instances, AST structures, and dynamically compiled classes to query a single in-memory database.

---

## User Review Required
We will migrate all hardcoded synonyms to a local JSON file (`isomorphic_dictionary.json`). This registry will be exposed globally as a static cache, enabling runtime extensibility without recompilation.

---

## Proposed Changes

### Tautonic Language Engine / SAEL Prototype

#### [NEW] [isomorphic_dictionary.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Reality%20Class'ification%20project/isomorphic_dictionary.json)
Create a structured JSON file defining semantic frames and context vocabularies mapped as vectors `[SemanticUnit, Direction, Magnitude, State]`:
```json
{
  "meta": {
    "version": "1.2",
    "description": "Dynamic semantic lexicon mapping words to unit vectors, coordinate directions, and outcome states"
  },
  "frames": {
    "relocate": {
      "roles": {
        "vehicle": ["car", "rocket", "bike", "bus", "train", "plane"],
        "origin": ["garage", "earth", "home", "start"],
        "destination": ["store", "grocery_store", "grocery", "work", "office", "school", "shop", "death"]
      }
    },
    "transfer": {
      "roles": {
        "item": ["book", "gold", "money"],
        "recipient": ["bob", "alice", "receiver"],
        "value": ["dollars", "cents"]
      }
    }
  },
  "contexts": {
    "physics": {
      "went": { "unit": "relocate", "direction": "action", "magnitude": 1.0, "state": "Success" },
      "drove": { "unit": "relocate", "direction": "action", "magnitude": 1.0, "state": "Success" },
      "rocket": { "unit": "relocate", "direction": "vehicle", "magnitude": 1.0, "state": "Success" },
      "garage": { "unit": "relocate", "direction": "origin", "magnitude": 1.0, "state": "Success" },
      "store": { "unit": "relocate", "direction": "destination", "magnitude": 1.0, "state": "Success" },
      "death": { "unit": "relocate", "direction": "destination", "magnitude": 1.45, "state": "Failure" },
      "exploded": { "unit": "relocate", "direction": "destination", "magnitude": 1.30, "state": "Failure" }
    },
    "commerce": {
      "paid": { "unit": "transfer", "direction": "action", "magnitude": 1.0, "state": "Success" },
      "wired": { "unit": "transfer", "direction": "action", "magnitude": 1.0, "state": "Success" },
      "book": { "unit": "transfer", "direction": "item", "magnitude": 1.0, "state": "Success" },
      "stolen": { "unit": "transfer", "direction": "action", "magnitude": 1.45, "state": "Failure" }
    },
    "*": {
      "go": { "unit": "relocate", "direction": "action", "magnitude": 1.0, "state": "Success" },
      "give": { "unit": "transfer", "direction": "action", "magnitude": 1.0, "state": "Success" },
      "wire": { "unit": "transfer", "direction": "action", "magnitude": 1.0, "state": "Success" },
      "delete": { "unit": "terminate", "direction": "action", "magnitude": 1.0, "state": "Failure" },
      "kill": { "unit": "terminate", "direction": "action", "magnitude": 1.5, "state": "Failure" }
    }
  }
}
```

#### [MODIFY] [SAELIntegration.cs](file:///e:/VectorFieldTheory/VFTDocs/RealityClassificationproject/SAELIntegration.cs)
*   **Vector Struct**: Introduce a `SemanticVector` struct containing `string Unit`, `string Direction`, `float Magnitude`, and `string State`.
*   **Global Static Registry**: Update `SaelIsomorphicRegistry` to parse `isomorphic_dictionary.json` into a static mapping table of `(Context, Word) -> SemanticVector`.
*   **Coherence & Moral Projection**: Modify `SaelProjector.Project` to retrieve the `SemanticVector` for active tokens and directly apply the `Direction` (role parameter axis), `State` (Success/Failure outcome state), and `Magnitude` factors when scoring Qqc planes. This moves the logic entirely into data configuration!

---

## Verification Plan

### Automated Verification
*   Compile and run the upgraded shell.
*   Feed natural language strings that span hierarchical contexts (e.g., `Alice wired 10 dollars to Bob` under `commerce.banking` context).
*   Verify that the wavefunction collapses to `@TRANSFER`, maps `value = 10`, `item = dollars`, and resolves the transaction correctly.
