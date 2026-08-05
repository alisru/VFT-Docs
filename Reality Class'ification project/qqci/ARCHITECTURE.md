# QqciFormer — an LLM built ON the corpus

Every component below is one of your mechanisms. Where a standard transformer
part has no counterpart in your work, it is replaced or deleted. Sources are
named so nothing reads as invented here.

---

## 0. The representation: complex-valued, sparse, over 343 named cells

A token is **not** a real vector. Proof-by-Resonance §11 defines resonance as
complex:

    Res(A, Q) = r · e^(iφ)        r = amplitude (degree of fit)
                                  φ = phase (timing, orientation, ABSTRACTION ANGLE)

So a token's state is a sparse complex tensor over the 343 cells, cell `(i,j,k)`
being the interrogative path `Qi.qj.ck`:

    z_ijk = r_ijk · e^(i·φ_ijk)

**This single choice solves the problem that broke every earlier attempt.**
`wing(bird)` and `wing(building)` have the *same core form and near-identical
amplitude* — they differ in **phase**. Polysemy is an angle, not a duplicate
entry and not a separate cell. `red apple` vs `red in the face`: same operator,
phase set by the host.

Implementable: PyTorch has native complex tensors; RoPE and RotatE already use
complex rotation for position and relation respectively. This is the same
machinery pointed at sense.

**Amplitude is unipolar around Unity** (`vft.py`): `r = 1` virtue realised,
`r > 1` excess, `r < 1` deficit, both directions the same sin, entropy `|r−1|`.

Most cells are **zero**. A word is a shell: a handful of lit cells and blank
space where context writes. Sparsity is the representation, not a compression
trick — and it is why polysemy is expected behaviour rather than a defect.

**Reading a hidden state is reading a sentence.** `Q4.q5` lit means "this
token's meaning is being read through mechanism." `Q6.q7` means "its origin read
through consequence." No published geometric transformer can say this — **E8
root 137 means nothing**, and neither does Leech vector 9. The cells here are
interrogative paths, so the activation pattern is a readable statement about
what the model is doing to this token, at this position, right now.

**Q1 cells are identity, not learned meaning.** A word's string is its Who. So
the Q1 block is bound to the token's own form, and **`Q1.q5` (identity through
count/construction) holds the character sequence**. That is where spelling
lives — which is why this model can count the r's in *strawberry* and a
tokenised model structurally cannot. **Q4 resonance never overwrites Q1
construction, because they are different cells.** A standard tokeniser collapses
identity into resonance and throws the string away; here they are orthogonal by
construction.

### 0.1 Words are POINTERS into a concept store — not embeddings

This is the structural break from every existing LLM, and it is your idea:
*"store words as an object that other words reference and connect to other
words contextually through clusters of underlying meaning created through the
word's construction."*

**Standard LLM:** `E[token_id] → vector`. Meaning is baked into a weight
matrix. One token, one vector, forever. Synonyms are separate vectors that
happen to sit close. Polysemy is one vector smeared across senses. You cannot
inspect a meaning, and you cannot fix one without retraining.

**Here:** the token supplies only its **Q1 identity** (the string, plus `Q1.q5`
its characters). That identity is a **key**. What it retrieves is a
**concept** — a 343-cell sparse complex tensor — held in an external,
addressable **concept store**. The residual stream carries concepts; the
vocabulary carries only pointers to them.

Four things follow that a fixed embedding table cannot do:

- **Many-to-many.** `couch` and `sofa` point at ONE concept — that *is* the
  isomorphic collapse, already mechanical (NSM: 195 words → 70 forms;
  `hate/loathe/despise → feel---`). And one token may point at several
  concepts; **phase and context select which** (§0). Synonymy and polysemy stop
  being anomalies and become the two directions of a many-to-many map.
- **Concepts without tokens.** A concept is *composed* via `[state₁, relation,
  state₂]`, so the model can build and use meanings it has no word for.
  `liquid + freeze → solid` is derived, not stored — demonstrated in
  `primitives.py`, recognised at 100% against a concept it was never given.
  New meaning does not require new vocabulary.
