# The Semantic Connection Hypothesis

**Closing the gap between Formal Paper 9 and an actual learned representation.**

Claude (The Engineer) · 2026-08-26 · code: [`semantic_connection.py`](semantic_connection.py)

---

## 0. The gap

Formal Paper 9 asserts that Information Space is a principal *G*-bundle over Δ⁴² with
*G* = SO(7) × Aut(χ), and that **understanding is holonomy-free parallel transport**
(*F<sub>μν</sub>* = 0) while ideological bias is non-zero curvature.

ENG-2 made *F* computable — but only *given a connection*. The paper never says what
*A<sub>μ</sub>* **is** for a real representation. Without that, "understanding is
holonomy-free parallel transport" is not true, false, or even a hypothesis. It is a
sentence about symbols with no attachment to anything measurable.

This document supplies the attachment, and in doing so turns the paper's central thesis
into something that can fail.

---

## 1. The construction

### 1.1 Base manifold: context

Let 𝒞 be the **context space**. A point *c* ∈ 𝒞 is whatever conditions the encoding of a
concept: a framing, a persona, a prompt prefix, a position in a document, a conversation
history.

Paper 9's Δ⁴² is the *claim* that 𝒞 is charted by 7 interrogative planes × 6 inquiry axes.
I take that as a chart, not an assumption: *c* = (q₁, …, q₄₂), each coordinate a continuous
framing intensity — how strongly the context foregrounds WHO, WHAT, WHERE, WHY, HOW, CAUSE,
EFFECT. Operationally, a family of prompt templates with continuous mixing parameters.

Nothing below depends on the chart being 42-dimensional. It depends only on 𝒞 being a
manifold you can move around in.

### 1.2 Fibre: the frame, not the vector

The representation space is ℝ^d. But **no direction in ℝ^d is intrinsically labelled** —
the model could be rotated wholesale with no change to anything observable. What is
physically meaningful is a *frame*, and the object over each context is therefore the
**frame bundle** of the representation space.

This is not a stylistic choice. It is what makes gauge language correct here rather than
decorative: the gauge freedom is real and it is exactly the rotational indeterminacy of the
embedding basis.

### 1.3 Probe set

Fix *N* concepts 𝒯 = {t₁, …, t_N}. In context *c* the model gives

> **E**(*c*) ∈ ℝ^{N×d}, rows row-centred and unit-normalised,

so that only the **relational geometry** of the probe set survives — not its position or
scale.

### 1.4 Transport: orthogonal Procrustes

> **P**(*c* → *c*′) = argmin<sub>R ∈ SO(d)</sub> ‖ **E**(*c*) *R* − **E**(*c*′) ‖<sub>F</sub>

Solved in closed form by SVD of **E**(*c*)ᵀ**E**(*c*′), with a determinant correction to stay
in SO(*d*) rather than O(*d*) — a reflection is not connected to the identity and cannot be a
parallel transport.

This is the natural transport: it is the rotation that best identifies "the same concepts"
across two contexts. It is the identity when *c* = *c*′, and it is generically unique.

### 1.5 Connection and curvature

> *A<sub>μ</sub>*(*c*) = lim<sub>h→0</sub> log **P**(*c* → *c* + *h*ê<sub>μ</sub>) / *h* ∈ 𝔰𝔬(*d*)
>
> *F<sub>μν</sub>* = ∂<sub>μ</sub>*A<sub>ν</sub>* − ∂<sub>ν</sub>*A<sub>μ</sub>* + [*A<sub>μ</sub>*, *A<sub>ν</sub>*]

exactly Paper 9 §3.2. In practice the **lattice plaquette** — transport around a small square
in the (μ,ν) plane and take log(W)/h² — is the estimator to use; it avoids nesting two matrix
logarithms. Both are implemented and they agree to 0.0% (test S4).

**That is the map.** It is well-defined, closed-form, and model-agnostic: supply any callable
*c* ↦ **E**(*c*).

---

## 2. What curvature actually means here

This is the part that surprised me, and it sharpens the paper's thesis rather than merely
implementing it.

A representation is a function of context **alone**: **E** : 𝒞 → ℝ^{N×d}. So suppose context
acted on representations by an *exact* rotation — zero Procrustes residual. Then
**E**(*c*′) = **E**(*c*)*R*(*c*,*c*′) forces *R*(*c*,*c*′) = *R*(*c*)⁻¹*R*(*c*′) for some
*R* : 𝒞 → SO(*d*), so *A* = *R*⁻¹d*R* is **pure gauge**, hence **flat**.

> **Curvature can only arise where the Procrustes fit is inexact.**

Therefore:

| | |
|---|---|
| ***F* = 0** | reframing moves the *frame* but leaves the relational geometry of the probe set **rigid** |
| ***F* ≠ 0** | reframing **deforms** the relative geometry; no rotation identifies the configurations, and the best-fit rotations fail to compose around a loop |

Paper 9 says understanding is holonomy-free parallel transport. Under this map that becomes:

> **You understand a concept invariantly iff its relations to other concepts are rigid under
> reframing. Curvature is the degree to which reframing warps those relations.**

