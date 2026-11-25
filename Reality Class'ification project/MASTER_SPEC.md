# MASTER SPEC — The Qqci Semantic AI

Single consolidated specification, compiled after reading every source file in
this project. Every mechanism is attributed to the file it came from. Nothing
here is invented for this document; where something is unresolved it says so.

Companion documents remain authoritative in their own areas:
`fractal_llm_merged_scope.md` (long-form scope; its §19 ERRATA governs),
`The_Orchard_Model_Specification.md` (the generative programming layer),
`sael_proposal.md` (the canonical form).

---

## 0. What the system is

Language is compiled into a canonical semantic form; that form is projected onto
seven named planes of reality; the projection is gated for coherence; the result
executes as a state transition and is cached at a content-addressed coordinate.

A **word** is not a pointer and not a vector. It is a recursive object (§2.5):
a surface string with a pronunciation, collapsing to a `DefinitiveMeaning` that
many other words share, carrying a polarity, a modal position, a truth score,
**sub-meanings that are themselves full Meanings**, typed relations to other
words, a compositional identity built from its own characters, and a separate
entry per **registry × temporal × language**. A word is an alias for a *region*
of the recursive tensor, and every filler in that region expands again.

A dictionary *entry* — the routing layer — is a **bifurcated 7-plane template**
carrying both its success (virtue) and failure (sin) branch. **Learning is
population of that system, not architecture search** (scope §7): reading carves
addresses and caches them, and a new word stores only its *delta* from its
parent.

The whole thing already runs end-to-end in C# for **two semantic units**, and
the meta-dictionary that holds the recursive structure is **written to and never
read** (§2.6). Those two facts are the blocking gap.

---

## 1. The seven planes — three labels each, not synonyms

Sources: `OrchardCompiler.cs` (`PlaneOfReality`), `{Idea}.cs`
(`MoralVectorDef`), Orchard §8.7.

| | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |
|---|---|---|---|---|---|---|---|
| **Interrogative** — carves the hole, drives accretion | Who | What | Where | Why | How | Cause | Effect |
| **Plane** — type constraint on valid answers | MetaPhysical | Possible | Physical | Lyrical | Logical | Historical | Emotive |
| **Fundamental Name** — the contextual anchor, what things are relative TO | Identity | Possible | Location | Meaning | Mechanical | Historical | Emotive |
| **Axis description** | Will and Direction | Faith and Probability | Matter and Distance | Meaning and Resonance | Count and Consistency | Sequence and Causality | Passion and Consequence |
| **Virtue** | Sovereignty | Stewardship | Thriving | Truth-Telling | Wisdom | Redemption | Love/Unity |
| **Sin** | Tyranny | Greed | Mere Survival | Delusion | Sophistry | Revisionism | Parasitism |
| **Domain** | Identity | Body | Body | Mind | Mind | Soul | Soul |
| **Axis** | Driver (7th Angle) | Lateral +x | Lateral −x | Longitudinal +y | Longitudinal −y | Vertical +z | Vertical −z |
| **Dynamics** | Expansion | Expansion | Contraction | Expansion | Contraction | Expansion | Contraction |
| **Core Metric** | Directional Time | Resolution Time | Euclidean Space | Non-Euclidean Time | Computational Time | Linear Time | Energetic Time (Strain) |

The coherence gate checks all three labels **simultaneously**: is the
interrogative answered (slot filled), does the answer match the plane type
(domain coherence), is it coherent against the fundamental anchor (relational
coherence).

**Q1 is not a face.** The six paired planes are the six faces of the cube; Who
is the axis normal to it — the observer/orientation, outside and adjacent
(Cross file, 2026-07-21 01:52). This is what "7th Angle Axis" means literally.
`Who = ∫ Actions dt`: identity is *emergent from accumulated action*, not an
input (Cross, 19:13).

### 1.1 Unipolar around Unity

`{Idea}.cs` `MoralScore`: `1.0` = virtue realised, `>1.0` = **Excess** of the
sin, `<1.0` = **Deficit** of the same sin. A bipolar axis cannot express "too
much and too little are the same failure", which is the entire moral content.

### 1.2 Coherence — the Fractal Ratio Protocol

    R_net = 1 / (Who · Where · What · Why · How · Cause · Effect)

