# Plan 027: Immutable Non-Destructive Message Sync

**Date:** 2026-10-14  
**Status:** Completed & Verified  

## 1. Rule & Requirement
"CHAT INFO WILL NEVER BE DELETED, JUST DONT DUPLICATE INFO"

## 2. Root Cause of Previous Data Loss
In long web conversations, Gemini's web client virtualizes the DOM: when you are scrolled toward the bottom, Google unmounts older turns from the top of the DOM to save browser memory.
Previously, `content.js` would scrape the visible DOM (e.g. only 12 messages).
The server's `ingest_payload()` previously ran:
```sql
DELETE FROM messages WHERE chat_id = ?;
```
This wiped out the previous turns (e.g. turns 0..40) that were already saved in the database!

## 3. Implemented Fix: 100% Non-Destructive Merge
1. **Permanent Removal of `DELETE FROM messages WHERE chat_id=?`**:
   The database never drops existing messages for a chat.
2. **`merge_messages()` Protocol**:
   - Ingestion loads all existing historical messages for `chat_id`.
   - Incoming messages are matched against existing messages using normalized content.
   - Already-existing turns are preserved in their original sequence and not duplicated.
   - Newly arrived turns are appended at the end of the history.
   - If the browser only sends a partial tail of the chat, the entire historical head remains untouched.
3. **Safe Legacy Alias Migration**:
   - When unifying multiple URL aliases into a canonical conversation ID, messages from the legacy aliases are absorbed into the unified history before any duplicate shell row is retired.
   - Canvases are safely re-parented with `UPDATE OR IGNORE canvases SET chat_id=?`.
4. **`ON CONFLICT(chat_id, idx) DO UPDATE`**:
   - Individual messages are upserted by index.
   - Message history is strictly cumulative and monotonically non-decreasing.

## 4. Verification
- Tested with multi-turn conversation followed by partial tail-end payload.
- Verified all earlier turns remain intact in SQLite with zero data loss and zero duplicates.
