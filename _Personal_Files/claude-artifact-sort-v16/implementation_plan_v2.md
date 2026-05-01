# Fix Claude UI Regressions & Stabilize Gemini Appendage

Stabilize the artifact management system by fully separating Gemini UI logic from the Claude core and fixing layout regressions in the Claude interface.

## User Review Required

> [!IMPORTANT]
> I am assuming that for **Claude**, you want the full sorting bar (A-Z, Newer, etc.) in the sidebar, but maybe **not** the "SUMMARISE" and "INJECT" buttons if they are already accessible via the header or flyout? The current regression shows them overlapping or appearing in the chat area.

## Proposed Changes

### [content.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js)

#### [MODIFY] [findArtifactSidebar](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js#L114-L139)
- **Strict Claude Targeting**: Explicitly distinguish between the `Artifacts Sidebar` (list) and the `Artifact Immersive Panel` (viewer).
- Target `[data-testid="artifacts-sidebar"]` or `nav`/`aside` elements that specifically contain the "Artifacts" heading but are NOT inside a message or the primary editor.
- Ensure the "Artifacts" label found is the actual section header.

#### [MODIFY] [injectSidebarSortBar](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js#L395-L480)
- Anchor the sort bar specifically to the **header** of the Artifacts sidebar (next to the "Artifacts" label) rather than prepending to the entire container which might be the immersive panel.
- If a header anchor is found, use `.appendChild()` on the header container or `.after()` the label to ensure it stays in the "Label" area as requested.
- [NEW] Add a check to prevent injection into the `Artifact Immersive Panel`.

#### [MODIFY] [refreshSummariseBadge](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js#L4009-L4047)
- Add platform check: Only append the "SUMMARISE" / "INJECT" toolbar to the sidebar bar on **Gemini**.
- For **Claude**, keep these actions in the flyout/header to avoid sidebar clutter and alignment issues.

#### [MODIFY] [injectToggleButtons](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Personal_Files/claude-artifact-sort-v16/claude-artifact-sort/content.js#L4149-L4245)
- Refine the anchor logic for Claude to ensure it doesn't push the "Open Sidebar" button out of view.
- Add descriptive tooltips to the Gemini-specific buttons in the main header as well.

## Verification Plan

### Manual Verification
1. Open Claude with multiple artifacts and verify the sort bar appears strictly at the top of the artifacts list in the sidebar, not in the chat.
2. Verify the `⬡` and `⌬` buttons in the Claude header are aligned correctly with the native "Share" and "Sidebar" buttons.
3. Switch to Gemini and verify the minimalist sidebar toolbar (Summarise Chat | Inject | ↺) is present with correct tooltips.
4. Verify that closing the sidebar/immersive panel on either platform does not cause ghost elements to remain.
