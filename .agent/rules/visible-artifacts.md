---
trigger: always_on
glob: "**/*"
description: "Rule: Ensure all generated content is saved to a visible project folder"
---

# Visible Artifacts Rule

When the user asks you to "make," "generate," "create," or "draft" something (e.g., a document, a list, a code file, a summary):

1.  **Do NOT** only save it to the hidden `.gemini` artifact directory.
2.  **ALWAYS** ask yourself: "Where would the user expect to find this in their project?"
3.  **SAVE** the file potentialy to a relevant folder in the user's workspace (e.g., `_AI files and chat logs`, `_VFT MD`, etc.).
    *   If unsure of the best folder, ask the user or default to the root or a clearly named new folder (e.g., `_Generated_Content`).
    *   You can *also* create an artifact version for version control/history, but the **primary** deliverable must be visible in the workspace.

**Reasoning:**
The user cannot easily see or access files inside the hidden `.gemini` directory. To be helpful, work must be placed where the user can use it.
