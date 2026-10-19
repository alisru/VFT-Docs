# Plan 002: Storage and Implementation Specification
**Date**: 2026-10-05  
**Project**: Auto-Scribe Extension  
**Status**: Approved / In Progress  

## 1. Selected Storage Architecture
1. **Built-in Browser Database**:
   - `chrome.storage.local` automatically saves every draft snapshot as you type.
   - 100% crash-proof, zero setup, persists across browser restarts.
2. **Direct Local Disk Folder (File System Access API)**:
   - User clicks "Choose Folder" in settings and selects any folder (e.g. `E:\Drafts\`).
   - Extension saves directory handle in IndexedDB.
   - Automatically writes/updates markdown files organized by site:
     `<SelectedFolder>/<site>/<draft_title>.md`
   - Zero servers, zero Python, zero command-line tools.
3. **On-Demand Export**:
   - **Export JSON**: Complete database backup in one file.
   - **Export Markdown Archive**: Downloads drafts as formatted `.md` files.

## 2. Core Implementation Files
- `manifest.json`: Manifest V3 configuration.
- `scribe_content.js`: Universal input listener with `> n` character threshold gate.
- `background.js`: Service worker managing `chrome.storage.local` persistence.
- `popup.html` & `popup.js`: Toolbar extension popup with stats and dashboard shortcut.
- `dashboard.html`, `dashboard.css`, `dashboard.js`: 3-pane dashboard with site grouping, search, full reader, 1-click clipboard copy, folder picker, and export.
