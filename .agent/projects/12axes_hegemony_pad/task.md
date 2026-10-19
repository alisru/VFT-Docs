# 12axes_hegemony_pad

**Current Focus**: Project Start

**Progress**: 5/5 complete

## Task List
- [x] Implement Square Grid [-2, +2] in QuestionTargetPad with Human (+-1) and Systemic (+-2) borders `ui geometry square` <!-- id: 0 -->
- [x] Replace internal notation ({Everyone}, Greek letters, Will Be) with plain grounded human options `ui jargon notation` <!-- id: 1 -->
- [x] Restore 12-Axis Relative Context above Target Pad showing active axis poles and tension impact `ui quiz context` <!-- id: 2 -->
- [x] Decouple drag and click from auto-advance so navigation only occurs on explicit Confirm button click `ui ux drag` <!-- id: 3 -->
- [x] Isolate English (user default) and Portuguese (author) strictly, removing Spanish references `i18n tokens` <!-- id: 4 -->

## Mistake Registry
> [!WARNING] ARC_001: Standard Vector [archaeology, historical]
> **Structure**: The Colonial Row (e.g., "Populate or Perish").
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_002: Partner Vector [archaeology, historical]
> **Structure**: The First Nations Row (e.g., "Anteriority").
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_003: Standard Mode [archaeology, historical]
> **Structure**: Gray/White styling, "The Vector" metadata.
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_004: First Nations Mode [archaeology, historical]
> **Structure**: Amber styling (`bg-amber-50`), "First Nations Perspective" metadata.
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_005: original [archaeology, historical]
> **Structure**: "Populate or Perish" (The Imperative)
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_006: partner [archaeology, historical]
> **Structure**: "Anteriority" (First Nations Perspective)
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_007: original [archaeology, historical]
> **Structure**: "The First Fleet" (The Seed)
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_008: partner [archaeology, historical]
> **Structure**: "Continuity" (First Nations Perspective)
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_009: Guilt, Abundance, Resistance [archaeology, historical]
> **Structure**: Identified these vectors were incorrectly located in Plane 3. Moved them to **Plane 4 (Drive)** wher
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_010: Attributions Updated [archaeology, historical]
> **Structure**: - **Guilt**: Sourced to Paul Keating ('Redfern Park Speech', 1992).
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] ARC_011: inline_fix [archaeology, historical]
> **Structure**: character encoding issue for Marcia Langton quote
> **Example**: Source: walkthrough:walkthrough.md
>
> [!WARNING] M001: Kanon Formatting Deviation [kanon, formatting]
> **Structure**: Incorrect Paragraph Structure
> **Example**: Merged context without distinct Description block
>
> [!WARNING] M002: Format Deviation [kanon, formatting]
> **Structure**: Missed Kanon Paragraph Structure
> **Example**: Merged context/meaning blocks and missed indentation
>
> [!WARNING] M003: Fragmented Meaning Block [plane6, formatting]
> **Structure**: Orphaned 'This establishes' sentence
> **Example**: Line 17 in Plane 6 Foundation: 'This establishes a foundation born...'
>
> [!WARNING] M004: Index Desynchronization
> **Structure**: Manually tracking IDs which diverge from system-assigned IDs.
> **Example**: Tried to mark task 32 as DONE when system only had 19 tasks.
>
> [!WARNING] M016: Notation Leaks in Public UI [ui, jargon, notation]
> **Structure**: Exposing internal dev shorthand and Greek notation in public-facing interfaces
> **Example**: Showing {Everyone} and Will Be (+u, +psi) on user question pad
>
> [!WARNING] M017: Square Grid Reversion to Circle [ui, geometry, regression]
> **Structure**: Replacing explicit square geometry [-2, +2] with circular polar radar
> **Example**: Rendering SVG circles and arcs instead of square horizon borders
>
> [!WARNING] M018: Premature Auto-Advance Snatching Input [ui, ux, drag]
> **Structure**: Triggering timer-based navigation on drag or pointerDown instead of requiring explicit confirmation
> **Example**: Advancing 200ms after user clicks pad while dragging
>
> [!WARNING] M019: Dropping Axis Relative Context [ui, quiz, context]
> **Structure**: Stripping out the explanation of what agreeing/disagreeing does to the active 12-axis balance
> **Example**: Removing axis pole tension labels from question view
>
> [!WARNING] M020: Unwanted Language Expansion and Bleed [i18n, tokens, scope]
> **Structure**: Expanding into Spanish and mixing languages instead of keeping clean English for user and Portuguese for author
> **Example**: Adding Spanish archetype translations and mixing languages
>