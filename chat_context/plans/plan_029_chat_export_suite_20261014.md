# Implementation Plan 029: Complete Export Suite for Single & All Chats

**Date**: 2026-10-14  
**Scope**: `chat_context/ctx/export.py`, `chat_context/ctx/server.py`, `chat_context/ui/index.html`, `chat_context/extension/chrome_extension/content.js`, `manifest.json`  

---

## 1. Capabilities Delivered

### A. Dedicated Export Engine (`chat_context/ctx/export.py`)
- **Single Chat Formats**:
  - **Markdown (`.md`)**: Full YAML frontmatter (`id`, `title`, `source`, `url`, `topic`, `started`, `updated`, `messages_count`, `canvases_count`), metadata header, attached canvases list, role headers with timestamps, and full preserved LaTeX/code blocks.
  - **HTML (`.html`)**: Beautiful, self-contained dark-theme document with responsive container, role badges, syntax code blocks, expandable canvas drawer, and print stylesheet (`@media print` for 1-click Save to PDF).
  - **JSON (`.json`)**: Formatted JSON structure with full metadata, messages array, and canvas documents.
  - **Plain Text (`.txt`)**: Clean text document with ascii separators, metadata header, and indexed turns.
  - **ZIP Archive (`.zip`)**: Compressed zip containing the chat markdown file plus all attached canvases in a dedicated `canvases/` subfolder.
- **Bulk / All Chats Export**:
  - **ZIP Archive**: Packages all 300+ conversations into organized topic subfolders (`Topic/Chat_Title.md`) with a `canvases/` folder and root `manifest.json` / `README.md`. Includes automated path deduplication to prevent zip collisions.
  - **JSON Bundle**: Consolidated JSON file containing all chats and their messages and canvases.
- **CLI Runner**:
  - `python -m ctx.export --all --format zip --out ./exports`
  - `python -m ctx.export --all --format json --out ./exports`
  - `python -m ctx.export --chat <chat_id> --format markdown --out ./exports`

---

### B. Server API Endpoints (`chat_context/ctx/server.py`)
- `GET /api/export/chat/{cid}?format=markdown|html|json|txt|zip`: Streams direct file download with `Content-Disposition: attachment`.
- `GET /api/export/all?format=zip|json&group_by=topic|flat&ids=id1,id2`: Streams full database or selected subset as a ZIP archive or JSON file.
- `POST /api/export/selected`: Accepts `{"ids": [...], "format": "zip"|"json"}` and returns downloadable archive.

---

### C. Web Dashboard UI (`chat_context/ui/index.html`)
- **Top Header**: "📥 Export All ▾" dropdown offering:
  - `📦 All Chats (ZIP, by Topic)`
  - `📦 All Chats (ZIP, Flat)`
  - `📄 All Chats (JSON Bundle)`
- **Active Chat View**: "Export:" chips next to topic/web actions:
  - `[Markdown]` `[HTML]` `[JSON]` `[TXT]` `[ZIP]`
- **Footer Checkbox Selection**: Dynamic "📦 Export Selected (N)" button that appears when checking boxes next to chats in the sidebar or search results.

---

### D. Chrome Extension Integration (`content.js`, `manifest.json`)
- Added **"Export"** button directly to the floating Gemini web widget.
- Added **"Dashboard ↗"** direct launch link in the Context Drawer header.
- Bumped extension version to **v1.4.4**.

---

## 2. Verification Results
- `GET /api/export/chat/gemini-424c86baff31945d?format=markdown`: 200 OK, full frontmatter and turns.
- `GET /api/export/chat/gemini-424c86baff31945d?format=html`: 200 OK, standalone HTML with dark styling.
- `GET /api/export/all?format=zip`: 200 OK, packed all 309 database chats cleanly with zero zip name collision warnings.
- Tested CLI export for single chat and bulk zip export.
