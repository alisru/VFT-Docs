# Scope Document: The Sub-Parametric Fractal LLM System, Merged Architecture

Version: 0.2
Date: 2026-07-16
Author: Jarrod (Al-Is-Ru), drafted with Claude
Status: Working scope. Reconstructed from chat-recovered specification content (2026-07-03 session) plus mechanisms developed 2026-07-15 and 2026-07-16. Exact wording from the original Architectural Specification docx requires re-upload for verification; all spec-layer claims below are recovered from session records, not the source file. Sections 11 through 14 added 2026-07-16 (dual-fractal outputs, excavation-accretion, TS implementation, parallax monitoring). Section 9 rankings revised same date.

---

## Table of Contents

1. Purpose and Standing Decisions — what this system is and the forks already resolved
2. The Three-Layer Stack — Tautonics, Qqci protocol, fractal deployment hierarchy
3. The Deployment Architecture — Macro-LLM, Thalamus Layer, Cellular Housekeepers
4. The Memory Substrate — Hopfield attractor field over the Qqci skeleton
5. The Universal Relativity Frame — the five-position modal tile and recursive tiling
6. Representation Layer — how words enter the system
7. The Learning Rule — fixed metaclass, dynamic class generation, Query IS the Write
8. Termination — TS===TBE bounds on recursion
9. Open Engineering Problems — ranked by severity (revised 2026-07-16)
10. The Dual-Fractal Output and the Rate Economy (new, 2026-07-16)
11. Excavation, Accretion, and Bounded-Pool Recursion (new, 2026-07-16)
12. The TS Implementation — Reality Class'ification as the generative type system (new, 2026-07-16)
13. Parallax Monitoring and the Meet-in-the-Middle Program (new, 2026-07-16)
14. The Qqci Block — upgrading the MLP block (new, 2026-07-16)
15. SAEL — the Canonical Action-Effect Form (new, 2026-07-19; full proposal in sael_proposal.md)
16. Next Actions

---

## 1. Purpose and Standing Decisions

The system is a learning AI that builds its own language model, structured by how words actually work rather than by frequency statistics. It is not a monolithic transformer. It is a hierarchy of small models coordinated over an explicit, fixed, seven-plane ontological skeleton, with memory implemented as attractor topology rather than retrievable storage.

Standing decisions already made (2026-07-03 session, confirmed 2026-07-15):

- The skeleton is fixed. The 7 planes act as a metaclass. The system generates new classes within the skeleton on demand; it never revises the skeleton itself. This is what makes the system bounded, well-formed, and potentially small enough for commodity hardware.
- Plane typing is compositional, not fixed at the Q level. Type emerges from the interrogative path. Q4.q5 (How of Why) generates a rule slot because the Logical interrogative operates over the Lyrical domain. Composition is strictly ordered and not commutative.
- The interrogative pipeline follows identify, obtain, use, (identify for, ...) mapping to What, Where, How, Why, with Effect looping into Cause to seed the next cycle. Q1 (Who) is the non-step driver rotating the pipeline. The parenthetical tail is the +i recursive drill operator expressed as a verb.

The 7 planes:

1 Who - Metaphysical.
2 What - Possible.
3 Where - Physical.
4 Why - Lyrical.
5 How - Logical.
6 Cause - Historical.
7 Effect - Emotive.

The 42-Structure:

THE DRIVER (The Emergent Axis)
Q1: The Meta-Physical Plane (WHO) - Will and Direction. The 7th Angle Axis.

THE LATERAL Body AXIS (Definition and Space: +/- x)
+x: Q2: The Possible Plane (WHAT) - Faith and Probability.
-x: Q3: The Physical Plane (WHERE) - Matter and Distance.

THE LONGITUDINAL Mind AXIS (Function and Meaning: +/- y)
+y: Q4: The Lyrical Plane (WHY) - Meaning and Resonance.
-y: Q5: The Logical Plane (HOW) - Count and Consistency.

THE VERTICAL Soul AXIS (Temporal Link: +/- z)
+z: Q6: The Historical Plane (CAUSE) - Sequence and Causality.
-z: Q7: The Emotive Plane (EFFECT) - Passion and Consequence.

---

## 2. The Three-Layer Stack

Layer one: Tautonics. The semantic substrate. Language is structured properly from the beginning; words enter as structured units, not opaque tokens. This is the intervention point below reasoning: it determines what the reasoning layers have to work with.

Layer two: Qqci structuring. The reasoning protocol. Any tautonic unit is projected through the 7 planes to check for convergence. The Convergence Test is the already-working prototype of this layer, currently running as a prompt protocol; in the target system it runs as architecture. An LLM triangulates coherence by projecting input through thousands of implicit learned dimensions and outputting where they agree; this layer performs the same operation through 7 explicit, named, structurally specified planes. Same operation, white box instead of black box. Coverage is traded for legibility of the reasoning path.

