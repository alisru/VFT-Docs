# Plan 018: Prevent Extraction of ASCII Diagrams / Code Snippets as Canvases

## Date: 2026-10-06

## Problem Description
- In chats like `Epistemology of Absolute Truth - Google Gemini`, Gemini generated inline ASCII diagram code blocks:
  - `Ground Truth (T = 1.0) | v ...` (17 lines)
  - `[ Fundamental Ground Truth (T = 1.0) ] | v ...` (17 lines)
- These were captured as separate fake "canvases":
  - `1. The Ontological Metric_ Reality as a Complete S.md` (577 bytes)
  - `1. Foundational Premise.md` (624 bytes)
- This obscured the real canvas document (`Epistemic Approximation and the Mechanics of Truth.md`, 12,511 bytes).

## Root Cause
1. **Over-Permissive DOM Selectors**:
   `content.js` queried `[aria-label*="Canvas" i]` and `[data-test-id*="canvas"]`.
   Gemini attaches `aria-label="Open in Canvas"` to buttons near standard chat code blocks and diagrams, causing their parent containers to be matched as canvas candidates.
2. **Loose Pre/Code Fallback**:
   When no Monaco or ProseMirror editor was found, the code grabbed any `<pre><code>` snippet.
3. **Low Length Threshold**:
   `content.length > 10` accepted any 11+ character code snippet.

## Solution
1. **Strict Canvas Selectors in `content.js`**:
   - Limit `canvasContainers` strictly to genuine top-level tags:
     `'immersive-entry-chip, immersive-editor, immersive-panel, aside[class*="immersive"]'`.
   - Remove `[aria-label*="Canvas" i]`, `[data-test-id*="canvas"]`, `inline-preview`, and `.canvas-container`.
2. **Remove Loose Code Block Fallback**:
   - Genuine code canvases in Gemini use Monaco (`.view-lines`) or CodeMirror (`.cm-content`).
   - Remove arbitrary `<pre><code>` fallback from non-editor containers.
3. **Document Length & Structure Guard**:
   - Enforce minimum canvas length (`content.length >= 250` characters).
   - In `ingest.py`, skip any canvas candidate where `c_type == 'code'` and `len(c_content) < 250`.
4. **Clean up Identified Snippet Files**:
   - Present identified bogus snippet files to user with exact `Remove-Item` command for confirmation before deletion.
