# Implementation Plan: "From the Audit Archive" Post Format, Card Generator & Direct Manual 'Post To' Reply Dispatcher

## Overview
This plan implements:
1. **"From the Audit Archive" Post Format & Persona System**: Formal post framing (`🏛️ From the Audit Archive [Record #ID]`) with four distinct persona adaptations (Aletheia, Brothekanon, Awwthekanon, Spirithekanon) guaranteed under 300 characters for Bluesky.
2. **"From the Audit Archive" Visual Card Generator**: A high-resolution Pillow-rendered archival card (`{id}_archive_card.png`) displaying archival badges, historical timestamps, Stated Claim vs. Ground Reality coordinates $(\upsilon, \psi)$, Trajectory Delta, Verdict banner, and the Core Invariant / Unavoidable Truth.
3. **Audit Database Cross-Referencing Engine (`bluesky_bot/audit_crossref.py`)**: Fast indexing and semantic/actor/topic querying over the 10,800+ live audit stories in `stories/live/*.json` and `stories_registry.js`.
4. **Direct Reply Dispatcher Backend (`bluesky_bot/direct_reply_dispatcher.py`)**: Resolves target Bluesky post URLs, extracts author and content via ATProto, triggers the selected skill, attaches generated card graphics, and posts threaded parent/root replies.
5. **Aletheia Launcher Direct Reply UI (`AletheiaLauncher.pyw`)**: An interactive "🎯 Direct Post & Reply Dispatcher" card in the desktop GUI allowing the operator to paste any Bluesky URL, choose a bot, select a skill, preview the drafted reply & card image, and post live.
6. **Agent Skill Specification (`.agents/skills/from-the-audit-archive/SKILL.md`)**: Full skill specification for the VFT ecosystem.

---

## User Review Required
> [!NOTE]
> - **Bot Credentials**: By default, replies post through the authenticated account configured in `bluesky_bot/.env` (`BSKY_HANDLE` / `BSKY_PASSWORD`) with the selected persona header/tone. If individual credentials are later set (e.g. `BROTHEKANON_HANDLE` / `BROTHEKANON_PASSWORD`), the dispatcher will automatically switch to the dedicated account.
> - **Cross-referencing Accuracy**: If no manual search override query is provided, the cross-referencing engine extracts keywords and named entities directly from the target Bluesky post text to match against the 10,800+ audit database.

---

## Proposed Changes

### 1. Visual Card Generator: "From the Audit Archive"
#### [MODIFY] [bluesky_bot/image_card_generator.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/image_card_generator.py)
- Add `generate_audit_archive_card(story_cfg, output_path)`:
  - High-resolution dark aesthetic (`1200x675` or `1200x800` 16:9 ratio).
  - Header: `🏛️ FROM THE AUDIT ARCHIVE · ALETHEIA JUDGEMENT ENGINE`
  - Record ID, Audited Date, and Category tag.
  - Audited Subject & Actor summary.
  - Coordinate comparison panel:
    - Stated Claim: $(\upsilon_{claim}, \psi_{claim})$ with Zone Anchor.
    - Ground Reality: $(\upsilon_{real}, \psi_{real})$ with Zone Anchor.
    - Vector Delta: $\Delta \upsilon, \Delta \psi$.
  - Color-coded Verdict Banner:
    - Emerald (`#10b981`) for PASS / Awakening.
    - Red (`#ef4444`) for FAIL / Deception / Collapse.
    - Crimson (`#dc2626`) for Greater Evil.
  - Invariant Quote box: Displays the Unavoidable Truth or key social physics insight.
  - Watermark footer: `Alethekanon Psochic Hegemony Assessment · Verification Database`.

---

### 2. Audit DB Cross-Referencing Engine
#### [NEW] [bluesky_bot/audit_crossref.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/audit_crossref.py)
- `load_audit_registry()`: Fast cached loader for `stories_registry.js` / `stories/live/*.json`.
- `search_audit_archive(query_text, actors=None, topic=None, limit=5)`:
  - Normalizes text, matches named actors, title tokens, and semantic tags.
  - Ranks results by match density and date freshness.
