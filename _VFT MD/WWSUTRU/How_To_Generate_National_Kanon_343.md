# Protocol: Generating a 343 National Kanon Analysis

## Part I: Semantic Architecture & Narrative Rules
This section defines the "Soul" of the Kanon—the meaning, logic, and writing standards.

This document outlines the precise format and methodology for generating a "343 Analysis" (The National Kanon) for any nation. The analysis is a recursive 7x7x7 structure derived from Vector Field Theory (VFT).

## The 7x7x7 Structure

The analysis serves to map the "Soul of a Nation" by dividing it into 343 distinct vectors.

1.  **7 Planes** (The Files): The highest level of division. Each Plane represents one of the 7 Semantic Vectors (Who, What, Where, Why, How, Cause, Effect).
2.  **7 Senses** (The Sections): Within each Plane, the analysis scans for the 7 constituent vectors *of that Plane*.
3.  **7 Vectors** (The Items): Within each Sense, the analysis identifies 7 specific cultural artifacts, quotes, or historical facts that anchor the concept.

**Total Vectors:** 7 Planes × 7 Senses × 7 Items = **343 Vectors**.

> **CRITICAL:** This document defines the "Gold Standard" format. Files must be generated with strict adherence to these rules to pass the `verify_kanon_rules.py` automated audit.

---

## 1. The 7 Planes (Files)

Create 7 Markdown files for the nation. The ordering must be strict.

| Order | Vector | Thematic Name (Default) | File Naming Convention |
| :--- | :--- | :--- | :--- |
| 1 | **WHO** | Identity | `[Nation]_Kanon_Plane_1_Identity.md` |
| 2 | **WHAT** | Definition | `[Nation]_Kanon_Plane_2_Definition.md` |
| 3 | **WHERE** | Land | `[Nation]_Kanon_Plane_3_Land.md` |
| 4 | **WHY** | Drive | `[Nation]_Kanon_Plane_4_Drive.md` |
| 5 | **HOW** | Method | `[Nation]_Kanon_Plane_5_Method.md` |
| 6 | **CAUSE** | Foundation | `[Nation]_Kanon_Plane_6_Foundation.md` |
| 7 | **EFFECT** | Result | `[Nation]_Kanon_Plane_7_Result.md` |

> **Note:** The "Thematic Name" can be adjusted if appropriate for the nation (e.g., "Foundation" for Cause, "Result" for Effect), but the Vector Order (1-7) and Base Vector (Who-Effect) are immutable.

## 1.1 The Geometric Mapping (The 42-Structure)

When structuring the vectors into the **42-Structure**, they map to the following Axes:

### THE DRIVER (The Emergent Axis)
*   **Q1: The Meta-Physical Plane (WHO)** – Will and Direction. The 7th Angle Axis.

### THE LATERAL Body AXIS (Definition & Space: +/- x)
*   **+x: Q2: The Possible Plane (WHAT)** – Faith and Probability.
*   **-x: Q3: The Physical Plane (WHERE)** – Matter and Distance.

### THE LONGITUDINAL Mind AXIS (Function & Meaning: +/- y)
*   **+y: Q4: The Lyrical Plane (WHY)** – Meaning and Resonance.
*   **-y: Q5: The Logical Plane (HOW)** – Count and Consistency.

### THE VERTICAL Soul AXIS (Temporal Link: +/- z)
*   **+z: Q6: The Historical Plane (CAUSE)** – Sequence and Causality.
*   **-z: Q7: The Emotive Plane (EFFECT)** – Passion and Consequence.

---

## 2. The Internal Structure (Per File)

Each Markdown file must follow this exact template.

### A. File Header
```markdown
# The [Nation] Kanon:
# Plane [Vector]; Values of [Nation] [Thematic Name]

> *"[Quote encapsulating the entire Plane]"*
> — **[Author]**, *[Source]*, [Year]

## THE PLANE OF [THEMATIC NAME] ([VECTOR])
```

