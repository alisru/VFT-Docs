# Plan 005: Gemini Canvas Capture & File Storage Architecture
**Date**: 2026-10-05  
**Author**: Antigravity  
**Status**: Completed  

## 1. Goal
1. Automatically capture Gemini Canvas / Artifact contents whenever a user creates or iterates on a canvas in Gemini Web.
2. Store each canvas as a dedicated Markdown (`.md`) file inside a chat-specific folder:
   `chat_context/canvases/<safe_chat_title_or_id>/<canvas_title>.md`
3. Automatically update these `.md` files whenever new revisions of the canvas are synced.
4. Index and track canvases in SQLite (`canvases` table) with timestamps and file paths.
5. Render canvases in the dashboard UI (`ui/index.html`) with previews and quick access.
6. Concurrently audit and fix memory leaks across the background sync worker, SQLite connection handling, FastEmbed ONNX runtime, and browser extension DOM observer.

## 2. Technical Architecture
### A. Chrome Extension (`extension/chrome_extension/content.js`)
- Add `extractCanvases()` targeting:
  - Open canvas pane / side-by-side surface:
    - Containers: `[data-test-id*="canvas" i]`, `immersive-panel`, `[aria-label*="Canvas" i]`, `.canvas-surface`, `.code-artifact`, `.document-artifact`
    - Titles: `[data-test-id="canvas-title"]`, `.canvas-title`, `.immersive-title`, `input.title-input`
    - Content: CodeMirror (`.cm-content`), Monaco (`.monaco-editor`), ProseMirror / TipTap (`.ProseMirror`, `[contenteditable="true"]`), markdown pre/code blocks.
  - In-line canvas chips / cards in conversation history.
- Include `canvases: [{ id, title, content, type, updated }]` in the payload sent to `/api/ingest/payload`.

### B. Database Schema (`ctx/db.py`)
- Add `canvases` table:
  ```sql
  CREATE TABLE IF NOT EXISTS canvases (
      id TEXT PRIMARY KEY,
      chat_id TEXT NOT NULL,
      title TEXT NOT NULL,
      content TEXT NOT NULL,
      type TEXT,
      file_path TEXT,
      updated TEXT NOT NULL,
      FOREIGN KEY(chat_id) REFERENCES chats(id) ON DELETE CASCADE
  );
  CREATE INDEX IF NOT EXISTS idx_canvases_chat ON canvases(chat_id);
  ```

### C. Ingestion & File Storage (`ctx/ingest.py`)
- Define `CANVASES_DIR = ROOT / "canvases"`.
- When `payload` has `canvases`:
  - Sanitize chat title and canvas title for filenames: `<CANVASES_DIR>/<chat_folder>/<canvas_name>.md`.
  - Write or update markdown with YAML metadata header.
  - Upsert into `canvases` table.

### D. Dashboard UI (`ui/index.html`)
- Display canvas count badge and expandable drawer/panel in the reader pane.
- Clickable link or copy action for canvas contents.

## 3. Dynamic Sync & Real-Time Revision Architecture
User reported that chats were no longer dynamically adding/updating automatically. Two root causes were identified and fixed:
1. **Extension Auto-Triggers (`content.js`)**:
   - Added SPA URL watcher polling `location.href` every 1s: detects switching conversations in Gemini's sidebar and resets hash to sync the newly selected chat immediately.
   - Added `characterData: true` to `MutationObserver`: catches streaming text and inline Canvas edits.
   - Added automatic sync 2s after initial page load without requiring manual button clicks.
   - Wrapped extractors in `try...catch` guards to prevent DOM query errors from blocking chat sync.
2. **Real-time Revision Tracking (`server.py` & `ui/index.html`)**:
   - Added monotonically increasing `STATUS["rev"]` counter.
   - Increments whenever a chat is ingested (`/api/ingest/chat`), canvases are updated, or background embedding completes.
   - Dashboard UI polls `s.rev !== lastRev`: instantly reloads the sidebar list and updates the active chat in the reader pane in real-time.
