# Implementation Plan v37 — Codebase Consolidation, Dead Code Purge & Clean Architecture

**Date:** 2026-11-07  
**Goal:** Clean up the sprawl in `bluesky_bot/`, isolate and retire 41+ redundant/dead scripts, eliminate duplicate split-brain engines, and establish a clean, strict modular structure with a single CLI entrypoint so the codebase never gets messy or chaotic again.

---

## 1. Inventory & Redundancy Audit

The root directory of `bluesky_bot/` currently has **87 Python scripts**, 17 files in `drawing_board/`, and duplicate rebuilder/patch scripts scattered everywhere. 

### Category A: The ONLY Files We Actually Need (Core Production Pipeline)
These are the permanent, production components of the bot:
1. **Harvester & Ingestion**:
   - `harvest_candidates.py` — RSS & Bluesky news harvesting, de-duplication, clustering.
   - `scraped_cache.py` — SQLite caching of article bodies.
   - `shard_manager.py` — Frontend JSON source text sharding.
2. **Evaluator & Math Engine**:
   - `google_ai_studio_one_shot.py` — 7-plane scan, 18-variable attractor calculation, story generator.
   - `actor_extract.py` — Actor name and 7-role extraction.
   - `policy_extract.py` — Policy topic and ideological stance mapping.
   - `validate_batch.py` — Pre-flight schema and format verification.
3. **Graph & Visual Cards**:
   - `generate_graph.py` — Hegemony vector field plot and deterministic trajectory resolver.
   - `image_card_generator.py` — 2-column and 5-word visual infographic card renderer.
4. **Publishing & Retraction**:
   - `aletheia_bot.py` — ATProto connection, 14-post thread chaining, image upload, rollback.
   - `post_batch.py` — Staged queue batch scheduler and poster.
   - `retract_story.py` — Errata retraction and correction reply poster.
   - `direct_reply_dispatcher.py` — Interactive reply dispatcher to user posts.
   - `delete_quarantined_bluesky_posts.py` — Clean batch deletion for quarantined threads.
5. **Registries & Services**:
   - `rebuild_registries_son.py` — Authoritative registry builder (consolidated with legacy rebuilder).
   - `export_audit_site.py` — Static site compiler.
   - `memory_store.py` — SQLite episodic and thread memory.
   - `chat_server.py` — Local web dashboard backend.
   - `source_server.py` — Local source snippet server.
   - `aletheia_mcp_server.py` — FastMCP server for AI agent queries.
6. **Launcher**:
   - `AletheiaLauncher.pyw` — Desktop GUI launcher (fixed for stream bottlenecks and venv paths).

---

### Execution Status Log:
- **Phase 1 (Surgical Bug Fixes)**: **COMPLETED**.
  * Agent A (Ingestion): Fixed Australia `.com.au` unscrapable block, Tavily knowledge leaks, slug title fallbacks, topic regex word boundaries.
  * Agent B (Math & Trajectory): Fixed canonical $4 \times 4$ geodesic lookup matrix (GG $\to$ LG = "Fall from Grace", zero negative redemption), deadband neutral logic ($|u| \le 0.15$), SON force coordinate recalculation, full post trimming <= 280 chars.
  * Agent C (Visual & Publishing): Fixed multi-aspect 5-word row mappings, un-inverted QR codes (ISO/IEC 18004 compliant), fixed quarantine exclusion and `return net_forces` in `rebuild_registries_son.py`, fixed in-thread errata replies in `retract_story.py`, fixed `AletheiaLauncher.pyw` stream buffering and subprocess cp1252 encoding.
  * All 12 modified files compiled with 0 errors via `py_compile`.
- **Phase 2 (Safe Archival)**: **COMPLETED**.
  * 60 redundant/legacy patch and test scripts safely moved to `bluesky_bot/_Archive/legacy_patches/`.
  * `bluesky_bot/drawing_board/` cleared and moved to `bluesky_bot/_Archive/drawing_board/`.
  * Zero files were deleted.
- **Phase 3 (Unified CLI)**: **COMPLETED**.
  * Created `bluesky_bot/aletheia.py` providing unified CLI commands (`harvest`, `eval`, `post`, `render`, `retract`, `rebuild`, `status`).
  * Tested and verified operational.
- **Phase 4 (P0 Emergency Remediation — Zero Coordinate Overwrite Fix & Purge)**: **COMPLETED**.
  * Root cause diagnosed: Unconditional `calculate_son_coordinates` on default-initialized 0.0 force dictionaries was wiping `claim_u` and `real_u` to (0.0, 0.0), branding stories as "Greater Evil" and "Destruction".
  * Code fixed in `google_ai_studio_one_shot.py`: Multi-aspect evaluations now prioritize `aspects` array averaging (`mean(claim_u)`, `mean(real_u)`). `calculate_son_coordinates` is guarded by `_has_nz()` so zero forces cannot overwrite coordinates.
  * Code fixed in `rebuild_registries_son.py`: Coordinates are derived from `aspects` directly. Recalculation is strictly guarded by `_has_nonzero_forces()`. Matplotlib render bottleneck gated behind `REGEN_ALL_GRAPHS=1`.
  * Bluesky takedown: Deleted all 1,269 posts across 86 corrupted stories since `3mzp43plvg52e` via ATProto in reverse order (100% clean).
  * Draft restoration: All 86 stories returned to `stories/drafts/` with their authentic coordinates restored from `aspects` and post text repaired.
  * Archive restored: 5,346 historical disk files recovered from `aspects`. Remaining live zeros reduced from 5,719 to 373 baseline neutral stories.

