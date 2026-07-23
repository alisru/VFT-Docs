# The Meaning Language — A Specification

How a word becomes a computable meaning in the Qqci system: the representation,
how it is filled, how concepts relate, and the tests that can prove it wrong.

Compiled 2026-07-23. Read after `HANDOVER.md`. This is the artefact the labelling
pass is built against and the input the trained model will eventually consume.

Provenance is tagged on every load-bearing claim so nothing authored is mistaken
for something proven:

- **[MEASURED]** reproduced on this machine, a number exists
- **[IMPLEMENTED]** code exists and runs, not yet a headline result
- **[DESIGN]** a decision, defensible but untested
- **[HYPOTHESIS]** a bet; the can-fail tests in §12 target these

---

## 1. What this defines, and what it deliberately does not

DEFINES: the structure of a single meaning, how meanings connect into a web, how a
meaning's cell gets occupied from data rather than by hand, and how "distance"
between meanings is computed.

DOES NOT DEFINE: the transformer. The geometry is proven free at depth 3
([MEASURED], `bottleneck_test.py`: SVD-343 = Kronecker-343 = 416.9), so the basis
was never the risk. The risk is whether the *content* of the cells is any good,
which is a language question, which is this document. The model build is a
downstream, well-specified delta on Leech-LILA (see `RESEARCH_NOTES.md` §2) and is
out of scope here.

---

## 2. The load-bearing separation (do not merge these)

Two structures, orthogonal, neither derived from the other. This has been the
single most-repeated correction in the project's history; the spec is built to
make merging them impossible.

**A. The Qqci FORM** — the geometry. 7 planes, recursive Q.q.c, the frozen
Kronecker basis. This is *what a meaning IS* as a position in 343-space. It is
never authored; it is learned/triangulated (§6, §7).

**B. The MEANING WEB (meta-dictionary)** — storage and content. Nodes, edges,
rules, senses, mass. This is *where a meaning is filed and what is recorded about
it*. It is authored and derived (§4, §5). It is **never indexed by plane** as a
filing key.

The one bridge, and why it is not a violation: web edges carry a **plane TYPE**
(which of 7 kinds of relation this is — §4). Recording that a relation is
"Q3-constitutive" describes the meaning; it is system-A content referenced inside
a system-B store, the way a library catalogue (B) records a book's subject (A).
That is legitimate. Filing a word *under* plane 7 as its storage location is the
error, and this spec never does it.

---

## 3. The atom: the plane-typed triple

Every unit of meaning is the same shape [DESIGN, converged from four independent
threads — AE-C, SAEL, the universal formula, proof-by-resonance §2]:

    [ state1 , relation , state2 ]

- **AE-C** reads it: context → action → effect.
- **SAEL** reads it: `@RELATION{agent:state1, patient:state2}` [IMPLEMENTED, `sael.py`].
- The **universal formula** reads it: the invariant is the *relation*, not the
  states, which is why `[fuel,consumes,fire]` and `[cell,metabolises,energy]` are
  the same atom in different clothing.

The **relation slot is plane-typed**: it is one of the 7 interrogatives. But the
interrogatives are NOT seven parallel peers. They have internal structure, and
getting this wrong (e.g. filing "what kind is it" under Who) corrupts every sort
downstream. Read each root as its LITERAL question:

    Q1 Who    identity ANCHOR       the thing itself, its name/pointer.
                                     bird's Q1 = "bird". NOT a relation to
                                     something else; it is the address root
                                     (handover: "a word's string is its Who").
                                     Unpaired driver. Q1.q5 = its spelling.

    Q2 What   SELECTOR / modifier    which-one / what-kind / how-much. Does NOT
                                     stand alone as content; it specifies a
                                     value ON another plane (see 3.1).
                                     bird --Q2--> animal (which kind)

    Q3 Where  matter / part / place  bird  --Q3--> wing
    Q4 Why    meaning / purpose      wing  --Q4--> flight
    Q5 How    mechanism / count      flight--Q5--> lift
    Q6 Cause  origin / history       bird  --Q6--> egg
    Q7 Effect consequence / result   wing  --Q7--> flight

`wing` disambiguates by which state1 it hangs off and which plane types the edge:
`bird --Q3--> wing` (part) vs `building --Q3--> wing` (subdivision) share the Q3
core form and split on the Q1 identity of state1. Same form, different context —
the shell filled differently (§6).

### 3.1 What is a modifier over the content planes, not a peer

