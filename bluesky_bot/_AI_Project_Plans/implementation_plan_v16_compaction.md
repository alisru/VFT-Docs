# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 16 (Active): Unlimited Hypocrisy Leaderboards Scroll Lists

### Goal Description
Modify the hypocrisy leaderboards (for both Actors and Outlets) to remove the threshold filtering (`minN = 2` stories) and max row limits (`maxRows = 60` rows). Render them inside scroll containers with sticky headers so that the user can browse every tracked actor/outlet.

### User Review Required
> [!NOTE]
> Leaderboards will now list one-off entries (n=1) and will have scroll bars inside their respective panel frames.

### Proposed Changes

#### [MODIFY] [control_panel.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/control_panel.html)
* Updated `_hypocrisyTable` to remove the story count threshold (`minN`) filter and display all rows.
* Wrapped the grid table in a `.scroll-container` style div block with `max-height: 400px; overflow-y: auto`.
* Styled table column headers as `position: sticky; top: 0; background: var(--panel-bg); z-index: 2` to keep them visible while scrolling.
* Cleaned up footer limits summary text blocks.

### Verification Plan
* Open the control panel, go to the Trends/Audit tab, and confirm that both the Actor and Outlet leaderboards show a scrollbar and list all actors/outlets (including single-story entries) with sticky headers.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Complete and unrestricted view of the entities database improves auditing efficiency.

---
