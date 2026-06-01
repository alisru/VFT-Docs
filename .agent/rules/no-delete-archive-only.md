# No Delete — Archive Only

NEVER delete any file in this workspace. This is an absolute rule with no exceptions.

## What to do instead of deleting
- If a file is outdated: rename it with an `_archive_YYYYMMDD` suffix and move it to an `_archive/` subfolder next to the original.
- If a file is being replaced: keep the old version as `filename_v1.md`, `filename_v2.md` etc. before writing the new one.
- If a file is broken or corrupt: move it to `_archive/` with a note in the filename explaining why (e.g. `factcheck_broken_schema_20260602.json`).

## Git commits
After EVERY file edit, creation, or rename: run `git add -A` and `git commit -m "descriptive message"`.
Do NOT batch multiple sessions of edits into a single commit. Commit after each meaningful change so the history is recoverable.

## Why
Files get overwritten and lost permanently because AI agents assume they can delete safely. They cannot.
The archive approach means nothing is ever truly gone and history is always recoverable.
