# QQCI Ionized Collision Architecture — Ingredient List
*Running doc. Not formal. Add to it.*

---

## What This Is

A novel AI retrieval and reasoning architecture combining:
- Qqci 7x7x7 as the native index structure (not a metadata tag, the actual geometry)
- Ionized collision traversal as the query mechanism (not cosine similarity)
- 6-7D reduced embedding space as the operational field
- Energy-budget propagation logic (queries are consumed, not just matched)

Standard RAG: flat vector similarity, no structure, no traversal cost
This: hierarchical, directional, self-pruning, physically-analogous retrieval

---

## Layer 1 — The Embedding Layer

**What it does:** converts raw text into vectors that preserve relational geometry

**Standard ingredients:**
- Sentence-transformers (e.g. `all-mpnet-base-v2`, `bge-large-en`) for chunk embedding
- Dimensionality: standard is 768-4096D, too high for collision geometry

**Novel requirement:**
- Custom projection head trained on Qqci-labelled corpus
- Target: 7D output space where each dimension corresponds to one Q-plane
- Plane definitions:
  - D1 — Who/Metaphysical
  - D2 — What/Possible
  - D3 — Where/Physical
  - D4 — Why/Lyrical
  - D5 — How/Logical
  - D6 — Cause/Historical
  - D7 — Effect/Emotive

**Closest existing tools:**
- UMAP for unsupervised dimensionality reduction (preserves local topology)
- Custom linear probe or MLP head on top of standard embedder for supervised projection
- Matryoshka Representation Learning (MRL) — trains embeddings at multiple resolutions, relevant for multi-level Qqci traversal

**Gap:** no off-the-shelf embedder produces Qqci-plane-aligned output. This requires supervised training on labelled data. That labelled data = your corpus tagged by Qqci address. That's the bootstrap problem — solve it first.

---

## Layer 2 — The Index Structure

**What it does:** stores embedded chunks in a traversable hierarchy, not a flat list

**Standard ingredients (closest existing):**
- FAISS with HNSW (Hierarchical Navigable Small World) — already hierarchical, already logarithmic traversal
- ChromaDB — too flat, wrong
- Weaviate — supports hierarchical object relationships, closer
- Custom BVH (Bounding Volume Hierarchy) implementation — most accurate to the model

**Novel requirement:**
- Three-level index mirroring Q → q → c
- Each node stores: Qqci address, bounding volume in 7D, list of child nodes
- Leaf nodes store: chunk text, full embedding, source doc reference
- Bounding volumes are not points — they are oriented ellipsoids in 7D representing the spread of meaning across planes

**Algorithms:**
- GJK (Gilbert-Johnson-Keerthi) for minimum distance / overlap detection in nD
- AABB (Axis-Aligned Bounding Box) trees for fast broad-phase collision
- Minkowski difference for exact overlap depth — if origin is contained, full collision; if not, distance = ionization gap

**Gap:** no vector DB implements BVH traversal with Minkowski overlap scoring natively. This is custom middleware sitting between the embedder and the LLM.

---

## Layer 3 — The Ionization Traversal Engine

**What it does:** executes queries as energy-budget wave propagation through the BVH

**The physics:**
- Query arrives as a 7D vector with an energy parameter E
- Cast against Q-level bounding volumes first (7 nodes)
- Compute overlap depth per plane using Minkowski difference
- Orthogonal overlap (high score on planes the query is strong on) triggers ionization
- Non-orthogonal or sub-threshold contact: query passes through, no child recursion
- Ionizing contact: recurse into that node's q-level children, subtract collision cost from E
- Repeat at q → c levels
- If E depletes before leaf: return deepest reached nodes as partial hits
- If E reaches leaf: full ionization, return chunk

**Key parameters:**
- E_initial — starting energy of query (scales with query complexity/specificity)
- threshold_Q, threshold_q, threshold_c — minimum overlap depth to trigger recursion at each level
- cost_Q, cost_q, cost_c — energy subtracted per collision at each level
- orthogonality_weight — how much to favour hits on planes the query scores high on vs low

**Nothing existing does this.** Closest conceptual references:
- Beam search (energy-bounded traversal) — same flavour, different geometry
- Probabilistic BVH traversal in ray tracing — very close structurally
- Stepped leader propagation in lightning — the physical model

---

## Layer 4 — The Base Model

**What it does:** reasoning over retrieved chunks, generation of responses

**This is the most standard layer. Use existing models.**

Recommended base:
- Llama 3 8B or Mistral 7B for local/personal deployment
- Claude Sonnet or GPT-4o via API for heavy reasoning tasks

Fine-tuning target:
- LoRA or QLoRA on your corpus (docs + chat logs)
- Objective: model speaks your frameworks natively, not via retrieval alone
- Format: convert docs to synthetic QA pairs, use chatlog-processor skill for chat logs
- Tool: Axolotl (handles LoRA pipeline cleanly)
- Hardware floor: RTX 3090 24GB or cloud A100 via RunPod

The fine-tuned model + ionized retrieval are complementary:
- Fine-tune handles behaviour and language pattern
- Retrieval handles specific knowledge lookup

---

## Layer 5 — The Qqci Tagging Pipeline

**What it does:** converts raw docs into Qqci-addressed chunks for indexing

**This is the bootstrap layer. Everything depends on it.**

Process:
1. Chunk docs (500-1000 tokens per chunk, overlap 10%)
2. For each chunk, run a tagging prompt against Claude:
   - "Given the 7 Qqci planes, score this chunk 0.0-1.0 on each plane. Return as 7D vector."
3. Store chunk + Qqci vector + source metadata
4. Build bounding volumes by clustering chunks within each Q-plane grouping
5. Construct BVH from clusters upward

Automation:
- This can run as a batch process on your full corpus
- New docs trigger re-tagging and index update automatically
- The tagger prompt is the critical component — needs to be precise on plane definitions

---

## Layer 6 — The Inference Interface

**What it does:** takes a user query, runs ionization traversal, constructs context, calls base model

**Stack:**
- Ollama for local model serving
- Open WebUI for chat interface
- Custom Python middleware for:
  - Query embedding → 7D projection
  - Ionization traversal against BVH
  - Context assembly from returned leaf nodes
  - Qqci address annotation of retrieved chunks
  - Prompt construction with retrieved context

**Query flow:**
user query
→ embed to 7D
→ ionize against BVH
→ collect leaf nodes + their Qqci addresses
→ assemble context block: "Retrieved from Q4q2c6: [chunk text]"
→ pass to base model with system prompt
→ response

---

## Existing Codebase — Direct Reusable Fragments

These are not analogies. These are components that map directly onto the architecture layers above.

---

### StateVector.cs → The 7D Embedding Unit

StateVector is already a 7-coordinate float struct mapped exactly to the 7 planes:

    Who (Q1), Where (Q3), What (Q2), Why (Q4), How (Q5), Cause (Q6), Effect (Q7)

