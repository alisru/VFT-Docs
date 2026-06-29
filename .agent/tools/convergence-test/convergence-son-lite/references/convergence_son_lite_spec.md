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

Scoring: **PASS** (magnitude 0.1–1.0), **BLANK** (null), or **FAIL** (0.0 / Phantom fill). Contrastive scoring: V_pass = coherence of selected fill / highest alternative.

---

## 2. Phase 2 — Vector Verification (SON Method)

Coordinates calculated as the equilibrium point of attractor forces:

### Grounding Definition: (p·t + n)
*   **Good**: Δ(p·t + n) > 0 (passive expansion/potential shifts to better futures).
*   **Bad**: Δ(p·t + n) < 0 (passive decay/neglect).
*   **Evil**: Δ(p·t + n) < 0 (active contraction/premature closure of futures).
*   **Saintly**: Δ(p·t + n) > 0 (active hold/expansion against closure forces).

*   **Greater Good (A_GG)** = (+1.0, +1.0) | A_GG_perp = (-1.0, +1.0)
*   **Greater Evil (A_GE)** = (-1.0, -1.0) | A_GE_perp = (+1.0, -1.0)
*   **Lesser Good (A_LG)** = (+1.0, -1.0) | A_LG_perp = (+1.0, +1.0)
*   **Lesser Evil (A_LE)** = (-1.0, +1.0) | A_LE_perp = (-1.0, -1.0)
*   **Good Preference (A_GP)** = (+1.0, 0.0) | Oppose (O_GP) drives Will negative (ψ → -1), Neutral (N) has 0.0 force.
*   **Bad Preference (A_BP)** = (-1.0, 0.0) | Oppose (O_BP) drives Will positive (ψ → +1), Neutral (N) has 0.0 force.

For each attractor i, score [0.0, 2.0] based on evidence:
*   **Support (S_i)**: Attraction.
*   **Oppose (O_i)**: Repulsion.
*   **Neutral (N_i)**: Orbit (for moral attractors) or Dilution (for preferences).

Scoring: 0.0 = No force | 1.0 = Condition Met (Human Horizon) | 2.0 = Totality of Exceedence (Systemic Horizon / Double gravity weight).

### Formulas (18-Variable Parameter Space)
To maintain structural resolution and prevent coordinate collapse, **every single one of the 6 attractors MUST have its full [S_i, O_i, N_i] triple scored** (18 variables in total). Scoring only a single dominant aspect per point is a methodological error.

1. **Net Attractor Force (F_i):**
   * For Moral Attractors (GG, GE, LG, LE):
     F_i = S_i * A_i - O_i * A_i + N_i * A_i_perp
   * For Good Preference (GP):
     F_GP = S_GP * (1.0, 0.0) - O_GP * (1.0, 1.0)
   * For Bad Preference (BP):
     F_BP = S_BP * (-1.0, 0.0) - O_BP * (-1.0, -1.0)

2. **Morality Coordinate (u):**
   Sum and normalize the u-components of the forces across all 6 attractors:
   u = sum(F_i_u) / sum(S_i + O_i + N_i)

3. **Will Coordinate (ψ) — Separated Will (Like-Type) Protocol:**
   To prevent positive narrative spin (S_LE) and actual physical destruction (S_GE) from cancelling each other out to a neutral stasis (ψ ≈ 0), calculate positive and negative Will forces independently:
   *   Group forces by Will sign:
       *   Ψ_pos = {i | F_i_ψ > 0}
       *   Ψ_neg = {i | F_i_ψ < 0}
   *   Sum absolute force magnitudes for each direction:
       *   F_pos = sum(|F_j_ψ|) for j in Ψ_pos
       *   F_neg = sum(|F_k_ψ|) for k in Ψ_neg
   *   Identify the dominant direction and calculate ψ using ONLY that dominant group:
       *   If F_pos >= F_neg: Net Will is positive (constructive/deceptive):
           ψ = sum(F_j_ψ) / sum(S_j + O_j + N_j) for j in Ψ_pos
       *   If F_neg > F_pos: Net Will is negative (destructive/suppressing):
           ψ = sum(F_k_ψ) / sum(S_k + O_k + N_k) for k in Ψ_neg

