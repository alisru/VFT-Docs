# Implementation Plan 012 - Inline Canvas Chat Linking & Interactive In-Flow Cards

**Date**: 2026-10-05  
**Component**: `chat_context` (Extension, Userscript, Server & Web UI)  
**Status**: Completed & Verified  

---

## 1. Problem Statement
When Gemini generates an inline canvas (via `<immersive-entry-chip>` or inline editor), it appears at a specific chronological point within the conversation turn (between introductory setup text and concluding explanatory text).
Previously:
1. The canvas text was stripped or dumped raw into the chat bubble text.
2. When isolated into standalone canvas files, the chat bubble had the canvas text completely removed with no inline reference, leaving a disconnect where the user couldn't see where the canvas was generated.
3. The user requested: *"pls link in the canvases where they appear in chat"*.

---

## 2. Architecture & Design

### A. Inline DOM Extraction & Marker Placement
In `chat_context/extension/chrome_extension/content.js` and `chat_context/extension/gemini_sync_userscript.js`:
- In `extractChatMessageMarkdown(element)`:
  - Finds all top-level canvas containers (`immersive-entry-chip`, `immersive-editor`, `inline-preview`, `[data-test-id*="immersive"]`, `[data-test-id*="canvas"]`, `.immersive-container`, `.canvas-container`).
  - Extracts the exact canvas title using `getCanvasTitleFromElement(el)`.
  - Replaces each top-level canvas element in the DOM clone with:
    `\n\n[[CANVAS: ${title}]]\n\n`
  - Replaced elements are excluded from leaking markdown into the chat message while anchoring the exact insertion location.

### B. Interactive Inline Canvas Card Rendering
In `chat_context/ui/index.html`:
- Added `renderCanvasCard(cv)`:
  - Renders a styled, non-intrusive container (`div.canvas-card`) inside the message bubble.
  - Header: 🎨 Canvas Icon, Title, and Badge (`MARKDOWN` or `CODE`).
  - Actions:
    - `📋 Copy Markdown`: One-click copy of the raw markdown/code with copied feedback state.
    - `👁️ Preview`: Toggleable `<pre>` block expanding the full canvas text in place without leaving the chat.
    - `📁 File`: Path display to the local synced asset.
- Added `renderMessageContent(text, canvases, referencedSet)`:
  - Uses regex `/\[\[CANVAS:\s*([^\]]+)\]\]/g` to split the message text.
  - Pairs each marker with its corresponding canvas object from `c.canvases`.
  - Inserts the rich interactive canvas card right between surrounding chat paragraphs.

### C. Canvas Navigation Bar & Legacy Fallback
In `openChat(id)` in `chat_context/ui/index.html`:
- Top Header Bar: `🎨 Canvases (N)` with clickable pills for each canvas:
  - If a canvas is rendered inline in the chat, its pill has a down arrow `[Title ↓]`. Clicking it smoothly scrolls the chat viewport directly to the inline canvas card and pulses a cyan highlight ring.
  - If a canvas was not referenced inline (e.g. legacy chats imported prior to marker insertion), its full card is rendered in the top drawer as a fallback so no canvas is ever lost.

### D. Data Remediation for "Genie Binding"
- Remediated message 1 of `gemini-4e95e5ac9ec7cf48` ("Philosophical Stress Test for Genie Binding - Google Gemini"):
  - Inserted `[[CANVAS: The Genie Binding Dilemma & The Hegemonikon]]` between the introductory paragraph and the cybernetic ethics analysis.
  - Tested and verified via `/api/chat/gemini-4e95e5ac9ec7cf48`.

---

## 3. Verification & Results
1. **API Verification**:
   - `http://127.0.0.1:8765/api/chat/gemini-4e95e5ac9ec7cf48` returns 1 canvas (`The Genie Binding Dilemma & The Hegemonikon`) and `[[CANVAS:...]]` in `messages[1].text`.
2. **UI Verification**:
   - Inline card renders in message 1 with Copy and Preview buttons.
   - Top canvas header displays `The Genie Binding Dilemma & The Hegemonikon ↓` with smooth scroll anchor.
3. **Extension & Userscript**:
   - Updated `content.js` and `gemini_sync_userscript.js` with inline marker substitution.
   - Bumped extension version to `1.1.1` in `manifest.json`.
