# Plan 013: Fix Deletion Duplication Bug & Restrict Submit Triggers

## Critical Defect Identified
- In the previous step, binding global `pointerdown` and `click` listeners to BOTH `window` and `document` caused every single mouse click (such as clicking into the box to select text or delete) to fire 4 times in rapid succession.
- Inside `triggerPotentialSubmit`, `currentText` fell back to `lastSavedText` if the box was empty.
- When the user deleted text and clicked, `triggerPotentialSubmit` resurrected the old deleted text from `lastSavedText`, detected that the actual box was empty, concluded that the post had cleared/submitted, and saved 3 to 4 duplicate copies of the deleted draft!

## Fixes Implemented
1. **Never Resurrect Deleted Text**:
   - `triggerPotentialSubmit` now strictly inspects the CURRENT text in the active editor (`extractText(target)`).
   - If `currentText` is empty or $< \text{minChars}$, it immediately aborts. It NEVER falls back to `lastSavedText`.
   - `deleteSavedDraft` now clears `lastSavedText = ''`, `lastActiveDraftId = null`, and `activeEmptyCheck = null`.

2. **Restrict Submit Detection to Explicit Submit Actions**:
   - Removed all generic `pointerdown` and `click` listeners on arbitrary elements.
   - Click triggers are strictly gated by `isSubmitClick(e)` (penetrating Shadow DOM via `composedPath`), which ONLY returns true if the clicked element is an actual submit/post/comment/send button, icon, or matching aria-label.
   - Keydown triggers are strictly gated to `e.key === 'Enter'`.

3. **Single Document-Level Bindings & Throttling**:
   - Replaced redundant `window` + `document` bindings with single `document.addEventListener(..., true)` listeners.
   - Throttled `triggerPotentialSubmit` to a maximum of once per 1.5 seconds to eliminate burst duplicates.
