---
name: hegemony_audit_workflow
description: Audit, calibrate, and map semantic concepts for the Psochic Hegemony Database (hegemony_db.js) using the 49-point fractal matrix and unstringified JS object format.
---

# Psochic Hegemony Concept Auditing Workflow (49-Point Matrix)

This workflow outlines the official five-phase protocol for evaluating, scoring, and integrating concepts, institutions, and strategies into the Psochic Hegemony database (`hegemony_db.js`).

## Critical Formatting & Data Type Constraints

When generating a database entry, you MUST output a raw, unstringified JavaScript object literal. It must perfectly match the schema of the `window.userMappedWordsExternal` array.

- **Numeric Floats:** The `u` and `p` axes values MUST be numbers (e.g., `1.0`, `-1.5`), not strings.
- **Strings:** The `rNet` and `deltaH` values MUST be formatted as strings with two decimal places (e.g., `"1.00"`, `"-0.50"`).
- **Keys:** Keys must be unquoted (e.g., `id:`, `name:`, `justification:`).

---

## The Vector Space Overview: $(\upsilon, \psi)$

Every concept is mapped to a 2D coordinate space defined by:

1. **Axis $\upsilon$ (Morality / Beneficiary):** Who does this benefit?
   * `+2.0` — **Everyone / All Beings** (Systemic Justice)
   * `+1.0` — **Other People / A Being** (Greater Good / Lesser Good)
   * ` 0.0` — **No One / Neutral**
   * `-1.0` — **My Group Only** (Lesser Evil / Tribally-oriented)
   * `-2.0` — **Only Me / Pure Extraction** (Tyranny / Pure Extraction)

2. **Axis $\psi$ (Will / Trajectory):** What is the energy doing?
   * `+2.0` — **Highly Active** (Actively creating systemic value)
   * `+1.0` — **Active** (Proactive, creating, building, acting)
   * ` 0.0` — **Stasis** (Neutral, no meaningful force applied)
   * `-1.0` — **Passive** (Allowing, suppressing, withholding)
   * `-2.0` — **Highly Passive** (Actively destroying or extracting value)

* **WHERE modifies $\upsilon$:** Energy injected into a structurally corrupt or decaying domain has its $\upsilon$ pulled toward negative regardless of stated intent.
* **HOW modifies $\psi$:** Coercive or deceptive HOW forces $\psi$ negative regardless of stated WHY. The will axis is bounded by method, not purpose.

---

## Phase 1: The Functional Systemic Interrogation (49-Point Fractal Matrix)

Before assigning coordinates, subject the concept to a rigorous semantic audit across the 7 primary vectors. For each sub-interrogative, track:

- **P (PASS, magnitude 0.0–1.0):** the sub-interrogative is filled; the score is the coherence of the selected fill relative to the best available fill in the field. `1.0` = optimal selection. Fractional = real but suboptimal. `0.0` = phantom fill (appears populated, possesses nothing) — treat as FAIL.
- **F (FAIL, = 0.0):** contradicts observable reality or breaks a structural connection.
- **B (BLANK, = null):** genuinely unpopulated — an open vessel awaiting context, not an error. Contributes to $z$ only.

The total count for each line MUST equal 7 ($n_P + n_F + n_B = 7$). Passes are not equal weight — record fractional magnitudes explicitly.

The contrastive field (what alternatives were available at each plane) is the internal mechanism producing the magnitude. It never appears in the output — the number carries it.

Do not provide superficial answers; you must unpack the full systemic meta-context for each vector in a single line, taking into account the counts and magnitudes you established.

- **Q1 WHO (Filter Vector / Meta-Physical):** Assess Intent, Sovereignty vs Tyranny. Who is the primary operator wielding the concept? Who is the intended beneficiary? [Touch on the who, what, where, why, how, cause, and effect of the actors involved].
- **Q2 WHAT (Definition Vector / Possible):** Assess Necessity, Verification vs Novelty. What is the precise structural mechanism and value payload? [Touch on the who, what, where, why, how, cause, and effect of the payload itself].
- **Q3 WHERE (Locus Vector / Physical):** Assess Boundaries, Understanding vs Misunderstanding. Where are the actual boundaries and environmental rules of this operational domain? [Touch on the who, what, where, why, how, cause, and effect of the domain].
- **Q4 WHY (Drive Vector / Lyrical):** Assess Resonance, Truth-Telling vs Delusion. Why is this absolute, unavoidable terminal end-state (telos) systemically required? [Touch on the who, what, where, why, how, cause, and effect of the purpose].
- **Q5 HOW (Method Vector / Logical):** Assess Consistency, Wisdom vs Sophistry. How are the precise rules of engagement and coercive/cooperative forces executed? [Touch on the who, what, where, why, how, cause, and effect of the methods].
- **Q6 CAUSE (Origin Vector / Historical):** Assess Causality, Redemption vs Revisionism. What is the root cause beneath the immediate trigger that initiated the foundational catalyst? [Touch on the who, what, where, why, how, cause, and effect of the pressure point].
- **Q7 EFFECT (Impact Vector / Emotive):** Assess Impact, Love/Unity vs Parasitism. What is the absolute systemic result plotted on an infinite timeline? [Touch on the who, what, where, why, how, cause, and effect of the consequences].

