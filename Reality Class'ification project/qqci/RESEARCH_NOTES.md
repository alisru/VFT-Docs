# Prior Art: Geometric Transformers and Structured Semantic Bases

Compiled 2026-07-21. All sources fetched this session; quotes are verbatim from the fetched pages.

---

## 1. Sovereign-Lila-E8 (the closest existing thing to this project)

- Repo: https://github.com/meta-introspector/sovereign-lila-e8
- Paper: https://www.academia.edu/164927700/Lila_E8_A_Geometric_Attention_Transformer_with_the_E8_Root_System
- Author: A. Kornienko, independent researcher. DOI 10.5281/zenodo.18731390. AGPLv3.
- Mirror/fork: https://github.com/SPUTNIKAI/E8-TRANSFORMER

Motto on the repo: **"Scale is the shadow, Geometry is the Light."**

### What it does

"By softly quantizing hidden states into the 240 roots of E8 and adding geometric biases to attention scores, the model achieves dense semantic packing and improved long-context coherence."

### Results

- 40M parameters, TinyStories, free Colab GPU. Loss 9.5 to 0.37 over 156k steps.
- Validation loss 0.46 to 0.6, "significantly lower than standard Transformer baselines of comparable scale."
- Coherent stories to 512 tokens (full training length), extrapolates to 1500 tokens without repetitive loops. Microsoft's comparable 33M/60M baseline "exhibits hard loops after 300-500 tokens."
- **Ablation:** "Disabling the geometric attention bias increases validation loss by 0.0221 (p < 0.001), proving that the E8 structure contributes meaningfully to performance."

### Mechanisms

- Differentiable E8 quantization with a straight-through estimator.
- Geometric attention bias: "Each attention head can learn to align with a specific E8 root vector, adding a learnable geometric bias to the standard dot-product scores."
- **Hierarchical self-organisation of geometry use:** "The distribution of these head scales (beta) across layers reveals a hierarchical self-organization: early layers ignore geometry, middle layers use it most strongly, and later layers moderately."
- Soft quantization "acts as a structured regularizer, packing information more densely and reducing hallucinations."
- **E8GraphResonator:** an optional associative memory that "stores token-to-token relations directly on the E8 root graph. During generation, it biases predictions toward contextually related tokens." Each token maps to its nearest of 240 roots; co-occurrence writes a relation. Tunable via `--resonance_strength` (0.05 to 0.15) and `--encode_relation_weight`.
- All checkpoints from step 0 to 170k released; the model is designed to be community-trainable and "living".

### Why this matters to us

This is the core bet of the whole scope document, already tested by someone else and passing: a fixed geometric structure imposed on attention beats an unstructured baseline at small scale. The ablation is the important number, because it isolates the geometry rather than the model.

The difference remains the one the scope doc claims: E8's 240 roots are mathematically beautiful but **semantically anonymous**. Nobody can say what root 137 means. A 7-plane basis is named. So Lila-E8 validates the mechanism and leaves the interpretability claim untouched.

Also note the resonator: an associative memory over a fixed graph, written during generation. That is Section 4's Hopfield-attractor-over-structured-skeleton, running in production code.

---

## 2. Leech-LILA (the buildable template)

- Paper: https://zenodo.org/records/18784424/files/Envoy_LEECH_LILA_V1_.pdf
- Same author, 26 Feb 2026. AGPLv3.
- Framework paper: "Geometric Attention: A General Framework for Injecting Discrete Symmetries into Transformers via High-Dimensional Lattices", doi:10.5281/zenodo.18729723

**This paper is the recipe we should copy, substituting our basis for theirs.**

### The mechanism, exactly

1. Take 24 linearly independent minimal vectors of the Leech lattice as matrix G.
2. QR decompose: G = QR, giving orthonormal Q (24x24).
3. Build `W_Leech = block_diag(Q, Q, ..., Q)`, frozen, never updated.
4. **Replace the learnable query and key projections with it:** `Q = X W_Leech`, `K = X W_Leech^T`. The value projection stays learnable.
5. Add a **resonance loss**: for hidden state h split into K blocks of 24, resonance of block k is the max absolute cosine similarity to any basis vector q_j. Then `L_res = 1 - mean(s_k)` and total `L = L_CE + lambda * L_res` with lambda around 0.01.

Their words: the frozen core "acts as a high-dimensional symmetry filter, guiding hidden representations toward lattice nodes and preventing attention collapse", and the resonance loss "softly pulls hidden states toward lattice nodes" and acts "as an anti-hallucination regularizer". The latent space is partitioned into independent 24-dimensional "semantic cells" by the block-diagonal structure.

Config: d_model 192 (24 x 8), 12 layers, 8 heads, head_dim 24, 40M params. Val loss ~0.45 at 150k steps, coherent to 1500 tokens.

