# Plan 016: Dedicated Canvas Repo Migration to `alisru/gemini-canvases`

## Date: 2026-10-05

## Context & Motivation
- The main workspace repository `alisru/VFT-Docs` is public.
- The user pointed out: `"oh, i just realised that vft repo is public, so lets use this new one https://github.com/alisru/gemini-canvases"`.
- Canvases generated in Gemini should not be publicly committed or tracked in `VFT-Docs`.
- Instead, `chat_context/canvases/` is now an isolated Git repository linked to `https://github.com/alisru/gemini-canvases`, while remaining dual-synced to Google Drive (`VFT:Canvases`).

---

## Actions Completed

### 1. Isolated Dedicated Repo in `chat_context/canvases/`
- Initialized a standalone git repository inside `e:\Vector Field Theory\VFT Docs\chat_context\canvases`.
- Created and switched to `main` branch.
- Added remote origin: `https://github.com/alisru/gemini-canvases.git`.
- Added all 30 clean canvas documents and committed them:
  - Commit `8a0d9fa`: `feat(canvases): initial import of 30 clean gemini canvas documents`.
- Pushed branch `main` to `https://github.com/alisru/gemini-canvases.git`.

### 2. Untracked Canvases from Public `alisru/VFT-Docs`
- Added `chat_context/canvases/` to `.gitignore` of `VFT-Docs`.
- Removed tracked files from git index: `git rm -r --cached chat_context/canvases`.
- Committed to `VFT-Docs` (`aaef8fba`: `chore(canvases): untrack chat_context/canvases/ in favor of dedicated private repo`).
- Pushed commit `aaef8fba` to `alisru/VFT-Docs` on `main`.
- Verified that `chat_context/canvases/` is completely scrubbed from `VFT-Docs` index and working tree status.

### 3. Updated Background Auto-Sync Worker (`chat_context/ctx/cloud_sync.py`)
- Changed git execution context from `cwd=REPO_ROOT` to `cwd=CANVASES_DIR`.
- Updated subprocess commands to:
  ```python
  subprocess.run(["git", "status", "--porcelain"], cwd=CANVASES_DIR, ...)
  subprocess.run(["git", "add", "."], cwd=CANVASES_DIR, ...)
  subprocess.run(["git", "commit", "-m", commit_msg], cwd=CANVASES_DIR, ...)
  subprocess.run(["git", "push", "origin", "main"], cwd=CANVASES_DIR, ...)
  ```
- Dual cloud synchronization now functions seamlessly:
  1. **Git**: commits and pushes directly to `https://github.com/alisru/gemini-canvases`.
  2. **Google Drive**: copies via rclone to `VFT:Canvases`.

### 4. Daemon Restart & Health Verification
- Stopped background daemon `task-1596`.
- Re-launched server daemon (`task-1655`) with updated sync worker.
- Verified `/api/status` is healthy on `http://127.0.0.1:8765`.
- Verified `chat_context/canvases` git status is clean and in sync with `origin/main`.
