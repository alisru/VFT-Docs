# Implementation Plan 021: Semantic Sorting "Sort by Recent" & Topics Drawer

**Date**: 2026-10-14  
**Goal**: Allow sorting semantic topic clusters by "Recent" (latest caught/updated chats first), "Name" (A-Z), and "Count" (largest first) in the Chat Context web dashboard and the Chrome extension drawer.

## Requirements
1. **Dashboard UI (`ui/index.html`)**:
   - In the "Topics" tab, add a quick sort control: `[Recent | Name | Count]`.
   - Default or allow selecting "Recent" so topics with the newest caught chats appear at the top.
   - Display the latest update timestamp / date badge on each topic header (e.g. `🎨 10-14` or `Updated 2h ago`).
   - Order the chats inside each topic by newest first.
   - Persist sort choice in `localStorage`.
2. **API Backend (`ctx/server.py`)**:
   - Enrich `/api/tree` topic objects with `updated` (max timestamp of member chats) and `count` so frontend can instantly sort without extra requests.
3. **Chrome Extension Context Drawer (`extension/chrome_extension/content.js` + `background.js`)**:
   - Add a `🗂️ Topics` tab to the drawer (`Alt+C`).
   - Support sorting topics by `Recent`, `Name`, and `Count`.
   - Allow expanding topics to see member chats, with one-click "Insert into Prompt" and "Copy".

## Verification
- Load `http://127.0.0.1:8765/` and test sorting by Recent, Name, Count.
- Check that topics with newly caught chats appear at the top when sorted by Recent.
- Verify drawer `🗂️ Topics` tab on Gemini web.
