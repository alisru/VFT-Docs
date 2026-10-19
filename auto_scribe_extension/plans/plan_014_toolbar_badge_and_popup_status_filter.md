# Plan 014: Toolbar Badge Count and Extension Popup Unposted Filter

## Context & Problem Statement
The user reported that while the dashboard (`dashboard.html`) correctly reflected updated/posted drafts, the browser extension button (toolbar icon and popup menu `popup.html` / `popup.js`) was still showing old/stale counts:
1. **Toolbar Icon Badge**: Showed `99+` because `background.js` calculated the badge count as `Object.keys(drafts).length`, counting all 323 total historical records in storage rather than filtering for unposted drafts (`status !== 'posted'`).
2. **Popup Stat Cards**: Showed `323 Drafts Saved` without distinguishing between active unposted drafts and posted records.
3. **Popup Recent List**: Section was labeled "Recent Unposted Drafts", but `popup.js` took `drafts.slice(0, 4)` directly from the unfiltered drafts list, which was dominated by already posted entries.
4. **No Real-Time Sync in Popup**: If the popup remained open while drafts changed in storage, it did not refresh.

## Proposed Modifications

### 1. `background.js`
- Modify `updateBadge(drafts)` to calculate `unpostedCount = draftsList.filter(d => d && d.status !== 'posted').length`.
- Only show badge text when `unpostedCount > 0` (e.g. `1`, `2`, ..., `99+`). If all drafts are posted or cleared, badge text is empty (`''`).
- Add `chrome.storage.onChanged` listener in `background.js` to ensure the badge stays updated in real time whenever `scribe_drafts` changes.

### 2. `popup.html`
- Update the stats bar to display two targeted metrics:
  - **Active Drafts** (`id="stat-drafts"`, highlighted accent)
  - **Posted** (`id="stat-posted"`, green accent)
- Retain clean styling and dashboard link.

### 3. `popup.js`
- Extract drafts and separate into `unposted` (`d.status !== 'posted'`) and `posted` (`d.status === 'posted'`).
- Update `statDrafts` and `statPosted` counters.
- Populate "Recent Unposted Drafts" strictly from `unposted.slice(0, 4)`.
- If `unposted.length === 0`, display a friendly status message: `"✓ No unposted drafts. All drafts have been posted or cleared."`
- Add `chrome.storage.onChanged` listener to dynamically update the popup if storage changes while the popup is open.

## Verification
- Run `node -c` on `background.js` and `popup.js`.
- Confirm no broken references or syntax errors.
