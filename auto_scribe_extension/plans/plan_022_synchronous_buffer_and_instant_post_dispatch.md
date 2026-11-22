# Plan 022: Synchronous Local Draft Buffer & Instant Post-Dispatch State Machine

## Context & Problem Statement
The user asked:
"it's still too slow, can it buffer or cache the changes so if its posted while its being sent it's simply recorded then marked posted?"

## Current Bottlenecks Identified
1. **Asynchronous Lag on Fast Post**:
   When typing and submitting in quick succession, `evaluateTextChange` had an 800ms debounce. If the user hit submit before 800ms:
   - `triggerPotentialSubmit` tried to send `SAVE_DRAFT` over `chrome.runtime.sendMessage`.
   - Then it waited through multiple delayed polling checks (`60, 150, 350, 700...` ms) to see if the box cleared.
   - If the page reloaded, navigated, or destroyed the frame immediately upon form submit (standard behavior on Drupal, forums, and traditional POST forms), all pending timeouts and async callbacks were killed before `SAVE_DRAFT` and `MARK_DRAFT_POSTED` could finish.
2. **Missing Synchronous Cache & Pre-Submit Lock**:
   - `currentWorkingTextMap` was just an in-memory `WeakMap` without an atomic payload cache.
   - The moment a submit action occurs (Enter keydown or submit button click in capture phase), we already know:
     1. The draft ID.
     2. The exact text.
     3. The URL and title.
     4. That a submit action is actively occurring.
   - Waiting for the box to clear or waiting on async roundtrips creates a race condition against page navigation.

## Proposed Architecture: The Synchronous Buffer & Atomic Post-Dispatch

### 1. Synchronous Working Buffer (`scribe_content.js`)
- Maintain a synchronous memory buffer `activeDraftBuffer`:
  ```javascript
  activeDraftBuffer = {
    id: draftId,
    site: currentHost,
    url: getEffectiveUrl(),
    page_title: getEffectiveTitle(),
    context_title: detectContext(),
    text: text,
    char_count: text.length,
    word_count: wordCount,
    updated_at: new Date().toISOString(),
    status: 'draft'
  };
  ```
- Updated synchronously on **every keystroke / input event** ($\ge 30$ chars).
- When any submit action triggers (Enter, button click, form submit event, or beforeunload):
  - If `activeDraftBuffer` has text $\ge 30$ chars:
    - Atomically upgrade `activeDraftBuffer.status = 'posted'`.
    - `activeDraftBuffer.posted_at = new Date().toISOString()`.
    - Dispatch `SAVE_DRAFT` with `status: 'posted'` immediately in the event capture phase!
    - Also use `navigator.sendBeacon` or background direct message so if the page navigates away in the next millisecond, the posted draft is already committed.

### 2. Fast Debounce & Atomic Pre-Save
- Reduce normal typing debounce to `300ms` (down from 800ms) with zero-cost memory buffering.
- When `triggerPotentialSubmit` runs:
  - If text is present, do not wait for box clearance to save. Save it as `posted` right away!
  - If box clears afterwards, it just confirms it. If the page unloads/navigates, it is already safely in storage as `posted`.

### 3. Background Race-Condition Defense (`background.js`)
- If a `SAVE_DRAFT` message arrives with `status: 'posted'`, it immediately records it as `posted` and never gets overwritten by a late-arriving background sync.

## Verification
- Validate JS syntax with `node -c`.
- Verify instant recording on form submits and Enter key without waiting for polling loops.
