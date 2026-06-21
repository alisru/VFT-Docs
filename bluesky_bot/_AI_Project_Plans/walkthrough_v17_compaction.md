# Walkthrough: Interactive Leaderboard Controls, Timescale Fix, and Expanded Calibration Chart

This document details the updates made to the [control_panel.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/control_panel.html) to enhance the usability, reliability, and precision of the Audit & Trends dashboard.

## Key Changes Made

### 1. Interactive Sorting & Filtering for Hypocrisy Leaderboards
We replaced the static list rendering with reactive, stateful controls above the **Actor / Entity** and **Source Outlet** tables:
* **Excel-Style Clickable Column Headers**: Headers can now be clicked directly to sort:
  * **Actor / Entity** or **Source Outlet**: Sorts alphabetically.
  * **n**: Sorts by story count.
  * **avg Δu**: Sorts by average deception gap.
  * **σ (consistency)**: Sorts by consistency (standard deviation of deception gap).
* **Ascending/Descending Toggle**: Clicking the active sort column header toggles between ascending (`▲`) and descending (`▼`) directions.
* **Green Color-Coding for Good/Honest Metrics**: Updated average deception gap coloring so that any honest or neutral average values ($\Delta u \le 0$, like `+0.00` or negative values) are colored green (`var(--pass-green)`), while deceptive values ($\Delta u > 0$) remain red.
* **Minimum Story Count Filter**: Allows filtering out noise by only displaying entities with a minimum of $1+$, $2+$, $5+$, $10+$, or $25+$ stories.

### 2. Comprehensive Metric Legends & Reference Panel
* Added a detailed, responsive legend grid at the very top of the Audit tab explaining all main metrics for easy reference:
  * **Morality & Utility ($u$)**: Explains systemic alignment (+u for Greater Good, -u for Lesser Evil).
  * **Deception Gap ($\Delta u$)**: Explains the deception equation ($\Delta u = \text{claim}_u - \text{real}_u$) and the meaning of positive/negative values.
  * **Will & Agency ($\psi$)**: Explains intent (+ψ for active creation, -ψ for suppression/chaos).
  * **Consistency ($\sigma$)**: Explains standard deviation of the deception gap.

### 3. Timescale Date-Stretching & Scope Window Fix
* Converted the "Daily, Weekly, Monthly" controls to **Date Scope Filters** (Last 24 Hours, Last 7 Days, Last 30 Days, All Time) anchored relative to the latest data entry. 
* Selecting a scope automatically adjusts the bin width and scales the SVG axis labels and plot lines proportionally over the selected period.

### 4. High-Density Calibration Drift Sampling
* Introduced a sample size selector supporting **120 (Fast)**, **300 (Detailed)**, **500 (Dense)**, and **All** stories with dynamic opacity scaling to keep the vector graph readable.

### 5. Direct Source and Bluesky Links in Related Stories
* Added clickable `🔗` (original article) and `🦋` (Bluesky thread) icons inside the expanded related story details rows.

---

## Moral Assessment Mapping
Applying the two-axis moral evaluation system to these changes:
* **AXIS $v$ (Morality) = +1.8 (Systemic Justice)**: By improving the clarity and auditability of bias-tracking tools, these changes enable communities to hold media entities accountable without distortion or hidden sampling gaps.
* **AXIS $\psi$ (Will) = +1.6 (Productive Justice)**: Actively creates systemic value by building high-fidelity visual representations of information flow and resolving date distortion bugs.
* **Result**: **(+1.8, +1.6) $\rightarrow$ Greatest Good / Productive Justice**.
