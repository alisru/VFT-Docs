# Token Efficiency Audit — `/bsky-reply-batch` Workflow
**Date:** 2026-06-05  
**Scope:** Full pipeline from workflow trigger → harvest → subagent spawn → registry rebuild

---

## Summary

The pipeline is architecturally sound and the parent/subagent separation is the right approach. However, there are **7 identified inefficiency vectors** spread across the workflow file, the master instructions index, the subagent prompts, and the evaluation modules themselves.

---

## Findings

### 🔴 HIGH IMPACT

---

#### FIND-01: Workflow file forces parent to read `operational_pipelines.md` — a *Sub-Agent Only* module

**File:** `bsky-reply-batch.md` → `bluesky_bot_instructions.md` (line 12)

The workflow's Step 2 says:
> "Operational Pipeline: Read `operational_pipelines.md`..."

But `bluesky_bot_instructions.md` explicitly flags `operational_pipelines.md` as **Module C — Sub-Agents Only**:
> "DO NOT open Module A (Convergence Test), Module B (Thread Formatting), or **Module C (Operational Pipelines)**. These are for sub-agents only."

**Waste:** The parent agent reads ~3,400 bytes of subagent-targeted execution steps it does not need. In a context window where each parent turn is expensive (and the parent model here is Claude Sonnet with thinking enabled), this pollutes parent context with irrelevant step-level detail on every invocation.

**Fix:** Remove Step 2 from the workflow trigger. The parent only needs Module D (subagent_spawning.md). The pipeline steps are for the *evaluators*, not the orchestrator. The workflow should read:
```
1. Read bluesky_bot_instructions.md (master index — rules + script locations)
2. Run harvest script (Step 1 of pipeline)
3. Read subagent_spawning.md → spawn evaluators (Step 2)
4. Parse JSON from subagent responses → write files (Step 3)
5. Run rebuild_registries.py (Step 4)
```

---

#### FIND-02: `thread_formatting.md` is 11,613 bytes — loaded in full by every evaluator subagent

**File:** `thread_formatting.md`

The 14-step blueprint with full examples is ~11.6 KB. With 4 concurrent evaluator subagents each reading this, you burn ~46 KB of input tokens just on formatting instructions — before any story text is processed.

**Observations:**
- The canonical example JSON (Section 4, lines 146–179) is ~1,800 characters of repetition of what's already in the step descriptions.
- The example per-step text (Elements 0–13, lines 41–143) has both a description *and* a quoted example for every element. Many examples are verbose (Element 6 alone is ~480 characters of example text).

**Fix options (pick one or combine):**
- **A) Create `thread_formatting_lite.md`** — strip the per-element quoted examples (keep descriptions only), remove the canonical JSON section (already in the schema description). Estimated 40–50% size reduction (~5–6 KB instead of 11.6 KB).
- **B) Inline a minimal schema reference** in `subagent_spawning.md` itself so evaluators don't need to open a separate file for the most-used rules. The full doc remains available but is not loaded by default.

---

#### FIND-03: `convergence_lite.md` loads the full p·t mathematical definition chain — not needed for batch mode

**File:** `convergence_lite.md` (11,451 bytes)

The file is already the "lite" version, but it still contains:
- Full measurement chain diagram (lines 25–50, ~1,200 chars)
- Detailed good/bad/evil/saintly definitions with formulas (lines 113–131)
- Conservative vs. innovative neutral discussion (lines 118–122)
- Full zone anchor table and perceptual inversion flag (lines 175–177)
- Object State blanking rule (line 179)
- Fake Maximiser and Helxis forensic tests (Phase 4, lines 196–204)

For **batch news story evaluation** (fast-moving news, not institutional deep audits), the evaluator's stated goal is:
> "Calculate coordinates and canonical path name *internally*. Do NOT output the 5-Phase report."

The Phase 4 forensic stress tests (Fake Maximiser / Helxis) and the p·t primitive derivations add ~2.5 KB that is effectively documentation the evaluator reads but rarely uses in output.

**Fix:** Create `convergence_batch.md` — a stripped version for the evaluator batch workers. Keep:
- The 7 Planes table
- The υ axis scoring table
- The ψ axis scoring table
- The Path Names table
- Phase 1 pass/fail conditions table
- Phase 3 ΔH threshold line

Remove or defer to a reference note:
- The full measurement chain diagram
- The p·t mathematical derivation prose
- The good/bad/evil/saintly philosophical definitions
- Phase 4 (Fake Maximiser / Helxis) — add a 1-line note: "If Helxis or Fake Maximiser are clearly present, flag in verdict. Full definitions in `convergence_lite.md`."

Estimated reduction: ~4–5 KB (35–40%).

---

### 🟡 MEDIUM IMPACT

---

#### FIND-04: Subagent prompt template uses ambiguous index notation

**File:** `subagent_spawning.md`, line 46