*   **Inversion Detection**: S_LE >> 0, S_GE >> 0, or S_BP >> 0 pulls u < 0 (Co-optation). O_LE >> 0, O_GE >> 0, or O_BP >> 0 pushes u > 0 (Subversion).
*   **Ambiguity (z)**: sum of B counts (max 49). **z-profile**: [B_Q1...B_Q7].
*   **V_Qn**: sum(P_magnitudes) / (sum(P_magnitudes) + n_F). (If P + F = 0, V_Qn = 1.0).
*   **R_net**: 1 / (V_Q1 * ... * V_Q7). 7-Tier Scale: 1.0=Absolute Truth, 1.0-1.5=Trustworthy, 1.5-2.0=Conditionally Sound, 2.0-5.0=Partially Distorted, 5.0-10.0=Meaningful Distortion, 10.0-100.0=Severe Deception, >100.0=Baseless Lies.
*   **Object State Blanking**: If inanimate, set Q1, Q4, Q5, Q7 = B. Q3, Q6, Q2 = P/F. (z = 28, z-profile = [7, 0, 0, 7, 7, 0, 7]).
*   **Qqci Precision**: Run SON per plane to find (u_j, ψ_j) at depth Q (Location) → q (Sense) → c (Use) → +i (Recursion). Addressing notation: Q1q5c4 (c4 of q5 of Q1).

---

## 3. Phase 3 — Source Integrity

**Hypocrisy Gap:**
ΔH = ||C_ideal - C_action||
*   ΔH < 0.3 → Pass
*   0.3 ≤ ΔH < 0.7 → Conditional
*   ΔH ≥ 0.7 → Fail

---

## 4. Phase 4 — Forensic Stress Test

*   **Fake Maximiser**: Flag if (capacity >> effort) AND (stated goal remains unsolved).
*   **Helxis**: Flag if bait beneficiary ≠ switch beneficiary.

---

## 5. Output Trajectory (Path Names)

Concatenated as `[Exit] into [Entry]`:
*   **Entry (destinations):** GG = Grace | LE = Deception | LG = Redemption | GE = Destruction.
*   **Exit (origins):** GG = Fall | LE = Revelation | LG = Awakening | GE = Reckoning.
*   *Same-zone = Stasis.*

---

## 6. Core Laws of Social Physics

### The 4 Foundational Axes
*   **Law 1 (Power vs. Empowerment)**: Anti-social (-υ) deception to hoard finite power vs. Social (+υ) empathy to empower others to find their own strength.
*   **Law 2 (Justification vs. Transparency)**: Anti-social (-υ) post-hoc pretexts (actions first, then justifications) vs. Social (+υ) upfront transparency (intentions first, aligned actions).
*   **Law 3 (Projection vs. Empathy)**: Anti-social (-υ) projection of corrupt motives onto opponents vs. Social (+υ) active empathy to understand motives and defuse division.
*   **Law 4 (Problems vs. Solutions)**: Anti-social (-υ) maintaining conflict/authority (invents problems if none exist) vs. Social (+υ) resolving strain to reach stable equilibrium.

### The 2 Modes (Forces)
*   **Possigravity (Positivity)**: Gravity pulling potential toward defined, stable, low-strain configurations.
*   **Perceptual Inversion (Negativity)**: Inverting possibility space (presents solutions as "insurmountable mountains" to maintain conflict).

### The 1 Process (Logic)
*   **Logic**: Causal rules reducing strain.
*   **Morality**: Resultant system state. **Good/Moral** = low-strain, logically efficient path; **Evil/Immoral** = high-strain, unstable configuration ignoring logical efficiency for pretexts.

### Actor Loops
*   **Smart Selfish Loop**: Secret Goal (Selfishness) → Pretext (Justification) → Scapegoat/Distraction (Projection).
*   **Smart Altruistic Loop**: Shared Goal (Altruism) → Coalition (Transparency) → Integration/Buy-in (Empathy).
