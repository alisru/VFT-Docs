# Plan 033: Canvas Title Extraction Fix, Content-First Metadata Resolution, and Filename Repair

**Date**: 2026-10-18  
**Status**: In Progress  
**Milestone**: v1.5.3  

---

## 1. Root Cause Analysis

Why were canvases being saved with generic or truncated "bullshit" titles?

1. **Ordering Bug in `content.js`**:
   In `content.js`, if the DOM toolbar title became empty after stripping buttons (`Contents Share & Export Create`), line 1816 assigned `Canvas ${idx + 1}`. Because this fallback ran *after* the `editable.querySelector('h1, h2')` check, documents with clear H1 headers (like `Canvas 6.md` which had `# H1: Lorem Ipsum Dolor Sit Amet`) were permanently stamped as `Canvas 6`.
2. **Passive Backend (`ingest.py`)**:
   `ctx/ingest.py` trusted whatever title the extension sent. It never inspected the actual canvas markdown body for YAML frontmatter (`title: ...`) or the top markdown header (`# Title`).
3. **Hard 50-Character Filename Truncation**:
   Line 369 of `ctx/ingest.py` executed:
   `safe_filename = re.sub(r'[\\/*?:"<>|]', '_', c_title)[:50].strip() or "canvas"`
   This arbitrarily chopped titles mid-word (e.g. `Auditing Governance_ A Topological Framework for P.md`, `The Hegemonikon and Somatic Truth_ Theological and.md`).

---

## 2. Implementation Steps

1. **Backend Title Resolution Engine (`ctx/ingest.py`)**:
   - Build `resolve_canvas_title(raw_title: str, content: str) -> str`:
     1. **Frontmatter Check**: Parse YAML `title:` if present.
     2. **Markdown Header Check**: Parse the first `# Heading` from the text (strip `# `, `H1: `, etc.).
     3. **HTML Title Tag Check**: Parse `<title>...</title>` for HTML/code artifacts.
     4. **DOM Title Sanitization**: Clean UI buttons (`Contents Share & Export Create`, `Close`, `Download`).
     5. **Reject Generic Fallbacks**: If the title is `Canvas \d+`, `Untitled`, `Artifact \d+`, enforce the document's true internal header.
   - Expand filename length cap from 50 to 120 characters, snapping to word boundaries.

2. **Extension Title Extraction (`content.js`)**:
   - Reorder fallback logic in `content.js`: always inspect content headings/frontmatter *before* falling back to `Canvas N`.
   - Strip toolbar suffixes earlier in `getCanvasTitleFromElement`.

3. **Present Existing Broken Files for Review**:
   - Identify all canvases on disk that currently have truncated or generic names.
   - Present the before/after title mapping to the user before running any rename migrations.

4. **Update Shared Distribution**:
   - Sync fixes to `chat_context_clean/` and update `chat_context_clean_v1.5.2.zip`.
