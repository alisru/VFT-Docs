# Bluesky Bot Posting Rules

Rules for generating Aletheia Bot thread configs and posts. Source of truth: `bluesky_bot/bluesky_bot_instructions.md`

---

## Character & Format Constraints
- Every post MUST be strictly under 250 characters. No exceptions.
- NEVER prefix posts with numbers (no `1/`, `2/14`, etc.). Thread reads as a seamless story.
- Strip all tracking parameters from URLs (no `?utm_source=...`).
- No robotic prefixes like `Subject:`, `The Claim:`, `The Reality:`, `What's happening:`.

---

## Thread Structure
- Exactly 14 posts in the JSON `"posts"` array — always.
- The 14 logical steps in order: Hook → Claim → Reality → Verdict → Context → Nuance → Breakdown → Switch → Trajectory → Destination → Unavoidables → Trinary Persona Reaction → Aletheia Synthesis → Resolution Vector.

---

## Step 1: The Hook (Critical)
Must contain ALL of the following in order:
1. A punchy, human scene-setter sentence.
2. The news title (no "Subject:" prefix).
3. `Source: [URL]` (if root mode) or `Target Post: [URL]` (if reply mode). URL must be the REAL, verified external news article URL — never a Bluesky post URL in this field.
4. The evidence line on its own line: `Evidence: [A in 2-5 words], [B in 2-5 words], [C in 2-5 words]`
5. The exact tag on its own final line: `Psochic Hegemony Graph`

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
