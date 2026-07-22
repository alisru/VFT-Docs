# Handover: Qqci Fractal LLM — Continuation Brief

Purpose: hand this to a fresh session so it can continue without re-deriving. Read this file and the four files in "Read these first". Do NOT re-read the whole `_VFT MD` corpus or the full scope doc unless a specific claim needs checking.

Last updated: 2026-07-21. Working dir: `E:\Vector Field Theory\VFT Docs\Reality Class'ification project\qqci\`

---

## The one-paragraph plot

The goal is a learning LLM built on a FIXED 7-plane ontology (the Qqci skeleton) instead of learned anonymous dimensions. The bet: a named, morally-typed geometric basis costs little against an anonymous one while buying legibility. Prior art (Lila-E8, Leech-LILA) already proved the general idea — a fixed geometric basis in attention beats an unstructured baseline at small scale (p<0.001). Our differentiator is that the basis is NAMED (7 planes with virtue/sin poles) and RECURSIVE (7x7x7, not flat 7). As of this session the core geometric claim is MEASURED AND CONFIRMED, and the remaining problem is narrowed to one thing: how words get assigned to cells.

---

## The single most important result (measured this session)

A frozen basis built from the 7x7x7 Kronecker structure — 49 floats, named, never trained — matches the mathematically OPTIMAL 343-dimensional basis to one decimal place on next-word prediction:

    FULL bigram (no bottleneck)          449.1 perplexity
    Kronecker-343 (frozen structured)    480.6
    SVD-343 (optimal ceiling)            480.6   <- identical
    RANDOM-343 rotation                40493.1

Structure is FREE at depth 3. This is the whole thesis and it holds. Reproduce with `bottleneck_test.py` plus the inline locality script (in session log).

Corollary, equally important: FLAT 7 DOES NOT WORK. SVD-7 (the ceiling for any 7-dim compression) scores 728 vs unigram 736 — seven dimensions retain only 2% of what context provides. 49 dims retain 48%, 343 retain 82%. The recursion is not decoration; it is doing all the work. The operative unit is Q.q.c, never Q. Anyone who tests flat 7 is testing a strawman the user never proposed.

---

## TWO SEPARATE SYSTEMS — the meta-dictionary has NO RELATION to Qqci (do not apply Qqci to it; this was the single most-repeated correction of the session)

**A. The Qqci FORM** — the semantic geometry. 7 planes, recursive Q.q.c, one 7x7 Kronecker generator (`fractal_basis.py`). This is what a meaning IS. This is where the 7 planes live.

**B. The MeaningMetaRegistry (the meta-dictionary)** — a SEPARATE concept, its own thing, NOT Qqci and NOT plane-valued. It is a nested store: a dictionary of dictionaries. Nesting from `{Meaning}.cs`:

    Registry > Temporal > Language > Phrase > Word > Char > Meaning

Each scale STORES THAT SCALE'S CONTENT:
- Char  : characters
- Word  : words
- Phrase: phrases
- Language: the LANGUAGE RULES themselves (the `---word+++` spectrum, the collapse dictionaries, the NSM reduction, grammar). This is where rules are kept.
- Temporal: time / versioning
- Registry: which contextual dictionary (0=General, 7=Conflict, ...)

The integer keys are KEYS, not plane readings. Do NOT index the meta-dictionary by plane. Do NOT read `wordLayer: 7` as "reads Effect at word scale" — that was a false story this session built and the user rejected repeatedly. The meta-dictionary is infrastructure for storing and retrieving the language system (its words, phrases, and especially its RULES). It is orthogonal to, and independent of, the 7-plane Qqci form.

A meaning HAS a Qqci form (A). A meaning is STORED IN and looked up FROM the meta-dictionary (B). B holds rules and content; A is geometry. They do not share axes and neither is derived from the other. `layers.py` and the `MeaningMetaRegistry` class in `qqci_engine.py` still carry the wrong plane-indexed framing and MUST be corrected: the meta-registry should not be indexed by `root_plane`.

Also distinct: the Trinary Stack (Actualism's n1 Plane / n2 Sense / n3 Use) is a THIRD structure that also comes in sevens. It is NOT the Qqci address. The Qqci address is recursive same-kind, which is why the Kronecker construction is correct.

---

## The 7 planes (the fixed metaclass — never revised at runtime)

Unipolar around Unity: 1.0 = virtue realised, >1.0 = Excess of the sin, <1.0 = Deficit of the same sin. NOT bipolar. This is load-bearing: a bipolar span cannot express "too much and too little are the same failure".

    Q1 Who    Metaphysical  Sovereignty/Tyranny        Driver, 7th angle, UNPAIRED
    Q2 What   Possible      Stewardship/Greed          +x  \ Body
    Q3 Where  Physical      Thriving/Mere Survival     -x  /
    Q4 Why    Lyrical       Truth-Telling/Delusion     +y  \ Mind
    Q5 How    Logical       Wisdom/Sophistry           -y  /
    Q6 Cause  Historical    Redemption/Revisionism     +z  \ Soul
    Q7 Effect Emotive       Love-Unity/Parasitism      -z  /

Coherence is R_net = 1 / product(7 scores), the Fractal Ratio Protocol. NOT a mean — a mean cannot diverge, and R_net must go to infinity when any plane collapses to zero (one dead plane collapses the whole idea). This is in `vft.py`.

Each plane has a Core Metric (its distance function), already specified in the corpus, which closes the old "seven-metrics problem":
Who=Directional Time, Why=Non-Euclidean Time, Cause=Linear Time, What=Resolution Time, Where=Euclidean Space, How=Computational Time, Effect=Energetic Time (Strain).

Q1 is special: a word's STRING is its Who (its identity). Q1 is not a score, it is the address root. Every word is Q1-rooted.

---

## Read these first (in order)

1. `fractal_llm_merged_scope.md` (parent dir) — the full scope. Sections 16-19 are newest; SECTION 19 IS ERRATA and lists every wrong claim from earlier versions. Read the errata before trusting any earlier section.
2. `vft.py` — faithful Python port of the user's C# (Idea, StateVector, FieldMath, Judgement, Optimism, Pessimism). The project's real math. Formula-for-formula, do not "improve" it.
3. `fractal_basis.py` — the Kronecker basis, sub-object sharing, the measured dead-end (interpolation, coherence 0.98, do not retry).
4. `bottleneck_test.py` — the decisive test above.

Everything else: `qqci_engine.py` (engine: planes, addresses, registry, meta-registry, TruthState), `sael.py` + `domains.py` + `isomorph.py` + `experiment.py` (the working symbolic retelling prototype, PASS), `tautonic.py` / `tautonic3.py` (character decomposition — USEFUL FOR IDENTITY ONLY, useless for meaning, see below), `q4_meaning.py` (NSM generalised-form layer), `model_concept.py` (concept modelling, note the house/home hardcoding caveat).

---

## What is validated vs open

VALIDATED (measured, reproducible):
- Frozen 7x7x7 basis = optimal 343-basis. Structure is free at depth 3.
- Flat 7 is insufficient (2% retention). Depth is mandatory.
- Symbolic retelling preserves structure across domains (100% round-trip, though only ~3 of the 8 checks are independent — see errata 19.10).
- SAEL canonical collapse beats bag-of-words on role reversal (9/9 vs 5/9), a weak baseline but a clean separation.
- Trigram (Q.q.c) word-form signatures are order-sensitive and collision-resistant (retention 0.87, anagram collapse 0%). GOOD FOR Q1 IDENTITY.
- Isomorphic collapse works at word rank via NSM (`hate/loathe/despise -> feel---`, mechanical, 195 words -> 70 forms).

OPEN (the actual frontier):
- **Word-to-cell assignment.** This is THE unsolved problem. Spelling (character tensor) is useless for meaning — measured same-type vs different-type cosine gap of +0.042 = noise. Plane scores must come from the CO-OCCURRENCE distribution (where the predictive signal demonstrably lives), not from spelling and not from hand-authoring. Every hand-authored attempt this session was a mistake the user caught.
- **Locality on the grid** ("contiguous medium, adjacent concepts connect emergently"). NOT YET TESTED CORRECTLY. The one attempt measured SEQUENTIAL adjacency (words that follow) which is the wrong relation; the right one is DISTRIBUTIONAL similarity (substitutable words, same context). Rerun before claiming anything.
- NSM covers scalar/affective words but 0/27 concrete nouns. A noun's Q4 is likely a mini-SAEL explication (a structure of primes), not a single base+degree. Derive explications distributionally, do not author them.
- L4 Language (only L0 ever populated), L5 Temporal (carved_at stored but unused; belief-state transitions across a sequence untracked), L6 Registry (corpus registries 0=General 7=Conflict not wired in).

---

## The build path, now justified

The trained model is now justified because its frozen basis is PROVEN to cost nothing. Copy Leech-LILA's recipe (working PyTorch in that paper), substituting our basis:

1. Frozen depth-3 Kronecker basis (from `fractal_basis.py`) in place of the learnable Q and K projections. Values stay learnable. d_model a multiple of 343, or 7 heads of 49 / 49 heads of 7. One head per plane is most interpretable.
2. Three-term loss: L = L_CE + lambda_geo * L_resonance + lambda_anchor * L_anchor.
   - L_resonance is Leech-LILA's verbatim (1 - mean max-cosine-to-basis). It is also the differentiable form of the fill gate.
   - L_anchor is OUR addition, the price of a named basis: pin a seed set to known plane scores so gradient descent cannot use the axes arbitrarily and leave the names as decoration. Lila models need no anchor because anonymity costs them nothing.
3. Train on TinyStories or the user's corpus. Word-to-cell assignment EMERGES from next-token prediction (this is what Lila-E8 does: the corpus builds occupancy, not the basis). The lexicon work is a VALIDATION set (does `hate` land near `loathe`?), not training input.

Depth (layer count) stays a free hyperparameter per prior art. The geometry lives in the frozen basis, not the layer count.

---

## Hard-won rules (the user enforces these; violating them wastes the session)

- READ THE SOURCE before building. This session repeatedly invented things already in `{Idea}.cs`, `FieldMath.cs`, and the `_VFT MD` corpus (`Tautonic_Semantic_Dictionary_Full.md`, `nsm_reduction/`, the contextual dictionaries). Possigravity (excavation), the moral poles, R_net, and the language rules all already existed.
- DO NOT HAND-AUTHOR plane scores and then report the result as a finding. It is the input read back. The user catches this every time.
- TEST can-fail claims. Retention 0.87 looked great and meant nothing until the second metric (family gap) showed it measured spelling. Always pair a "distinctness" metric with a "does it track meaning" metric.
- Prefer the user's own corpus as data (14,258 word types harvested, domain-matched) over external datasets.
- The user says recursive 7x7x7, always. Never collapse the claim to flat 7.
- Search before asserting present-day facts; the user banned fabricated quotes and requires marking claim provenance in chat.

---

## Immediate next action (pick one)

A. Corrected locality test: do DISTRIBUTIONALLY SIMILAR words (same-context, from SVD) land in adjacent 343 cells, and is the adjacency smooth enough for a concept to grow into neighbours? Cheap, CPU, tests the "contiguous medium" claim properly.

B. Build the trained model (Leech-LILA fork with the 7x7x7 frozen basis and 3-term loss). The basis is validated; the blocker was never the geometry.

Recommendation: A first (hours, decides whether the substrate is right), then B.