**Phantom fills:** After scoring all 7 planes, identify any sub-interrogative that appears populated but whose generator $z$ is high at that plane — a fill offered by a source that does not structurally possess it. Phantom fills score `0.0` and are treated as FAILs. List phantom fills detected at the end of Phase 1.

*Requirement:* Format the output of this phase in the database explicitly tracking the $[P, F, B]$ counts with magnitudes on $P$:
```javascript
phase1: {
    who: "[P: X×mag, F: Y, B: Z] [Detailed contextual breakdown covering the 7 sub-points...]",
    what: "[P: X×mag, F: Y, B: Z] [Detailed contextual breakdown covering the 7 sub-points...]",
    where: "[P: X×mag, F: Y, B: Z] [Detailed contextual breakdown covering the 7 sub-points...]",
    why: "[P: X×mag, F: Y, B: Z] [Detailed contextual breakdown covering the 7 sub-points...]",
    how: "[P: X×mag, F: Y, B: Z] [Detailed contextual breakdown covering the 7 sub-points...]",
    cause: "[P: X×mag, F: Y, B: Z] [Detailed contextual breakdown covering the 7 sub-points...]",
    effect: "[P: X×mag, F: Y, B: Z] [Detailed contextual breakdown covering the 7 sub-points...]"
}
```

---

## Phase 2: Net Reality & Vector Magnitude Audit

This phase derives the mathematical strength of the concept using the counts and magnitudes from Phase 1.

1. **Calculate $rNet$ (Net Reality Ratio):** For each plane, derive $V_{Qn}$ using fractional pass magnitudes:
   $$V_{Qn} = \frac{\sum P_{\text{magnitudes}}}{\sum P_{\text{magnitudes}} + n_F}$$
   If $P + F = 0$: $V_{Qn} = 1.0$ (perfect coherence as pure potential — blanks do not damage coherence).
   Phantom fills score 0.0 and are included in $n_F$.
   $$R_{\text{net}} = 1 \div (V_{Q1} \times V_{Q2} \times V_{Q3} \times V_{Q4} \times V_{Q5} \times V_{Q6} \times V_{Q7})$$
   Ideal = `1.0`. Output as a STRING.

2. **Calculate $z$ (Ambiguity Volume):** $z$ = sum of all $B$ counts across all 7 planes (max 49). Also record $z\text{-profile} = [B_{Q1}, B_{Q2}, B_{Q3}, B_{Q4}, B_{Q5}, B_{Q6}, B_{Q7}]$ — the distribution fingerprint.
3. **Calculate variance fields:** Baseline $n_\upsilon$ and $n_\psi$ derived from locked (P/F) vectors only. Blanks generate swing ranges $?\upsilon$ and $?\psi$. Full coordinate expression: $[n_\upsilon \pm ?\upsilon, n_\psi \pm ?\psi, z]$.
4. **Identify dominantFailure:** Classify the structural collapse point if unaligned (e.g., `Egoic Capture`, `Semantic Drift`, `Systemic Necrosis`, `Phantom Fill`, `N/A`).
5. **Set flag:** Detail any active structural distortions, perceptual inversions, or object state blanking applied.

*Requirement:* Format the output of this phase as:
```javascript
phase2: { rNet: "X.XX", dominantFailure: "...", flag: "..." }
```

---

## Phase 3: Hypocrisy Gap & Social Dissonance Audit

This phase measures the delta between the objective ideal and the pragmatic action.

The objective ideal is the highest-coherence fill available at each plane relative to the full field of alternatives — not the stated intent. For each Q plane: given everything available to this actor at this time, what was the best possible selection? $\Delta H$ is calculated against that optimal coordinate, not the marketing.

1. **Calculate $\Delta H$ (Hypocrisy Gap):** Coordinate distance between $\text{Vector}_{\text{Ideal}}$ (built from optimal plane fills) and $\text{Vector}_{\text{Action}}$ (what the concept actually does). Output as a STRING.
2. **Identify tribalGap:** Assess the level of tribal boundary exclusion (e.g., `High`, `Medium`, `Low`, or `N/A`).

