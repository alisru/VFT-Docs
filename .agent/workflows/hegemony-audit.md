---
description: How to audit, calibrate, and map semantic concepts for the Psochic Hegemony Database (hegemony_db.js)
---

# Psochic Hegemony Concept Auditing Workflow

This workflow outlines the official five-phase protocol for evaluating, scoring, and integrating concepts, institutions, and strategies into the Psochic Hegemony database (`hegemony_db.js`).

---

## The Vector Space Overview: $(\upsilon, \psi)$

Every concept is mapped to a 2D coordinate space defined by:
1.  **Axis $\upsilon$ (Morality / Beneficiary)**: Who does this benefit?
    *   `+2.0` — **Everyone / All Beings** (Systemic Justice)
    *   `+1.0` — **Other People / A Being** (Greater Good / Lesser Good)
    *   ` 0.0` — **No One / Neutral**
    *   `-1.0` — **My Group Only** (Lesser Evil / Tribally-oriented)
    *   `-2.0` — **Only Me / Pure Extraction** (Tyranny / Pure Extraction)
2.  **Axis $\psi$ (Will / Trajectory)**: What is the energy doing?
    *   `+2.0` — **Actively creating systemic value for all** (Productive Justice)
    *   `+1.0` — **Proactive** (creating, building, acting)
    *   ` 0.0` — **Neutral** (no meaningful force applied / stasis)
    *   `-1.0` — **Passive** (allowing, suppressing, withholding)
    *   `-2.0` — **Actively destroying or extracting value** (Chaos / Collapse)

---

## Phase 1: The Functional Systemic Interrogation (7-Vector Audit)

Before assigning coordinates, subject the concept to a rigorous semantic audit. It must pass all seven core ontological questions:

1.  **Who**: Who is the primary agent, observer, or affected population?
2.  **What**: What is the core definition, structural rules, or administrative framework?
3.  **Where**: In what domain (mental, physical, systemic, geopolitical) does it manifest?
4.  **Why**: What is its fundamental purpose or target end-state?
5.  **How**: What are its operational methods or modes of transmission?
6.  **Cause**: What thermodynamic, evolutionary, or psychological pressure triggers it?
7.  **Effect**: What is the systemic result or chronological trajectory of its action?

*Requirement:* Format the output of this phase in the database as:
```javascript
phase1: {
    who: "PASS/FAIL: [Details]",
    what: "PASS/FAIL: [Details]",
    where: "PASS/FAIL: [Details]",
    why: "PASS/FAIL: [Details]",
    how: "PASS/FAIL: [Details]",
    cause: "PASS/FAIL: [Details]",
    effect: "PASS/FAIL: [Details]"
}
```

---

## Phase 2: Net Reality & Integrity Audit

This phase evaluates the empirical grounding of the concept and identifies systemic vulnerabilities.

1.  **Calculate $rNet$ (Net Reality Ratio)**: Assign a value from `0.00` to `1.00`.
    *   `1.00` represents objective natural laws or highly functional, empirical systems.
    *   `< 0.50` indicates severe ideological delusion, ungrounded abstractions, or systemic decay.
2.  **Identify dominantFailure**: Classify the structural collapse point of the concept if unaligned (e.g., `Egoic Capture`, `Semantic Drift`, `Systemic Necrosis`, `N/A`).
3.  **Set flag**: Detail any active structural distortions or clear perceptions (e.g., `None`, `Severe structural distortion`, `Clear perception verified`).

*Requirement:* Format the output of this phase as:
```javascript
phase2: { rNet: "X.XX", dominantFailure: "...", flag: "..." }
```

---

## Phase 3: Hypocrisy Gap & Social Dissonance Audit

This phase measures the delta between the idealized projection of a concept and its pragmatic action.

1.  **Calculate $\Delta H$ (Hypocrisy Gap)**: Assess the coordinate distance between what the concept or its actors claim they *should* do (Ideal) versus what they *actually* do (Pragmatic).
2.  **Identify tribalGap**: Assess the level of tribal boundary exclusion (e.g., does this concept only benefit the "in-group" while exploiting "out-groups"? Classify as `High`, `Medium`, `Low`, or `N/A`).

