# Plan 008: Reliable Post-Submit & Real-Time Deletion Engine

## Problem Root Causes Identified
1. **Missed Submissions in Modern Web Apps**:
   - Modern web editors (Gemini, Reddit, Facebook, Twitter, Discourse) programmatically wipe the DOM/input (`input.value = ''` or clear ProseMirror/Lexical innerHTML) upon submission without firing user `input` or `keyup` DOM events.
   - Users submit using plain `Enter` or clicking SVG/icon Send buttons (`aria-label="Send message"`), which were previously bypassed by strict textarea and text-only submit regex.
   - SPAs reuse the exact same DOM input element for consecutive messages. Because the session key map kept the old draft ID attached to the element, subsequent messages overwrote previous ones, causing race conditions between `SAVE_DRAFT` and `MARK_DRAFT_POSTED`.
2. **Failure to Detect Draft Deletions**:
   - When users selected text and hit Backspace/Delete to abandon a draft, the content script cleared its local buffer but never notified the background worker to delete the stored draft record (`DELETE_DRAFT`).

## Implemented Architecture

### 1. Unified Content Script Lifecycle (`scribe_content.js`)
- **Canonical Editable Resolution (`getEditableRoot`)**: Normalizes events from nested `<span>` or `<p>` tags up to the actual container.
- **Active DOM MutationObserver (`observeElement`)**: Watches child additions/removals and character data mutations in real-time. Programmatic wipes by website scripts immediately trigger text re-evaluation.
- **Real-Time Deletion Hook (`evaluateTextChange`)**:
  - If text drops below threshold ($<50$ chars) or is wiped completely:
    - If `submittedDrafts.has(draftId)` or within 5s of a submit trigger $\rightarrow$ `MARK_DRAFT_POSTED(draftId)`.
    - If no submit trigger occurred $\rightarrow$ `DELETE_DRAFT(draftId)` removes the draft from `chrome.storage.local`.
    - Automatically cleans `savedDraftMap` and `sessionKeyMap.delete(root)` so any new text in that box gets a fresh draft ID and never overwrites previously posted messages.
- **Universal Submit Capture**:
  - `handleKeydown`: Intercepts `Ctrl+Enter` and plain `Enter` across all inputs and comment textareas.
  - `handleSubmitClick`: Broad matching for Send/Post buttons, icons, `aria-label`, and SVG containers.
  - `handleFormSubmit`: Immediately dispatches `MARK_DRAFT_POSTED` before form submission navigation.
  - `schedulePostVerification`: Multi-stage checks (100ms, 300ms, 600ms, 1200ms, 2000ms, 3500ms) to detect asynchronous website clearing or unmounting.

### 2. Race-Condition Protection (`background.js`)
- `SAVE_DRAFT`: Guard against trailing debounced saves accidentally reverting an already posted draft back to `draft`.
- `MARK_DRAFT_POSTED`: Supports creating immediate posted entries with fallback payload if submission happened before initial debounce.

### 3. Visual Feedback
- Pinpoint indicator pinned to bottom-right of the active input:
  - Blue rotating circle while typing/saving.
  - Crisp green tick (✓) when saved or posted, with auto-fadeout.
