# Walkthrough - Fix Bluesky Blob Upload Timeout & Retries

## Summary
Resolved the issue where live posting failed during trajectory graph and card uploads due to `atproto`'s default 5-second `httpx.WriteTimeout`.

## Changes Made
1. **`bluesky_bot/aletheia_bot.py`**:
   - Added `ensure_client_timeout(client)` to configure the underlying `httpx.Client` with `httpx.Timeout(60.0, connect=20.0)`.
   - Added `safe_upload_blob(client, img_data, desc, max_retries=3, delay=2.0)` which ensures timeout enforcement, up to 3 upload retries on network/server drops, and descriptive error logging with `str(e) or repr(e)` (preventing blank error messages from `InvokeTimeoutError`).
   - Replaced all image blob uploads in `post_thread()` (trajectory graph, 5-word card, verdict split card, analysis split card) with `safe_upload_blob`.
   - Ensured client timeout is set in `main()` upon client creation.
2. **`bluesky_bot/post_batch.py`**:
   - Explicitly configured `client.request._client.timeout = httpx.Timeout(60.0, connect=20.0)` immediately after `Client()` is instantiated.

## Verification
- Ran `python -m py_compile` across both modified files without error.
- Successfully verified live blob upload of `paramount_antitrust_settlement_graph.png` (520 KB) via `safe_upload_blob` with CID return:
  `bafkreib5f5zdk2lszvw6p3w3kdhf3b22aehvtntin2w4tglgfz5pfs52ua`.
- Running AletheiaLauncher processes were not touched or interrupted.
