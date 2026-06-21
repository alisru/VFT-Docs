---
description: Manage the lifecycle of cover-art subagents to prevent context bloat and compile prompt palettes.
---

This workflow defines the management, retirement, and palette extraction process for cover-generation subagents to keep the main chat fast while retaining design knowledge.

### 1. Rationale (Context Isolation)
Loading high-resolution images via the `view_file` tool creates massive vision tokens that cause long prompt-ingestion delays (1+ min). To prevent this, all image generation, validation, and OCR checks are delegated to isolated subagents (the "Artists").

---

### 2. Spawning the Artist Subagent
When starting a batch of cover generations, launch a new, clean subagent. Use a versioned identifier so they are easy to track.

```json
{
  "Subagents": [
    {
      "TypeName": "self",
      "Role": "Cover Artist v1",
      "Prompt": "Create and inspect cover images for the following video folders: [folders]. Use the 16:9 aspect ratio and write a report of text readability."
    }
  ]
}
```

---

### 3. Monitoring Context & Retirement Thresholds
As the Artist subagent generates and views images, its context window will fill up. 

* **The Threshold:** When the Artist's response time exceeds 30–45 seconds per turn, it has become "fat with context."
* **Retirement Action (DO NOT KILL):** Do not terminate the subagent using `manage_subagents` with action `kill`. Instead, let it go idle. Keeping it alive allows us to query it or view its transcript logs as a historical design library.
* **Hiring a New Artist:** Spawn a new subagent (e.g., `Cover Artist v2`) to handle the next batch.

---

### 4. Reusing the Retired Artist as a "Palette"
The newly hired Artist (`Cover Artist v2`) needs to know the established visual styles, successful color accents, and prompt parameters that worked. We extract this knowledge from the retired Artist:

1. **Prompt Ingestion:** Read the transcript of the retired Artist to extract successful prompt strings.
2. **Context Injecting:** Pass the extracted prompts (the "Palette") as a plain text instruction to the new Artist:
   > "Here is the visual palette established by your predecessor: [paste successful prompt text]. Mirror this composition and structure."
3. **Programmatic Audit:** Ensure the new Artist knows to output its validation reports to a plain text log file (e.g., `readability_report.txt`) in the workspace, so the parent agent can read it without ingesting image tokens.