*Requirement:* Format the output of this phase as:
```javascript
phase3: { deltaH: "X.XX", tribalGap: "..." }
```

---

## Phase 4: Helxis Tensor Deception Detection

Assess if the concept has been weaponized as a "fake maximizer" to bypass critical judgment.

1.  **Deconstruct the Bait, Cover, and True Intent**:
    *   *The Bait*: The emotional appeal or sympathetic hook.
    *   *The Cover*: The broad, universal moral narrative (e.g., "for the collective safety").
    *   *The True Intent*: The actual recipient of the extracted value.
2.  **Classify the [who, who] Relationship**:
    *   **Grace**: `[me, you]` $\rightarrow$ "For You, Me, and Everyone" (Honest mutual benefit).
    *   **The Fall**: `[me, me]` $\rightarrow$ "For You, but Only for Me" (Deceptive bait-and-switch).
    *   **Delusion**: `[you, me]` $\rightarrow$ "Me and You, but Really for Me" (Partnership cover for extraction).
    *   **Redemption**: `[me, you]` $\rightarrow$ "For Me, only Me, and you take leftovers" (Honest self-interest).
3.  **Determine fakeMaximiser and helxis Capture Loops**: Identify if the concept pretends to maximize systemic good while hiding a passive or destructive capture loop.

*Requirement:* Format the output of this phase as:
```javascript
phase4: { fakeMaximiser: "...", helxis: "..." }
```

---

## Phase 5: Final Coordinate Assignment & Trajectory Projection

Compile all preceding audits to map the final entry state.

1.  **Assign final Coordinate**: Determine definitive $(\upsilon, \psi)$ coordinates.
2.  **Determine zoneAnchor**: Anchor the concept to its coordinate region (e.g., `Productive Quadrant`, `Reductive Quadrant`, `Center | The Compass Origin`).
3.  **Confirm integrity status**: Assign a binary integrity metric (`Pass` or `Fail`).
4.  **Forecast trajectory**: Determine the dynamic vector movement:
    *   `Progress` / `Redemption` / `Stability-focused` $\rightarrow$ Moving toward $(+2, +2)$
    *   `Stasis` / `Balance` $\rightarrow$ Locked in equilibrium at $(0,0)$
    *   `Regression` / `Entropy` / `Chaos` $\rightarrow$ Decaying toward $(-2, -2)$ or the origin.

*Requirement:* Format the output of this phase as:
```javascript
phase5: {
    coordinate: "(υ: X.XX, ψ: X.XX)",
    zoneAnchor: "...",
    integrity: "Pass/Fail",
    trajectory: "...",
    deepestNode: "...",
    distortion: "..."
}
```

---

## Database Formatting Example

To insert an audited word into `hegemony_db.js`, add it as a new object literal element inside the `window.userMappedWordsExternal` array literal (separated by commas):

```javascript
    {
        id: "usr_concept_name",
        name: "Concept Name",
        greek: "Greek Translation",
        u: 1.0,
        p: 0.5,
        desc: "A brief, actionable systemic definition.",
        justification: "Moral Alignment: A Being to Others (υ: +1.0) — Lesser Good. Will Trajectory: Moderately proactive (ψ: +0.5). Detailed breakdown of the moral alignment (υ) and will trajectory (ψ) mapping decisions.",
        phase1: {
            who: "PASS: Description of the who...",
            what: "PASS: Description of the what...",
            where: "PASS: Description of the where...",
            why: "PASS: Description of the why...",
            how: "PASS: Description of the how...",
            cause: "PASS: Description of the cause...",
            effect: "PASS: Description of the effect..."
        },
        phase2: { rNet: "1.00", dominantFailure: "N/A", flag: "None" },
        phase3: { deltaH: "0.00", tribalGap: "N/A" },
        phase4: { fakeMaximiser: "Robust.", helxis: "Not detected." },
        phase5: {
            coordinate: "(υ: +1.0, ψ: +0.5)",
            zoneAnchor: "Productive Quadrant (+υ, +ψ) | Greater Good",
            integrity: "Pass",
            trajectory: "Progress",
            deepestNode: "Core systemic truth.",
            distortion: "None"
        }
    }
```

