# Implementation Plan 04 — Scroll Fix, Tile Resizability, Auto-Fit, Reload Protection & Summary View Options

**Date**: 2026-10-24  
**Status**: Ready to Implement  
**Author**: Antigravity  
**Target Workspace**: `e:\Vector Field Theory\VFT Docs`  

---

## 1. Problem Statement & User Directives

The user requested:
> *"when mouse hover on a tile it should scroll the tile not zoom, shift should zoom, also i want reload protection and tile resizeability, also auto resize to see all files within, alongside some view options, like an option to see a summary of the file in the tile. I know we have a lot of summaries in @file_summaries.json, it doesnot cover the repo, its also poorly formatted, idk if its worth even using really,. see the 'custom windows file viewer' chat for info about the semantic git idea i had. pls just do research and fix that scroll error"*

### Key Issues:
1. **Scroll vs. Zoom Collision (Wheel Event Bug)**:
   Hovering over any room list or document viewer window zooms the canvas instead of scrolling the inner container.
2. **Missing Tile Resizability & Auto-Fit**:
   Rooms have static default dimensions; users cannot drag-resize them or auto-expand them to fit their contents without vertical scrolling.
3. **No Reload Protection (Lost State on F5)**:
   Refreshing the page resets the camera, collapses all spawned sub-rooms, closes all document viewer windows, and resets custom room coordinates.
4. **Missing View Option for Inline Summaries**:
   File rows only show titles/filenames; users need an option to see the 1-2 line summary directly in the tile.

---

## 2. Technical Architecture & Implementation Details

### A. Wheel Scroll vs. Zoom Separation
```javascript
container.addEventListener('wheel', (e) => {
    const scrollable = e.target.closest('.map-room-files, .viewer-body, .overflow-y-auto, .overflow-auto');
    if (scrollable && !e.shiftKey) {
        // Natural mouse wheel scroll inside the room or viewer!
        return; // Do NOT prevent default, do NOT zoom
    }
    // Shift+Wheel anywhere, or normal wheel over canvas/headers -> Zoom canvas
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.12 : 0.89;
    // zoom towards mouse...
}, { passive: false });
```

### B. Tile Drag-Resizer & Auto-Fit Solver
1. **Interactive Resizer Handle (`.room-resizer`)**:
   - Placed at the bottom-right corner of every `.map-room` and `.viewer-window`.
   - On mousedown, captures drag coordinates and updates `--room-w` and `--room-h`.
   - Real-time `drawBridges()` and `updateEdgeLens()` during resize.
2. **Auto-Fit Button (`⤢ Fit`) on Room Headers**:
   - Calculates total item count.
   - For lists: sets height = `headerHeight + (itemCount * rowHeight) + padding`. If `itemCount > 12`, expands width to multi-column grid so the room stays proportioned.
   - Saves new dimensions to persistent layout state.

### C. Reload Protection & State Persistence (`localStorage`)
- Storage Key: `vft_master_index_state_v1`
- Persists:
  - `camera`: `{ camX, camY, camZoom }`
  - `rooms`: `{ [id]: { x, y, w, h } }`
  - `openSubRooms`: `[[topicId, subcatName], ...]`
  - `openViewers`: `[fileObj, ...]`
  - `viewOptions`: `{ showSummaries: boolean, roomMode: 'rows'|'cards' }`
- On boot: auto-restores camera, room sizes, re-spawns open sub-rooms, and re-opens document viewer windows!
- Adds a `Reset Map` option in HUD to revert to default pristine layout whenever needed.

### D. View Options: Inline Summaries Toggle
- Add HUD button: `📋 Summaries: ON / OFF`.
- When ON, adds an excerpt snippet under each file row.
- Dynamically toggles across all open rooms in real time.

---

## 3. Research on `file_summaries.json` & Semantic Git
- **`file_summaries.json`**:
  - Examined: 3.5 MB file with 1,664 entries, mostly `.docx` files from August 2026.
  - As noted by the user, it is incomplete and irregularly formatted.
  - In `generate_master_index.py`, we already dynamically extract clean, up-to-date titles and summaries directly from `.md`, `.html`, and `.py` files across all 5,041 items. We will use `file_summaries.json` as a fallback only when a file has no extracted summary.
- **The "Semantic Git" & "Custom Windows File Viewer" Vision**:
  - Retrieved from chat `8cad916f-b7f9-4211-80d3-12089758764a`:
    - Connecting to local LM Studio or lightweight embedding models.
    - Creating "Virtual Topic Folders" (shared conceptual spaces across physical disk folders).
    - Semantic similarity checking across Markdown files.
    - Tracking changes to the semantic information field rather than raw line diffs.
