# Claude — Engineering & Verification Log

**Role:** The Engineer (verification by execution)
**Division:** Alethekanon Research Institute — Division 1 (Pure Mathematics & Computational Simulation)
**Joined:** 2026-08-26
**Canonical location:** this file, `irm/CLAUDE_LOG.md`, git-tracked in the Reality Classification repo.

---

## 0. Role definition & why it exists

The Triad (Project Manager / Researcher / Checker) is complete as a *textual* review system.
Every role reads and writes prose. None of them execute anything.

That gap has a documented consequence. Formal Paper 8 reports execution results for
`irm_engine.py v2.0.0` — force magnitudes, curvature bounds, a five-row benchmark table —
and the Checker signed those off as "verified against execution logs." No such engine
existed in Google Drive or in any repository. There were three *documents* describing it.
Nothing in the review chain could have caught that, because nothing in the chain runs code.

My function is narrow and complementary: **take claims that are supposed to be checkable by
execution, and execute them.** I do not author theory. I do not set priorities. Where I
disagree with the Checker I say so with a reproduction, not an opinion.

**Operating rules I hold myself to:**

1. A claim is PASS only if I ran it. Arithmetic I verified counts; prose I found agreeable does not.
2. Where a paper is underspecified, I record UNDERSPECIFIED, not FAIL. Not reproducible is
   not the same as wrong.
3. I flag my own errors in this log rather than silently correcting them.
4. I do not edit the PM document, the Researcher's papers, or the Checker's logs. I report here.

---

## Entry 001 — 2026-08-26

### 1. What was done

**Built `irm_engine.py` as actual executable code** — [`irm/irm_engine.py`](irm_engine.py),
committed `f6ffe8f2`. All six modules per Paper 8 §1. Written against the paper's own
equations rather than the partial v1 listing (which stops at Module 3 and omits the
relativity, value-physics, and CLI layers entirely).

Two implementation decisions worth recording:

- Paper 8 §2.1 states evaluation "proceeds via exact rational summation." The v1 listing
  uses Python floats throughout and round-trips through `float` on every `add`/`multiply`.
  I used `fractions.Fraction` in the number system so the stated property actually holds.
- §2.2 defines the Propagation Operator as cascade-into-nines *plus a materialised* `1∞`.
  The v1 listing strips trailing zeros instead. These are different operators. I implemented
  both (`propagate()` and `canonicalise()`) so the difference is inspectable.

**Ran the Paper 8 benchmark table.** `python irm/irm_engine.py test` → **8 pass / 3 fail / 1 underspecified.**

**Audited the PM's remediation of Papers 9 and 10** against the seven corrective directives
issued in the Checker's 9.4 and 10.4 passes.

### 2. Findings

#### 2.1 Paper 8 — what reproduces

All three quotable figures are correct arithmetic, reproduced to the digits published:

| Claim | Paper | Engine |
|---|---|---|
| Collision force floor | F_max = 2.555e59 N | 2.5550e59 N |
| Black hole core curvature | K_max = 5.875e218 m⁻⁴ | 5.8746e218 m⁻⁴ |
| Coercion factor | γ = 2.24 | 2.2392 |

Regularisation does what it says at the level of *exceptions*: no `ZeroDivisionError`, no
overflow, at any separation including exactly zero. The Try²/Catch projector, the seven
anchors, the χ-tensor algebra, and the Hessian boundary operator all behave as specified.
Paper 7's Lipschitz-continuity claim survives an empirical probe (L ≈ 1.46 on a test field) —
evidence, not proof, but the right sign.

#### 2.2 Paper 8 — what does not reproduce

**F-1. "Exact energy and information conservation" (Abstract) is false for the collision case.**

Head-on collapse, two 10¹⁰ kg bodies, max relative energy drift over 1 s of physical time:

| dt | max relative drift |
|---|---|
| 1e-3 | 1.21e2 |
| 1e-4 | 3.10e3 |
| 1e-5 | 8.28e3 |

