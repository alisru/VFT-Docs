# POSTMORTEM: Root Cause Analysis of Harvester Source Bias & Queue Audit Failures

## Executive Summary
This postmortem details the critical engineering failures, algorithmic biases, and structural oversights that caused the Aletheia autonomous news auditing pipeline to degrade into an echo chamber for right-wing tabloid media (Fox News, NY Post, Breitbart), starve reputable newsrooms (ABC Australia, The Guardian, Reuters, AP), and generate severely skewed, hallucinated, and partisan audit threads.

---

## The 7 Planes of Reality Decomposition

### Plane 1: WHO — The Metaphysical Plane (Will, Agency & Stewardship)
* **The Actors**:
  * **The System / Aletheia Bot**: Intended as a substrate-neutral epistemic judge mapping moral vector trajectories $(\upsilon, \psi)$.
  * **The News Outlets**: Polarized actors (Fox News, NY Post, Breitbart) providing sensationalized framing; neutral wires (Reuters, AP) and public broadcasters (ABC Australia, BBC, NPR) providing empirical records.
  * **The Public & Users**: Victims of epistemic distortion when an automated truth-auditor adopts partisan tabloid assumptions as foundational ground truth.
* **The Will Inversion**: Instead of applying objective social physics across all actors, the audit engine succumbed to the **0.5 Perceptual Inversion Zone**: it mistook inflammatory tabloid assertions for objective reality, validating partisan cynicism while labeling normal democratic processes as systemic evil.

---

### Plane 2: WHAT — The Possible Plane (Potential, Probabilities & Failure Modes)
* **What Went Wrong**:
  1. **Monopolization of Candidate Slots**: A small cluster of right-wing outlets seized over 80% of candidate intake slots.
  2. **Ideological Asymmetry in Audits**:
     * Democratic election victories and progressive policy amendments were scored at $+1.2$ to $+1.5$ (Productive Manifestation / PASS) with editorial cheerleading.
     * Republican election victories (e.g. Michael Alfonso winning WI-7) or voter rejection of tax propositions (California Prop 40) were audited as $-0.9$ (Systemic Destruction / FAIL) under the pretext of "dynasty" or "corporate resistance."
     * Routine political consensus statements (Pelosi) were branded as $-0.8, -0.9$ "Severe Deception."
  3. **Uncritical Adoption of Tabloid Smears**: In the Ilhan Omar audit, unproven allegations regarding marriage fraud published by the NY Post were accepted as verified facts, resulting in a personal moral condemnation $(-0.75, -0.85)$.
  4. **Factual Hallucinations**: Fabricated or satirical race calls (Amy Klobuchar winning the Minnesota Governor seat with Tim Walz resigning) were audited as verified historical facts.
  5. **Deterministic Trajectory Invariant Violations**: 5+ stories in the queue labeled $(+, +) \to (-, -)$ transitions as `The Path of Deception` instead of the mathematically required `Fall into Destruction (The Path of Fall)`.

---

### Plane 3: WHERE — The Physical Plane (Substrate, Files & Code Locations)
* **Exact Locations of the Failure**:
  * `bluesky_bot/AletheiaLauncher.pyw` (Lines 1240–1255 & Line 1713):
    * `sorted_feed_names = sorted(list(self.feed_definitions.keys()))`
    * Feed checkbuttons generated and dispatched in strict alphabetical order.
  * `bluesky_bot/unscrapable_domains.json`:
    * Contained 252 domains, including `theguardian.com`, `apnews.com`, `reuters.com`, `axios.com`, `aljazeera.com`, `bloomberg.com`, `nytimes.com`, and `washingtonpost.com`.
  * `bluesky_bot/harvest_candidates.py` (Lines 473–494 & Lines 336–370):
    * `SCRAPING_WHITELIST`: Protected `foxnews.com`, `nypost.com`, `breitbart.com`, `dailymail.co.uk`, `thefederalist.com`, `washingtonexaminer.com` with permanent ban immunity.
    * `distinct_sources[0]`: Multi-source cluster deduplication defaulted to index 0, guaranteeing early-scraped Fox News was chosen as the primary authoritative publisher.
  * `bluesky_bot/stories/factcheck_*.json`:
    * 22 queued draft story files in `bluesky_bot/stories/`.

