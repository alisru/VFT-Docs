# Implementation Plan: Anthony Albanese Hegemonic Audit (Plane 2 Completion)

This plan outlines the procedural workflow for completing the hegemonic audit of Anthony Albanese against **Plane 2 (Definition)** of the Australian Kanon. 

All work will be performed within the active project folder: [Albo_Audit](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit).

---

## User Review Required

> [!IMPORTANT]
> **Strict Verification Boundaries**: We will verify all quotes and actions before adding them. In accordance with the project's lessons-learned constraints, we will not overprove actuality sections with multiple unneeded examples, and we will verify complete timelines (e.g., ensuring subsequent policy reversals are recorded).

---

## Open Questions
There are no major open questions. We will use the local Hansard corpus first for parliamentary speeches, and targeted web searches for non-parliamentary context.

---

## Proposed Changes

### Plane 2 Document
#### [MODIFY] [Plane_2_Definition_Albanese.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit/Plane_2_Definition_Albanese.md)
We will append the remaining 17 nodes to the document:
1. `What.How.Cause` - **The Census** (coords: \+0.5, \+0.3)
2. `What.How.Effect` - **The Spill** (coords: \-0.3, \+0.6)
3. `What.Cause.Who` - **The Prophet** (coords: \+0.7, \+0.8)
4. `What.Cause.What` - **The Imperial Act** (coords: \+0.3, \-0.4)
5. `What.Cause.Where` - **The Stockade** (coords: \+0.8, \+0.9)
6. `What.Cause.Why` - **The Slump** (coords: \+0.0, \-0.5)
7. `What.Cause.How` - **The Corowa Plan** (coords: \+0.9, \+0.7)
8. `What.Cause.Cause` - **State Socialism** (coords: \+0.6, \+0.5)
9. `What.Cause.Effect` - **Federation Day** (coords: \+0.6, \+0.4)
10. `What.Effect.Who` - **The Anzac** (coords: \+0.6, \+0.7)
11. `What.Effect.What` - **The Lucky Country** (coords: \+0.3, \-0.4)
12. `What.Effect.Where` - **The Tyranny of Distance** (coords: \+0.0, \-0.6)
13. `What.Effect.Why` - **The Cultural Cringe** (coords: \-0.4, \-0.5)
14. `What.Effect.How` - **Mateship** (coords: \+0.7, \+0.4)
15. `What.Effect.Cause` - **The Great Silence** (coords: \-0.8, \-0.6) (Primary)
16. `What.Effect.Cause` - **Voice [First Nations Perspective]** (coords: \+0.9, \+0.6) (Shadow)
17. `What.Effect.Effect` - **The Nanny State** (coords: \+0.4, \-0.5)

For each node, we will write:
- **Canonical Header**: Address, Vector Name, Coordinates (escaped), Verdict (HIT/FAIL), Quote, and Footnote marker. The quote MUST be cited with a footnote marker immediately following the source context.
- **Description**: Plain text explanation (no coordinate symbols: \(\upsilon\), \(\psi\), \(\pm 0.x\)). Written as a single contiguous paragraph.
- **Justification**: Explaining the moral (\(\upsilon\)) and will (\(\psi\)) axes in plain sentences. Written as a single contiguous paragraph.
- **Actuality**: Evidence of execution over time, ending with TENTATIVE FAIL if necessary. Every specific claim, date, or figure in this section MUST carry its own footnote marker. Written as a single contiguous paragraph.
- **Line Spacing**: Standard paragraph blocks separated by blank lines. No double newlines between sentences within a section (unlike Plane 1, Plane 2 uses standard single-paragraph blocks).

### Sources Master Key
#### [MODIFY] [Sources.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit/Sources.md)
We will append all new verified citations to `Sources.md` and to the `Sources` section of the Plane 2 file.

---

## Verification Plan

### Automated Checks
* **Strict Node Count**: Confirm that all 53 nodes of Plane 2 are present and formatted correctly.
* **Citation Alignment**: Ensure every `[^marker]` used in the body has a corresponding entry in the footer of `Plane_2_Definition_Albanese.md` and `Sources.md`, and that no unused markers exist.
* **Coordinate Consistency**: Validate that all coordinates in the headers match the canonical `Plane_2_Definition_compact.json` exactly.
* **No Coordinate Notations in Descriptions/Actualities**: Verify that symbols like \(\upsilon, \psi, \pm 0.x\) do not appear in the `Description` or `Actuality` sections.