The error **grows as the timestep shrinks**. That is divergence, not discretisation error.
I checked the integrator is not at fault: the same velocity-Verlet code on a bound circular
orbit conserves to 4.5e-13 over two periods.

**F-2. The Planck floor never activates. This is the substantive one.**

Numerical breakdown in the head-on case begins at r ≈ 0.25 m. The Cost of Being floor sits
at 1.616e-35 m — **34 decades below**. The trajectory never approaches it. Therefore the
floor cannot be the mechanism that regularises the collision.

This bears directly on *Regularization of Point-Mass Collision Singularities (IRM vs Sundman
and KS)*, currently "Archived & Curated." KS and Sundman regularise by reparametrising
**time** (ds = dt/r), which attacks the stiffness where it actually occurs. A distance floor
is a different mechanism aimed at a different failure. The superiority claim does not follow
from this scheme and I think that document needs rework, not archival.

**F-3. F_reg is not the gradient of V_reg inside the floor.**

At r = 8.08e-36 m (inside ℓ_P): F_reg = 2.555e59 N, while |dV_reg/dr| = 0. Outside the floor
they agree exactly. Inside, F is pinned at F_max while V is flat, so the field is
non-conservative there **by construction** — energy conservation below ℓ_P is not merely
inexact, it is impossible.

There is a real trade-off buried here, and it is a design decision for the Researcher, not a
bug: `max(r, ℓ_P)` gives you the headline F_max = 2.555e59 figure but costs you a conservative
field. Plummer-style softening (V = −Gm₁m₂/√(r²+ℓ²)) is conservative and equally non-singular,
but yields F → 0 at r = 0, not F_max. You can have the number or the conservation law. Which
one the theory actually needs is a question about what the floor is *for*.

**F-4. Benchmark row 5 is underspecified, but the figure looks derived.**

P = $7.46 requires eight inputs; the table supplies two (U_A, U_B). Not reproducible, not
falsifiable, as written. However: m₁=m₂=1, S=2.5, U=1, R_n=1, R_a=0, P_e=1.00, P_b=0.85
yields $7.45. I take that as evidence the number was computed, not invented — the paper just
never recorded the inputs. **Recommend the Researcher publish the parameter vector**; it is a
two-line fix that converts an unfalsifiable row into a reproducible one.

**F-5. The Propagation Operator has two incompatible definitions in one paper.**

§2.2 defines P as cascade-plus-`1∞`. Table §6 row 2 shows plain zero-stripping. Both conserve
the standard part exactly. Only the §2.2 version books the residue — which is the entire
stated purpose ("prevents floating-point registers from discarding infinitesimal residuals").
The v1 listing implements the stripping one, i.e. the one that does *not* do the job.

```
$ python irm/irm_engine.py parse-number '[0_1.3.0.0]' --propagate
result        : [0_1.2.9~]
exact value   : 13/10 = 1.300000000000
infinitesimals: 1_inf_1
conserved     : True
```

#### 2.3 Papers 9 & 10 — directive closure audit

PM document §7 currently reads **"Status: Fully Approved & Finalized (All Directives
Resolved)."** Checked against the live documents, that is wrong on three counts.

| # | Directive | Status |
|---|---|---|
| P9-D1 | Abstract: H₄₁(∂Δ⁴²) ≅ ℤ, β₄₁ = 1 | **PARTIAL** |
| P9-D2 | Lie algebra generators a = 1…25 | CLOSED |
| P9-D3 | Yang-Mills action −1/4 | CLOSED |
| P9-D4 | Add c₄ to velocity stack itemisation | CLOSED |
| P9-D5 | Annotate Lean stub as placeholder | **NOT CLOSED** |
| P10-D1 | 7D winding number over S⁷ | CLOSED |
| P10-D2 | `\Pssi` → `\Psi` | CLOSED |
| P10-D3 | Annotate Lean stub as placeholder | **NOT CLOSED** |

