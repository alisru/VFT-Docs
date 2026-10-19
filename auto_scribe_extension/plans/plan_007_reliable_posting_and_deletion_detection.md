# Plan 007: Reliable Post & Deletion Detection
**Date**: 2026-10-06  
**Project**: Auto-Scribe Extension  
**Status**: In Progress  

## 1. Problem Diagnosis
User reported: *"i dont think the delete or posting is being detected, there's lots of ones ive posted in the auto-scribe"*.

Root causes identified:
1. **JavaScript DOM Clears Don't Fire `input` Events**: When a website submits a post, its framework clears the text (`editor.innerText = ''` or resets state). Browsers DO NOT fire `input` or `keyup` events for programmatic DOM modifications. Auto-Scribe never knew the text was gone.
2. **Missing Plain `Enter` Detection**: In modern web apps (Gemini, Claude, ChatGPT, Facebook comments, Discord, Slack), users post using plain `Enter` (without `Shift`). Auto-Scribe was only listening for `Ctrl+Enter`.
3. **Button Selectors Missed Icon-Only Buttons**: Send buttons with SVGs or icon fonts (e.g. Gemini's `↑` button with `aria-label="Send message"`) were missed by strict regex.
4. **Rich-Text Target Instability**: In contenteditable/ProseMirror/Lexical, `e.target` fluctuates between inner `<p>` and outer containers. Without resolving to the canonical editable root (`el.closest(...)`), session IDs and saved maps lost synchronization on full delete.

## 2. Implementation Solution
1. **Canonical Root Resolution**:
   - Resolve all events via `getEditableRoot(e.target)` to guarantee stable draft IDs and WeakMap persistence across inner paragraph changes.
2. **Comprehensive Submit Trigger Tracking**:
   - `Ctrl+Enter` / `Cmd+Enter` across all fields.
   - Plain `Enter` (`!e.shiftKey`) across inputs, contenteditables, and chat fields.
   - Click listener on any button matching `/comment|post|reply|send|publish|tweet|submit|respond|share|arrow_upward/i` in text, aria-label, title, or data-testid.
   - Record `lastSubmitTime = Date.now()` and `lastSubmittedDraftId`.
3. **Active MutationObserver & Post-Submit Verification**:
   - Attach a MutationObserver to the active editor that detects when child nodes or text are cleared programmatically by website scripts.
   - Post-submit verification loop checks at 250ms, 600ms, 1200ms, and 2500ms after any submit action.
4. **Unified Text-Disappearance Logic**:
   - When text drops from `>= minChars` to `< minChars` (or 0):
     - If within 3 seconds of a submit trigger -> **MARK POSTED**.
     - If NOT within 3 seconds of a submit trigger -> **DELETE DRAFT** (user erased it).
