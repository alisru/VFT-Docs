# Implementation Plan: Fractal Polytrope Transformer Engine (v1)
**Creation Timestamp:** 2026-10-09T14:40:00+11:00  
**Status:** Active Draft / Phase 1 In Progress  
**Project Location:** `polytrope_transformer/`  

---

## 1. Project Motivation & Core Vision
Standard dense embedding models (BGE, OpenAI, BERT) collapse the multi-plane, multi-dimensional reality of human communication into an ungrounded 1D scalar vector, failing on negation (`is` vs `is not`), modal horizons (`can be`, `is like`, `was like`), and asymmetric physical consequence. 

The objective of this project is to build a functional **Fractal Polytrope Transformer** engine that:
1. Formalizes the hand-drawn relational kernel:
   - Inclusivity axis ($\upsilon \in [-2, +2]$)
   - Will / Latency axis ($\psi \in [-2, +2]$)
   - Actuality depth ($z \in [-1, +1]$)
   - 3D angular trajectory ($\vec{\theta}_{xyz} \in \text{SO}(3)$)
   - 4 Modal Rays (`is`, `can be`, `is not`, `is like`, `was like`)
2. Integrates the $(7 \times 6 + n)$ structural architecture ($7 \text{ Q-Planes} \times 6 \text{ Intent Vectors} = 42 \text{ sub-transformers} + n \text{ context observers} + 1 \text{ volume vertex}$).
3. Grounds training in the dual-stream pipeline: Invariant Dictionary Bedrock (QQCI / AE-C) + Empirical Prose Shearing Loss.

---

## 2. Phased Roadmap

### Phase 1: Mathematical Foundations & Coordinate Schema (Current)
- [x] Document the core relational kernel diagram and coordinate mappings in `docs/ARCHITECTURE_SPECIFICATION.md`.
- [x] Archive the primary diagram image to `docs/core_polytrope_kernel_diagram.png`.
- [x] Verify empirical performance on negation, modal horizons, and directional asymmetry in `drawing board/benchmark_relative_polytrope.py`.
- [ ] Define the formal Python data classes and geometric tensors for $(\upsilon, \psi, z, \vec{\theta}_{xyz})$ in `src/coordinates.py`.

### Phase 2: Invariant Dictionary Grounding Engine
- [ ] Ingest the existing QQCI Semantic Dictionary (`Reality Classification v2/aec_dictionary.json` and `qqci_dictionary.json`) as the invariant bedrock.
- [ ] Map each root entry to its home Q-Plane ($Q_1$ to $Q_7$) and invariant coordinate anchor.
- [ ] Implement the anchor lookup and boundary constraint checker in `src/dictionary_anchor.py`.

### Phase 3: The 42-Cell Multi-Plane Tensor Engine
- [ ] Implement the $(7 \times 6)$ matrix of specialized sub-transformer attention heads in `src/polytrope_layers.py`.
- [ ] Construct the $+1$ observer vertex calculation to guarantee non-zero hypervolume in 42D space.
- [ ] Build the polyhedral passthrough kernel (measuring volume overlap and shearing loss) in `src/passthrough_kernel.py`.

### Phase 4: Integration, Benchmarking & Tool Registry
- [ ] Build an end-to-end tokenizer and inference pipeline in `src/inference.py`.
- [ ] Run comparative semantic audits against the 343-vector National Kanon and Hansard corpus.
- [ ] Provide an interactive visualization interface (rendering 3D gyro-compasses and $(x, y, z, \vec{\theta}_{xyz})$ trajectories).

---

## 3. Running Notes for Post-Compaction
* **Key Invariant**: Inclusivity is explicitly $+\upsilon$ (absorptive, systemic justice); Exclusivity is $-\upsilon$ (private, extractive demarcation).
* **Key Invariant**: Latent Active is $+\psi$ (proaction, kinetic creation); Latent Counteractive is $-\psi$ (drag, friction, structural floor).
* **Key Invariant**: Actuality is $+z$ (`IS`); Negation is $-z$ (`IS NOT`).
* **Key Invariant**: The angle is 3-dimensional ($\vec{\theta}_{xyz}$), enabling the tracking of pitch (potential-to-actuality tilt), roll (4-phase thermodynamic cycle), and yaw (inclusivity-actuality alignment).
* **Key Invariant**: Dimensionality formula is $d = (7 \times 6) + n = 42 + n$, requiring $43 + n$ vertices for non-zero semantic volume.
