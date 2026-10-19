# Plan 011: Live Dashboard Sync & Placeholder-Aware Clearing

## Critical Root Causes Discovered

1. **Stale Dashboard UI (`dashboard.js` had no storage listener)**:
   - When Auto-Scribe successfully saved or updated a draft in `chrome.storage.local`, any already-open dashboard tab never re-rendered because `dashboard.js` had zero `chrome.storage.onChanged` listeners.
   - The user looking at an open dashboard tab was seeing the initial static snapshot, which continued to display "Draft" even after background storage marked it posted.

2. **Placeholder Text Blocking the Empty-Box Check**:
   - In Gemini and Reddit, when the editor is cleared by the website upon posting, the DOM is populated with default placeholder text (e.g. `"Enter a prompt here"` [20 chars] or `"What are your thoughts?"` [23 chars]).
   - The previous condition tested `remText.length < 15`. Because 20 and 23 are $> 15$, the check falsely decided the box was still full of text.
   - `extractText` did not strip custom placeholder attributes or check against element `aria-label` / `data-placeholder`.

3. **No Real-Time Console Visibility**:
   - Auto-Scribe previously output no console logs, making it impossible to see in DevTools whether content scripts were active, when checks armed, or what character counts were returned.

## Implemented Fixes

1. **Live Real-Time Dashboard Sync (`dashboard.js`)**:
   - Added `chrome.storage.onChanged` listener targeting the `local` area.
   - Any state change in background storage instantly updates the stream, counts, badges, and active reader without requiring a manual page refresh.

2. **Placeholder-Aware & Delta Clearing Logic (`scribe_content.js`)**:
   - Updated `extractText` to filter out placeholder elements and return `""` if the text matches the placeholder or `aria-label`.
   - Updated the clearing condition to:
     `const isCleared = isUnmounted || !remText || (remText.length < config.minChars && remText !== activeEmptyCheck.text);`
   - If the text drops from the original $>50$ character draft down to 0, placeholder length, or $< 50$ chars, Auto-Scribe confirms the submission.

3. **Extended Polling Window**:
   - Extended the empty-box check window across `[60, 150, 300, 500, 800, 1200, 1800, 2600, 3800, 5000, 7000]` milliseconds to accommodate slower Gemini API turnarounds.

4. **Transparent Console Logging**:
   - Added `[Auto-Scribe]` logs for content script loading, draft saving, submit arming, and post confirmations.