### B. The 7 Senses (Sections)
You must create 7 distinct sections (Headers) corresponding to the 7 Vectors, strictly ordered: `q1` to `q7`.

**Naming Convention:** `The [Sense Vector] of the [Plane Thematic Name] ([Plane Vector])`

*Example for Plane 1 (Identity/Who):*
*   Sense q1: The Who of the Identity (Who)
*   Sense q2: The What of the Identity (Who)
*   Sense q3: The Where of the Identity (Who)
*   ...etc.
*   ...etc.

### C. Deriving the Vector (The Logic)
To effectively fill each slot, you must "Triangulate" the meaning using the 3 coordinates:

**Formula:** `[Vector (Item)]` of the `[Sense (Section)]` of the `[Plane (File)]`.

*   **Plane (Context):** The broad subject (e.g., Identity/Who).
*   **Sense (Lens):** The specific aspect being examined (e.g., Land/Where).
*   **Vector (Detail):** The atomic interrogative property (e.g., Motivation/Why).

**Example Calculation: (Who.Where.Why)**
1.  **Plane (Who):** We are discussing *Identity*.
2.  **Sense (Where):** We are looking at the *Origins/Land* aspect of Identity.
3.  **Vector (Why):** We need the *Motivation/Drive* of that aspect.
*   **The Question:** "What is the *Motivation* (Why) derived from the *Land* (Where) that shapes the *Identity* (Who)?"
*   **The Answer (Australia):** "Populate or Perish" (The drive to fill the empty land to survive).

### D. The 7 Vectors (Items)
Under each "Sense" header, you must generate 7 specific items.

**Format Rule:**
*   **Bold** the Vector ID and Concept Name.
*   **Terminator:** Use a semi-colon `;` after the concept name.
*   **Citation:** Quote first, then Author, Source, Year.

```markdown
**([Plane].[Sense].[Vector]) [Concept Name]**; "[Specific Quote]" - [Author]. *[Source]*, [Year]

    [Paragraph 1: Historical/Narrative Context (Min 2 sentences). Explain the quote and the event. Keep it objective.]

    This establishes [Core Value] as the [Detailed Definition]. [Paragraph 2: Analytical Conclusion (Min 5 sentences). Use "This establishes X as Y" phrasing. Explain why this vector defines the nation's psychology.]
```

### E. Verification Standards (The "7-Sentence Rule")
To ensure depth, each Vector Item must meet the following density metrics (enforced by the `verify_kanon_rules.py` script):
1.  **Total Length:** Minimum **7 sentences** per item (Context + Meaning).
2.  **Structuring:**
    *   **Context Block:** ~2 sentences setting the scene.
    *   **Meaning Block:** ~5 sentences unpacking the philosophical implication.
3.  **Strict Syntax:**
    *   The **Semi-Colon (;)** must be OUTSIDE the bolding: `**...Name**;`.
    *   The **Quote** must follow immediately.
4.  **Spacing (Critical):**
    *   **Blank Line 1:** Must exist between the Title Line and the Context Paragraph.
    *   **Blank Line 2:** Must exist between the Context Paragraph and the Meaning Paragraph.
5.  **Indentation:**
    *   Both paragraphs must be indented by **4 spaces** to visually separate them from the header.

### D. The Narrative Summary
At the end of *each* Sense section (after the 7 vectors), provide a summary block.

