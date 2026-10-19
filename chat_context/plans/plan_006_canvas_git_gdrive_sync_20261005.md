# Plan 006: Canvas Git & Google Drive Auto-Sync Engine
**Date**: 2026-10-05  
**Author**: Antigravity  
**Status**: In Progress  

## 1. Goal
Implement automatic, background cloud synchronization for all captured Gemini Canvases:
1. **Git Auto-Commit & Push**: Track every canvas revision in the GitHub repository (`main`) with clean commit messages and line-by-line diff history.
2. **Google Drive Sync (via `rclone`)**: Incrementally copy new/modified `.md` canvas files to the user's authenticated Google Drive remote (`VFT:Gemini Canvases`).
3. **Debounced & Non-Blocking**: Bundle rapid successive edits (30s quiet period) into a single batch commit and push, executed asynchronously so the web UI and Gemini extension experience zero latency.

## 2. Components
1. **`ctx/cloud_sync.py`**:
   - `CanvasCloudSync`: Thread-safe debounced timer that collects modified canvas titles.
   - Executes `git add`, `git commit`, `git push origin main` on `chat_context/canvases`.
   - Executes `rclone copy "chat_context/canvases" "VFT:Gemini Canvases"`.
   - Graceful fallback: handles no-change states, offline states, and logs output.
2. **Integration into `ctx/ingest.py`**:
   - Call `cloud_sync.notify_change(c_title)` whenever a canvas is written/updated.
3. **Server Endpoint (`ctx/server.py`)**:
   - Add `POST /api/sync/canvases` to allow immediate, non-debounced sync from UI.
   - Status reporting for canvas sync state.
