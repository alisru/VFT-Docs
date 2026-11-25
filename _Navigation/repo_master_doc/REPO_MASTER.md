# REPO MASTER — functional files (scripts, apps, data stores)

Scope: every non-document file in `VFT Docs` (815 functional files: `.py` `.pyw` `.js` `.html` `.css` `.cs` `.bat` `.ps1` `.sh` `.db` `.sqlite` `.lnk` `.yaml`). The `.md` / `.docx` documents are NOT covered here. Excluded from the list: `.git`, `.venv`, `__pycache__`, `dist_audit_site`.
Raw lists: `_Navigation/repo_master_doc/inventory/files_functional.csv` (path, ext, size, date) and `headers.tsv` (first comment line of each file).

**Confidence key**
- **[read]** = purpose taken from the file's own docstring or title.
- **[name]** = purpose inferred from the filename and first lines only. Not yet confirmed by reading the code.
- **Status:** live = in use / has launcher; legacy = replaced or one-off already run; unknown = could not tell.

Last updated: 2026-10-04 · Draft 1 (see `walkthrough.md` for what is still unchecked)

---

## 1. The big picture (what this repo is)

A research repo for "Vector Field Theory" (VFT): a body of writing (`_VFT MD`), plus the code around it. The code falls into 8 jobs:

1. **Document handling:** convert, sort, index and summarise the writing (root scripts, `io/`, `_VFT MD/System`).
2. **Semantic search:** embed the writing into a vector DB and search it (`Semantic_Clusters`, `chat_context`, `_AI files and chat logs`).
3. **Aletheia bot:** finds news posts, audits them against the framework, posts replies on Bluesky (`bluesky_bot`).
4. **Kanon audits:** score a politician or nation against the 343-vector Kanon, with quote checking against Hansard (`_VFT MD/WWSUTRU/...`).
5. **Dictionaries and engines:** QQCI word dictionary, Reality Classification v1/v2, IRM physics model (`Reality Class'ification project`, `Reality Classification v2`, `io/irm`).
6. **Visualisers:** interactive HTML graphs and 3D models (`Visualisers`, `hegemony_attractor`, `_Personal_Files`, root `*.html`).
7. **Video / YouTube production:** transcribe, make cards, upload (`_AI files and chat logs/Videos`).
8. **Browser extensions and agent tooling:** `gemini-latex-exporter`, `claude-artifact-sort`, `.agent`, `.agents`.

---

## 2. Folder map (functional content only)

| Folder | Point | Functional files |
|---|---|---|
| (root) | Sync/launch/summary scripts and shared data (see §3) | ~60 |
| `.agent/` | Local agent tooling: IO processing, missing-summary finders, task manager, one scratch folder | 14 |
| `.agents/` | Agent config (`config.yaml`); skills and rules live here too (markdown) | 1 |
| `_VFT MD/` | The main document library. Functional files inside are audits, site generators, Hansard tools, physics scripts | 279 |
| `bluesky_bot/` | Aletheia Bluesky bot, its servers, stores, tests, archive | 116 |
| `_AI files and chat logs/` | Old working area: dictionary/index/VDB scripts, plus the YouTube production tools in `Videos/` | 89 |
| `_Personal_Files/` | Personal side projects: 3D Tao ring, 650-statements grid, Claude artifact sorter extension, small visualisers | 68 |
| `Reality Class'ification project/` | Original QQCI dictionary, C# prototypes, Python `qqci/` and `irm/` experiments | 60 |
| `Semantic_Clusters/` | Embed and cluster the writing, NotebookLM batch tools, Qdrant sync, **VFT MCP server** | 42 |
| `drawing_board/`, `chat_context/drawing_board/` | Throwaway test scripts (feeds, graphs, regeneration tests) | 17 + 6 |
| `chat_context/` | Local "chat notebook": imports AI chat exports, embeds, topic clusters, dashboard at a local server | 17 |
| `gemini-latex-exporter/` | Chrome extension that exports Gemini chats with LaTeX; plus saved test pages | 16 |
| `Reality Classification v2/` | Rebuilt dictionary (AEC = Action–Effect–Context) with build and prune scripts, viewer | 14 |
| `io/` | Landing folder for new files + IRM physics model (`io/irm`) | 13 |
| `WWSUTRU/` | Early Kanon pages (American, Australian) + one extract script | 9 |
| `hegemony_attractor/` | Attractor map HTML, with 6 saved edit copies | 7 |
| `Actualism/` | Interactive pages and C# files for soul/belief states | 5 |
| `Visualisers/` | Standalone visualisers (polytrope, triangles, Basileia sim) | 5 |
| `test code memory/` | A `code_memory.db` test copy | 1 |
| Folders with **no** functional files found | `Altruistic Leaders`, `Log for review`, `Muses`, `Physics`, `Protocols`, `geometry of definitions`, `there was an attempt`, `Google`, `_Archive`, `_Generated_Content`, `_Navigation`, `drawing board` (with a space) | 0 |

