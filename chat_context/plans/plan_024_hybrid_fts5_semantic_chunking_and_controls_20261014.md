# Plan 024: Hybrid FTS5 + BGE Semantic Search & Advanced Controls Implementation

**Date:** 2026-10-14  
**Status:** Completed & Live on Server (Port 8765) and Chrome Extension (v1.4.0)  

---

## 1. Summary of Changes

### A. Context-Aware Semantic Chunking & BGE Asymmetric Retrieval (`ctx/embed.py`)
- **Asymmetric Query Instruction Prefix**: Added `embed_query(query)` applying `"Represent this sentence for searching relevant passages: "` required by the `bge-small-en-v1.5` architecture for retrieval.
- **Context-Aware Framing**: Updated `chunk_messages(msgs, chat_title)` so every conversation's chunks inherit the conversation title and topical framing, preventing fragments from floating without context.

### B. SQLite FTS5 Full-Text Search Integration (`ctx/db.py`)
- Created external content virtual table `chunks_fts USING fts5(text, chat_id UNINDEXED, content='chunks', content_rowid='id')`.
- Zero disk duplication: reads raw text from `chunks`.
- Added automatic synchronization triggers (`chunks_ai`, `chunks_ad`, `chunks_au`) and automated rebuild check in `init_db()`.

### C. Advanced Hybrid Search Backend (`ctx/server.py`)
- **Query Parsing**: Automatically extracts quoted phrases (`"god" "goal"`) into mandatory filters.
- **Search Modes**:
  - `hybrid` (Default): Blends 65% dense vector cosine similarity + 20% normalized SQLite FTS5 BM25 rank + 15% keyword presence ratio (+ bonus if all search words appear).
  - `semantic`: Pure dense vector cosine similarity (with BGE instruction prefix).
  - `exact`: Pure SQLite FTS5 BM25 match.
- **Granular Controls**:
  - `group_by`: `chat` (collapses all matching passages into 1 clean card per conversation, taking the highest-scoring passage + passage count) vs `chunk` (raw individual passages).
  - `must_contain`: Mandates specified terms before ranking.
  - `topic_id`: Filters search directly into a specific semantic cluster.
  - `source`: Filters by platform (`gemini`, `antigravity`, `claude`, `chatgpt`, `file`).
  - `min_score`: Strictness threshold slider (e.g., 50%, 60%, 70%).
  - `sort`: `relevance` (score DESC) vs `recent` (updated DESC).
- Added `/api/topics` and `/api/sources` endpoints for dynamic UI filters.

### D. Web Dashboard UI (`chat_context/ui/index.html`)
- Added two-tier interactive controls bar at the top of search results:
  - **Toggles**: Mode (`⚡ Hybrid` / `🎯 Semantic` / `🔍 Exact`), View (`💬 Chat` / `📄 Chunks`), Sort (`🎯 Relevance` / `🕒 Recent`).
  - **Filters**: Must Contain input box, Topic dropdown, Source dropdown, Min Match strictness slider (`0% - 80%`), and Reset Filters button.
- Rich Search Cards:
  - Clickable topic badges (`🏷️ epistemic / theology / theological`) that instantly filter search to that cluster.
  - Source badge (`GEMINI`, `ANTIGRAVITY`, etc.).
  - Passages count badge (`📄 4 passages`).
  - Caught timestamp badge (`🕒 YYYY-MM-DD HH:mm`).
  - Match score badge (`🎯 % match`).

### E. Gemini Chrome Extension (`content.js`, `background.js`, `manifest.json`)
- Updated `background.js` to relay all search options to `/api/search`.
- Updated Context Drawer (`Alt + C`) search bar in `content.js`:
  - Added multi-row controls bar under search input (`Mode`, `View`, `Sort`, and active Topic filter pill).
  - Added clickable topic badges on search cards so clicking any topic filters results directly into that cluster.
  - Added passage count, source badge, caught timestamp badge, and score badge.
- Bumped extension version to **1.4.0** in `manifest.json`.

---

## 2. Verification
Tested with the query: `'god goal for you'`:
- **Hybrid Search (Grouped by Chat)** immediately surfaced:
  1. `Limits of Omnipotence and Definition - Google Gemini` (*"Lets use God as an teleological, praxeological process goal of 'a being of perpetual good' ..."*)
  2. `Google Gemini` (*"All religions that teach this fact, this goal of God to increase potential options, these prescribed actions for worship..."*)
  3. `Divine Sovereignty and Human Choice - Google Gemini` (*"God holds His own sovereign, macro-level plan that establishes ultimate direction, values, and places for humanity... dynamic, branching field of real opportunities..."*)
- Irrelevant tarot spreads (`Daily Spread Divination Analysis`) and fear verses (`Scripture for Fear and Anxiety`) were eliminated from top ranks.
