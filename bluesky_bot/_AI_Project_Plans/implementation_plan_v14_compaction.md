# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 14 (Active): Enhanced Interactive Controls for Trend Over Time Graph

### Goal Description
Improve the control panel's "Trend Over Time" graph by adding standard interactive controls. These include interval settings (Daily, Weekly, Monthly), metric toggle options to show/hide lines (`reality_u`, `Δu`), and an interactive SVG hover vertical guide line and tooltip tracker.

### User Review Required
> [!NOTE]
> This updates the client-side JavaScript rendering of the trends graph. No database files or server scripts are altered.

### Proposed Changes

#### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/control_panel.html)
* Define global state variables `_trendInterval = 'week'`, `_showRealityU = true`, `_showDeltaU = true`.
* Add `setTrendInterval(interval)` and `toggleTrendLine(line, visible)` functions to handle interactions.
* Implement `handleTrendHover(evt, svg)` and `handleTrendLeave(svg)` to draw the guide line, render the indicators, and position a dynamic HTML tooltip element.
* Update `auditTimeSeries(stories)` to support interval calculations (Daily, Weekly, Monthly), generate dynamic legend control checkboxes and interval pill buttons, and render interactive hooks inside the SVG element.

### Verification Plan
* Open the control panel, navigate to the Trends tab, and confirm that:
  - Toggling intervals (Daily, Weekly, Monthly) rebuilds the trend bins correctly.
  - Checkboxes for `reality_u` and `Δu` immediately toggle line and dot visibility.
  - Hovering the mouse over the chart displays a vertical guide line and a rich tooltip with bin date ranges, story count, and averages.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Interactive telemetry makes temporal analysis significantly more readable and accessible for operators.

---
