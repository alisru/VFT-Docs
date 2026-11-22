# Implementation Plan v41 — Permanent Castration of Rebuild Mutation Loop & Full Remediation

## 1. Problem Statement & Forensic Root Cause

The user discovered that story audits on disk (such as `factcheck_first_home_buyers_1_8m_alexandria_sydney.json`) suffered catastrophic verdict and coordinate corruption:
- A $1.8M property auction framed by real estate agents as a "buyers' market" was stamped with `Claim: (1.0, 1.0) -> Real: (0.69, 1.0) | Verdict: PASS — Small Fall from Grace`.
- Stated claims across virtually all 22 active drafts were cloned to `(1.0, 1.0)`.
- Top-level JSON coordinates (`claim_u: 1.0, real_u: 0.69`) directly contradicted the post text (`Post 1: (+0.5, +0.5)`, `Post 2: (+0.1, -0.1)`).

### Forensic Root Cause: The Rebuild Registry Mutation Loop
1. **The Static Prompt Template**: In `google_ai_studio_one_shot.py` (lines 1413–1429), the prompt's `OUTPUT FORMAT` example provided a static boilerplate dictionary for `stated_forces`:
   `{"GG": {"S": 1.2, "O": 0.0}, "GE": {"S": 0.0, "O": 1.2}, "LG": {"S": 1.0}, "LE": {"O": 0.8}, "GP": {"S": 1.2}, "BP": {"O": 1.2}}`
   The LLM copied this exact force block into `stated_forces` for every single candidate.
2. **The Rogue Recalculator**: In `rebuild_registries_son.py` (lines 171–225, 271, 383), `process_and_update_coordinates(cfg, authoritative_file)` was called on EVERY story during registry builds. It called `calculate_son_coordinates(cfg["stated_forces"])`, which mathematically resolved that copied template into `(1.0, 1.0)`, and overwrote `cfg["claim_u"]` and `cfg["claim_psi"]`.
3. **The Verdict Rape**: `rebuild_registries_son.py` then immediately called `enforce_deterministic_trajectory(cfg)` (line 221). Because `claim_u = 1.0` and `real_u = 0.69` (where `real_u > 0`), it declared the story a `PASS`, stamped `Small Fall from Grace`, and **forcibly overwrote Post 3 (`Verdict: PASS...`) and Post 8 (`The Trajectory:...`) on disk**.
4. **Desynchronization**: Because Post 1 and Post 2 contained broken Unicode replacement characters (`\ufffd`), the text-replacement failed to update Posts 1 and 2, leaving the file internally torn in half.

---

## 2. Architectural Invariants (Never to be Violated Again)

1. **Registry Compilers Are Read-Only (Idempotent Projection Invariant)**:
   - `rebuild_registries.py` and `rebuild_registries_son.py` must ONLY read story files, build `stories_registry.js`, and generate index summaries.
   - **ABSOLUTE BAN**: A registry compiler must NEVER write back to `factcheck_*.json`, must NEVER recalculate coordinates from forces, and must NEVER overwrite post text or verdicts.
2. **Authoritative Metadata Invariant**:
   - The coordinates, posts, and verdicts generated during the audit are authoritative. No downstream helper script is permitted to mutate them on disk.
3. **Anti-Boilerplate Invariant**:
   - Evaluation prompts must never provide static force dictionaries or pre-filled coordinate examples in the output schema instructions that the model can lazily mirror.
4. **Active Drafts Invariant**:
   - `stories/` is the ONLY active drafts folder. No subfolders like `stories/drafts/` are permitted.

---

## 3. Step-by-Step Remediation Plan

### Step 1: Castrate `rebuild_registries_son.py`
- Remove all calls to `process_and_update_coordinates()` in `rebuild_registries_son.py` (lines 271 and 383).
- Remove the file write-back block in lines 384–389.
- Ensure `rebuild_registries_son.py` only performs read-only parsing, image card/graph generation, and registry compilation.

### Step 2: Remove Boilerplate Force Examples in `google_ai_studio_one_shot.py`
- Replace static non-zero force values in the prompt schema example with generic instructions so the model evaluates real forces instead of mirroring a template that resolves to `(1.0, 1.0)`.

### Step 3: Surgically Remediate `factcheck_first_home_buyers_1_8m_alexandria_sydney.json`
- Ground the evaluation in actualist reality:
  - Subject: Real estate marketing spin framing $1.8M inner-city entry price as a "buyers' market".
  - Stated Claim: `(+0.80, +0.60)` — Inclusive Active Capacity (framing market as accessible to young buyers).
  - Ground Reality: `(-0.90, +0.75)` — Greatest Lie / Deception (corporate spin to protect sales commission and normalize debt).
  - Verdict: `FAIL — Fall into Deception`.
  - Geodesic: `Red Top (The Imperial Trap)`.
  - Modal Dynamics: `can be` -> `is not`.
  - Ensure Post 1, Post 2, Post 3, and JSON keys are 100% synchronized with clean UTF-8.

### Step 4: Audit & Remediate the Remaining 21 Active Stories in `stories/`
- Review each active story in `stories/` to eliminate cloned `(1.0, 1.0)` Stated Claims and ensure the verdicts, coordinates, and posts match the actual journalistic event.

### Step 5: Verification & Clean Registry Compile
- Run `rebuild_registries_son.py` to verify it compiles `stories_registry.js` without modifying a single story file on disk.
