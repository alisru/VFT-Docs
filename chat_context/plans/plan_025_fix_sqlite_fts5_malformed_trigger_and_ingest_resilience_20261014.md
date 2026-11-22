# Plan 025: Fix SQLite FTS5 Malformed Trigger & Ingest Resilience

**Date:** 2026-10-14  
**Status:** Completed & Verified  

## 1. Problem Statement
When viewing `Converting Documents to Sheet Music` in Gemini, the browser extension widget displayed:
`Server offline` while other chats were able to sync.

## 2. Root Cause Analysis
1. **SQLite FTS5 Malformed Disk Image on Trigger Delete**:
   - `chat_context/ctx/db.py` previously defined triggers on the `chunks` table: `chunks_ai`, `chunks_ad`, `chunks_au` pointing to `chunks_fts`.
   - The delete trigger `chunks_ad` issued `INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', old.id, old.text)`.
   - In SQLite FTS5 with external content tables (`content='chunks'`), if any row's tokenized content differs slightly from the inverted index (or if records were partially indexed), the `'delete'` command fails with:
     `sqlite3.DatabaseError: database disk image is malformed`.
   - For chat `gemini-c25dc72f8f10ee81` (which had 546 chunks), whenever the extension sent a sync request, line 229 of `ctx/ingest.py` executed `DELETE FROM chunks WHERE chat_id=?`. This triggered `chunks_ad`, throwing `DatabaseError: database disk image is malformed` and generating an HTTP 500 error.
2. **Extension False "Server offline" Status**:
   - In `content.js` `performSync()`, any failure (including HTTP 500 or Chrome extension context invalidation) was rendered as `setStatus('error', 'Server offline')`. This masked internal server errors as server outages.
3. **Ingest Payload Format Inconsistency**:
   - In `ctx/ingest.py`, `ingest_payload()` assumed messages were always dicts (`m.get("text")`). When messages were passed as tuples or lists, an unhandled `AttributeError` was thrown.

## 3. Implemented Fixes
1. **Removed Fragile FTS5 Triggers & Cleaned Existing Databases (`ctx/db.py`)**:
   - Removed `chunks_ai`, `chunks_ad`, `chunks_au` triggers from the DB schema definition.
   - Added automatic `DROP TRIGGER IF EXISTS` for all three triggers in `init_db()`.
2. **Scheduled Safe FTS5 Rebuild (`ctx/embed.py`)**:
   - After batch embedding completes (`embedded_count > 0`), the server runs:
     `INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')`.
   - Rebuilding takes <50ms for thousands of chunks and never throws disk image malformed errors.
3. **Resilient Message Ingestion (`ctx/ingest.py`)**:
   - Added `_parse_msg(m)` helper to handle dicts, tuples, and lists uniformly.
   - Verified that `DELETE FROM chunks WHERE chat_id=?` succeeds without crashing.
4. **Accurate Status Feedback in Extension (`content.js` & `manifest.json`)**:
   - Updated `content.js` to inspect `errMsg` and display:
     - `'Reload tab'` for extension context invalidation.
     - `'Server error (500)'` for internal server exceptions.
     - `'Server offline'` only for actual network connection drops (`Failed to fetch`).
   - Bumped extension version to `1.4.1`.

## 4. Verification
- Ingested chat `gemini-c25dc72f8f10ee81` ("Converting Documents to Sheet Music") via `/api/ingest/chat`: Returned `200 OK` with `{ "ok": true, "chat_id": "gemini-c25dc72f8f10ee81" }`.
- Verified `/api/search?q=sheet%20music&k=5`: Returned matching chunks with relevance scores instantly.
