# Plan 003: Storage Modes & Real-Time Offscreen Disk Sync
**Date**: 2026-10-05  
**Project**: Auto-Scribe Extension  
**Status**: Completed & Verified  

## 1. Goal
Add configurable storage modes so the user can choose:
1. **Browser Database Only** (`chrome.storage.local`) — 0 MB extra RAM, fast, internal crash-proof database.
2. **Direct Disk Folder Only** (File System Access via `chrome.offscreen`) — Writes `.md` files directly to user's PC folder (e.g. `E:\Drafts\`) in real time, bypassing browser memory.
3. **Dual Mirroring (Both)** — Saves to browser storage for instant dashboard access AND writes real `.md` files to disk simultaneously.

## 2. Architecture & Files Implemented
- **Manifest V3** (`manifest.json`): Added `"offscreen"` permission alongside `"storage"`.
- **Offscreen Worker** (`offscreen.html` & `offscreen.js`):
  - Lightweight hidden page holding the `FileSystemDirectoryHandle` from IndexedDB (`AutoScribeFolderDB`).
  - Formats Markdown files with frontmatter and writes them to `<SelectedFolder>/<site>/<slug>.md`.
  - Managed dynamically by `background.js`: only created if `saveToDisk` is active, and automatically destroyed when disabled to keep RAM at 0 MB.
- **Background Service Worker** (`background.js`):
  - Inspects `saveToBrowser` and `saveToDisk` settings on every `SAVE_DRAFT`.
  - Routes drafts to `chrome.storage.local` and/or `chrome.offscreen`.
- **Dashboard UI** (`dashboard.html` & `dashboard.js`):
  - Added checkboxes in Settings for Browser Storage vs. Real-Time Disk Sync.
  - Folder picker connects folder and triggers immediate sync.
  - Direct folder status displayed in sidebar and settings.

## 3. Verification
- All files in `auto_scribe_extension` verified.
- `chat_context` remains completely untouched.