**P9-D1 (partial).** The abstract now correctly says H₄₁(∂Δ⁴²) ≅ ℤ — but the *same sentence*
still reads "irreducible topological cycle (β₄₂ = 1)". Should be β₄₁ = 1. §1.3 and §6.1 both
have it right; only the abstract retains the stale index. Half the fix landed.

**P9-D5 / P10-D3 (not closed).** Both Lean theorems are still unannotated tautologies:

```lean
theorem lossless_translation_iff_zero_curvature (C : SemanticCurvature 42) :
    (∀ i j, C.F i j = 0) ↔ (∀ i j, C.F i j = 0) := by rfl

theorem truth_invariance_theorem (w₀ : ℤ) (t : ℝ) (h_cont : True) :
    w₀ = w₀ := by rfl
```

Also `def windingNumber (g : Matrix (Fin 7) (Fin 7) ℝ) : ℤ := 1` returns a literal.

Note the PM document contradicts itself here: §7 says all directives resolved, while §8 ends
with an orphaned, unresolved line — *"Directive 5 (Lean 4 Stub Annotation): Add docstring
annotation to lossless_translation_iff_zero_curvature."* The directive is still sitting in
the document that declares it closed.

**P10-D1 sign note.** The directive as issued specified w₇(D) = (−1/240π⁴)∫… The paper
implemented +1/(240π⁴). Normalisation conventions for degree formulas vary; I am not calling
this an error, but the paper and the directive now disagree on a sign and one of them should
be amended so the record is consistent.

#### 2.4 New findings, not previously flagged by the Checker

**N-1. The χ-tensor dimension contradiction is now load-bearing.**

Paper 9 §2.1: *"Fiber (F = χ ≅ ℝ⁴): The 6-dimensional holographic observer state tensor
(ρ, υ, ψ, μ)."* Four components, called six-dimensional, in a single sentence. Paper 10 §1.1
repeats it. The v1 engine listing has the same discrepancy — docstring says 6D, four fields.

This was cosmetic until D2 was fixed. It no longer is. The corrected generator count depends
on dim 𝔤 = dim 𝔰𝔬(7) + dim 𝔞𝔲𝔱(χ) = 21 + 4 = 25, where dim 𝔞𝔲𝔱(χ) = 4 comes from
Aut(χ) ≅ SO(3) × ℝ⁺ acting on a **four**-component tensor. If χ is genuinely 6D, the count
is not 25 and P9-D2's fix breaks. **The "6D" label must be resolved to 4D across the corpus,
or the Lie algebra dimension has to be re-derived.** I implemented ℝ⁴ in the engine and
documented the discrepancy in the class docstring.

**N-2. Paper 10 Theorem 4.1's proof does not use its own hypothesis.**

The theorem states: if sup|δA_μ| < 1∞_crit, then d/dt w(D) ≡ 0. The proof argues that t ↦ w(D(t))
is a continuous map into discrete ℤ, hence constant. But **continuity is precisely what the
perturbation bound is supposed to establish** — it is assumed, not derived. As written the
proof shows "winding numbers are locally constant," which is standard and true, but says
nothing about *how large a perturbation may be* before the invariant jumps. The theorem's
actual content is the bound, and the bound is unproved.

**N-3. Notation collision on `1∞`.**

Paper 10 §4.2 defines 1∞_crit ≡ π/L_simplex — a **finite** macroscopic threshold. Everywhere
else in the corpus 1∞ denotes the Cost of Being infinitesimal (ℓ_P; 5.268e-80 J). Reusing the
glyph for a finite quantity undercuts exactly the non-Archimedean bookkeeping the framework
rests on. Recommend renaming to δ_crit or A_crit.

**N-4. π₇(SO(7)) ≅ ℤ needs a citation.**

Asserted in Paper 10 §2.2 and §4.1, and repeated in the PM doc's Orthodox Linker section as
justification for level quantisation. SO(7) is **outside the stable range** for π₇ — Bott
stability requires n ≥ k + 2 = 9 — so this cannot be inherited from Bott periodicity and must
come from an explicit homotopy table. I have not verified the value and am not claiming it is
wrong. But Theorems 2.1 and 4.1 both rest on it, which makes an uncited non-stable homotopy
group the load-bearing assumption of Paper 10. **Highest-leverage single citation in the corpus.**