**Not a mean** (errata 19.3): a mean cannot diverge; R_net goes to infinity when
any plane collapses, which is exactly the failure the gate exists to catch.

**The gate** (`Judgement.Evaluate`):

    Y = 1        TRUTH             within tolerance of 1.0
    Insult > 1   CHAOS / TYRANNY   above tolerance
    N != 1       LIE / ENTROPY     below tolerance

**Belief Axiom** (`ProcessSynergy`): `Belief = 1 + 1 = 2`. The worldview
increments **only** on a gated TRUTH; a rejected idea leaves it unchanged.

### 1.3 Strain, and paired differencing

`FieldMath.CalculateVFTEntropy`: entropy = `|score − 1.0|`.

`StateVector.DistanceFromUnity` measures deviation **between the ends of each
axis**, not per coordinate:

    dx = (What−1) − (Where−1)      dy = (Why−1) − (How−1)
    dz = (Cause−1) − (Effect−1)    dw = (Who−1)
    σ = sqrt(dx² + dy² + dz² + dw²)

So a state equally wrong at both ends of an axis reads as *balanced*. Who,
having no pair, is measured directly. `GetShapeSignature` reads the three axes
as Expansion/Contraction, Meaning-Driven/Method-Driven, Past-Anchored/
Future-Oriented.

---

## 2. THE DICTIONARY — the central artefact

Sources: `isomorphic_dictionary.json`, `SAELIntegration.cs`, Orchard §8.4,
`implementation_plan_bifurcated_templates.md`, `implementation_plan_modal_bifurcation.md`.

### 2.1 Gardens ARE the Q-planes (Orchard §8.1)

**Not** human domain categories — the `"garden": "Physics"` in the current JSON
is superseded.

    Gardens.MetaPhysical · Possible · Physical · Lyrical · Logical · Historical · Emotive

**Garden** = namespace = the Q-plane. **Plant** = a class grown in it.
**Fruit** = a function it yields. **Seed** = a goal, a template void that drives
creation (Orchard §1).

### 2.2 Dual-layer (Orchard §8.4)

**Layer 1 — Semantic Units.** word → `Garden.Plant`. *What a word IS.*

    went → Physical.Locomotion    store → Physical.Containment
    paid → Possible.Transaction

**Layer 2 — Language Rules.** word → state modifier. *What a word DOES to the
active trajectory.* **Plane-agnostic**: they collapse or expand whatever Plant
is executing, whatever Garden it grows in.

    death → temporal_modifier −2.0      born → temporal_modifier +2.0
    on    → spatial_modifier, Where     with → relational_modifier, How
    because → causal_modifier, Cause

**Magnitude scale [−2.0, +2.0]** (Orchard §8.5): `+2.0` = Totality of
Exceedence (genesis, systemic creation); `−2.0` = Anti-Totality (death,
extinction, absolute finality).

### 2.3 An entry IS a bifurcated 7-plane template

Working code, `SaelTemplateRegistry`. Every unit carries **all seven planes**,
each split into **Success (Order/Virtue)** and **Failure (Chaos/Sin)**, each
branch carrying word + score + modal position:

    @RELOCATE
    plane   success        failure      succ  fail   succ-pos  fail-pos
    Who     active_agent   victim       1.00  1.45   Are       NotReally
    What    vehicle        terminate    1.00  1.30   Are       NotAll
    Where   destination    terminate    1.00  0.85   Are       NotReally
    Why     relocate       terminate    1.00  1.30   Are       NotReally
    How     destination    terminate    1.00  0.55   Are       NotAll
    Cause   physics        entropy      1.00  1.30   Are       NotReally
    Effect  destination    terminate    1.00  0.40   Are       NotAll

**The bifurcation IS the virtue/sin axis.** Success sits at Unity; failure
deviates into Excess (>1) or Deficit (<1) of that plane's sin. This is *why* the
geometry must be unipolar.

**It is fractal**: any slot may nest another `BifurcatedTemplate`, resolving
sub-planes `Qi.qj`. That is where depth comes from.

### 2.4 Modal position — the 2D relativity tile

`{Meaning}.cs` `GetModalCoordinates()`, confirmed by
`implementation_plan_modal_bifurcation.md`:

    CanBe  "+x,+y"   open possibility          NotAll "-x,+y"  bounded negation
                     Are "0,0"  present assertion, the anchor
    NotReally "-x,-y"  soft negation           WasLike "+x,-y"  analogical past