> Flag: `drawing board` (space) and `drawing_board` (underscore) both exist. Only the underscore one holds scripts.

---

## 3. Root-level files

### 3a. Document pipeline and summaries
| File | What it does | Status |
|---|---|---|
| `convert_io_to_md.py` | Converts new files dropped in `io/` to markdown [name] | live |
| `sync_gdrive_io.bat` | Syncs the `io` folder with Google Drive [name] | live |
| `Move-IOFiles.ps1` | Moves processed `io` files into the document library [read] | live |
| `Move-42Files.ps1`, `Move-MoralityFiles.ps1` | One-off moves of named file groups; the second also syncs docs [read] | legacy |
| `Convert-ShadowRepo.ps1` | Converts the Docx "shadow repo" to markdown with Pandoc [read] | unknown |
| `Repair-Docs.ps1` | Repairs documents (details not confirmed) [name] | unknown |
| `Sync-Docs.ps1`, `Sync.bat` | Sync documents with a remote using rclone (`Sync.bat` runs a dry run first) [read] | live |
| `Push.bat` | Git push helper, starts with a dry run [read] | live |
| `cleanup_structure_v2.py`, `audit_structure.py` | Reorganise folders / audit folder layout; outputs are `cleanup_report.md`, `audit_report.md` [name] | legacy |
| `bulk_extract_media.py` | Pulls embedded media out of documents [name] | unknown |
| `vft_summarizer_v2.py` | Summarises each `.md` and tags it from a fixed tag list [read] | live |
| `batch_summarize_local.py`, `run_batch_summarizer.bat` | Runs the summariser in batches locally [name] | live |
| `discover_unsummarized.py` | Finds `.md` files that have no entry in the summaries file [read] | live |
| `Heal-Summaries.ps1` | Fills in missing summaries [read] | live |
| `append_vft_summaries.py`, `append_vft_batch_swarm.py`, `append_vft_wwsutru_batch_1.py`, `append_vft_wwsutru_batch_2.py` | Hold hand-written summaries as data and append them to `file_summaries.md`. Already run [read] | legacy |
| `convert_summaries_to_db.py` | Loads `file_summaries.md` into `file_summaries.db` [name] | live |
| `file_summaries.db` | Database of file summaries for the `.md` documents | live |
| `file_summaries_data.js`, `file_summaries_viewer.html` | Browser viewer for those summaries and the data it reads [read] | live |
| `Master_Index.html` | Master project index / search page (also at `_VFT MD/System/Master_Index.html`) [read] | live |
| `code_memory.db` | Store for the "code-memory" MCP (copies in `io/`, `_VFT MD/io/`, `test code memory/`) [name] | unknown |

Related non-code files at root: `file_summaries.md/.json/.bak/_fixed.md`, `file_list.txt`, `batch_*`, `next_100_*`, `raw_*` are lists and old copies of the same job. Not functional; flagged as clutter.

### 3b. Bluesky bot launchers
| File | What it does | Status |
|---|---|---|
| `AletheiaLauncher.pyw` | Windows launcher (no console) for the bot UI [read] | live |
| `AletheiaLauncher.pyw - Shortcut.lnk`, `alethekanon.exe.lnk` | Shortcuts to the launcher [name] | live |
| `Run-AbskyBotControlPanel.bat` | Starts the control panel [name] | live |
| `Run-BskyBotOneShotBatch.bat` | Runs one batch of the bot [name] | live |
| `Post-LiveBatch.ps1`, `Post-LiveBatch-bsky.bat` | Posts a batch live; asks for min/max delay between threads [read] | live |
| `rebuild_store.bat` | Rebuilds the bot's memory store (copy also in `bluesky_bot/`) [name] | unknown |