*Requirement:* Format the output of this phase as:
```javascript
phase3: { deltaH: "X.XX", tribalGap: "..." }
```

---

## Phase 4: Forensic Stress Test & Helxis Tensor

Assess if the concept has been weaponized as a "fake maximizer" to bypass critical judgment.

1. **Determine fakeMaximiser:** Identify if the concept pretends to maximize systemic good while hiding extraction (e.g., `Yes`, `No`, `Partial: [note]`).
2. **Determine helxis:** Identify deceptive capture loops (e.g., `Detected: [bait -> switch]`, `Not detected.`).

*Requirement:* Format the output of this phase as:
```javascript
phase4: { fakeMaximiser: "...", helxis: "..." }
```

---

## Phase 5: Final Coordinate Assignment & Trajectory Projection

Compile all preceding audits to map the final entry state. The $z$ axis value is determined by summing all the $B$ (BLANK) counts from Phase 1.

1. **Assign final Coordinate:** Determine definitive $(\upsilon, \psi, z)$ coordinates using baseline values with variance fields applied. Output format: `"(υ: +X.X ± ?υ, ψ: +Y.Y ± ?ψ, z: Z)"`. For the database `u` and `p` fields, use the baseline $n_\upsilon$ and $n_\psi$ values.
2. **Determine zoneAnchor:** Anchor the concept to its coordinate region.
3. **Confirm integrity status:** Assign a binary metric (`Pass` or `Fail`).
4. **Forecast trajectory:** Determine the dynamic vector movement (e.g., `Progress`, `Stasis`, `Entropy`).
5. **Identify deepestNode:** Address the deepest structural node impacted.
6. **Identify distortion:** Address any systemic distortion (`None` if clear).
7. **State conditional convergence if applicable:** `"Converges IF [blank vector address] = [specific context fill]."`

*Requirement:* Format the output of this phase as:
```javascript
phase5: {
    coordinate: "(υ: X.XX, ψ: Y.YY, z: ZZ)",
    zoneAnchor: "...",
    integrity: "Pass/Fail",
    trajectory: "...",
    deepestNode: "...",
    distortion: "..."
}
```

---

## Golden Standard Database Formatting Template

To insert an audited word into `hegemony_db.js`, it MUST strictly follow this blueprint without any inline comments. Properties `id`, `name`, `greek`, `u`, and `p` MUST sit on the first line.

**Crucial Format Rule:** Do NOT use the bloated multi-line `desc` format found in older parts of the database. Keep `desc` strictly as the definition. The `justification` MUST explicitly explain the mechanics behind the coordinates.

```javascript
{ id: "usr_concept_name", name: "Concept Name", greek: "Greek Translation", u: 1.0, p: 0.5,
  desc: "A brief, actionable systemic definition.",
  justification: "Explicitly explain the reasoning behind the coordinates. State exactly why the beneficiary (υ) leans toward self or others, and why the energy (ψ) is active, passive, or neutral. Note WHERE and HOW modifier effects if applicable. Do not just restate the numeric labels.",
  phase1: {
      who: "[P: 7×1.0, F: 0, B: 0] [Context covering all sub-interrogatives...]",
      what: "[P: 5×0.8, F: 0, B: 2] [Context covering all sub-interrogatives...]",
      where: "[P: 7×1.0, F: 0, B: 0] [Context covering all sub-interrogatives...]",
      why: "[P: 1×0.4, F: 1, B: 5] [Context covering all sub-interrogatives...]",
      how: "[P: 2×0.6, F: 0, B: 5] [Context covering all sub-interrogatives...]",
      cause: "[P: 7×1.0, F: 0, B: 0] [Context covering all sub-interrogatives...]",
      effect: "[P: 0, F: 0, B: 7] [Context covering all sub-interrogatives...]"
  },
  phase2: { rNet: "1.00", dominantFailure: "N/A", flag: "None" },
  phase3: { deltaH: "0.00", tribalGap: "N/A" },
  phase4: { fakeMaximiser: "Robust.", helxis: "Not detected." },
  phase5: {
      coordinate: "(υ: +1.0, ψ: +0.5, z: 19)",
      zoneAnchor: "Productive Quadrant (+υ, +ψ) | Greater Good",
      integrity: "Conditional",
      trajectory: "Context-Dependent",
      deepestNode: "Core systemic truth.",
      distortion: "None"
  }
}
```
<!-- Generated by memories.sh at 2026-09-24T15:15:23.584Z -->