---
name: from-the-audit-archive
description: Cross-reference external claims or Bluesky posts against the 10,800+ Hegemonic Audit database to retrieve historical vector precedents, render high-resolution Archival Badge Cards, and format persona-grounded replies (Aletheia, Brothekanon, Awwthekanon, Spirithekanon).
---

# From the Audit Archive

Cross-references any target claim, post, or actor against the permanent 10,800+ Hegemonic Audit Database (`stories/live/*.json` and `stories_registry.js`) to generate historical vector receipts, render official archival badge graphics, and deploy persona-aligned replies.

## Core Capabilities

1. **Semantic & Entity Cross-Referencing**:
   - Searches historical records across subject matter, named actors, topical tags, and vector coordinates.
   - Extracts exact Stated Claim $(\upsilon_{claim}, \psi_{claim})$ vs Ground Reality $(\upsilon_{real}, \psi_{real})$ horizons.
   - Computes historical Hypocrisy Stress Index ($\Delta \upsilon, \Delta \psi$).

2. **High-Resolution Archival Card Generation**:
   - Renders 16:9 dark-slate visual verification cards (`{slug}_archive_card.png`).
   - Displays Stated Claim vs Ground Reality horizons with Zone Anchors.
   - Embeds color-coded Verdict Banner (Emerald for PASS, Red for FAIL, Amber for CONDITIONAL).
   - Inscribes the Core Invariant / Unavoidable Truth and source QR code.

3. **Multi-Persona Archival Post Formatting**:
   - **⚖️ Aletheia Bot (`@judgement-bot.bsky.social`)**: Formal vector balance, case record ID, audit timestamp, invariant breakdown.
   - **🛹 Brothekanon (`@brothekanon.bsky.social`)**: Irreverent street-level reality check citing the historical audit receipt.
   - **🧸 Awwthekanon (`@awwthekanon.bsky.social`)**: Empathetic, human-centric memory of the audited event.
   - **🕊️ Spirithekanon (`@spirithekanon.bsky.social`)**: Perennial wisdom, scriptural invariant, and moral physics mapping.
   - Enforces strict character limits ($\le 290$ chars) to guarantee clean Bluesky delivery.

## Local Sourcing & CLI Usage

### 1. Direct Targeted Reply Dispatcher
Run via CLI or execute within `AletheiaLauncher.pyw`:
```bash
# Dry-run inspection and card generation
python bluesky_bot/direct_reply_dispatcher.py --target-url "https://bsky.app/profile/<handle>/post/<rkey>" --bot aletheia --skill archive

# Live threaded reply to Bluesky
python bluesky_bot/direct_reply_dispatcher.py --target-url "https://bsky.app/profile/<handle>/post/<rkey>" --bot brothekanon --skill archive --live
```

### 2. Python Programmatic Query
```python
from bluesky_bot.audit_crossref import search_audit_archive, format_archive_reply
from bluesky_bot.image_card_generator import generate_audit_archive_card

# 1. Query archive
matches = search_audit_archive("Trump tariffs", limit=3)
top_audit = matches[0]

# 2. Generate graphic card
card_path = f"bluesky_bot/graph_png/{top_audit['id']}_archive_card.png"
generate_audit_archive_card(top_audit, card_path)

# 3. Format persona reply text
reply = format_archive_reply(top_audit, persona="brothekanon")
print(reply)
```

## Post Format Standards

### Aletheia Analytical Receipt
```text
🏛️ From the Audit Archive [Record #{id}]:

Case: "{subject}"
Audited: {date} · Verdict: {verdict} [({real_u}, {real_psi})]

Invariant: "{unavoidable_truth}"
```

### Brothekanon Street Receipt
```text
🛹 Brothekanon Archive Receipt:
Audited {date} (#{id}).
Verdict: {verdict} [({claim_u}, {claim_psi}) → ({real_u}, {real_psi})]

"{bro_quote}"
```

### Awwthekanon Empathy Lens
```text
🧸 Awwthekanon Archive Memory:
Audited "{subject}" ({date}) · {verdict}:

"{aww_quote}"
```

### Spirithekanon Scriptural Invariant
```text
🕊️ Spirithekanon Archive Wisdom:
Record #{id} · Verdict: {verdict}:

"{spirit_quote}"
```
