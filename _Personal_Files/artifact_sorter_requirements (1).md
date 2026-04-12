# Claude Artifact Sorter — Requirements

Chrome extension for sorting, annotating, and browsing generated artifacts in the Claude.ai sidebar.

---

## What It Is

A Chrome extension injecting a floating control panel and sidebar sort bar into claude.ai. It operates exclusively on **generated artifacts** — the cards rendered in the right sidebar Artifacts panel. It does not touch uploaded files or project content.

---

## Scope Boundary

**In scope — generated artifacts only:**
- Cards matching `[role="button"][aria-label$=". Open artifact."]`
- Scoped to the sidebar Artifacts section (h3 text "Artifacts") — not inline message flow

**Out of scope — leave completely alone:**
- `[data-testid="file-thumbnail"]` with inner `<a href>` — project Google Docs
- `[data-testid="file-thumbnail"]` with inner `<button>` — uploaded files (Content section)
- No sort, no DOM manipulation, no injection on either of those buckets

---

## Core Features

### Sorting
- Sort generated artifacts by name A→Z, Z→A, or restore original DOM order
- Sort operates within the generated bucket only — never touches uploads or project files
- Two sort surfaces: sidebar sort bar (injected above artifact list) and floating panel

### Sidebar Sort Bar
- Injected directly above the artifact card list in the Artifacts sidebar section
- Buttons: A→Z / Z→A / ↺ (restore)
- Active sort highlighted in yellow
- Does not affect any other sidebar section

### Floating Panel
- Fixed-position draggable panel
- Two tabs: **This Chat** and **Project**
- Header controls: ↺ rescan, ⚙ DOM dump to console, ▾ collapse, ✕ close
- Auto-scans on panel build (no manual trigger needed on load)
- Panel auto-builds when Artifacts h3 appears in DOM (MutationObserver, not setTimeout)

---

## Summary System

### Sidebar Sort Bar — Summary Controls
- When new unsummarised artifacts are detected, badge appears: **"N new — summarise?"**
- Badge click: fills the chat input with the summary prompt (does NOT auto-send — user reviews and sends manually)
- After filling, badge transitions to **"↓ Inject"**
- Inject click: reads last Claude response from DOM, parses JSON array, injects summaries, button clears

### Floating Panel — Summary Controls
Three distinct controls in the panel summary section:

1. **⎘ Copy prompt** — builds prompt from artifact names, copies to clipboard (unchanged)
2. **↓ Summarise** — fills chat input with prompt AND auto-sends it (panel equivalent of the full flow in one click)
3. **↓ Inject** — reads last Claude response from DOM and injects; also has a **manual JSON paste field** — user can paste a JSON array directly into the field and inject from that instead of reading the DOM

### Length Options
- 1 sentence / 2–3 sentences / 5 sentences (selector in panel, applies to both prompt paths)

### Injection Target
- Summary injected as styled block under the type line of each artifact card in the actual sidebar DOM
- Also shown as a line under each artifact row in the floating panel list

### Persistence
- Summaries stored in `chrome.storage.local` keyed by chat ID (or project/chat prefix)
- Re-injected automatically on every scan — survives page refresh and new tabs
- Cleared only on extension storage wipe

---

## Timestamp System

- First-seen timestamp recorded in `chrome.storage.local` on first scan of each artifact name
- Format: `HH:MM DD.MM` (e.g. `14:32 30.03`)
- Not artifact creation time — first time the extension scanned and saw it (close enough)
- Shown in panel list alongside artifact name

---

## New Artifact Detection

- MutationObserver scoped to the Artifacts container (not document.body)
- Debounced at 500ms — only fires after DOM settles
- On new artifact detected: records first-seen timestamp, checks if unsummarised
- If unsummarised: shows badge **"N new — summarise?"** in sidebar sort bar
- Badge click: fills chat input with prompt, does NOT auto-send — user reviews before sending
- After fill, badge transitions to **"↓ Inject"** and clears after inject completes

---

## Project View (Panel Tab)

- Lists all chats in the current project that the extension has scanned
- Shows: chat name, artifact count, last-seen timestamp
- Current chat highlighted in yellow dot
- Each chat row has an **↗ link button** — real `<a href target="_blank">` for middle-click / new tab
- Chats with artifacts: single click expands inline artifact sub-list (name, timestamp, summary)
- Chats with no artifacts: single click navigates to chat
- Double-click always navigates
- Sub-list is lazy-rendered on first expand — pulls from storage
- Project ID extracted from URL or breadcrumb `<a href="/project/UUID">`
- Storage key structure: `proj_UUID/chat_UUID_cas_summaries`, `proj_UUID/chat_UUID_cas_first_seen`, `proj_UUID_chat_index`
- Standalone chats (no project): `chat_UUID_cas_summaries` etc.

---

## Storage Key Structure

| Key | Contents |
|-----|----------|
| `proj_UUID/chat_UUID_cas_summaries` | `{ artifactName: summaryText }` |
| `proj_UUID/chat_UUID_cas_first_seen` | `{ artifactName: "HH:MM DD.MM" }` |
| `proj_UUID_chat_index` | `{ chatId: { name, artifactCount, lastSeen, projectId, projectName } }` |
| `chat_UUID_cas_summaries` | Same, for standalone chats |
| `chat_UUID_cas_first_seen` | Same, for standalone chats |

---

## Performance Rules

- No polling loops, no fixed setTimeout for init — MutationObserver only
- Observer scoped tightly (artifacts container, not document.body)
- Debounce on observer: 500ms
- DOM operations use requestAnimationFrame, not setTimeout guesses
- Remaining intentional timeouts: highlight flash (1800ms), send button tick (100ms)
- No API calls — zero Claude token usage from the extension itself

---

## Known Issues / Open Items

- Two artifact cards with the same name (e.g. duplicate "Zenodo readme") — dedup keeps first by node reference, second is ignored in panel and inject mapping
- React may revert DOM reorders — if so, sort is visual-only until next scan
- Project file summaries (Google Docs in project) — not implemented; proposed path is a PROJECT_SUMMARIES.md maintained in the project, extension reads names and matches on scan


