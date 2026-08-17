# Implementation Plan v26: Topic Threading, Dual-Track Memory & 2-MCP Modular Architecture

## 1. Overview
This implementation establishes a modular, high-precision reasoning and memory architecture:

1. **Hierarchical Topic Threading (`aletheia_chat.html` & `chat_server.py`):** Branching conversation trees with parent inheritance, token isolation, narrative spine tracking, and one-click synthesis merging.
2. **Local SQLite/FTS5 Memory Store (`memory_store.py`):** Fast local storage for observations, categories, and full-text indexed search over all 170+ Gemini & Claude transcripts in `_AI files and chat logs/`.
3. **Dedicated Aletheia News Audit MCP (`bluesky_bot/aletheia_mcp_server.py`):** Focused strictly on the 8,651+ factchecks, hypocrisy leaderboards, policy ledger, and chat session memory.
4. **Dedicated VFT Corpus & VDB MCP (`Semantic_Clusters/vft_mcp_server.py`):** Focused strictly on Qdrant `vft_paragraphs` vector search and philosophical topic cluster mapping across the repository.

---

## 2. Architecture & Data Flow

```
                      ┌────────────────────────────────────────────────────────┐
                      │                    OPERATOR / USER                     │
                      └───────────────────────────┬────────────────────────────┘
                                                  │
                ┌─────────────────────────────────┴─────────────────────────────────┐
                ▼                                                                   ▼
    [Aletheia Chat UI & Server]                                            [Claude Desktop / AGY]
   • Topic Threading (Tree Branches)                                       • Connects via stdio
   • Dual-Track Prompt Assembler                                           • Two independent MCP servers
                │                                                                   │
                ├─────────────────────────────────┬─────────────────────────────────┤
                ▼                                 ▼                                 ▼
   [MCP 1: aletheia]                     [SQLite Memory & Archives]        [MCP 2: vft-vdb]
   • 8,651+ News Audits                  • FTS5 Indexed Search             • Qdrant `vft_paragraphs`
   • Actor/Outlet Hypocrisies            • 170+ Gemini/Claude Logs         • `doc_ism_mapping.json`
   • 21-Domain Policy Ledger             • Structured Observations         • `topic_ism_mapping.json`
   • Thread & Narrative Memory           • Zero extra daemon overhead      • Deep VFT math proofs
```

---

## 3. Component Details

### 1. `bluesky_bot/memory_store.py` (Local SQLite Engine)
- Tables: `memories`, `archive_documents`, `archive_chunks`, `fts_archive`, `fts_memories`.
- Automatic indexing of all `.md` and `.txt` files in `_AI files and chat logs/`.
- Fast search functions for observations and historical transcripts.

### 2. `bluesky_bot/chat_server.py` (Topic Threading Engine)
- Multi-thread session schema with automated backward compatibility for legacy flat sessions.
- Endpoints: `POST /session/thread/create`, `POST /session/thread/merge`, `POST /session/thread/rename`.
- Dual-Track Context Assembler: `System Prompt + Narrative Spine + Ancestor Messages + Active Thread Turns + Recalled Chunks`.

### 3. `bluesky_bot/aletheia_chat.html` (Frontend UI)
- Thread Navigator breadcrumb header (`# Main Trunk` > `↳ 🏠 Housing Policy`).
- Sidebar collapsible tree displaying topic branches under each session.
- `🧵 Branch Thread` button on message bubbles.
- `📥 Merge Takeaways to Parent` action button with executive summary card.

### 4. `bluesky_bot/aletheia_mcp_server.py` (News Audit & Chat Memory MCP)
- `list_stories`, `get_story`, `get_moral_average`, `get_corpus_overview`, `get_gap_distribution`.
- `get_actor_hypocrisy_leaderboard`, `get_outlet_hypocrisy_leaderboard`, `get_policy_status`, `get_policy_report`.
- `search_chat_memory`, `get_chat_session`, `get_narrative_spine`, `create_memory_observation`.

### 5. `Semantic_Clusters/vft_mcp_server.py` (VFT Corpus & VDB MCP)
- `search_semantic_clusters(query, limit=5)`: Vector search against Qdrant `vft_paragraphs`.
- `get_topic_clusters(topic_or_ism)`: Cluster and tag lookup from `topic_ism_mapping.json`.
- `search_archive_logs(query, limit=5)`: Full-text search across `_AI files and chat logs/`.
- `get_archive_file(filename)`: Retrieve full raw transcript.

---

## 4. Verification Plan
1. **Automated Testing:** Test script validating SQLite FTS5 ingestion, thread branching/inheritance, thread merge distillation, and Qdrant vector retrieval.
2. **Manual UI Verification:** Branch a topic thread in the UI, converse, merge to parent, and test MCP queries.
