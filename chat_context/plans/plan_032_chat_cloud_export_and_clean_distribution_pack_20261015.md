# Plan 032: On-Demand Chat Git & Drive Export and Clean Distribution Pack

**Date**: 2026-10-15  
**Status**: Completed  
**Milestone**: v1.5.2  

---

## 1. Objectives

1. **On-Demand Chat Git & Google Drive Export**:
   - Provide on-demand export of all conversations as structured Markdown files organized by topic.
   - Sync exported Markdown chats to a dedicated Git repository (`--sync-git` CLI & Web Dashboard action).
   - Sync exported Markdown chats to Google Drive via Rclone (`--sync-gdrive` CLI & Web Dashboard action).
   - Wire configuration into `ctx/config.py`, `config.example.json`, and `setup_sync.py`.

2. **Clean Standalone Distribution Pack**:
   - Create a clean distribution directory (`chat_context_clean/`) stripped of all personal data, local databases (`data/*.sqlite`), `.venv`, staging files, and personal credentials.
   - Include all core Python backend code (`ctx/`), the Chrome extension (`extension/`), the full documentation pack (`docs/`), `README.md`, `requirements.txt`, `setup_sync.py`, `config.example.json`, and `.gitignore`.
   - Generate a single, portable ZIP package (`chat_context_clean.zip`) for instant 1-click sharing.

---

## 2. Implementation Steps

1. **Backend Integration**:
   - Added `chat_git_sync` and `chat_gdrive_sync` to `ctx/config.py`.
   - Added `export_all_to_directory()`, `sync_chats_to_git()`, and `sync_chats_to_gdrive()` to `ctx/export.py`.
   - Added CLI flags `--sync-git` and `--sync-gdrive` to `cli_main()`.
2. **Dashboard & API**:
   - Added `/api/export/sync-git` and `/api/export/sync-gdrive` POST endpoints in `ctx/server.py`.
   - Added `☁️ Sync All to Google Drive` and `🐙 Push All to Git Repository` to the `Export All` dropdown in `ui/index.html` with asynchronous fetch and toast alerts.
3. **Setup Wizard Update**:
   - Updated `setup_sync.py` to prompt for Chat Git and Google Drive configurations and display them in `--status`.
4. **Clean Distribution Creation**:
   - Created clean distribution folder at `chat_context_clean/`.
   - Created standalone distribution archive at `chat_context_clean.zip` (90 KB, 26 files, 0 personal databases/logs/credentials).

---

## 3. Verification

- Verified `python -m ctx.export --help` exposes `--sync-git` and `--sync-gdrive`.
- Verified server endpoints `/api/export/sync-git` and `/api/export/sync-gdrive` are registered and running.
- Verified contents of `chat_context_clean.zip`: 26 files, strictly production source code, docs, setup wizard, requirements, and empty directory placeholders (`data/.gitkeep`, `canvases/.gitkeep`).

