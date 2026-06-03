# Walkthrough: Enhanced Trajectory Graphs and Change-Tracking Push Flag Script

This document summarizes the changes made to update the trajectory graph scale axes, coordinate titles, evaluator guidelines, and provide change-tracking validation.

## Changes Made

### 1. Trajectory Graph Coordinate Axis Labels & Coordinate Displays
* Modified [generate_graph.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/generate_graph.py):
  - Set explicit `xticks` at `[2.0, 1.0, 0.5, 0.0, -0.5, -1.0, -2.0]` mapped to multi-line labels: *Everyone (+2.0), Others (+1.0), Other (+0.5), No One (0.0), My Group (-0.5), Me (-1.0), Only Me (-2.0)*.
  - Set explicit `yticks` at `[2.0, 1.0, 0.0, -1.0, -2.0]` mapped to labels: *Active-Active (+2.0), Passive-Active (+1.0), Neutral (0.0), Passive-Passive (-1.0), Active-Passive (-2.0)*.
  - Appended a third line to the graph title rendering the exact numerical coordinates for Stated Claim and Actual Reality: `Stated: (x, y) | Actual: (x, y)`.
  - Added `plt.close(fig)` to release pyplot memory after rendering each graph to prevent figure memory leaks.
  - Removed old Good/Bad Preference text label clutter from the grid.

### 2. Gnostic Actualism Evaluator Guidelines
* Modified [Convergence-test-v2.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/Convergence-test-v2.md):
  - Updated Section "Phase 2 — Vector Verification" to map the exact coordinate scale ticks and definitions to assist evaluators during convergence checks.

### 3. Change-Tracking and Registry Rebuild Utilities
* Created [track_changes.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/track_changes.py):
  - Validates JSON config files recursively under `stories/` and `stories/live/`.
  - Audits keys, post limits (exactly 14 posts for dry runs), character limits (<250 characters per post for dry runs), and corresponding local and remote graph PNG existences.
  - Excludes legacy files and filters only for files with `factcheck_` prefix to avoid false-positives.
  - Integrates with Git status to show a summary of target modified and untracked changes, and prompts the user to rebuild registries and stage changes ready to push.
* Created [regenerate_graphs.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/regenerate_graphs.py):
  - Programmatically iterates through all active factcheck configs and rebuilds all graph PNGs to apply coordinate scale changes.

## Verification Results
* Successfully ran [regenerate_graphs.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/regenerate_graphs.py) to rebuild 81 active trajectory graphs with the new scales and titles.
* Rebuilt the javascript database registers using [rebuild_registries.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/rebuild_registries.py).
* Ran [track_changes.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/scratch/track_changes.py) to verify that all target active files are validated cleanly and ready for git staging.

## Batch 4 Evaluation Notes (Post-Compaction)
* **Stories Evaluated (Indices 12 to 15)**:
  1. **EU Ukraine Fast-Track Membership** (`eu_ukraine_membership`): Stated (+1.0, +1.0) -> Actual (-1.0, +1.0). Path: *The Path of The Fall*.
  2. **Latter-day Saints USAID Advocacy** (`latter_day_saints_usaid`): Stated (+1.0, +1.0) -> Actual (+1.0, -1.0). Path: *The Path of Empty Mass (The Fall)*.
  3. **Mexico City World Cup Sculptures Damaged** (`mexico_city_world_cup_sculptures`): Stated (+1.0, +1.0) -> Actual (-1.0, -2.0). Path: *The Path of Deception*.
  4. **Graze Social News Feed Funding** (`graze_social_funding`): Stated (+1.0, -1.0) -> Actual (+1.0, +1.0). Path: *The Path of Grace*.
* **Validation**: Shortened hook in Latter-day Saints to ensure it meets the strict 250 character limit per post. Verified that all Batch 4 files validate successfully under `track_changes.py`.
