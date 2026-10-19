# Plan 019: Native Google Docs Sync for Drive + Pure Markdown for Git

## Date: 2026-10-06

## Goal
Implement dual storage sync:
1. **GitHub (`alisru/gemini-canvases`)**: Receives clean, version-controlled `.md` Markdown files.
2. **Google Drive (`VFT:Canvases`)**: Receives native **Google Docs** (converted via pandoc DOCX import), enabling full rich-text reading and editing on web and mobile with clean titles (no `.md` extension).

---

## Architecture & Workflow

### 1. Local Filesystem (Ground Truth)
- Stored as Markdown files in `chat_context/canvases/<Chat Folder>/<Canvas Title>.md`.
- Maintains YAML frontmatter metadata, KaTeX formulas, and Markdown tables.

### 2. Git Sync (`alisru/gemini-canvases`)
- Executed directly inside `chat_context/canvases/` via `git add .`, `git commit -m ...`, `git push origin main`.
- Pushes pure `.md` files to the dedicated repository.

### 3. Google Drive Sync (`VFT:Canvases`)
- Uses `pandoc` to convert each updated `.md` file into a formatted `.docx` document in `chat_context/drawing_board/gdocs_staging/<Chat Folder>/<Canvas Title>.docx`.
- Runs `rclone copy` with:
  - `--drive-import-formats docx`
  - `--drive-allow-import-name-change`
  - `--tpslimit 3`
- Google Drive imports the `.docx` and creates/updates a native **Google Doc**.
- Result in Google Drive: A native, rich-text editable Google Doc with headings, tables, and bullet formatting, displayed with the blue Docs icon and clean title (no `.md`).

---

## Next Steps
1. Update `chat_context/ctx/cloud_sync.py` to add the pandoc staging conversion and rclone Google Docs import flags.
2. Restart the background server daemon.
3. Test a live sync on a canvas.
4. Present the list of old raw `.md` files in Google Drive for user confirmation to clean up.
