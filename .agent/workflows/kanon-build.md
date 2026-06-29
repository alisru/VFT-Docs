---
description: How to systematically search, harvest, draft, and compile a 343 National Kanon using the compact JSON architecture.
---

# 343 National Kanon Build Workflow (Compact JSON Edition)

This workflow defines the protocol for generating and compiling a "343 Analysis" (The National Kanon) for any nation. It adapts the core semantic architecture, selection strategies, and analytical rules from `How_To_Generate_National_Kanon_343.md` to use the **compact JSON** format exclusively as the source of truth and destination.

---

## Part I: Semantic Architecture & Narrative Rules
This section defines the "Soul" of the Kanon—the meaning, logic, and writing standards.

### The 7x7x7 Structure
The analysis maps the "Soul of a Nation" by dividing it into 343 distinct vectors:
1. **7 Planes** (The Files): The highest level of division. Each Plane represents one of the 7 Semantic Vectors:
   * **Plane 1 (WHO):** Identity
   * **Plane 2 (WHAT):** Definition
   * **Plane 3 (WHERE):** Land
   * **Plane 4 (WHY):** Drive
   * **Plane 5 (HOW):** Method
   * **Plane 6 (CAUSE):** Foundation
   * **Plane 7 (EFFECT):** Result
2. **7 Senses** (The Sections): Within each Plane, the analysis scans for the 7 constituent vectors *of that Plane* (ordered `q1` to `q7`).
3. **7 Vectors** (The Items): Within each Sense, the analysis identifies 7 specific cultural artifacts, quotes, or historical facts that anchor the concept.

**Total Vectors:** 7 Planes × 7 Senses × 7 Items = **343 Vectors**.

### Geometric Mapping (The 42-Structure Axes)
* **THE DRIVER (Emergent Axis):** `Plane 1 (WHO)` – Will and Direction.
* **LATERAL Axis (+/- x):** `Plane 2 (WHAT)` (+x: Faith/Probability) & `Plane 3 (WHERE)` (-x: Matter/Distance).
* **LONGITUDINAL Axis (+/- y):** `Plane 4 (WHY)` (+y: Meaning/Resonance) & `Plane 5 (HOW)` (-y: Count/Consistency).
* **VERTICAL Axis (+/- z):** `Plane 6 (CAUSE)` (+z: Sequence/Causality) & `Plane 7 (EFFECT)` (-z: Passion/Consequence).

### Deriving the Vector (The Logic)
Formulate the meaning of each coordinate by "triangulating" the 3 coordinates:
`[Vector (Item)]` of the `[Sense (Section)]` of the `[Plane (File)]`.
* *Example for (Who.Where.Why):* What is the *Motivation* (Why) derived from the *Land* (Where) that shapes the *Identity* (Who)?
* *Answer (Australia):* "Populate or Perish" (The drive to fill the empty land to survive).

---

## Part II: Content Selection Strategy (Building the Ideal)
The primary goal is to **construct the Ideology** of the nation—what the nation *strives* to be, regardless of current political or economic capture.

1. **The Heuristic of Age (Priority Rule):**
   * **Foundational Authority:** Always prioritize the *Founders* or *Originators* of the concept (e.g., Washington, Jefferson, Barton, Parkes).
   * **Trajectory:** If the Founder defined it, show how it has endured or evolved.
   * **Fallback:** High-quality historical quotes.
   * **Last Resort:** Documentary/Administrative facts (Only if no "Soul" quote exists).
2. **Iconic Resonance:** The quote should be deeply embedded in national consciousness.
3. **Emotional Voltage:** Select quotes that provoke pride, shame, tears, or chills.
4. **Relevance:** The quote must be purely relevant to the specific geometric node.

---

## Part III: Analytical & Auditing Rules
1. **Evidence-Based:** Every vector must be anchored by a real snippet of reality (a direct quote, a law, a date, an event). No paraphrasing. No inference. No direct quote means the vector is left unaudited.
2. **Audit Verdicts:**
   * **Stated Score:** Derived from the direct quote. HIT if conduct aligns with the vector's coordinates. FAIL if conduct inverts them.
   * **Actuality Score:** Recorded at the end of the Actuality field. If the subject's actual output over time contradicts their stated position, record TENTATIVE FAIL. If actuality aligns, no second verdict is needed.
