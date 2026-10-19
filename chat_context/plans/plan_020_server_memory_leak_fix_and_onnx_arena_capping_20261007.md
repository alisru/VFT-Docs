# Implementation Plan 020: Server Memory Leak Fix and ONNX Arena Capping

**Date**: 2026-10-07  
**Goal**: Eliminate the 5.2 GB server memory ballooning by capping ONNX Runtime thread arena allocations in FastEmbed, throttling background ingest cycles, and optimizing embedding batch size.

## Root Cause Analysis
1. **Unbounded Thread Arenas in FastEmbed/ONNX Runtime**:
   - `FastEmbed` initialized `TextEmbedding` with default `threads=None`.
   - On a 12-core system, ONNX Runtime allocated dedicated memory pools (arenas) across all 12 worker threads.
   - Combined with default `batch_size=256`, every batch triggered huge multi-gigabyte memory allocations that ONNX never released to the OS.
2. **High-Frequency Ingest Wake Cycles**:
   - Every keystroke/message payload from the browser called `/api/ingest/chat`, which directly called `_wake.set()`.
   - This forced `_run_once()` to execute immediately in a tight loop.
3. **Continuous Re-embedding of Antigravity Transcripts**:
   - Every active Antigravity session continuously modifies `transcript_full.jsonl` mtime.
   - The server re-read the multi-megabyte transcript, deleted all chunks, set `emb=NULL`, and repeatedly embedded hundreds of chunks.
4. **Missing Python Garbage Collection**:
   - Large numpy arrays and SQLite row buffers lingered across thread cycles without explicit `gc.collect()`.

## Benchmark Proof
- Uncapped (`threads=None`, `batch_size=256`): Jumped from 205 MB to **1,869 MB** in 400 chunks, and **5,229 MB** in production.
- Capped (`threads=2`, `batch_size=32`): Leveled off strictly at **440 MB** (flat across repeated 1,000-chunk loops).
- Capped (`threads=1`, `batch_size=16`): Leveled off strictly at **321 MB**.

## Action Items
1. **`ctx/embed.py`**:
   - Configure `TextEmbedding(model_name=MODEL_NAME, threads=2)`.
   - Enforce `batch_size=32` in `embed_texts()`.
   - Call `gc.collect()` after bulk embeddings.
2. **`ctx/server.py`**:
   - Add debouncing to `_wake` (minimum 30-second cooldown between background sync runs).
   - Call `gc.collect()` in `_run_once()` finally block.
3. **`ctx/ingest.py`**:
   - For Antigravity transcripts, skip re-ingestion if the number of messages in the transcript hasn't changed.
4. **Restart Daemon**:
   - Restart `task-2173` with the hardened configuration and verify working set memory stays under 500 MB.