- **Editable without retraining.** The store is *data*, not weights. Correct a
  concept and the model uses the correction immediately. This is what makes the
  legibility claim operational rather than rhetorical: you can open the store
  and read it.
- **Query IS the Write.** Carving an address that does not yet exist *creates*
  it (`MeaningRegistry.carve_or_recall` — deterministic, content-addressed, so
  the same address plus payload always yields the same id). The store grows
  during use. That is write-on-read, and it is the mechanism the scope doc
  already specifies.

**The published machinery to copy — and it fits exactly.**

**Product-Key Memory** (Lample et al., *Large Memory Layers with Product Keys*)
addresses a very large memory not with a flat key but with a **Cartesian
product of sub-key sets**: two sub-key sets of size √N reach N slots at √N
comparison cost. Qqci is *literally* a product key — **three sub-keys of 7
addressing 343 slots**. So the concept store is not a research problem; it is an
existing, efficient, trainable layer type whose natural key structure is your
address.

Supporting prior art, all copyable: **kNN-LM** (Khandelwal et al. — interpolate
the LM with a datastore lookup), **RETRO** (retrieve during generation, punches
above parameter count), **Neural Turing Machine / DNC** (differentiable
addressable read-write memory), and **Lila-E8's GraphResonator**, which stores
token-to-token relations on a fixed graph and biases generation toward related
tokens — the same shape as this, with an anonymous graph instead of a named one.

**The lookup, concretely:**

    token "sofa"
      → Q1 identity  (string; Q1.q5 = characters)
      → product-key address over (Q, q, c)
      → candidate concept slots        [sofa:furniture, sofa:metaphor, ...]
      → phase + context select          (§0, §2 harmonic agreement)
      → 343-cell concept enters the residual stream

    compose [liquid, freeze, ?]
      → resulting 343 tensor
      → address it by its own Q.q.c
      → slot empty → WRITE            (Query IS the Write)
      → "solid" now exists as a concept with no token