3. **Style and Formatting Constraints:**
   * Organize output by Plane then sub-section.
   * No summaries, tallies, framing, or poetic language unless requested.
   * No emojis.
   * No em dashes.

---

## Part IV: Technical Execution & Compact JSON Architecture
All data, coordinates, and narratives are stored in 7 compact JSON files: `Plane_1_Identity_compact.json` to `Plane_7_Result_compact.json`. There are **no separate content markdown files or shadow judgment files**.

### 1. File Structure & Schema
Each plane file is a JSON array containing 49 flat objects (plus alternate perspective entries if applicable) conforming to this schema:
```json
{
  "address": "Plane.Sense.Vector",
  "plane": 1,
  "plane_name": "Identity",
  "name": "Concept Name",
  "canonical_quote": "The quote text.",
  "attribution": "Speaker/Author",
  "source": "Document Source, Year",
  "description": "Description: 3-5 lines explaining the context of the audit and quote. (Min 4-5 sentences)",
  "justification": "Justification: 3-5 lines justifying why the quote and conduct result in a HIT or FAIL against the fixed coordinates. (Min 4-5 sentences)",
  "actuality": "Actuality: 3-5 lines about their actual output relative to their capacity over time, whether they had reasonably met the ideal. End with TENTATIVE FAIL if actuality contradicts the stated score. (Min 4-5 sentences)",
  "coordinates": {
    "v": 0.7,
    "psi": 0.4
  },
  "zone": "Greater Good / Good / Lesser Good / Tension Point / Greatest Lie / Constraint",
  "judgment_rationale": "Short explanation of the coordinate scoring."
}
```

### 2. Moral Coordinate Mapping $(\upsilon, \psi)$
Assign the coordinates using the Psochic Hegemony coordinate rules:
* **Axis $\upsilon$ (Morality - Beneficiary):** Who does this benefit?
  * `+2.0` — Everyone / All Beings (Systemic Justice)
  * `+1.0` — Other People (Greater Good)
  * ` 0.0` — Neutral
  * `-1.0` — My Group Only (Lesser Evil)
  * `-2.0` — Only Me (Tyranny / Pure Extraction)
* **Axis $\psi$ (Will - Trajectory):** What is the energy doing?
  * `+2.0` — Actively creating systemic value for all (Productive Justice)
  * `+1.0` — Proactive (creating, building, acting)
  * ` 0.0` — Neutral (stasis)
  * `-1.0` — Passive (allowing, suppressing, withholding)
  * `-2.0` — Actively destroying or extracting value (Chaos / Collapse)

**Zone Classifications:**
* **Greater Good:** $(+\upsilon, +\psi)$
* **Good:** $(+\upsilon)$
* **Lesser Good:** $(+\upsilon, -\psi)$
* **Tension Point:** Mixed vectors or highly controversial.
* **Greatest Lie:** $(-\upsilon, +\psi)$
* **Constraint:** Neutral/Environmental Fact.

### 3. Alternate Perspective Shadowing
For settler-colonial or historically complex nations, the mainstream narrative often contains an ideological blindspot:
* **The Rule:** For any coordinate where a mainstream concept has a corresponding indigenous or marginalized shadow, **add a second, shadowing entry in the JSON file with the same address**.
* Label the shadowing entry with `[First Nations Perspective]` or similar in its name (e.g., `Anteriority [First Nations Perspective]`).
* Provide the alternate quote, alternate coordinates, and alternate judgment rationale.

### 4. Validation (The Compact Audit)
To ensure depth, each Vector Item must meet the density metrics. Run the compact validation script:
```powershell
python verify_compact_kanon.py
```
This script checks:
* **Completeness:** Verify exactly 49 primary coordinates are present (plus shadowing records).
* **Depth:** Enforce a minimum of 4-5 sentences for BOTH the `description` and `justification` and `actuality` fields.
* **Key Verification:** Verify `description`, `justification`, and `actuality` are present and that `establishes` is not used.
* **Coordinates:** `v` and `psi` values must reside strictly within $[-2.0, 2.0]$.
