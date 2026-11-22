# Aletheia Bluesky Bot — Master Codebase Audit & Streamlining Report

**Date:** 2026-11-07  
**Scope:** `bluesky_bot/` project root, instructions, data stores, registries, and `AletheiaLauncher.pyw`.  
**Auditors:** 4 Parallel Audit Subagents + Primary Supervisor  
**Status:** Read-Only Line-by-Line Inspection Complete. No code or story files modified on disk.

---

## Executive Summary: The 5 Systemic Failures

The audit uncovered five critical architectural bugs that explain the recent pipeline anomalies (Frankenstein threads, Tavily commercial URLs, broken trajectories, and deleted vector forces):

1. **The Tavily Knowledge Graph Leak & Bare Domain Bypass**:
   `search_counter_sources_tavily()` never ran `is_news_url()` on results and had no check for `tavily.com`. Because `tavily.com` is unrated, it received bias family `'other'`, which bypassed family checks. Tavily's internal company database (`tavily.com/knowledge/company/...`) was ingested directly into dossiers. Simultaneously, `is_news_url()` had no check for empty paths or root `/`, allowing bare corporate sites like `http://Start.coop` to pass as news.
2. **The "Article" Title Collapse & Frankenstein Clustering**:
   `scrape_via_tavily()` returns `"Article"` as a fallback title when meta tags fail. In `cluster_candidate_stories()`, any story titled `"Article"` has a 100% token overlap with other `"Article"` stories. Furthermore, an over-permissive condition (`len(intersection) >= 2`) grouped completely unrelated articles (e.g. an Alaska Mpox outbreak, an election recount, and a White House arrest) into a single "multi-source topic cluster".
3. **The Accidental Australia & Wire Service Blacklist**:
   `unscrapable_domains.json` contained `"com.au"`, `"reuters.com"`, `"bloomberg.com"`, `"nytimes.com"`, and `"wsj.com"`. Because `is_news_url()` bans any domain where `host.endswith('.' + bad)` without checking the scraping whitelist, the bot **permanently banned every `.com.au` website in Australia** and blocked all major global wire services.
4. **Trajectory Invariant Breakdown ("Fall into Redemption")**:
   `get_path_name()` independently concatenated `exit_name` and `entry_name`. Any shift from Greater Good ($+u, +\psi$) to Lesser Good ($+u, -\psi$) produced the forbidden name **`"Fall into Redemption"`**. Furthermore, `enforce_deterministic_trajectory()` was never called in the live posting pipeline (`post_batch.py` or `aletheia_bot.py`), so unvalidated LLM trajectories went straight to Bluesky.
5. **Silent Vector Force Destruction During Registry Rebuild**:
   `calculate_aggregated_forces()` in `rebuild_registries_son.py` had an orphaned `return` statement inside an inner helper function, causing the outer function to return `None`. Whenever a story had sub-aspects, it evaluated to `None` and **permanently wiped out `stated_forces` and `actual_forces` on disk**.

---

## Part 1: Sourcing, Ingestion & Scraping Pipeline

### 1.1 Tavily Search Ingestion (`harvest_candidates.py:162–240`)
* **Root Cause**: `search_counter_sources_tavily()` queried Tavily with `{"topic": "news"}`. Tavily returned internal company intelligence entries (`https://tavily.com/knowledge/company/<id>`). The loop (lines 208–240) never called `is_news_url()`, never checked for `tavily.com`, and treated `tavily.com` as an `Independent / Unrated` news outlet.
* **Disk Artifacts Found**: `harvested_candidates.json` line 17 (`tavily.com/knowledge/company/okuqUb9qhOh2` as NHS counter-source) and `harvested_stories_log.jsonl` line 23502 (`tavily.com/knowledge/company/G5FXYj47VIG1` for Newcastle United).
* **Fix**:
  1. Add `tavily.com` and `api.tavily.com` to `NON_NEWS_DOMAINS`.
  2. In `search_counter_sources_tavily()`, require `is_news_url(r_url)` and explicitly reject `tavily.com`.
  3. Ensure Tavily is strictly a Level 4 last-resort fallback after local clusters, SQLite cache, and Google News RSS.

### 1.2 Bare Domain & Non-News Leak in `is_news_url()` (`harvest_candidates.py:727–749`)
* **Root Cause**: `parsed.path` for `http://Start.coop` is `""` or `"/"`. `path_parts` is `[]`, which bypassed `AD_OR_LIFESTYLE_PATH_SEGMENTS`.
* **Fix**:
  1. Require `len(path_parts) > 0` and reject `path in ('', '/', '/index.html', '/index.php')`.
  2. Add `CORPORATE_OR_NON_NEWS_PATHS` (`about`, `pricing`, `careers`, `terms`, `privacy`, `login`, `product`, `docs`, etc.).
  3. Require at least one substantial path slug (>3 chars) or date/id pattern.

