# Implementation Plan v40: Multi-Source Event Clustering & Objective Aspect Auditing

## Goal Description
Enable the Bluesky bot to capture **2 to 3 distinct publisher perspectives** (e.g. Left, Right, Wire/Center) for breaking news events directly from existing RSS/Bluesky feeds, combine them into an objective multi-source evidence dossier, and audit the **real-world event aspects** (Instigator, Acted-Upon/Victim, Regulator, Beneficiary) per the Vector Field Theory coordinates $(\upsilon, \psi)$ without partisan capture.

---

## User Review Required

> [!IMPORTANT]
> **Pre-Quota Event Clustering**:
> Previously, the harvester truncated the incoming list to `TARGET_RSS + TARGET_BSKY` (e.g. 20 items) *before* clustering, meaning alternative coverage for an event that appeared further down the feed was dropped before it could be matched.
> We move event clustering to run over the **entire raw pool of harvested feed items** before quota trimming. If multiple outlets report on the same event, they are grouped into a single multi-source candidate containing 2 to 3 distinct perspectives.

---

## Open Questions
- None. The scope and requirements are aligned with the project specification.

---

## Proposed Changes

### Component 1: Candidate Harvester (`bluesky_bot/harvest_candidates.py`)

#### [MODIFY] [`bluesky_bot/harvest_candidates.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvest_candidates.py)
1. **Pre-Quota Clustering on Full Pool**:
   - In `main()` / harvest loop: do not truncate `combined_candidates` to `TARGET_RSS + TARGET_BSKY` before clustering.
   - Run `cluster_candidate_stories(combined_candidates)` across the full set of fetched feed entries.
2. **Distinct Publisher Selection (Up to 3 Outlets)**:
   - For each cluster of articles covering the same event:
     - Select up to **3 distinct publisher perspectives** across different bias families (Left, Right, Center/Wire).
     - De-duplicate identical syndicated wire stories (e.g. local outlets republishing the same AP text).
   - Scrape full article bodies for each selected outlet using `scrape_article_content(url)`.
   - Assemble `c["cross_source_dossier"]` containing the full bodies labeled by outlet and bias.
   - Set `c["is_multi_source"] = True` and populate `c["cluster_sources"] = [{"publisher": ..., "url": ..., "bias": ...}]`.
3. **Targeted Fallback for Truly Isolated Partisan Stories**:
   - If an event is covered by only 1 source in our harvest AND that source is a partisan outlet (Left or Right), invoke `search_counter_sources_tavily()` to fetch 1 wire or opposing counter-article.
   - If the single source is already a neutral wire (Reuters, AP, BBC) or local report, skip Tavily entirely.
4. **Post-Cluster Quota Trimming**:
   - Trim the final clustered and enriched candidates to the target batch size.

---

### Component 2: Evaluation Prompt & Payload Assembly (`bluesky_bot/google_ai_studio_one_shot.py`)

#### [MODIFY] [`bluesky_bot/google_ai_studio_one_shot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
1. **Preserve `cross_source_dossier` in Payload**:
   - In `run_one_shot_evaluations()` (line 1836): Ensure `cross_source_dossier` and `cluster_sources` are passed in `clean_candidates` and injected into the candidate context prompt so Gemini receives all 2–3 perspectives.
2. **Objective Event Aspect Auditing Directive**:
   - Update `build_system_instruction`:
     - Clarify that the multi-source dossier provides the **empirical evidence base**.
     - Direct the model to evaluate the **actual event aspects** (the real-world instigators, victims, and regulators) per $(\upsilon, \psi)$ physics, rather than adopting the ideological spin of any single reporting outlet.
     - Post 5 (Sub-Audits Breakdown) lists the evaluated event aspects with their individual coordinates and verdicts.
3. **Structured Tri-URL Assignment**:
   - Assign the 3 outlet URLs explicitly in the story schema:
     - `link` = Source 1 (Initial reporting outlet)
     - `grounding_url` = Source 2 (Wire / empirical verification)
     - `secondary_url` = Source 3 (Alternative / counter-perspective outlet)

---

### Component 3: Per-Post Link Embed Dispatch (`bluesky_bot/aletheia_bot.py`)

#### [MODIFY] [`bluesky_bot/aletheia_bot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aletheia_bot.py)
- Map the 3 URLs into their dedicated post slots during publishing:
  - **Post 2 (Stated Claim)**: Injects `link_embed` for Source 1.
  - **Post 3 (Ground Reality)**: Injects `grounding_embed` for Source 2 (Wire / official record).
  - **Post 5 (Sub-Audits Breakdown)**: Injects `secondary_embed` for Source 3 (Counter-perspective).

---

## Verification Plan

### Automated Tests
1. **Clustering Test**:
   Run `python -c "from harvest_candidates import cluster_candidate_stories; ..."` on a mock list of 5 articles (2 on event A, 3 on event B) to verify that articles from different domains covering the same event are grouped together into 2-3 source dossiers.
2. **Batch Compile Check**:
   Run `python -m py_compile bluesky_bot/harvest_candidates.py bluesky_bot/google_ai_studio_one_shot.py` to ensure clean syntax.

### Manual Verification
- Run a small test harvest (`python bluesky_bot/harvest_candidates.py --rss 10 --bsky 10`) and inspect `harvested_candidates.json` to verify:
  - Candidates covering the same event contain `is_multi_source = True` with 2–3 distinct publishers.
  - Zero redundant Tavily calls made for clustered events.
