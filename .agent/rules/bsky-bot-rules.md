# Bluesky Bot Posting Rules

Rules for generating Aletheia Bot thread configs and posts. Source of truth: `bluesky_bot/bluesky_bot_instructions.md`

---

## Character & Format Constraints
- Every post MUST be strictly under 250 characters. No exceptions.
- NEVER prefix posts with numbers (no `1/`, `2/13`, etc.). Thread reads as a seamless story.
- Strip all tracking parameters from URLs (no `?utm_source=...`).
- No robotic prefixes like `Subject:`, `The Claim:`, `The Reality:`, `What's happening:`.

---

## Thread Structure
- Follow the official step-by-step thread formatting guidelines strictly:
  - Standard Mode: Follow [thread_formatting.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting.md)
  - SON Mode: Follow [thread_formatting_son.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting_son.md)

---

## Element 0: The Hook (Critical)
Must contain ALL of the following in order:
1. A punchy, custom, human-style scene-setter one-liner (exposing structural framing, irony, or systemic dynamics). **DO NOT** repeat the subject title or copy/summarize the candidate text dryly.
2. The news title (no "Subject:" prefix).
3. The evidence line on its own line: `Evidence: [A in 2-5 words], [B in 2-5 words], [C in 2-5 words]`

## Evidence Line Fills (2-5 words each — HARD LIMIT)
- [A] = what the actor claims (their stated ideal), in 2-5 concrete words
- [B] = what physically happened on the ground, in 2-5 concrete words
- [C] = what the stated ideal would structurally require to be coherent, in 2-5 concrete words
- WRONG: abstract summaries, jargon, academic language
- CORRECT: physical events and physical requirements only

---

## URL Rules
- `"link"` key = the actual external news article URL
- `"target_url"` key = the Bluesky post URL (reply mode only, else empty)
- Never hallucinate or guess a URL. Verify it resolves before using it.

---

## JSON Config Keys (exact, in order)
`subject`, `link`, `claim_u`, `claim_psi`, `real_u`, `real_psi`, `mode`, `target_url`, `posts`, `rkeys` (optional), `post_urls` (optional), `status`, `id`

Do NOT include: `subject_slug`, `verdict`, `graph_img`, or any other custom keys.

---

## Default Mode
ALWAYS dry run by default. Only post live when explicitly run with `--live` flag after manual review.

---

## Registry Compilation Security (No Data Pruning)
- **NEVER strip, remove, or omit the `"posts"` field** (or any other generated metadata like `"rkeys"`, `"post_urls"`, `"actors"`, etc.) from `stories_registry.js` during registry compilation or store rebuild.
- **NEVER attempt to optimize file sizes** by deleting, truncating, or omitting the `"posts"` arrays from compiled stories. The frontend thread emulator relies completely on the `"posts"` array to function.
- File size optimization for `stories_registry.js` must be handled on the client side via chunked/lazy rendering (already implemented in `control_panel.html`), NOT by destroying database integrity on disk.