### 1.3 Blacklist Disasters in `unscrapable_domains.json`
* **Root Cause**: Line 46 contains `"com.au"`. Lines 32, 134, 159, 227 contain `bloomberg.com`, `nytimes.com`, `reuters.com`, `wsj.com`.
* **Failure Mode**: `is_news_url()` line 743 checks `DYNAMIC_BANNED_DOMAINS` without checking the `SCRAPING_WHITELIST`. Any URL ending in `.com.au` was permanently rejected.
* **Fix**: Surgically remove `"com.au"`, `"reuters.com"`, `"bloomberg.com"`, `"nytimes.com"`, `"wsj.com"`, `"ft.com"` from `unscrapable_domains.json`. In `is_news_url()`, bypass dynamic bans if the domain is on the scraping whitelist.

### 1.4 The "Article" Title Fallback & Over-Permissive Clustering
* **Root Cause**: `scrape_via_tavily()` line 118 returns `"Article"` as the title. In `cluster_candidate_stories()` (lines 295–300), the condition `if jaccard >= similarity_threshold or len(intersection) >= 2:` merged any two stories with 2 common words or with the title `"Article"`.
* **Fix**:
  1. Derive fallback titles from the URL slug (e.g. `re.sub(r'[-_]+', ' ', path_slug).title()`), never `"Article"`.
  2. Remove `or len(intersection) >= 2`. Require `jaccard >= 0.40` AND at least 3 shared non-stopword tokens.

### 1.5 Regex & Keyword Flaws in `banned_topics.json`
* **Boundary Bug**: Line 77 has `"disney+"`. `\bdisney\+\b` fails to match `"watching disney+ tonight"` because `+` is a non-word character.
* **Overly Broad Filters**:
  - Line 79: `"review"` in entertainment rejects judicial reviews, budget reviews, and policy reviews.
  - Line 92: `"garden"` in gardening rejects "White House Rose Garden".
  - Line 97: `"style"` rejects "governance style".
* **Fix**: Use lookarounds `(?<!\w){re.escape(k)}(?!\w)` instead of `\b`. Narrow keywords to `"movie review"`, `"gardening"`, `"fashion style"`.

### 1.6 Supporting Cache & Server Issues
* **`scraped_cache.py:32` vs `harvest_candidates.py:847`**: Inconsistent URL normalization (one strips trailing slash, one does not), causing cache misses.
* **`scraped_cache.py:180–200`**: Crawls all files on disk on every cache miss (up to 25,000 JSON reads per run).
* **`shard_manager.py:136–148`**: Incompatible table schema drops `title`, `description`, and `scraped_at` on insert.
* **`source_server.py:24–37`**: Loads JSON log into memory once at startup; all newly harvested stories return 404 until server restarts. Binds to `"localhost"` instead of `"127.0.0.1"`.

---

## Part 2: AI Evaluator, Convergence Math & Prompt Engine

### 2.1 Calculated Attractor Forces Ignored at Generation Time (`google_ai_studio_one_shot.py:2354–2390`)
* **Root Cause**: The prompt extracts 18-variable attractor forces (`stated_forces`, `actual_forces`) alongside raw coordinates (`claim_u`, `real_u`, etc.). In `transpose_flat_to_json()`, the code stores the LLM's raw hallucinated coordinates directly and never invokes `calculate_son_coordinates()`.
* **Fix**: Import `calculate_son_coordinates` from `rebuild_registries_son.py` and recalculate `(claim_u, claim_psi)` and `(real_u, real_psi)` directly inside `transpose_flat_to_json()` before writing to disk.

### 2.2 Zone Label Desynchronization in Registry Rebuild (`rebuild_registries_son.py:220–224`)
* **Root Cause**: When recalculating `(real_u, real_psi)` from actual forces, coordinates update but the text label is recycled via `post.split("—")[-1].strip()`.
* **Fix**: Derive the zone label dynamically from the newly calculated coordinates.

### 2.3 Zero-Boundary Bias Branded Neutral News as "Destruction" (`generate_graph.py:30–41, 75–81`)
* **Root Cause**: Strict `real_u <= 0` with no deadband routed `real_u == 0.0` to `Destruction`, `Greater Evil`, and `Verdict: FAIL`.
* **Fix**: Introduce a neutral deadband ($|u| \le 0.15$ or $|u| \le 0.1$ and $|\Delta H| \le 0.3$) that routes to `Stasis` / `NEUTRAL` / `PASS`.

