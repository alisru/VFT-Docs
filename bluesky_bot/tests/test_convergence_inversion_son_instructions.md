# Test Instructions: Convergence-Inversion Test using the SON Method

This document outlines the test instructions for evaluating context-in-context narratives using the **Multi-Attractor Vector Force Equilibrium (SON) Method**. This protocol calculates coordinates and detects perceptual inversions dynamically.

---

## 1. The 4 Attractor Fields

The coordinate space is defined by four moral/volitional attractors:
*   **Greater Good ($\vec{A}_{GG}$)** = $(+1.0, +1.0)$
*   **Greater Evil ($\vec{A}_{GE}$)** = $(-1.0, -1.0)$
*   **Lesser Good ($\vec{A}_{LG}$)** = $(+1.0, -1.0)$
*   **Lesser Evil ($\vec{A}_{LE}$)** = $(-1.0, +1.0)$

For each attractor $i$, the evaluator provides three readings in the range $[0.0, 1.0]$:
*   **Support ($S_i$)**: Attraction (pull toward $\vec{A}_i$)
*   **Oppose ($O_i$)**: Repulsion (push away from $\vec{A}_i$, which is a pull toward $-\vec{A}_i$)
*   **Neutral ($N_i$)**: Orbit (orthogonal force $\vec{A}_i^{\perp}$)

---

## 2. Mathematical Calculation Step

1.  **Define Orthogonal Vectors**:
    For each attractor vector $\vec{A}_i = (u_i, \psi_i)$, the orthogonal vector $\vec{A}_i^{\perp}$ is defined as:
    $$\vec{A}_i^{\perp} = (-\psi_i, u_i)$$

2.  **Compute Individual Attractor Forces**:
    $$\vec{F}_i = S_i \vec{A}_i - O_i \vec{A}_i + N_i \vec{A}_i^{\perp}$$

3.  **Sum and Normalize**:
    $$\vec{C}_{net} = \frac{1}{\sum_{i} (S_i + O_i + N_i)} \sum_{i} \vec{F}_i$$

---

## 3. Test Cases & Expected Outcomes

We test using the coordinates of the primary research reference **`gaethje-ufc-white-house-show`**:
*   **Macro Container**: Stated $GG$, Actual $GE$ (Birthday ball co-optation).

### Case 1: Co-opted Interpretation (Supports Bad Frame)
*   **Attractor Pulls**:
    *   $GG$ (Greater Good): $S=0.1, O=0.8, N=0.1$ (high opposition/conflict with absolute good)
    *   $GE$ (Greater Evil): $S=0.8, O=0.1, N=0.1$ (strong support/reinforcement of the bad frame)
*   **Expected Coordinate**: Net morality $u < 0$ (pulled negative on the fly).

### Case 2: Subversive Interpretation (Opposes Bad Frame)
*   **Attractor Pulls**:
    *   $GG$ (Greater Good): $S=0.8, O=0.1, N=0.1$ (strong alignment with absolute good)
    *   $GE$ (Greater Evil): $S=0.1, O=0.9, N=0.0$ (strong active opposition to the bad frame)
*   **Expected Coordinate**: Net morality $u > 0$ (pushed positive on the fly).