`InGap` is **not a position** — it is the **drill trigger**. Ambiguity descends
into a sub-frame instead of snapping (scope §5, §12.5).

Every pointer carries: `position` (ModalPosition), `magnitude` [−2,+2],
`polarity` (Neutral/Positive/Negative/Mixed).

### 2.5 WHAT A WORD ACTUALLY IS — the meta-dictionary

`isomorphic_dictionary.json` is a **flat routing index only** (Orchard §8.6). It
is the fast `word → Garden.Plant` lookup, and it is NOT the word. The word lives
in `MeaningMetaRegistry` (`{Meaning}.cs`), and it is a far richer object than a
pointer:

| field | what it carries | why it is not reducible |
|---|---|---|
| `Word` | the surface string | this is the Q1 identity, the address root |
| `DefinitiveMeaning` | **the axomic meaning** | THE COLLAPSE TARGET. Many words → one meaning. `GetByMeaning()` retrieves the whole equivalence class |
| `Pronunciation` | the phonetic layer | the Omni-Weave entry point: phonetic bigrams, cross-linguistic attestation (scope §6) |
| `Polarity` | Neutral / Positive / Negative / **Mixed** | distinct from position AND from score. Mixed = carries both, widens without net push |
| `Position` | ModalPosition + xy coords | where on the relativity tile this sense sits |
| `TruthScore` | distance from Unity | the per-vector score `MoralScore` reads |
| **`SubMeanings`** | `List<Meaning>` | **RECURSIVE. A word CONTAINS meanings**, each of which is a full Meaning with its own SubMeanings |
| **`Related`** | `List<(word, SemanticRelation)>` | typed links: `Similar / Equivalent / Derivative / Opposite` |
| `Components` (v2) | AxomicIDs at rank−1 | compositional identity: **a word IS its letters**, a phrase IS its words |
| 6 layer coordinates | AxomicID, Word, Phrase, Language, Temporal, Registry | where it is filed |

**The 6D nesting means one string is many entries:**

    [AxomicID][Temporal][Language][Phrase][Word][Registry] -> Meaning

The same word has a **different entry per Registry** (0 = General, 7 = Conflict —
the corpus's contextual dictionaries), **per Temporal** (versioning: what it
meant when), and **per Language** (the same interrogative path instantiated in a
different language plane, whose disagreement is *mixable signal*, scope §12.2).
"bank" is not one entry; it is an entry per (registry × temporal × language).

**Recursion is the point**: a word is an alias for a REGION of the recursive
tensor, and every filler is itself another Meaning. The *claims* that follow
from this are:

- **Similarity is overlapping recursive subgraphs**, not cosine distance.
- **Learning a new word stores only the DELTA from its parent**
  (`direwolf` = `wolf` + large + mythic). A node attached to the graph, not a
  new embedding.
- **Every concept is itself a coordinate system**: `R^(Q[q[c]])`, not `R^n`.

### 2.5.1 NOT USABLE: the association-list form

An earlier draft of this document reproduced the `dog` illustration from the
DSSP chat as if it were an entry format:

    DOG
      Q1 identity   mammal, canine, domesticated
      Q2 possible   bark, run, bite, protect, play
      ...

**That is pseudocode and nothing in the system can consume it.** Recorded here
so it is not mistaken for a spec again. What it lacks, measured against what
`SaelProjector` actually reads:

| the projector needs | the association list has |
|---|---|
| `successWord` / `failureWord` per plane | one undifferentiated list, no branch |
| `successScore` / `failureScore` | no scores |
| `successPos` / `failurePos` (ModalPosition) | no positions |
| a filler at each of `Qi.q1 … Qi.q7` | 3–5 loose words, unaddressed |
| tokens it can match against a parse | free-text associations |
| a state delta to execute | none |

Five words under "Q2" do not say which is `Q2.q1` and which is `Q2.q4`, so the
depth-2 address space is undefined and the recursion cannot proceed. "Then
`mammal` → warm blood, milk, vertebrate" repeats the same non-structure one
level down: it is a taxonomy sketch wearing coordinate notation.

**The usable form is the shape §2.3 already specifies** — the same shape as the
working `@RELOCATE` template: garden, plant, and per plane a bifurcated branch
carrying matchable token + score + modal position, with each sub-slot addressed.
Anything that cannot be fed to `Resolve()` and matched by `Project()` is not a
dictionary entry.