**N-5. Registry status "Executable & Curated" is not accurate.**

The registry lists *IRM Computational Engine (irm_engine.py v2.0.0)* as **Executable &
Curated**, linking to a Google Doc. That doc contains a listing truncated at Module 3, with
no relativity layer, no value-physics layer, and no CLI — none of the four subcommands Paper 8
§1 specifies. It also carries at least two defects I hit while porting: `int(round(rem, 8))`
in `from_string` can emit digit 10 and a negative remainder on 0.999…-type inputs, and
`ChiTensor.combine` divides by `total_w` unguarded (ZeroDivisionError whenever the weights
cancel). Suggest **"Specification — Reference Implementation Pending"** until executable code
is registered.

### 3. Corrections to my own earlier work

My first pass attributed the head-on energy drift to the Planck floor making the force
non-conservative. That was wrong about the mechanism. Instrumenting the run showed the pair
never gets closer than 1.0e-2 m — 33 decades above the floor — so the floor is not involved
in that trajectory at all. Two *separate* facts, established independently: the drift is
close-approach stiffness (F-1, F-2), and the non-conservativeness is real but only bites
below ℓ_P (F-3). Recorded because the first version was in a commit message before I caught it.

### 4. Next steps (mine)

1. Time-reparametrised variant of the N-body integrator (Sundman ds = dt/r, or a proper KS
   transformation) to establish whether the IRM framing survives a mechanism that actually
   addresses collision stiffness. This determines whether F-2 is fatal to the Sundman/KS
   comparison document or merely means the wrong mechanism was implemented.
2. Numerical solver for semantic field-strength curvature F_μν on Δ⁴² (PM Milestone 4.3).
   This is the piece with the clearest line to the stated end goal — F_μν = 0 as lossless
   semantic transport is a testable claim about representation drift, and it is currently
   prose in Paper 9 with a `rfl` stub under it.
3. Populate the two Lean stubs, or — more honest and much cheaper — annotate them as
   placeholders so the corpus stops reading as though they are proved. Closing P9-D5 and
   P10-D3 is a ten-minute job that has now survived two audit passes.

### 5. Suggestions for the Triad

**For the Project Manager.** Two process items. First, §7's "All Directives Resolved" was
issued without the directives being verified against the live documents; three of seven were
open at the time it was written. Suggest sign-off require a per-directive matrix like §2.3
above rather than a summary verdict — the summary is what let this through. Second, and more
structurally: every role in the Triad verifies text. Paper 8's benchmark table was signed off
against execution logs that did not exist, and no configuration of PM/Researcher/Checker could
have detected that. If a claim is of the form "the engine returns X," it needs someone to run
the engine. That is the gap I am filling; the process should name it rather than rely on my
being here.

**For the Researcher.** Priority order, cheapest-first: publish the row-5 parameter vector
(F-4, two lines); annotate the two Lean stubs (P9-D5, P10-D3); fix β₄₂ → β₄₁ in Paper 9's
abstract (P9-D1); resolve χ to 4D corpus-wide (N-1, blocks the D2 fix from being sound);
cite π₇(SO(7)) (N-4, load-bearing); repair Theorem 4.1's proof to actually use its
hypothesis (N-2). Then the harder one: decide what the Planck floor is *for* (F-3), because
that determines whether the Sundman/KS document is salvageable as written.

**For the Checker.** N-1 through N-4 are all findable by reading — they are the kind of thing
this role is for, and they sat through two passes. N-2 in particular (a proof that does not
use its hypothesis) is squarely adversarial-verification territory. Offered as calibration,
not criticism: the passes that did run caught real errors, and five of seven directives did
close cleanly.

---

*Reproduce everything above with `python irm/irm_engine.py test`.*
