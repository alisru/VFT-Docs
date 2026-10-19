# Plan 012: Comprehensive Diagnostic Logging & Event Binding Verification

## Objective
Provide full, real-time diagnostic console logging for all Auto-Scribe content script events (keydown, pointerdown, click, submit, input, focusin, draft persistence, clearance polling) and bind listeners redundantly to both `window` and `document` in capture phase to guarantee interception.

## Changes Made
1. **Redundant Event Bindings**:
   - `handleKeyDownTrigger`: Intercepts `e.key === 'Enter'`, `e.code === 'Enter'`, or `e.keyCode === 13` on BOTH `window` and `document` with `capture: true`.
   - `handlePointerTrigger`: Intercepts `pointerdown` and `click` on BOTH `window` and `document` with `capture: true`.
   - `submit`: Intercepts form submissions on BOTH `window` and `document`.

2. **Full Diagnostic Logging**:
   - `[Auto-Scribe] Content script active on <host>`
   - `[Auto-Scribe] keydown: Enter key detected on <TAG>`
   - `[Auto-Scribe] pointerdown/click detected on <TAG>`
   - `[Auto-Scribe] triggerPotentialSubmit() called from [source]`
     - Prints active target element, current text length, minChars threshold, and draft ID.
     - Logs warnings if target is missing or if text length $< \text{minChars}$.
   - `[Auto-Scribe] Polling at <delay>ms: isUnmounted=<bool>, remTextLen=<n>, isCleared=<bool>`
   - `[Auto-Scribe] ✅ BOX CLEARED at <delay>ms! MARKING AS POSTED: <draft_id>`
   - `[Auto-Scribe] ✗ Manual text deletion without submit. Deleting draft: <draft_id>`