### Category B: Redundant & Conflicting Files to Consolidate
These files duplicate existing functionality or create split-brain divergence:
1. **`rebuild_registries.py`**:
   * *Conflict*: Diverged duplicate of `rebuild_registries_son.py`. Lacks 18-variable attractor calculations and spiritual tradition tagging. Different scripts import different ones!
   * *Action*: Merge any unique roundup logic into `rebuild_registries_son.py`, rename to `rebuild_registries.py`, and remove the duplicate.
2. **`expand_harvested_with_multisources.py`**:
   * *Conflict*: Uses Google News redirect links (`news.google.com/rss/articles/...`) that hit botwalls, and overwrites the multi-source clustering already performed by `harvest_candidates.py`.
   * *Action*: Retire to `_Archive/`.
3. **`build_source_shards.py`**:
   * *Conflict*: Duplicates the sharding logic inside `shard_manager.py`, but with different key formats.
   * *Action*: Retire to `_Archive/`; use `shard_manager.py` exclusively.
4. **`reply_to_post.py`**:
   * *Conflict*: 104-line proof-of-concept with hardcoded `motherjones.com` target URL. Duplicates `direct_reply_dispatcher.py`.
   * *Action*: Retire to `_Archive/`.
5. **`test_quadrant_outlets.py`**:
   * *Conflict*: 95% identical duplicate of `test_complete_quadrant.py`.
   * *Action*: Retire to `_Archive/`.
6. **`regenerate_draft_graphs.py` & `regenerate_info_cards.py`**:
   * *Conflict*: 30-line batch loops that ignore `stories/live/`.
   * *Action*: Replace with a unified CLI command `aletheia render --all`.

---

### Category C: Dead One-Off Patch, Hotfix & Scratch Scripts (41 Files to Move to `_Archive/`)
These were created during past emergency fixes or single-issue migrations. They are dead, dangerous, or cluttering the workspace:
* **One-off corrections & hotfixes**:
  `apply_seyfried_fix.py`, `patch_rebuild.py`, `update_girlboss.py`, `fix_syntax.py`, `post_seyfried_correction.py`, `post_talarico_correction.py`, `apply_potential_update.py`, `apply_domain_diversity.py`, `patch_control_panel.py`, `patch_generate_graph.py`, `patch_google_one_shot.py`, `patch_pipeline.py`, `post_correction.py`, `post_full_redone_thread.py`, `clean_and_redo_bad_stories.py`.
* **One-off backfills & migrations**:
  `populate_harvested_log.py`, `backfill_harvested_history.py`, `migrate_actor_roles.py`, `move_reaudited_to_drafts.py`, `quarantine_staged_queue.py`, `remediate_draft_stories.py`, `remediate_tabloid_corrections.py`, `repair_failed_stories.py`, `reset_roundups.py`, `fix_all_paper_maps.py`, `fix_roundups.py`, `consolidate_roundups.py`.
* **Ad-hoc exploratory / dead test scripts**:
  `test_calibration_prompt.py` (broken path), `test_moral_prompt.py`, `test_blame.py`, `test_clustering_standalone.py`, `test_full_extract.py`, `research_probe.py`, `scan_churn.py`, `scan_last_100_live.py`, `screen_live_partisan_stories.py`, `bof_exact.py`, `check_db.py`, `check_log.py`, `find_all_in_log.py`, `get_full_log_stories.py`, `list_drafts.py`, `make_doc.py`, `match_stories.py`, `parse_archive_logs.py`, `update_scrapers_boilerplate.py`, `audit_crossref.py`, `audit_duplicates.py`, `audit_past_200.py`, `audit_right_wing_queue.py`, `compile_paper.py`, `generate_paper_file.py`, `reaudit_live_batch.py`, `reaudit_new_suspects.py`.
* **Stale Drawing Board Folder**:
  `bluesky_bot/drawing_board/` (all 17 files violated user workspace rules and must be archived).

---

## 2. Proposed Target Architecture: The Clean Modular Blueprint

To prevent `bluesky_bot/` from ever turning into a chaotic dumping ground again, the codebase will be organized into clear functional layers:

