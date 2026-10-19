# Plan 015: Stream Grouping Compact Cards, No Redundant Site/Title, and Collapsible Groups

## Context & Problem Statement
The user reported that the dashboard stream wastes significant vertical space by repeatedly rendering the site tag and title on every single draft card within a group, even though that information is already prominently displayed at the top of the group header (e.g. `[CHATGPT.COM]` and `Formalize Moral Algebra` repeated 34 times across all 34 cards).
The user requested:
1. Eliminate the redundant site tag and title inside cards within a group.
2. Only show the post snippet and status with `(word:char)` count within group items.
3. Allow collapsing and expanding site/URL groups in the stream.

## Proposed Modifications

### 1. `dashboard.html`
- Update `#group-select` to support:
  - `Group by URL` (default)
  - `Group by Site`
  - `Flat List`
- Add a `#btn-toggle-collapse-all` button next to the group selector to allow one-click collapsing or expanding of all groups.

### 2. `dashboard.css`
- **Collapsible Groups**:
  - Add pointer styling, hover feedback, and a chevron icon (`▼`) to `.url-group-header`.
  - Add `.url-group.collapsed .url-group-cards { display: none; }`.
  - Add `.url-group.collapsed .group-collapse-icon { transform: rotate(-90deg); }`.
- **Compact Draft Cards (`.draft-card-compact`)**:
  - Reduce padding from `12px` to `8px 10px` and gap to `4px`.
  - Eliminate the separate footer line: status badge and `(word:char)` count sit on `.card-top`.
  - Place timestamp and quick actions (`[↩/✓]`, `[📋]`, `[🗑️]`) on the right side of `.card-top`, cleanly flipping from timestamp to action buttons on card hover.
  - Compact 2-line snippet display.
  - Saves over 50% vertical space per card.

### 3. `dashboard.js`
- Modify `createDraftCard(d, isGrouped)`:
  - If `isGrouped` is true:
    - Omit the site tag and card title.
    - Render status badge + `(${words}w : ${chars.toLocaleString()}c)`.
    - Render snippet.
    - Embed hover action buttons (`status`, `copy`, `delete`).
  - If `isGrouped` is false (flat list):
    - Retain site tag and title for context.
- Support both `groupBy === 'url'` and `groupBy === 'site'`.
- Maintain a `collapsedGroups` Set to preserve collapsed state across filtering and sorting cycles.
- Wire `#btn-toggle-collapse-all` to toggle all groups collapsed/expanded.

## Verification
- Validate JS syntax with `node -c`.
- Verify CSS classes and HTML structure.
