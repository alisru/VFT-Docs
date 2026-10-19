# Plan 001: Auto-Scribe Extension — Scope & Storage Architecture
**Date**: 2026-10-05  
**Project**: Auto-Scribe Extension  
**Status**: Proposal / Review  

## 1. Project Goal
Build a lightweight, crash-proof Chrome extension that acts as an **Authoring Scribe**:
- Automatically records unposted drafts (Reddit comments, Facebook posts, forum entries, etc.).
- Filters out 99% of web junk by only capturing text longer than **n characters** (configurable, e.g. 50+ chars).
- Provides a clean, modern dashboard to view, search, and copy text **grouped by site**.

---

## 2. Storage Location Options

Users can choose where their drafts live directly in the dashboard settings:

### Option 1: Built-in Browser Database (`chrome.storage.local` / IndexedDB) [Default]
- **How it works**: Uses Chrome's native persistent storage allocated to the extension.
- **Pros**: Zero setup, works instantly upon installation, survives Chrome restarts, tab crashes, and OS reboots. Completely isolated and secure.
- **Cons**: Drafts live inside Chrome's data store (accessible through the extension dashboard) rather than as visible text files in Windows Explorer.

### Option 2: Direct Local Disk Folder (Native File System Access API) [Recommended for Disk Files]
- **How it works**: In dashboard settings, user clicks **"Choose Folder"** once and selects any directory on their PC (e.g., `E:\MyDrafts\`).
- **Pros**:
  - **Zero background servers or Python required.**
  - Writes actual `.md` files organized by site directly:
    `E:\MyDrafts\reddit.com\discussion_title.md`
    `E:\MyDrafts\facebook.com\group_post.md`
  - Fully visible and editable in Windows Explorer, VS Code, Obsidian, etc.
- **Cons**: User must grant one-time directory permission via the browser prompt.

### Option 3: Optional Local HTTP Server Sync [Advanced Hook]
- **How it works**: For power users who already run a local HTTP endpoint (e.g. `http://127.0.0.1:8765/api/drafts`), the extension can POST drafts in JSON format on every snapshot.
- **Pros**: Integrates with custom local Python/Node backends or databases.
- **Cons**: Requires keeping an external process running.

### Option 4: On-Demand Archive Export
- **How it works**: Buttons in the dashboard:
  - **"Export JSON"**: Single file containing all historical drafts.
  - **"Export Markdown (.zip)"**: Zipped collection of Markdown files sorted by site.
- **Pros**: No continuous permissions needed; export whenever desired.

---

## 3. Core Mechanics

### A. The Input Interceptor (`scribe_content.js`)
- **Universal Capture**: Attaches a single global `input` listener to `document`.
- **Text Retrieval**:
  - Standard `<textarea>` / `<input>`: reads `element.value`.
  - Rich-text / `[contenteditable="true"]`: reads `element.innerText`.
- **Noise Gate (`> n` chars)**:
  - If trimmed length $< n$, ignore completely.
  - Default $n = 50$ (customizable: 20, 50, 100, 200).
- **Auto-Debounce**:
  - Waits 1.5 seconds after typing stops before saving.
  - Immediately commits if the user switches tabs or navigates away.
- **Session Tracking**:
  - Keyed by current URL and field identity, so editing an existing post updates that entry instead of generating duplicate fragments.

### B. The Scribe Dashboard (`dashboard.html`)
- Opens in its own browser tab from the extension toolbar icon.
- **Layout**:
  - **Left Sidebar**:
    - Sites breakdown list with draft counts (e.g. `reddit.com (18)`, `facebook.com (9)`, `x.com (4)`).
    - Quick search bar.
    - Length filter chips (All, >100c, >500c).
  - **Middle Column**:
    - Cards showing page title / subreddit context, timestamp, word count, character count, and 2-line snippet.
  - **Right Reading Pane**:
    - Full text display with formatting intact.
    - Clickable source URL link.
    - **`[Copy to Clipboard]`** button (1-click).
    - **`[Download .md]`** button.
    - **`[Delete]`** button.
  - **Settings Modal**:
    - Minimum character threshold $n$.
    - Storage location selector (Browser Database vs. Direct Local Disk Folder vs. Server Hook).
    - Excluded domain blacklist (banks, password managers).

---

## 4. File Structure (Inside `auto_scribe_extension/`)
```
auto_scribe_extension/
├── manifest.json         # Manifest V3 configuration
├── background.js         # Service worker handling storage & file writing
├── scribe_content.js     # Universal input listener with threshold gate
├── popup.html / popup.js # Toolbar popup with quick status & "Open Dashboard"
├── dashboard.html        # Clean 3-pane dashboard
├── dashboard.css         # Modern dark theme styles
├── dashboard.js          # Filtering, grouping by site, search, and file export
└── plans/
    └── plan_001_scope_and_save_options.md
```
