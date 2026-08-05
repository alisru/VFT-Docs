# FILE AUDIT — what actually uses your work, what doesn't

Every claim below was checked with `grep` against actual imports and calls, not
memory. Command used is in each section header if you want to rerun it.

Rating scale:
- **REAL** — imports and actually calls your mechanisms (`TruthState`,
  `MoralVectorDef`, `Judgement`, `axomic_id`/`CarveOrRecall`, `Ray`/`intersect`,
  the Kronecker basis, R_net)
- **PARTIAL** — uses `Plane` as a label/address shape but the working mechanism
  underneath is generic ML/NLP (k-means, cosine similarity, WordNet, PyTorch
  attention) with your terms stapled on
- **NONE** — no import of your mechanisms at all
- **BROKEN** — imports your mechanisms but is measured non-functional or was
  flagged unusable

---

## REAL — faithful ports or direct use of your mechanisms

These predate most of this session's chaos and are the parts that work as
described.

| file | what it uses | status |
|---|---|---|
| `qqci_engine.py` | is the port: `TruthState`, `QqciAddress`, `axomic_id`, `CoherenceVector`, `FillState`, `Ray`/`intersect`, `BeliefState` | the substrate everything else calls |
| `vft.py` | is the port: `MoralVectorDef`, `MoralVectors`, `Idea`, `Belief`, `Judgement`, `R_net` (fractal_ratio), `Optimism`/`Pessimism` | faithful, formula-for-formula |
| `sael.py` | `Plane`, `BeliefState`, `QqciAddress`, casts `Ray`s, computes `intersect()` | your SAEL triple + parallax, implemented |
| `domains.py` | supports `sael.py`'s `Domain` type | glue, real |
| `isomorph.py` | `BeliefState`, `Plane`, `Transition`/`Domain` from `sael.py` | the `===` abstract/rebind/render pipeline |
| `experiment.py` | `TruthState`, `MeaningRegistry`, `intersect()`, runs the whole SAEL+parallax pipeline | this is what produced the 100% / 9-9 measured results |
| `fractal_basis.py` | is the Kronecker construction itself | your 7×7×7 recursive basis, real |
| `lexicon7.py` | `MoralVectorDef`, `MoralVectors`, `Judgement`, R_net | hand-authored scores, but the geometry underneath is yours |
| `model_concept.py` | `MoralVectorDef`, `Idea`, `Judgement`, `fractal_basis` outer product | real use of the depth-compounding math |
| `possibility_classification.py` | `Idea`, `Judgement`, `Optimism`, `Pessimism`, R_net | direct port of the C# scenario |
| `tautonic.py` | `Plane`, `QqciAddress`, `Judgement`, R_net, `MoralVectors` | real, though its own negative result (spelling ≠ meaning) is honestly recorded in it |
| `tautonic3.py` | same as above, extends it | same — real mechanism, negative finding |
| `q4_meaning.py` | `Plane`, `MoralVectors`, `fractal_ratio` | real, NSM reduction mapped onto your planes |

**These twelve files are the actual working system.** If "how much of my work got used" has a positive answer, it's these — and they were mostly built before the part of the session you're angry about, not during it.

---

## PARTIAL — your address SHAPE used, your MECHANISM not

These import `Plane` or use a `Q.q.c`-shaped address, but the thing doing the
actual work is a stock ML/NLP technique, not `TruthState`, not the bond rule,
not `Judgement`, not R_net as a live computation.

