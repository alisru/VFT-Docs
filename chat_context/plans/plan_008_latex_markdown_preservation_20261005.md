# Plan 008: High-Fidelity LaTeX & Markdown Preservation Engine
**Date**: 2026-10-05  
**Author**: Antigravity  
**Status**: Completed & Deployed  

## 1. Problem Diagnosed
Canvases extracted from Gemini Web were previously using `innerText` on the ProseMirror container:
1. Stripped all Markdown semantic tags: `#` headings, `**` bold, `*` italics, `-` lists, code fences, and tables.
2. Stripped and mangled LaTeX: KaTeX math spans (`.katex`, `.katex-display`, `<math-block>`, `<math-inline>`) were converted to flattened rendered Unicode glyphs, splitting exponents and subscripts across line breaks and losing original LaTeX syntax (`\upsilon`, `\text{...}`, etc.).

## 2. Solution Implemented
Integrated the battle-tested LaTeX extraction and Markdown serializer into both the Chrome Extension (`content.js`) and the Tampermonkey Userscript (`gemini_sync_userscript.js`):
1. **KaTeX Source Recovery (`extractTeX`, `replaceKaTeX`)**:
   - Inspects `data-math`, `data-tex`, `data-latex`, `data-latex-source`.
   - Reads `<annotation encoding="application/x-tex">` and `<math alttext="...">`.
   - Replaces display math (`math-block`, `.katex-display`) with clean `\n\n$$\n${tex}\n$$\n\n`.
   - Replaces inline math (`math-inline`, `.katex`) with clean ` $${tex}$ `.
2. **Structural Markdown Serializer (`htmlToMarkdown`)**:
   - Converts `H1`–`H6` to `#`–`######`.
   - Converts `P` to paragraph blocks (compact inside `LI`).
   - Converts `STRONG`/`B` to `**...**` and `EM`/`I` to `*...*`.
   - Converts `CODE` and `PRE` (with language attribute preservation).
   - Formats `UL`, `OL`, `LI` lists with proper indentation.
   - Converts HTML `TABLE` into clean Markdown tables (`| ... |`).
   - Retains blockquotes (`> ...`), horizontal rules (`---`), and links.
3. **Applied to Both Canvases and Assistant Chat Responses**:
   - Both `.ProseMirror` canvas editors and assistant message bubbles now export with 100% preserved LaTeX and Markdown hierarchy.
4. **Frontmatter Kept**:
   - Retains the structured YAML metadata at the top of canvas `.md` files as requested.
