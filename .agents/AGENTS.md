# Workspace Rules

## Brain Step Output Rule

When any tool call returns the message:
> "The output was large and was saved to: file:///C:/Users/hungh/.gemini/antigravity/brain/..."

**Immediately** run a `Copy-Item` to copy that file to the active project folder with a descriptive name, **before** reading or acting on the content:

```powershell
Copy-Item "C:\Users\hungh\.gemini\antigravity\brain\<conv-id>\.system_generated\steps\N\output.txt" `
  "e:\Vector Field Theory\VFT Docs\<active-project-path>\fetch_<description>_<YYYYMMDD>.json"
```

Rules:
- Filename must be descriptive (e.g. `fetch_shangri_la_2023.json`, `search_matildas_speech.json`)
- Destination is the **active project folder** — not drawing_board, not a temp folder, not the brain
- Copy happens **before** reading — so the file exists even if the session is interrupted or quota-crashed
- After copying, also extract key quotes/URLs into the project's `sources_raw.md` as a human-readable record