Q2/What does not carry content of its own; it **selects or quantifies a value on
another plane** [DESIGN, per the "what modifies where/why/how/cause/effect"
correction]. It is the "which-one / how-much" operator, and it lives at the `q`
sub-address of its host, never as a standing Q root:

    "big house"        Q3(house) . q2(big)      What picks a magnitude on Where
    "which reason"     Q4(reason). q2            What picks a value on Why
    "red in the face"  Q1(he) . q7 . q2(red)     What filters an Effect of an identity

This is why modifiers (big, really, red, very) are What-forms with almost no root
of their own (§4): they are nearly all `q`, borrowing their `Q` from whatever they
attach to. The host sets the root; What writes the sub-cell.

Structure of the seven, then, is 1 + 1 + 5:

    Who    (Q1)         the identity ANCHOR (what the reading is about)
    What   (Q2)         the SELECTOR over the content planes
    Where..Effect (Q3-Q7)  the five CONTENT planes that carry the meaning

OPEN [flagged, do not silently resolve]: the handover's 42-Structure pairs
What(+x)/Where(-x) as one Body axis. Treating What as a cross-cutting selector
(this section) is in tension with treating it as Where's axis-partner. Both may
hold at different depths — What as Where's partner on its home axis, AND What as
the selector elsewhere — but this is unreconciled and must not be papered over.
Only the LITERAL roots above are authorable; the reconciliation is a §12-style
question to be settled by measurement, not by argument.

---

## 4. A word is a SPARSE Qqci form

The central representational choice [HYPOTHESIS — this is the bet §12.1 tests].

A word is NOT a dense point in 343-space. It is a **shell**: a mostly-empty Qqci
tensor that carries

- its **Q1 identity** — the string itself (a word's spelling IS its Who; the
  address root, not a score),
- a **Q3 symbol-form** — that it is a mark/sound pointing at something,
- a **pointer to an intended Q4 object** — the meaning it refers to,

and leaves the remaining ~340 cells at **zero** until context fills them.

Two consequences that make this worth betting on:

1. **Capacity without opacity.** The bottleneck test needed 343 dimensions
   [MEASURED]. A *sparse* 343-vector — a handful of lit cells — keeps that capacity
   but stays readable: a word activates, say, `Q4.q6 + Q3.q1`, and you can *name*
   what lit. This is sparse dictionary coding on a NAMED basis, which is the entire
   legibility thesis made concrete.

2. **Polysemy is expected, not pathological.** `wing` lights Q3-form strongly and
   leaves Q1-identity empty; `bird` vs `building` write that empty cell
   differently. The emptiness is where context writes. A word that tried to be a
   single dense point could not do this, which is exactly why spelling-based
   assignment scored at noise ([MEASURED], PLANE-7 ~13% of the way to optimal).

### 4.1 Occupancy before value (two stages)

A meaning is resolved in two passes [DESIGN, mirrors proof-by-resonance §2's
Satisfaction-then-Isomorphism]:

- **Occupancy** — a binary gate per cell: 0 = silent/unresolved, 1 = engaged. This
  is *which* planes are lit. Cheap, sparse, categorical.
- **Value** — a magnitude on each lit cell only, unipolar around Unity (1.0 =
  virtue realised, >1 excess, <1 deficit) [IMPLEMENTED, `vft.py`]. This is *how*
  each lit plane reads.

Never collapse occupancy and value into one number: the binary pattern is what you
read back to explain the meaning; the value is what you compute with. Merging them
destroys the legibility that is the point.

---

## 5. The Meaning Web

The system-B store. A weighted directed graph [DESIGN, from proof-by-resonance §15].

**Node** — one concept (a definitional structure Q):

    id            axomic id (deterministic, content-addressed)
    lemma         surface string (its Q1 identity)
    core_form     the sparse Qqci occupancy that holds ACROSS contexts
                  (the "what it IS" — §6 derives this, not the author)
    qualia        Pustejovsky decomposition, each a plane-typed edge:
                    constitutive (Q3) — its parts
                    formal       (Q1) — its kind
                    telic        (Q4) — its purpose
                    agentive     (Q6) — its origin
    senses        contextual variants: same core_form, different filled cells
    mass          conceptual mass — DERIVED, graph centrality (§5.1)
    class         resonance/homogeneity class it belongs to (§8)

**Edge** — a plane-typed relation (the atom of §3):

    src, dst      concept ids
    plane         Q1..Q7 — which kind of relation
    relation      the canonical middle term (the verb/link)
    weight        resonance distance ON THIS AXIS

