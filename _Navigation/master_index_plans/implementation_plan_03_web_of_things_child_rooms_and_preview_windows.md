# Implementation Plan 03 — Web of Things: Subcategory Child Rooms & In-HTML File Reader

**Date**: 2026-10-24  
**Status**: Ready to Implement  
**Author**: Antigravity  
**Target Workspace**: `e:\Vector Field Theory\VFT Docs`  

---

## 1. User Feedback & Architectural Requirements

The user specified:
1. > *"oh its meant to open up the web of things, so if i click on an entry it opens up a new window thng"*
2. > *"then the file should be openable within the html as well"*

### Core Interaction Paradigm:
- **No More Disjointed Context Switching**:
  Clicking entries does not force the user away into an external browser tab or navigate away from the canvas. Everything happens **inside the landscape canvas** as a connected spatial graph ("the web of things").
- **Subcategory Doorways (e.g. `bluesky_bot (83)`)**:
  Clicking spawns a dedicated **Sub-Room Island** on the canvas, tethered to the parent topic room by an SVG bridge.
- **File Entries (e.g. `task_v13_compaction.md` or visualizers)**:
  Clicking spawns an **In-Canvas File Reader / Viewer Window** tethered by an SVG bridge directly to that room/entry.
  - **Markdown & Text (`.md`, `.txt`, `.py`, `.json`)**: The file content is loaded and rendered directly inside the HTML window with full formatting, headings, code styling, and copy buttons.
  - **Interactive Visualizers & Apps (`.html`)**: Rendered directly in a live interactive `<iframe>` inside the canvas window so the user can interact with the app side-by-side with other documents!
  - **Controls**: Draggable, resizable (`⤡`), Maximize (`⤢`), Open in New Tab (`↗`), and Close (`✕`).

---

## 2. Technical Architecture

### A. Subcategory Child Room Engine
- `spawnSubcategoryRoom(parentTopicId, subcatName)`:
  - Finds all files where `file.topic === parentTopicId` and `file.subcat === subcatName`.
  - Computes collision-free outward coordinate `(x, y)` relative to parent room.
  - Registers child room in `roomMap` with unique id `sub-${parentTopicId}-${subcatName}`.
  - Registers SVG bridge from parent room to child room.
  - Highlights the subcategory pill in the parent room with an active glow.
  - Clicking the pill again or clicking `✕` on the sub-room closes it and tears down its bridge.

### B. In-HTML File Reader Window Engine
- `openFileViewer(file, sourceRoomId)`:
  - If a viewer window for this file is already open, centers camera on it.
  - Otherwise, spawns a `.map-room.file-viewer-window` (`w: 560px, h: 420px`).
  - Registers SVG observation bridge from `sourceRoomId` to this viewer window.
  - Header:
    - File icon, title, path, type pill.
    - `↗ New Tab` button (for pop-out if desired).
    - `⤢ Maximize / Restore` button.
    - `✕ Close` button.
  - Viewer Body:
    - Asynchronously fetches file content from `getResolvedPath(file.path)`.
    - If `.html`: renders `<iframe src="${targetPath}">`.
    - If `.md`: renders using embedded zero-dependency Markdown parser (handling `#` headers, `**bold**`, `*italic*`, lists, code blocks, tables).
    - If code (`.py`, `.json`, `.js`): renders inside styled monospace `<pre><code>` block.
    - If fetch is blocked (e.g. strict `file:///` sandbox), displays rich metadata card with instant launch options.

### C. Live Bridge Updates
- Whenever any room (Parent Topic, Subcategory Child Room, or File Viewer Window) is dragged, `drawBridges()` recalculates all active bridge endpoints in real time.

---

## 3. Verification Steps
1. Verify clicking `bluesky_bot (83)` in the `Autonomous Bots & Social Agents` room spawns a new connected `📁 bluesky_bot` room on the map.
2. Verify clicking any `.md` file inside that room opens an in-canvas Reader Window displaying the rendered document.
3. Verify clicking an `.html` visualizer (e.g. in `Visualisers`) embeds a live interactive iframe inside the viewer window.
4. Verify closing a window removes it and its connecting bridge.
5. Verify both `http://localhost:8000/Master_Index.html` and `file:///` protocol handling.
