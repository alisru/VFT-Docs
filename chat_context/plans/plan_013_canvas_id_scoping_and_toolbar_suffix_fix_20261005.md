# Implementation Plan 013 - Canvas ID Scoping & Toolbar "Export" Suffix Remediation

**Date**: 2026-10-05  
**Component**: `chat_context` (Extension, Userscript, Backend Ingestion, Database Schema & UI)  
**Status**: Completed & Verified  

---

## 1. Problem Diagnosis
In the server logs, the sync worker logged:
`[canvas-sync] Starting sync for: ['Domestic Oversaturation and Forced Labor Redeployment AnalysisExport', 'Workforce Deficits and Domestic Career Realignment Under Proposed Migration CutsExport']`
However, the Workforce Deficits canvas was not appearing in the chat or HTML viewer for *Debunking Authoritarian Property Investor Rants*.

### Root Causes
1. **Canvas ID Collision Across Chats**:
   - The browser extension emitted sequential generic IDs (`canvas-1`, `canvas-2`).
   - In `ctx/ingest.py`, `c_id = cv.get("id")`, so every chat ingested its first canvas under the key `canvas-1`.
   - The SQLite upsert statement used `ON CONFLICT(id) DO UPDATE SET title=..., content=...` without updating `chat_id`.
   - Consequently, `canvas-1` permanently retained the `chat_id` of the first chat that ever registered a canvas (`gemini-965a07d336ea4dda`). When *Debunking Authoritarian Property Investor Rants* (`gemini-dd82cf235ec796b0`) queried `/api/chat/`, its canvas was hidden under a different conversation.
2. **Toolbar Suffix Leaking into Canvas Titles**:
   - In Gemini's canvas toolbar, the title container element contains both the title text and adjacent buttons (such as `Export` or `Close`).
   - Extracting `.textContent` from `.title-wrapper` or `.title-container` resulted in strings like `Workforce Deficits ... CutsExport`.
   - This corrupted filenames, frontmatter, and inline marker tags.

---

## 2. Implemented Fixes

### A. Ingestion Scoping (`ctx/ingest.py`)
- Canvas IDs are now explicitly scoped to their chat:
  `c_id = f"{chat_id}-{raw_cv_id}"`
- The upsert query now explicitly updates `chat_id`:
  ```sql
  INSERT INTO canvases(id, chat_id, title, content, type, file_path, updated)
  VALUES(?,?,?,?,?,?,?)
  ON CONFLICT(id) DO UPDATE SET
      chat_id=excluded.chat_id,
      title=excluded.title,
      content=excluded.content,
      type=excluded.type,
      file_path=excluded.file_path,
      updated=excluded.updated
  ```
- Strips any trailing `Export`, `Download`, or `Close` suffixes from `c_title` before saving.

### B. Extension & Userscript Extraction (`content.js` & `gemini_sync_userscript.js`)
- `getCanvasTitleFromElement(el)` now:
  - Clones the title element and strips `button`, `[role="button"]`, and icon tags before retrieving `.textContent`.
  - Strips trailing `Export`, `Download`, or `Close` suffixes via regex: `replace(/\s*(Export|Download|Close)\s*$/i, '')`.
- Bumped Chrome extension version to `1.1.2`.

### C. Resilient UI Matching (`ui/index.html`)
- `renderMessageContent` normalizes both the inline marker title and each canvas candidate's title by stripping trailing action words before comparing, guaranteeing matches even if legacy data has minor suffix variances.

### D. Data & Database Migration (`repair_canvases.py`)
- Executed database repair across all markdown assets in `chat_context/canvases/`.
- Replaced un-scoped `canvas-N` records with clean, chat-prefixed IDs.
- Cleaned frontmatter in affected markdown files on disk.
- Cleaned message tags in `messages` table from `[[CANVAS: ...Export]]` to `[[CANVAS: ...]]`.

---

## 3. Verification & Results
- Verified `/api/chat/gemini-dd82cf235ec796b0`:
  - Returns all 4 associated canvases:
    1. `Workforce Deficits and Domestic Career Realignment Under Proposed Migration Cuts`
    2. `Domestic Oversaturation and Forced Labor Redeployment Analysis`
    3. `1. Context: Proposed Migration Contractions`
    4. `1. Executive Summary: The Arithmetic of Border Autarky`
  - Messages 6 and 8 contain clean canvas tags.
  - Both canvases render with interactive preview and copy buttons in the HTML viewer.
