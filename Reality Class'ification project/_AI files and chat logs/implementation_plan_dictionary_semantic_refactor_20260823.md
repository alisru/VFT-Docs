# QQCI Dictionary Semantic Refactor & Protocol Alignment Plan

## 1. Objective
Refactor all 44 entries in `qqci_dictionary.json` to strictly comply with `dictionary_dev_protocols.md`:
- Eliminate all banned and academic jargon (e.g. `entropy`, `state transition matrices`, `glycolysis`, `ATP`, `teleological`, `biochemical transduction`, `subjective awareness`).
- Enforce the uniform plane projection format for `word_in_context_of_plane`: `"[dimension] as [anchor/role] — [what the word IS when viewed strictly through this plane's lens]"` across all 44 entries.
- Ensure strict plane separation (Rule 4): purge all purpose bleed (`so that...`, `in order to...`) from planes Q1, Q2, Q3, Q5, Q6, Q7 into Q4 only.
- Generalize universal root concepts (Rule 3) so they are domain-agnostic (valid across physics, biology, algorithms, individuals, and social systems) without human civic bureaucratic or narrow biological lock-in.
- Remove non-standard schema fields (`survival_need`) and ensure consistent schema integrity across all entries.
- Maintain Goldilocks word length (15–25 words per plane).
- Re-run `build_dict_js.ps1` to sync `qqci_dictionary.js`.

## 2. Target Entries (44 Words)
- **Batch 1 (Genotype & Phenotype Primitives 1–14)**: `store`, `shop`, `library`, `book`, `know`, `word`, `recognition`, `purpose`, `shelter`, `refreshment`, `power`, `morale`, `moral`, `sustenance`.
- **Batch 2 (Core Interrogative & Ontological Primitives 15–24)**: `who`, `what`, `where`, `why`, `how`, `cause`, `effect`, `be`, `do`, `have`.
- **Batch 3 (Core Operational Verbs 25–34)**: `make`, `see`, `say`, `give`, `take`, `go`, `come`, `find`, `think`, `feel`.
- **Batch 4 (Core Vitality & Structural Verbs 35–44)**: `need`, `want`, `live`, `die`, `grow`, `hold`, `move`, `change`, `build`, `break`.

## 3. Verification & Validation
- Validate JSON syntax.
- Verify zero instances of banned jargon.
- Verify all 44 entries have proper `word_in_context_of_plane` projection formatting.
- Verify no purpose bleed in non-Q4 planes.
- Verify `qqci_dictionary.js` is regenerated cleanly.
