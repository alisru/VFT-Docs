# Semantic Action-Effect Language (SAEL)

## A Formalism for Isomorphic Collapse and Context-Preserving Action-Effects

Version: 0.1 draft
Date: 2026-07-19
Author: Jarrod (Al-Is-Ru), core formalism; assembled with Claude
Status: Proposal start. Core formalism (Sections 1 through 5) authored by Jarrod, 2026-07-19 session. Section 6 onward: integration notes and extensions from the same session. Companion to fractal_llm_merged_scope.md (Section 16 there summarises this document).

---

In natural language and traditional programming, there are infinite ways to express the same fundamental transition. For example, "I bought a coffee for $5", "A coffee was purchased by me for five dollars", and "I paid $5 to get a coffee" all describe the exact same state transition.

SAEL is a minimal, algebraic language designed to strip away syntactic noise, collapse these isomorphic expressions into a single canonical representation, and retain the essential contextual parameters.

## 1. Core Mathematical Intuition

We define a system state transition as a triple:

$$\mathcal{T} = \langle C, \alpha, \Delta \rangle$$

Where:

$C$ (Context): The domain envelope or namespace. This answers "What semantic domain are we in?" (e.g., commerce, locomotion, communication).

$\alpha$ (Action Primitive): The collapsed, canonical action. This is the single "meaning-word" representing an entire equivalence class of isomorphic verbs.

$\Delta$ (Effect Matrix / State Delta): The actual mutation of entities or properties within the context.

### Isomorphic Collapse

Let $L$ be a natural language expression. Let $\Phi$ be a mapping function:

$$\Phi(L) \to \langle C, \alpha, \Delta \rangle$$

If two expressions $L_1$ and $L_2$ result in the exact same state change $\Delta$ within the same context $C$, they are isomorphic ($L_1 \cong L_2$). SAEL collapses them to the same canonical representation:

$$\Phi(L_1) = \Phi(L_2)$$

## 2. Language Grammar (EBNF)

SAEL is designed to be extremely compact, resembling a blend of lisp-like S-expressions and algebraic type signatures.

    Expression     ::= Context "::" Action "{" ParameterList "}" "->" EffectList
    Context        ::= Identifier
    Action         ::= "@" Identifier
    ParameterList  ::= Parameter ("," Parameter)*
    Parameter      ::= Identifier "=" Value
    EffectList     ::= Effect (";" Effect)*
    Effect         ::= Variable "=>" (Value | Mutation)
    Mutation       ::= "+" Value | "-" Value | "to" Value

## 3. The Collapse Dictionary (Mapping Isomorphisms)

To collapse synonyms and syntactic variations, SAEL maps incoming expressions to a finite set of Canonical Actions ($\alpha$).

| Canonical Action (@Action) | Collapsed Synonyms / Isomorphisms |
|---|---|
| @TRANSFER | give, send, pay, wire, hand over, donate, bequeath, pass |
| @ACQUIRE | buy, purchase, obtain, get, grab, fetch, secure, receive |
| @MUTATE | edit, change, modify, transform, adjust, tweak, update |
| @RELOCATE | go, travel, walk, fly, move, drive, run, displace |
| @TERMINATE | delete, kill, destroy, end, stop, cancel, erase |

## 4. Concrete Examples

Here is how wildly different sentences collapse into identical, clean SAEL expressions.

### Example A: Transactional Exchange

Sentence 1: "Alice paid Bob $10 for the book."

Sentence 2: "Bob received 10 dollars from Alice, and Alice got the book."

Sentence 3: "The book was purchased by Alice from Bob at the cost of ten dollars."

Collapsed SAEL Representation:

    commerce :: @TRANSFER { actor=Alice, recipient=Bob, item=Book, value=10 } ->
      Alice.balance => -10;
      Bob.balance => +10;
      Book.owner => Alice

Note: The context commerce keeps the action grounded. The action @TRANSFER handles both the physical asset exchange and the financial ledger change simultaneously.

### Example B: Physical Locomotion

Sentence 1: "I drove my car from the garage to the grocery store."

Sentence 2: "My car was relocated to the grocery store from the garage by me."

Sentence 3: "I moved my vehicle out of the garage and into the grocery store parking lot."

Collapsed SAEL Representation:

    physics :: @RELOCATE { actor=I, vehicle=car, origin=garage, destination=grocery_store } ->
      car.position => to grocery_store;
      I.position => to grocery_store

## 5. Why This Solves the Isomorphism Problem

Context-Grounding: By prefixing every action with a context (e.g., physics:: or commerce::), we don't lose the "what" of the conversation. The word "get" means different things in "I get sick" (biology) vs. "I get a package" (logistics).

Determinism: Programmatic interpreters do not need to parse 50 different verb structures. They only need to implement a parser for the 5-10 canonical action primitives per context.

Lossless Delta: Despite collapsing the phrasing, the state change ($\Delta$) preserves the exact parameters (the quantities, names, and targets) of the original statement.

---

## 6. Integration with the Qqci Architecture (session notes, 2026-07-19)

### 6.1 The missing fourth coordinate: the style residue

The triple as drafted is a pure quotient: it maps every member of an equivalence class to the class and discards which member was chosen. The design requirement established earlier in this session is a factoring, not a bare quotient: collapse the referent, retain the manner. The proposed extension is a fourth coordinate:

$$\mathcal{T} = \langle C, \alpha, \Delta, \sigma \rangle$$

where $\sigma$ (style residue) records which surface realisation carried the transition: register, ornament, word choice, emphasis. The residue is not noise; it is Q4/Q7 content (the choice to say a thing archly instead of plainly carries reason and emotive charge). Example A's three sentences share $\langle C, \alpha, \Delta \rangle$ and differ only in $\sigma$: sentence 3's passive-formal $\sigma$ signals distance; sentence 1's direct $\sigma$ signals plainness. Storage economy: the referent tuple is stored once at its address; each $\sigma$ is a cheap delta hanging off it. Meaning-level deduplication over real corpora, most of which is restatement.

### 6.2 Plane mapping

The tuple components land on the Qqci planes as follows: $C$ on Q2/Q3 (the possible and physical domain envelope), $\alpha$ on Q5 (the mechanic), $\Delta$ on Q6/Q7 (cause committed, effect realised), the actor parameter on Q1, and $\sigma$ mostly on Q4/Q7/Q1. Gap to resolve: the tuple as drafted has no explicit Q4 slot (WHY the transition occurred, as distinct from what it did). Options: a reason parameter inside the ParameterList, or Q4 assigned wholly to $\sigma$. The former is recommended, because "Alice paid Bob $10 reluctantly, to settle a debt" carries a reason that is part of the transition's meaning, not its phrasing.

### 6.3 SAEL is the rank-2 node format

In the tensor rank ladder (scope doc Section 12.3), SAEL specifies what a Phrase-rank (rank 2) node is: not a bag of word IDs but the typed role tuple. The Collapse Dictionary is the rank-2 stratum of the new dictionary: canonical actions are addresses, their synonym lists are the surface forms whose word-TS compositions contract to the same address. Same-referent detection needs no dedicated module: two sentences are isomorphic precisely when their plane projections intersect at the same coordinate, which is the Section 13 parallax/intersection machinery doing paraphrase detection as a side effect.

### 6.4 Code-level autocomplete

Because effects are executable state deltas, prediction becomes slot completion against a signature rather than next-token guessing. Given "commerce :: @TRANSFER { actor=Alice," the remaining parameters and the effect-list shape are type-determined, the way an IDE completes a call from a function signature. Completion becomes constraint satisfaction over a template: cheaper, checkable, and wrong in detectable ways rather than plausible ways. This is the concrete mechanism behind the fractal system's claim to produce low-level work as first-class output (scope doc Section 10): a completed SAEL tuple is simultaneously a prediction, a deliverable, and an executable test.

### 6.5 Nearest kin, for positioning

Abstract Meaning Representation (AMR): many sentences to one graph; no style residue kept. Davidsonian event semantics: every sentence an event variable plus role arguments; the academic ancestor of action-effect form. Machine-translation interlingua: the canonical pivot idea at language scale. Natural Semantic Metalanguage (Wierzbicka): roughly 65 cross-linguistic semantic primes; empirical support that a small canonical action vocabulary can span everything. Frame semantics / FrameNet: contexts as frames with typed slots; closest existing thing to the Context envelope. None of these keeps $\sigma$ as a first-class stored coordinate, and none pins the canonical form to an explicit plane geometry. Those two moves are SAEL's novel claims.

### 6.6 The falsifier: Experiment 0.5

Paraphrase corpora provide ready-made ground truth: MRPC, PAWS, STS (sentence pairs labelled same-meaning or different-meaning). Test: the SAEL parser maps paraphrase pairs to the same $\langle C, \alpha, \Delta \rangle$ at rates well above non-paraphrase pairs, while their $\sigma$ residues differ. PAWS is the vicious case, high word overlap with different meaning ("flights from New York to Florida" vs "flights from Florida to New York"), which tests exactly whether the role tuple catches what bag-of-words collapse would wrongly merge: the origin/destination parameters differ, so $\Delta$ differs, so no collapse. Pass criterion to fix before running: collapse precision and recall against the labelled pairs, reported separately for MRPC (easy) and PAWS (hard).

### 6.7 Resolution of the Tautonics fork output type

The scope doc's open fork (Sections 2 and 6: training-data variant vs translation-layer variant) gains its missing specification on the translation-layer side: the parser's target format is SAEL tuples plus style residues. English in, $\langle C, \alpha, \Delta, \sigma \rangle$ out, routed through the fractal Qqci nodes, English back out through $\sigma$-aware rendering. The lower-risk first build now has a defined interface at both ends.

## 7. Next Steps

- Fix the canonical action inventory per context: target 5 to 10 primitives per context per the determinism argument, seeded from the five drafted (@TRANSFER, @ACQUIRE, @MUTATE, @RELOCATE, @TERMINATE) and checked against NSM primes and FrameNet frames for coverage gaps.
- Decide the Q4 slot question (6.2): reason parameter vs $\sigma$-only.
- Specify $\sigma$'s representation: minimum viable version is the SignedSpan vector over Q1/Q4/Q7 (scope doc Section 14.3).
- Build the minimal $\Phi$ parser for one context (commerce) and run Experiment 0.5 against MRPC and PAWS subsets.
- Define the rendering inverse $\Phi^{-1}(\mathcal{T}, \sigma)$: canonical tuple plus residue back to natural English. Round-trip fidelity is the second falsifier.
