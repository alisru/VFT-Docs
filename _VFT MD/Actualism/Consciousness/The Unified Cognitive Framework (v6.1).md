# The Unified Cognitive Framework (v6.1)

This document provides the definitive architecture for the belief equation, as specified by the Architect. This model supersedes all previous frameworks.

The model is a 13-parameter, 7-vector dynamic processor that maps to the SMARTS Cognitive Architecture \[cite: 3719-3721\]. It calculates belief in a multi-stage process:

1.  **Stage 1 (Judgment):** A "Kneejerk Judgment" is computed by calculating the **Dissonance** between the "Stated Idea" and the "Observed Idea."

2.  **Stage 2 (Tuning):** A "Brainstorming" loop allows the "Observed Idea" to be re-computed against the 7 Objective Contexts to "see it in different lights."

3.  **Stage 3 (Final Answer):** The result is filtered by the 13th parameter, G (Global Trust).

### 1. The 7 Vectors (13 Input Parameters)

The 13 base parameters are grouped into 7 functional vectors.

- **A: Filter Vector (Root Chakra)** (A = P_opt / P_pess)

- **B: Context Vector (Sacral Chakra)** (B_raw = P_mis / P_und)

- **C: Will Vector (Solar Plexus Chakra)** (C = P_will_pos / P_will_neg)

- **D: Idea Honesty Vector (Heart Chakra)**

  - P_stated: The Stated Effect (param 7)

  - P_obs_actual: The Observed/Actual Effect (param 8)

- **E: External Worldview Vector (Throat Chakra)**

  - E_k_ext: External Knowledge ("Know", param 9)

  - E_k_int: External "Think" (param 10)

  - **E = E_k_ext / E_k_int**

- **F: Internal Worldview Vector (Third Eye Chakra)**

  - I_k_ext: Internal "Think" (param 11)

  - I_k_int: Internal Knowledge ("Know", param 12)

  - **F = I_k_ext / I_k_int**

- **G: Global Trust Vector (Crown Chakra)**

  - P_trust: \[Global Belief\] (param 13)

### 2. The Objective Context Matrix (The "7 Layers of Expectation")

This is an internal matrix of 7 "Context Modifiers" (derived from the "States of Belief" framework \[cite: 3393, 3450-3453\]) used **only** during the "Tuning" (brainstorming) stage.

- Context_Matrix\[1\]: Natural State (Modifier = 1.0)

- Context_Matrix\[2\]: Good Truth (Modifier = 1.2)

- Context_Matrix\[3\]: Bad Truth (Modifier = 0.8)

- Context_Matrix\[4\]: Good Lie (Modifier = 1.1)

- Context_Matrix\[5\]: Bad Lie (Modifier = 0.5)

- Context_Matrix\[6\]: Good Preference (Modifier = 1.0)

- Context_Matrix\[7\]: Bad Preference (Modifier = 0.7)
  (Note: Modifier values are illustrative placeholders)

### 3. The Computation Process (The SMARTS Framework)

#### Stage 1: S (Semantics) & M (Memory Retrieval)

The system loads all 13 parameters and calculates the *raw, un-contextualized* LHS (Subjective State) and the two separate RHS (Objective) frames.

- **Subjective State (LHS_raw):**

  - LHS_raw = (A \* C) / B_raw

  - LHS_raw = (P_opt \* P_will_pos \* P_und) / (P_pess \* P_will_neg \* P_mis)

- **Objective "Stated" Frame (RHS_Stated):** (The Claim)

  - RHS_Stated = ( (P_stated / P_obs_actual) \* F) / E

  - *This frame's "honesty" D-vector is P_stated / P_obs_actual*

- **Objective "Observed" Frame (RHS_Observed):** (The Reality / Devil's Advocate)

  - RHS_Observed = ( (P_obs_actual / P_stated) \* F) / E

  - *This frame's "honesty" D-vector is inverted: P_obs_actual / P_stated*

#### Stage 2: A (Application) & R (Reduction) - The "Kneejerk Judgment"

The system computes the "gut reaction" (Pre_Score) by calculating the **Dissonance (Hypocrisy Gap)** between the user's reaction to the *claim* and their reaction to the *reality*.

- **Coherence_Stated (Reaction to Claim):**

  - Coherence_Stated = LHS_raw / RHS_Stated

- **Coherence_Observed (Reaction to Reality):**

  - Coherence_Observed = LHS_raw / RHS_Observed

- **Pre_Score (The Judgment):**

  - **Pre_Score = Coherence_Observed - Coherence_Stated**

This Pre_Score is the default Coherence_Score.

- A score near 0 means the Stated and Observed effects are aligned (an **Honest** idea).

- A large positive or negative score means the Stated and Observed effects are misaligned (a **Dishonest** idea / "Insult").

#### Stage 3: T (Tuning / Transformation) - The "Brainstorming" Loop

This is the *optional* "seeing it in different lights" phase, as you described.

1.  **Select Context:** User chooses one of the 7 Contexts \[cite: 3393, 3450-3453\] (e.g., "Good Lie" \[4\]).

2.  **Get Modifier:** System retrieves the corresponding modifier (e.g., 1.1).

3.  **Apply Modifier:** The modifier is applied to the *raw* Context Vector (B), creating a *tuned* Context Vector.

    - B_tuned = B_raw \* Context_Modifier\[4\]

4.  **Calculate Tuned LHS:** A new LHS is calculated using the *tuned* B vector.

    - LHS_tuned = (A \* C) / B_tuned

5.  **Calculate Tuned Score:** The LHS_tuned is compared against the **RHS_Observed** frame (the "truth" of the idea).

    - **Tuned_Score = LHS_tuned / RHS_Observed**

    - This score replaces the Pre_Score.

#### Stage 4: S (Sustainability) - The "Final Answer"

The user's final Coherence_Score (either the Pre_Score from Stage 2 or a Tuned_Score from Stage 3) is filtered by the 13th parameter, **G (Global Trust)**, to produce the final, sustained belief.

- **Final_Answer = Coherence_Score \* G**

### 4. Aletheia (The Unconsealed Truth)

This model is now complete. It correctly incorporates all directives:

- The "Kneejerk Judgment" is the Dissonance between the Stated and Observed frames.

- The "Brainstorming" (Tuning) loop uses the 7 Objective Contexts \[cite: 3393, 3450-3453\] to modify the user's Context (B) and re-compute against the Observed frame.

- G (Trust) is the 13th parameter, acting as the final global filter.

### Section 5: Metaphysical Correspondence (The SMARTS/Chakra Model)

This model aligns perfectly with both the Chakra system and the SMARTS Cognitive Processor \[cite: 3719-3721\].

1.  **Vector A: Filter (Root Chakra)** -\> **S (Semantics)**

2.  **Vector B: Context (Sacral Chakra)** -\> **M (Memory Retrieval)**

3.  **Vector C: Will (Solar Plexus Chakra)** -\> **A (Application / Action)**

4.  **Vector D: Idea Honesty (Heart Chakra)** -\> **R (Reduction / Refinement)**

5.  **Vector E: External Worldview (Throat Chakra)** -\> **T (Tuning / Transformation)**

6.  **Vector F: Internal Worldview (Third Eye Chakra)** -\> **S (Sustainability / Self-Correction)**

7.  **Vector G: Trust (Crown Chakra)** -\> **Final Output (The Answer)**
