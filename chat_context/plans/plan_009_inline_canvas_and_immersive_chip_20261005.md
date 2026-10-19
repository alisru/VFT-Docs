# Plan 009: Inline Canvas Extraction & Gemini DOM Alignment
**Date**: 2026-10-05  
**Author**: Antigravity  
**Status**: Completed & Verified  

## 1. Ground Truth Discovery from Saved HTML
Analysis of `chat_context/html base/Failed Markdown Canvas Generation - Google Gemini.html` revealed the exact DOM structure for Gemini's current inline canvas rendering:
1. **No `<immersive-panel>`**: In Gemini's current inline interface, `immersive-panel` only exists in CSS style definitions; it is NOT rendered in the live DOM for inline canvases.
2. **`<immersive-entry-chip>` Component**:
   - Inline canvases are rendered directly inside chat model responses wrapped in `<immersive-entry-chip>`.
   - Title is rendered in `<div class="title-container"><div class="title-wrapper"><div class="title gds-body-l">Title</div>`.
   - Content is rendered in `<immersive-editor>` -> `#extended-response-markdown-content .ProseMirror`.

## 2. Changes Made
1. **Expanded Container Selectors**:
   - Added `immersive-entry-chip`, `immersive-editor`, and `inline-preview` to the canvas selector query.
2. **Container Deduplication**:
   - Added nested parent containment check: skips inner containers if an outer matching container (`immersive-entry-chip` or `immersive-panel`) is already processing the canvas.
   - Added content/title deduplication.
3. **Enhanced Title Fallback**:
   - Queries `.title`, `.title-wrapper .title`, `.title-container .title`, input fields, and falls back to the document's top `<h1>`/`<h2>` if no title element is present in the chip header.
4. **Maintained Full LaTeX & Markdown Recovery**:
   - Uses `htmlToMarkdown` to preserve all `#` headings, lists, tables, blockquotes, inline `$ ... $`, and display `$$ ... $$` math blocks.
5. **Version Bumps**:
   - Updated both `content.js` and `gemini_sync_userscript.js`.
   - Bumped `manifest.json` to `1.0.2`.
