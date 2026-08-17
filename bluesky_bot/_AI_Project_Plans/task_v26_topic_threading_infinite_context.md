# Detailed Task List v26: Unified Topic Threading, Memory Engine, Archive Ingestion & Semantic Clusters

## Phase 1: Local SQLite/FTS5 Memory Store & Ingestion (`bluesky_bot/memory_store.py`)
- [ ] **Task 1.1: Database Schema & Initialization**
  - [ ] Initialize `bluesky_bot/memory_store.sqlite` with WAL mode.
  - [ ] Create `memories` table: `(id TEXT PRIMARY KEY, category TEXT, content TEXT, tags TEXT, coords_u REAL, coords_psi REAL, session_id TEXT, thread_id TEXT, created_at TEXT, updated_at TEXT)`.
  - [ ] Create `archive_documents` table: `(id TEXT PRIMARY KEY, filename TEXT, filepath TEXT, file_hash TEXT, chunk_count INT, mtime REAL, created_at TEXT)`.
  - [ ] Create `archive_chunks` table: `(id TEXT PRIMARY KEY, doc_id TEXT, filename TEXT, chunk_index INT, content TEXT, tokens_est INT)`.
  - [ ] Create `fts_archive` FTS5 virtual table indexing `(filename, content)`.
  - [ ] Create `fts_memories` FTS5 virtual table indexing `(category, content, tags)`.
- [ ] **Task 1.2: External Chat Logs Ingester**
  - [ ] Implement `index_ai_chat_logs(dir_path)` to scan `_AI files and chat logs/` for `.md` and `.txt` files.
  - [ ] Implement smart paragraph/heading chunker (300–600 word chunks with overlap and heading preservation).
  - [ ] Compute file mtimes and hashes to only re-index new or modified files.
- [ ] **Task 1.3: Archive & Memory Search API**
  - [ ] Implement `search_archive_logs(query, limit=5)` using FTS5 rank scoring and snippet extraction.
  - [ ] Implement `search_memories(query, category=None, tags=None, limit=10)`.
  - [ ] Implement `create_memory(content, category, tags, coords_u=None, coords_psi=None, session_id=None, thread_id=None)`.
  - [ ] Implement `delete_memory(memory_id)`.
- [ ] **Task 1.4: Qdrant Vector & Semantic Cluster Connector**
  - [ ] Implement `search_qdrant_clusters(query, limit=5)` using `SentenceTransformer('all-MiniLM-L6-v2')` connecting to Qdrant `vft_paragraphs`.
  - [ ] Implement `get_topic_cluster_mapping(topic)` reading `Semantic_Clusters/topic_ism_mapping.json` and `doc_ism_mapping.json`.

---

## Phase 2: Hierarchical Topic Threading & Backend Logic (`bluesky_bot/chat_server.py`)
- [ ] **Task 2.1: Session Schema Migration & Multi-Thread Storage**
  - [ ] Upgrade `load_session(session_id)` to parse `threads: { [thread_id]: { id, name, parent_thread_id, fork_message_index, created_at, messages } }` and `narrative_spine: []`.
  - [ ] Add auto-migration logic: if legacy flat session `messages: []` is detected, migrate it to `threads: { "main": { id: "main", name: "Main Trunk", parent_thread_id: null, fork_message_index: 0, messages: [...] } }`.
  - [ ] Upgrade `save_session(session_data)` to persist multi-thread trees atomically.
- [ ] **Task 2.2: Thread Branching & Merging Endpoints**
  - [ ] Implement `POST /session/thread/create`: parameters `(session_id, parent_thread_id, fork_message_index, name)` -> creates new branch.
  - [ ] Implement `POST /session/thread/merge`: parameters `(session_id, thread_id)` -> triggers LLM distillation of branch, extracts $(\upsilon, \psi)$ coordinates, updates `narrative_spine`, and inserts summary card into parent thread.
  - [ ] Implement `POST /session/thread/rename` and `POST /session/thread/delete`.