### 2.4 Lesser Good (+u, -ψ) Scored as FAIL (`policy_extract.py:179–181`)
* **Root Cause**: `verdict = "PASS" if (real_u >= 0 and real_psi >= 0) else "FAIL"`.
* **Fix**: Change to `verdict = "PASS" if real_u > 0.0 else ("CONDITIONAL" if abs(real_u) <= 0.1 else "FAIL")`.

### 2.5 Cross-Candidate Grounding URL Leak (`google_ai_studio_one_shot.py:3026–3037`)
* **Root Cause**: In batch evaluation, `primary_url = grounding_urls[0]` was assigned to every candidate in `parsed`.
* **Fix**: Key grounding URLs by candidate index or ID.

### 2.6 Schema Contradictions & Prompt Issues
* **Bold Markdown**: `google_ai_studio_one_shot.py:1364` used `**Social Physics Analysis:**`, while `thread_formatting_son.md:147` bans bold asterisks.
* **Post Truncation Budget**: `google_ai_studio_one_shot.py:2147–2156` only checked `range(min(4, len(clean)))`. Posts 4–12 were never auto-trimmed under 280 characters.
* **Non-Existent Fallback Models**: `DEFAULT_FALLBACKS` included `gemini-3.8-flash`, `gemini-3.5-flash`, `gemini-3.6-flash`.
* **Hardcoded Root Mode**: `google_ai_studio_one_shot.py:683, 1028` hardcoded `"mode": "root"`, preventing automated reply mode.

---

## Part 3: Graph Generation, Visual Cards & Publishing/Retraction

### 3.1 "Fall into Redemption" Bug (`generate_graph.py:14–46`)
* **Root Cause**: `get_path_name()` independently computed `exit_name` and `entry_name` based on quadrant signs:
  - $\text{GG} (+u, +\psi) \to \text{Fall}$
  - $\text{LG} (+u, -\psi) \to \text{Redemption}$
  - Result: `f"{exit_name} into {entry_name}"` $\to$ **`"Fall into Redemption"`**.
* **Fix**: Implement an explicit $4 \times 4$ geodesic lookup table:
  - $(\text{GG}, \text{LG}) \to$ `"Fall from Grace"`
  - $(\text{GG}, \text{GE}) \to$ `"Fall into Destruction"`
  - $(\text{GG}, \text{GL}) \to$ `"Fall into Deception"`
  - $(\text{GE}, \text{LG}) \to$ `"Reckoning into Redemption"`
  - $(\text{GL}, \text{GG}) \to$ `"Revelation into Grace"`

### 3.2 Dead Code in Trajectory Enforcement (`generate_graph.py:100–113`)
* **Root Cause**: Line 106 overwrote `t_lines[j]` with `The Trajectory: The Path of {math_path}.`, making lines 108–111 (`if "via Constructive" in t_lines[j]`) unreachable.
* **Fix**: Perform replacements before overwriting line content.

### 3.3 Trajectory Enforcement Never Called on Live Posts
* **Root Cause**: `enforce_deterministic_trajectory()` was not invoked in `post_batch.py` or `aletheia_bot.py`.
* **Fix**: Call `enforce_deterministic_trajectory()` during pre-flight thread validation in `aletheia_bot.py`.

### 3.4 Visual Card Row Shift on Multi-Aspect Stories (`image_card_generator.py:739–775`)
* **Root Cause**: `_generate_five_word_card()` used a static row array. When post 4 was `Sub-Audits Breakdown`, rows shifted by one, mislabeling all sections and dropping Brothekanon.
* **Fix**: Dynamically map posts by prefix/type instead of fixed row indices.

### 3.5 Errata Retraction Posted as Standalone Broadcast (`retract_story.py:114–134`)
* **Root Cause**: Called `client.send_post(text=errata_text)` without `parent_ref` or `root_ref`.
* **Fix**: Fetch root and parent post CIDs and pass `models.AppBskyFeedPost.ReplyRef` so the errata threads under the original post.

### 3.6 Untracked Ghost Posts on Network Failure (`aletheia_bot.py:799–808`)
* **Root Cause**: If mid-thread rollback deletion failed over a socket error, surviving posts were not saved to disk and became untracked ghost posts.
* **Fix**: Immediately record surviving orphan rkeys to `stories/quarantine/orphaned_{story_id}.json`.

---

## Part 4: Registries, Data Integrity & Codebase Sprawl

### 4.1 Destruction of Raw Vector Forces (`rebuild_registries_son.py:138–157, 183–189`)
* **Root Cause**: `calculate_aggregated_forces()` lacked an outer `return` statement; execution fell into `classify_spiritual_tradition`, leaving an orphaned return on line 157. It returned `None`, which overwrote `stated_forces` and `actual_forces` with `None` on disk.
* **Fix**: Properly return `net_forces` from `calculate_aggregated_forces()`.

