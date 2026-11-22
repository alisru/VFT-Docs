# Plan 031: Clean Sharing Architecture, Configurable Cloud Sync & Setup Wizard

**Date**: 2026-10-15  
**Status**: Completed  
**Milestone**: v1.5.1  

---

## 1. Objectives

1. **Decouple Personal Configurations from Code**:
   - Extract hardcoded Google Drive folder IDs, rclone remote names (`VFT:`), and Git remote URLs from `ctx/cloud_sync.py` into a structured, modular configuration system.
   - Maintain full backward compatibility with the current user's active setup so existing sync pipelines continue to work seamlessly.

2. **Interactive Setup Wizard (`setup_sync.py` / `python -m ctx.setup`)**:
   - Provide an automated CLI wizard that guides any new user through configuring Google Drive (via `rclone`) and Git auto-backup for canvases.
   - Test CLI availability (`git`, `rclone`, `pandoc`) and offer actionable remediation instructions if tools are missing.

3. **Shareable Templates & Privacy Safeguards**:
   - Create `config.example.json` and a project-level `chat_context/.gitignore`.
   - Prevent any accidental leaks of personal databases (`data/*.sqlite`), personal conversation transcripts, or local tokens.

4. **Documentation Updates**:
   - Update `chat_context/README.md`, `chat_context/docs/02_USER_GUIDE.md`, and `chat_context/docs/03_ARCHITECTURE_AND_HOW_IT_WORKS.md` with step-by-step setup instructions for new users sharing or cloning the project.

---

## 2. Implementation Steps

1. Create `chat_context/ctx/config.py`:
   - Load `config.json` if it exists.
   - Fall back to user's existing defaults if in the original workspace, or generic safe defaults (`enabled: false`) if unconfigured.
   - Save current user's existing settings into `chat_context/config.json`.
   - Create `chat_context/config.example.json`.
2. Refactor `chat_context/ctx/cloud_sync.py`:
   - Read settings from `ctx.config`.
   - Guard against missing `git`, `rclone`, or `pandoc` executables without throwing uncaught exceptions.
3. Build `chat_context/setup_sync.py`:
   - Interactive questionnaire for Git and Google Drive setup.
   - Performs health checks and directory initializations.
   - Supports `--status` flag with cp1252-safe ASCII output.
4. Add `chat_context/.gitignore`:
   - Ignore SQLite databases, local `config.json`, personal exports, staging caches, and virtual environments.
5. Update Documentation:
   - Detailed setup process in `02_USER_GUIDE.md`, `03_ARCHITECTURE_AND_HOW_IT_WORKS.md`, and `README.md`.

---

## 3. Verification

- Tested `python setup_sync.py --status`:
  - Verified detection of `git`, `rclone`, and `pandoc`.
  - Verified active settings read correctly from `config.json`.
- Tested `chat_context/.gitignore` rules against `git status`.
- Verified server continues to operate normally with `ctx.config` integration.

