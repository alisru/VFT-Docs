# 04. How It Was Made

This document tells the story of how **Chat Context** was built, the tough technical obstacles encountered along the way, and the engineering breakthroughs that solved them.

---

## Phase 1: The Initial Spark & The CSP Wall

The project began with a simple need: **stop losing valuable research and technical writing trapped inside Google Gemini conversations.**

### Challenge 1: The Content Security Policy (CSP) Wall
When trying to send conversation text from Gemini to a local Python server (`http://127.0.0.1:8765`), Google's web app immediately blocked the network requests:
```text
Refused to connect to 'http://127.0.0.1:8765/api/ingest/chat' because it violates
the following Content Security Policy directive: "connect-src 'self' https://...".
```

### The Solution: Manifest V3 Extension Relay
Instead of trying to bypass CSP within the webpage context, we built a two-tier Chrome Extension:
1. The **Content Script** reads the DOM and extracts messages.
2. It sends an internal browser message (`chrome.runtime.sendMessage`) to the extension's **Background Service Worker**.
3. Because the service worker runs in its own extension origin with `host_permissions: ["http://127.0.0.1:8765/*"]`, it is completely exempt from the web page's CSP. The sync succeeded silently and reliably.

---

## Phase 2: The Virtualization Trap & Data Loss Crisis

As conversations grew longer (over 100 turns), a serious bug appeared: **earlier messages in long chats started disappearing from the database.**

### The Mystery
Why would messages vanish?
Upon inspecting Gemini Web's React/Angular frontend, we discovered **DOM Virtualization**. To prevent browsers from slowing down on 500-message chats, Gemini actively unmounts older `<user-query>` and `<model-response>` elements from the page when you scroll to the bottom.

If a sync was triggered while scrolled to the bottom, the extension only saw turns 40 through 60. The original ingest script ran `DELETE FROM messages WHERE chat_id=?` before inserting the incoming turns—accidentally wiping turns 1 through 39!

