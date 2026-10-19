# Implementation Plan: Fractal Polytrope Transformer Engine (v2)
**Creation Timestamp:** 2026-10-09T17:35:00+11:00  
**Supersedes:** `plans/PLAN_20261009_v1_Fractal_Polytrope_Transformer.md`  
**Status:** Active Working Plan  
**Project Location:** `polytrope_transformer/`  

---

## 1. Architectural Evolution: The Causal "Is Also" Z-Axis
In v1, the $Z$-axis was tentatively drafted as a binary Actuality vs. Negation floor. Following user alignment, v2 formalizes the true Action-Effect geometry:
1. **The 2D $(\upsilon, \psi)$ Plane**: The Context ($C$). Houses the immediate identity node (`IS` at origin) and the four modal perimeter rays (`can be`, `is not`, `is like`, `was like`).
2. **The Orthogonal $Z$-Axis**: The **"Is Also" Causal Dimension**:
   - Deviation from $0$ measures relational coupling strength and co-presence.
   - **$Z > 0$ ("To Effect Of")**: Downstream consequences, manifest fruits, and resultant yields ($E$ in $A \to E \mid C$).
   - **$Z < 0$ ("To Cause Of")**: Upstream antecedent roots, energetic expenditures, and causal drivers ($A$ in $A \to E \mid C$).
   - **$Z = 0$**: The immediate focal state in isolation.

---

## 2. Updated Phased Roadmap

### Phase 1: Mathematical Foundations & Coordinate Schema (Updated)
- [x] Document core relational kernel in `docs/ARCHITECTURE_SPECIFICATION.md`.
- [x] Archive kernel diagram to `docs/core_polytrope_kernel_diagram.png`.
- [x] Formalize the Causal "Is Also" $Z$-axis ($z < 0$ cause $\leftrightarrow$ $z > 0$ effect) in `src/coordinates.py`.
- [x] Implement 3D angular torque and causal tilt metrics in `src/coordinates.py`.

### Phase 2: Invariant Dictionary Grounding Engine (Current Focus)
- [ ] Ingest QQCI Semantic Dictionary (`aec_dictionary.json` and `qqci_dictionary.json`).
- [ ] Map each root entry to its dual causal vectors: Upstream Root ($A$, $z < 0$) and Downstream Fruit ($E$, $z > 0$).
- [ ] Implement dictionary anchor lookup and multi-plane boundary verification in `src/dictionary_anchor.py`.

### Phase 3: The 42-Cell Multi-Plane Tensor Engine
- [ ] Build $(7 \times 6)$ sub-transformer tensor layers in `src/polytrope_layers.py`.
- [ ] Implement $+1$ observer vertex volume calculation ($v_{\min} = 43 + n$).
- [ ] Construct polyhedral passthrough kernel in `src/passthrough_kernel.py`.

### Phase 4: Benchmarking, Kanon Auditing & 3D Visualizer
- [ ] Benchmark causal tracking on economic and political texts (e.g. tracing inflation to corporate margins vs. worker wages).
- [ ] Connect with 343-vector National Kanon.
- [ ] Build interactive 3D visualizer showing $(\upsilon, \psi, z, \vec{\theta}_{xyz})$.

---

## 3. Running Notes for Post-Compaction
* **Invariant**: Inclusivity is $+\upsilon$ (absorptive, systemic justice); Exclusivity is $-\upsilon$ (private, extractive boundary).
* **Invariant**: Latent Active is $+\psi$ (proactive kinetic creation); Latent Counteractive is $-\psi$ (drag, friction, structural floor).
* **Invariant**: $Z$ is the "Is Also" causal axis: $z < 0$ tracks "to cause of" (upstream inputs), $z > 0$ tracks "to effect of" (downstream fruits), with $|z|$ as coupling strength.
* **Invariant**: The 3D orientation $\vec{\theta}_{xyz}$ tracks roll (thermodynamic cycle) and pitch/yaw (causal tilt between roots and fruits).
* **Invariant**: System dimensionality is $d = 42 + n$, requiring $43 + n$ vertices to maintain non-zero semantic hypervolume.
