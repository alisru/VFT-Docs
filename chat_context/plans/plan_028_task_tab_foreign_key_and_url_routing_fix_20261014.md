# Implementation Plan 028: Task Tab Foreign Key Constraint & URL Routing Resolution

**Date**: 2026-10-14  
**Scope**: `chat_context/ctx/ingest.py`, `chat_context/extension/chrome_extension/content.js`, `manifest.json`  

---

## 1. Problem Diagnosis
When syncing a Gemini Scheduled Prompt / Task tab (`424c86baff31945d`):
1. **Foreign Key Violation on Legacy Migration**:
   - `ingest_payload` attempted to execute `UPDATE OR IGNORE canvases SET chat_id=? WHERE chat_id=?` before `chat_id` was inserted into the `chats` table.
   - Because `canvases` enforces `FOREIGN KEY (chat_id) REFERENCES chats(id)`, SQLite immediately aborted with `sqlite3.IntegrityError: FOREIGN KEY constraint failed`.
   - The FastAPI endpoint threw an uncaught HTTP 500 error, causing `background.js` and `content.js` to fail the sync and report `"Server offline"` / `"Server error"`.
2. **Task & Prompt URL Matching**:
   - Gemini Task run tabs and scheduled prompts can utilize paths such as `/task/` or `/tasks/` or `/prompt/`.
   - `content.js` previously only allowed `/app/`, `/share/`, and `/gem/`, ignoring other valid Gemini views.
3. **Task Tab Title Fallback**:
   - Scheduled task runs frequently contain only automated model turns (all roles are `'assistant'`). The title fallback expected a `'user'` message and would remain generic (`"Gemini"`) if none existed.

---

## 2. Solution & Architectural Fix
1. **Foreign Key Order Inversion**:
   - Collect `alias_ids` for legacy duplicate shells.
   - Gather all messages from alias shells into `existing_msgs`.
   - Merge messages non-destructively via `merge_messages`.
   - **Upsert canonical `chats` record FIRST** so `chat_id` exists in `chats`.
   - **Migrate canvases and retire alias shells SECOND**: foreign key check passes cleanly without error.
   - Insert/update all messages by index into `messages`.
2. **Support All Gemini URL Patterns**:
   - Updated `content.js` and `ingest.py` to match `/(?:app|share|task|tasks|prompt|gem\/[^/]+)\/([a-zA-Z0-9_-]+)/`.
3. **Model-Only Title Fallback**:
   - If no user prompt is present, falls back gracefully to `msgs[0].text.slice(0, 60)`.
4. **Extension Version Bump**:
   - Bumped `manifest.json` to version **1.4.3**.

---

## 3. Verification Results
- Ingestion of `gemini-424c86baff31945d` ("Fractal Polytrope transformer"): returned HTTP 200 OK (`{"ok": true, "chat_id": "gemini-424c86baff31945d"}`).
- Verified 14 messages safely stored in SQLite with zero data deletion.
- Background server daemon running healthy on port 8765.
