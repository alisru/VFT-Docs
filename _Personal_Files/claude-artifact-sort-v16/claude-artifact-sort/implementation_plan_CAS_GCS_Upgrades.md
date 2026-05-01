# Implementation Plan - AI Artifact & Canvas Sorter (CAS/GCS) Upgrades

This plan outlines the upgrades for the CAS extension, expanding it to support Gemini (GCS) and adding advanced metadata, version tracking, and download/Drive monitoring.

## User Review Required

> [!IMPORTANT]
> **Gemini Integration (GCS)**: The extension will be refactored to support both `claude.ai` and `gemini.google.com`. The UI panel will be shared, but data extraction will use a "Site Adapter" pattern.
> **Drive Tracking**: I will implement event listeners for "Save to Google Drive" and "Open in Docs" buttons to track artifact migration status.

## Proposed Changes

### 1. Unified Metadata Tracking & Site Adapters
- **[MODIFY] [content.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js)**
    - Implement `SiteAdapter` architecture (`ClaudeAdapter`, `GeminiAdapter`).
    - Update `extractNodeData` to handle Gemini "Canvases".
    - Implement a download & Drive listener to track `cas_activity` (Downloads, Drive exports).

### 2. Multi-Site UI Panel
- **[MODIFY] [content.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js)**
    - Update `injectArtifactMeta` to support Gemini's DOM.
    - Ensure the CAS panel is injected on `gemini.google.com`.
    - Display recorded dates, versions, and tags on both Claude sidebar cards and Gemini canvas links.

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

### 5. Gemini Specific Logic (GCS)
- **[MODIFY] [content.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js)**
    - Add `GeminiAdapter.scanCanvases()` to detect Gemini's artifacts.
    - Map Gemini chats to "Projects" and treat Gemini as a top-level category.

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