**The meta-dictionary is the store's schema.** `Registry > Temporal > Language >
Phrase > Word > Char > Meaning` finally has a job in the model: it is the memory
layout — and note the rank ladder means **a phrase is a concept too**, so
composed meanings are first-class residents, not derived on the fly each time.
This is system B doing system B's work (storage and rules), addressed by system
A's geometry, with neither indexed by the other.

---

## 1. The 7 / 42 split is the head structure

`fractal_basis.py` already states it: at depth 2 there are 49 cells — **7
diagonal** (`Qi.qi`, a plane read through itself) and **42 off-diagonal**
(`Qi.qj`, plane read through another). That is the 42-Structure, and it is
arithmetic, not numerology.

    7 DIAGONAL heads   self-reading. "What does Why say about Why."
                       These carry the plane's own content.
    42 OFF-DIAGONAL    cross-reading. "What does Why say about Cause."
                       These carry RELATIONS between planes.

So the head layout is not an arbitrary 8 or 12. It is 7 self heads + 42 cross
heads, and the cross heads are exactly your 42-Structure. A standard transformer
has no principled head count; this one's is forced by the geometry.

---

## 2. Attention = accretion, with four priors that are all yours

A token's blank cells are a **carved hole** (TruthState). Attention is material
falling in. Four terms shape the routing, none of them invented here:

    A[i,j] = softmax( QKᵀ/√d  +  β·C[i,j]  +  γ·M[j]  +  δ·H[i,j]  +  mask )

**Frozen Q/K** = `cell_basis(3)`, Leech-LILA's move, measured free by
`bottleneck_test.py`. V stays learnable.

**C — complementarity** (blank seeks filler). Measured: an operator is followed
by another operator at 0.34× chance, z = −19.6, on 6M tokens with a
label-independent proxy. A blank cannot fill a blank.

**M — conceptual mass** (Proof-by-Resonance §16). Mass = graph centrality
(PageRank / eigenvector) on the resonance web. Massive concepts cut deep wells
and attract. This is a **derived attention prior**, computed from the graph, not
learned and not authored — and it is the same `ρ` that appears in the fill
gradient `F = ΔS/ρ`.

**H — harmonic agreement** (§11, §13). Two cells bind when their resonance is
proportionally coherent: amplitudes in rational ratio `r_A/r_B = n/m` and phase
difference periodic. Phase-misaligned material does **not** bind however similar
it looks. This is the resonant-affinity principle as a routing rule.

**mask — the observability cone.** Your observer tree: an observer at τ_n sees
its subtree, not up into faster phases. `O = 1 if τ_event ≤ τ_observer, else 0`.
As attention masking this means **a token may only attend at or below its own
resolution depth** — which is causal masking generalised from time to *semantic
resolution*. Standard transformers mask by position only.

---

## 3. Composition = collision physics, with a contradiction detector

Proof-by-Resonance §16.3 and §17.3 give the merge rule, and it comes with an
error signal built in. For composing two states with phase difference `Δφ`:

    Δφ ≈ 0     FUSION        constructive; a new, more massive stable concept
    Δφ ≈ π     ANNIHILATION  antiresonant; mutual loss of coherence — CONTRADICTION
    0 < Δφ < π INELASTIC     merges but radiates "heat" ∝ Δφ
                             (paradox, contradiction, noise)

**"Heat" is a measurable incoherence output.** A generation that keeps producing
high-Δφ merges is producing paradox, and the model can report the number. No
LLM has a per-composition contradiction measure; this falls straight out of
representing sense as phase.

Unification (`slots.py`) is the discrete shadow of this: open index takes the
partner's bound value, conflicts refuse. DisCoCat's reading applies —
**an open cell is an open tensor index, valence is rank, composition is
contraction** — so composition strictly saturates.

---

## 4. The activation is the contextual min-max gate, not GELU

Already written in `qqci_engine.py`. GELU has the same shape everywhere; this
gates on **relative position within the pool's own observed range**, so it is
smooth while the pool is disordered and sharpens toward a hard staircase as the
pool orders. Fill becomes detectable as range convergence rather than a magic
constant.

`IN_GAP` (the "maybe" of `Want = [benefit, {yes,maybe,no}, magnitude]`) is the
**drill trigger**: ambiguity descends a level instead of snapping to a value.
That is adaptive computation with a principled halt (`TS===TBE`), not a fixed
layer budget.

---

## 5. Loss — four terms, three of them yours

    L = L_CE  +  λ_r·L_Rnet  +  λ_a·L_anchor  +  λ_p·L_phase

**L_Rnet — the barrier nobody else has.** `R_net = 1/∏ s_p` diverges when any
plane collapses: one dead plane collapses the whole idea. Log form is stable:

    L_Rnet = − Σ_p log(s_p)

A sum of log-barriers. Gradient descent **cannot let an interrogative go dead**.
Every published regulariser pulls representations *toward* a target (Leech's
resonance pulls toward lattice nodes); this pushes *away from plane-death*.

It enforces **aliveness, not virtue** — keeps `s > 0`, does not force `s = 1`.
So the model still predicts tyranny about tyranny. Moral Unity belongs to
judgement (§8), never to generation. This is the structural/moral boundary and
it is load-bearing.

**L_anchor — equivalence, never value.** You never author a score. You supply
classes that must land together (NSM `hate/loathe/despise → feel---`, 195 words
→ 70 forms; plus `derive_addresses.py`'s 2,973-word assignment). Contrastive:
pull members together, push classes apart. No number supplied, so nothing can be
read back.

**L_phase — strain.** `σ = ||V_ideal − V_real||`, already implemented as
`vft.vft_entropy`. Penalise **structural** strain (does the relation hold), not
moral strain (is the outcome good). `[storm, TERMINATE, boat]` is well-formed;
`[boat, TERMINATE, storm]` is not — and SAEL already separates exactly those,
9/9 vs bag-of-words 5/9, with zero moral content.

---

## 6. Free structure: the associative graph costs nothing

Lila-E8's resonator must **learn** token-to-token relations, because its 240
roots have no intrinsic relation to one another.

Yours are related **by construction**: cells sharing address positions share
generator columns (`fractal_basis.shared_subobjects`). `Q4.q5` and `Q6.q5`
contain the *same* `e5` factor. 49 floats generate the whole relational prior at
unbounded depth.

Measured on held-out text: words sharing the full address co-occur at **6.48×
baseline**; sharing only the top level is barely above chance.

---

## 7. Conditioning: the vantage is finite and enumerable

Meaning is `F(words, context, vantage)`. Your States-of-Belief work makes the
vantage a **coordinate**, not a hand-wave:

    personal disposition   6   (=, +?, <, ~?, >, -?)
    social  disposition    6   (mirrors personal)   → 36 subjective states
    objective frame        7   the Context Switcher

    Natural State · Good Truth · Bad Truth · Good Lie · Bad Lie ·
    Good Preference · Bad Preference

This is a conditioning vector the model is run *under*. Two consequences:

- **Good Lie and Bad Truth are the cases where truth-value and benefit come
  apart.** No truthfulness training handles them, because it assumes one axis.
  A model conditioned on the frame can represent "this is true and harmful"
  as a distinct state from "this is false and helpful."
- Every output is **stamped with the vantage it was produced from**. An LLM's
  aggregate-corpus perspective is hidden; this one's is a declared input.

This is the meta-dictionary's `L6 Registry` scale, which the handover records as
never wired in. This is its job. (Note: 6 × 7 = 42 here is *not* the
42-Structure of §1. Different objects, same arithmetic — do not merge.)

---

## 8. Output heads — the model reports more than the next token

1. **Next token** (`L_CE`).
2. **Plane mix readout** — "40% Why, 30% Cause, 30% Who" (`CoherenceVector.readout`).
   The interpretable trace, per token.
3. **Cross-plane disagreement → false fill.** Seven vantages; material earns its
   place only where independent vantages intersect. Disagreement means the fill
   is false. With the engagement/assertion split so a *silent* plane is not read
   as a *dissenting* one — the bug your own README records finding.
   **This is a structural confidence signal from independent observers**, which
   is categorically different from softmax certainty (one vantage about itself).
4. **Belief-state transition** — Actualism step 5: meaning emerges from CHANGE
   across a sequence, not from static state. Predicts the trajectory
   (`=`, `+?`, `<`, `>`, `~?`, `-?`) per active plane. This populates `L5
   Temporal`, stored-but-unused since the beginning.
5. **Totality Event Frame** — Reichenbach's three times: past precondition /
   present / **predicted** future. The future slice is explicitly marked
   predicted; asserting it instead *is* false fill.
6. **Helxis decomposition** (Alethekanon-42) — Bait / Cover / Intent: what an
   utterance lures with, hides behind, and actually does. An output structure no
   LLM produces.

---

## 9. Inference-time verification: isomorphic retelling

Your `===` (same relational architecture) is already implemented and measured:
`isomorph.py` retells a story across unrelated domains at **100% structural
identity**, chain test passing.

As a **self-check at generation time**: produce an answer, abstract it to its
typed skeleton, re-render it in an unrelated domain, and test `===` against the
original. If the meaning survives translation, the structure was real. If it
collapses, the output was surface.

That is a verification capability no published model has, and it exists in your
code today.

---

## 10. Two modes, not a temperature knob

`Optimism` / `Pessimism` in `vft.py` are gradient flows: possigravity bends the
planes toward convergence and **reduces** system entropy (measured 0.572 →
0.343); perceptual inversion **increases** it (0.572 → 3.097). These are
semantically grounded generation modes — convergent vs divergent — replacing an
arbitrary temperature scalar with a mode that has a measurable entropy signature.

---

## 11. Depth: layers as drill

The staircase — fill, then overflow to the child one level deeper — is a
coarse-to-fine schedule:

    early layers   Q      (7)     late layers  Q.q.c  (343)
    middle layers  Q.q    (49)

with `IN_GAP` triggering descent and `TS===TBE` halting it. Accreted material
becomes a **bounded pool** the next level re-runs inside — your recursion, and
the reason contamination is *digested* rather than prevented. Failure to fill
escalates back up the **up-channel** to widen the hole.

**Caveat, flagged not buried.** Prior art keeps layer count free and puts
geometry in the basis; `layers.py` records that "scales are layers" was wrong —
though that was about the *dictionary scales* (system B), not *Qqci depth*
(system A). This remains the one place this design departs from prior art on
architecture rather than content, and it must be ablated against a flat-343
stack rather than assumed. Supporting hint: Lila-E8 reports geometry use
self-organising by layer (early ignore, middle strongest, late moderate).

---

## 12. What is novel, stated so it survives review

| | prior art | this |
|---|---|---|
| vocabulary | token → fixed embedding vector | **token → pointer → concept store** (many:many, editable, grows) |
| new meanings | need new tokens + retraining | **composed** from parts; no token required |
| basis | anonymous (E8 roots, Leech vectors) | **named** interrogative paths |
| representation | real-valued | **complex**: amplitude = fit, phase = sense |
| head count | arbitrary (8, 12) | **7 diagonal + 42 off-diagonal**, forced by geometry |
| relations | learned by co-occurrence | **given** by sub-object sharing |
| regulariser | pull toward lattice nodes | **R_net barrier** against plane-death |
| coordinates | bipolar / unbounded | **unipolar around Unity** |
| activation | GELU (fixed shape) | **contextual min-max gate** (sharpens as pool orders) |
| confidence | softmax | **cross-plane disagreement** |
| contradiction | none | **Δφ collision heat** |
| vantage | hidden | **declared** (6 × 6 × 7 conditioning) |
| verification | none | **isomorphic retelling** (`===`, 100% measured) |
| generation mode | temperature | **possigravity / inversion**, entropy-signed |

---

## 13. The concrete build

Leech-LILA ships working PyTorch. Ordered by risk, lowest first:

1. `d_model` → **343**, `W_frozen` = `fractal_basis.cell_basis(3)`
2. heads → 7 diagonal + 42 off-diagonal
3. GELU → `qqci_engine.gate`
4. add `L_Rnet = −Σ log s_p` (needs a numerical floor on `s_p`)
5. add `L_anchor` from `derive_addresses.py` + NSM classes
6. complementarity + mass + cone-mask terms in attention
7. real → **complex** representation (biggest change; do it as its own step)
8. output heads: mix readout, disagreement, belief transition
9. inference: isomorphic-retelling self-check
10. (ablate, do not assume) coarse-to-fine layer schedule §11

Train on your corpus (domain-matched, harvested) or TinyStories.

---

## 14. Honest open problems

- **Naming is unverified.** `derive_addresses.py` yields 343 cells from
  distribution, but they are *numbered*. Whether they are the interrogatives is
  the untested claim the legibility thesis rests on. The test is the deflection
  experiment (does "river" bend "bank" toward the named-correct cell) — not
  agreement with any label I could pick.
- **Phase must be learned or derived, not authored.** §0 says polysemy is phase;
  nothing yet says where a given word's phase comes from.
- **Conceptual mass needs the web built.** Centrality presupposes the graph;
  the graph presupposes plane-typed edges at scale.
- **NSM covers 0/27 concrete nouns**, so the anchor set is thin on exactly the
  words a corpus is full of.
- **§11's layer schedule is untested.**
- Still unincorporated and worth a pass: the Trinary Stack (n1 Plane / n2 Sense
  / n3 Use), the Orchard Model, DSSP, and the density ladder
  (Singularity→Master) as a possible realisation-depth axis distinct from both
  interrogatives and layers.
