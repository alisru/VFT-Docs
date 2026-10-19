# Plan 010: Canvas Chat Isolation & Remediation of Genie Binding
**Date**: 2026-10-05  
**Author**: Antigravity  
**Status**: Completed & Verified  

## 1. Problem Diagnosed
In `Philosophical Stress Test for Genie Binding - Google Gemini`:
1. **Chat Message Swallowing Canvas**: Because inline canvases (`<immersive-entry-chip>`) are rendered inside the assistant's `model-response` container, `htmlToMarkdown` on the message container converted the entire response including the canvas. The canvas text (`The Genie Binding Dilemma & The HegemonikonExport # Formal Analysis...`) got embedded directly inside the chat bubble text.
2. **Missing Canvas Entity**: Because the in-memory content script in the browser tab hadn't reloaded the new chip selectors, the canvas was not extracted into `chat.canvases`.

## 2. Solutions Implemented
1. **Chat Message Isolation (`extractChatMessageMarkdown`)**:
   - Before converting assistant message HTML to Markdown, automatically strips all canvas components (`immersive-entry-chip`, `immersive-editor`, `inline-preview`, `artifact-card`, `canvas-card`, `.immersive-container`).
   - Ensures conversational text remains pure dialogue, while canvas documents live strictly in the Canvases entity/drawer.
2. **Title Cleanup**:
   - Strips any trailing `Export` button text attached to the title element (`title.replace(/Export$/i, '').trim()`).
3. **Database & File Remediation**:
   - Cleaned `Msg 1` of `Philosophical Stress Test for Genie Binding - Google Gemini` in `chats.sqlite` to contain only the dialogue text.
   - Extracted `The Genie Binding Dilemma & The Hegemonikon.md` with 100% LaTeX preservation (`$\upsilon > 0$`, `$\psi$`, `$$ \text{When a measure...} $$`, headings, and bold points).
   - Saved canvas file to `chat_context/canvases/Philosophical Stress Test for Genie Binding - Google Gemini/The Genie Binding Dilemma & The Hegemonikon.md`.
   - Committed and pushed to `origin main` on GitHub.
