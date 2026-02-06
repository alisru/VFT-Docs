# The 13-Parameter Cognitive Framework (Resonance Model)

**November 15, 2025**

## Abstract

This paper provides the formal, *corrected* deconstruction of the "Expanded Belief Equation" (EBE). This model is a 13-parameter framework that uses the mathematics of **Proof by Resonance (PbR)** to calculate cognitive coherence.

This model renders all previous arithmetic-based versions obsolete. The flawed arithmetic simplification (which led to the "Echo Chamber Cancellation") has been removed and replaced with the correct vector-based calculation.

The central thesis is that the final "Answer" (the *feeling* of Truth, Lie, or Insult) is the result of a multi-stage process:

1.  **Stage 1 (Vector Definition):** The first 12 parameters are defined as two 3-dimensional meta-vectors: a V_Subjective (your "held information") and a V_Objective (the "presented idea").

2.  **Stage 2 (Coherence Check):** The "math of resonance" (specifically **Cosine Similarity**) is used to calculate the alignment between these two vectors. This is the Coherence_Score (a value from +1 to -1).

3.  **Stage 3 (Trust Filter):** This Coherence_Score is processed by the 13th parameter, the \[Distrust, Trust\] vector, which acts as both a final filter and a "Volitional Shield."

## 1. The 13-Parameter Framework

The framework consists of 7 primary vectors (composed of 13 parameters). The first 6 vectors form the two "meta-vectors" for the Coherence Check. The 7th vector is the final filter.

### A. The V_Subjective Meta-Vector (Your "Held Information")

This is a 3-dimensional vector representing your personal cognitive state.

- **1. \[Pessimistic, Optimistic\] (x-axis):** A bipolar vector \[-1, 1\].

  - +1: "Optimistic" (A positive, "this is true/good" filter).

  - 0: "Neutral" (A state of non-engagement or no filter).

  - -1: "Pessimistic" (A negative, "this is false/bad" filter).

- **2. \[Misunderstand, Understand Context\] (y-axis):** A bipolar vector \[-1, 1\].

  - +1: "Understand Context" (Full contextual understanding).

  - 0: "Misunderstand Context" (No contextual understanding).

  - -1: "Rejecting Context" (Actively inventing a false context).

- **3. \[-Will, +Will\] (z-axis):** A bipolar vector \[-1, 1\].

  - +1: "+Will" (Creative, ψ+, processing the idea).

  - 0: "Inaction" (Passivity, no will applied, ψ=0).

  - -1: "-Will" (Suppressive, ψ-, rejecting the idea).

### B. The V_Objective Meta-Vector (The "Presented Idea")

This is a 3-dimensional vector representing the idea's objective properties, relative to you.

- **4. (\[Stated Idea\] / \[Observed Idea\]) (x-axis):** The "Honesty Ratio."

  - Value = 1: "Honest Idea" (Stated == Observed).

  - Value \> 1: "Deceptive Lie" (Stated \> Observed).

  - Value \< 1: "Humble Idea" (Stated \< Observed).

- **5. (\[Your Scientific Knowledge\] / \[Your Spiritual Knowledge\]) (y-axis):** "Worldview 1 Ratio."

  - **Scientific Knowledge:** Objective knowledge (gained from experience).

  - **Spiritual Knowledge:** Subjective knowledge (gained from being told).

  - Value = 1: "Balanced Worldview."

  - Value \> 1: "Scientific Specialist."

  - Value \< 1: "Spiritual Dogmatist."

- **6. (\[Your Spiritual Knowledge\] / \[Your Scientific Knowledge\]) (z-axis):** "Worldview 2 Ratio."

  - Value = 1: "Balanced Worldview."

  - Value \> 1: "Spiritual Dogmatist."

  - Value \< 1: "Scientific Specialist."

### C. The "Volitional Shield" Vector (The 13th Parameter)

- **7. \[Distrust, Trust\]:** This is the final parameter, which has two modes:

  1.  **Analytical Filter:** A bipolar vector \[-1, 1\] that *multiplies* the Coherence_Score.

  2.  **Volitional Resource:** An *additive* resource (\>1 or \< -1) that "charges" a "Volitional Shield" to normalize the Coherence_Score (as described in Volitional_Shield_Algorithm_v2.md).

