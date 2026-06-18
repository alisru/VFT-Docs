# Convergence Test (SON Lite)

Token-efficient instructions for batch evaluation. Silent internal calculations. Outputs JSON.

---

## 1. The 7 Planes

| Q | Plane | Interrogative | Pass Condition |
|---|---|---|---|
| Q1 | Metaphysical | WHO | Stated beneficiary matches actual beneficiary |
| Q2 | Possible | WHAT | Failure modes acknowledged, not suppressed |
| Q3 | Physical | WHERE | Concrete, falsifiable physical prediction exists |
| Q4 | Lyrical | WHY | Narrative honest; no obfuscation required |
| Q5 | Logical | HOW | Causal chain holds under load/adversity |
| Q6 | Historical | CAUSE | Origin chain acknowledged; history not erased |
| Q7 | Emotive | EFFECT | Emotional payload matches stated intent |

Scoring: **PASS** (1.0), **PARTIAL** (fractional), or **FAIL** (0.0 / Phantom fill).

---

## 2. Phase 2 — Vector Verification (SON Method)

Coordinates calculated as the equilibrium point of attractor forces:
*   **Greater Good ($\vec{A}_{GG}$)** = $(+1.0, +1.0)$ | $\vec{A}_{GG}^{\perp} = (-1.0, +1.0)$
*   **Greater Evil ($\vec{A}_{GE}$)** = $(-1.0, -1.0)$ | $\vec{A}_{GE}^{\perp} = (+1.0, -1.0)$
*   **Lesser Good ($\vec{A}_{LG}$)** = $(+1.0, -1.0)$ | $\vec{A}_{LG}^{\perp} = (+1.0, +1.0)$
*   **Lesser Evil ($\vec{A}_{LE}$)** = $(-1.0, +1.0)$ | $\vec{A}_{LE}^{\perp} = (-1.0, -1.0)$
*   **Good Preference ($\vec{A}_{GP}$)** = $(+1.0, 0.0)$ | Oppose ($O_{GP}$) drives Will negative ($\psi \to -1$), Neutral ($N$) has $0.0$ force.
*   **Bad Preference ($\vec{A}_{BP}$)** = $(-1.0, 0.0)$ | Oppose ($O_{BP}$) drives Will positive ($\psi \to +1$), Neutral ($N$) has $0.0$ force.

For each attractor $i$, score $[0.0, 2.0]$ based on evidence:
*   **Support ($S_i$)**: Attraction.
*   **Oppose ($O_i$)**: Repulsion.
*   **Neutral ($N_i$)**: Orbit (for moral attractors) or Dilution (for preferences).

Scoring: $0.0$ = No force | $1.0$ = Condition Met (Human Horizon) | $2.0$ = Totality of Exceedence (Systemic Horizon / Double gravity weight).

### Formulas (18-Variable Parameter Space)
To maintain structural resolution and prevent coordinate collapse, **every single one of the 6 attractors MUST have its full $[S_i, O_i, N_i]$ triple scored** (18 variables in total). Scoring only a single dominant aspect per point is a methodological error.

1. **Net Attractor Force ($\vec{F}_i$):**
   * For Moral Attractors ($GG, GE, LG, LE$):
     $$\vec{F}_i = S_i \vec{A}_i - O_i \vec{A}_i + N_i \vec{A}_i^{\perp}$$
   * For Good Preference ($GP$):
     $$\vec{F}_{GP} = S_{GP} (1.0, 0.0) - O_{GP} (1.0, 1.0)$$
   * For Bad Preference ($BP$):
     $$\vec{F}_{BP} = S_{BP} (-1.0, 0.0) - O_{BP} (-1.0, -1.0)$$

2. **Morality Coordinate ($u$):**
   Sum and normalize the $u$-components of the forces across all 6 attractors:
   $$u = \frac{\sum_{i=1}^{6} F_{i, u}}{\sum_{i=1}^{6} (S_i + O_i + N_i)}$$

3. **Will Coordinate ($\psi$) — Separated Will (Like-Type) Protocol:**
   To prevent positive narrative spin ($S_{LE}$) and actual physical destruction ($S_{GE}$) from cancelling each other out to a neutral stasis ($\psi \approx 0$), calculate positive and negative Will forces independently:
   *   Group forces by Will sign:
       *   $\Psi_{\text{pos}} = \{i \mid F_{i, \psi} > 0\}$
       *   $\Psi_{\text{neg}} = \{i \mid F_{i, \psi} < 0\}$
   *   Sum absolute force magnitudes for each direction:
       *   $F_{\text{pos}} = \sum_{j \in \Psi_{\text{pos}}} |F_{j, \psi}|$
       *   $F_{\text{neg}} = \sum_{k \in \Psi_{\text{neg}}} |F_{k, \psi}|$
   *   Identify the dominant direction and calculate $\psi$ using ONLY that dominant group:
       *   If $F_{\text{pos}} \ge F_{\text{neg}}$: Net Will is positive (constructive/deceptive):
           $$\psi = \frac{\sum_{j \in \Psi_{\text{pos}}} F_{j, \psi}}{\sum_{j \in \Psi_{\text{pos}}} (S_j + O_j + N_j)}$$
       *   If $F_{\text{neg}} > F_{\text{pos}}$: Net Will is negative (destructive/suppressing):
           $$\psi = \frac{\sum_{k \in \Psi_{\text{neg}}} F_{k, \psi}}{\sum_{k \in \Psi_{\text{neg}}} (S_k + O_k + N_k)}$$

*   **Inversion Detection**: $S_{LE} \gg 0$, $S_{GE} \gg 0$, or $S_{BP} \gg 0$ pulls $u < 0$ (Co-optation). $O_{LE} \gg 0$, $O_{GE} \gg 0$, or $O_{BP} \gg 0$ pushes $u > 0$ (Subversion).
*   **Qqci Precision**: Run SON independently per plane to find $(u_j, \psi_j)$ at depth $Q \to q \to c \to i$.

---

## 3. Phase 3 — Source Integrity

**Hypocrisy Gap:**
$$\Delta H = \|\vec{C}_{ideal} - \vec{C}_{action}\|$$
*   $\Delta H < 0.3 \to$ Pass
*   $0.3 \le \Delta H < 0.7 \to$ Conditional
*   $\Delta H \ge 0.7 \to$ Fail

---

## 4. Phase 4 — Forensic Stress Test

*   **Fake Maximiser**: Flag if (capacity $\gg$ effort) AND (stated goal remains unsolved).
*   **Helxis**: Flag if bait beneficiary $\neq$ switch beneficiary.

---

## 5. Output Trajectory (Path Names)

Concatenated as `[Exit] into [Entry]`:
*   **Entry (destinations):** GG = Grace | LE = Deception | LG = Redemption | GE = Destruction.
*   **Exit (origins):** GG = Fall | LE = Revelation | LG = Awakening | GE = Reckoning.
*   *Same-zone = Stasis.*
