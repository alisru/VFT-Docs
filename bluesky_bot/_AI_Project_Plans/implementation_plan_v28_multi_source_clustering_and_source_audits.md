# Implementation Plan: Multi-Source Topic Clustering & Per-Source Quality Sub-Audits (v28)

## 1. Overview & Problem Statement
When multiple news outlets report on the same breaking event (e.g. Breitbart, Reuters, Washington Post), evaluating them as separate candidates creates redundant posts. Furthermore, picking only one source discards the rich framing divergences across media factions.

This updated plan utilizes the codebase's **existing scraping infrastructure** (`scrape_article_content` in `harvest_candidates.py`) to:
1. **Multi-Source Topic Clustering**: Automatically group candidate stories covering the same real-world event into a single cluster, selecting 2–3 distinct editorial perspectives (e.g. Right, Mainstream Wire, Left/Institutional) while de-duplicating wire syndicates.
2. **Direct Article Scraping via Existing Scraper**: Use `scrape_article_content(url)` in [`harvest_candidates.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvest_candidates.py#L82) to extract clean body text from the 2–3 distinct URLs, generating a Cross-Source Comparison Dossier with zero search API tokens.
3. **Per-Source Quality Scorecard Post (Post 5)**:
   - When a story has $\ge 2$ sources, a dedicated **Source Quality Scorecard** post is generated, individually auditing the editorial integrity, omissions, and framing bias of each reporting outlet separate from the underlying real-world event.
   - When a story is single-source, it skips the source scorecard and executes the standard event-level audit.

---

## 2. User Review Required

> [!NOTE]
> **Post Index & Thread Length Alignment**:
> For **Multi-Source Stories ($\ge 2$ sources)**:
> - Post 4 = Overall Event Verdict (Judges the real-world actors & policy outcome).
> - Post 5 = **Source Quality Breakdown** (Audits the 2–3 reporting outlets individually).
> - Post 6 = Context & Background.
> - Posts 7–13 = Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Alethekanon, Empathy/Casual Takes.
>
> For **Single-Source Stories (1 source)**:
> - Standard 13-post thread (Post 5 is Context; no redundant source breakdown).

---

## 3. Proposed Changes

### Component 1: Topic Clustering & Existing Scraper Integration
#### [MODIFY] [`e:\Vector Field Theory\VFT Docs\bluesky_bot\harvest_candidates.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvest_candidates.py)
- Add `cluster_candidate_stories(candidates, similarity_threshold=0.55)`:
  - Extracts key entities and normalized title tokens.
  - Groups stories sharing $\ge 55\%$ lexical/entity overlap into topic clusters.
  - De-duplicates exact syndicates (e.g. AP republishers).
  - Selects up to 3 distinct publisher perspectives per cluster.
  - Uses existing `scrape_article_content(url)` to fetch full text for the distinct URLs in the cluster.
  - Compiles the `cluster_sources` list and `cross_source_dossier` into the candidate object with `is_multi_source = True`.

---

### Component 2: Prompt Formatting & Per-Source Scorecard Directive
#### [MODIFY] [`e:\Vector Field Theory\VFT Docs\bluesky_bot\google_ai_studio_one_shot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
- In `build_formatting_rules(...)`:
  - When `is_multi_source = True` (or cluster sources $\ge 2$), inject the **Multi-Source Editorial Audit Directive**:
    - Guides Post 5 to format as:
      ```
      Source Quality Breakdown:
      - [Outlet A]: [PASS/FAIL/COND] ([u], [psi]) — [Specific framing/omission reason under 60 chars].
      - [Outlet B]: [PASS/FAIL/COND] ([u], [psi]) — [Specific framing/omission reason under 60 chars].
      ```
    - Maps the per-source evaluations into the JSON `aspects` array (item[27]).
- Update `run_one_shot_evaluations` to inject `cross_source_dossier` into `extra_context` for multi-source candidates.

---

### Component 3: Post Assembly & Link Card Handling
#### [MODIFY] [`e:\Vector Field Theory\VFT Docs\bluesky_bot\aletheia_bot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aletheia_bot.py)
- When publishing threads for multi-source stories:
  - Attach the primary story URL card to Post 2 (Stated Claim).
  - Attach secondary/counter-source link cards to Post 5 (Source Quality Breakdown).

---

## 4. Verification Plan

### Automated Tests
1. **Clustering & Existing Scraper Test**:
   - Run `harvest_candidates.py` against live feeds to verify that duplicate stories form a single multi-source cluster with distinct publishers and scraped text.
2. **End-to-End One-Shot Evaluation**:
   - Run a test evaluation of a multi-source candidate chunk through `google_ai_studio_one_shot.py` with `gemini-3.7-flash` / `3.5-flash` to verify that:
     - Post 4 gives the real-world event verdict.
     - Post 5 generates the concise, accurate Source Quality Breakdown.
     - The `aspects` array correctly captures the per-outlet coordinates.
