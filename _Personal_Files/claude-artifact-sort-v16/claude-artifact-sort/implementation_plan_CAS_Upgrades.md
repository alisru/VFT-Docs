# Implementation Plan - Claude Artifact Sorter (CAS) Upgrades

This plan outlines the upgrades for the CAS extension, focusing on artifact metadata visibility, version tracking, download monitoring, and a comprehensive tagging system.

## User Review Required

> [!IMPORTANT]
> **Versioning Logic**: Since Claude's internal versioning is opaque, CAS will implement a "Sequence Versioning" system. Artifacts with the same name in a single chat will be numbered (v1, v2, v3...) based on their order in the conversation flow.
> **Tagging Data**: Tags will be stored locally in `cas_tags`. These are NOT synced to Claude's servers and are purely for CAS organization.

## Proposed Changes

### 1. Enhanced Metadata Tracking & Storage
- **[MODIFY] [content.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js)**
    - Implement `ArtifactHistory` storage to track updates and "fake" versions.
    - Update `extractNodeData` to include version detection.
    - Implement a download listener to track `cas_downloads`.

### 2. Side Panel UI Upgrades
- **[MODIFY] [content.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js)**
    - Generalize `injectSummary` into `injectArtifactMeta`.
    - Display recorded date, version number, and tags directly on Claude's sidebar artifact cards.
    - Add "Premium" styling for these metadata labels (glassmorphism/subtle glow).

### 3. Tagging System (Matrix)
- **[MODIFY] [content.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js)**
    - Add a constant `TAG_MATRIX` based on the user's provided list.
    - Add a Tagging UI to the CAS Modal and Chat Flyout.
    - Implement a searchable tag selector.
    - Store tags per chat and per artifact.

### 4. Sorting & Manual Interaction
- **[MODIFY] [content.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js)**
    - Add `date-asc` and `date-desc` sorting to the Sort Engine.
    - Enhance "Manual Injection" to support direct chat summary overrides via the Flyout.

## Verification Plan

### Automated Tests
- I will use the browser subagent to:
    1. Verify the CAS panel loads correctly.
    2. Check if the "Recorded Date" appears in the sidebar cards.
    3. Test the "Sort by Date" functionality.
    4. Validate that clicking a download button (mocked) triggers a record.

### Manual Verification
- Test tagging an artifact and ensuring the tag persists and displays in the sidebar.
- Verify "Manual Injection" from the Flyout updates the stored summary correctly.
