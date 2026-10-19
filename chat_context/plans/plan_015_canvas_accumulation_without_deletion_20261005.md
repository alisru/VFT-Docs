# Implementation Plan 015 - Canvas Accumulation Without Deletion

**Date**: 2026-10-05  
**Component**: `chat_context` (Ingestion Engine & Persistence)  
**Status**: Completed & Verified  

---

## 1. Problem Statement
The user pointed out a critical flaw:
*"updating can remove canvases, updating removes whats there and replaces it with whats loaded on the gemini page"*.

In Single Page Applications like Gemini:
- Older or non-active canvases in a long conversation may not be mounted in the DOM at the exact moment a sync occurs (Gemini often only renders the currently active canvas or chips currently in view).
- In a previous commit, `ctx/ingest.py` executed `DELETE FROM canvases WHERE chat_id = ?` prior to saving incoming canvases from the payload.
- As a consequence, whenever a chat synced while only one canvas was mounted in the DOM, all other previously captured canvases for that conversation were deleted from the database.

---

## 2. Solution: Additive Accumulation & Merge Storage
1. **Removed Destructive Deletion**:
   - Stripped `DELETE FROM canvases WHERE chat_id = ?` from [`ctx/ingest.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/ctx/ingest.py).
   - Canvases are treated as persistent, cumulative artifacts of the conversation.
2. **Deterministic Title-Hash Primary Keys**:
   - `c_id = f"{chat_id}-{hashlib.sha1(norm_title.encode()).hexdigest()[:8]}"`
   - When Gemini re-sends a canvas that is already saved, SQLite executes `ON CONFLICT(id) DO UPDATE SET title=..., content=..., updated=...`, updating it in place without creating duplicates.
   - When Gemini sends a newly generated canvas or one that wasn't in earlier payloads, it is added to the chat's existing collection.
   - Older canvases that aren't in the current DOM payload remain completely intact in both the database and on disk.
3. **Server Reload & Verification**:
   - Restarted `ctx.server` with the non-destructive ingest engine.
   - Ran [`repair_canvases.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/repair_canvases.py) to guarantee all on-disk canvases across all chats are restored.