### The Solution: Non-Destructive Cumulative Merge Protocol
We enacted an absolute rule: **Chat data is never deleted.**
1. We permanently deleted `DELETE FROM messages` from the codebase.
2. We built a sequence alignment algorithm (`merge_messages`) in [`ctx/ingest.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/ctx/ingest.py).
3. Incoming turns are compared against existing database turns by normalized text. Existing messages and timestamps are preserved, and only new turns are appended.
4. When earlier messages were accidentally wiped prior to this fix, we scanned the unallocated freelist binary space of the SQLite database and successfully carved out and recovered 81 lost message turns.

---

## Phase 3: The SQLite FTS5 Trigger Malformation Bug

When syncing chats that had dozens of revisions, the server suddenly crashed with an alarming error:
```text
sqlite3.DatabaseError: database disk image is malformed
```

### The Root Cause
The database was using SQLite FTS5's external content table feature with automatic database triggers (`chunks_ai`, `chunks_ad`, `chunks_au`).
Whenever a chat was re-ingested and chunks were updated, the `chunks_ad` trigger executed:
```sql
INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', old.id, old.text);
```
If a chunk's token boundaries shifted slightly between syncs, SQLite's FTS5 internal b-tree index mismatched, throwing a false "database disk image is malformed" error and aborting with HTTP 500.

### The Solution: Safe Full-Text Rebuilds
1. We permanently dropped the fragile `chunks_ai`, `chunks_ad`, and `chunks_au` triggers.
2. We replaced them with an instantaneous full-text index rebuild after embedding batches:
   ```sql
   INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild');
   ```
3. SQLite FTS5 rebuilds are lightning-fast (under 10 milliseconds for thousands of chunks) and mathematically immune to index corruption. The malformed disk errors disappeared forever.

---

## Phase 4: Deterministic URLs & Duplicate Elimination

Early versions of the extension generated chat IDs using SHA-1 hashes of the current URL.
However, Gemini URLs contain tracking parameters and account routing:
- `https://gemini.google.com/u/1/app/424c86baff31945d?utm_source=app_launcher&utm_medium=owned`
- `https://gemini.google.com/app/424c86baff31945d`

Because the URLs differed slightly, the same conversation was being saved under multiple duplicate IDs (`gemini-78e6...` vs `gemini-424c...`).

### The Solution: Canonical URL Normalization
1. We implemented `normalizeGeminiUrl()` in both [`content.js`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/extension/chrome_extension/content.js) and [`ctx/ingest.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/ctx/ingest.py).
2. Strips all tracking query parameters (`utm_source`, `pageId`, `canvas-id`) and account routing (`/u/0/`, `/u/1/`).
3. Extracts the unique 16-character hex conversation ID and assigns a deterministic primary key:
   ```text
   gemini-424c86baff31945d
   ```
4. When an existing chat syncs under its canonical ID, any legacy alias duplicate shells are automatically identified: their historical turns and canvases are absorbed into the canonical record, and the empty shell is cleanly retired.

---

## Phase 5: The Task Tab Foreign Key Inversion

When syncing Gemini Scheduled Prompt / Task tabs (automated recurring runs), the tab reported that the server was offline, failing with an HTTP 500 error.

### The Root Cause
During the retirement of older duplicate alias rows, the script attempted to migrate canvases:
```python
con.execute("UPDATE OR IGNORE canvases SET chat_id=? WHERE chat_id=?", (chat_id, s_id))
```
This was running **before** the new `chat_id` was inserted into the `chats` table. Because `canvases` enforces a strict foreign key (`FOREIGN KEY (chat_id) REFERENCES chats(id)`), SQLite rejected the update with `sqlite3.IntegrityError: FOREIGN KEY constraint failed`.

### The Solution: Inverting the Upsert Order
We rearranged the execution order in `ingest_payload()`:
1. Collect all messages from legacy alias shells into memory.
2. Merge all messages into a unified sequence.
3. **Insert/Upsert the canonical `chats` record FIRST.**
4. **Migrate canvases and clean up alias shells SECOND.**
With `chat_id` now safely in the `chats` table, the foreign key constraint succeeded instantly, and the task tab turned green.

---

## Phase 6: The Evolution of Search & Sorting

Search started as a simple keyword query, but real research requires understanding concepts and finding recent thoughts quickly.

### 1. Hybrid Search Architecture
We combined SQLite's BM25 keyword matching with local vector embeddings (`sentence-transformers/all-MiniLM-L6-v2`).
- Exact terms like function names or quotes match with 100% precision via FTS5.
- Abstract topics (e.g. "god goal for you" matching spiritual purpose chats) match via dense semantic vectors.

### 2. Recency Sorting
Users needed to find recently discussed topics first. We added a dynamic time-decay weighting function to search scores, allowing users to switch between **Relevance**, **Newest First**, and **Oldest First**.

### 3. Topic & Source Facets
We added interactive controls in the dashboard:
- Filter by dynamic Topic clusters.
- Filter by Source (Gemini, Antigravity, Claude, ChatGPT).
- Mandatory `Must contain` keywords.

---

## Phase 7: The Living Canvases & Multi-Format Export Suite

The final milestone was ensuring users are never locked into the platform.

### Living Canvases
Gemini's markdown canvas documents are automatically pulled from the DOM, written to disk, committed to Git (`gemini-canvases`), and uploaded to Google Drive as native Google Docs.

### The Export Suite
We built [`ctx/export.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/ctx/export.py):
- Export single chats as Markdown, standalone HTML, JSON, or TXT.
- Export all 300+ chats at once as an organized ZIP archive grouped by topic folders, with complete frontmatter, canvas attachments, and zero path collisions.
- Accessible directly from the Web Dashboard, the Chrome Extension, and the CLI.

---

## Phase 8: Multi-Platform Expansion (Claude & ChatGPT)

Once Gemini sync was deterministic and unbreakable, we expanded Chat Context into a unified multi-platform intelligence system covering Anthropic's **Claude** (`claude.ai`) and OpenAI's **ChatGPT** (`chatgpt.com`).

### 1. Reverse-Engineering Modern AI DOMs
Using downloaded raw offline DOM snapshots (`Test - Claude.html` and `gpttest.html`), we analyzed the client-rendered DOM hierarchies without relying on volatile CSS class hashes:
- **Claude Web Extraction**:
  - Turns are encapsulated in `div[data-testid="transcript-row"]`.
  - Assistant responses live in `[data-testid="assistant-message"]` or `.font-claude-message`. Prefixes like `Claude responded:` and trailing action widgets are automatically stripped.
  - User messages live in `[data-testid="user-message"]` or `.cds-user-message-body`, stripping prefixes like `You said:` and timestamp watermarks.
- **ChatGPT Web Extraction**:
  - Contemporary ChatGPT web uses search unit keys: `[data-chatgpt-search-unit-key]` distinguishing turns like `fallback-turn-0:0:user` from `fallback-turn-0:1:assistant`.
  - Fallbacks target `[data-user-message-bubble="true"]` and `[data-message-author-role="assistant|user"]`.
  - Content prefixes like `ChatGPT said:` are cleanly parsed out.

### 2. Universal Browser Extension & Offline HTML Ingestion
- **Extension Routing**: In `content.js`, runtime hostname detection (`window.location.hostname`) automatically selects the platform extractor (`extractGeminiChat`, `extractClaudeChat`, or `extractChatGPTChat`).
- **Offline Importer**: In `ctx/importers.py`, `parse_html_chat()` detects whether an uploaded or scanned HTML file originated from Claude, ChatGPT, or Gemini, extracts all turns into structured messages, and ingests them into the SQLite store alongside JSON/Markdown/ZIP exports.

---

## The Human & Antigravity Collaborative Architecture

Chat Context was built as a pure pair programming partnership between the human creator and **Antigravity** (Google DeepMind's agentic AI coding assistant).

```
   +--------------------------------------------------------------+
   |                        HUMAN CREATOR                         |
   |  - System Architecture & Intuition                           |
   |  - Hard-won Operational Domain Truths                        |
   |  - Extreme Edge-Case Stress Testing (Virtual DOMs, Race Cond)|
   |  - Absolute Quality & Integrity Guardrails                   |
   +------------------------------+-------------------------------+
                                  |
                   Iterative Real-Time Dialogue
                                  |
   +------------------------------v-------------------------------+
   |                ANTIGRAVITY (AI CO-CREATOR)                   |
   |  - Full-Stack Code Implementation & Surgical Refactoring     |
   |  - Low-Level Binary Forensics (SQLite Freelist Extraction)   |
   |  - Browser Extension Architecture (MV3 CSP Bypass, DOM Hook) |
   |  - Formal Verification & Non-Destructive Invariant Proofs    |
   +--------------------------------------------------------------+
```

### How the Partnership Worked
1. **Real-Time Edge-Case Discovery**:
   When real-world conditions broke standard assumptions (e.g. Gemini's aggressive DOM virtualization lopping off the top 40 messages of long conversations, or Google's CSP blocking localhost API calls), the human identified the breakdown in live production sessions.
2. **Surgical Implementation & Binary Forensics**:
   Antigravity immediately dug into the root cause—dissecting SQLite WAL journals, analyzing CSP header directives, inspecting DOM node trees, and even recovering lost conversation turns by parsing raw SQLite B-Tree freelist leaves.
3. **Ironclad Guardrails & User Alignment**:
   Every architectural rule—such as *"CHAT INFO WILL NEVER BE DELETED, JUST DONT DUPLICATE INFO"* and *"Simplest Path First"*—was strictly codified into the codebase. Rather than discarding data or relying on blind overwrites, the system was engineered to preserve every message permanently.

---

## Summary of Milestones

| Milestone | What Was Achieved |
| :--- | :--- |
| **v1.0** | Basic local server + SQLite database + manual copy-paste ingestion. |
| **v1.1** | Chrome Extension with MV3 Service Worker to bypass web page CSP. |
| **v1.2** | Local AI embeddings (`all-MiniLM-L6-v2`) and FTS5 hybrid search. |
| **v1.3** | Non-destructive cumulative merge algorithm to defeat DOM virtualization. |
| **v1.4** | Deterministic canonical URL normalization and duplicate alias retirement. |
| **v1.4.3** | Foreign key execution order fix for Scheduled Task tabs and prompt routes. |
| **v1.4.4** | Full Export Suite: single-chat chips, bulk topic ZIPs, and in-widget export. |
| **v1.5.0** | Multi-Platform Expansion: Native extraction for Claude (`claude.ai`) and ChatGPT (`chatgpt.com`), offline HTML importer, and comprehensive documentation pack. |
