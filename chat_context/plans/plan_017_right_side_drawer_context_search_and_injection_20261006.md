# Plan 017: Right-Side Context Drawer with Semantic Search, Related Chats, and One-Click Prompt Insertion & Copy

## Date: 2026-10-06

## Goal
Build a sleek, non-intrusive right-side drawer inside the Gemini web UI that:
1. Opens via the bottom-right Context pill or keyboard shortcut (`Alt + C`).
2. Automatically displays **Related Chats** to the current Gemini conversation.
3. Provides a live **Semantic Search Bar** querying the local offline vector database (`/api/search`).
4. Allows browsing **Recent Canvases** (`/api/canvases/recent`).
5. Offers both **"Insert into Prompt"** (auto-injects `<context>...</context>` into Gemini's active prompt box) and **"Copy to Clipboard"** for individual snippets and full synthesized Context Packs.

---

## Architectural Components

### 1. Backend Server Enhancements (`chat_context/ctx/server.py`)
- `POST /api/related_live`:
  - Accepts `{ chat_id?: str, url?: str, text?: str, k?: int }`.
  - Resolves chat ID from DB or URL.
  - If chat exists and has embeddings, computes cosine similarities against all chat vectors.
  - If text/query provided or chat is new, embeds `text` and performs nearest-neighbor search across chat and chunk vectors.
  - Returns top related chats with similarity score and matching excerpt snippet.
- `GET /api/canvases/recent`:
  - Returns latest 30 canvases with title, chat_id, type, updated date, and excerpt.

### 2. Chrome Extension Background Relay (`chat_context/extension/chrome_extension/background.js`)
- Add message listener handlers for:
  - `SEARCH_CHATS`: relays to `GET /api/search?q={query}&k=15`.
  - `GET_RELATED`: relays to `POST /api/related_live`.
  - `GET_PACK`: relays to `POST /api/pack`.
  - `GET_RECENT_CANVASES`: relays to `GET /api/canvases/recent`.

### 3. Extension Content Script (`chat_context/extension/chrome_extension/content.js`)
- **Drawer Component**:
  - Right-docked slide-over panel (width: 440px, height: 100vh, dark glassmorphism theme matching Gemini's palette).
  - Toggled by clicking `[ 🔍 Context ]` on the widget or pressing `Alt + C`.
  - Smooth sliding animation (`transform: translateX(...)`).
  - Search input with autofocus and 300ms debouncing.
  - Tabs: `📌 Related`, `🔎 Search`, `🎨 Canvases`.
- **Gemini Prompt Injection Engine**:
  - Targets Gemini's `rich-textarea .ql-editor`, `div[contenteditable="true"][role="textbox"]`, or `textarea[aria-label*="prompt" i]`.
  - Uses `document.execCommand('insertText', false, text)` with fallback to DOM paragraph insertion and synthetic `input`/`change` event dispatching.
  - Formats inserted context cleanly with markdown boundaries.
- **Copy Engine**:
  - Uses `navigator.clipboard.writeText` with immediate visual feedback (`✓ Copied`).

### 4. Userscript Alignment (`chat_context/extension/gemini_sync_userscript.js`)
- Mirror the drawer UI and handlers using direct `GM_xmlhttpRequest` / `fetch` so userscript environments have full parity.

---

## Verification
- Test `/api/related_live` and `/api/canvases/recent` endpoints on `127.0.0.1:8765`.
- Verify background message relay in extension.
- Verify drawer DOM creation, toggle behavior, search responsiveness, and prompt injection on Gemini HTML structure.