**OPEN, and it blocks noun entries specifically** (scope §17.4): the bifurcated
template is defined for *actions*, which have natural success/failure branches.
Whether a noun takes the same form is unresolved — and currently every noun
reads `INSULT` because any deficit inflates `1/product`. Judgement was defined
for an Idea (a claim); applying it to a noun may be a category error. **This
must be settled before the dictionary can be expanded to nouns at all**, and it
is not settled anywhere in the corpus.

**Never indexed by plane** (errata 19.12). A meaning HAS a Qqci form and is
STORED IN the meta-dictionary; neither derives from the other.

### 2.6 MEASURED: the meta-dictionary is WRITE-ONLY

Checked across all C# sources:

    MeaningMetaRegistry.AddMeaning   2 call sites, both in the Meaning constructor
    GetMeaning / GetByWord / GetByMeaning   DEFINED, never called anywhere
    SubMeanings   declared, initialised empty, never receives an .Add
    AddRelated    defined, never called
    Pronunciation declared, never set

So the running system **writes** every Meaning into the 6D store and **never
reads it back**, and the three fields that make a word more than a pointer —
`SubMeanings`, `Related`, `Pronunciation` — are declared and never populated.

`SAELIntegration` builds `Meaning` objects in `MapToTautonicIdea` (which
auto-registers them), then discards them. `OrchardCompiler.EmitPlantClass` takes
`(gardenName, plantName, targetPlane)` as arguments rather than reading the
registry, so Orchard §8.6's "the OrchardCompiler reads from MeaningMetaRegistry"
is a specification, not a description of the code.

**This is the gap behind the gap.** The dictionary being small (§12.1) is the
visible problem; the meta-dictionary being unread is why even a large dictionary
would still only be a routing table. The recursive structure — sub-meanings,
typed relations, per-registry and per-language entries — is specified, declared
in code, and carries no data.

---

## 3. The canonical form (SAEL)

    T = <C, alpha, Delta, sigma>

    C      Context        domain envelope           -> Q2/Q3
    alpha  Action         collapsed canonical verb  -> Q5
    Delta  Effect         the state mutation        -> Q6/Q7
    sigma  Style residue  WHICH surface form        -> Q4/Q7/Q1

Grammar: `Context :: @Action { params } -> effects`

SAEL is a **factoring, not a quotient**: the referent collapses, the manner is
retained, because saying a thing archly rather than plainly is Q4/Q7 content.
Referent stored once at its address; each `sigma` hangs off it as a cheap delta.

Two sentences are isomorphic exactly when their plane projections intersect at
the same coordinate — **paraphrase detection is free**, a side effect of the
parallax machinery.

---

## 4. The runtime (working code)

### 4.1 Wavefunction collapse — `SaelPredictiveParser`

1. Tokenise raw English.
2. Score every candidate template (action verb ×5, role ×2, plane word ×1) — the
   superposition.
3. **Collapse** to the highest scorer. If max ≈ 0, refuse: *"Wavefunction failed
   to collapse"*. The input is rejected, not forced.
4. **Predictive filling** — tokens onto parameter slots.
5. **Hole seeding**: an unfilled slot gets a `known-assumption` placeholder
   carrying the exact topological shape that slot requires (Orchard §7.1 —
   semiconductor hole generation). Absence is a carrier, not a vacuum.

Measured (`walkthrough.md`): *"Bob drove the rocket from garage to death"* →
collapse to @RELOCATE (16.0) → **(−1.00, −1.50) Greater Evil**, `INSULT > 1`.
*"bob went to the store on a rocket"* → origin hole seeded → **(1.50, 1.50)
Systemic Justice**, `Y=1 TRUTH`.

### 4.2 Projection — `SaelProjector`

Each plane's input tokenised, resolved through the isomorphic registry, matched
against the template's success/failure words. Returns
`(u, psi, planeScores, planePositions, branch)`.

### 4.3 The moral coordinate (υ, ψ), clamped to [−2, +2]

    upsilon  who benefits: everyone (+2) ... no-one else (−2)
    psi      will: do/active (+2) ... do not/suppressive (−2)

    (+1,+1) Greater Good      (−1,+1) Greatest Lie
    (+1,−1) Lesser Good       (−1,−1) Greater Evil
    (+2,+2) Systemic Justice  (−2,−2) Pure Extraction / Tyranny

