# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 15 (Active): Calibration Drift Graph Axis Correction

### Goal Description
Correct the axis mapping inside the `auditCalibration(stories)` function on the trends dashboard. The original implementation plotted Stated Judgement vs Reality using Will ($\psi$) on the horizontal axis and Morality ($u$) on the vertical axis. This has been flipped to align with standard convention (Morality $u$ horizontal, Will $\psi$ vertical).

### User Review Required
> [!NOTE]
> This is a client-side layout correction for SVG coordinate plotting. No file structures or backend databases are affected.

### Proposed Changes

#### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/control_panel.html)
* Swapped variables in `auditCalibration` so `x1` and `x2` calculate based on morality values (`s.claim_u`, `s.real_u`), and `y1`/`y2` calculate based on will values (`s.claim_psi`, `s.real_psi`).
* Corrected vertical labels to read `+ψ` and `−ψ`, and horizontal label to read `u →`.

### Verification Plan
* Open the control panel, navigate to the Trends/Audit tab, scroll to the **Calibration Drift** graph, and confirm that the X axis represents morality ($u$) and the Y axis represents will ($\psi$).

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.0)` -> Greater Good & Productive Action.
* Verdict: Ensures that the user dashboard graphs show correct, standard coordinates, avoiding any user interpretation confusion.

---