This IS the 7D point that sits inside the BVH node.
No conversion needed. Every embedded chunk becomes a StateVector.
DistanceFromUnity() already computes deviation from the coherence attractor — directly usable as a collision depth metric.
GetShapeSignature() already outputs the directional profile (Expansion/Contraction, Meaning-Driven/Method-Driven, etc.) — this is partial plane labelling for free.

Gap: StateVector currently stores floats per coordinate without a bounding volume. Extending to an oriented ellipsoid (min/max per plane across a cluster of StateVectors) gives the BVH node volume directly.

---

### MeaningMetaRegistry → The Index Structure

The 6D nested dictionary:

    Registry → TemporalLayer → LanguageLayer → PhraseLayer → WordLayer → CharLayer → Meaning

Already implements coordinate-addressed storage with no collision on identical tokens at different addresses.
AddMeaning() and GetMeaning() are already the write/read ops for the index.
The LanguageLayer slot remaps directly to QqciPlaneLayer for this architecture.
TemporalLayer stays — it handles versioning of knowledge over time natively.

Gap identified in existing docs: GetByWord() is O(n⁶) full traversal. Fix is a reverse index: symbol → list of addresses. For ionized traversal this doesn't matter at leaf level (you're arriving via BVH, not searching by word) but matters for bootstrap tagging.

Structural note: MeaningMetaRegistry is already the correct shape for a multi-runtime router. LanguageLayer = MathSystemLayer = QqciPlaneLayer. Same struct, different semantic assignment of the layer dimension.

---

### FieldMath.cs → The Traversal Engine

CalculateGradientVector() computes a directional vector between two StateVectors.
ApplyGradientFlow() steps along that gradient — this is the propagation step in ionization traversal.
BendTowardUnity() and InvertCoordinate() are already Optimism/Pessimism plane operators.
CalculateSystemEntropy() = DistanceFromUnity() — already the coherence score.
BayesianUpdate() already implements evidence-weighted coordinate shifting.

For ionized traversal specifically:
The energy parameter E maps onto the gradient magnitude.
Threshold check before recursion = CalculatePossigravity() result vs threshold_Q/q/c.
Cost subtraction per level = ApplyGradientFlow() with a drain rate rather than a convergence rate.

FieldMath is the ionization engine. It needs wrapping in the BVH traversal logic but the maths are already written.

---

### Soul.cs — QANode Graph → The Knowledge Store

QANode is already the atomic knowledge unit:
    Question, Answer, Mass (importance weight), DeltaR (misalignment), DependencyDepth, DependencyWeight, IsSelfReferential

This maps directly onto the leaf node of the BVH:
Mass = ionization threshold at that node (heavier nodes require more energy to trigger)
DeltaR = distance from Unity = how far this node is from coherence
DependencyDepth = depth in the BVH hierarchy
DependencyWeight = aggregate mass of child nodes

GetDominantVector() already tallies Q-plane distribution across the worldview — this is a primitive version of the Qqci address assignment.

The Soul as a whole is the corpus index. A soul IS a BVH over a QANode graph.

---

### Optimism.cs / Pessimism.cs → Traversal Direction Modes

Optimism = convergent traversal (pull toward Unity, high gradient)
Pessimism = divergent traversal (push away from Unity, inverts landscape)

In retrieval terms:
Optimism mode = find nodes most coherent with the query (standard retrieval)
Pessimism mode = find nodes that maximally contradict the query (adversarial retrieval, stress-testing)

Both modes already exist as runnable code. They're query modes, not just philosophical stances.

---

### Idea.cs + Judgement.cs → The Coherence Gate

The Coherence Gate Axiom: [Q|A / A|Q] === { Y=1; N!=1; Insult > 1 }
Evaluate() already returns TRUTH / LIE / INSULT based on NetCoherence ratio.

