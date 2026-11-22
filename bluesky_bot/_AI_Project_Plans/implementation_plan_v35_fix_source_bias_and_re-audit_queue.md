# Implementation Plan v35: Fix Source Bias, Harvester Pipeline & Re-Audit Queued Stories

## Goal
Eliminate right-wing tabloid/Fox News monopoly in the news harvesting pipeline, restore balanced multi-source harvesting (Guardian, ABC, Reuters, AP), eliminate alphabetical bias, and surgically re-audit all 22 queued stories to restore empirical neutrality and deterministic trajectory invariants.

## User Constraints
- Do NOT purge the queued stories — REDO them.
- Document everything across the 7 Planes of Reality (Who, What, Where, Why, How, Cause, Effect).
- Never overwrite historical implementation plans; maintain this plan in `bluesky_bot/_AI_Project_Plans/`.
- No scratch folders; work inside `bluesky_bot/`.

## Proposed Changes

### 1. Root Cause Documentation (7 Planes of Reality)
Create `bluesky_bot/SOURCE_BIAS_AND_HARVESTER_POSTMORTEM.md` documenting:
- Q1 Metaphysical (WHO): The actors, victims of distortion, and epistemic stewardship.
- Q2 Possible (WHAT): The failure modes, hallucinations, and false assumptions.
- Q3 Physical (WHERE): The code lines, files (`AletheiaLauncher.pyw`, `harvest_candidates.py`, `unscrapable_domains.json`).
- Q4 Lyrical (WHY): The narrative distortion, partisan polarization, and editorial drift.
- Q5 Logical (HOW): The exact causal code mechanisms (alphabetical sorting, dynamic banning, index-0 selection).
- Q6 Historical (CAUSE): The timeline and sequence of commits that created the vulnerability.
- Q7 Emotive (EFFECT): The loss of credibility, anger, and systemic collapse of audit integrity.

### 2. Scraping Whitelist & Dynamic Banlist Sanitization
- File: `bluesky_bot/unscrapable_domains.json`
  - Remove all legitimate journalism and wire outlets: `theguardian.com`, `apnews.com`, `reuters.com`, `axios.com`, `bbc.com`, `abc.net.au`, `nytimes.com`, `washingtonpost.com`, `wsj.com`, `bloomberg.com`, `aljazeera.com`, `france24.com`, etc.
- Files: `bluesky_bot/harvest_candidates.py` & `bluesky_bot/google_ai_studio_one_shot.py`
  - Update `SCRAPING_WHITELIST` to permanently protect `theguardian.com`, `apnews.com`, `reuters.com`, `axios.com`, `abc.net.au`, `bbc.com`, `smh.com.au`, `aljazeera.com`.
  - Fix scraping failure logic: instead of appending failing domains to `unscrapable_domains.json`, route the URL to `scrape_via_tavily()` or fallback parsers.

### 3. De-biasing Feed Scheduling & Multi-Source Selection
- Files: `bluesky_bot/harvest_candidates.py` & `bluesky_bot/google_ai_studio_one_shot.py`
  - Round-robin or shuffle feed iteration order so early alphabetical feeds (`Daily Caller`, `Fox News`) cannot monopolize the candidate quota.
  - Multi-source clustering: in `cluster_by_semantic_similarity`, select the most neutral publisher (`center`/`wire` > `left`/`right`) as `primary_c` instead of naively defaulting to `distinct_sources[0]`.

### 4. Re-Auditing and Correcting All 22 Queued Stories
- Iterate through each story in `bluesky_bot/stories/factcheck_*.json`:
  1. Recalculate and enforce deterministic trajectories (`enforce_deterministic_trajectory()`).
  2. Correct trajectory names:
     - $(+, +) \to (-, -)$: strictly `Fall into Destruction (The Path of Fall)`
     - $(+, +) \to (-, +)$: strictly `Fall into Deception (The Path of Deception)`
  3. Correct coordinates and editorial rationale:
     - Remove partisan double standards (no $+1.5$ cheerleading for ordinary elections; no $-0.9$ destruction for democratic winners or rejected tax measures).
     - Rectify tabloid smear acceptance in Ilhan Omar audit.
     - Address hallucinated/incoherent race reporting (Klobuchar governor race).
     - Properly categorize police/domestic violence reporting (evaluating reporting transparency rather than treating domestic murder as an editorial failure).
  4. Synchronize `stories/index.json` and `stories_registry.js`.

## Verification Plan
- Run automated validation script across all 22 re-audited stories to confirm:
  - 0 deterministic trajectory name violations.
  - Objective balanced coordinates within reasonable bands.
  - Valid schema and complete 15-key/post structure.
- Verify `unscrapable_domains.json` no longer bans Guardian, Reuters, AP, Axios, BBC, ABC.
- Verify feed scheduler processes feeds in interleaved/balanced order.