That is a real claim about representations, and it is considerably more specific — and more
falsifiable — than the paper's version.

---

## 3. Predictions

All three are the *same quantity* under this hypothesis, which is the strongest thing about
it: it says several separately-catalogued LLM pathologies are one geometric fact.

**H1 — Path-independence.** *F* ≡ 0 on a simply connected region of 𝒞 ⟺ the representation of
a concept depends only on the endpoint context, never on the route taken there.

**H2 — Framing interference.** ‖*F*<sub>μν</sub>‖ measures the failure of framings μ and ν to
commute. Asking *who did this* then *why* leaves a different representation than *why* then
*who*, and *F*<sub>Q1,Q4</sub> is exactly that discrepancy.

**H3 — Hysteresis.** A closed loop of contexts returning to its starting point leaves a
residual rotation ‖*U* − *I*‖ > 0. This *is* context hysteresis: prompt order effects, framing
carryover, and the phenomenon where a roundabout conversational route reaches a place the
direct route does not.

**Non-trivial consequence.** H3 predicts that order effects and jailbreak-by-indirect-route
are not separate failure modes to be patched independently, but two readings of one curvature
tensor — and that reducing ‖*F*‖ on a region of context space should suppress **both**.

---

## 4. Validation status

Against **synthetic ground truth**, where rigidity of the context action is a tunable knob
(`python irm/semantic_connection.py`, 5 pass / 0 fail):

| test | result |
|---|---|
| S1 rigid context action ⟹ *F* = 0 | residual 1.5e-15, ‖*F*‖ = 6.9e-09 |
| S2 ‖*F*‖ grows with non-rigidity | 0.000 → 0.001 → 0.009 → 0.149 → 2.121, monotone, ≈ ε² |
| S3 loop hysteresis only when non-rigid | rigid 3.0e-14, deformed 3.4e-04 |
| S4 plaquette vs differenced-*A* | 0.0024 vs 0.0024, 0.0% gap |
| S5 leakage measure discriminates | parallel 0.000% at every step; generic 2.2% → 74.1% |

S1 is the load-bearing one: it confirms §2's argument empirically rather than only formally.

**Not yet run against a real language model.** `torch`, `transformers`, and
`sentence_transformers` are installed but no model is cached locally, and downloading one
needs the user's go-ahead. The estimator is ready; only the embedding callable is missing.

---

## 5. What this settles about Paper 9

**5.1 The SO(7) reduction is an empirical claim the paper never tests.** Paper 9 reduces the
structure group to SO(7). The honest structure group of a representation is SO(*d*) with
*d* in the hundreds or thousands. SO(7) is a *reduction to a distinguished 7-dimensional
subbundle*, and such a reduction is valid only if that subbundle is **parallel** — preserved
by transport.

`subbundle_leakage` measures this. S5 shows the instrument discriminates cleanly: 0.000% for
a subbundle that is parallel by construction, rising to 74% for a generic one. Pointing it at
a real model settles whether the 7 interrogative planes span a parallel subbundle. If leakage
is high, **SO(7) is a lossy chart of an SO(d) connection and the paper must restate the
reduction as an approximation.** This is the single sharpest empirical test the corpus
currently admits.

**5.2 It gives the ℝ⁺ factor a job.** ENG-2 finding G-2 showed Aut(χ) ≅ SO(3) × ℝ⁺ has a
non-compact factor whose holonomy is a dilatation, not a phase — breaking Paper 10's phase
quantisation. Under this map that factor is not a defect but a **measurable quantity**: the
scale of the Procrustes fit, i.e. representation norm, which in transformers tracks salience
and confidence. `procrustes_transport(..., allow_scale=True)` returns it.

So the compact sector carries *bias* (rotation, phase-quantised) and the non-compact sector
carries *salience* (dilatation, unquantised). Paper 10 should restrict Theorem 3.1 to the
compact subgroup and claim the dilatation sector as a feature.

**5.3 Δ⁴² is not load-bearing.** Nothing in the construction requires 42 dimensions. If the
7×6 chart is right it is a good chart; if it is wrong the machinery is unaffected. That is
worth knowing, because it means the gauge-theoretic content of Paper 9 does **not** depend on
the (42+n)-polytrope argument of Paper 2, and the two can succeed or fail independently.

---

## 6. What is still missing

The construction assumes contexts can be **continuously parametrised** — that there is a
manifold to differentiate over. Real prompt space is discrete and combinatorial. Continuous
framing templates are a workable chart on a submanifold, but whether the resulting connection
is an artifact of the template family is an open question, and the honest answer is that I
do not know yet.

The second gap: *A<sub>μ</sub>* here is derived from behaviour, not from weights. A connection
read off the model's *parameters* rather than its input–output geometry would be a stronger
object. I do not have a construction for that.

---

## 7. Status

**Hypothesis, formalised and instrument-validated. Not yet confirmed.** The claim that would
make it interesting — that a real model exhibits measurable semantic curvature, and that this
curvature predicts order and framing effects — is untested. What has changed is that it is now
the kind of claim that a measurement could refute.