```
"Batch Evaluator Worker [Worker ID]. Your task is to evaluate Batch [Batch ID]
(Stories [Start Index] to [End Index], which are indices [Start Index - 1] to [End Index - 1])"
```

The double-counting (`Stories 1 to 5, which are indices 0 to 4`) has caused real confusion in past runs — subagents have evaluated wrong story ranges or asked clarifying questions back to the parent, burning a round-trip.

**Fix:** Simplify to array-index-only language:
```
"Your task is to evaluate stories at array indices [N] through [M] (0-based) 
from harvested_candidates.json."
```
Drop the "Stories X to Y" human-numbering entirely. The model counts from 0 natively.

---

#### FIND-05: `bluesky_bot_instructions.md` Section 4 (Profile Bio) is dead weight for the parent

**File:** `bluesky_bot_instructions.md`, lines 62–69

The parent agent reads the full master index including the Bluesky profile bio/persona text. This section is irrelevant to batch orchestration — it exists for the UI/posting layer.

**Fix:** Move the Profile Bio section to a separate `persona.md` or embed it only in the posting scripts. The master index loaded by the parent orchestrator should contain only operational rules and script locations.

---

#### FIND-06: Evaluator prompt says "Do not read the master index" — but it still loads TWO files sequentially before working

**File:** `subagent_spawning.md`, lines 50–52

Each evaluator's **mandatory first action** is to run `view_file` on:
1. `convergence_lite.md`
2. `thread_formatting.md`

These are loaded sequentially (one tool call each, one LLM turn each before work begins). That's 2 idle turns per evaluator × 4 evaluators = **8 mandatory warm-up turns** producing no story output.

**Fix:** Pass both file contents directly inside the spawning prompt as inline text blocks (using the compressed/lite versions from FIND-02 and FIND-03). This eliminates the file-read warm-up turns entirely. Each subagent starts working immediately.

> Note: This requires the parent to read the lite files once and embed them. Net cost: parent reads ~8 KB once → saves 8 × 2 subagent idle turns. Break-even at 1 evaluator; profitable from 2+.

---

### 🟢 LOW IMPACT / HOUSEKEEPING

---

#### FIND-07: `operational_pipelines.md` Step 2 description says evaluators output "JSON blocks in their chat responses"  — but this is inconsistently enforced

**File:** `operational_pipelines.md`, line 40

> "Outputs the completed 14-step evaluation JSON blocks directly in their chat responses to the parent (consuming 0 file-write tool calls)"

In practice (based on prior batch runs), evaluators have occasionally attempted to write files mid-evaluation, then been corrected by the parent. The constraint is stated in `subagent_spawning.md` but the framing is weak:

> "You are strictly prohibited from calling any file writing tools"

**Fix:** Strengthen the prohibition with a consequence framing:
> "Any file write tool call will cause your output to be discarded. Output JSON in your final message only."

This is a low-cost prompt hardening change.

---

## Token Cost Summary

| Finding | File(s) Affected | Est. Token Waste per Run | Effort to Fix |
|---|---|---|---|
| FIND-01 | `bsky-reply-batch.md` | ~850 parent tokens | Trivial — 1 line edit |
| FIND-02 | `thread_formatting.md` | ~12,000 tokens × 4 evaluators | Medium — create lite version |
| FIND-03 | `convergence_lite.md` | ~6,000 tokens × 4 evaluators | Medium — create batch version |
| FIND-04 | `subagent_spawning.md` | Variable (retry cost) | Trivial — rephrase |
| FIND-05 | `bluesky_bot_instructions.md` | ~400 parent tokens | Trivial — relocate section |
| FIND-06 | `subagent_spawning.md` | 8 idle LLM turns | High effort, high payoff |
| FIND-07 | `subagent_spawning.md` | Low (behaviour correction cost) | Trivial — rephrase |

**Priority order:** FIND-01 → FIND-04 → FIND-05 → FIND-07 (trivial edits first) → FIND-02 → FIND-03 (new lite files) → FIND-06 (inline embedding, highest payoff but most effort)

---

## Recommended Actions (Prioritised)

1. **[IMMEDIATE]** Edit `bsky-reply-batch.md` — remove the instruction to read `operational_pipelines.md` from the parent. The parent doesn't need it.
2. **[IMMEDIATE]** Edit `subagent_spawning.md` — fix the index notation (FIND-04) and strengthen the no-file-write constraint (FIND-07).
3. **[IMMEDIATE]** Edit `bluesky_bot_instructions.md` — move or strip the Profile Bio section (FIND-05).
4. **[MEDIUM]** Create `thread_formatting_lite.md` — examples-stripped version for evaluators (FIND-02).
5. **[MEDIUM]** Create `convergence_batch.md` — tables-only version stripping prose and Phase 4 (FIND-03).
6. **[FUTURE]** Update `subagent_spawning.md` to inline the lite content directly in the prompt so subagents need zero file reads on startup (FIND-06).
