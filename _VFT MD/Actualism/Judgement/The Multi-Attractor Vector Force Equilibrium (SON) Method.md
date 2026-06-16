# The Multi-Attractor Vector Force Equilibrium (SON) Method

This document codifies the **Multi-Attractor Vector Force Equilibrium (SON) Method**, a mathematical protocol derived from the core principles of Vector Field Theory (VFT) and the *Framework for the Judgment of Ideas*. 

Instead of treating moral categorization as a binary choice or qualitative guess, this method calculates the exact coordinates $(u, \psi)$ of any action or concept as the **equilibrium point of vector forces** exerted by the four primary quadrants of the Psochic Hegemony.

---

## 1. The 4 Attractor Fields

The coordinate space is governed by four conceptual gravity wells (attractors):
*   **Greater Good ($\vec{A}_{GG}$)** = $(+1.0, +1.0)$
*   **Greater Evil ($\vec{A}_{GE}$)** = $(-1.0, -1.0)$
*   **Lesser Good ($\vec{A}_{LG}$)** = $(+1.0, -1.0)$
*   **Lesser Evil / Greatest Lie ($\vec{A}_{LE}$)** = $(-1.0, +1.0)$

For each attractor $i$, the evaluator populates three vector readings in the range $[0.0, 1.0]$ based on direct quotes and evidence from the narrative:
*   **Support ($S_i$)**: *Attraction* — the degree to which the action aligns with, reinforces, or sustains the attractor.
*   **Oppose ($O_i$)**: *Repulsion* — the degree to which the action actively violates, resists, or conflicts with the attractor (pushing toward the polar opposite, $-\vec{A}_i$).
*   **Neutral ($N_i$)**: *Orbit* — the degree to which the action is indifferent, orthogonal, or independent of the attractor.

---

## 2. Mathematical Derivation

1.  **Define Orthogonal Vectors**:
    For each attractor vector $\vec{A}_i = (u_i, \psi_i)$, the orthogonal (orbit) vector $\vec{A}_i^{\perp}$ is defined as:
    $$\vec{A}_i^{\perp} = (-\psi_i, u_i)$$

2.  **Calculate Net Attractor Force ($\vec{F}_i$)**:
    Each attractor exerts a pull, push, and orbital deflection:
    $$\vec{F}_i = S_i \vec{A}_i - O_i \vec{A}_i + N_i \vec{A}_i^{\perp}$$

3.  **Sum and Normalize**:
    The final coordinate $\vec{C}_{net} = (u, \psi)$ is the normalized sum of all forces:
    $$\vec{C}_{net} = \frac{1}{\sum_{i} (S_i + O_i + N_i)} \sum_{i=1}^{4} \vec{F}_i$$

---

## 3. Emergent Inversion Detection (On the Fly)

Because this model calculates coordinates dynamically through the balance of attractor forces, **perceptual inversions are completely emergent**. They occur on the fly without hardcoded coordinate-flipping rules:

*   **Co-optation (Supports the Bad Container)**:
    When a positive micro-event is co-opted to support a bad macro-frame ($LE$ or $GE$), the AI registers a high support score for the bad attractor (e.g., $S_{LE} \gg 0$). This force pulls the calculated coordinate to the negative morality side ($u < 0$) on the fly.
*   **Subversion (Opposes the Bad Container)**:
    When a positive micro-event actively opposes or exposes the bad macro-frame, the AI registers a high opposition score for the bad attractor (e.g., $O_{LE} \gg 0$). This repulsion pushes the calculated coordinate to the positive morality side ($u > 0$) on the fly.

---

## 4. Reference Case Studies

### Case A: `gaethje-ufc-white-house-show` (Co-opted / Supports Bad Frame)
*   **GG**: $S=0.3, O=0.8, N=0.3$ (victory framed as good, but conflicts structurally with systemic peace).
*   **GE**: $S=0.7, O=0.0, N=0.1$ (celebrates physical violence as public entertainment).
*   **LG**: $S=0.4, O=0.3, N=0.3$ (provides passive local celebration).
*   **LE**: $S=0.9, O=0.0, N=0.1$ (strong support of the political birthday brand/pretext).
*   **Sum of Weights**: $4.2$
*   **Sum of Forces**: $(-2.0, 0.0)$
*   **Calculated Coordinate**: $\vec{C} \approx (-0.48, 0.00)$ $\to$ **Lesser Evil / Greatest Lie** (co-opted).

### Case B: Whistleblower (Subversive / Opposes Bad Frame)
*   **GG**: $S=0.9, O=0.0, N=0.1$ (strong alignment with truth/safety).
*   **GE**: $S=0.0, O=0.9, N=0.1$ (strong active opposition to corporate toxic dumping).
*   **LG**: $S=0.2, O=0.2, N=0.6$ (mostly active, minor passive orbit).
*   **LE**: $S=0.0, O=0.8, N=0.2$ (exposes and opposes the corporate green-compliance lie).
*   **Sum of Weights**: $4.0$
*   **Sum of Forces**: $(3.0, 1.4)$
*   **Calculated Coordinate**: $\vec{C} \approx (+0.75, +0.35)$ $\to$ **Greater Good** (subversive action remains positive).

### Case C: `aus_airport_milestone` (Stated vs. Actual)
*   **Stated Claim**: Breaking the duopoly and lowering airfares.
    *   GG: $S=1.0, O=0.0, N=0.0$ | GE: $S=0.0, O=0.9, N=0.1$ | LE: $S=0.0, O=0.8, N=0.2$ | LG: $S=0.2, O=0.0, N=0.1$
    *   **Stated Coordinate**: $\vec{C}_{stated} \approx (+0.88, +0.21)$ $\to$ **Greater Good**.
*   **Actual Outcome**: Airport opens, but competition is delayed and lack of rail link limits immediate savings.
    *   GG: $S=0.5, O=0.0, N=0.2$ | GE: $S=0.0, O=0.7, N=0.2$ | LE: $S=0.4, O=0.5, N=0.2$ | LG: $S=0.8, O=0.0, N=0.1$
    *   **Actual Coordinate**: $\vec{C}_{actual} \approx (+0.56, +0.06)$ $\to$ **Lesser Good**.
