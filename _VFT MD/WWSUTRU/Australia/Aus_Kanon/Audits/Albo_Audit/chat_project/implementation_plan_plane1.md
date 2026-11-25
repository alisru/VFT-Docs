# Implementation Plan: Anthony Albanese Hegemonic Audit (Plane 1)

This plan outlines the strict procedural workflow for executing a fresh hegemonic audit of Anthony Albanese against **Plane 1 (Identity)** of the Australian Kanon. 

All files will be managed inside the project folder: [Albo_Audit](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit).

---

## 1. Procedural Execution Workflow (Node-by-Node)

 we will proceed strictly **one node at a time** (starting with `Who.Who.Who` and moving through all 53 Plane 1 entries). For each node, we will execute the following four steps:

### Step 1: Conceptual Triangulation (Move 1)
* Retrieve the fixed coordinates, name, and definition from the ground-truth file [Plane_1_Identity_compact.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agents/skills/kanon-audit/references/Plane_1_Identity_compact.json).
* Triangulate the ideal: `[Vector]` of the `[Sense]` of `Plane 1 (Identity)`. Define the underlying mechanism (e.g., who does the ideal benefit, and what energy does it require).

### Step 2: Training-Data Hypothesis (Move 2a)
* Before touching the database, identify a **specific real-world event, speech, or policy** from Albanese's public record that matches this mechanism.
* Define a clear hypothesis: *"For this vector, Albanese's record is anchored by his [incident/date/speech] where he reacted by [action/stance]."*

### Step 3: Verbatim Verification & Fetching (Move 2b)
* If the hypothesized or web-discovered quote/incident is a **Hansard parliamentary speech** within the 1998–2025 range, we query the local Parquet database (`corpus_1998_to_2025.parquet`) via DuckDB to retrieve the exact verbatim text and metadata.
* If it is a **non-Hansard source** (e.g. press conference, TV interview, policy document, or news article), we fetch the direct primary source via web search/local file reading rather than using DuckDB.
* Extract the exact verbatim text for the **Header Quote** and a separate verified action/statement with dates for the **Actuality** section, compiling precise URLs for the citations.

### Step 4: Write Node to file
* Write the fully compiled node directly to [Plane_1_Identity.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit/Plane_1_Identity.md) and log the source citations in [Sources.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit/Sources.md).

---

## 2. Formatting & Verification Standards

We will enforce the following structural rules on the output document:
* **Header Format**: `**(Address) Vector Name (upsilon: \+X.X, psi: \+Y.Y): HIT/FAIL.** **Quote:** "quote text"[^ref_id]` (on a single line, with escaped coordinates).
* **Footnote Citations**: Every quote and actuality point must have a footnote link (e.g. `[^ref1]`) pointing to a detailed entry in `Sources.md` containing the speaker, title, date, Hansard page, and URL.
* **Paragraph Structure**: Exactly three body sections (`Description`, `**Justification:**`, and `Actuality`). 
  * Sentence count: **Minimum 4-5 sentences** for each section.
  * To match the project's layout style, each sentence within these sections will be separated by a double newline.
* **No Code in Text**: No coordinate symbols ($\upsilon$, $\psi$, $+0.x$, $-0.x$) allowed in the body text of `Description` or `Actuality` (Justification explains the axes in plain language only).

---

## 3. Structural Completion Checklist
Before declaring the plane complete, we will run validation checks to ensure:
1. Every node's name, address, and coordinates match the ground-truth JSON exactly.
2. Every footnote link matches a source in `Sources.md`.
3. The final average coordinates use **verdict-weighted scoring**: 
   $$\text{Avg} = \frac{\sum (\text{Coordinate} \times \text{Verdict Weight})}{\text{Total Count}}$$
   *(Where Verdict Weight = $+1$ for HIT and $-1$ for FAIL).*