- [ ] **Task 2.3: Dual-Track Prompt Assembler & Ancestral Context**
  - [ ] Implement `build_dual_track_payload()`:
    - 1. System Prompt + Global Memory Profile.
    - 2. Narrative Spine (timeline of session topics).
    - 3. Ancestral parent thread messages from root up to `fork_message_index`.
    - 4. Active thread recent turns (with rolling compaction if > 12 turns).
    - 5. Retrieved Archive Chunks (from `_AI files and chat logs/`).
    - 6. Retrieved Semantic Clusters (from Qdrant `vft_paragraphs`).
    - 7. Retrieved Story Audits (from 8,651 database).
  - [ ] Update `call_llm_chat()` to execute the assembled payload.

---

## Phase 3: FastMCP Server Integration (`bluesky_bot/aletheia_mcp_server.py`)
- [ ] **Task 3.1: Conversation Memory Tools**
  - [ ] Implement `@mcp.tool() search_chat_memory(query, session_id="", limit=5)`.
  - [ ] Implement `@mcp.tool() get_chat_session(session_id)`.
  - [ ] Implement `@mcp.tool() get_narrative_spine(session_id)`.
  - [ ] Implement `@mcp.tool() create_memory_observation(topic, observation, tags=[])`.
  - [ ] Implement `@mcp.resource("aletheia://chat-sessions")`.
  - [ ] Implement `@mcp.resource("aletheia://memory-profile")`.
- [ ] **Task 3.2: External Archive Tools**
  - [ ] Implement `@mcp.tool() search_archive_logs(query, limit=5)`.
  - [ ] Implement `@mcp.tool() get_archive_file(filename)`.
- [ ] **Task 3.3: Semantic Clusters Vector Tools**
  - [ ] Implement `@mcp.tool() search_semantic_clusters(query, limit=5)`.
  - [ ] Implement `@mcp.tool() get_topic_clusters(topic)`.
- [ ] **Task 3.4: Story Audit Analytical Tools**
  - [ ] Expose `list_stories`, `get_story`, `get_moral_average`, `get_corpus_overview`, `get_gap_distribution`, `get_actor_hypocrisy_leaderboard`, `get_outlet_hypocrisy_leaderboard`, `get_policy_status`, `get_policy_report`.

---

## Phase 4: Frontend UI Threading & Memory Visualizer (`bluesky_bot/aletheia_chat.html`)
- [ ] **Task 4.1: Thread Navigator & Breadcrumb Header**
  - [ ] Add sticky thread breadcrumb bar: `# Main Trunk` > `↳ 🏠 Housing Policy`.
  - [ ] Add thread switcher dropdown / pill strip to jump between sibling branches.
- [ ] **Task 4.2: Nested Thread Tree in Sidebar**
  - [ ] Render expandable tree under each chat session showing all sub-threads with message counts.
  - [ ] Add `+ New Thread` button in sidebar.
- [ ] **Task 4.3: Message Branching & Merging Controls**
  - [ ] Add `🧵 Branch Thread` button on every message bubble with name prompt modal.
  - [ ] Add `📥 Merge to Parent` button in the thread header with loading spinner and confirmation card.
- [ ] **Task 4.4: Grounding Source Indicators**
  - [ ] Display badges when context is retrieved: `📚 Audits`, `📑 Archive Logs (_AI files)`, `🔮 Semantic Clusters (Qdrant)`.

---

## Phase 5: Verification, Testing & Documentation
- [ ] **Task 5.1: Automated Unit Tests**
  - [ ] Write `bluesky_bot/tests/test_unified_memory.py`.
  - [ ] Test SQLite FTS5 ingestion and search on `_AI files and chat logs/`.
  - [ ] Test Qdrant vector retrieval.
  - [ ] Test thread creation, inheritance, and thread merge distillation.
- [ ] **Task 5.2: Manual End-to-End Testing**
  - [ ] Open UI, branch a thread, send messages, merge to parent.
  - [ ] Query concepts from `_AI files and chat logs/` and Qdrant.
  - [ ] Test MCP tool responses over stdio.
- [ ] **Task 5.3: Documentation & Dialogue**
  - [ ] Update `running_dialogue.md` and walkthrough.
