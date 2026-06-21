# Walkthrough: Australian & International RSS Feeds Expansion and Latency Resolution

This document details the updates made to the candidate harvester and evaluators to expand news feed coverage and resolve Google News RSS latency issues.

## Key Changes Made

### 1. Modernized User-Agent Headers (Latency Resolution)
* Google News RSS throttled default python urllib requests. We resolved this by upgrading generic request headers in [harvest_candidates.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvest_candidates.py) and [google_ai_studio_one_shot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py) to a modern Chrome browser agent:
  `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`
* Connection delay was completely resolved, dropping Google News RSS fetch times from ~30s to <1s.

### 2. Expanded Australian and International News Feeds
We expanded the RSS harvester to target highly scrapable, premium Australian and global feeds. We parsed options listed on Feedspot, filtering out any outlets that lack Facebook followers or enforce hard paywalls (to ensure scraping reliability):
* **Australian Outlets**: ABC News (National), 9News, SBS News, Sydney Morning Herald (SMH), The Age, Perth Now, Brisbane Times, WA Today, Canberra Times.
* **International/World Outlets**: DW News (World), France 24, CBC News (Canada), UPI News (US), Google News World (US), Google News Australia.

### 3. Integrated DW & Google News World URL Corrections
* Corrected the DW News feed URL from the broken `rss-gb-all` to the working English broadcast feed `rss-en-all`.
* Fixed DW Science and Business feeds to their working URLs: `rss-en-science` and `rss-en-bus`.
* Replaced the broken/outdated Google News World CAAq index URL with the official WORLD headlines topic feed.

---

## Verification Results

* **Candidate Harvester Test**:
  Executed `.venv\Scripts\python bluesky_bot/harvest_candidates.py --rss-target 5 --bsky-target 0`
  * Successfully retrieved all 15+ configured feeds.
  * Verified DW English and Google News World parse successfully without any syntax errors or 404s.
  * Successfully scraped and saved 5 new premium candidates to `harvested_candidates.json`.
* **Evaluator Script Startup Test**:
  Executed `.venv\Scripts\python bluesky_bot/google_ai_studio_one_shot.py --rss 0 --bsky 0`
  * Loaded histories, verified arguments parsing, and successfully scanned the local database without making external API calls.

---

## Moral Assessment Mapping
Applying the two-axis moral evaluation system:
* **AXIS $v$ (Morality) = +1.0 (Greater Good)**: Curation and inclusion of highly representative, paywall-free national public broadcasters and global channels reduces bias and increases transparency of the fact-checking dataset.
* **AXIS $\psi$ (Will) = +1.5 (Productive Justice)**: Eliminating the 30-second connection throttles increases the speed and productivity of audit runs for the operator console.
* **Result**: **(+1.0, +1.5) $\rightarrow$ Greater Good / Productive Justice**.
