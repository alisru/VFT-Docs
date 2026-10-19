# Plan 006: Pure Extension Architecture & In-Input Status Indicator
**Date**: 2026-10-06  
**Project**: Auto-Scribe Extension  
**Status**: In Progress  

## 1. Goal
1. **Pivot to Pure Extension & On-Demand Export**:
   - Eliminate the problematic background offscreen File System Access sync (which fails silently without user clicks due to Chrome's security model).
   - Solidify `chrome.storage.local` as the zero-overhead, 100% crash-proof storage engine for all drafts.
   - Maintain the fast 1-click **Export Markdown (.zip)** and **Export JSON** tools in the dashboard, plus on-demand folder sync when in the dashboard.
2. **Move Status Indicator to Bottom-Left of Text Entry Box**:
   - Discard the bottom-right fixed screen pill widget.
   - Create a clean, lightweight indicator anchored dynamically to the **bottom-left corner of the active text entry box** (`<textarea>`, `<input>`, or `[contenteditable]`).
   - Display:
     - **Circle icon** while actively typing / waiting to save.
     - **Tick icon (✓)** once successfully saved.
   - Softly fade out after a brief moment of inactivity so it does not obstruct reading, and reappear immediately on keystroke once threshold is met.