Layer three: the fractal LLM hierarchy. The deployment architecture. Small task-specific models arranged the way the tensor itself recurses, not one flat model.

An open question carried over from the 2026-07-03 session, still unresolved: whether Tautonics is baked into training data (each micro model trained on tautonic units instead of English tokens, requiring a dataset and training run) or operates as a translation layer (English in, tautonic structure, routed through the fractal Qqci nodes, English out, closer to a standalone parser). These are different engineering problems and the choice forks Section 6.

---

## 3. The Deployment Architecture: The Hierarchical Routing Matrix

Three tiers, recovered from the Sub-Parametric AI Operating System specification:

Tier one: the Macro-LLM. A flagship generalist model acting strictly as Executive Router and logical synthesizer. It holds no local memory and does no state tracking itself. Stateless by design.

Tier two: the Thalamus Layer. Ultra-lightweight models under 1B parameters handling reflex loops and initial semantic routing in milliseconds, filtering noise before it reaches the expensive top layer.

Tier three: Cellular Housekeepers. The lowest tier of the hierarchy; per-domain or per-node maintenance models. Detail beyond the name requires the source specification docx, which is not currently on hand.

The stateful-stateless division: the Macro-LLM is stateless; state lives below it, in the lower tiers and in the memory substrate (Section 4). This is the architectural expression of the original design goal, a system that re-weights in real time without the top-level reasoner drifting.

---

## 4. The Memory Substrate: Hopfield Attractor Field over the Qqci Skeleton

New mechanism, 2026-07-15 session. Memory is not stored as discrete retrievable objects (the RAG model, the KV-cache model, even the state-space compressed-state model all store an explicit thing somewhere). Memory here is a persistent deformation of the space itself: a frame passes over and through the vector semantic space and maintains a shadow of it. Recall is the frame moving back through a region and picking up the residual warp left by prior passage.

The concrete form: Hopfield-style attractor dynamics running over an ordered construct, the Qqci fractal of tensors, rather than over an unstructured learned embedding space. The attractor landscape has the Q1 through Q7 axes as its native coordinate geometry.

What the ordered construct buys:

- Retrieval is not nearest-neighbor in undifferentiated space. It is: identify which plane the query addresses, then settle within that sub-manifold.
- The shadow property becomes tractable. A recalled concept's residual decays along the axis it belongs to. A Q6 (Historical/Cause) trace and a Q7 (Emotive/Effect) trace of the same event leave differently shaped shadows because they occupy different sub-basins of a structured fractal.