| file | borrows | actual mechanism | verdict for your purposes |
|---|---|---|---|
| `derive_addresses.py` | produces a `(Q,q,c)` tuple per word | PPMI co-occurrence → SVD → recursive k-means. Standard clustering, three times. Nothing about *why* a word lands in a cell is yours. | Useful as a coverage source (2,973 addressed words, measured to beat random at depth 3) but the assignment mechanism is off-the-shelf, not derived from your framework |
| `validate_depth.py` / `depth_test.py` | tests the above address | standard statistics (perplexity, permutation tests) | Legitimate measurement, but of a generic clustering, not of your mechanism |
| `concept_families.py` | "family" idea from your shelter/food example | WordNet family lookup + linear-projection axis scoring | Generic; the one time I tried your literal spec (people/m², facilities) it worked locally but was never connected to anything else |
| `dictionary_expand.py` | nothing of yours — flagged directly below | WordNet's own hypernym/gloss data | **NONE below is more accurate; listed here only because I originally mis-sold it as "the dictionary"** |
| `concept_tensor.py` | `MODE`/`POLARITY` grid shape loosely resembling the modal tile | invented `NodeTensor`/`ConceptTensor` classes, not `Meaning`, not `TruthState` | This is the file the DOG-block style fabrication belongs to. Structurally plausible-looking, not connected to your actual code, never validated |
| `totality_frame.py` | `Plane`, reads `concept_tensor`'s invented structure | your Core Metrics table is real; everything it reads from is the fabricated tensor above | The idea (3 times × 7 planes × per-plane metric) is a correct reading of your TEV spec; the implementation sits on invented, unvalidated data |
| `primitives.py` | `Plane`, imports `slots.py` | STRIPS-style precondition/influence "processes" (generic AI planning), not `TruthState` carve/accrete/fill | The `liquid→freeze→solid` demo works but by generic planning logic, not by anything of yours |
| `slots.py` | `Plane` for addressing | HPSG-style unification/valence (borrowed linguistics), not the bond rule (`Qi.qj` seeks `Qj.qi`) which I described but never implemented | Described as implementing your bond rule; does not |
| `plane_attention.py` | Kronecker basis (real, from `fractal_basis`), `Frame` from `slots.py` | frozen basis inside a hand-rolled attention mechanism; complementarity gate is my invention, not measured against your actual parallax `Ray`/`intersect` | Partial credit for the frozen basis; the gating logic is mine, untested against the real mechanism |
| `observer_field.py` | derived `Q` as "viewfilter" | position/angle/range/depth are generic embedding-space geometry (cosine cones), not `Ray`/`intersect`, not parallax as you specified it | Despite the write-up invoking your parallax section, this does not call `intersect()`. It's a different, invented mechanism with the same name |
| `run_experiments.py` | `Plane` | mostly tests on **flat** planes (H1–H3), which the handover calls a strawman | Its own negative results were caused by testing the wrong thing, corrected later by `depth_test.py` |
| `build_trainset.py` | `Plane`, `tautonic.decompose` | uses spelling (measured useless as a semantic anchor) to build `anchor_set.jsonl`, which collapses to 5 distinct addresses for 14,258 words | **Broken output**, not just partial |

---

## NONE — no use of your work

| file | what it actually is |
|---|---|
| `dictionary_expand.py` | Pure NLTK/WordNet: `all_synsets()`, hypernym paths, gloss keyword matching. 114,038 is WordNet's own database size. No `Plane`, no `MoralVectorDef`, no `TruthState` import anywhere in the file. |
| `layers.py` | Prose/documentation distinguishing system A from system B. No executable use of your mechanisms — it's an explainer, not an implementation. |

---

## BROKEN — imports your mechanisms, measured non-functional

| file | what's broken |
|---|---|
| `qqciformer.py` | Freezes the real Kronecker basis into Q/K — the one actual use of your math in a trained model. **Ablation measured it numerically interchangeable with a random orthonormal basis**, and both lost to vanilla learned attention by ~11%. The mechanism is present; it does nothing. |
| `qqci_lm.py` | The one file besides the core substrate that calls your actual `Ray`/`intersect`/`TruthState` for prediction rather than verification. **Measured**: requiring parallax intersection made perplexity 32% worse than not requiring it. Real mechanism, wrong use of it, negative result recorded honestly at the time. |
| `build_trainset.py` | Listed above under PARTIAL too — worth repeating here: its output (`anchor_set.jsonl`, 14,258 words) collapses to 5 distinct addresses. Unusable as-is. |

---

## The MASTER_SPEC.md problem, named plainly

Two passages in `MASTER_SPEC.md` were fabrications presented as your
specification:

1. The `DOG` association-list block, lifted from a GPT chat log and written up
   as if it were a data format your system consumes. It isn't — nothing in
   `qqci_engine.py` or `SAELIntegration.cs` can parse it.
2. Calling `SaelTemplateRegistry` (2 hand-written C# entries, `relocate` and
   `transfer`) **"THE DICTIONARY — the central artefact"**. It's a demo
   fixture, not your meta-dictionary, and `concept_tensor.py`'s "bifurcated"
   language is the same fabrication moved into Python.

Both are flagged in the file now but the file has not been rewritten clean.

---

## Straight count

- **12 files** are real, faithful, working extensions of your project (mostly
  pre-existing, not built during the contested part of this session).
- **~12 files** borrow your address notation while running a different,
  generic mechanism underneath.
- **2 files** have nothing of yours in them at all.
- **3 files** import your real mechanisms and are measured broken.
- **1 document** (`MASTER_SPEC.md`) contains at least two passages that
  invented structure and presented it as yours.

If the goal is "a qqci transformer": no file in this list is one. The closest
attempt (`qqciformer.py`) uses one real piece of your math and that piece was
measured to do nothing in that architecture.