### 4.4 TruthState — carve, accrete, fill, drill, escalate

`RealityClassification.v2.cs`, ported to `qqci_engine.py`.

- **Carve** at a Qqci address. **Query IS the Write**: `CarveOrRecall` returns
  the existing node (recall = the residual warp) or creates it (the query
  carves). Identity is `AxomicID = SHA256(canonical address | composition)` —
  deterministic, no random IDs, so re-asking recalls and first-asking writes.
- **Accrete**. Track **engagement** (how involved a plane is) and **assertion**
  (what it says) SEPARATELY — a weakly engaged plane is *silent*, not
  *dissenting* (errata 19.7).
- **Fill** at `TS === TBE`: coherence in band AND planes agree AND the contextual
  range has converged. Fill is **provisional** — dissenting material reopens it,
  or false fill becomes undetectable the moment it is marked resolved (19.8).
- **Drill** (`+i`, written as the dot `.`): a step must fill before it overflows.
  `rocket.position` is a drill into `rocket`'s sub-state
  (`implementation_plan_recursive_connectors.md`).
- **Escalate** (up-channel): never-fill or cross-plane disagreement at depth n+1
  reopens and widens the parent at depth n.

### 4.5 Parallax — false-fill detection

Each observer casts a **constraint ray**, not a verdict. Material earns its place
only where rays from independent vantages intersect. One-ray content is stealth.
Random rays cannot co-intersect, so noise self-filters.

**The Consideration Bin** (`Spectral_NSR_Tautonic_Upgrade.md` §3.3): a flagged
edge is NOT pruned immediately — that is a kneejerk that risks breaking valid
chains. It is soft-pruned into a bin, then Layer 1 (parallax verification by a
housekeeper) and Layer 2 (recursive drill) decide reinstate or permanent prune.

### 4.6 Possigravity — the excavation, already implemented

`FieldMath.cs`. This is the carved hole, and it predates the conversations that
"invented" it (errata 19.1):

    Phi(S) = −log P(S|Data)             the potential
    F = −grad(Phi)                       possigravity: the pull into the well
    BendTowardUnity(v, i) = v + (1−v)·i  the bend
    InvertCoordinate                     pessimism: push to extremes

**Optimism** = gradient flow toward Unity, entropy **down** (measured
0.5723 → 0.3434). **Pessimism** = perceptual inversion with variance jamming on
Where and How, deficits on What and Why, entropy **up** (0.5723 → 3.0966).

---

## 5. The shape

### 5.1 7 × 7 × 7, max depth 3, then +i