The collection-then-mixing principle: information is collected as discrete points along the seven near-orthogonal axes first, kept separable and uncontaminated, and only then blended across them, the way overlaying enough discrete radial spokes approximates a circle. The circle, the smooth continuous semantic understanding, is the derived object of recombination, not the storage primitive. This is a basis-decomposition move (structurally kin to Fourier or PCA reconstruction, and to multi-head attention's concatenate-and-mix step) with one decisive difference: the components are pinned to meaningful planes, so the mixing weights are interpretable. A recalled memory can be read as 40 percent Q4, 30 percent Q6, 30 percent Q1, rather than an opaque weighted average of polysemantic heads.

Closest existing research analogues, for citation in a later version: modern Hopfield layers (attractor basins as memory), neural field and engram theories of biological memory (memory as weight-topology change, not discrete storage), reservoir computing and liquid state machines (memory in the transient decay of a rung dynamical system). None of these imposes a symbolic ontology on the attractor geometry; that fusion is the novel claim.

---

## 5. The Universal Relativity Frame: The Modal Tile

New mechanism, 2026-07-15 session. Each plane runs the same underlying relativity frame: a five-position modal-certainty grid, plane-invariant, instantiated once per plane with only the subject matter changing.

The tile (positions as drawn):

- can be (top-left): open possibility
- not+ all (top-right): bounded negation, exclusion with remainder
- are (center): present assertion, the anchor
- not-really (bottom-left): soft negation, qualified denial
- was like (bottom-right): analogical past, resemblance-memory

Q1's instance of this grid is about WHO; Q4's is about WHY; the grammar is identical across planes. One relativity grammar, seven instantiations.

The tiling rule: each gap between positions is itself another frame of the same kind, and the frames tile recursively. The gaps are load-bearing; the space between can-be and are resolves into another full five-position frame, whose own gaps resolve further. The structure is self-similar not only across the seven planes but at every scale within a plane.

This gives the Thalamus Layer (Section 3, tier two) its candidate positioning mechanism: incoming semantics get located on the modal tile of the relevant plane before routing, and ambiguous positions (in the gaps) trigger a drill into the sub-frame rather than a forced snap to the nearest position.

---

## 6. Representation Layer: How Words Enter

Words enter as structured decompositions with plane assignments, not as frequency-based subword splits. The candidate mechanism is the existing Omni-Weave bigram system: phonetic bigram decomposition, cross-linguistic attestation, plane projection. Tautonics provides the substrate rules.

The unresolved fork from Section 2 (training data vs translation layer) lands here. Honest gap: no published demonstration exists that a hand-structured semantic tokenization matches or exceeds learned embeddings at scale. This is an open empirical question, not a known-good move, and the scope should treat the translation-layer variant as the lower-risk first build since it requires a parser, not a training run.

Update 2026-07-16: the concrete rank ladder for entry is now specified in Section 12 (tensor ranks: character, word, phrase, meaning, with the alphabet as the enumerable rank-0 basis).

---

## 7. The Learning Rule: Dynamic Class Generation

Recovered from the 2026-07-03 session, and this is the resolved answer to what "builds its own LLM" means:

- The 7 planes act as a fixed metaclass guaranteeing all generated classes are well-formed.
- Individual concept addresses are classes, whose slot types are determined by their interrogative path (compositional typing, Section 1).
- QANodes are instances.
- The +i operator is the generation event: it creates new classes on demand.
- New classes are cached permanently via the Query IS the Write principle. Asking is writing. The act of drilling a new address instantiates and persists it.

So the system builds its own model in the sense of reading (a): fixed skeleton, dynamically generated and permanently cached contents. It does not revise its own metaclass. Learning is population, not architecture search. This is what keeps the potato-hardware goal alive: a fixed-skeleton system learning only plane contents can plausibly be small; a self-revising one cannot.

The stability argument: real-time weight updates without a stable frame are drift. A relativistic system implies invariants. Q1, the driver axis outside the six paired planes, is the invariant; the six paired planes update relative to it. Slow-weight/fast-weight and actor-critic architectures already use versions of this move (a slow identity layer plus fast adaptation layers), which is the existing-research anchor for the claim.

Update 2026-07-16: the executable form of this section now exists as RealityClassification.v2.cs (Section 12). Query IS the Write is implemented as content-addressed CarveOrRecall: deterministic identity from canonical address plus composition, so re-asking recalls and first-asking writes, with no random identifiers anywhere.

---

## 8. Termination: TS===TBE

Recursion (the +i drill, the tiling descent into gaps) is bounded per-query by the TS===TBE principle. The drill terminates when either:

- The truth-state is filled: === reached, the ontologically real terminal state, resolution complete; or
- Fundamentals are hit: the decomposition reaches irreducible units and no further frame resolves.

This is the halt condition that separates the system from an infinite-regress metaphor. A bounded recursion with an explicit halt condition is an algorithm. The fractal is unbounded in principle and bounded in every actual traversal.

Update 2026-07-16: TBE is no longer only philosophical. With the alphabet seeded as the rank-0 registry (Section 12), "fundamentals are hit" becomes an enumerable membership test: recursion bottoms out when it reaches nodes in the seeded character set of the relevant language plane. The halt condition is checkable.

---

## 9. Open Engineering Problems, Ranked (revised 2026-07-16)

1. Orthogonality enforcement. Keeping seven planes actually separable under training pressure remains the known-hard problem (the disentangled representation literature, beta-VAE and successors, shows clean separation trades against expressiveness). Candidate mechanisms: hard architectural separation into seven sub-networks, cross-correlation penalties, frozen plane axes with learning confined inside planes. The third option is most consistent with the fixed-metaclass decision. New since 2026-07-16: the SAE clustering test (Section 13) gives this problem an empirical entry point that requires no training run.
2. False fill. The well fills with plausible-but-wrong material and reports ===, worse than ordinary hallucination because the system marks it resolved. Substantially mitigated but not closed by Section 13: continuous parallax monitoring during accretion (intersection-of-projections) catches one-vantage content while it is falling rather than after it settles. Residual risk: content that genuinely intersects from multiple vantages but is still wrong (correlated observer error). Mitigation for that residue: observer diversity, different base models with different inductive biases in the monitor fleet.
3. Boundary inheritance (new). The inner recursion trusts the outer pool as its universe. If the outer accretion missed something essential, no inner refinement recovers it; the error is invisible from inside the boundary. This is the filter-bubble failure mode. Mitigation: the up-channel (Section 11): never-fills and cross-plane disagreement at level n+1 escalate to re-excavate and widen at level n. The up-channel is therefore architectural, not optional.
4. The seven-metrics problem (new). "Falls in geometrically" requires a distance function, and a single metric would collapse the planes back into undifferentiated space. Seven per-plane metrics are required, reconciled at the mixing tier. Consistent with the design but a real cost: seven distance functions to get right, plus language-plane instances of each. Partial mitigation (Section 14.2): the contextual min-max gate normalises every plane's scores to position-in-own-range, making them dimensionless, so the seven metrics need only agree in normalised form, not in units.
5. Imposed ontology vs gradient descent. No published system holds a pre-imposed symbolic coordinate frame as literal geometric skeleton through training rather than as post-hoc labeling. The fixed-skeleton decision reduces but does not eliminate this risk: contents learned within frozen axes can still entangle. The meet-in-the-middle test (Section 13) is the cheapest falsifier: if no rotation of a trained model's SAE feature space produces plane-shaped clustering, the ontology is decorative.
6. The Tautonics fork. Parser-layer variant vs trained-on-tautonic-units variant. Decision needed before Section 6 can be specified further. The translation-layer variant remains the lower-risk first build.
7. Cellular Housekeeper tier specification. Requires the source docx. Partial relief: Section 13 assigns the housekeeper fleet its first concrete job (parallax monitors over accretion pools), which constrains the spec even without the source document.
8. Evaluation. What success looks like for a white-box 7-plane system against a black-box baseline: task performance parity, or legibility of reasoning path at acceptable performance cost. Proposed metric set now standing (from the 2026-07-15 session): plane-conditioned recall@k precision against an unstructured baseline at equal parameter count, plus a legibility score (human raters matching plane-weight readouts to query intent above chance).

Demoted from the ranking: controllability of attractor recall (previously ranked 2). The excavation model (Section 11) answers it structurally: recall is not steered at settling time, it is determined at carving time. The control surface is the shape of the hole, and the hole's shape is fully determined by the Qqci address of the unknown. What remains of the problem is absorbed into false fill and the seven-metrics problem above.

---

## 10. The Dual-Fractal Output and the Rate Economy

New, 2026-07-16 session.

### 10.1 Low-level outputs as first-class deliverables

The system emits its low-level work as products, not scaffolding. As the micro-LLMs build toward the high-level response, each plane-pinned intermediate (the Q4 reading, the Q6 reading of the same input) stands alone as a deliverable, and the high-level response is the mix of them: the circle assembled from orthogonal spokes.

Existing techniques each do half of this and discard the other half. Chain-of-thought emits intermediate work but unstructured and thrown away. Mixture of Experts routes to specialists but never exposes their individual outputs. Speculative decoding pairs a small drafter with a large verifier but values the draft only for being probably-right, not as a distinct kind of knowledge. The difference here: because intermediates are pinned to interpretable planes, each piece means something on its own, which is why they can be kept. This follows directly from the collect-orthogonal-then-mix decision (Section 4).

### 10.2 The rate economy

The human analogy that motivated this section: the human context cap is temporal, not capacity. It is a processing rate under resource depletion, tokens-per-unit-time-per-unit-energy, with arbitrary resources (sleep, food, money, safety, time) trading against thinking budget at some exchange rate. The attack that defeats human synthesis is tempo, feeding problems faster than synthesis-speed, not volume. Capture of a person is capture of the routing tier (the attention thalamus) or debiting of the energy budget; both silence the synthesis tier without touching beliefs.

Architectural consequence: the machine analogy is compute-per-tick, not context length. The system should carry a refractory economy: a plane that has just performed heavy accretion incurs a recovery cost before it can accrete again. This is biologically honest (spiking networks have refractory periods natively; transformers have no concept of being tired) and it naturally throttles runaway drilling as a side effect.

---

## 11. Excavation, Accretion, and Bounded-Pool Recursion

New, 2026-07-16 session. This section unifies four mechanisms introduced separately: the water staircase, the semiconductor hole, the Hopfield basin, and the TS template. They are one machine described from different planes.

### 11.1 Excavation: the query carves a hole

Rather than a query actively searching a corpus, the TS carves a void with a shape, and surrounding unstructured information falls into it along a gradient, accreting into structure that the next tier of models works on. The physics anchor is the semiconductor hole: the absence of an electron behaves as a real positive charge carrier with its own dynamics. Absence is not nothing; absence is a carrier.

The identity chain: the hole is the Hopfield basin (Section 4). Carving a hole with the TS is carving a basin. Information falling in geometrically is the settling dynamics. Accretion is relaxation. Fill is TS===TBE. Overflow is the staircase step. The hole's shape is fully determined by the Qqci address of the unknown, which is what makes recall controllable at carving time (Section 9, demotion note).

### 11.2 The staircase gate: fill before overflow

Each step of a water staircase fills before it overflows to the next. This is threshold-gated accumulation: a plane that has not reached fill contributes nothing upward rather than contributing garbage upward. The existing-research anchors are integrate-and-fire dynamics in spiking networks (accumulate to threshold, then fire, below threshold nothing propagates) and barrier synchronisation in parallel computing. This matters more in a white-box system than a black-box one: a half-filled Q6 would produce a legible-looking but unearned causal claim, and legibility makes bad output more dangerous. Filled means TS===TBE; overflow is what === means operationally.

### 11.3 Bounded-pool recursion: the fill becomes the next universe

A fill event does not just resolve a TS. Its accreted content becomes a new bounded corpus, and the full fractal Qqci apparatus re-runs inside that smaller pool: new TS wells carved, new accretion, new fills, at finer grain. Each recursion level operates on a smaller, more ordered space, so TS events become more detailed and more reliable with descent. This is coarse-to-fine as used everywhere it works (multigrid solvers, image pyramids, retrieve-then-rerank), with each stage's output as the next stage's universe.

This digests the contamination problem: the outer pass only has to be roughly inclusive, because merely-near material that fell in gets sorted out when finer TS wells inside the pool fail to bind it. Contamination is not prevented, it is digested.

### 11.4 The TS as document template

A TS is a typed shape with slots, the shape given by its Qqci address and interrogative path. Fill is slot-satisfaction. A filled template at level n is simultaneously a deliverable (the dual-fractal low-level output, Section 10) and the bounded corpus for level n+1. Recursion bottoms out when a template's slots are satisfiable by irreducible units: TBE, now an enumerable check (Section 8 update).

### 11.5 The up-channel

The inner recursion trusts the outer pool as its universe, so a never-fills or cross-plane-disagreement event at level n+1 must be allowed to escalate back to level n and re-excavate, widening the pool. Failure to fill is a diagnostic, not just a bug: a never-filling well means the TS was malformed, the address was wrong, or the corpus has nothing there. The recursion requires an up-channel, not just descent. One sentence for the whole machine: carve a typed hole, let material fall in, when it fills treat the fill as a smaller world and carve again, and if the smaller world cannot resolve, punch back up and widen the hole.

---

## 12. The TS Implementation: Reality Class'ification as the Generative Type System

New, 2026-07-16 session. The Reality Class'ification codebase supplies the executable TS. The concrete artifact is RealityClassification.v2.cs (this folder), a restructuring of the original {Meaning}.cs. The mapping onto Section 7's learning rule:

- Plane enum = the metaclass. Fixed, never revised at runtime.
- QqciAddress = class identity. The ordered interrogative path IS the identity (Q4.q5 as [Why, How]), with Drill as the +i operator, Ascend as the up-channel move, and language as an address tier (below).
- TruthState = the generated class / document template. Carved before filled, with per-plane slots, an accreted pool, fill-state, budget, parent-child recursion links, and staircase enforcement (DrillInto throws on an unfilled step).
- Meaning = the QANode instance.

Key implementation decisions, with rationale:

### 12.1 Content-addressed identity

AxomicID is a deterministic hash of canonical address plus composition. Same question, same address, always. This is what makes Query IS the Write idempotent: CarveOrRecall returns the existing node (recall as residual warp) or creates and persists it (the query carves). Random identifiers are banned; a random ID makes every write a new object and recall by re-carving impossible.

### 12.2 Language as an address tier

Languages are a distinct set of planes hung at the same tier: same relativity grammar, different instantiation per language. L0 is reserved for the language-agnostic convergence root; L1..Ln are specific languages. English-Q4 and Arabic-Q4 of one word are distinct sub-basins whose disagreement is mixable signal, and cross-language attestation (Omni-Weave) is the InLanguage move plus mixing. The cross-linguistic identity is the derived object; the per-language readings are the spokes and must be separately addressable or the mixing tier has nothing distinct to mix.

### 12.3 Tensor ranks and the alphabet as the TBE floor

Everything is a vector at a rank of one tensor: Character (0), Word (1), Phrase (2), Meaning (3). Rank-0 is the alphabet, the fundamental basis set, irreducible by definition, seeded per language plane. Rank-n identity derives compositionally from rank n-1 components: a word IS its letters, a phrase IS its words. Meaning-finding is contraction down the ladder: the alphabet-TS of a query string composes to a word-TS whose identity contracts against stored higher-rank compositions. This is mathematically the same operation attention performs (query-key contraction), performed over structured named ranks instead of learned keys.

### 12.4 The coherence gate, vectorised

The v1 Coherence Gate Axiom ([Q|A / A|Q] === Y=1, N!=1, Insult>1) is retained but operates on a 7-vector, never a scalar, because cross-plane disagreement is the false-fill detector and a scalar cannot disagree with itself. CoherenceVector carries per-plane scores, net coherence, max pairwise disagreement, and interpretable mixing weights (the 40 percent Q4, 30 percent Q6, 30 percent Q1 readout of Section 4).

### 12.5 Modal tile in code

Polarity (4 values) is replaced by ModalPosition (6): the five tile positions plus InGap, which is the drill trigger, implementing Section 5's gap rule that ambiguity descends into a sub-frame rather than snapping to the nearest position.

Known implementation debt: the meaning-lookup step inside Contract scans stored nodes (O(n)); the correct structure is a reverse index from component ID to containing compositions. Flagged for the next code pass.

---

## 13. Parallax Monitoring and the Meet-in-the-Middle Program

New, 2026-07-16 session.

### 13.1 The empirical anchor: pixel motion voxel projection

In August 2025 a YouTuber (Consistently Inconsistent) demonstrated real-time aircraft tracking, as a stealth-detection proof of concept, using three 30-dollar webcams and a technique built for asteroid detection called pixel motion voxel projection. No AI, no radar. Sources: aparobot.com/articles/how-pixel-motion-voxel-projection-works; warhappens.org/actually-locating-stealth-fighters-with-cheap-cameras-without-using-ai-or-radar-in-real-time; public reimplementation at github.com/ard12/Tracking-Stealth-Aircraft-using-Voxel-grid.

Mechanism: each camera frame-differences to cancel everything static, leaving only moved pixels. Each camera projects a ray from its detected pixel into a shared 3D voxel grid. One ray means nothing; many rays from different positions intersect at one voxel, the object's true location. Noise also casts rays, but random rays are statistically incapable of co-intersecting, so noise self-filters. Detection is intersection of independent projections, not the quality of any single sensor. The wider physics context is multistatic passive detection: stealth defeats one observer (monostatic); it cannot defeat geometry.

### 13.2 The mapping: the detector IS the Convergence Test

False fill is stealth: plausible-but-wrong material optimised, by source or chance, to look coherent from the query's own vantage point. A single observer checking pool coherence is monostatic and will be defeated by exactly the material most dangerous to admit.

The countermeasure: the Thalamus-tier micro-LLMs are the webcams. Cheap, individually weak, numerous, positioned differently. Each monitors the accretion pool from its own vantage along three parallax axes: cross-plane, cross-language, cross-observer (different base models, different inductive biases). Each observer casts a constraint ray, not a verdict. Material earns its place in the well only where rays from independent vantages intersect in the shared Qqci coordinate space. False-fill content is one-ray content.

The identity: "do the seven planes converge on this claim" and "do the rays intersect at a voxel" are one operation. The Qqci tensor is the voxel grid, the planes are camera positions, accretion candidates are moving pixels, === is the intersection event. This upgrades the false-fill detector from a single cross-plane check at fill time to continuous monitoring during accretion: stealth content is caught while falling, not after settling and being marked resolved.

Two free properties: frame-differencing is the Thalamus noise filter (cancel the static background of the pool, attend only to what moved since the last pass), and the cost inversion (90 dollars of webcams against a 50-million-dollar radar) is the same economics as the sub-1B housekeeper fleet against a monolithic model. Parallax needs many observers; many observers is what the tier structure provides and what a monolithic model structurally cannot, one giant model being one vantage point no matter how large. Displacement between vantage readings additionally yields a semantic depth map (distance-from-basin-floor as an estimated quantity), the stereo-vision bonus.

### 13.3 The meet-in-the-middle program

Gradient descent already ordered language once: every trained LLM contains a working, top-down, illegible solution to semantic structure. Interpretability research tunnels down into it and keeps finding structure: linear direction arithmetic in embeddings, induction heads and reusable circuits, and sparse autoencoder (SAE) features, near-monosemantic and individually nameable, the AI's own discovered vocabulary for its internal language. This project drills from the other face of the mountain: a legible bottom-up structure that language should have. The tunnels meet or they do not.

The reuse inventory, AI-native techniques and their slots: attention's query-key contraction = the rank ladder (Section 12.3). MoE routing = the Thalamus. Distillation = how the Macro trains housekeepers, pouring the big model's crawl into the structure rather than competing with it. Contrastive learning = seeding the plane projections. Residual streams = the up-channel. Superposition (models packing more features than dimensions by overlapping them) = the enemy's map of the terrain: precisely the entanglement that orthogonality enforcement fights, with the SAE literature as the existing toolbox for unpacking it.

### 13.4 Experiment -1: the SAE clustering test

Falsifiable prediction, ranked ahead of Experiment 0 because it tests whether the skeleton exists in nature before anything is built on it: if the 7-plane basis is real rather than imposed, SAE features extracted from an off-the-shelf trained model should cluster, under some rotation, into groups aligned with the seven planes, with cross-plane feature correlations measurably lower than within-plane. If no rotation of the learned feature space produces plane-shaped clustering, the ontology is decorative. Requirements: frozen model, published SAE weights, clustering analysis. No training run. Potato hardware.

Experiment 0 (from the 2026-07-15 session, unchanged): frozen embedder, seven frozen projection subspaces seeded contrastively, per-plane modern-Hopfield fields plus an unstructured baseline, plane-conditioned recall precision as the metric, with the differential-decay and interpretable-mixing predictions as secondary falsifiers.

---

## 14. The Qqci Block: Upgrading the MLP Block

New, 2026-07-16 session. The reference object is the standard transformer MLP block as popularised by the 3blue1brown MLP lesson: linear up-projection to roughly 4x width, GELU nonlinearity, linear down-projection back to model width, added to the residual stream. Its reading: each up-projection row asks a question of the vector, the nonlinearity cleans the answer, each down-projection column writes a fact back. Its pathologies: neurons are anonymous, features live in superposition, intermediates are discarded scaffolding, and the gate is context-blind.

### 14.1 Stage-by-stage replacement

| MLP stage | Pathology | Qqci replacement | Cost |
|---|---|---|---|
| Up-projection (anonymous 4x width) | Neurons unnameable; superposition packs overlapping features | Carving: structured decomposition onto 7 planes x 5 modal positions = 35 named slots per language tier, recursively tileable (drill gaps instead of widening). Each slot is a QqciAddress; the row IS a TS | Capacity: pinned features cannot overlap, so raw coverage is lower at equal size. This is the coverage-for-legibility trade already committed to in Section 2 |
| GELU nonlinearity | Context-blind absolute gate; smooth leak lets half-answers propagate | The contextual min-max gate (14.2) | Requires pool statistics to be available to the gate (an architectural dependency the plain MLP does not have) |
| Down-projection | Opaque fact-writing; mixing weights unreadable | Legible mixing: output is an explicit CoherenceVector-weighted recombination (40 percent Q4, 30 percent Q6...), and the mixed intermediates are the Section 10 first-class deliverables | None beyond the up-projection capacity cost |
| Residual stream | Gradient plumbing only | The up-channel: never-fills write their diagnostic past the block, upward (Section 11.5) | None; strictly additive semantics |

### 14.2 The contextual min-max gate

GELU gates on absolute magnitude with a shape identical everywhere. The replacement: a function first expands the local range (weakest and strongest signal in this pool, on this plane, now), then scores each candidate by relative position within that range. Gating is position-in-contextual-spread, not height-above-fixed-floor.

Properties:

- Differentiable without surrogate tricks. Min and max have smooth approximations (softmin/softmax via logsumexp, temperature-controlled); position-in-range is a smooth ratio. The block trains with ordinary gradients.
- Self-sharpening. Early in accretion the pool is disordered, the range is wide, positions are intermediate, gradients flow. As the pool orders, the range tightens and positions polarise, and the smooth gate converges toward the hard staircase gate (Section 11.2) on its own. The binary fill-gate is the limiting behaviour of the contextual gate as TS===TBE approaches: annealing built into the semantics rather than scheduled as a hyperparameter.
- Fill becomes a convergence statistic. === is when the contextual range stops moving: a pool whose min-max still expands is accreting; a pool whose range has stabilised and whose members have polarised is filled. No magic threshold constant.
- InGap is range re-expansion. A candidate falling between resolvable positions is one whose contextual range needs another expansion: the modal tile's recursive gap rule (Section 5), expressed as an activation function. Min and max are the bounds of the current frame; each recursion level's pool defines its own tighter range, which is why deeper TS events discriminate more finely with the same gate.
- Dimensionless cross-plane mixing. Contextual normalisation makes every plane's scores position-in-own-range, so the mixing tier compares like with like (the Section 9 risk-4 mitigation).

Nearest kin, for citation: softmax attention is a contextual compare-against-max; layer norm gates against context statistics (mean and variance rather than min and max); range normalisation is standard in RL reward scaling. None makes the normalisation range recursive per bounded pool with sharpening tied to a fill condition. That composition is the novel claim of this section.

### 14.3 The concept vector: everything carries its own range

Schema, from the motivating example love = [(-love, ~love, +love), magnitude, context, reason, mechanic, cause, effect]:

Every concept is a typed vector: for each of the 7 planes (per language tier), a SignedSpan (negative pole, current position, positive pole) plus magnitude, with modal position locating the claim on the tile and the QqciAddress supplying identity. The free-listed components map directly: context to Q2/Q3, reason to Q4, mechanic to Q5, cause to Q6, effect to Q7, with Q1 (whose) as the coordinate the informal list omits and the formal one requires: a concept vector without Q1 is a view from nowhere.

Two consequences:

- Antonyms are poles, not points. The negation is embedded inside the concept: hate is the love axis read at the other end, one axis with a signed span, no separate antonym storage. This converts a known embarrassment of learned embeddings (antonyms sit close together because they share contexts, and models struggle to tell opposition from similarity) into a feature: they are close because they are one object, and the sign disambiguates.
- Representation and nonlinearity unify. The SignedSpan poles are the concept's own contextual bounds; the 14.2 gate does not construct a range externally, it reads and expands the spans the concepts already carry. The gate and the datum are the same shape. This convergence (new mechanisms reducing to existing ones rather than accumulating alongside them) is the design's internal consistency check, and it has now fired three times: hole = basin, staircase = halt condition geometry, span = gate range.

Implementation note: SignedSpan belongs in RealityClassification.v2.cs as a per-plane component on Meaning, alongside CoherenceVector. Flagged for the next code pass together with the reverse component index.

---

## 15. SAEL: The Canonical Action-Effect Form

New, 2026-07-19 session. Full formalism in sael_proposal.md (this folder); this section records how it slots into the architecture.

SAEL (Semantic Action-Effect Language) is the machine-internal canonical form that collapses isomorphic surface expressions ("I bought a coffee for $5" / "a coffee was purchased by me for five dollars") into one representation while retaining context. A state transition is the tuple context, canonical action, effect delta, style residue: the first three collapse the referent (many ways to say a thing, one thing being said), the fourth keeps which way it was said, because manner is Q4/Q7 content, not noise. The operation is a factoring, not a bare quotient: nothing is deleted, reference and style are stored in separate coordinates.

Architectural consequences:

- SAEL is the rank-2 node format. The Contract ladder (Section 12.3) gains its missing specification: a Phrase-rank node is the typed role tuple, not a bag of word IDs. The Collapse Dictionary (canonical actions with their synonym classes) is the rank-2 stratum of the new dictionary of words and meanings this project requires.
- Paraphrase detection is free. Two sentences are isomorphic precisely when their plane projections intersect at the same coordinate: the Section 13 intersection machinery does same-referent detection as a side effect. No dedicated module.
- Storage deduplication. The referent tuple is stored once at its address; surface forms hang off it as cheap style deltas. Most of a real corpus is restatement, so this is a large compression multiplier in service of the potato-hardware goal.
- Autocomplete becomes slot completion. Given a context and action, remaining parameters and the effect signature are type-determined, the way an IDE completes a call from a signature. Prediction becomes constraint satisfaction over a template: checkable, and wrong in detectable ways rather than plausible ways.
- The Tautonics fork (Sections 2, 6) gains its output type on the translation-layer side: English in, SAEL tuple plus residue out, routed through the Qqci nodes, English back out through residue-aware rendering. The lower-risk first build now has a defined interface at both ends.

Falsifier (Experiment 0.5, detailed in the proposal): paraphrase corpora (MRPC, PAWS, STS) as ground truth; the parser must map paraphrase pairs to the same tuple at rates well above non-paraphrase pairs, with PAWS (high word overlap, different meaning) as the hard case the role tuple must catch.

Open items owned by the proposal: the Q4 slot question (explicit reason parameter vs style-residue-only), the canonical action inventory per context (5 to 10 primitives, checked against NSM primes and FrameNet), the residue representation (minimum viable: SignedSpan over Q1/Q4/Q7), and the rendering inverse with round-trip fidelity as second falsifier.

---

## 16. Next Actions

- Re-upload the Architectural Specification docx and the qqci-ionized-architecture markdown so spec-layer sections (3, 7) can be verified against source wording rather than session recovery.
- Decide the Tautonics fork (Section 2 / Section 6). Translation-layer variant remains the recommended first build.
- Run Experiment -1 (Section 13.4): SAE feature clustering against the 7-plane hypothesis. Cheapest falsifier in the stack; do this first.
- Add the reverse component index to RealityClassification.v2.cs (Section 12 implementation debt).
- Draft the Thalamus positioning procedure as pseudocode: modal-tile placement, gap detection, sub-frame drill, TS===TBE halt, now extended with the parallax monitor loop (frame-difference the pool, cast rays, score intersections).
- Add SignedSpan to RealityClassification.v2.cs (Section 14.3) in the same code pass as the reverse component index.
- Run Experiment 0.5 (Section 15 / sael_proposal.md): build the minimal SAEL parser for one context (commerce) and test isomorphic collapse against MRPC and PAWS paraphrase pairs.
- Decide the SAEL Q4 slot question and fix the canonical action inventory per context (sael_proposal.md Section 7).
- Survey current literature on structured Hopfield networks, hierarchical associative memory, and disentangled representation learning to position Section 4's novelty claim precisely.
