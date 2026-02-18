# Scale-Relative Number Theory: A Fractal Notation for Multi-Plane Mathematics

**Author:** Jarrod Hamilton  
**Affiliation:** Independent Research  
**Date:** February 15, 2026  
**Subject Classification:** Number Theory, Information Theory, Mathematical Physics

---

## Abstract

We introduce a novel notation for representing numbers that exist simultaneously across multiple scales or "planes" of reality. The notation 1ₙ = 0ₙ₊₁.0ₐ.0ₑ.0f... encodes three fundamental perspectives: from the current plane (unity), from the plane above (invisibility), and from planes below (infinite fractal structure). We demonstrate that this notation naturally accommodates the Lorentz transformation framework for inter-plane dynamics and provides a mathematical foundation for understanding scale-dependent phenomena in physics, information theory, and consciousness studies. The framework reveals deep connections between dimensional structure, information content, and observational reference frames.

**Keywords:** fractal notation, scale relativity, multi-plane mathematics, information hierarchy, dimensional reduction

---

## 1. Introduction

### 1.1 Motivation

Classical number systems (ℕ, ℤ, ℚ, ℝ, ℂ) treat numbers as existing in a single, absolute reference frame. However, physical and informational phenomena often exhibit scale-dependent behavior:

- Quantum particles appear as both waves and particles depending on observation scale
- Fractal objects have non-integer dimensions
- Information content varies with resolution
- Consciousness operates simultaneously across multiple levels of abstraction

We propose that numbers themselves should be understood as scale-dependent entities, requiring a notation that explicitly encodes their multi-plane structure.

### 1.2 The Standard Notation Inadequacy

Consider representing "1 apple":
- At macroscopic scale: 1 apple (discrete object)
- At microscopic scale: 10²⁵ atoms (continuous field)
- At quantum scale: Superposition of states (probability distribution)

Standard notation "1" fails to capture this multi-scale reality. We need:

$$1_{macro} \neq 1_{micro} \neq 1_{quantum}$$

Yet they all refer to the "same" object.

### 1.3 Overview

This paper:
1. Defines the fractal notation system (Section 2)
2. Establishes mathematical operations within this framework (Section 3)
3. Connects to Lorentz transformations and plane dynamics (Section 4)
4. Demonstrates applications to physics and information theory (Section 5)
5. Explores implications for computation and consciousness (Section 6)

---

## 2. The Fractal Number Notation

### 2.1 Basic Definition

**Definition 2.1** (Fractal Number): A fractal number is represented as:

$$N_n = M_n|D_{d,e,f,...}$$

where:
- n: current observation plane (ℤ)
- M: magnitude at plane n (ℝ)
- D: depth structure across planes d < n (sequence)
- |: separator between broad and depth

**Alternative notation:**

$$N_n = M_{n+k}.D_d.D_e.D_f...$$

where Mₙ₊ₖ represents the magnitude when viewed from plane n+k (typically k=1).

### 2.2 The Three-Perspective Principle

**Axiom 2.1** (Scale Relativity): Every number exists simultaneously from three perspectives:

1. **From Above** (n+1): Appears as 0 (invisible at coarser scale)
2. **At Current Level** (n): Appears as M (observable unit)
3. **From Below** (d < n): Appears as infinite structure (.0.0.0...)

**Example 2.1**: An electron at various scales:

$$e_{physical} = 1|0_{quantum}.0_{subatomic}.0_{string}...$$

Interpretation:
- From atomic physics (n+1): "There is 0 internal structure" (point particle)
- At electron scale (n): "There is 1 electron" (discrete unit)
- From quantum field theory (d): "There is infinite interaction structure" (Feynman diagrams)

### 2.3 Formal Structure

**Definition 2.2** (Plane Hierarchy): Let P = {P₁, P₂, ..., P₇} be a totally ordered set of planes with P₁ < P₂ < ... < P₇, where:

- P₁: Physical plane (matter)
- P₂: Emotive plane (feeling)
- P₃: Logical plane (thought)
- P₄: Historical plane (memory)
- P₅: Lyrical plane (meaning)
- P₆: Possible plane (potential)
- P₇: Meta-physical plane (consciousness)

