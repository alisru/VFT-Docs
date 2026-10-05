# Implementation Plan - Bluesky Blob Upload Timeout & Retry Fix

## Problem
Posting failed on `factcheck_ai_charismatic_leader.json` with `Failed to upload graph: ` (empty error string) and stalled on `factcheck_paramount_antitrust_settlement.json`.
Root cause:
The `atproto` SDK sets default `httpx` timeout to 5.0 seconds. Uploading 500+ KB PNG graph images over transpacific network routes to the Bluesky PDS takes ~12-18 seconds, causing `httpx.WriteTimeout` / `atproto_client.exceptions.InvokeTimeoutError`. In `atproto`, `InvokeTimeoutError.__str__()` is empty, causing blank error messages and failed thread posts.

## Proposed Changes
1. **`bluesky_bot/aletheia_bot.py`**:
   - Introduce `ensure_client_timeout(client, timeout=60.0, connect=20.0)` to ensure the underlying `httpx.Client` has a 60-second write/read timeout.
   - Introduce `safe_upload_blob(client, img_data, desc="blob", max_retries=3, delay=2.0)` with automatic retries and descriptive error reporting via `str(e) or repr(e)`.
   - Update `post_thread` to use `safe_upload_blob` for trajectory graph, five-word terminal card, verdict split card, and analysis split card.
   - Configure timeout upon client instantiation in `main()`.
2. **`bluesky_bot/post_batch.py`**:
   - Configure client timeout immediately after `client = Client()` before logging in.

## Verification
- Run `python -m py_compile` on `aletheia_bot.py` and `post_batch.py`.
- Verify running Launcher process is not disturbed.