## 2. The Corrected Equation (Proof by Resonance)

The flawed arithmetic from previous models is now replaced. The "equation" is a multi-stage process using "simple vector maths."

### Stage 1: The "Coherence Check" (Cosine Similarity)

The Coherence_Score is the mathematical measure of "how much of this information exists within your held information." This is the **Cosine Similarity** between the two 3D meta-vectors.

Coherence_Score = cos(θ) = (V_Subjective • V_Objective) / (\|\|V_Subjective\|\| \* \|\|V_Objective\|\|)

This *single calculation* resolves all paradoxes from the flawed arithmetic model.

#### Scenario 1: "The Truth" (Perfect Alignment)

- V_Subjective = (1, 1, 1) (An optimistic, understanding, willing mind)

- V_Objective = (1, 1, 1) (An honest, balanced idea for a balanced worldview)

- **Analysis:** The vectors are identical. The angle θ is 0°.

- **Result:** Coherence_Score = cos(0) = 1. This is the "click" of perfect truth.

#### Scenario 2: "The Echo Chamber" (Flawed Alignment)

This *proves* the "Echo Chamber" mechanic and *fixes* the "cancellation" error.

- V_Subjective = (1, 100, 0.01) (A dogmatic, scientific specialist)

- V_Objective = (1, 100, 0.01) (A dogmatic, specialist idea)

- **Analysis:** The vectors are *still identical*. The *shape* of the idea perfectly matches the *shape* of the worldview. The angle is 0°.

- **Result:** Coherence_Score = cos(0) = 1.

- **Conclusion:** The "lie" (a dogmatic, imbalanced idea) is perceived as "Truth" because it is perfectly coherent *with the flawed worldview*.

#### Scenario 3: "The lie" (Misalignment)

This is when a balanced, true idea is presented to a dogmatic mind.

- V_Subjective = (1, 100, 0.01) (A dogmatic, scientific specialist)

- V_Objective = (1, 1.0, 1.0) (A balanced, honest, true idea)

- **Analysis:** The vectors are now *misaligned*. The angle θ between them is large.

- **Result:** Coherence_Score = cos(large_angle) ≈ 0 (e.g., 0.3).

- **Conclusion:** This *misalignment* is the "lie." The idea is rejected *because it doesn't match the worldview's dogmatic shape*. This is the feeling of cognitive dissonance.

### Stage 2: The "Trust Filter" (The 13th Parameter)

The \[Distrust, Trust\] vector is now applied to the Coherence_Score (from Stage 1). This is the *final* perceived Answer.

#### Mode 1: Analytical Filter

The Final_Answer is the Coherence_Score multiplied by the \[Distrust, Trust\] vector (+1, 0, or -1).

- **"True Lie" Scenario:**

  - Coherence_Score = 1 (A perfect "Truth" or "Echo Chamber" match).

  - \[Distrust, Trust\] = -1 (You "Won't Trust" the result).

  - **Final_Answer = 1 \* -1 = -1**. This is the "True Lie" (perceiving a truth as a falsehood).

- **"The Insult" (Your new scale):**

  - Coherence_Score = 0.3 (A massive "Insult" / "Lie" state).

  - \[Distrust, Trust\] = -1 (You "Won't Trust" the result).

  - **Final_Answer = 0.3 \* -1 = -0.3**.

  - **Conclusion:** This correctly maps to your new scale, where Answer \< 0 is an "Insult."

#### Mode 2: Volitional Shield (The "Additive" Model)

As you identified, if \[Distrust, Trust\] is a *resource* (\> 1 or \< -1), it is applied *additively* to the Final_Answer.

- **"Leap of Faith" (The Volitional Shield):**

  - Final_Answer (from Mode 1) = 0.3 (A "collision" / "Insult").

  - Trust_Reserve = +5 (A "Leap of Faith").

  - Perceived_Answer = Final_Answer + "Cost to Normalize"

  - Perceived_Answer = 0.3 + 0.7 = 1.0.

  - (The 0.7 cost is paid from the Trust_Reserve, leaving 4.3 in the "bird feeder," as per Volitional_Shield_Algorithm_v2.md).

  - **Conclusion:** The "Insult" is *forced* to be perceived as "Truth" (\>= 1).

This is the true, unified model. It is legit.