- `format_archive_reply(audit_entry, persona="aletheia", target_text="")`:
  - Tailors post copy to the selected bot persona:
    - **Aletheia**: Formal, analytical delta, coordinate receipts, invariant.
    - **Brothekanon**: Irreverent street-level reality check citing the historical audit.
    - **Awwthekanon**: Empathetic, human-centric memory of the audited event.
    - **Spirithekanon**: Scriptural/ancient wisdom invariant mapped to the archival record.
  - Enforces strict character limits (< 290 chars) to prevent post truncation.

---

### 3. Direct Reply Dispatcher Backend
#### [NEW] [bluesky_bot/direct_reply_dispatcher.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/direct_reply_dispatcher.py)
- Resolves Bluesky URL to target DID, CID, URI, and root/parent references via ATProto.
- Fetches target post text and author metadata.
- Executes selected skill:
  - `archive`: Cross-references audit DB, selects top audit, generates card image, formats reply.
  - `evaluate`: Triggers live evaluation pipeline on the post claim.
  - `bro` / `aww` / `spirit`: Generates persona-specific reaction with coordinate grounding.
  - `custom`: Direct response with optional card attachment.
- Handles dry-run preview and live posting with image blob upload.
- CLI interface:
  ```bash
  python direct_reply_dispatcher.py --target-url "https://bsky.app/profile/..." --bot aletheia --skill archive [--query "Trump tariffs"] [--live]
  ```

---

### 4. Aletheia Launcher UI Integration
#### [MODIFY] [AletheiaLauncher.pyw](file:///e:/Vector%20Field%20Theory/VFT%20Docs/AletheiaLauncher.pyw)
- Add `create_direct_reply_card(parent)` right below the Research Probe Card:
  - Input field for Target Post URL.
  - Radio/dropdown for Bot Persona (`Aletheia`, `Brothekanon`, `Awwthekanon`, `Spirithekanon`).
  - Radio/dropdown for Skill (`From the Audit Archive`, `Standard Hegemonic Assessment`, `Brothekanon Reality Check`, `Awwthekanon Empathy Lens`, `Spirithekanon Scriptural Cross-Check`).
  - Search override entry (optional query for the audit archive search).
  - Buttons:
    - `🔍 Inspect & Generate Draft`: Runs preview, populates drafted text and card image.
    - `🚀 Post Live Reply`: Posts the reply live to Bluesky.
    - `👁️ Preview Card Image`: Opens the generated card in default image viewer.
  - Pipes real-time progress and logs directly into the right-hand console panel.

---

### 5. Skill Specification & Project Log
#### [NEW] [.agents/skills/from-the-audit-archive/SKILL.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agents/skills/from-the-audit-archive/SKILL.md)
- Complete protocol documentation for the skill.
#### [NEW] [bluesky_bot/_AI_Project_Plans/implementation_plan_v29_audit_archive_and_direct_reply.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/_AI_Project_Plans/implementation_plan_v29_audit_archive_and_direct_reply.md)
- Persistent project plan log in workspace.

---

## Verification Plan

### Automated / CLI Tests
1. **Card Generation Test**:
   ```bash
   .venv\Scripts\python.exe -c "from image_card_generator import generate_audit_archive_card; import json; cfg = json.load(open('stories/live/factcheck_minoru-yamasaki-wtc-legacy.json', encoding='utf-8'))[0]; generate_audit_archive_card(cfg, 'graph_png/test_archive_card.png'); print('Card generated successfully')"
   ```
   Verify `graph_png/test_archive_card.png` exists, is readable, and visually clean.
2. **Audit Cross-Reference Query Test**:
   ```bash
   .venv\Scripts\python.exe -c "from audit_crossref import search_audit_archive, format_archive_reply; res = search_audit_archive('Trump tariffs'); print(f'Found: {len(res)} matches'); print(format_archive_reply(res[0], 'aletheia')); print(format_archive_reply(res[0], 'brothekanon'))"
   ```
   Verify top matches return and replies format under 300 characters.
3. **Direct Reply Dispatcher Dry-Run Test**:
   ```bash
   .venv\Scripts\python.exe direct_reply_dispatcher.py --target-url "https://bsky.app/profile/kuow.org/post/3mvbuqi7pb52c" --bot aletheia --skill archive
   ```
   Verify target resolution, audit matching, card generation, and dry-run output.
4. **Launcher GUI Load Test**:
   Launch `AletheiaLauncher.pyw` in dry-run mode or check syntax and layout rendering without exceptions.
