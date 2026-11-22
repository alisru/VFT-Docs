# Implementation Plan v36: Re-Audit Last 100 Live Stories

## Objective
Systematically re-audit and correct the 100 most recently posted stories in `bluesky_bot/stories/live/` to eliminate deterministic trajectory invariant violations, correct extreme partisan/cynical coordinate distortions ($\le -0.7$), and de-escalate sensationalized tabloid smear framing.

## User Rules & Guardrails
- **Identify and Present First**: Present the complete scan and findings directly in chat for user review before running bulk modifications.
- **NO AI Studio API Calls**: All re-auditing and coordinate recalibration must be performed using local deterministic social physics rules (`generate_graph.py`, `enforce_deterministic_trajectory()`, and bounded tensor mapping), with zero calls to AI Studio.
- **Maintain Historic Plans**: Never overwrite historical plans; archive this plan in `bluesky_bot/_AI_Project_Plans/`.
- **Zero Data Loss**: No files are deleted. Corrected stories remain in `stories/live/` with updated coordinates, posts, and invariants.

## Findings Summary (Last 100 Live Stories)
- **Total Stories Analyzed**: 100
- **Outlet Composition**:
  - `dailymail.com`: 18
  - `foxnews.com`: 15
  - `breitbart.com`: 9
  - `goodnewsnetwork.org`: 9
  - `dailycaller.com`: 7
  - `abc.net.au`: 6
  - `washingtonexaminer.com`: 6
  - `nypost.com`: 6
  - `thefederalist.com`: 4
  - `optimistdaily.com`: 4
  - Others (NPR, LATimes, Kyiv Independent, etc.): 16
  - **Right-Wing Tabloid Total**: 65 / 100 (65%)
- **Deterministic Trajectory Invariant Violations**: 40 / 100 (40%)
  - Cases where $(+,+) \to (-,-)$ were incorrectly labeled "The Path of Deception" or "The Path of Redemption".
- **Extreme Negative Outliers ($\le -0.7$)**: 53 / 100 (53%)
  - Severe coordinate inflation where standard campaign speeches, basketball chatter, or bipartisan outreach were labeled as $(-0.8, -0.9)$ "Systemic Destruction".

## Remediation Strategy

### 1. Invariant Enforcement
Run all 100 stories through `enforce_deterministic_trajectory(story)`:
- $(+,+) \to (-,-)$ strictly mapped to `Fall into Destruction (The Path of Fall)`.
- $(+,+) \to (-,+)$ strictly mapped to `Fall into Deception (The Path of Deception)`.
- $(-,+) \to (+,+)$ strictly mapped to `Revelation into Grace (The Path of Awakening)`.
- $(+,+) \to (+,+)$ mapped to `Awakening into Grace` (PASS).

### 2. Coordinate & Editorial De-Biasing
- **Bipartisan Outreach / Routine Politics**: Recalibrate stories penalizing standard legislative checks, bipartisan bills, or routine party rhetoric from $(-0.8, -0.9)$ to $(+0.2, +0.2)$ or $(0.0, +0.1)$ (PASS / CONDITIONAL).
- **Tabloid Clickbait / Celebrity Sports Commentary**: Recalibrate celebrity sports or lifestyle fluff (Spike Lee White House visit) from $(-0.8)$ destruction to neutral $(0.0, 0.0)$ baseline.
- **Crime / Local Tragedy Reporting**: Recalibrate legitimate crime reports to evaluate police transparency and factual accuracy rather than treating criminal acts as an editorial hypocrisy of the news outlet.

### 3. Registry & Web Sync
Recompile `stories/live/index.json` and `stories_registry.js` using `rebuild_registries_son.py` to ensure all shards and web viewers reflect the cleansed data.
