# Plan 021: Fix 30-Char Freezing Loop in WYSIWYG Iframes

## Context & Problem Statement
The user reported: "it types 30char then freezes" on the CKEditor form.

## Root Cause Analysis
At exactly 30 characters (`config.minChars`), `text.length >= 30` becomes true for the first time:
```javascript
if (text.length >= config.minChars) {
  currentWorkingTextMap.set(root, text);
  updateIndicator('saving', root);  // <--- THE CAUSE
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    persistDraft(root, text);
  }, config.debounceMs || 800);
}
```
Inside `updateIndicator('saving', root)`:
1. `ensureIndicator()` executes:
   `(document.body || document.documentElement).appendChild(el);`
2. When the user is typing inside an iframe, `root` is inside the iframe's document (`frameDoc.body`).
   Appending the indicator to `document.body` of the iframe creates a DOM mutation inside the iframe.
3. Simultaneously:
   - `observeElement(root)` has a `MutationObserver` on `root` (`childList: true, subtree: true`).
   - The outer page has `wysiwygObserver` watching `{ childList: true, subtree: true }`.
4. When `appendChild(el)` executes, the `MutationObserver` triggers `evaluateTextChange` synchronously on every character/microtask.
5. In an iframe with `height: 100px`, `positionIndicator` checks bounds or triggers reflow/mutation, which triggers `observeElement`, calling `evaluateTextChange` infinitely in a synchronous feedback loop. The browser main thread freezes completely.
6. Moreover, an in-input floating widget inside an iframe editor can disrupt CKEditor's internal selection/caret management.

## Solution

### 1. Guard `updateIndicator` in Iframes
If `window !== window.top` or the target is inside an iframe document, do NOT append indicator elements into the iframe's DOM tree.
The floating status indicator is only intended for the top-level main page.

### 2. Disconnect Observer Before Updating Indicator
Ensure `activeObserver` ignores our own `__auto_scribe_field_indicator` elements, and ignore mutations originating from indicator creation.

### 3. Infinite Loop Prevention
In `observeElement`:
Filter mutation records so that if the only added or removed nodes are `__auto_scribe_field_indicator`, ignore the mutation.

## Verification
- Run `node -c` on all JS files.
- Verify no DOM element is inserted into editable bodies or iframes.
