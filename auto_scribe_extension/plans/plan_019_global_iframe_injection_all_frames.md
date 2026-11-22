# Plan 019: Global iframe Injection (`all_frames`) for Embedded Textboxes

## Context & Problem Statement
The user asked: "is it not recording on every site's text boxes?"
Inspection of `manifest.json` revealed:
`content_scripts` had:
```json
"content_scripts": [
  {
    "matches": ["<all_urls>"],
    "js": ["scribe_content.js"],
    "run_at": "document_idle"
  }
]
```
Crucially, `"all_frames": true` was missing.

Many modern web apps, forums, comment widgets, and editors (such as Disqus, Zendesk, Salesforce, Substack comments, TinyMCE, iframe-based rich-text editors, embedded support widgets, embedded forms, Google Docs/Sheets widgets, and payment/login-adjacent portals) run inside `<iframe>` elements.
Without `"all_frames": true`, Chrome only injects `scribe_content.js` into the top-level window. Any text typed inside an iframe was completely invisible to Auto-Scribe.

## Proposed Modifications

### 1. `manifest.json`
- Add `"all_frames": true` to `content_scripts`.
- This ensures `scribe_content.js` runs across all subframes and embedded editors on all domains.

### 2. `scribe_content.js`
- Ensure `window.location.hostname` properly captures parent frame context or fallback if running in a frame, and doesn't break.
- Verify `isSensitiveElement` still guards passwords, card numbers, and pins.

## Verification
- Validate JSON syntax of `manifest.json`.
- Validate JS syntax with `node -c`.
