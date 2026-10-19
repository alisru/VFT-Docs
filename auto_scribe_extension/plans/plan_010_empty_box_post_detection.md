# Plan 010: Empty-Box Post-Submission Detection

## Key Breakthrough & User Insight
- Trying to pattern-match every website's button labels, SVG icons, and keyboard shortcuts is prone to edge cases (e.g., Shadow DOM, custom event listeners, framework re-renderings).
- The universal ground truth of post submission is:
  **If an Enter keypress or click occurs, and the active text box subsequently clears (becomes empty or unmounts from the DOM), the post was submitted.**

## Architecture

1. **Fixed `getEditableRoot`**:
   - Previously returned `el` as a fallback, causing non-editable elements (such as clicked buttons or wrapper divs) to be treated as editable roots.
   - Now returns `null` for non-editable elements, preventing corruption of `activeElement` and `lastActiveElement`.

2. **Empty-Box Detection Polling (`triggerPotentialSubmit`)**:
   - Triggered on any `Enter` keypress, button click, or `pointerdown`.
   - Records the active draft element, current text, and draft ID into `activeEmptyCheck`.
   - Polls at progressive intervals (`[70ms, 180ms, 350ms, 650ms, 1100ms, 1800ms, 3000ms]`):
     - If the element is unmounted (`!document.contains(target)`) OR its remaining text length drops to $<15$ characters:
       - Confirms the post submission.
       - Dispatches `SAVE_DRAFT` with `status: 'posted'`.
       - Dispatches `MARK_DRAFT_POSTED`.
       - Cleans `savedDraftMap` and `sessionKeyMap.delete(target)`.
       - Renders the green saved tick on the indicator.

3. **Distinction from Manual Deletion**:
   - If the user deletes text with Backspace or Delete, no Enter or click was performed. `evaluateTextChange` recognizes the manual deletion and removes the draft from storage (`DELETE_DRAFT`).
   - If Enter or a click was performed and the box cleared, `isRecentSubmit` evaluates to `true` and the draft is marked `posted`.
