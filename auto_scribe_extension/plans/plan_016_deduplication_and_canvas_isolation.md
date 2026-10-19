# Plan 016: Storage Content Deduplication, Canvas Protection, and Redundant Entry Cleanup

## Context & Problem Statement
The user reported:
1. Auto-Scribe is capturing ChatGPT and Gemini Canvases. While capturing canvases is valuable, identical canvas content was duplicated 3×, 4×, and up to 13× in storage (e.g., 22,221 chars duplicated 4 times on ChatGPT, and 2,186 chars / 5,875 chars duplicated 3 times each on Gemini).
2. Existing duplicates from previous sessions are cluttering the dashboard.
3. The user notes: "I don't think it'd be possible to avoid this without banning canvases from being captured which defeats purposes, i think we can avoid duplications tho".

## Root Causes Identified
1. **Random Session IDs**: `getSessionId(el)` minted `draft_${host}_${path}_${rand}` with `Math.random()`. Whenever a SPA (React/Next.js in ChatGPT/Gemini) remounted the DOM element or the user refreshed/re-opened the canvas, a new random ID was generated for identical text.
2. **Blind Insert in `background.js`**: `SAVE_DRAFT` keyed storage strictly by `payload.id`. It performed zero content deduplication to check if an existing draft on the same page/site already had identical text.
3. **Spurious Submit Triggers on Canvas**: Pressing `Enter` anywhere on the document triggered `triggerPotentialSubmit` on `lastActiveElement`. In document editors and canvases, `Enter` is merely a newline/paragraph break. When the canvas was closed or switched, it was falsely marked as `POSTED`, leading to multiple posted duplicates across sessions.

## Proposed Modifications

### 1. `background.js` Content Deduplication & Retroactive Merging
- **In `SAVE_DRAFT`**:
  - Before inserting a new draft entry, inspect existing drafts for the same URL / site.
  - If an existing draft has identical normalized text (`d.text.trim() === payload.text.trim()`), update that existing draft (`targetId = d.id`) instead of creating a new duplicate.
  - Return `{ success: true, id: targetId }` so the content script locks onto the canonical ID.
- **In `deduplicateDrafts(draftsDict)`**:
  - Group drafts by `(site + canonical URL + normalized text)`.
  - Retain the latest canonical entry, preserving `status: 'posted'` if any duplicate was posted.
  - Remove redundant duplicate keys from storage.
- **Auto-Deduplicate on Startup & New `DEDUPLICATE_DRAFTS` Action**:
  - Run deduplication on startup.
  - Add message action `DEDUPLICATE_DRAFTS` for manual triggering from the dashboard.

### 2. `scribe_content.js` Protection & Stable ID
- When `SAVE_DRAFT` completes, bind `sessionKeyMap.set(el, res.id)` to use the background's canonical ID.
- **Enter Key Filtering**:
  - Discard Enter events in canvas / rich document editors (`.canvas`, `[data-testid*="canvas"]`, `[class*="canvas" i]`, CodeMirror). In document editors, Enter is a newline, not a post submission.
  - Only arm submit checks on Enter if the target is an actual chat/message input or Ctrl+Enter is used.
- Ensure `triggerPotentialSubmit` only evaluates the element where the submit action actually occurred.

### 3. `dashboard.html` & `dashboard.js`
- Add a "🧹 Clean Duplicates" button in the dashboard top navigation bar.
- Clicking the button calls `DEDUPLICATE_DRAFTS`, removes all existing duplicate copies from storage, and refreshes the stream and counters with a friendly toast/notification.

## Verification
- Validate JS syntax with `node -c`.
- Verify deduplication logic handles identical and whitespace-normalized text properly.
