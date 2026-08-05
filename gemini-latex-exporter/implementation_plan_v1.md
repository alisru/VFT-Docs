# Implementation Plan - Gemini LaTeX Exporter Chrome Extension (v1)

## Goal
Create a lightweight, robust Manifest V3 Google Chrome Extension that adds an **"Export to Docs (Clean LaTeX)"** option to the Gemini web interface (`gemini.google.com`). 

When clicked:
1. It parses the selected response, extracting the original LaTeX code from the KaTeX DOM elements.
2. It replaces the complex KaTeX DOM markup with clean plain text delimiters:
   - Inline equations: `\( ... \)` or `$ ... $`
   - Block display equations: `$$\n ... \n$$`
3. It copies the resulting styled HTML (and plain text) to the clipboard.
4. It opens a new Google Doc (`https://docs.new`).
5. On the new Google Doc, the extension displays a beautiful, modern banner instructing the user to paste their content (using `Ctrl+V` or `Cmd+V`), and attempts an automatic paste event.

---

## User Review Required

> [!IMPORTANT]
> **Authentication & Permissions:**
> - To avoid the complex overhead of registering OAuth2 credentials (which requires Google Cloud Console setup for each developer/user), we use a **Clipboard-based transfer workflow**.
> - The extension will ask for `"clipboardWrite"` permissions.
> - This is 100% local, runs client-side, has no server dependencies, no API quotas, and works seamlessly with the user's existing Google Docs browser session.

---

## Proposed Files and Architecture

We will organize the extension code under:
`e:\Vector Field Theory\VFT Docs\gemini-latex-exporter/`

### 1. [manifest.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/manifest.json) [NEW]
Defines metadata, Manifest Version 3, permissions, content scripts for Gemini and Google Docs, and web accessibility resources.

### 2. [content_gemini.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/content_gemini.js) [NEW]
Runs on `https://gemini.google.com/*`:
- Listens to clicks on "Share & export" buttons.
- Uses a `MutationObserver` to watch for the appearance of the popup share menu.
- Dynamically injects an "Export to Docs (Clean TeX)" option below "Export to Docs".
- When clicked, targets the `<message-content>` element of the last active response, extracts and cleans the LaTeX from KaTeX spans, writes the rich HTML/text to the clipboard, sets a state flag in `chrome.storage.local`, and opens `https://docs.new`.

### 3. [content_docs.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/content_docs.js) [NEW]
Runs on `https://docs.google.com/document/*`:
- Checks `chrome.storage.local` for the `pendingPaste` flag.
- If present, immediately clears the flag to prevent duplicate paste actions.
- Renders a floating banner informing the user: "📋 **LaTeX Export Ready!** Press **Ctrl+V** (or **Cmd+V**) to paste."
- Attempts to dispatch a synthetic paste event to automate the insert.

### 4. [style.css](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/style.css) [NEW]
Injected stylesheet containing:
- Hover and style rules for the injected menu item in Gemini.
- Premium aesthetics (glassmorphism, subtle animations, transitions) for the floating instructions banner in Google Docs.

---

## Verification Plan

### Manual Verification
1. Load the extension in developer mode:
   - Open `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select `e:\Vector Field Theory\VFT Docs\gemini-latex-exporter`
2. Go to `https://gemini.google.com` and ask a question containing LaTeX:
   - e.g. "Write down Euler's formula and explain it with inline and display math."
3. Hover/Click the share button, verify that "Export to Docs (Clean TeX)" appears.
4. Click it, verify that it opens a new tab with a Google Doc, shows our elegant banner, and that pasting (either auto or manual) populates the document with clean formatting and text LaTeX instead of an image.
