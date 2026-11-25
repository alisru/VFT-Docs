# Walkthrough / running log — repo master doc

## 2026-10-04
- Plans: `implementation_plans/plan_v1`, `plan_v2`.
- Phase 1 done: `inventory/files_functional.csv` (815 functional files; excludes .git, .venv, __pycache__, dist_audit_site).
- Phase 2 pass 1 done: `inventory/headers.tsv` = first comment line per file (222 had none).
- Phase 4 draft 1: `REPO_MASTER.md` written. Tags: [read] = from docstring/title, [name] = from filename/first line only.

## Still unchecked (next session)
1. Confirm [name] entries by reading code: root `convert_io_to_md.py`, `sync_gdrive_io.bat`, `Repair-Docs.ps1`, `bulk_extract_media.py`, `.agent/scripts/*`, `Semantic_Clusters` v2 pipeline order and NotebookLM tools.
2. Check what calls what (grep .bat/.ps1 -> .py) and fill the "called by" column.
3. `bluesky_bot` main flow: aletheia_bot.py -> harvest -> post_batch; confirm which are live vs `_Archive`.
4. Not inventoried: `.json` config/data files, `.md` docs (out of scope), `.png`, media.
5. Phase 5: add a rule to AGENTS.md so new scripts get a row (needs user OK).
6. Open decisions for user: hard-coded Qdrant key; duplicate files/folders (flag only).
