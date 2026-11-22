# Plan 026: Canonical Gemini URL & Conversation ID Deduplication

**Date:** 2026-10-14  
**Status:** Completed & Verified  

## 1. Problem Statement
The user reported duplicate entries in the drawer tree:
Two entries for `Action-Oriented Bible Translation Strategy` (one with 🎨3 and one with 🎨4), and shared two Gemini URLs for the same conversation:
1. `https://gemini.google.com/u/1/app/14015447ebaca385?utm_source=app_launcher&utm_medium=owned&utm_campaign=base_all&pageId=none`
2. `https://gemini.google.com/u/1/app/14015447ebaca385`

## 2. Root Cause Analysis
1. **Raw `window.location.href` Hashing**:
   - `content.js` previously passed `window.location.href` directly without normalization.
   - When launching Gemini from the Google app launcher, query parameters like `?utm_source=app_launcher&utm_medium=owned&utm_campaign=base_all&pageId=none` are present.
   - When navigating directly, refreshing, or opening an artifact canvas, parameters change (`&canvas-id=...` or no query parameters).
   - In multiple Google profile sessions, the pathname contains `/u/0/` or `/u/1/`.
2. **Hash-Based ID Generation**:
   - In `ctx/ingest.py`, `chat_id` was computed as `f"{source}-" + hashlib.sha1(url.encode()).hexdigest()[:16]`.
   - Different URL strings for the exact same Gemini chat generated distinct hashes (`gemini-9b340db4742f3b89`, `gemini-0705234f48b59aa3`, `gemini-8bfee0cd9c2b7148`).
   - Consequently, the chat context drawer rendered multiple rows for the same conversation, each with varying message and canvas counts.

## 3. Implemented Fixes
1. **Extension-Side URL & ID Canonicalization (`content.js` & `manifest.json`)**:
   - Implemented `normalizeGeminiUrl(rawUrl)` in `content.js`:
     - Strips all query parameters (`?...`) and hash fragments (`#...`).
     - Strips account index path routing (`/u/0/`, `/u/1/`).
     - Returns canonical URL: `https://gemini.google.com/app/{convo_id}`.
   - Extracts `convoId` and sets `id: gemini-{convoId}` directly in the sync payload.
   - Bumped extension to **v1.4.2**.
2. **Server-Side Ingestion Normalization & Legacy Deduplication (`ctx/ingest.py`)**:
   - Normalizes any raw incoming URL identically.
   - Enforces deterministic `chat_id = f"gemini-{convo_id}"` for all Gemini chats.
   - Automatically cleans up legacy hash-based duplicate rows for that conversation ID on sync:
     - Safely re-parents any associated canvases (`UPDATE OR IGNORE canvases SET chat_id=? WHERE chat_id=?`).
     - Cleans up stale duplicate messages, chunks, and chat rows.

## 4. Verification
- Ingested both dirty URL (`...14015447ebaca385?utm_source=...`) and clean URL (`...14015447ebaca385`).
- Both returned `chat_id: "gemini-14015447ebaca385"`.
- Checked SQLite database: exactly one unified chat row exists for `gemini-14015447ebaca385`.
- Verified `/api/tree`: displays only a single entry for the conversation.
