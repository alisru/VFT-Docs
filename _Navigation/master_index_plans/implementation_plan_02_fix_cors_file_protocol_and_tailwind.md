# Implementation Plan 02 — Fix CORS file:// Protocol & Tailwind Warning

**Date**: 2026-10-24  
**Status**: Ready to Implement  
**Author**: Antigravity  
**Target Workspace**: `e:\Vector Field Theory\VFT Docs`  

---

## 1. Problem Diagnosis

The user encountered two issues when launching `Master_Index.html`:
1. **CORS Block on `file:///` Protocol**:
   ```
   Access to fetch at 'file:///E:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/System/index_data.json' from origin 'null' has been blocked by CORS policy
   ```
   **Cause**: The user opened `Master_Index.html` directly from Windows Explorer as a local file (`file:///...`). Modern browsers (Chrome, Brave, Edge) block `fetch()` calls to `file:///` URLs due to the `origin 'null'` CORS security policy.
2. **Tailwind CDN Production Warning**:
   ```
   cdn.tailwindcss.com should not be used in production...
   ```
   **Cause**: Tailwind's browser runtime logs a warning on load.

---

## 2. Solution Strategy

### A. Dual Data Loading (`index_data.js` + `fetch('index_data.json')` Fallback)
1. In `generate_master_index.py`:
   - Generate `index_data.js` containing `window.VFT_INDEX_DATA = { ... };`.
   - Also generate `index_data.json` for standard HTTP clients.
   - Save both files to:
     - `e:\Vector Field Theory\VFT Docs\`
     - `e:\Vector Field Theory\VFT Docs\_VFT MD\System\`
2. In `Master_Index.html`:
   - Include `<script src="index_data.js"></script>`.
   - Browsers allow `<script src="...">` over `file:///` without CORS restrictions.
   - If `window.VFT_INDEX_DATA` exists, the app initializes instantly (0 ms latency, no network request, works offline and locally).
   - If not present (e.g. dynamic reload), fall back to `fetch('index_data.json')`.
   - If both fail, render a helpful diagnostic message explaining how to launch the local server or load `index_data.js`.

### B. Suppress Tailwind CDN Console Warning & Add Fallback CSS
- Add an inline filter before Tailwind CDN loads to silence the non-blocking production warning.
- Include essential styling fallbacks so the app renders even if offline without internet access.

### C. Update Batch Launchers & Add Root Launcher
- Update `_VFT MD\System\Scripts\start_vft_index.bat` to call `generate_master_index.py`.
- Create a root launcher `Launch_Master_Index.bat` in `e:\Vector Field Theory\VFT Docs\` that automatically checks port 8000, starts the server if needed, and opens `http://localhost:8000/Master_Index.html` in the user's default browser.