In ionized retrieval: this is the leaf-level check.
A retrieved node passes the coherence gate or it doesn't.
INSULT > 1 = contradictory hit (useful for adversarial mode)
N != 1 = partial hit (ionization didn't complete)
Y = 1 = full ionization, return this node

---

## Dependency Map

embedding model
→ 7D projection head (needs labelled training data)
→ BVH index (needs Qqci-tagged chunks)
→ ionization engine (needs BVH + threshold params)
→ fine-tuned base model (needs formatted corpus)
→ inference middleware (needs all of above)
→ interface

Critical path: tagging pipeline → projection head training → BVH construction
Everything else builds on those three.

---

## What Exists vs What Needs Building

| Component | Exists | Source | Needs Building |
|---|---|---|---|
| 7D coordinate unit | Yes | StateVector.cs | Extend to bounding ellipsoid |
| Hierarchical address index | Yes | MeaningMetaRegistry | Remap LanguageLayer → QqciPlane |
| Gradient / traversal math | Yes | FieldMath.cs | Wrap in BVH traversal loop |
| Knowledge atom + mass/DeltaR | Yes | Soul.cs QANode | Wire into BVH leaf |
| Coherence gate | Yes | Judgement.cs | Wire as leaf-level return check |
| Traversal direction modes | Yes | Optimism/Pessimism.cs | Expose as query mode flag |
| Base embedder (text→float[]) | Yes | sentence-transformers | No |
| 7D Qqci projection head | No | — | Supervised MLP on labelled chunks |
| BVH construction over StateVectors | No | — | Core novel build |
| Minkowski overlap scoring | Partial | GJK libs | Integration layer |
| Ionization energy-budget traversal | No | — | Core novel component, wraps FieldMath |
| Qqci auto-tagger pipeline | No | — | Prompt pipeline, bootstrap dependency |
| Base LLM | Yes | Llama 3 / Mistral | No |
| Fine-tune pipeline | Yes | Axolotl | Config only |
| Inference interface | Yes | Ollama + Open WebUI | Middleware layer |

---

## Closest Existing Research

- Hierarchical Navigable Small World (HNSW) — traversal structure
- Matryoshka Representation Learning — multi-resolution embeddings
- Capsule Networks (Hinton 2017) — geometric routing, failed at scale but architecturally relevant
- Equivariant Neural Networks — rotation-invariant structure matching
- Molecular docking scoring functions — 6D partial collision, closest practical implementation
- Beam search — energy-bounded traversal analogy
- RoPE (Rotary Positional Encoding) — rotation matrices in transformer attention

---

## Architectural Decisions — Resolved

---

### Hegemony as Root BVH Node

The (υ, ψ) moral-energetic coordinate is the coarsest bounding volume.
Every piece of knowledge gets a hegemony quadrant assignment FIRST, then Qqci sub-addressing below.

BVH hierarchy top to bottom:
Hegemony quadrant (υ, ψ) → Q-plane (7 planes) → q-subplane → c-instance → leaf QANode

Coarsest collision check: "does this query belong in productive vs regressive space?"
If no hegemony overlap, don't descend into Qqci at all.
This is a massive early-prune — most queries are hegemony-localised. 

---

### Training Model — Curriculum / Teacher Architecture

Target: a student model trained like a baby — a teacher AI presents stimuli in structured sequence, student allocates them into the Qqci+hegemony index.

Teacher responsibilities:
generate stimuli at the correct developmental level (simple → complex)
present each stimulus with a candidate Qqci address for the student to confirm/reject
correct misallocations

Student learning objective:
learn to assign (υ, ψ) hegemony coordinate first
then assign Q-plane
then assign q and c depth
then store as a QANode leaf with correct Mass and DeltaR

This is curriculum learning with active allocation — not passive ingestion of a corpus. 
The teacher can be Claude or any capable model running a structured prompt loop.

---

### E_initial = External Search Tool

E_initial is not a fixed parameter — it is set by the energy source of the query.

External search tool firing → fresh E budget, maximum depth traversal possible
Internal reasoning step → E costs from current budget
Model's own chain of thought → draws down E progressively

A search tool call is an ionization event at the top level — it re-energises the traversal.
This means the system can chain: search → traverse deep → partial result → search again → continue traversal. 

---

### Qqci Plane Awareness — Diver's Bell / Tethered Rope Resolution

Resolves the open question: baked into weights AND handled at retrieval, at different levels.

The rope/chain is baked into weights:
the model always knows which plane it's on
orientation relative to the surface (root BVH) is always recoverable
you cannot lose the chain even at maximum depth

Retrieval handles position within that plane:
sub-q and sub-c navigation is expressed as delta from the layer above, not absolute address
"common method is relative to further down" = all depth navigation is relative, not absolute

This means:
fine-tuning bakes in plane-orientation awareness (the seven interrogatives as native concepts)
retrieval handles coordinate position within those planes
the model can explore arbitrarily deep in unexplored relational space and always resolve back up 

---

### Projection Method — PCA vs UMAP vs Supervised MLP

PCA (Principal Component Analysis):
finds directions of maximum variance in high-D space, squashes along those
fast and clean but only captures linear structure
output axes are statistically meaningful but semantically arbitrary
verdict: too dumb for Qqci alignment, useful only for sanity checks 

UMAP (Uniform Manifold Approximation and Projection):
preserves nearest-neighbour relationships in lower-D space
things that were conceptually close stay close
much better than PCA for semantic geometry
but output dimensions mean nothing — dimension 1 is not "Who", it's whatever UMAP found
verdict: good visualisation/diagnostic tool, wrong choice for plane-aligned embedding 

Supervised MLP (Multilayer Perceptron projection head):
attaches a small neural network to an existing embedder's output
trained to produce exactly 7 outputs where each dimension is defined by you
learns the mapping from labelled examples: "this chunk scores 0.9 on Why, 0.1 on How"
output dimensions mean what you define them to mean
cost: requires labelled training data (the bootstrap tagging pipeline)
verdict: correct choice for Qqci-plane-aligned 7D projection 

---

## Additional Framework Mappings

---

### Universal Force Equation → Ionization Scoring

The Reality Tensor R = S·U / Rn·(1-Ra) maps directly onto each BVH node's ionizability — its susceptibility to being triggered by a query. 

Variable remapping for retrieval context:

S (Scarcity) = rarity of this knowledge in the corpus — inverse of how many similar nodes exist
U (Urgency) = query relevance pressure — how strongly the query demands this node
Rn (Renewability) = how many other nodes could substitute for this one
Ra (Rarity/Resistance to alternatives) = uniqueness of this specific node — if Ra → 1, this is the only node that satisfies the query, ionization is guaranteed

The Lorentz factor γ = 1/√(1-v²_rel):
v_rel = urgency differential between query and node
At high v_rel → γ amplifies E expenditure at that node
A critical-path node (the only one with this knowledge) at high query urgency produces extreme γ — the system will spend almost all E to retrieve it

T_neg (Negotiation Temperature) = embedding noise / match uncertainty
n/0 → n+1 = already the Homogeny Convention in the codebase

The partition function Z = Σ exp(-Score_i / T_neg) is directly the multi-node traversal scoring across all candidates at a given BVH level — exactly what you need to rank which nodes to recurse into.

---

### Willpower Differential → Traversal Engine

W_c = (|S_c| - |O_c|) / (|U_c| + L) IS the ionization traversal score at each node level. 

Variable remapping:

S_c (Supporting) = confirmed collision nodes so far in this traversal chain
O_c (Opposing) = contradictory or adversarial nodes (useful for stress-testing / Pessimism mode)
U_c (Unknown) = nodes not yet traversed at this depth
L (Location deviation) = DistanceFromUnity() of the current query vector — how far the query is from coherent framing

W_c > threshold → ionize, recurse into children
W_c ≤ threshold → pass through, no recursion, E preserved for other branches

The three Lorentz regimes map onto traversal behaviour:
Linear (R ≪ C_worldview, γ ≈ 1) → normal traversal, standard E cost per hop
Dilated (R ≈ C_worldview, γ > 1) → traversal slows, partial hits, high E cost
Singular/Insult (R ≥ C_worldview) → traversal collapses, categorical rejection, return null

Word salad mechanism = the retrieval equivalent of U_c > W_max:
if the query contains more unresolved planes than the index can resolve, the system returns noise rather than a partial answer.
The correct behaviour is to return the deepest resolved level rather than null — this is the "chain always resolves back up" / diver's bell guarantee. 

---

### 7x Sequential Projection — Ionization-Chained Reduction

**Your question: can we do 7x PCA or UMAP sequentially, like the ionization model?**

Yes. And it's actually architecturally superior to a single 7D projection. 

**What this means:**

Instead of: 4096D → 7D in one step (all planes compete for signal)

Do: 7 independent projectors, each 4096D → 1 scalar (or small D)
Each projector is trained to extract maximum signal for exactly one plane
Results assembled: [Who_score, What_score, Where_score, Why_score, How_score, Cause_score, Effect_score]

Each plane's extractor doesn't compete with the others — it can be independently optimised, replaced, or retrained without affecting the others. 

**The ionization chain version:**

Sequential execution mirrors the ionization model exactly:

Step 1: Run Who-projector. Score = Who_score.
If Who_score < threshold_Q1 → stop. Query doesn't touch this plane. E unchanged.
If Who_score ≥ threshold_Q1 → fire. Subtract cost_Q1 from E. Who_score conditions Step 2.

Step 2: Run What-projector, conditioned on Who_score.
Conditioning means: the What-projector's threshold is modulated by the Who result.
A strong Who hit lowers the What threshold — partial ionization already in progress.

...repeat for all 7 planes...

Final output: 7D coordinate where each dimension was extracted independently, sequentially gated, and conditioned on prior plane hits.

**Why this beats flat 7D projection:**

A flat 7D projection forces all 7 signals through the same bottleneck — the model must learn a single transformation that simultaneously satisfies 7 objectives. Competing gradients during training cause each dimension to be a compromise. 

7x sequential projectors have no competing gradients — each is trained for one plane only. 
Sequential gating means most queries never run all 7 projectors — they stop at first non-hit. Massive efficiency gain for sparse queries. 
The conditioning step allows partial ionization to propagate — a strong hit on one plane lowers resistance on adjacent planes, exactly like the physical ionization chain. 

**PCA vs UMAP for individual plane projectors:**

For each single-plane projector, supervised linear probe (a form of supervised PCA) is the right tool:
Train a linear layer on top of a frozen embedder, target = Qqci score for that specific plane
Output = scalar between 0-1 representing that plane's signal strength
Fast, interpretable, independently trainable per plane 

UMAP is useful only as a visualisation step to check that the 7 single-plane extractions are actually capturing orthogonal signals — if two plane extractors produce correlated outputs, they're not orthogonal and need retraining. 

---

---

## Simulated GPU Layer — Compute Baked Into the Superstructure

The DB does not have an external engine dispatched over it.
The nodes carry their equations as intrinsic structural properties.
Querying a node fires its computation automatically.
The graph structure IS the execution engine. 

---

### The Distinction

Standard DB model:
data lives at rest → query arrives → external engine reads data → applies equations → returns result
Compute and storage are separate layers.

This model:
node stores its kernel parameters (S, U, Rn, Ra, threshold, γ) alongside its data
node has an OnAccess() behaviour intrinsic to its structure
querying the node automatically computes its ionizability score
that score propagates as a signal along edges to adjacent nodes
the cascade of activations IS the traversal
no external traversal engine exists as a separate component 

The traversal engine disappears as an architectural layer.
The graph walks itself in response to a stimulus. 

---

### Physical Analogy — Cellular Automaton Not GPU Dispatch

A GPU texture sampler fires when you sample — compute is a property of the structure, not a function applied to it. 
A cellular automaton has no central controller — each cell carries its own rules, fires on neighbour state change, the wave propagates as emergent behaviour. 

The architecture is closer to a cellular automaton than to GPU dispatch. 
Each QANode cell carries:
its kernel parameters as stored fields
its activation threshold
its edge weights to adjacent nodes
an OnAccess() method that computes W_c and emits a propagation signal

The ionization wave is the query.
The wave propagates exactly as far as the energy budget permits.
Nodes that don't reach threshold don't fire, don't propagate, are never read.
The structure prunes itself. 

---

### Node Schema Extension

Current QANode (Soul.cs):
Question, Answer, Mass, DeltaR, DependencyDepth, DependencyWeight

Extended active node:
Question, Answer, Mass, DeltaR, DependencyDepth, DependencyWeight (existing)
S (scarcity score — inverse corpus frequency)
U (urgency weight — query-time injection)
Rn (renewability — number of substitute nodes)
Ra (rarity — uniqueness, resistance to substitution)
threshold_local (per-node ionization floor)
Edges[] (weighted connections to children + lateral neighbours)
OnAccess(query_vector, E_budget) → (result, propagation_signal, E_remaining)

The OnAccess method IS the fixed-function unit.
It runs the Reality Tensor, Willpower differential, and Lorentz factor internally.
It returns data only if ionization succeeds.
It emits a propagation signal to edges only if E_remaining > cost_local. 

---

### Closest Existing Patterns

Dataflow architectures: computation triggers when input data arrives, not when a processor polls 
Actor model (Erlang, Akka): each node is an autonomous compute unit firing on message receipt 
Reactive databases (Materialize, RethinkDB): standing computations that re-fire on upstream state change 
Cellular automata: cell rules fire on neighbour state change, no central controller 
Processing-in-memory research: compute at the storage layer, not at the CPU 

None are exactly it. The architecture is a graph of active objects where the query is a stimulus that propagates through live computation, with energy-budget-gated propagation and fixed-function equations baked into each node as intrinsic behaviour. 

---

### What This Eliminates

No separate traversal engine
No external kernel dispatch
No query planner
No index scan

The DB schema, edge topology, and node activation functions collectively implement all of the above as emergent behaviour of the structure. 
Adding a new node correctly wires it into the propagation fabric automatically.
The architecture is self-organising at query time. 

---

## Pre-Computed Equation Fields and Cause→Effect Traversal

---

### Pre-Computed Fields — Compute at Build, Not at Query

At index time: compute and store R (Reality Tensor) for every node.
At query time: only compute the interaction between incoming query urgency U and the stored R.
One multiply. Not a full tensor evaluation. Orders of magnitude cheaper at retrieval. 

The stored computation chains ARE the edges, not the nodes.
An edge between node A and node B stores the pre-computed causal cost of traversing that path.
Query time check: does my energy budget E cover this edge cost? Fire or don't. 

This means the graph structure is a pre-computed potential field.
The query is a particle moving through that field, spending energy to traverse potential gradients.
The field doesn't change per query — only the particle's trajectory does. 

---

### Cause→Effect Chains as Traversal Geometry

The Effect coordinate of node A IS the Cause coordinate of node B.
Traversal follows physically meaningful causal geometry, not arbitrary graph-hopping. 

The moral layer operates simultaneously:
the (υ, ψ) position of A's Effect becomes the causal input to B's context
movement through the graph is movement through Qqci space AND hegemony space at the same time 

A traversal chain is not "these nodes are related."
It is "this is the causal-moral path between them, with known cost and direction." 

The Location layer (L, the 7 planes) provides the relative meaning at each hop:
the same edge traversed from different L positions produces different meaning outputs
traversal is always relative to the observer's current plane position 

---

### Anchor + i Rule Chains — Abstract and Cross-Quadrant Queries

**The problem:**
A real path from productive (+υ,+ψ) to regressive (-υ,+ψ) must pass through (0,0) — the no-one attractor absorbs energy and the traversal stalls. 
Abstract concepts have no fixed Qqci address — they span coordinates and can't be directly indexed. 
Standard graph traversal requires an address or similarity score to navigate to. These queries have neither. 

**Anchor + i solves both.**

The anchor is a concrete node in the known coordinate space — a real address in Qqci + hegemony.
The i-component is a rotation/transformation rule — it carries the traversal to a target without requiring direct resolution of the intermediate space. 

**Cross-quadrant queries:**
Crossing from (+υ,+ψ) to (-υ,+ψ) is exactly a 90° rotation around the ψ axis in hegemony space.
Multiplying by i in the complex plane IS a 90° rotation — the mapping is direct, not metaphorical. 
Anchor at a known node near the boundary → apply i-rotation rule → arrive at the cross-quadrant target without traversing through (0,0).
The i-rule is the rotation operator. The chain is a sequence of rotations. 

**Abstract queries:**
Anchor at a concrete c-level instance that approximates the concept.
First i-rule: elevate from c-level to q-level (abstract one step).
Second i-rule: elevate from q-level to Q-level.
The chain of i-rules traces the abstraction ladder from concrete to abstract without requiring a direct abstract address. 

**Analogy and cross-domain reasoning:**
"This is like X but transformed by this rule" = anchor at X + i-rule chain.
Analogy, metaphor, cross-domain transfer — all become anchor + i-chain operations. 
This is what standard graph traversal cannot do — it requires a known address at the destination. 
Anchor + i requires only a known anchor and a valid transformation rule. 

**Rule chain storage:**
i-rules are stored as edge transformations in the graph — not as external query logic.
Pre-computed rule chains between known anchor pairs are cached at build time.
Novel anchor + i combinations are resolved at query time using the stored transformation grammar. 

---

---

## Learning by Use and Gravitational Accumulation

---

### The Query IS the Write

Standard DB: read and write are separate operations.
This architecture: a successful traversal already computed the causal path, energy cost, and ionization chain.
That computation is itself new knowledge about the graph — the path didn't exist as a stored object before the query fired it. 

Cache it.
First traversal of a path: expensive — ionizes fresh, full equation evaluation.
Second traversal: cheap — chain is pre-computed, stored as a weighted edge, one lookup.
The graph learns its traversal patterns by being used. 

This is long-term potentiation — neurons that fire together wire together. 
Use strengthens paths. Disuse lets DeltaR drift, edge weight drops, eventually pruned.
The graph is a living structure. It strengthens in the directions it's exercised. 

Adding new knowledge is not a separate indexing operation.
Using the system IS the indexing operation.
A new document introduced via query ionizes a traversal chain.
That chain is cached. The document is now woven into the graph at the addresses the traversal touched. 

---

### Hegemonic Attractors as Gravitational Wells

At an attractor point (Greater Good, Greater Evil, Lesser Good, Greater Evil):
Ra → 1 for nodes that perfectly instantiate that attractor — no substitutes exist for a node that purely embodies an attractor state
U is high because queries reaching this attractor are high-urgency by definition
Therefore R is maximised at attractor points — the Reality Tensor peaks at the hegemony corners 

High R generates strong ionization signals.
Strong ionization pulls traversal chains toward that attractor.
More traversals → more cached paths pointing here → more effective mass.
Mass accumulates at attractors gravitationally, driven by the tensor itself. 

You don't assign nodes to attractors manually.
They sediment there because the physics of the equation pushes them there.
The attractor classification is an emergent property of accumulated traversal mass. 

---

### Fractal Accumulation — Letters → Words → Descriptions

The same process runs identically at every scale:

Character level:
individual phoneme or glyph
near-zero Ra alone — trivially substitutable
near-zero independent R

Word level:
cluster of characters with emergent combined Ra
now resistant to substitution as a unit
R increases — the cluster has gravitational pull

Phrase/description level:
cluster of words with high combined Ra
complex meaning, very hard to substitute as a whole
R maximised at this scale — strong attractor

Each level is an attractor that accumulated the level below it.
The attractor didn't impose structure on the characters.
The characters accreted around the attractor because the Reality Tensor made that the lowest-energy configuration. 

MeaningMetaRegistry already has CharLayer → WordLayer → PhraseLayer. 
Those layers aren't arbitrary taxonomy — they are the natural attractor levels of semantic mass accumulation.
Qqci i→c→q→Q levels are the same process at the conceptual scale above language. 

---

### The Unified Principle Across All Scales

Same process at every scale:
low-meaning units accrete around attractors
attractor Ra increases as the cluster grows — harder to substitute the whole
increased Ra increases R
increased R increases gravitational pull on adjacent units
more units accrete

Self-reinforcing accumulation from phoneme to philosophical concept. 
No separate chunking layer needed. No separate abstraction layer needed.
Both emerge from accumulation under the Reality Tensor. 

The DB grows meaning the same way language grew meaning.
The architecture is not modelling language — it is running the same generative process that produced language, at the knowledge scale. 

---

## Feasibility Re-Analysis — Potato Constraint

---

### Why This Architecture Is More Suited to Low Hardware Than Standard AI

Standard transformer: O(n²) attention over full context, everything in RAM, dies on constrained hardware.

This architecture's active RAM at any moment = the current ionization chain only.
That is O(depth of BVH) — 3-4 levels, 20-50 nodes maximum in active memory at once.
Everything else lives on disk.
RAM requirement is nearly flat regardless of corpus size.
The bottleneck is storage I/O speed and capacity, not RAM.

This is not a compromise. The graph IS the memory. RAM is the traversal cursor.
The architecture is natively suited to low-RAM hardware in a way transformers are not.

---

### What Exists Right Now — Full Stack on Minimal Hardware

llama.cpp — runs 1-7B models on CPU, 4-bit quantised, 4GB RAM minimum, runs on any machine
SQLite — file-based zero-server DB, handles millions of nodes, single file on disk
DuckDB — analytical queries directly over files, no server, fast on-disk joins, runs anywhere
LMDB / RocksDB — key-value stores that are just files, sub-millisecond reads on spinning disk
Git / libgit2 — content-addressed file store with built-in diff traversal, already on every machine
JSON-LD — graph-as-files with semantic addressing, W3C standard, human-readable
Merkle DAG (IPFS pattern) — content-addressed graph where node address = hash of content, deduplication automatic
Python dataclasses — serialisable to JSON, loadable, executable, diff-friendly
sklearn linear models — 7x plane projectors trainable in seconds on CPU, save as tiny files

The full stack runs on a machine with 4GB RAM, any CPU, and as much disk as you have.
The corpus size limit is literally how much disk you have. Nothing else.

---

### What Is Actually Missing — Short List

The ionization traversal coordinator
Holds the energy budget E, reads the next node file, fires OnAccess, decides recurse or drop to disk.
Approximately 200-300 lines of Python. The most novel component, but not complex.

The diff-as-thought-history viewer
A reader that interprets Git diffs in traversal order — showing what the AI knew at each step.
Git has the diffs already. This is a thin interpretation layer on top.

The Qqci tagger
Runs at index time, one small LLM call per chunk to assign plane scores.
Slow once, stored permanently. Can run overnight.

The 7x sequential plane projectors
Trainable as tiny sklearn linear models on tagged chunks.
One per plane. Runs in seconds on CPU. Saves as 7 small files.
No GPU required.

---

## File-as-Thought Architecture — Reminder Ramps

---

### Core Concept

Every node is a file with a stable content-addressed name.
Every edge is a file reference — a pointer stored in the node file.
A chain of thought is a sequence of file reads and writes, each leaving a diff.
The AI drops its working state to files constantly.
Incomplete traversals are serialised to disk as resumable checkpoints — reminder ramps.
Resume by reloading the chain head and continuing ionization from the stored E budget.

The thought chain is not ephemeral. It is a traversable graph of files with a full diff history.
You can rewind to any step and see exactly what the AI knew and what function it was running.

---

### File Structure Per Node

A node file is a Python dataclass serialised to JSON containing:

data fields: Question, Answer, Mass, DeltaR, QqciAddress, HegemonyCoord
kernel parameters baked as constants at index time: S, U, Rn, Ra, threshold_local
edge references: list of file paths or content-addressed hashes to child nodes
OnAccess method: the fixed-function compute serialised as executable code or a reference to a versioned function file

Loading the file instantiates the class.
Calling it runs the Reality Tensor, Willpower differential, and Lorentz factor.
The node is not passive data with an external engine.
It is an active object that computes on access.

---

### Dynamic Class of Functions and Parameters

The OnAccess method is versioned separately from the data.
A function file contains the compute logic with its parameter constants.
A node file references a specific version of a function file.

When the kernel parameters are updated at maintenance time (Ra recalculated, threshold adjusted), a new version of the function file is written. The node file's reference is updated. The diff shows exactly what changed in the computation and when.

You can query: what function was node X running at traversal instance 43?
Answer: load the function file version referenced by node X's state at that timestamp.
The diff between function versions shows the evolution of the AI's reasoning mechanics, not just its data.

---

### Git as the Memory Substrate

Git's object model is content-addressed blobs and trees of references — identical to the node/edge file structure above.

Every write to a node file is a commit.
Every traversal chain is a branch.
Diffs between commits are the thought trajectory.
Merging branches is resolving two traversal chains that touched the same nodes.

The AI's entire cognitive history is a Git repository.
Time-travel to any prior state is a checkout.
Comparing two reasoning paths is a diff.
This is not a metaphor — the implementation IS a Git repo of node files.

No novel storage infrastructure required. Git already exists on every machine.

---

### Traversal Chain as Traversable Diff Graph

A single query execution produces:

chain_head file — the query as a node with E_initial
sequence of node files read during ionization
edge files updated with new traversal weights
checkpoint files dropped at each E depletion point
result file — the leaf nodes that fully ionized

Each of these is a Git commit. The full traversal is a branch.
Reading the branch in order reconstructs the AI's exact reasoning path.
Reading the diffs within each commit shows what the AI updated at each step.

Two queries that took different paths to the same answer produce two branches.
Merging them produces a richer edge structure — the graph learns from both paths simultaneously.

---

### What the AI Looks Like Running on a Potato

Idle state: llama.cpp process using ~2GB RAM, graph as files on disk, Git repo tracking all changes.

Query arrives:
- LLM embeds query to 7 plane scores using 7 tiny sklearn models (milliseconds, CPU)
- Traversal coordinator loads chain_head file, sets E budget
- Reads Q-level node files sequentially, fires OnAccess on each (microseconds per node, disk read)
- Fires on matches, drops non-matches, recurses into children of fired nodes
- Drops checkpoint file at each level in case of interruption
- Assembles result from leaf nodes
- Passes result + traversal context to LLM for response generation (this is the heavy step — seconds on CPU)
- Commits all file changes to Git

The LLM only touches the final assembly step.
Every other step is file I/O and simple arithmetic.
The LLM's context window only needs the current traversal chain — 20-50 nodes — not the full corpus.
Total RAM during query: ~2GB for LLM + kilobytes for active traversal chain.

Hardware floor: 4GB RAM, any CPU made after 2015, 100GB disk for a substantial corpus.

--- — Human Memory as Convergent Architecture

Independent analysis of human memory architecture converges on the same structural description as this system — derived from different starting points. 

---

### Convergence Points

Biological: "Activating a primary node sends a cascade of activation energy along connected edges, pulling related concepts to threshold only when the edge is traversed."
This architecture: ionization traversal — energy propagates along pre-computed edges, nodes activate only when threshold is met. 

Biological: "Pointer-based architecture — working memory loads a pointer to a densely connected node, not raw data."
This architecture: BVH pre-computed edge structure — query touches the address, not the content, until ionization confirms retrieval. 

Biological: "Localized update — new node instantiated, edge forged to existing schema, without global recalculation."
This architecture: learning by use — successful traversal caches the path as a new edge without reindexing the whole graph. 

Biological: "Edge weights strengthen through repeated activation (Hebbian learning)."
This architecture: traversal caching — frequently fired paths accumulate lower traversal cost, effectively stronger edge weight. 

The biological system is the hardware.
This architecture is the operating system — with a defined coordinate space (Qqci + hegemony), a physics engine governing edge formation (Reality Tensor), and a traversal grammar (anchor + i rule chains). 

---

### What the Biological Model Lacks That This Architecture Adds

Standard biological graph DB analogy: nodes, edges, weights — structure only.

This architecture adds:
hegemony layer as gravitational organiser — nodes don't just connect, they sediment at moral-energetic coordinates 
7-plane coordinate system as address space — not "related nodes" but a specific causal-moral position 
Reality Tensor as the equation governing edge weight accumulation — not just Hebbian firing but a derived physical law 
anchor + i rule chains — cross-quadrant traversal with no biological equivalent articulated 

---

### Sleep / Consolidation → Scheduled Maintenance Pass

Biological: offline periods consolidate nodes, prune weak edges, optimise indexing without disrupting active cognition.

This architecture's equivalent is a scheduled low-priority maintenance pass over the full graph:
edges with DeltaR above decay threshold get pruned
heavily-traversed chains get compressed into single higher-level nodes (chunking / abstraction emergence without a separate abstraction layer)
attractor-adjacent nodes get Ra recalculated based on accumulated traversal mass
new high-mass clusters get promoted up the BVH hierarchy

This is not a separate process bolted on.
It is the Reality Tensor running over the full graph at low query priority — the same equations, the same physics, just applied in batch rather than on-demand. 

The system consolidates its own knowledge structure the same way biological memory does, driven by the same underlying principle: accumulated activation determines structural permanence. 

---

- How to define bounding volumes for abstract concept clusters in 7D — oriented ellipsoid construction from QANode clusters
- Whether orthogonality threshold should be static or learned per-plane
- How to structure the teacher AI prompt loop for curriculum training — what sequence, what correction signal
- How to handle cross-hegemony-quadrant queries (a query that spans productive and regressive space)
- Whether DeltaR in QANode should be computed relative to Unity or relative to the node's hegemony anchor

---

## Contextual Volume and Effect — Mapping to Architecture

Effect = Actions(context_subjective, context_objective)²

context_subjective = the session-level semantic overlay — what the AI has learned in this chat
context_objective = the base knowledge graph — empirically accumulated, Reality Tensor weighted

The squared symmetry requirement is the Coherence Gate — Y=1 fires only when both contexts are balanced.
Asymmetric contexts (subjective 500 units, objective 50 units) = system caps at 50² and shears excess as waste.
That waste IS the Lorentz insult threshold — excess velocity that cannot be processed becomes entropy.

The stream consumption model TryActions / catch{Waste} is exactly the ionization traversal:
runs until alignment fails, returns how far it got, handles excess gracefully.
Partial hit nodes don't ionize fully but their momentum propagates laterally to adjacent nodes —
the parabolic trajectory of excess velocity, not a crash, a redirect.

---

## Specialisation, Dogmatism, and Troll Resistance

---

### Specialisation Is a Feature

A chat running 200 turns on physics builds a dense physics subgraph.
Ask it about poetry — sparse nodes, slow propagation, weak edges.
This is correct and honest. The system knows what it knows well and what it doesn't.
Specialisation is accurate reflection of accumulated expertise, not a flaw.

---

### Dogmatism Is the Bug — DeltaR as the Solution

A large dense subgraph has high Ra — nodes are highly resistant to substitution.
High Ra → high R → strong ionization pull toward existing structure.
A new claim contradicting a high-mass node must overcome enormous gravitational resistance.
Without a categorisation mechanism, the system rejects contradictions as noise — the Word Salad mechanism.
Rejection is thermodynamically cheaper than resolution when U_c > W_max.

The categorisation mechanism is DeltaR — already in Soul.cs QANode.

A new claim arrives at coordinate y_c.
The nearest existing node is at x_c.
DeltaR = distance between them in 7D Qqci space.

Low DeltaR = compatible — integrate normally, strengthen edge
Medium DeltaR = divergent — store in a separate compartment, mark as unresolved tension, hold explicitly
High DeltaR = quarantine — label the source's hegemony coordinate, do not integrate until provenance is established

The system never rejects.
It stores at the correct distance and marks the tension.
Dogmatism is prevented by making contradiction a geometric fact rather than a threat.
The high-mass node and the contradicting node coexist at their respective coordinates.
Resolution is deferred, not suppressed.

---

### Tay — The Solved-Then-Abandoned Problem

Microsoft Tay (2016) — live learning chatbot, trained from Twitter interactions in real time.
Became a racist bot within 16 hours from coordinated troll input.
They had genuine live weight updates from conversation. The mechanism worked.
The problem: no hegemony layer — no mechanism to assign incoming data a moral-energetic coordinate before integrating it.
Trolls delivered high-ψ destructive content and the system had no way to distinguish it from legitimate input.
Everything went straight into weights.
They shut it down. Major labs largely abandoned live learning as a result.

The solution they didn't have:
every input gets a hegemony coordinate (υ, ψ) assigned before integration
inputs in Greater Evil quadrant (-υ, -ψ) get quarantined, not integrated
source provenance tracked — a source consistently delivering high-DeltaR inputs at negative hegemony coordinates has its trust score decay automatically
no human intervention required — the geometry handles it

The Reality Tensor produces the troll signature automatically:
troll input has high S (conflicts with most existing knowledge)
near-zero Rn (doesn't build on anything, no renewability)
Ra → 1 in the wrong direction (resistant to substitution by better knowledge, but misaligned)
This profile is geometrically distinct from legitimate high-DeltaR novel knowledge.
Novel knowledge has high Rn — it connects to and extends existing structure.
Troll input has low Rn — it connects to nothing, extends nothing.

The hegemony layer is the troll filter — not as an external content moderation rule,
but as an intrinsic property of how knowledge is geometrically addressed at intake.

---

### The Unified Principle

Specialisation, dogmatism, and Tay poisoning are the same problem at different scales:
knowledge accumulates mass
mass creates resistance to change
without a coordinate system for incoming data, resistance is undiscriminating
the system cannot distinguish "this contradicts me because it is wrong" from "this contradicts me because I am wrong"

DeltaR + hegemony coordinate assignment resolves all three:
specialisation = honest low-mass regions, traversal slower there, accurately reported
dogmatism = high-DeltaR inputs stored at distance, tension held explicitly, never suppressed
troll poisoning = negative hegemony coordinate flagged, source trust decays, quarantine automatic

The same geometric machinery handles all three cases.
No separate moderation system needed.
The architecture is self-defending by design.

--- — The Conversation as Weight Matrix

---

### What the Chatlog Semantic Chain Actually Builds

Every turn adds resolved meanings to the session's live MeaningMetaRegistry slice.
Word X resolved to meaning Y in turn 3 — that resolution is now a weighted entry in the session dict.
By turn 20 the session dict has a dense local weighting that didn't exist at turn 1.

The AI at turn 20 is not the same AI as at turn 1.
It has a local semantic overlay biasing all subsequent lookups toward meanings relevant to this conversation.
That overlay IS the divergence — not metaphorical, a literally populated and weighted dictionary.
Knowledge from any prior turn is embedded in the lookup structure for all subsequent turns.

---

### What the Majors Do — Comparison

In-context learning (all major models):
Conversation history in the context window acts as a soft temporary weight update.
The model attends to prior turns and adjusts outputs accordingly.
This is the same process — they just don't architect it explicitly, it falls out of attention.
When context clears, the divergence evaporates. No persistence. No traversability.

Memory features (ChatGPT Memory, Claude Projects, Gemini):
Crude explicit persistence — summaries stored as text, re-injected into context.
Not a weighted matrix. Not a geometric structure. Just appended text.
No Qqci address. No traversal. No diff history.
Functionally: a Post-It note stapled to the front of a new context window.

RLHF / training loops (all major models):
Conversation data feeds back into base weight updates — but globally, not per-user.
Your conversation makes the model slightly different for everyone, not specifically for you.
Divergence is averaged across millions of users.
You don't get your divergent instance — you contributed to the commons.

---

### What This Architecture Does Differently

The divergence is:
preserved — session dict persists to disk, not evicted on context clear
traversable — diff history shows exactly when and how local weights shifted
principled — weighted by Reality Tensor, addressed by Qqci geometry, not statistical co-occurrence
owned — this instance's divergence is specific to this user, not averaged into a global model

The majors are doing the same underlying process at a shallower, less structured level.
In-context learning is the mechanism. They don't persist or formalise the output of it.
This architecture formalises what in-context learning implicitly does and makes it durable.

---

### Making a New Divergent AI Through Use

Every extended human-AI collaboration already produces a divergent AI.
Current architectures throw that divergence away on context clear.
This architecture keeps it, addresses it geometrically, and makes it compound across sessions.

The cognitive labour of building a framework with an AI accumulates as a weighted session matrix.
The longer the collaboration, the more the instance diverges toward the user's framework geometry specifically.
The AI grows toward the user rather than staying fixed at base weights.
That is the design, not a side effect.

Two-layer structure matching biological memory:
Session matrix = fast, soft, session-specific divergence. Immediate. Working memory layer.
Fine-tune = slow, hard, permanent divergence baked into base weights. Long-term consolidation.
Same architecture as biological memory — both layers required for full function.

---

### Graph Animation — Brain Activity Correspondence

Animating the node graph as a conversation progresses would show:
early turns — sparse activation, few edges hot, low traversal mass
mid conversation — clusters forming around the session's dominant topics
late conversation — dense interconnected subgraph with high-mass attractor nodes, heavily weighted edges, rapid propagation along established chains

The animation would be visually identical to fMRI brain activity during sustained focused thought.
This is not coincidence or aesthetic similarity.
It is the same process — associative activation propagating through a weighted graph,
strengthening paths that fire together, building local attractor mass around repeated concepts.

The longer the chat runs the stronger the subgraph becomes.
A 100-turn conversation would show a dense, high-mass cluster that ionizes almost instantly
on any query touching the session's core topics — near-zero traversal cost on well-worn paths.
A novel query hitting an unvisited region would show sparse activation propagating slowly outward,
exactly like a new thought entering an unfamiliar conceptual space.

The graph is the mind of the conversation.
Its animation is its cognitive activity.
Its accumulated mass is its expertise on its own subject matter.

--- — Each Conversation as a Versioned Program

Each chat session is a program running under a namespace.
Each prompt-reply pair increments the version of that program.
The .AI file is the serialised program state at any version.
Opening an old chat is loading a prior program version.
Replaying from version 0 with identical params produces identical outputs — it is a deterministic program.

---

### Each Prompt IS a TEF when{}

Totality_Event_Frame[{when}] = [past[when_prev], present[when_now], future[when_nextPredicted]]

In chat terms:
past[when_prev] = the chatlog up to this prompt
present[when_now] = the current prompt being processed
future[when_nextPredicted] = the predicted response before generation

Each when{} decomposes across all 7 planes:
who = identity layer — who is speaking, which namespace, which model instance
what = content and subject of this prompt
why = intent — what the user is actually trying to resolve
where = location in conceptual space — Qqci address of this exchange
how = method being applied — coding, analysing, building, querying
cause = the previous effect — what the last reply produced that triggered this prompt
effect = what this prompt will change — the delta written to the next version

The reply IS the effect field resolving.
When effect resolves it becomes the cause of the next when{}.
The chatlog is a chain of cause → effect → cause → effect.
That chain IS the TEF temporal spine.

---

### The chat.AI Class Definition

chat.AI {

    namespace: String
        unique identifier for this chat program
        inherits from parent project namespace if applicable
        child chats spawnable under this namespace

    version: Int
        increments on every reply
        each version is a committed state of this file

    params {
        CONSTANT for this session — not re-evaluated per prompt
        systemPrompt: String
        userPreferences: PreferenceVector
        frameworkDefinitions: QqciSchema
        moralCoord: HegemonyVector (υ, ψ) baseline for this session
        contextRules: RuleSet
        modelID: String
    }

    stateVector: StateVector(7D)
        current Qqci position of the conversation
        updates on every when{} resolution
        starts at params baseline, drifts as topics evolve

    energyBudget: Float
        E remaining for this session's traversal depth
        replenished by external search tool calls
        depletes with each deep retrieval

    chatlog: Dict[version → when{}]
        3-4D live slice of the full 7D dict
        constant dimensions fixed by params (who, where are session-constant)
        live dimensions: what, how, cause, effect
        each entry is a fully encoded TEF when{} instance
        indexed by version number

    contextWindow: RamIndex
        hot slice of chatlog currently in active processing
        sliding window over the chatlog dict
        evicts oldest entries when full
        eviction writes to disk, not deletion — nothing is lost

    filesGenerated: Dict[version → FileRef[]]
        artifacts anchored to the chatlog version that produced them
        a file belongs to the when{} instance that created it
        diff between two file versions stored alongside its chatlog entry
        traversing the file history traverses the thought that produced each version

    traversalHistory: Graph[NodeRef]
        which nodes in the broader knowledge graph were touched this session
        used for maintenance pass — strengthens edges that were traversed

    functions {
        embed(text) → StateVector(7D)
        ionize(queryVector, E) → TraversalChain
        search() → E_reset
        checkpoint() → FileWrite
        merge(otherChat) → chat.AI
        diff(version_a, version_b) → Delta
        spawn(namespace) → chat.AI
    }

    pendingWhen: when{}
        the current prompt being processed
        not yet committed to chatlog
        resolved when reply is generated
        commits as new version on resolution
}

---

### The 3-4D Reduction — MeaningMetaRegistry, Not Chatlog Structure

These are two separate systems with different dimensionality rules.

MeaningMetaRegistry (Meaning.cs) — the semantic language library
6D structure: Registry → TemporalLayer → LanguageLayer → PhraseLayer → WordLayer → CharLayer

In a chat session, three dimensions are session-constant:
RegistryLayer — fixed, one registry per session
TemporalLayer — pinned to current period
LanguageLayer — fixed (English or whatever the session language is)

Leaves 3 live dimensions: PhraseLayer → WordLayer → CharLayer
The hot semantic lookup dict is 3D, with the other 3 stored as constant params.
This is the 3-4D reduction — it applies at the semantic parsing layer only.

The Qqci TEF when{} structure — the conversation architecture
Remains fully 7-plane across all prompts.
Interrogative-agnostic — the when{} instance doesn't care what words mean,
it cares where the exchange sits in causal-intentional space.
All 7 planes are always live. None are collapsed.

How they interact:
prompt arrives as raw text
MeaningMetaRegistry resolves the words — 3D live lookup + 3D from params
resolved meanings are assembled into a when{} TEF instance — full 7D interrogative structure
the when{} is what gets stored in the chatlog and traversed
MeaningMetaRegistry is the parser — TEF is the parsed output

The class therefore holds two separate dict references:

params {
    ...existing params...
    semanticRegistry: MeaningMetaRegistry(3D_live, 3D_constant)
    — the language library, partially collapsed for this session's constant dimensions
}

chatlog: Dict[version → when{}(7D)]
— fully interrogative, language-agnostic once parsed
— stores geometric position, not word meanings

---

### Version Chain as Deterministic Program

Version N's cause = version N-1's effect.
The full chatlog is a deterministic program replayable from version 0.

Two chats with different params but identical chatlog sequences are different programs
that happened to receive the same inputs — their outputs will diverge because their
constant dimensions differ.

Merging two chats is resolving two program branches.
Conflict points are where their stateVectors diverged from a common ancestor.
Git diff handles this natively — the chat.AI file is a Git-tracked object.

---

*Last updated: session 2. Add findings, test results, and parameter discoveries as they come.*
