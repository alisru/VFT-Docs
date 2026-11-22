# Plan 017: Stream Header Layout, Filter Wrapping, and Sort By Visibility

## Context & Problem Statement
The user reported that `Sort by` disappeared and `Group by` was cut off in the dashboard stream pane (`media_1793172387431_351c6304.png`).
Inspection reveals:
- `.app-main` sets `.stream-pane` to a fixed 380px width (`grid-template-columns: 240px 380px 1fr`).
- `.stream-header` used a single horizontal flex line (`display: flex; justify-content: space-between; align-items: center;`) with `nowrap`.
- In a 380px container, Title + Count Badge (~120px), Status (~110px), Group (~130px), Collapse All (~85px), and Sort (~120px) require >560px of horizontal space.
- As a result, the right side overflowed the pane: `Group by` was cut off, while `Collapse All` and `Sort by` were pushed completely outside the visible screen.

## Proposed Modifications

### 1. `dashboard.css`
- **Two-Row Stream Header**:
  - Update `.stream-header` to `display: flex; flex-direction: column; gap: 8px; padding: 10px 14px;`.
  - Row 1 (`.stream-title-row`): Displays the active site title (`#stream-active-site`) on the left and the draft count badge (`#filtered-count-badge`) on the right (`justify-content: space-between;`).
  - Row 2 (`.stream-controls`): Holds `Status:`, `Group:`, `Sort:`, and the `Collapse All` button in a flexible wrapping container (`display: flex; align-items: center; flex-wrap: wrap; gap: 8px;`).
- **Control Select Inputs**:
  - Set compact padding and clean min-widths so labels and dropdowns fit cleanly.
- **Main Layout Grid**:
  - Update `grid-template-columns: 240px minmax(380px, 420px) 1fr;` to give the stream pane breathing room while maximizing reader space.

### 2. `dashboard.html`
- Keep the logical order clean:
  - `Status:` dropdown
  - `Group:` dropdown
  - `Sort:` dropdown
  - `Collapse All` button

## Verification
- Validate JS syntax with `node -c`.
- Inspect CSS rules to guarantee zero horizontal clipping.
