# Implementation Plan 022: Fast Semantic Search with Recency Sorting

**Date**: 2026-10-14  
**Goal**: Make search instantaneous by caching chunk vectors in-memory (<16MB) and implement dual sorting (Relevance vs. Recent) across both the Web Dashboard and the Chrome Extension Context Drawer.

## 1. Problem Diagnosis
1. **Slow Search Speed**:
   - Every search query executed `SELECT id, chat_id, idx, emb FROM chunks` and unpickled 10,000+ byte blobs from disk on every search, taking hundreds of milliseconds to seconds.
2. **Missing Recency Sorting on Search**:
   - Search results were rigidly sorted by dot-product similarity (`top = np.argsort(-sims)[:k]`).
   - There was NO option to sort semantic matches by recency (`updated DESC`).
   - As a result, recently caught chats and canvases were drowned out by older high-scoring chats.
   - Result cards didn't even show the date/timestamp.

## 2. Technical Architecture
1. **In-Memory Vector Cache (`ctx/server.py`)**:
   - Cache `_chunks_cache`: `{"rev": None, "mat": np.ndarray, "metadata": [...]}`.
   - When `/api/search` is called, perform dot product `mat @ qv` in <1ms.
   - Auto-invalidates whenever `STATUS["rev"]` increments (when new chats are ingested).
2. **Dual-Mode Semantic Sorting (`/api/search`)**:
   - Parameter: `sort`: `"relevance"` (default) or `"recent"`.
   - Filter semantic candidates above threshold (e.g. `sims >= 0.25` or top 100 matches).
   - If `sort == "recent"`: Sort matches by `c.updated DESC`.
   - If `sort == "relevance"`: Sort matches by `score DESC`.
   - Each hit includes `chat_id`, `title`, `updated`, `score`, `text`, `idx`.
3. **Web Dashboard (`ui/index.html`)**:
   - Search results header with sort toggle: `[ Relevance | Recent ]`.
   - Render date badge (`YYYY-MM-DD HH:mm`) on each result card alongside score.
   - Instant client-side re-sorting between Relevance and Recent.
4. **Gemini Context Drawer (`content.js`)**:
   - In `🔎 Search` tab, add a sort bar: `[ 🎯 Relevance | 🕒 Recent ]`.
   - Show date badge on each search result card.
   - Allow instant switching between relevance ranking and recency ranking.