### 4.2 Quarantine Leakage in Registry (`rebuild_registries_son.py:525–536`)
* **Root Cause**: Stories marked `"status": "QUARANTINED"` were bundled into `stories_registry.js`.
* **Fix**: Exclude any story with `"status": "QUARANTINED"` or located in `stories/quarantine/`.

### 4.3 Script Sprawl: 41 Obsolete / Throwaway Scripts
Out of 87 Python files in `bluesky_bot/`, 41 are one-off patches or redundant test scripts that should be retired to `_Archive/`:
- **One-off hotfixes**: `apply_seyfried_fix.py`, `patch_rebuild.py`, `update_girlboss.py`, `fix_syntax.py`, `post_seyfried_correction.py`, `post_talarico_correction.py`, `apply_potential_update.py`, `apply_domain_diversity.py`, `patch_control_panel.py`, `patch_generate_graph.py`, `patch_google_one_shot.py`, `patch_pipeline.py`.
- **Duplicate test / benchmark scripts**: `test_quadrant_outlets.py` (duplicate of `test_complete_quadrant.py`), `test_blame.py`, `test_clustering_standalone.py`, `test_full_extract.py`, `research_probe.py`, `scan_churn.py`, `scan_last_100_live.py`, `bof_exact.py`.
- **Redundant helpers**: `update_scrapers_boilerplate.py`, `regenerate_draft_graphs.py`, `regenerate_info_cards.py`, `reply_to_post.py` (proof of concept).
- **Stale Drawing Board**: 17 scripts in `bluesky_bot/drawing_board/`.

---

## Part 5: `AletheiaLauncher.pyw` Audit Findings

1. **Character-by-Character Stream Bottleneck (`Line 500`)**:
   `char = stream.read(1)` in a Python loop into a Queue locks the Tkinter event loop during heavy log output.
   *Fix*: Change to `line = stream.readline()` or `chunk = stream.read(1024)`.
2. **Relative `.venv` Path (`Lines 314–319`)**:
   Used `".venv/Scripts/python.exe"` instead of `os.path.join(script_dir, ".venv/Scripts/python.exe")`. External shortcuts fell back to system Python.
3. **Relative Icon Path (`Line 322`)**:
   `"bluesky_bot/alethekanon.png"` fails when CWD is already `bluesky_bot/`.
4. **Encoding Crashes on Windows Subprocess Pipes**:
   Lacked `errors="replace"`, crashing on cp1252 characters.

---

## Part 6: Proposed Prioritized Implementation Roadmap

1. **Phase 1: Security & Sourcing Hardening (P0)**
   - Remove `"com.au"`, `"reuters.com"`, `"bloomberg.com"`, `"nytimes.com"`, `"wsj.com"` from `unscrapable_domains.json`.
   - Add `tavily.com` to `NON_NEWS_DOMAINS` and enforce `is_news_url()` + non-tavily check in `search_counter_sources_tavily()`.
   - Update `is_news_url()` to reject bare root homepages and corporate/SaaS path patterns.
   - Fix fallback title in `scrape_via_tavily()` to derive from URL slug instead of returning `"Article"`.
   - Remove `or len(intersection) >= 2` in `cluster_candidate_stories()`.
2. **Phase 2: Trajectory & Math Corrections (P0)**
   - Replace Cartesian concatenation in `get_path_name()` with the canonical $4 \times 4$ geodesic lookup table.
   - Enforce deterministic trajectory checks in `post_batch.py` and `aletheia_bot.py`.
   - Fix the outer return in `rebuild_registries_son.py` to prevent vector force data loss.
   - Derivation of zone labels dynamically on registry rebuilds.
   - Add neutral deadband to prevent neutral procedural news from auto-failing into `Destruction`.
3. **Phase 3: Publishing, Retraction & Threading (P1)**
   - Fix `retract_story.py` to post errata as threaded replies to the original root post.
   - Add surviving orphan rkey quarantine logging on partial thread rollback failures.
   - Fix `image_card_generator.py` row mapping for multi-aspect stories and un-invert QR codes.
   - Fix `_REPLIED_TARGETS` cache key consistency (use `rkey` uniformly).
4. **Phase 4: Architecture Simplification & Archive (P2)**
   - Move 41 obsolete patch scripts to `bluesky_bot/_Archive/legacy_patches/`.
   - Remove stale `bluesky_bot/drawing_board/`.
   - Unify `rebuild_registries.py` and `rebuild_registries_son.py` into a single authoritative rebuilder.
   - Fix `AletheiaLauncher.pyw` streaming bottleneck, venv resolution, and icon paths.

*(Awaiting user review before any code modifications are applied.)*