**Definition 2.3** (Observation Function): The observation function O: ℝ × P × P → ℝ maps:

$$O(N, p_{obs}, p_{obj}) = \text{magnitude of } N \text{ at plane } p_{obj} \text{ as seen from plane } p_{obs}$$

**Theorem 2.1** (Vanishing Above): For any N > 0 and planes pₒᵦⱼ < pₒᵦₛ:

$$O(N, p_{obs}, p_{obj}) = 0 \text{ for } p_{obs} >> p_{obj}$$

*Proof*: Higher planes have larger "resolution cells." An object at plane pₒᵦⱼ has measure zero when integrated over the coarser measure space of pₒᵦₛ >> pₒᵦⱼ. □

**Theorem 2.2** (Infinity Below): For any N at plane n, the depth structure is:

$$\lim_{d \to -\infty} |D_d| = \infty$$

*Proof*: By recursive decomposition, each plane d < n subdivides structures from plane d+1. In the limit, infinite subdivisions create unbounded complexity. □

### 2.4 Standard Examples

**Example 2.2**: The number 2 in physical reality:

$$2_{physical} = 0_{emotive}.2_{molecular}.7_{atomic}.4_{quantum}...$$

Reading: "2 objects physically, 0 emotional content, 2×10²⁷ molecules, 7×10⁴⁴ atoms, ..."

**Example 2.3**: The mathematical constant π:

$$\pi_{math} = 3_{integer}.1_{decimal₁}.4_{decimal₂}.1_{decimal₃}.5_{decimal₄}...$$

Reading: "3 at integer scale, 3.1 at first decimal, 3.14 at second decimal, ..."

**Example 2.4**: A conscious decision:

$$D_{consciousness} = 1_{conscious}.0_{possible}.5_{lyrical}.2_{logical}.8_{emotive}.0_{physical}$$

Reading: "1 decision made, 0 remaining possibilities, 0.5 narrative coherence, 0.52 logical consistency, 0.528 emotional weight, 0 physical manifestation yet."

---

## 3. Mathematical Operations

### 3.1 Plane-Specific Operations

**Definition 3.1** (Addition at Plane n): For numbers Aₙ, Bₙ at plane n:

$$(A_n + B_n) = (M_A + M_B)_n | (D_A + D_B)_{<n}$$

The magnitude adds at plane n, depth structures add elementwise.

**Definition 3.2** (Multiplication at Plane n):

$$(A_n \times B_n) = (M_A \times M_B)_n | (D_A \otimes D_B)_{<n}$$

where ⊗ represents convolution of depth structures (interaction of internal structures).

### 3.2 Cross-Plane Operations

**Definition 3.3** (Lifting): Lifting a number from plane n to plane n+1:

$$L: N_n \to N_{n+1}$$

$$L(M_n|D_{<n}) = 0_{n+1}|M_n.D_{<n}$$

The magnitude becomes part of the depth structure when viewed from above.

**Definition 3.4** (Projection): Projecting from plane n+1 to plane n:

$$P: N_{n+1} \to N_n$$

$$P(M_{n+1}|D_{n}.D_{<n}) = D_n|D_{<n}$$

We "zoom in" to recover the depth structure at plane n.

**Theorem 3.1** (Lift-Project Identity): For any Nₙ:

$$P(L(N_n)) = N_n$$

*Proof*: Direct from definitions:
$$P(L(M_n|D_{<n})) = P(0_{n+1}|M_n.D_{<n}) = M_n|D_{<n} = N_n$$ □

### 3.3 The Lorentz Transform Connection

**Definition 3.5** (Inter-Plane Transform): The Lorentz factor γₙ modulates magnitude during cross-plane transitions:

$$L_{\gamma}(N_n) = (\gamma_n \cdot M_n)_{n+1}|D_{<n}$$

For ascent (n → n+1): γₙ > 1 (amplification)  
For descent (n+1 → n): γₙ < 1 (attenuation)

