# Walkthrough: Multi-Source Topic Clustering & Per-Source Quality Audits

We have completed the implementation of **Multi-Source Topic Clustering, Direct Article Scraping, and Per-Source Quality Sub-Audits** across the Aletheia Bot pipeline.

---

## Key Changes Made

### 1. Feed-Level Topic Clustering & De-Syndication
- **File**: [`harvest_candidates.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvest_candidates.py#L98)
- Added `cluster_candidate_stories(...)`:
  - Groups candidates reporting on the same real-world event into a unified cluster based on entity and lexical overlap.
  - Filters out exact wire syndicates from the same publisher while selecting up to 3 distinct publisher perspectives (e.g. Breitbart, Washington Post, Reuters).
  - Automatically compiles a `Cross-Source Comparison Dossier` comparing all outlets' coverage.
  - Sets `is_multi_source = True` and populates `cluster_sources = [...]`.

### 2. Multi-Source Prompt Formatting & Scorecard Directive
- **File**: [`google_ai_studio_one_shot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py#L1026)
- Updated `build_formatting_rules(...)` and execution loop:
  - When `is_multi_source` is detected, automatically triggers `use_multi_aspect = True`.
  - Directs Post 4 to judge the **real-world event/actors** themselves.
  - Directs Post 5 to format as the **Source Quality Scorecard** with concise per-outlet bullet points:
    ```
    - [Outlet A]: [PASS/FAIL/COND] ([u], [psi]) — [Specific framing/omission reason under 60 chars].
    - [Outlet B]: [PASS/FAIL/COND] ([u], [psi]) — [Specific framing/omission reason under 60 chars].
    ```
  - Maps per-outlet evaluations cleanly into the JSON `aspects` array (item[27]).

### 3. Post Thread Assembly & Comparative Link Cards
- **File**: [`aletheia_bot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aletheia_bot.py#L573)
- When publishing threads for multi-source stories:
  - Part 2 (Stated Claim) receives the primary story preview card.
  - Part 3 (Ground Reality) receives the official fact-checking verification card.
  - Part 5 (Source Quality Scorecard) receives the secondary comparative source preview card.

---

## Verification Results

### Unit Test: `cluster_candidate_stories`
Tested with multi-feed scenario (2 breaking articles on same event from Breitbart and Washington Post + 1 standalone Bloomberg article):
```
[Cluster Created] 'ICE Arrests 1,300 in Massive DC Suburb Operation' (2 distinct sources: Breitbart, Washington Post)
Clustered 3 raw candidates into 2 distinct topics (1 multi-source cluster(s)).
Total raw input: 3 -> Total clustered: 2

--- ICE CLUSTER VERIFICATION ---
is_multi_source: True
Cluster sources count: 2
Publishers: ['Breitbart', 'Washington Post']

--- ABBOTT STORY VERIFICATION ---
is_multi_source: False

ALL CLUSTERING TESTS PASSED SUCCESSFULLY!
```
## Tavily API Integration Update (v28.1)
- Added `TAVILY_API_KEY` to `bluesky_bot/.env`.
- Integrated `scrape_via_tavily` as an automatic smart fallback inside `scrape_article_content()` in `harvest_candidates.py`.
- Verified live: When a site blocks standard python requests (e.g. Reuters, paywalled / Cloudflare-protected domains), `scrape_article_content` automatically falls back to Tavily to extract full article text.
## Syntax Bug Fix (v28.2)
- Fixed `TypeError: can only concatenate tuple (not "str") to tuple` in `build_output_format()`.
- Root cause: Trailing commas inside the multi-line parenthesized assignment of `output_format` implicitly created a tuple in Python.
- Removed trailing commas so `output_format` evaluates to a single continuous string across all combinations of SON, Multi-Aspect, and Spiritual modes.
- Verified cleanly across all permutations with 0 errors.
## Fast Grounding & Output Budget Fix (v28.3)
- Prioritized `gemini-2.5-flash-lite` before `gemini-2.5-flash` in `harvest_search_grounding`. `2.5-flash-lite` executes search grounding in 4-8s without suffering the 60-120s hangs and 503 capacity spikes of `2.5-flash`.
- Expanded `max_output_tokens` from 32,768 to 65,536 on Gemini 3.x calls to prevent output truncation when returning dense multi-candidate JSON schemas with deep thinking tokens.
## Auto-Fit & Spiritual Schema Auto-Repair (v28.4)
- **Spiritual Prefix & Quote Auto-Repair**: If the AI model generates a valid scripture quote and canonical citation but omits the `Spirithekanon:\n` prefix or double-quotes, `sanitize_story_posts` and `validate_batch.py` automatically format and wrap the passage into standard schema.
- **300-Character Auto-Fitting**:
  - Raw posts destined for Bluesky (Hook, Claim, Reality, Verdict, Spirithekanon) are auto-fitted under 300 characters across `aletheia_bot.py` and `post_batch.py`, trimming trailing hashtags or excess whitespace rather than throwing fatal validation errors.
- **Result**: Rescued all failed drafts in `stories/fail/`. All **37 out of 37 stories** passed pre-flight validation with 100% success rate.
## Full Drafts Bias & Multi-Source Audit (v28.5)
- **Selective Audit Executed**: Audited all 64 draft stories in `stories/` for partisan bias, framing spin, and selective cherrypicking.
- **Objective/Neutral Stories Preserved (10)**: Non-political events (meteor sightings, forensic genealogy, measles health reports, direct crime arrests) were preserved as clean single-source audits.
- **Biased/Partisan Stories Enriched (54)**: 54 political/controversial stories sourced from single partisan outlets were enriched with secondary/contrasting news outlets (e.g. *The New York Times*, *Reuters*, *The Hill*, *WSJ*, *AFR*, *BBC*, *NPR*, *Axios*).
- **Post 5 Upgraded**: All 54 enriched stories received a calibrated **Source Quality Scorecard** in Post 5.
- **Validation**: 64/64 drafts passed pre-flight validation with 100% success rate.
## Full Multi-Source Re-Audit & Pipeline Execution (v28.6)
- **End-to-End AI Re-Audit Executed**: Re-audited all 38 partisan/sensationalist stories from scratch using AI Studio batch processing with full multi-source dossiers attached in context.
- **Synthesized Ground Reality**: Evaluated stated claims vs. multi-perspective ground reality $(u, \psi)$, neutral institutional facts, and scriptural/canonical perspectives.
- **Card & Graph Generation**: Promoted and auto-generated trajectory graphs, Verdict split cards, and Analysis/Perspectives split cards for all 38 stories.
- **Pre-Flight Validation**: All **67 draft stories** in `stories/` passed 100% of pre-flight validation checks.