```
bluesky_bot/
│
├── aletheia.py                    # THE ONLY ENTRYPOINT: Unified CLI router
│                                  #   aletheia harvest  [--rss N] [--bsky N]
│                                  #   aletheia evaluate [--model ...] [--live]
│                                  #   aletheia post     [--folder ...] [--live]
│                                  #   aletheia render   [--graphs] [--cards]
│                                  #   aletheia retract  <story_id>
│                                  #   aletheia rebuild  [--clean]
│
├── AletheiaLauncher.pyw           # Desktop GUI launcher (calls aletheia.py CLI)
│
├── config/                        # Canonical, single-source-of-truth configuration
│   ├── banned_topics.json         # Audited category and topic banlist
│   ├── unscrapable_domains.json   # Cleaned scraper banlist (Australia & Wires restored)
│   └── outlet_bias.json           # Known media outlet ratings & bias families
│
├── core/                          # The 5 Core Pipeline Engines
│   ├── __init__.py
│   ├── harvester.py               # News & Bluesky harvester + topic clustering
│   ├── evaluator.py               # 7-plane AI Evaluator & 18-variable attractor calculus
│   ├── publisher.py               # ATProto thread posting, validation & rollback
│   ├── visualizer.py              # Vector field graph & infographic card rendering
│   └── registries.py              # Consolidated, authoritative registry generator
│
├── storage/                       # Data persistence & caches
│   ├── __init__.py
│   ├── cache.py                   # SQLite article cache & source shards
│   └── memory.py                  # Episodic & thread conversational memory
│
├── servers/                       # Network Interfaces & APIs
│   ├── chat_server.py             # Web dashboard API
│   ├── source_server.py           # Local source snippet server
│   └── mcp_server.py              # Aletheia FastMCP server
│
├── tests/                         # Automated test suite (no loose test_*.py in root)
│   ├── test_trajectories.py       # Trajectory geodesic invariants
│   ├── test_attractors.py         # 18-variable attractor calculus tests
│   └── test_sourcing.py           # News URL validation & domain filter tests
│
├── stories/                       # Story Lifecycle Directories
│   ├── darkroom/                  # Staged raw candidate evaluations
│   ├── drafts/                    # Reviewed/edited candidate stories
│   ├── live/                      # Successfully published Bluesky stories
│   └── quarantine/                # Retracted or quarantined stories
│
└── _Archive/                      # Safe burial ground for retired legacy scripts
    ├── legacy_patches/            # The 41 retired one-off fix/patch scripts
    └── drawing_board/             # Stale scratch files moved out of root
```

---

## 3. Four-Phase Execution Roadmap

### Phase 1: Surgical Fixes on Core Pipeline Files (Zero Structural Move Yet)
Before moving files into folders, fix the active P0 bugs in place so current scripts work properly:
1. **`unscrapable_domains.json`**: Remove `"com.au"`, `"reuters.com"`, `"bloomberg.com"`, `"nytimes.com"`, `"wsj.com"`, `"ft.com"`.
2. **`harvest_candidates.py`**:
   - In `search_counter_sources_tavily()`: filter through `is_news_url()` and ban `tavily.com`.
   - In `is_news_url()`: reject bare root domains (`path in ('', '/')`) and add corporate/SaaS path filtering.
   - In `cluster_candidate_stories()`: remove `or len(intersection) >= 2`.
   - In `scrape_via_tavily()`: derive title from URL slug instead of hardcoded `"Article"`.
3. **`generate_graph.py`**:
   - Replace Cartesian concatenation with the canonical $4 \times 4$ geodesic trajectory matrix (eliminating `"Fall into Redemption"`).
   - Add neutral deadband ($|u| \le 0.15$) so neutral news is not branded `"Destruction"`.
   - Fix unreachable dead code in `enforce_deterministic_trajectory()`.
4. **`rebuild_registries_son.py`**:
   - Fix orphaned `return` inside helper function so `stated_forces` and `actual_forces` are never wiped with `None`.
   - Derive zone labels dynamically on recalculation.
5. **`retract_story.py`**:
   - Fix errata posting to reply to the original root post CID instead of broadcasting top-level.
6. **`AletheiaLauncher.pyw`**:
   - Fix character-by-character stream bottleneck (`read(1)` $\to$ `readline()`).
   - Fix relative `.venv` resolution and relative icon paths.

### Phase 2: Safe Archival of the 41 Dead/Patch Scripts
Per user safe-deletion rule:
- Present the exact list of 41 files to be moved to `bluesky_bot/_Archive/legacy_patches/`.
- No files are deleted (`Remove-Item` is banned); they are moved safely into `_Archive/`.
- Clear out `bluesky_bot/drawing_board/` into `_Archive/drawing_board/`.

### Phase 3: Consolidate Split-Brain Scripts
- Merge `rebuild_registries.py` and `rebuild_registries_son.py` into a single authoritative rebuilder.
- Retire redundant wrappers (`regenerate_draft_graphs.py`, `regenerate_info_cards.py`, `expand_harvested_with_multisources.py`, `reply_to_post.py`).

### Phase 4: Create the Unified CLI (`aletheia.py`)
- Build a clean `argparse` router (`bluesky_bot/aletheia.py`) with subcommands:
  - `aletheia harvest`
  - `aletheia eval`
  - `aletheia post`
  - `aletheia render`
  - `aletheia retract`
  - `aletheia rebuild`
- Update `AletheiaLauncher.pyw` buttons to call `aletheia.py <subcommand>` uniformly.

---
*Plan recorded in `bluesky_bot/_AI_Project_Plans/implementation_plan_v37_codebase_consolidation_and_architecture_cleanup.md`.*