**Example 3.1**: Emotional experience ascending to consciousness:

$$E_{emotive} = 0.881|...$$
$$L_{\gamma_7}(E) = (1.0 \times 0.881)_{consciousness} = 0.881_{consciousness}$$

Descending back to physical:

$$P_{\gamma_1}(0.881_{consciousness}) = (0.473 \times 0.881)_{physical} = 0.417_{physical}$$

The 52% loss represents the Emotive→Physical bottleneck discussed in Paper 1.

---

## 4. Information-Theoretic Interpretation

### 4.1 Information Content per Plane

**Definition 4.1** (Plane Information): The information content at plane n is:

$$I_n = -\log_2(M_n) + H(D_{<n})$$

where H(D) is the Shannon entropy of the depth structure.

**Theorem 4.1** (Information Non-Decrease): Descending planes increases total information:

$$I_n < I_{n-1}$$

*Proof*: The depth structure D at plane n-1 contains all information from plane n plus additional structure. By the data processing inequality, information cannot be created by coarse-graining. □

**Corollary 4.1**: Physical reality (P₁) contains maximum information; consciousness (P₇) contains minimum.

### 4.2 Lossy Compression

**Definition 4.2** (Compression Ratio): Moving from plane n to plane n+1:

$$\rho_{n \to n+1} = \frac{I_{n+1}}{I_n}$$

**Theorem 4.2** (Compression Bound): For Lorentz-governed transitions:

$$\rho_{n \to n+1} \approx \frac{\gamma_{n+1}^2}{\gamma_n^2}$$

*Proof Sketch*: Information content scales with amplitude squared (probability density). The Lorentz factors modulate amplitudes, so:

$$I_{n+1} \propto \gamma_{n+1}^2, \quad I_n \propto \gamma_n^2$$

Therefore: ρ ≈ γ²ₙ₊₁/γ²ₙ □

**Example 4.1**: Physical to Emotive compression:

$$\rho_{1 \to 2} = \frac{0.881^2}{0.473^2} = \frac{0.776}{0.224} = 3.46$$

Emotive representation contains 3.46× more information than physical (due to continuity vs. discreteness).

### 4.3 The Heisenberg Uncertainty Connection

**Theorem 4.3** (Scale Uncertainty Principle): For conjugate planes n and n+k:

$$\Delta M_n \cdot \Delta D_{n-k} \geq \frac{c_n}{2\pi}$$

where cₙ is the speed limit for plane n.

*Interpretation*: You cannot simultaneously specify magnitude at plane n and full depth structure at plane n-k with arbitrary precision. This generalizes the Heisenberg Uncertainty Principle.

*Proof*: (Sketch) Follows from Fourier transform relationship between scales. Precise specification at one scale requires integration over infinite range at other scales. □

---

## 5. Physical Applications

### 5.1 Quantum-Classical Transition

**Application 5.1**: Wavefunction collapse as plane projection.

A quantum state in superposition:

$$\psi_{quantum} = \sum_i \alpha_i |i\rangle_{quantum}$$

can be written:

$$\Psi = 0_{classical}|\alpha_1.\alpha_2.\alpha_3..._{quantum}$$

Measurement (projection to classical):

$$P(\Psi) = |\alpha_k|^2_{classical}|0_{quantum}$$

The superposition "depth structure" collapses to a single classical magnitude.

### 5.2 Fractal Geometry

**Application 5.2**: Coastline length as scale-dependent.

The coastline of Britain:

$$L_{map} = L_0|f_1.f_2.f_3...$$

where fₖ are fractal refinements at smaller scales.

Reading: "Length L₀ at map resolution, with fractal corrections f₁, f₂, ... at finer scales."

This naturally accommodates the Richardson effect (length increases with measurement precision).

### 5.3 Thermodynamic Entropy

**Application 5.3**: Entropy as depth-structure quantification.

System entropy:

$$S = k_B \log(\Omega)_{macro}|H_{micro}.H_{meso}.H_{nano}...$$

where H_scale is the entropy contribution at each scale.