---

### Plane 4: WHY — The Lyrical Plane (Resonance, Narrative & Editorial Drift)
* **The Narrative Fracture**:
  * Aletheia was conceived as an objective, calm, post-partisan analytical instrument.
  * When fed tabloid crime stories and culture-war headlines, the LLM prompt resonance shifted from structural analysis to moral indignation.
  * The prompt began mirroring the emotional temperature of the input articles: high-strain clickbait generated hyper-dramatic audit text ("grotesque spectacle", "family warfare", "dynasty upgrade"), abandoning epistemic detachment.

---

### Plane 5: HOW — The Logical Plane (Algorithmic Mechanisms & Data Flow)
* **The Causal Chain of Execution**:
  ```
  1. Launcher GUI initializes -> sorts feed names alphabetically.
  2. Early alphabetical feeds (Daily Caller, Daily Mail, Fox News Latest, Fox News Politics, New York Post) placed at top of list.
  3. Harvester loops through feeds sequentially -> fills quota (TARGET_RSS) before reaching lower-alphabet feeds (SBS, SMH, The Guardian, WA Today).
  4. When Guardian/AP/Reuters URLs were encountered in search/Bluesky, any Cloudflare 403 or HTML parsing hiccup dynamically appended them to unscrapable_domains.json.
  5. Subsequent runs rejected Guardian/AP/Reuters at line 518, while whitelisted Fox/NYPost bypassed the ban.
  6. Cluster deduplicator merged co-occurring stories and picked distinct_sources[0] (Fox News).
  7. Gemini was prompted with Fox/NYPost copy -> accepted claims as baseline -> issued extreme polarized coordinates.
  8. Trajectory enforcement failed to catch string mismatches, printing "The Path of Deception" for (-,-) endpoints.
  ```

---

### Plane 6: CAUSE — The Historical Plane (Sequence, Genesis & Decisions)
* **Historical Origins**:
  1. **The Dynamic Banlist Patch**: Added to prevent bot crashes on paywalled articles (WSJ, FT). It had no verification threshold; a single failed request permanently blacklisted the entire domain.
  2. **The Right-Wing Whitelist Addition**: Created during a test phase to ensure conservative outlets could be audited for bias ("audit right wing queue"). The whitelist prevented them from ever being auto-banned. This created an accidental asymmetric filter: mainstream news got banned, tabloids were protected.
  3. **Alphabetical Sorting Convenience**: Implemented in the Tkinter GUI simply to make feeds look organized in 3 columns, inadvertently turning feed intake into an alphabetical priority queue.
  4. **The Index-0 Deduplication Shortcut**: Implemented as a quick way to pick a cluster representative without implementing publisher neutrality ranking.

---

### Plane 7: EFFECT — The Emotive Plane (Impact, Consequence & Remediation)
* **Systemic Consequences**:
  * **Brand Erosion**: The bot appeared to Bluesky users as an ideological partisan weapon or Fox News parrot.
  * **Wasted Inference Tokens**: Generating 22 skewed audit drafts that could not be published without severe reputational damage.
  * **Loss of Trust**: Sidelining Australia's national broadcaster (ABC) and premier international investigative outlets (The Guardian, Reuters).
* **Remediation Invariants**:
  1. Cleanse `unscrapable_domains.json` of all legitimate newsrooms.
  2. Grant `SCRAPING_WHITELIST` immunity to all legitimate wire services and public broadcasters.
  3. Implement round-robin / randomized feed processing to eliminate alphabetical priority.
  4. Implement neutrality-weighted primary source selection for clusters.
  5. Surgically re-audit and correct all 22 queued stories rather than deleting them.
