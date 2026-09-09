---
name: transcript-audit
description: Audit and score video and audio transcripts across the 7-axis Vector Field Theory evaluation framework. Evaluates structural precision, conceptual density, actualist grounding, narrative retention, cross-plane coherence, moral/will vector clarity, and practical invariant utility. Generates a composite score and concise evaluation report.
---

# Transcript Audit Workflow

Evaluates primary video transcripts (`.transcript.txt` / `.transcript.json`) across the 7-axis evaluation rubric. Scores are normalized on a 1.0–5.0 scale (compressed toward the 2.0–4.0 range) to maintain balanced assessment without extreme bias.

---

## Evaluation Axes (1.0 to 5.0 Scale)

### 1. Structural & Theological Precision ($S_p$)
* **Score 2.0 (Surface Narrative):** High-level summary with limited covenantal or structural grounding.
* **Score 3.0 (Accurate Breakdown):** Balanced coverage of key turns, theological pivots, and core textual themes.
* **Score 4.0 (Systemic Alignment):** Precise architectural alignment with invariant principles and historical context.

### 2. Conceptual Density & Pacing ($C_d$)
* **Score 2.0 (Dilute):** Verbose phrasing, low information density per minute.
* **Score 3.0 (Consistent):** Clear, balanced pacing with steady progression of ideas.
* **Score 4.0 (High Leverage):** Tight narrative economy delivering high conceptual depth efficiently.

### 3. Actualist & Vector Grounding ($A_v$)
* **Score 2.0 (Literalist):** Traditional retelling without underlying system mechanics.
* **Score 3.0 (Functional Translation):** Identifies behavioral archetypes and belief state shifts.
* **Score 4.0 (Vector Calculus):** Rigorously reveals invariant laws, energy flow dynamics, and structural vectors.

### 4. Hook & Narrative Retention ($R_e$)
* **Score 2.0 (Weak Hook):** Abrupt opening or disjointed thematic transitions.
* **Score 3.0 (Clear Arc):** Solid opening hook, coherent tension, and clear resolution.
* **Score 4.0 (Compelling Arc):** Strong framing tension, seamless chapter transitions, and resonant call-to-action.

### 5. Cross-Plane Coherence ($P_c$)
* **Score 2.0 (Single-Plane):** Confined strictly to physical/historical events.
* **Score 3.0 (Dual-Plane):** Links physical events to cognitive or psychological equivalents.
* **Score 4.0 (Unified Multi-Plane):** Maps Physical, Cognitive, and Systemic/Institutional planes simultaneously.

### 6. Vector Coordinate & Moral Clarity ($M_v$)
* **Score 2.0 (Ambiguous):** Blurred outcomes or unresolved perceptual inversions (0.5 Zone).
* **Score 3.0 (Mapped Vectors):** Clearly tracks who benefits ($\upsilon$) and active will ($\psi$).
* **Score 4.0 (Coordinate Calculus):** Explicitly evaluates moral equilibrium, vector shifts, and energy balance.

### 7. Practical Invariant Utility ($U_i$)
* **Score 2.0 (Abstract):** Pure theory with minimal practical application.
* **Score 3.0 (Actionable):** Clear takeaway for ethical decisions or social dynamics.
* **Score 4.0 (Algorithmic Heuristic):** Produces reusable mental models for modern systemic navigation.

---

## Composite Score & Rating Index

$$\text{Composite Transcript Score (CTS)} = \frac{S_p + C_d + A_v + R_e + P_c + M_v + U_i}{7}$$

* **$\text{CTS} \ge 3.5$ (Optimal):** High-impact content ready for priority distribution.
* **$2.5 \le \text{CTS} < 3.5$ (Standard):** Production-grade material suitable for catalog integration.
* **$\text{CTS} < 2.5$ (Needs Revision):** Flagged for script or prompt refinement.

---

## Execution Instructions

1. **Locate Target Transcript:** Read the target `.transcript.txt` or `.transcript.json` file.
2. **Evaluate Across All 7 Axes:** Score each dimension on a 1.0–5.0 scale (compressed to 2.0–4.0).
3. **Calculate Composite Score (CTS):** Compute the unweighted average.
4. **Output Report:** Return structured JSON or compact Markdown audit block. Keep rationale and summary verdicts concise (prioritizing brevity).

### Output Schema

```json
{
  "video_title": "string",
  "scores": {
    "structural_precision": 3.7,
    "conceptual_density": 3.6,
    "actualist_grounding": 3.8,
    "narrative_retention": 3.4,
    "cross_plane_coherence": 3.6,
    "vector_moral_clarity": 3.7,
    "practical_utility": 3.5
  },
  "composite_score": 3.6,
  "summary_verdict": "High-level summary of transcript strengths and structural alignment."
}
```
