# Plan 005: "Posted" vs "Unposted" Status Tracking
**Date**: 2026-10-06  
**Project**: Auto-Scribe Extension  
**Status**: Ready for Implementation  

## 1. Goal
Address the user's inquiry: *"ok so idk if we can track 'posted' status, probably not, but can we group by url pls"*.
While web pages don't have a single standardized DOM API for "post completed", we can reliably track "posted" status using multi-layer submission heuristics + content clearing detection + manual toggle fallback.

## 2. Detection Mechanisms
1. **Submit Shortcut Listener (`Ctrl+Enter` / `Cmd+Enter`)**:
   - Universal shortcut on Reddit, X/Twitter, Facebook, LinkedIn, GitHub, Discord, Slack.
   - When detected on an active scribed element, queue verification.
2. **Action Button Click Listener**:
   - Listen globally for clicks on buttons, submit inputs, or role="button" matching keywords: `Comment`, `Post`, `Reply`, `Send`, `Publish`, `Tweet`, `Submit`.
   - Also match `button[type="submit"]` and platform-specific test IDs (`[data-testid*="tweetButton"]`, `[data-testid*="submit"]`, `shreddit-comment-action-row`).
3. **Form `submit` Event Listener**:
   - Standard HTML `<form>` submit events on any parent form containing the scribed input.
4. **Post-Submission Content Clearing Verification**:
   - 300ms to 1200ms after a submit trigger, check if the input element has been cleared or removed from DOM. If text is cleared or form submitted, mark status as `'posted'`.
5. **Dashboard Manual Override**:
   - Add a "Mark as Posted" / "Mark as Draft" button in the reader pane and on card actions for manual control.
6. **Dashboard Filtering**:
   - Add a Status filter in the stream controls: `All`, `Drafts (Unposted)`, `Posted`.