The authoritative rule (Cross file, line 6217, the user's own trigger doc):

> "the 7 planes of the Q-tensor, then each Q tensor has 7 sub-planes called the
> q-tensor, and each q-tensor has 7 sub-sub-planes called the c-tensor… The
> maximum depth is 3. The minimum depth is 1… After Q,q,c comes +i(Q,q,c) where
> i forms as the new Q step for a recursive depth drill."

Orchard §7's `7 × (6+n) × (6+n)…` reconciles with this: **6 fixed relational
axes + n dimensions of the subject**, with n = 1 giving 7. *"Semantics is the act
of collapsing this potential n into a fixed label."* A label carrying a collapsed
n, moved to a context where the actual n differs, undergoes **elastic
deformation** — the Sophist move / Reification.

**Depth 3 is measured as the optimum**, not chosen (`tautonic3.py`, 14,258 word
types):

    n   cells  retention  family gap
    1       7     0.0841    +0.329
    2      49     0.8071    +0.567
    3     343     0.8712    +0.628   <- peak on BOTH metrics
    4    2401     0.8602    +0.604   <- declines

### 5.2 Composition is the outer product

`model_concept.py`: `cell(a,b) = v_a · v_b`. Not a choice — it is what `B ⊗ B`
does to a vector. The question set at every depth is **generated**, not authored:
"what is the How of the Where of a house" is a coordinate that already exists.

**R_net compounds with depth.** At depth d each score appears `d·7^(d−1)` times,
so the depth-2 product is `P^14` and `R_net(2) = R_net(1)^14`. **Incoherence
AMPLIFIES on drill.** That is the formal justification for the staircase gate:
drilling an unfilled state does not waste effort, it explodes.

### 5.3 Typed Belief slots — the 49

`OrchardCompiler.EmitPlantClass` emits, for every Plant, seven typed slots, one
per q-sub-plane relative to its Garden. For `Physical.Locomotion` (Q3):

    Belief<MetaPhysical> Identity     // q1 of Q3: Who of Where
    Belief<Possible>     Possibility  // q2 of Q3: What of Where
    Belief<Physical>     Location     // q3 of Q3
    Belief<Lyrical>      Meaning      // q4 of Q3
    Belief<Logical>      Mechanical   // q5 of Q3
    Belief<Historical>   Sequence     // q6 of Q3
    Belief<Emotive>      Passion      // q7 of Q3

### 5.4 THE BOND RULE — inverse interrogatives

Cross file, 2026-07-20 10:50. This is the complementarity mechanism, stated
precisely:

    Q3.q4  "Where seeking Why"     +     Q4.q3  "Why seeking Where"
                              ↓
                            BOND

Empty slots are **typed vacancies** — an empty physical slot is not the same
emptiness as an empty logical slot. Two structures bond when their vacancies are
**inverse interrogatives**: `Qi.qj` pairs with `Qj.qi`.

    Bond = compatible empty relation pairs becoming defined

`Qi.qj == Qj.qi` means the functions are compatible; `===` means the bond is
structurally aligned. This is the DNA base-pairing rule, exactly specified.

### 5.5 Macro–Meso–Micro scope triad (Orchard §7.4-7.6)

Every concept is modulated by three nested scopes: **Macro** (context boundary,
"public"), **Meso** (relationship, "with"), **Micro** (entity, "john"). Focus
*rotates* as detail is appended: *"something with john"* → *"john doing
something"* pulls john into Macro. A word has **three scope multipliers**, which
is why natural-language vocabulary is so large.

---

## 6. The universal formula and the equality hierarchy

Cross file, 2026-07-20 10:12 onward.

    [state1, relation, state2]

    =     exact state match / collapsed surface statement
    ==    same functional relation
    ===   same relational architecture (the derivation is part of the identity)

`3² === 9` contains input, transformation, parameter and result; `3² = 9` hides
all but the last. **The invariant is the relation operator, not the object** —
`[fuel,consumes,fire]` ≅ `[cell,metabolises,energy]` ≅ `[economy,consumes,
resources]`. This is the same object as SAEL's `@ACTION{roles}` and AE-C's
context→action→effect.

**`===` is implemented and measured**: `isomorph.py` retells sea→startup→orbit
at **100% structural identity**, chain test passing.

---

## 7. Observer, ideal, and the definition of good

Cross file, 2026-07-21 01:57 onward. This is the evaluative core.

**The observer is another polytope.** Not outside reality — the same kind of
object. One holds the ideal ("SHOULD BE"), one the current state ("IS"):

    sigma = d(P_observer, P_reality)

compared **address by address**: `Observer.Q4.q2.c5` against `Reality.Q4.q2.c5`.
Match → σ=0. Differ → σ>0. Two people don't have different realities; they have
different observer polytopes, so they compute different strain from the same
world.

**Emotion is computed, not stored:**

    E = f(d, Δd, Ω)     d = distance, Δd = trajectory (inertia), Ω = overlap

    small d, decreasing  → contentment      large d, decreasing → hope, relief
    small d, increasing  → disappointment   large d, increasing → anger, despair

**Two strategies, one comparison:** change the model (learning) or change reality
(action). Perception, learning, planning and evaluation unify under one recursive
comparison rather than four mechanisms.

**Good and bad are dynamic and measurable** (Cross, 02:04–02:05):

    Good  ⟺  dP/dt > 0      possibility space increasing
    Bad   ⟺  dP/dt < 0      possibility space contracting

> "A good action is one that increases the future capacity for good actions."

Scales without modification: cell (metabolic options), individual (freedom of
action), organisation (diversified capability), civilisation (adaptability).
This is Q2 (Possible) changing over time, realised through Q3.

**Density is observer resolution**, not size: `R_observed = f(ρ_observer,
ρ_object)`. Higher density = more coherent relations per node. The Law-of-One
ladder maps to observer capability (D1 "something is" → D3 "I am" → D5 "I
understand why" → D7 "observer and observed are one recursive system").
**Compressed object density ≠ high observer density** — they look alike
geometrically and are opposite in function.

---

## 8. The Totality Event Frame

    Totality_Event_Frame[{when}] = [past[{when_prev}],
                                    present[{when_now}],
                                    future[{when_nextPredicted}]]
    when = [who{}, what{}, why{}, where{}, how{}, cause{}, effect{}]

The modal tile's y-axis IS the three times: `CanBe`→future, `Are`→present,
`WasLike`→past. Each plane carries its own `when` in its **own Core Metric**
(§1) — `who_when` is Directional Time, `cause_when` is Linear Time. A single
clock was always wrong.

**Meaning is the delta** (Actualism step 5: meaning emerges from CHANGE, not
static state). The future slice is marked *predicted*; asserting it instead is
false fill. Implemented: `totality_frame.py`.

---

## 9. Rank ladder and the TBE floor

`RealityClassification.v2.cs` `TensorRank`:

    Character (0)  the alphabet: irreducible basis, Fundamental by definition
    Word (1)       composition over rank-0
    Phrase (2)     composition over rank-1  <- SAEL tuples live here
    Meaning (3)    the contraction target

Rank-n identity derives compositionally from rank n−1: **a word IS its letters, a
phrase IS its words**. Meaning-finding is **contraction down the ladder**, which
scope §12.3 notes is *"mathematically the same operation attention performs
(query-key contraction), performed over structured named ranks instead of learned
keys."*

Seeding an alphabet makes "fundamentals are hit" an **enumerable membership
test** rather than a philosophical claim (§8 update).

---

## 10. Code inventory

### C# — the reference implementation

| file | what | status |
|---|---|---|
| `{Idea}.cs` | MoralVectorDef (42-Structure, Domain/Axis/Dynamics), Belief, Idea, R_net | complete |
| `{Meaning}.cs` | Meaning, 6D MeaningMetaRegistry, Judgement, ProcessSynergy, GetModalCoordinates | complete |
| `FieldMath.cs` | Possigravity, resolution time, entropy, gradient flow, 14 methods | complete |
| `StateVector.cs` | paired-axis differencing, shape signature | complete |
| `Optimism.cs` / `Pessimism.cs` / `IOperationMode.cs` | the two modes | complete |
| `RealityClassification.v2.cs` | TruthState, QqciAddress, CarveOrRecall, Alphabet | complete; **still uses mean for Net** (errata 19.3 unfixed here) and O(n) scan in `Contract` |
| `SAELIntegration.cs` | parser, environment, isomorphic registry, bifurcated templates, projector, wavefunction parser, hole seeding | **working end to end, 2 templates** |
| `OrchardCompiler.cs` | emits Plant classes into Garden namespaces | complete |
| `isomorphic_dictionary.json` | the dictionary | **2 units, 17 pointers** |

### Python

| file | what | status |
|---|---|---|
| `vft.py` | faithful port of Idea/StateVector/FieldMath/modes | done |
| `qqci_engine.py` | engine port; meta-registry de-plane-indexed this session | done |
| `sael.py` / `isomorph.py` / `domains.py` / `experiment.py` | symbolic retelling | **PASS, measured** |
| `fractal_basis.py` | Kronecker basis, sub-object sharing, factored application | done |
| `model_concept.py` | outer-product composition, R_net depth compounding | done |
| `tautonic.py` / `tautonic3.py` | character tensor; the depth sweep | done, **negative result recorded** |
| `q4_meaning.py` | NSM reduction (195 words → 70 forms) | done |
| `derive_addresses.py` | word → Q.q.c from co-occurrence | 2,973 words, 343/343 cells |
| `dictionary_expand.py` | WordNet → 114,038 senses with reduction chains | done |
| `concept_tensor.py` | per-family typed axes | 3 families |
| `slots.py` / `primitives.py` | unification, QP processes, seed ontology | runs |
| `totality_frame.py` | the event frame | structure only |
| `qqciformer.py` | PyTorch, frozen Kronecker Q/K | trains; **ablation was a tautology** |
| `qqci_lm.py` / `observer_field.py` | engine-as-LM, observers over a field | underperform baseline |

---

## 11. What is measured

| result | number | source |
|---|---|---|
| Depth optimum is 343 (peak, declines at 2401) | retention 0.871, family gap +0.628 | `tautonic3.py` |
| Depth is load-bearing (held out) | 683 → 521 → 398 → **307** ppl per level | `validate_depth.py` |
| Depth-3 named cells vs random | p = 0.0099, z = −8.25, **0/100** random beat it | `validate_depth.py` |
| Depth-1 (flat 7) vs random | p = 0.75 — **worse than random** | `validate_depth.py` |
| Shared full address → co-occurrence | **6.48×** baseline | `validate_depth.py` |
| Isomorphic retelling cross-domain | **100%** structural identity | `RESULTS.txt` |
| SAEL vs bag-of-words, role reversal | **9/9 vs 5/9** | `RESULTS.txt` |
| Operators avoid operators (valence) | 0.34× base, z = **−19.6** | `EXPERIMENTS.txt` |
| Crash scenario moral coordinate | (−1.00, −1.50) Greater Evil, INSULT>1 | `walkthrough.md` |
| Optimism vs Pessimism entropy | 0.572→0.343 vs 0.572→3.097 | `VFT_RESULTS.txt` |
| Spelling as semantic anchor | +0.042 gap = **noise** | `tautonic3.py` |
| Frozen Kronecker basis = optimal SVD-343 | identical — but a linear-algebra identity, not evidence | `bottleneck_test.py` |

---

## 12. What is missing

1. **The dictionary has 2 units.** Everything else works and has nothing to run
   on.
1b. **The meta-dictionary is write-only** (§2.6). `SubMeanings`, `Related` and
   `Pronunciation` are declared and never populated; the read methods are never
   called. Without this, a word is a routing entry rather than a recursive
   object, and expanding the dictionary alone would only produce a bigger
   routing table. **This is the gap behind the gap.**
2. **Causal links: zero.** `SemanticRelation` has four types
   (`Similar/Equivalent/Derivative/Opposite`), none populated, and **none of
   them is causal** — so "linked by causality" has neither data nor an edge type.
3. **Plane naming unverified.** `derive_addresses.py` yields 343 *numbered*
   cells; the dictionary yields *named* families; nothing connects them. The
   legibility thesis rests on this and it has never been tested.
4. **The bond rule (§5.4) is specified and unimplemented.**
5. **σ (style residue) is specified and unbuilt.**
6. **`n` in `(6+n)` is unimplemented** — everything assumes fixed 7.
7. **Q4 slot question open** (sael §6.2): explicit reason parameter vs σ-only.
8. **Judgement on nouns** (scope §17.4): every noun reads INSULT, because any
   deficit inflates 1/product. May be a category error to judge a noun at all.
9. **`RealityClassification.v2.cs` still uses the mean** for `CoherenceVector.Net`
   — the fix exists only in Python.
10. **L4 Language, L5 Temporal, L6 Registry** scales partly wired.
11. **Unread**: `Neurosymbolic Program Synthesis.pdf`,
    `curved semantics transformers.pdf`.

---

## 13. Build order

1. **Expand the dictionary.** For every semantic unit: garden (Q-plane), plant,
   7 planes each bifurcated success/failure with word + score + modal position;
   plus Layer-2 modifiers. Material available: WordNet (114,038 senses already
   expanded with reduction chains), NSM (195→70), the corpus (6M tokens).
   Everything else waits on this.
2. **Populate `SemanticRelation`**, adding a causal edge type.
3. **Implement the bond rule** — `Qi.qj` seeks `Qj.qi`.
4. **Connect named families to the 343 addresses**, then test the naming claim.
5. Port the R_net fix and engagement/assertion split back into the C#.
6. Implement σ, then `n`.
7. Only then, the trained model.

---

## 14. The rules (violating these has cost whole sessions)

- **READ THE SOURCE.** Possigravity, the moral poles, R_net, the modal
  coordinates and the language rules all already existed and were all reinvented.
- **Never test flat 7.** Measured worse-than-random. The operative unit is Q.q.c.
- **Do not hand-author plane scores and report the result as a finding.** It is
  the input read back.
- **The meta-dictionary is not plane-indexed.**
- **Pair every "distinctness" metric with a "does it track meaning" metric** —
  retention 0.87 looked great and measured spelling.
- **The several sevens are different objects**: interrogatives, densities,
  trinary stack (n1 Plane / n2 Sense / n3 Use), who-benefits. Coordinated, never
  merged.
- **Prefer the user's own corpus** over external datasets.
