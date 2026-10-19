# Plan 004: Group Drafts by URL / Thread Context
**Date**: 2026-10-06  
**Project**: Auto-Scribe Extension  
**Status**: In Progress  

## 1. Goal
Allow drafts in the dashboard to be **grouped by URL** (e.g. specific Reddit thread, Facebook post/group, or webpage), so drafts written on the same page are organized together under clean thread/URL headers instead of a disorganized flat stream.

## 2. UI / UX Design
1. **Grouping Controls**:
   - Add a toggle in the stream header:
     `[ 📑 Group by URL / Thread ]` vs `[ ⏱️ Flat Timeline ]`
   - Default to **Group by URL / Thread**.
2. **URL Group Headers in Stream**:
   - Clean grouping header for each unique URL:
     - Thread / Page Title (e.g. `r/australia: Energy Transition Megathread`)
     - Clickable URL link icon opening the exact thread
     - Count badge: e.g. `3 drafts on this page`
   - Nested draft cards belonging to that specific URL.
3. **Sidebar URL Sub-Tree / Quick Jump**:
   - Shows site counts, and when a site is selected, filters to that site's URLs.
4. **Clean Canonical URL Normalization**:
   - Strips query tracking junk like `?utm_source=...`, `?ref=...`, `#comment-...` to ensure multiple comments on the same post group together accurately under the same canonical URL.
