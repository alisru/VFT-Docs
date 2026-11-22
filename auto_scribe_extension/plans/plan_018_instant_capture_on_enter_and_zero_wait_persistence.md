# Plan 018: Instant Capture on Enter/Submit & Zero-Wait Debounce Discard Prevention

## Context & Problem Statement
The user reported that the majority of what they type has not been recorded, asking:
"wtaf has happened here? has a majorty of my typings just vanished? why are the majority of the shit i say not FUCKING NOT BEING RECOREDEd? WHAT is it that i have to fkn wait for the tick to load before posting for it to record the post? what!"

The user's intuition was 100% accurate.

## Root Causes Discovered
1. **The 1500ms Tick Barrier**:
   - `evaluateTextChange` put saving behind a 1500ms `debounceTimer`.
   - When a user finished typing a prompt and pressed Enter or clicked Submit quickly (e.g. 500ms after typing the last character), `persistDraft` had NOT run yet.
   - When the site accepted the prompt and cleared the input box, `evaluateTextChange` was called with `text = ""`.
   - It executed `clearTimeout(debounceTimer)` (killing the pending save).
   - Because `savedDraftMap.get(root)` was still empty, it discarded the typed text into the void!
2. **`[role="document"]` in `isCanvasOrDocEditor` Broke Gemini**:
   - Google Gemini's workspace uses `role="document"` on its main container.
   - Because `isCanvasOrDocEditor` used `[role="document"]`, it treated Gemini's active prompt textbox as a canvas!
   - This caused `keydown` on Enter to `return` immediately without calling `triggerPotentialSubmit`!
3. **Delayed Flushes**:
   - `triggerPotentialSubmit` did not immediately flush and persist the text; it waited for an async timer chain. If the box cleared before or during unmount, the text was lost if not already in storage.

## Proposed Modifications

### 1. `scribe_content.js`
- **Instant Working Memory (`currentWorkingTextMap`)**:
  - Keep the latest text in `currentWorkingTextMap.set(root, text)` synchronously on every input event.
- **Instant Flush on Submit & Enter**:
  - In `triggerPotentialSubmit`, immediately call `persistDraft(target, currentText)` without waiting for any debounce timer.
  - When Enter is pressed or Submit button is clicked, text is guaranteed to be saved instantly.
- **Rescue on Box Clearance**:
  - If a box empties and `currentWorkingTextMap` had meaningful text, preserve and mark that text as `POSTED` if a submit occurred, even if the debounce timer had not yet fired.
- **Surgical `isCanvasOrDocEditor`**:
  - Explicitly exempt all `textarea`, `input`, and `[role="textbox"]` elements (like Gemini's `rich-textarea` and ChatGPT's `#prompt-textarea`).
  - Remove `[role="document"]` and `[aria-label*="document"]` entirely.
  - Only match dedicated canvas/code side-panels (`[class*="canvas-editor"]`, `CodeMirror`, `monaco-editor`).
- **Debounce Optimization**:
  - Reduce default debounce to 800ms while casually typing, with 0ms (instant) on Enter, click, blur, or submit.

### 2. `background.js`
- Adjust `minChars` default to `30` (from 50) so concise prompts (30-49 chars) are not discarded.

## Verification
- Validate JS syntax with `node -c`.
- Verify Enter key triggers instant flush on Gemini, Reddit, and ChatGPT.