### 3c. Data and visual files
| File | What it does | Status |
|---|---|---|
| `hegemony_db.js` | Pre-seeded database for the Psochic Hegemony visualiser [read] | live |
| `hegemony_db - Copy.js` | Older copy of the above | legacy |
| `hegemony_word_meaning_graph.html` | Graph of hegemony words and their meanings [read] | live |
| `qqci_dictionary.js` | Auto-generated from `qqci_dictionary.json`; do not edit by hand [read] | live |
| `simulate_homogeneous_scope.py` | Simulation that made `homogeneous_scope_subdivision.gif` [name] | legacy |
| `scratch.py` | Scratch file [name] | likely dead |

---

## 4. `.agent/` and `.agents/`
| File | What it does |
|---|---|
| `.agent/scripts/Get-New-Summaries.ps1` | Lists summaries added recently [name] |
| `.agent/scripts/Process-IO-Files.ps1` | Processes files landing in `io/` (convert, sort) [name] |
| `.agent/tools/find_missing_summaries.py`, `_smart.py`, `_v2.py` | Three generations of "which files have no summary" finders. `_smart` also handles repeated filenames [read] |
| `.agent/tools/read_batch_chunk.py`, `read_batch_content.py` | Read a chunk of a batch list and print file contents for summarising [read] |
| `.agent/tools/alethekanon_judge.py` | Simple word-list scorer using the Alethekanon dictionary [read] |
| `.agent/tools/task_manager/task_manager.py`, `conversation_archaeology.py` | Task state engine ("No More Fuckups Task Engine") and a tool for recovering past chats [name] |
| `.agent/temp/*.py` (4 files) | One-off edits to the summaries file. Legacy |
| `.agents/config.yaml` | Agent config |

---

## 5. Semantic search and clustering

### `Semantic_Clusters/`
**MCP server (not a loose script):**
- `vft_mcp_server.py` — MCP server "VFT Corpus & Vector DB" (tool names in the agent: `search_semantic_clusters`, `get_topic_clusters`, `search_archive_logs`, `get_archive_file`). Searches the Qdrant collection `vft_paragraphs` and the bot memory store. **Flag: Qdrant API key is hard-coded in the file.**

**Numbered rebuild pipeline (run in order):** [name]
`v2_00_corpus_manifest.py` → `v2_01_sentence_extract.py` → `v2_02_embed.py` (keeps a checkpoint of chunks) → `v2_03_layer_tag.py` → `v2_04_bertopic.py`

**Vector store:** `sync_to_qdrant.py` recreates the Qdrant collection (384-dimension MiniLM) and uploads paragraphs [read]. `test_qdrant_search.py`, `test_find_vector.py`, `test_get.py`, `test_parser.py` are checks.

**NotebookLM batch tools** [name]: `generate_notebooks.py` (sorts documents into notebook groups; skips drafts/archives/duplicates), `batch_upload_notebooks.py`, `align_manifests.py`, `analyze_google_notebooks.py`, `deduplicate_notebook_sources.py`, `initialize_filelists.py`, `subtraction_test_notebooks.py`, `reset_ids.py`, `list_notebooklm_tools.py`, `scan_gdrive_metadata.py`.

**Analysis:** `classify_documents.py` (scores documents against 16 hegemony points) [read]; `cluster_topics.py`, `analyse_semantic_topics.py`, `generate_literal_topic_analysis.py`, `generate_philosophical_tags.py`, `analyze_vdb_categories.py`, `inspect_clusters.py`, `document_coherence_analyzer.py`, `compile_granular_sentences.py`, `categorize_files.py`, `pipeline_prepare.py` [name]; `harvest_coherent_compilation.py` and `harvest_hegemony_treatise.py` pull relevant paragraphs from the vector DB to build compilation documents [read].

**Housekeeping:** `find_workspace_duplicates.py`, `cleanup_plans.py`, `merge_geometry_of_definition.py`, `repair_latex.py`, `inspect_docx.py` [name].

**Viewer:** `viewer.html` (Semantic & Graph Explorer), `start_viewer.py` (local server for it), `run_viewer.bat` [read].

### `chat_context/`
Local searchable archive of AI chats. `ctx/ingest.py` + `importers.py` read chat exports; `embed.py` chunks and embeds them offline; `topics.py` clusters; `server.py` is a FastAPI server with dashboard `ui/index.html`; data in `data/chats.sqlite`; `extension/gemini_sync_userscript.js` is a browser userscript that syncs Gemini chats in; `start_chat_context.bat` starts it. `drawing_board/` there holds clustering tests. [read]