**Format:**
```markdown
```markdown
> **The Narrative of [Sense Concept] (The [Sense Vector] of the [Plane Thematic Name] ([Plane Vector])):
> The [Nation] [Plane] begins with **[Concept 1]**... [Synthesize the 7 vectors into a cohesive paragraph. Bold the Concept Names to cross-reference the list above.]
```

### F. The Totality Narrative (Plane Summary)
At the very end of the file (after Sense q7), you must provide a "Totality Narrative" that synthesizes the entire Plane (all 49 vectors, but focusing on the 7 Sense narratives).

**Format:**
```markdown
> **The Totality of [Nation] [Plane Thematic Name]** is a complex architecture... [Write a high-voltage philosophical summary. Use metaphors of circuitry, architecture, or organisms. Explain how the 7 Senses interact to form the whole.]
```

---

## 3. Detailed Ordering Guide

To ensure the 343 structure is complete, follow this matrix for every file.

### Plane 1: Identity (Who)
- **q1:** The Who of the Identity (Who) - *(Authenticity)*
- **q2:** The What of the Identity (Who) - *(Roles)*
- **q3:** The Where of the Identity (Who) - *(Origins)*
- **q4:** The Why of the Identity (Who) - *(Motivations)*
- **q5:** The How of the Identity (Who) - *(Character/Habit)*
- **q6:** The Cause of the Identity (Who) - *(Ancestry/Roots)*
- **q7:** The Effect of the Identity (Who) - *(Legacy)*

*(Repeat this explicit q1-q7 pattern for all Planes, changing the Parent Context).*

### Plane 2: Definition (What)
- The Who of the Definition (What) / The What of the Definition (What) / ...etc.

### Plane 3: Land (Where)
- The Who of the Land (Where) / The What of the Land (Where) / ...etc.

### Plane 4: Drive (Why)
- The Who of the Drive (Why) / The What of the Drive (Why) / ...etc.

### Plane 5: Method (How)
- The Who of the Method (How) / The What of the Method (How) / ...etc.

### Plane 6: Foundation (Cause)
- The Who of the Foundation (Cause) / The What of the Foundation (Cause) / ...etc.

### Plane 7: Result (Effect)
- The Who of the Result (Effect) / The What of the Result (Effect) / ...etc.

---

## 4. Content Selection Strategy: Building the Ideal
The primary goal is to **construct the Ideology** of the nation. We are mapping the "National Ideal"—what the nation *strives* to be. Remember, each vector meant to be an example of what the nation means irrespective of political or economic ideology, purely based on the intention of its founders and its motivating members through history, matched to each fractal interrogative

**The Primary Objective:**
Use the words of the **Founders** (Originators) to define the specific "Ideal" of the nation, then use quotes over time to show the trajectory of that Ideal.

**Criteria for Selection:**
1.  **The Heuristic of Age (Priority Rule):**
    *   **Foundational Authority:** Always prioritize the *Founders* or *Originators* of the concept. (e.g., Washington, Jefferson, Barton, Parkes).
    *   **Trajectory:** If the Founder defined it, show how it has endured or evolved.
    *   **Fallback:** High-quality historical quotes.
    *   **Last Resort:** Documentary/Administrative facts (Only if no "Soul" quote exists).

2.  **Iconic Resonance:** Does every schoolchild know this? (e.g., "I Have a Dream", "Lest We Forget").
3.  **Emotional Voltage:** Does it provoke Pride, Shame, Tears, or chills?
4.  **Relevance:** The quote must be *purely relevant* to the specific Node.

*   **Bad Vector:** "The Tax Act of 1993 adjusted brackets." (Low Voltage / Dry).
*   **Good Vector:** "No Taxation Without Representation." (High Voltage / Foundational).

---

## 5. Analytical Rules (The "Kanon" Tone)

1.  **Evidence-Based:** Every vector must be anchored by a real snippet of reality (a quote, a law, a date, an event). Do not use vague generalizations.
2.  **The "This Establishes" Formula:** The second paragraph of every item *must* begin with "This establishes [Concept] as...". This is the mechanism that transforms history into philosophy.
3.  **Strict Hierarchy:**
    -   **Plane:** The General Context.
    -   **Sense:** The Specific Lens.
    -   **Vector:** The Atomic Unit of Reality.
4.  **No Logic Mixing:**
    -   Do not put a "Why" quote in a "Who" section unless you are explicitly analyzing the "Why of the Who".
    -   Respect the geometry.

---

## Part II: Technical Execution & Generation

This section defines the "Body" of the Kanon—the file systems, data structures, and code required to compile the analysis into a working website.

## 6. The Shadow Files (Judgment Data)

For every Content File (Plane), you must create a corresponding **"Shadow File"** to store the discrete data values (Moral Vector, Will Vector, and Judgment Category). 

> **CRITICAL:** The HTML Generator (`generate_pages.py`) looks for these files to create the "Badges" (e.g., Green/Red indicators) in the site. If missing, the site will generate without data badges.

### 6.1 File Naming
Append `_JUDGMENT.md` to the content filename.
*   **Content:** `[Nation]_Kanon_Plane_1_Identity.md`
*   **Shadow:** `[Nation]_Kanon_Plane_1_Identity_JUDGMENT.md`

### 6.2 Internal Structure
The file must contain **Markdown Tables** for each Sense. The columns `υ` (Nu/Moral) and `ψ` (Psi/Will) are processed by the script.

**Template:**
```markdown
# [Nation] Kanon Plane [N] — Judgment Shadow File

