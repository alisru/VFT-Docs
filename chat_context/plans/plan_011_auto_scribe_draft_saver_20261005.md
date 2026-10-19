# Plan 011: Crash-Proof Auto-Scribe & Draft Recovery Extension
**Date**: 2026-10-05  
**Author**: Antigravity  
**Status**: Completed & Verified  

## 1. Goal & Requirements
1. **Crash-Proof Unposted Draft Saver**: Capture unsent text across Reddit, Facebook, Twitter/X, and any site with rich-text (`contenteditable`, Lexical, ProseMirror, Draft.js) or standard `<textarea>`/`<input>`.
2. **Configurable Meaningful Threshold (`> n` chars)**:
   - Filter out web junk (search bars, usernames, captchas, 1-word inputs).
   - Only save text when character length exceeds a user-configurable threshold `n` (default: 50 characters).
3. **High-Craft Extension Dashboard**:
   - Fix the atrocious, cluttered UX of legacy form recovery extensions (like Typio).
   - Group entries cleanly by site (e.g. `reddit.com`, `facebook.com`, `x.com`).
   - Clean 3-column studio layout: Sites Filter & Search -> Drafts Timeline Stream -> Full Reading & Export Pane.
   - 1-click clipboard copy, markdown export, and draft deletion.
4. **Dual Persistence (Browser Local + Local Disk/Markdown)**:
   - Browser `chrome.storage.local` ensures 100% functionality even when offline or without backend.
   - Pings local server `http://127.0.0.1:8765/api/drafts` to automatically write `.md` files to `chat_context/drafts/{site}/` for permanent hard-drive safety.
5. **Integrated Web UI**:
   - Serve `/scribe` on `http://127.0.0.1:8765/scribe` and add a link in `chat_context/ui/index.html`.

## 2. Architecture & Files Implemented
- `chat_context/extension/chrome_extension/`:
  - `manifest.json`: Upgraded to v1.1.0 with `<all_urls>` host permissions, `scribe_content.js` content script, popup action, and `dashboard.html` options page.
  - `scribe_content.js`: Real-time input/contenteditable monitor, clean text extraction (cleans zero-width spaces, Lexical cursors, ProseMirror tags), debounced auto-save (1500ms), threshold filtering (`minChars`), in-page quick recovery drawer and pill badge.
  - `background.js`: Relay server, storage management (`chrome.storage.local`), CSP bypass, message router for `SAVE_DRAFT`, `GET_DRAFTS`, `DELETE_DRAFT`, `GET_SETTINGS`, `SAVE_SETTINGS`.
  - `popup.html` & `popup.js`: Quick extension toolbar widget displaying active monitoring status, saved draft count, monitored site count, recent drafts with 1-click copy, and "Open Scribe Dashboard" link.
  - `dashboard.html`, `dashboard.css`, `dashboard.js`: The dedicated Auto-Scribe Notebook dashboard with 3-pane layout (Sites Sidebar, Drafts Timeline Stream, Reader/Export Pane), settings modal with configurable threshold presets, and JSON export.
- `chat_context/ctx/`:
  - `db.py`: `drafts` table schema + `chat_context/drafts` directory setup.
  - `server.py`: `/api/drafts` POST, GET, DELETE endpoints + `/scribe` redirect to `/extension/dashboard.html`.
- `chat_context/ui/`:
  - `index.html`: Header link to `✍️ Scribe Drafts`.

## 3. Verification Completed
- `db.py`: Verified `init_db()` creates `drafts` table with `['id', 'site', 'url', 'page_title', 'context_title', 'text', 'char_count', 'word_count', 'created_at', 'updated_at', 'file_path']`.
- `server.py`: Verified FastAPI server loads 21 routes cleanly.
- End-to-end saving tested: Saved sample drafts for both `reddit.com` and `facebook.com`.
- Markdown generation tested: Verified `.md` files created in `chat_context/drafts/reddit.com/` and `chat_context/drafts/facebook.com/` with frontmatter and full text.
- Tested `list_drafts()` returning aggregate site counts `{'facebook.com': 1, 'reddit.com': 1}`.
