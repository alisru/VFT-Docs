# Plan 023: Search Diagnostics, Semantic Chunking & Advanced Search Controls

**Date:** 2026-10-14  
**Status:** Investigation Complete & Architecture Proposed  
**Context:** User reported that searching `'god goal for you'` returned broad, loosely related content across random religious/tarot/fear passages rather than narrowing down to chats where the user actually discussed God's goals, plans, and opportunities for people.

---

## 1. Diagnostic Findings & Root Causes

### A. Dense Embedding "Semantic Bleed" (Unconstrained Cosine Similarity)
* The model `BAAI/bge-small-en-v1.5` compresses text into 384 dimensions.
* Searching `'god goal for you'` pulls in texts that contain:
  - Any religious words (`god`, `scripture`, `theology`, `Joshua 1:9`, or even tarot spreads like `Daily Spread Divination Analysis`).
  - Combined with personal advice words (`for you`, `believe in yourself`, `your immediate environment flourishes`).
* Pure vector similarity cannot enforce keyword presence or Boolean intersections.

### B. Missing BGE Query Instruction Prefix
* `bge-small-en-v1.5` is trained as an asymmetric retriever.
* Queries MUST be prefixed with: `"Represent this sentence for searching relevant passages: "`.
* When we tested adding this prefix, the user's primary conversation `Divine Sovereignty and Human Choice` ("God has an overarching intention, destination, and order... Within that master design...") immediately vaulted from below the fold into **#1**.

### C. Naive Character-Count Chunking
* `ctx/embed.py` currently cuts text purely at 1500 characters on `\n\n`.
* Chunks do NOT inherit the conversation title, topic, or role context.
* If a user asks "what is god's goal for people?", and the assistant replies with 3 long paragraphs, chunks 2 and 3 lose the question entirely and float as disconnected theological fragments.

### D. Result Fragmentation (No Conversation Roll-up)
* Search returns individual chunk rows. A single loosely matching conversation can occupy 4-5 slots in the top 10, pushing other relevant conversations off the screen.

### E. Lack of Filtering & Search Controls
* Users currently have no way to:
  - Force required keywords or exact phrases (`"god" "goal"` or `+god +goal`).
  - Toggle between **Hybrid Search** (Semantic + BM25 keyword matching), **Semantic Only**, and **Exact Match (FTS5)**.
  - Filter by **Topic / Semantic Cluster** (e.g. `epistemic / theology / theological`).
  - Filter by **Source** (`Gemini`, `Antigravity`, `Canvases`, `File Logs`).
  - Group results by **Conversation** (1 card per chat with best snippet) vs **Raw Chunks**.
  - Adjust a **Match Strictness / Threshold Slider**.

---

## 2. Proposed Architecture & Solutions

1. **BGE Query Prefix**: Automatically format all query embeddings with `"Represent this sentence for searching relevant passages: "`.
2. **Context-Aware Chunking**:
   - Prepend `[Chat: <title>]` and maintain conversational turn pairs (`[user] ... [assistant] ...`) so chunks never lose their topical anchor.
3. **SQLite FTS5 Hybrid Search (BM25 + Dense Cosine)**:
   - Index chunks in SQLite FTS5.
   - Hybrid scoring blends semantic similarity + BM25 match score + keyword presence bonus.
4. **Group by Conversation vs Chunks**:
   - Provide a toggle in UI: `[ 💬 Group by Chat | 📄 All Chunks ]`. Grouped view collapses duplicate chunks into a single clean chat card.
5. **Advanced Search Controls in Web UI & Chrome Extension**:
   - **Mode Toggle**: `[ ⚡ Hybrid | 🎯 Semantic | 🔍 Exact (FTS5) ]`.
   - **Topic Filter Dropdown**: Filter to specific semantic topic clusters.
   - **Required Keywords Box**: Optional field or quote syntax (`"god" "goal"`) to enforce mandatory terms.
   - **Match Strictness Slider**: Filter out low-confidence noise (<60%, <70%).