### `_AI files and chat logs/` (old working area)
- **Index/search:** `generate_vft_index.py`, `search_vft_index.py`, `simple_search.py` [name]
- **Vector DB:** `vdb_harvest.py`, `vdb_ingest_project.py` (+ `_DRAFT`), `ingest_tautonic.py`, `query_qdrant.py`, `inspect_vdb_obj.py`; data in `vdb_data/` (210 MB) and `test_vdb_data/` [name]
- **Clean-up and moves:** `move_to_io.py`, `move_loose_files_v2.py`, `process_io_files.py`, `clean_io_duplicates.py`, `find_duplicates_and_overlaps.py`, `mirror_purge.py`, `restore_files.py`, `restore_structure.py`, `audit_non_md.py` [name]
- **LaTeX repair:** `remediate_latex.py`, `fix_latex_script.py`, `fix_fractal.py`, `fix_anahole.py` [name]
- **Tautonic / causal words:** `extract_tautonic.py`, `batch_tautonic_all.py`, `build_word_causal_db.py`, `build_symbol_table.py`, `extract_judgment_word_tags.py`, `extract_all_unique_tags.py` [name]
- **Other:** `extract_full_chat.py`, `extract_docx_media.py`, `generate_bertopic_clusters.py`, `generate_topic_review.py`, `soft_graph_manager.py`, `split_master.py`, `batch_regenerate_graphs.py`, `debug_*`, `test_api_connection.py`
- `Hegemony_Graph/hegemony_graph.html` — graph page

---

## 6. Aletheia bot (`bluesky_bot/`)

| File | What it does |
|---|---|
| `aletheia_bot.py` | Main bot logic [name] |
| `harvest_candidates.py`, `search_bsky.py`, `research_probe.py` | Find news posts on Bluesky; research probe targets a topic or period [read] |
| `google_ai_studio_one_shot.py` | One-shot audit generation via Google AI Studio (calls an API; do not run without asking) [name] |
| `post_batch.py`, `direct_reply_dispatcher.py`, `reply_to_post.py` | Post threads / reply to one target post [read] |
| `validate_batch.py`, `audit_duplicates.py`, `consolidate_roundups.py`, `fix_roundups.py`, `reset_roundups.py` | Check batches, remove duplicates, merge roundups [name] |
| `actor_extract.py`, `policy_extract.py` | Rules-based (no AI) actor and policy extraction from stories [read] |
| `audit_crossref.py` | Search engine over the 10,800+ audit entries [read] |
| `generate_graph.py`, `image_card_generator.py`, `regenerate_draft_graphs.py`, `regenerate_info_cards.py`, `generate_paper_file.py`, `make_doc.py`, `export_audit_site.py` | Make graph images, info cards, documents, static audit site [read/name] |
| `chat_server.py`, `aletheia_chat.html`, `launch_chat.bat` | Local chatbot server and its page [read] |
| `control_panel.html`, `launch_panel.bat`, `source_server.py` | Control panel and thread viewer; `source_server.py` serves sources from an in-memory index [read] |
| `aletheia_mcp_server.py` | **MCP server "Aletheia Bot"**: audits, hypocrisy leaderboards, chat memory [read] |
| `memory_store.py` + `memory_store.sqlite` | Local SQLite+FTS memory engine for bot and archive [read] |
| `scraped_cache.py` + `scraped_articles_cache.sqlite` (91 MB) | Cache of scraped articles [read] |
| `parse_archive_logs.py` | Parse archive logs [name] |
| `rebuild_registries.py`, `rebuild_registries_son.py`, `stories_registry.js` (62 MB) | Rebuild the story registry the panel reads; `_son` is the 6-attractor variant [name] |
| `backfill_harvested_history.py`, `populate_harvested_log.py`, `expand_harvested_with_multisources.py`, `get_full_log_stories.py`, `match_stories.py`, `find_all_in_log.py`, `check_db.py`, `check_log.py`, `list_drafts.py`, `remediate_draft_stories.py`, `repair_failed_stories.py` | Log/draft maintenance helpers [name] |
| `run_full_vanilla_benchmark.py` | Benchmark run [name] |
| `test_*.py` (7) | Ad-hoc tests |
| `scripts/` (9) | Actor-map checks and draft-duplicate tools; `delete_bolton_post.py` deletes a posted item |
| `tests/` (13) | Tests for convergence, banlist, memory, info cards, etc. |
| `_Archive/` (36) | Old batch pipeline from earlier versions (orchestrator, worker evals, batch generators). **Legacy** |
| `dist_audit_site/` | Exported static site (excluded from this inventory) |