## 1.1 The [Sense] of the [Plane]

| Vector | Entry | υ | ψ | Judgment |
|--------|-------|---|---|----------|
| P.S.V | **[Concept Name]** | +0.7 | +0.4 | **Greater Good** — [Short Note < 100 chars] |
| P.S.V | **[Concept Name]** | -0.5 | +0.8 | **Greatest Lie** — [Short Note] |
...
```

### 6.3 Judgment Categories (Standard)
The `Judgment` column determines the **Badge Color** in the HTML.

| Judgment | Criteria | Color (in CSS) |
| :--- | :--- | :--- |
| **Greater Good** | (+υ, +ψ) Universal Benefit + Proactive | Green |
| **Good** | (+υ) Benefit (Passive or Active) | Green |
| **Lesser Good** | (+υ, -ψ) Benefit with Passivity | Green-Light |
| **Greatest Lie** | (-υ, +ψ) Self-Benefit + High Will | Red |
| **Tension Point** | Mixed vectors or highly controversial | Orange |
| **Constraint** | Neutral/Environmental Fact | Gray |

---

## 7. Site Generation Protocol

Once the 14 Markdown files (7 Content + 7 Judgment) are drafted, use the Python engine to compile the site.

### 7.1 Directory Structure
Ensure your workspace matches this structure:
```
[Nation]/
├── [Nation]_Kanon_Plane_1_Identity.md
├── [Nation]_Kanon_Plane_1_Identity_JUDGMENT.md
├── ... (All 14 files)
└── site/
    └── generate_pages.py
```

### 7.2 Running the Generator
1.  Navigate to the `site/` directory.
2.  Run the script: `python generate_pages.py`
3.  The script will parse both the Content and Shadow files and output 7 HTML files (e.g., `Plane_1_Identity.html`).

### 7.3 Mobile Responsiveness Standards
The generated HTML must meet these specific responsive criteria (enforced by the script's CSS):
1.  **Mobile Card View:** On screens < 640px, the data tables must transform into **Vertical Cards** (Code → Concept → Description) to eliminate horizontal scrolling.
2.  **Hamburger Navigation:** The desktop sidebar/topbar must collapse into a standard **Hamburger Menu** on mobile.
3.  **Visual Badges:** On mobile, the Judgment Vectors (υ/ψ) must remain legible, usually formatted as "Pills" within the Concept card.

---

## 8. Verification (The Audit)

Before finalizing, run the `verify_kanon_rules.py` script against your Content Files.

**Command:**
```bash
python verify_kanon_rules.py
```

**What it Checks:**
*   **Structure:** proper `**(Code) Name**;` syntax.
*   **Depth:** Enforces the **7-Sentence Rule** (Context + Meaning block length).
*   **Completeness:** Ensures all 7 vectors per Sense are present.