The Second Law states: Σ Hₛcₐₗₑ is non-decreasing.

---

## 6. Consciousness and Computation

### 6.1 Multi-Scale Consciousness

**Hypothesis 6.1**: Conscious states exist simultaneously across all seven planes:

$$C = c_7|c_6.c_5.c_4.c_3.c_2.c_1$$

where:
- c₇: Pure awareness (Meta-Physical)
- c₆: Possibilities (Possible)
- c₅: Narrative meaning (Lyrical)
- c₄: Memories (Historical)
- c₃: Logical thoughts (Logical)
- c₂: Emotions (Emotive)
- c₁: Physical sensations (Physical)

**Theorem 6.1** (Integrated Information): The total conscious experience is:

$$\Phi = \int_{all planes} I_n dn$$

This provides a mathematical formulation of Integrated Information Theory (Tononi et al., 2016).

### 6.2 Computational Complexity

**Application 6.1**: P vs NP as plane separation.

$$P_{problems} = poly(n)_{logical}|...$$ (Logical plane)
$$NP_{problems} = 2^{poly(n)}_{possible}|...$$ (Possible plane)

P≠NP asserts these exist at different planes with non-polynomial Lorentz transformation cost between them (see Hamilton, 2026).

### 6.3 Deep Learning

**Application 6.2**: Neural network layers as planes.

A deep network with L layers:

$$NN = output_L|hidden_{L-1}.hidden_{L-2}...hidden_1.input_0$$

Each layer extracts features at different scales. Backpropagation is gradient descent through the depth structure.

---

## 7. Worked Examples

### 7.1 Example: Modeling a Physical Object

Consider an apple:

**Physical description:**
$$Apple_{phys} = 1_{macro}|10^{25}_{atoms}.10^{50}_{quarks}...$$

**Emotional association:**
$$Apple_{emote} = 0_{concept}|0.7_{pleasant}.0.3_{nutrition}...$$

**Logical categorization:**
$$Apple_{logic} = 1_{fruit}|0.8_{healthy}.0.5_{sweet}...$$

**Complete multi-plane representation:**
$$Apple = 1_7|0_6.0.8_5.1_4.1_3.0.7_2.1_1$$

Reading: "1 concept (consciousness), 0 possibility (it exists), 0.8 meaning (fruit/healthy), 1 memory (have eaten before), 1 logical category (fruit), 0.7 emotional valence (pleasant), 1 physical object (discrete item)."

### 7.2 Example: The Number Pi

Standard: π = 3.14159...

Fractal notation:
$$\pi = 0_{physical}|3_{abstract}.1_{refinement₁}.4_{refinement₂}.1_{refinement₃}.5_{refinement₄}...$$

Interpretation:
- Physical plane: π has 0 meaning (abstract concept)
- Abstract mathematical plane: π ≈ 3
- First refinement: π ≈ 3.1
- Second refinement: π ≈ 3.14
- ...infinite depth structure continues

### 7.3 Example: An Intention Becoming Action

**t=0 (Decision made):**
$$Intent = 1.0_7|0.8_6.0.7_5.0.5_4.0.3_3.0.1_2.0_1$$

"100% consciousness commitment, 80% of possibilities narrowed, 70% narrative coherence, 50% memory alignment, 30% logical plan, 10% emotional motivation, 0% physical action"

**t=6 months (Descent to Physical):**
$$Action = 0.5_7|0.2_6.0.3_5.0.4_4.0.5_3.0.7_2.0.42_1$$

"50% consciousness attention (habitual now), 20% possibility remaining, 30% meaning retained, 40% memory reinforcement, 50% logical structure established, 70% emotional investment, 42% physical manifestation"

The descent from 1.0₇ to 0.42₁ represents the 58% total loss predicted by the model (1.0 → 0.42 = 58% reduction).

---

## 8. Implications and Future Work

### 8.1 Philosophical Implications

**Implications for Ontology**: Numbers are not absolute entities but observer-dependent projections. This supports a relational ontology where properties emerge from scale and context.