Working PyTorch code for `LeechAttention` and `LeechResonanceLoss` is printed in the paper.

### The substitution we would make

Replace the 24-dimensional Leech basis with a 7-plane basis (or 7 x n for sub-addresses). Everything else is unchanged:

- frozen block-diagonal projection on Q and K -> our frozen plane axes (scope doc Section 9 risk 1, option three: "frozen plane axes with learning confined inside planes")
- semantic cells -> planes, but NAMED
- resonance loss -> **the differentiable form of the fill gate.** This is the answer to the non-differentiability problem flagged for the contextual min-max gate: alignment-to-basis as a soft penalty, not a hard threshold.
- resonance loss as anti-hallucination regularizer -> our false-fill detector, in trainable form

That makes the trained variant (build posture C) a small, well-defined delta on published working code, rather than a from-scratch research project.

---

## 3. The Curved Spacetime of Transformer Architectures

- Paper: https://arxiv.org/pdf/2511.03060 (6 Nov 2025)
- Code: https://github.com/rdisipio/llm-curvature

Frames attention as differential geometry: "queries and keys induce an effective metric on representation space, and attention acts as a discrete connection that implements parallel transport of value vectors across tokens." Stacked layers are "discrete time-slices"; a token's path through layers "approximates a discrete geodesic: each layer corresponds to a tick in semantic time." Backpropagation is a least-action principle over an effective action S_LM.

Two pieces worth stealing:

- **Multi-head attention as an atlas of charts.** "Each attention head defines its own (W_Q, W_K, W_V) projections, effectively a separate chart on the manifold... multi-head attention provides overlapping local views. The output projection W_O acts as a transition map." That is precisely the parallax framing (many vantages, one object) with established mathematical vocabulary, and it is a better citation for Section 13 than the webcam story.
- **The deflection experiment.** They test curvature by measuring whether a disambiguator bends a token's trajectory ("bank" with and without "river"), modelled on gravitational lensing. That is a ready-made experimental design for testing whether OUR planes bend trajectories the way they should.

Their stated limitation is also our opening: "In General Relativity, curvature and matter interact dynamically (back-reaction), whereas Transformer inference unfolds in a static geometry: the W_Q and W_K matrices define the manifold but remain fixed once trained. A natural direction for future work is to explore architectures where these matrices adapt during inference."

Adaptation during inference is exactly what the scope doc's Query-IS-the-Write plus attractor-deformation memory describes. They name it as future work; the scope doc has a design for it.

---

## 4. Supporting references

- **TinyStories** (Eldan and Li, arXiv 2305.07759): models below 10M parameters, or with a single transformer block, produce fluent coherent stories. This is the corpus and the evidence base for the potato-hardware goal, and it is what both LILA models train on. GPT-4-as-grader evaluation paradigm included.
- **Reactive Transformer / RxT** (arXiv 2510.03561): event-driven stateful architecture, fixed-size short-term memory, asynchronous memory consolidation, residual gates, linear O(N*T) conversation cost. Nearest sibling for the stateful half.
- **Neural Basis Models** (Radenovic, Dubey, Mahajan, NeurIPS 2022): GAMs with a small shared basis of learned shape functions, interpretable by construction. https://github.com/facebookresearch/nbm-spam
- **Mechanistic interpretability survey** (ACM Computing Surveys, Feb 2026, doi 10.1145/3787104): current state of superposition, polysemanticity, circuits, sparse dictionary learning. The toolbox for Experiment -1.
- **Geometry-guided transformers** overview: https://www.emergentmind.com/topics/geometry-guided-transformer

---

## 5. Where this leaves the project

Validated by prior art, no longer speculative:

- fixed geometric structure on attention improves small models (Lila-E8 ablation, p < 0.001)
- frozen basis plus alignment loss is trainable and stable (Leech-LILA)
- associative memory over a fixed graph works during generation (E8GraphResonator)
- attention as transport on a structured manifold is a defensible formalism (Curved Spacetime)
- small models can be coherent (TinyStories)
- stateful beats stateless for dialogue (RxT)

Still unclaimed by anyone, and therefore still ours to prove:

- a **named** basis. E8 roots and Leech vectors are anonymous. The 7 planes are not.
- **moral/functional content on the axes** (Sovereignty/Tyranny, Truth-Telling/Delusion, etc). No published geometric transformer carries semantics on its basis vectors.
- **unipolar-around-Unity scoring**, where excess and deficit are the same sin. Every published system uses bipolar or unbounded coordinates.
- **R_net as a coherence measure** (1/product), which can diverge to infinity when one plane collapses. No published loss has this property.
- the **isomorphic-retelling verification** capability.

The honest framing for any writeup: we are not proposing geometric attention, which now has prior art. We are proposing that the geometry be *named and morally typed*, and the claim to test is that a named basis costs little against an anonymous one while buying legibility.
