# Plan 030: Claude & ChatGPT Multi-Platform Support, Offline HTML Importer, and Collaborative Origins

**Date**: 2026-10-15  
**Status**: Completed  
**Milestone**: v1.5.0  

---

## 1. Objectives

1. **Multi-Platform Web Support**:
   - Add native DOM scrapers for Anthropic Claude (`claude.ai`) and OpenAI ChatGPT (`chatgpt.com`, `chat.openai.com`) to the Chrome Extension.
   - Update `manifest.json` with permissions and content script matches for Claude and ChatGPT.
   - Support universal prompt injection across Gemini, Claude, and ChatGPT input fields.

2. **Offline HTML File Ingestion**:
   - Provide an offline HTML parser in `ctx/importers.py` so saved web page dumps (`.html`) from Claude, ChatGPT, and Gemini can be ingested directly into the SQLite knowledge store without needing live web sessions.

3. **Backend Canonical Ingestion**:
   - Update `ctx/ingest.py` to recognize `claude.ai/chat/{id}` and `chatgpt.com/c/{id}` URLs and generate clean canonical IDs (`claude-{id}` and `chatgpt-{id}`).

4. **Comprehensive Documentation Pack**:
   - Create a clean 5-part documentation pack in `chat_context/docs/` (`00_INDEX.md`, `01_OVERVIEW_AND_FEATURES.md`, `02_USER_GUIDE.md`, `03_HOW_IT_WORKS.md`, `04_HOW_IT_WAS_MADE.md`).
   - Create the project `README.md`.
   - Explicitly document the role of the AI co-creator (**Antigravity**, Google DeepMind agentic AI assistant) and the collaborative human-AI pair programming architecture.

---

## 2. Changes Made

### A. Chrome Extension (v1.5.0)
- **`extension/chrome_extension/manifest.json`**:
  - Bumped version to `1.5.0`.
  - Added matches and host permissions:
    - `https://chatgpt.com/*`
    - `https://chat.openai.com/*`
    - `https://claude.ai/*`
- **`extension/chrome_extension/content.js`**:
  - Added `extractClaudeChat()`:
    - Queries `div[data-testid="transcript-row"]`.
    - Extracts assistant messages from `[data-testid="assistant-message"]` or `.font-claude-message`, stripping `Claude responded: ` and trailing UI controls.
    - Extracts user messages from `[data-testid="user-message"]` or `.cds-user-message-body`, stripping `You said: ` and timestamps.
  - Added `extractChatGPTChat()`:
    - Queries `[data-chatgpt-search-unit-key]` distinguishing `fallback-turn-*:*:user` vs `assistant`.
    - Fallbacks for `[data-user-message-bubble="true"]` and `[data-message-author-role]`.
    - Strips `ChatGPT said:` and trailing action toolbars.
  - Dynamically routes in `extractChatPayload()` using `window.location.hostname`.
  - Updated floating export buttons and prompt injection to handle input nodes on all 3 platforms.

### B. Backend Canonical URLs (`ctx/ingest.py`)
- Added pattern matchers:
  - Claude: `re.search(r"claude\.ai/chat/([a-zA-Z0-9_-]+)", url)` -> `claude-{convo_id}`
  - ChatGPT: `re.search(r"chat(?:gpt)?\.(?:com|openai\.com)/(?:c/)?([a-zA-Z0-9_-]+)", url)` -> `chatgpt-{convo_id}`

### C. Offline HTML Ingestion (`ctx/importers.py`)
- Created `parse_html_chat(text, filename)`:
  - Uses BeautifulSoup to detect platform type based on DOM markers.
  - Claude: parses `[data-testid="transcript-row"]`.
  - ChatGPT: parses `[data-chatgpt-search-unit-key]` and role wrappers.
  - Gemini: parses `<user-query>` and `<model-response>`.
  - Ingests seamlessly through `parse_chat_file()`.

### D. Documentation & Collaborative Origins
- Created:
  - `chat_context/README.md`
  - `chat_context/docs/00_INDEX.md`
  - `chat_context/docs/01_OVERVIEW_AND_FEATURES.md`
  - `chat_context/docs/02_USER_GUIDE.md`
  - `chat_context/docs/03_HOW_IT_WORKS.md`
  - `chat_context/docs/04_HOW_IT_WAS_MADE.md`
- Added dedicated section **"The Human & Antigravity Collaborative Architecture"** highlighting:
  - Human leadership: vision, operational edge-case stress testing, domain truth.
  - Antigravity agentic execution: DOM reverse-engineering, SQLite B-tree freelist recovery, CSP bypass, deterministic foreign key repair, full export suite.
  - Invariant rules: no data loss, simplest path first, local-first intelligence.

---

## 3. Verification & Results

- Tested offline DOM extraction against:
  - `chat_context/html base/Test - Claude.html`: 2 turns parsed with 100% precision.
  - `chat_context/html base/gpttest.html`: 2 turns parsed with 100% precision.
- Server running healthy on `http://127.0.0.1:8765`.
- Extension v1.5.0 ready to be reloaded in Chrome (`chrome://extensions`).
