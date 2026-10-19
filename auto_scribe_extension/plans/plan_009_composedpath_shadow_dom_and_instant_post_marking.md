# Plan 009: ComposedPath Shadow DOM Submit Detection & Instant Post-Marking

## Root Cause of Failed Post Detection on Reddit & Gemini

1. **Reddit Shadow DOM Encapsulation**:
   - Modern Reddit encapsulates its comment and post boxes inside Web Components (`<shreddit-composer>`, `<shreddit-comment-action-row>`, `<faceplate-form>`).
   - Standard `e.target` retargets to the custom element host when an event bubbles out of a shadow root. Consequently, `e.target.closest('button')` returned `null` because the button exists inside the Shadow DOM.
   - Using `e.composedPath()` provides the full event propagation path across all shadow boundaries, exposing the actual `<button slot="submit-button">Comment</button>` element.

2. **Debounce Race Condition on Reused Containers (Gemini & Single-Page Apps)**:
   - When a user submitted on Gemini, the delayed intervals of `schedulePostVerification` encountered the prompt still present in the DOM during the first 100-300ms.
   - This re-triggered a 1.5s debounced `persistDraft` timer. When that timer expired after the prompt cleared and the session key was refreshed, it generated a brand-new draft ID and persisted the old prompt as a new unposted draft.

## Solution

1. **`composedPath()` Submit Detection**:
   - Inspects all nodes in `e.composedPath ? e.composedPath() : [e.target]` to penetrate shadow roots.
   - Detects Reddit's `slot="submit-button"`, `data-testid` submit tags, and button text "Comment", "Post", "Reply", "Send".
   - Detects Gemini's `aria-label="Send message"` and `send-button` class attributes.

2. **Instant Post-Marking (`markCurrentDraftSubmitted`)**:
   - Triggers synchronously on `pointerdown`, `click`, or submit keypress (`Enter` on Gemini, `Ctrl+Enter` on Reddit).
   - Cancels any pending `debounceTimer` immediately.
   - Directly sets `status: 'posted'` and dispatches `SAVE_DRAFT` + `MARK_DRAFT_POSTED`.
   - Cleans the element from `savedDraftMap` and resets `sessionKeyMap.delete(target)` so subsequent messages get a fresh draft ID and never clobber posted items.

3. **Window Capture Listeners**:
   - Listeners for `pointerdown`, `click`, `keydown`, and `submit` are registered on `window` with `capture: true` to guarantee Auto-Scribe runs before website-level `stopPropagation()` or `preventDefault()`.