---

## 7. Kanon audits (`_VFT MD/WWSUTRU/`)

| Area | What it holds |
|---|---|
| `America/` (≈60) | Scripts that built the American Kanon and Trump audit: plane fixers (`fix_plane_6/7`, `refine_*`, `hard_reset_planes`), score updaters (`update_*`), site generators (`generate_kanon_site.py`, `generate_trump_site.py`), nav patchers, and the output sites `site/` and `trump_site/` (7 plane pages each). Legacy once pages were built. |
| `Australia/` | `reorder_kanon.py`, `verify_kanon_rules.py`, `debug_regex.py` (empty), plus `site/` (generated Australian Kanon pages and `generate_pages.py`) |
| `Australia/Aus_Kanon/` | Kanon JSON tools: `kanon_manager.py`, `validate_kanon.py`, `verify_compact_kanon.py`, `migrate_kanon.py`, `audit_kanon.py`, `generate_kanon_template.py` [name] |
| `Aus_Kanon/hansard/` | **Local Hansard corpus**: `harvest.py` (download XML) → `parse.py` (paragraph parquet) → `members.py` (speaker lookup) → `index.py` (search index) → `search.py`; `sources.py` (non-chamber source archive and quote check), `verify_quotes.py` (gate for audit documents), `propose_fixes.py` (suggests fixes for near-miss quotes); **`hansard_mcp.py` is the Hansard MCP** [read] |
| `Aus_Kanon/compact JSON/` | Scrapers: `hansard_scraper.py`, `aph_scraper.py`, `news_quote_scraper.py`, `search_oa.py`, `query_hansard_corpus.py`, GUI `hansard_gui.pyw` + `Launch Hansard Scraper.bat` [name] |
| `Aus_Kanon/Audits/Albo_Audit/` | `dump_best.py`, `find_quotes.py`, and `drawing_board/` (≈35 one-off quote/URL finders) |
| `Aus_Kanon/Audits/Hanson_Audit/` | Hanson audit dashboard (`index.html`), `fetch_archive.py`, and `quote_db/` — a quote verification DB (`quote_verification.db`, 1.6 MB) with builder, CLI (`db_cli.py`), dashboard, and about 60 `_fix_batch*.py` / `_check_*.py` one-offs that were run once to load sources. |
| `Aus_Kanon/Audits/Hanson_Audit_AI_Logs/` | Remediation and mapping scripts used to rebuild the Hanson audit plane by plane; `generate_website.py` builds the site; ~50 small inspect scripts. Legacy. |
| `Aus_Kanon/Audits/Hanson_Audit_Website/` | Built Hanson site (index, about, archetype, 7 plane pages) |
| `Collapse/Taxonomy/` | `generate_matrix_md.py`, `sort_matrix.py` |
| `KineticMilitaryAttrition/` | One HTML page |
| other | `extract_bread_final.py`, `search_bread_json.py`, `search_vdb_bread.py` (bread-topic search scripts) [name] |

**MCP config note:** `Aus_Kanon/.mcp.json` registers only `hansard`, and only applies when the editor opens that folder.

---

## 8. Dictionaries and engines