Crucial [DESIGN, from the Kevin-Bacon case, proof-by-resonance §15.3]: **likeness
is a 7-vector, not a scalar.** `Res(KevinBacon, bacon)` ≈ 1 on the linguistic axis,
0 on taxonomic, 0 on functional. Every attempt to collapse a word's relation to
another into one distance was destroying the signal. Keep the per-plane vector.

### 5.1 A sentence is a PATH, not a stored string

Sentences are not stored as text. A sentence is a **traversal** of the web — a
chain of plane-typed edges `[A -rel-> B -rel-> C ...]` where each word licenses
the next [DESIGN, from "store effective sentences in potential chains of causal
words"].

- **Potential chains** = all edges licensed out of a node (what can follow).
- **Effective sentence** = a chain that COHERES end to end: it fills without
  cross-plane disagreement (§7.1). A garbled order traces no stable chain.
- **Generation** = walk the highest-resonance chain from the current node.
- **Understanding** = find the chain a given string traces; if none coheres within
  budget (§9), the honest output is "malformed", not a forced fit.

This is the field of §7 unrolled over a sentence: `F(inputs, vantage)` routes the
tokens along a causal path to an end-place. The web stores the graph; meaning is
the path through it.

### 5.2 Mass is derived, not authored

Conceptual mass = graph centrality (PageRank / eigenvector centrality) on the web
[DESIGN, proof-by-resonance §16]. Massive concepts (`truth`, `time`) are those
highly connected to other massive concepts. This is computed from the graph, never
hand-set, and it is the `rho` term in the fill gradient (§7) and the engagement
gate on anchors (§8).

---

## 6. How a cell gets filled: triangulation

The answer to the project's hardest open problem — word-to-cell assignment —
without authoring and without spelling.

A concept's core_form is **the fixed point its concrete instances resonate to**
[DESIGN, from the parable structure + prototype theory; the mechanism is
[MEASURED] as `===`].

- An abstract like `discernment` has no physical referent to point at. It is taught
  the way parables teach: multiple concrete instances (`pearl of great price`,
  `field with treasure`), each a vantage, and the meaning sits at their
  **intersection**.
- The instances are the same triple in different clothing —
  `[merchant, sells-all, obtains pearl]` and `[man, sells-all, buys field]` — which
  is `===` (same relational architecture). `isomorph.py` extracts that shared
  skeleton and scored **100% structural identity** across domains [MEASURED,
  `RESULTS.txt`].
- So: to fill a cell, collect the corpus instances that resonate to it and take
  their plane-wise intersection. The invariant across instances IS the meaning.
  This is the parallax construction — "material earns its place only where
  independent vantages intersect" [IMPLEMENTED, `experiment.py`].

A single instance underdetermines an abstract. Needing *more* vantages is the
measurement telling you the concept's dimensionality, not a defect in the teaching.

---

## 7. Strain and fill: the accretion dynamics

How a shell fills and how it knows it is done [IMPLEMENTED in pieces; the fill loop
is `TruthState` in `qqci_engine.py`].

- **Strain** is distance from the ideal form:

      sigma = || V_ideal - V_real ||          [IMPLEMENTED, vft.py:339 vft_entropy]

  With Unity as the ideal, strain is per-plane deviation from 1.0.

- **The fill gradient** pulls material into a hole against the local density:

      F = delta_S / rho                        [DESIGN, from the strain-force thread]

  where `delta_S` is the per-plane gap (seven metrics, not one — this is what keeps
  the planes from collapsing into an undifferentiated space) and `rho` is
  conceptual mass/occupancy. Accretion slows as the cell fills, so fill is
  detectable as the gradient going flat — not as a magic constant.

- **Halt** at `TS===TBE`: filled when sigma -> 0 (agreement) or the material hits
  fundamentals (irreducible). Overflow then spawns a child cell one density deeper
  (§9) [IMPLEMENTED].

### 7.1 Structural ideal, NOT moral ideal (a safety boundary)

The ideal that strain pulls toward is **structural well-formedness** (does the
relation actually hold between these states), NOT **moral Unity** (is the outcome
good) [DESIGN — this is a hard boundary].

If fill pulled toward moral Unity, the model would predict what *ought* to be
instead of what *is*: it would rewrite tyranny into virtue and be unable to narrate
a villain or report bad news. `[storm, TERMINATE, boat]` is structurally coherent;
`[boat, TERMINATE, storm]` is not — and SAEL already separates exactly those with
zero moral content [MEASURED, 9/9 role-reversal vs 5/9 bag-of-words].

Moral typing belongs to the convergence test that *judges* a claim, never to the
mechanism that *generates* one. Structural fit: yes. Moral certification: not here.

---

## 8. Anchoring by equivalence, not by value

The anchor set for the trained model, derived so nothing is read back [DESIGN,
resolves the standing "do not hand-author scores" rule].

You never author a cell's value. You author (or derive) an **equivalence**: these
words must land together. Gradient descent stays free to place the class anywhere
in 343-space; it just cannot split it. A contrastive loss — pull class members
together, push classes apart — with no number ever supplied.

Sources of classes, mechanical not authored:

- NSM collapse: `hate/loathe/despise -> feel---`, 195 words -> 70 forms
  [IMPLEMENTED, `q4_meaning.py`]. Those 70 forms are the classes.

**The false-anchor trap** (this is `README.md` bug #3 resurfacing — "a plane that
is barely engaged is silent, not dissenting"). sigma -> 0 has two causes:

- **converged** — the plane is engaged and the members agree (real homogeneity),
- **silent** — the plane never activated, so there is no strain because there is no
  signal (zero by absence).

So the anchor gate requires BOTH conditions, using the mass/engagement term already
present [IMPLEMENTED, `CoherenceVector` engagement/assertion split]:

    homogeneous(P, W)  <=>  engagement(P, W) HIGH  AND  sigma(P, W) -> 0

Either alone is a false anchor. Mass (§5.1) supplies the engagement measure, so
this is computable, not hand-judged.

---

## 9. Distance = moments of required reasoning

Meaning as computation, not as a static point [HYPOTHESIS — §12.3 tests it;
the mechanism is [IMPLEMENTED] as the TruthState cycle].

- Each interrogative is a **binary gate**: 0 unresolved, 1 resolved.
- **Density (depth)** = how many gates deep the resolution has gone — *how many*,
  not *which*. This is a different seven from the interrogatives (§11).
- **Distance** = the number of resolution moments still required.

The gates resolve in **dependency order**: you cannot resolve Q5-How until Q4-Why
is known. So distance is not a raw count but a **path** through the dependency
graph — which is the resonance web's meaning-lineage / shortest path (§5), the
staircase fill-order, and process-time depth, all the same quantity by different
names.

This is adaptive computation (Graves' ACT is the citation): harder meanings take
more steps. It is already the `TruthState` cycle — the number of accrete steps to
reach `TS===TBE` IS the moment-count. The parable supplies Q4 first precisely so
the dependent gates *can* resolve, which is why abstracts need examples before
their other planes light (§6).

Gives a concrete, MEASURABLE quantity: for any word, how many resolution moments to
fill? Concrete nouns shallow, abstracts deep, function words near-zero — a
prediction that can fail (§12.3).

---

## 10. Want (the agent's orientation) — kept separate from meaning

Not part of a meaning's form; the orientation of an agent *toward* a thing
[DESIGN]. Recorded here only to keep it from leaking into the plane scores.

    Want = [ benefit-direction , [yes | maybe | no] , magnitude ]

- **benefit-direction** — the upsilon coordinate (universal <-> self benefit), the
  hegemony x-axis.
- **[yes | maybe | no]** — `ModalPosition`. The **maybe is `IN_GAP`**
  [IMPLEMENTED, `qqci_engine.py`]: ambiguity descends rather than snapping. The
  "maybe" is the *drill trigger* — it is what drives the fractal descent one level
  deeper. This is why the trinary is not a bipolar scalar and must not be flattened
  to one.
- **magnitude** — intensity.

Want is an agent's stance; plane_scores are what a meaning is. Different objects,
kept apart — the same discipline as A vs B.

---

## 11. The several sevens (never the same seven)

The project has at least four seven-fold structures. Every historical failure came
from collapsing two of them. They are coordinated, not identical:

    interrogatives   Who..Effect        WHICH aspect of a meaning      (a basis you span)
    densities        Singularity..Master WHICH depth of realisation    (a ladder you climb)
    trinary stack    n1/n2/n3 x ...      Plane/Sense/Use               (per HANDOVER)
    who-benefits     Everyone..no-one    WHICH target of will          (the hegemony axis)

Rule: seven-ness recurs across the framework, but a ladder you climb and a basis
you span are different objects. Density counts resolution steps (§9); the
interrogative names the gate. Coupled, never merged.

---

## 12. The tests that can fail

A claim that cannot fail is decoration. Each hypothesis above gets a falsifier.

### 12.1 Sparsity is real (tests §4)
Derive each word's occupancy from corpus co-occurrence. PASS if word meanings are
genuinely sparse (few lit cells) AND the lit cells are stable across contexts for
monosemous words while shifting predictably for polysemous ones. FAIL if occupancy
is dense (everything lit) or random across contexts — then the shell model is wrong
and words are dense points after all.

### 12.2 The web predicts distribution (tests §5, §6 — the real locality test)
Build the web from labelled instances; compute shortest-path distance between
concepts. PASS if web distance correlates with distributional similarity in the
corpus (substitutable words are near). FAIL if the correlation is flat — then the
web is a pretty graph describing nothing the corpus contains. This is the locality
test run on the structure you believe in, not on an SVD grid.

### 12.3 Reasoning depth tracks abstractness (tests §9)
Compute moments-to-fill per word from the TruthState cycle. PASS if depth orders
words sensibly: function words ~0, concrete nouns shallow, abstracts deep. FAIL if
depth is flat across word types — then "distance = reasoning" is decoration.

### 12.4 Triangulation reproduces known classes (tests §6, §8)
Take the NSM equivalence classes as ground truth. Derive classes independently by
triangulating instances (§6) and gating by §8. PASS if the derived classes
substantially reproduce the NSM ones WITHOUT being given them. FAIL if they do not
— then triangulation is not recovering real structure.

### 12.5 Deflection (the eventual model test, tests the whole thesis)
After training: does a disambiguator bend a token's trajectory toward the
NAMED-correct plane? "river" before "bank" should pull toward Q3/Where.
[from Curved Spacetime, `research/`]. PASS if bends are plane-legible and
predictable. FAIL if "bank" drifts to a numerically-convenient cell with no plane
meaning — then the geometry is real but the names are decoration on an anonymous
embedding.

---

## 13. What is authored, derived, learned (the build inputs)

Keeping these columns apart is what keeps the result honest.

    AUTHORED (by human or LLM annotator, on the INPUT side only — legitimate
      because the tests in §12 are independent of the annotation):
      - the plane-type of a relation (which of 7 kinds an edge is)
      - the qualia decomposition per word (parts/kind/purpose/origin)
      - the AE-C triple for concrete nouns NSM cannot reach (0/27)
      - seed equivalence classes where NSM is silent
      All of this lives in the WEB (system B). None of it is a plane SCORE.

    DERIVED (computed, no hand input):
      - conceptual mass (centrality)
      - homogeneity classes from NSM collapse
      - web distances (per-plane, 7-vector)
      - moments-to-fill (TruthState cycle)

    LEARNED (the model earns these; never authored):
      - a word's actual POSITION in 343-space (its Qqci form / system A)
      - which cells a context lights
      The lexicon work is a VALIDATION set for this, never training input.

If a value is a plane SCORE and it was typed by a human, it is in the wrong column
and the result will be the input read back.

---

## 14. What this does not answer (honest open edges)

- **Open-domain parsing into triples.** SAEL's parser is hand-seeded over toy
  declarative English. Turning arbitrary text into `[state1, relation, state2]` at
  scale is an AMR-parsing problem, imperfect and unsolved here. The web can be
  built from labelled data first; open parsing comes later.
- **Whether the qualia roles are the right decomposition.** Pustejovsky's four are
  borrowed [DESIGN]; they may not be sufficient for all word classes. §12.4 is the
  check.
- **The formula `t = n + (x*y)`** for reasoning depth is deliberately NOT pinned.
  The mechanism (count accrete-steps-to-fill, respect gate dependencies) is
  specified; the algebra falls out of measurement, not authoring.
- **L4 Language, L5 Temporal, L6 Registry** scales remain only partly wired
  (`layers.py`), so cross-language disagreement and belief-state transitions across
  a sequence are still unmeasured.

---

## 15. Minimal first build (what to do Monday)

1. Pick the SAEL-parseable slice of the corpus.
2. Author (LLM-assisted) the web for a few hundred concepts: qualia roles as
   plane-typed edges, per §5 schema. Input side only.
3. Derive mass, classes, per-plane distances.
4. Run §12.2 (web distance vs distributional similarity) and §12.4 (recover NSM
   classes). Both are cheap, CPU, and can fail.

If 12.2 and 12.4 pass, the language describes real structure and the model build is
justified with the anchor set (§8) in hand. If they fail, the failure is cheap and
located before any training run — which is the whole point of specifying the
language before the transformer.
