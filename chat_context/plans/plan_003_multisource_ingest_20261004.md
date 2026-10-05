# Plan 003 – Multi-Source Ingest (Gemini Web, Folder Archives, Live Webhook) – 2026-10-04

Historic log. Maintained alongside plan_001 and plan_002.

## Goals
1. Ingest existing multi-model chat transcripts stored in `_AI files and chat logs` (Gemini, ChatGPT, Claude).
2. Support ongoing Gemini web chats via:
   - `chat_context/inbox/` drop folder.
   - Live HTTP webhook endpoint (`POST /api/ingest/chat`).
   - Tampermonkey/Violentmonkey auto-sync userscript for `https://gemini.google.com/*`.
3. Support direct links to original web chats (`url` field) with visual source badges in the UI.

## Implementation Details
- `ctx/importers.py`:
  - `parse_gemini_markdown`: Parses `# Title \n **Link:** ... \n ## Prompt: ... \n ## Response: ...`.
  - `parse_chatgpt_text`: Parses `You said: ... \n ChatGPT said: ...`.
  - `parse_claude_text`: Parses date-stamped turn blocks (`Feb 5`, etc.).
  - `parse_gemini_copypaste`: Parses `Conversation with Gemini ... Custom Gem / Alethekanon`.
  - `parse_json_chat`: Parses arbitrary JSON exports, Takeout message arrays, and ShareGPT schemas.
- `ctx/ingest.py`:
  - `ingest_folder`: Incremental scanner tracking file `mtime`.
  - `ingest_payload`: Ingests real-time payloads from browser scripts/extensions.
  - Monitors Antigravity brain, `_AI files and chat logs`, `google_chat_log`, and `chat_context/inbox`.
- `ctx/server.py`:
  - Added `CORSMiddleware` to accept cross-origin requests from `https://gemini.google.com`.
  - Added `POST /api/ingest/chat` webhook.
  - Auto-scans all folders in the background worker loop.
- `chat_context/extension/gemini_sync_userscript.js`:
  - Tampermonkey/Violentmonkey script for `gemini.google.com`.
  - MutationObserver automatically detects completion of model responses (debounced 2.5s) and POSTs chat to local server.
  - Includes visual badge indicator and manual "Sync to Context" button.
- `ui/index.html`:
  - Color-coded source badges: `GEM` (Gemini), `GPT` (ChatGPT), `CLA` (Claude), `ANT` (Antigravity).
  - Web links: `🔗 Open on Web` button when chat URL is present.

## Ingest Results
- Total chats in SQLite: 110 (75 Antigravity, 13 Gemini, 13 ChatGPT, 9 Claude).
- Background worker actively embedding passages and re-clustering into unified semantic topics.