| Folder | What it holds |
|---|---|
| `Reality Class'ification project/` | `qqci_dictionary.js` (+`_v2`) and viewers (the 44-word QQCI dictionary); `.cs` C# prototypes (`FieldMath`, `StateVector`, `SAELIntegration`, `{Idea}`, `{Meaning}`, `Optimism`/`Pessimism`, etc.); `obj/` build output; `qqci/` (≈30 Python experiments: engine, tautonic, slots, validate_depth, `vft.py`, `qqciformer.py`); `irm/` (5 files, copy of `io/irm`); `_AI files and chat logs/` (dictionary build/validate scripts) [read/name] |
| `Reality Classification v2/` | AEC dictionary: `aec_dictionary.js`, `build_v2_js.py`, `migrate_v1_to_v2.py`, `grow_simplify_prune.py`, `execute_evolution_pass.py`, `epistemic_hunter_pipeline.py`, `find_semantic_voids.py`, `pdp_engine.py`, `validate_v2.py`, `viewer_v2.html` [name] |
| `io/irm/` | IRM physics model: `irm_engine.py`, `gauge.py`, `regularization.py`, `eng3_decay.py`, `eng4_realmodel.py`, `semantic_connection.py`, `orthodox_bridge.py`, `base_systems.py`, `paper1_s5_levicivita.py` [name] |
| `io/` others | `merge_similar_docs.py`, `God.cs`, `GodAndSoulExamples.cs` |
| `Actualism/`, `_VFT MD/Actualism/`, `_VFT MD/*.cs` | Soul/belief-state C# models and interactive pages (`StatesofBelief.html`, `Hegemonic Stress Tensor.html`, 7x7x7 cube, Speciography) |
| `_VFT MD/Physics/` | `simulate_temporal_drag.py`, LaTeX fix scripts (`fix_latex.py`, `fix_escaped_brackets.py`), `truncate_monograph.py` |
| `_VFT MD/bible/` | `generate_numbers_31.py` (builds a Hebrew-verse study document), shrunk-source upload script, a transcriber copy |

---

## 9. Visualisers and personal projects
- `Visualisers/`, `hegemony_attractor/` (six map versions; `hegemony_attractor_map.html` is the master engine, the rest are copies/edits), `_AI files and chat logs/Hegemony_Graph`.
- `_Personal_Files/3D Printable Tao Ring/`: three.js models of a hegemony frame and Vitruvian figure for 3D printing; `start_server.bat`.
- `_Personal_Files/650 statements/`: political statement grid (generated from CSV by `generate_from_csv.py`) with launchers.
- `_Personal_Files/claude-artifact-sort-v16/`: Chrome extension that sorts Claude/Gemini artifacts (`content.js`, patch files, saved test pages). `content - Copy (10).js` and `patch*.js/ps1/py` are build steps and copies.
- `_Personal_Files/hegemony visualization/`, `image tag/`, `rate_my_australianness.py`: small standalone tools.
- `gemini-latex-exporter/`: Chrome extension (`background.js`, `content_gemini.js`, `style.css`, `generate_key.py`); the rest is saved test pages and DOM inspect scripts.

## 10. Video / YouTube production (`_AI files and chat logs/Videos/`)
Control panel (`server.py` + `video_control_panel.html`, started by `start_control_panel.bat`; data in `dashboard_data.js`, 2 MB). Transcribe (`yt_transcribe*.py`, `Run-TranscribeBatch.bat`), make covers/cards (`generate_covers.py`, `yt_overlay_text.py`, `Audios/create_*cards.py`), render (`render_video_*.py`, per-video `make_video.py`), upload and fix descriptions (`yt_upload.py`, `publish_videos.py`, `yt_update_desc.py`, `yt_auth.py`), audit what is uploaded (`audit_uploaded.py`, `full_audit_summary.py`, `rescan_youtube.py`), NotebookLM downloads (`download_via_chrome.py`, `sync_all_notebooks.py`). Also reads API keys from `bluesky_bot/.env`. `test_*.py` and `_test*.js` are checks. [read/name]

---

## 11. MCP servers in this repo
| Name | File | Registered? |
|---|---|---|
| `vft-vdb` | `Semantic_Clusters/vft_mcp_server.py` | Yes (per user, 2026-10-04) |
| `aletheia` | `bluesky_bot/aletheia_mcp_server.py` | Yes (per user) |
| `hansard` | `_VFT MD/WWSUTRU/Australia/Aus_Kanon/hansard/hansard_mcp.py` | Yes (per user) |

## 12. Flags (nothing changed; for the user to decide)
1. `vft_mcp_server.py` has a hard-coded Qdrant API key.
2. Duplicate folders: `drawing board` / `drawing_board`; duplicate `Master_Index.html`, `irm/`, `code_memory.db` copies, `hegemony_db - Copy.js`, six `hegemony_map*` variants.
3. Clutter at root: summary copies, batch lists, `scratch.py`.
4. Large data in the repo: `memory_store.sqlite` (21 MB), `scraped_articles_cache.sqlite` (91 MB), `stories_registry.js` (62 MB), `vdb_data` (210 MB), `_VFT MD/io/code_memory.db` (65 MB).
5. One-off script piles: Hanson `_fix_batch*` (~35), `Albo_Audit/drawing_board` (~35), `bluesky_bot/_Archive` (36), `America/` fixers.