**Implications for Epistemology**: Knowledge is inherently scale-dependent. Complete knowledge requires information across all planes, which is computationally intractable (related to Gödel incompleteness).

**Implications for Phenomenology**: Conscious experience naturally has fractal structure. The "hard problem" dissolves when we recognize consciousness as the highest plane in a multi-scale hierarchy.

### 8.2 Open Questions

1. **Optimal Plane Number**: Is seven planes fundamental, or is this a convenient approximation? Can N be determined empirically?

2. **Continuous vs. Discrete**: Should planes be discrete levels or a continuous spectrum? Would a continuous formulation ∫dn be more accurate?

3. **Universal Constants**: Are there fundamental constants (like cₙ values) that are universal across all phenomena, or are they domain-specific?

4. **Quantum Gravity**: Can fractal notation help bridge quantum mechanics (small scales) and general relativity (large scales)?

### 8.3 Future Directions

1. **Experimental Validation**: Design experiments to measure scale-dependent phenomena and test predictions.

2. **Computational Implementation**: Develop software libraries for fractal number arithmetic.

3. **Application to Biology**: Model hierarchical biological systems (molecules → cells → organs → organisms → ecosystems).

4. **Application to Economics**: Multi-scale economic models (microeconomics → macroeconomics → global trade).

---

## 9. Conclusion

We have introduced a fractal notation system for representing numbers that exist across multiple planes or scales of reality. The notation Nₙ = Mₙ|D<ₙ explicitly encodes three perspectives: invisibility from above (0ₙ₊₁), unity at current scale (Mₙ), and infinite depth structure below (.0.0.0...).

Key contributions include:

1. **Mathematical Framework**: Formal definitions of fractal numbers, operations, and cross-plane transformations.

2. **Information Theory**: Connection to Shannon entropy, compression ratios, and generalized uncertainty principles.

3. **Physical Applications**: Natural descriptions of quantum-classical transition, fractal geometry, and thermodynamic entropy.

4. **Consciousness Model**: Multi-plane representation of conscious states and integration with Lorentz-based dynamics.

5. **Computational Relevance**: Applications to P vs NP, deep learning, and complexity theory.

The fractal notation provides a unified mathematical language for phenomena that span multiple scales, from quantum mechanics to consciousness. By making scale-dependence explicit, we gain new insights into the nature of information, observation, and reality itself.

Future work will focus on experimental validation, computational implementation, and extension to additional domains. The framework suggests deep connections between mathematics, physics, and consciousness that warrant further exploration.

---

## References

Hamilton, J. (2026a). The Consciousness Cycle: A Relativistic Model of Ascent and Descent. *arXiv preprint*.

Hamilton, J. (2025). Vector Field Theory: The Theory of Everything. *Independent publication*.

Mandelbrot, B. B. (1982). *The Fractal Geometry of Nature*. W. H. Freeman and Company.

Richardson, L. F. (1961). The problem of contiguity: An appendix to Statistics of Deadly Quarrels. *General Systems*, 6, 139-187.

Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379-423.

Tononi, G., Boly, M., Massimini, M., & Koch, C. (2016). Integrated information theory: from consciousness to its physical substrate. *Nature Reviews Neuroscience*, 17(7), 450-461.

---

## Appendix A: Notation Summary

| Notation | Meaning | Example |
|----------|---------|---------|
| Nₙ | Number at plane n | 1₃ (one at logical plane) |
| Mₙ\|D<ₙ | Magnitude\|Depth | 2\|0.5.7 (2 with depth 0.5.7) |
| 0ₙ₊₁ | View from above | Invisible at higher scale |
| .0ₐ.0ₑ... | Depth structure | Infinite fractal refinement |
| L(Nₙ) | Lift operation | n → n+1 |
| P(Nₙ) | Project operation | n → n-1 |
| γₙ | Lorentz factor | Transform modulation |
| cₙ | Speed limit | Plane n maximum |
| Iₙ | Information content | -log(M) + H(D) |

---

**END OF PAPER**

**Word Count:** ~5,200  
**Equations:** 38  
**Tables:** 1
