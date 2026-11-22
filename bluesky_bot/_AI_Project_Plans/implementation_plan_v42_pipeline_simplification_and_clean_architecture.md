# Implementation Plan v42 — Pipeline Simplification, Hazard Remediation & Mode Modularization

**Date:** 2026-11-10  
**Project:** Aletheia Bluesky News Factcheck & Audit Bot (`bluesky_bot`)  
**Desire Tracking:** `semantic-gluon` Project `PRJ-BSKY-BOT` (`DES-028`)

---

## 1. Goal Description

Address all structural bottlenecks, duplicate prompt injections, contradictory schema definitions, broken archived module imports, and code bloat identified during the full architectural audit of `bluesky_bot`.

This plan accomplishes five key objectives without changing your Convergence Test philosophy, removing any operational modes, or overriding AI judgement with mechanical formulas:
1. **Restore Core Modules:** Move [`audit_crossref.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/_Archive/legacy_patches/audit_crossref.py) and [`research_probe.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/_Archive/legacy_patches/research_probe.py) out of `_Archive/legacy_patches/` back to `bluesky_bot/` root to unbreak Direct Reply Dispatcher and `--probe` mode.
2. **Eliminate Duplicate Context Injections:** Ensure search grounding dossiers and multi-source event clusters are injected into Gemini requests exactly once.
3. **Resolve Output Schema Contradictions:** Harmonize the two schema copies in [`build_output_format()`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py#L1409-L1605) so `item[27]` (`aspects`) strictly uses the `v38` direct coordinate format (`[{"aspect": "...", "claim_u": ..., "claim_psi": ..., "real_u": ..., "real_psi": ..., "verdict": "...", "reason": "..."}]`) instead of the deprecated `v23` force-averaging format.
4. **Purge Dead Legacy Harvester Code:** Remove lines 302–1125 in [`google_ai_studio_one_shot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py#L302-L1125) (an unused 820-line copy of `harvest_news`) to shrink the file by ~30%, making [`harvest_candidates.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/harvest_candidates.py) the single source of truth.
5. **Unify Registry Rebuilding:** Update [`rebuild_registries.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/rebuild_registries.py) to delegate directly to the `v41` read-only compiler in [`rebuild_registries_son.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/rebuild_registries_son.py).
6. **Clean Mode Rule Injections:** Move inline Python string directives (`COORDINATE_SCALE_CALIBRATION`, `core_concept_directive`) into their respective external `.md` files so `google_ai_studio_one_shot.py` loads clean, non-duplicated instructions.

---

## 2. User Review Required

> [!IMPORTANT]
> - **Zero AI Judgement Overwrite:** No Python math will ever override or cap `(υ, ψ)` coordinates or verdicts. All coordinates and verdicts remain 100% judged by the AI reasoning through the Convergence Test.
> - **All Modes Preserved:** All CLI flags (`--son`, `--potential`, `--multi-aspect`, `--spiritual`, `--compact`, `--compact-single`, `--five-word`, `--search`, `--probe`) and UI controls in `AletheiaLauncher.pyw` remain functional.
> - **Zero API Calls During Migration:** No AI Studio tokens will be burned during code refactoring or test runs.

---

## 3. Inventory of What is Broken & Proposed Changes

### Component 1: Core Module Restoration (`DES-028-T1`)
In `v37`, an automated archival script moved active files into `_Archive/legacy_patches/`.
- `direct_reply_dispatcher.py:42` imports `audit_crossref`, causing an `ImportError`.
- `google_ai_studio_one_shot.py:2934` imports `research_probe`, causing an `ImportError`.

#### Proposed Fix:
Move both files back to `bluesky_bot/` root:
- `bluesky_bot/_Archive/legacy_patches/audit_crossref.py` $\to$ `bluesky_bot/audit_crossref.py`
- `bluesky_bot/_Archive/legacy_patches/research_probe.py` $\to$ `bluesky_bot/research_probe.py`

---

### Component 2: Eliminate Duplicate Context & Search Dossier Injections (`DES-028-T2`)
In [`google_ai_studio_one_shot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py):
- When search grounding runs, line 1670 stores the grounding text in `c["grounding_context"]`, and lines 1962–1966 append the same text to `extra_context`.
- Line 1989 puts it into `cand_entry["verified_grounding"]`.
- Line 1998 appends `extra_context` to `user_payload`.
- Line 2000 serializes `clean_candidates` (which contains `verified_grounding`), resulting in the identical text being sent twice in the same payload.

#### Proposed Fix:
Keep `extra_context` as the single canonical location for external search dossiers and topic clusters in `user_payload`, and omit `verified_grounding` from the individual candidate JSON objects when `extra_context` already contains it.

---

### Component 3: Resolve Contradictory `item[27]` Aspect Schemas (`DES-028-T3`)
In [`google_ai_studio_one_shot.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py#L1409-L1605):
- Lines 1480 defines `item[27]` using the `v38` format:
  ```json
  [{"aspect": "Aspect Name", "claim_u": 0.5, "claim_psi": 0.0, "real_u": -0.9, "real_psi": -0.8, "verdict": "FAIL", "reason": "1-line reason under 60 chars"}]
  ```
- Lines 1566–1579 (under `EXAMPLE RESPONSE`) defines `item[27]` using the deprecated `v23` format with `stated_forces` and `actual_forces`.

#### Proposed Fix:
Update the `EXAMPLE RESPONSE` in `build_output_format()` to use the exact same `v38` coordinate schema as line 1480, completely eliminating the prompt contradiction.

---

### Component 4: Purge Dead 820-line Harvester from `google_ai_studio_one_shot.py` (`DES-028-T4`)
Lines 302–1125 in `google_ai_studio_one_shot.py` contain an uncalled copy of `harvest_news()`, RSS feeds, and scraping functions. `harvest_candidates.py` is the actual active harvester called by `main()`.

#### Proposed Fix:
Safely delete the dead lines 302–1125 from `google_ai_studio_one_shot.py`, reducing the file size by ~820 lines without altering any evaluation, formatting, or execution logic.

---

### Component 5: Unify Registry Rebuilding (`DES-028-T5`)
[`rebuild_registries.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/rebuild_registries.py) is a diverged legacy script that does not handle all 18 attractor variables or the `v41` read-only invariant.

#### Proposed Fix:
Update `rebuild_registries.py` to import and execute `rebuild_registries_son.main()`, ensuring that any call to either script executes the authoritative, read-only `v41` compiler.

---

### Component 6: Clean Mode Rule Injections (`DES-028-T6`)
Move `COORDINATE_SCALE_CALIBRATION` and `core_concept_directive` into the external `.md` files ([`convergence_son_potential.md`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/convergence_son_potential.md) and [`thread_formatting_potential.md`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting_potential.md)) so the Python code loads clean markdown files rather than stringing raw Python essays together.

---

## 4. Verification Plan

### Automated Checks
1. **Module Compilation:**
   ```powershell
   python -m py_compile "e:\Vector Field Theory\VFT Docs\bluesky_bot\google_ai_studio_one_shot.py"
   python -m py_compile "e:\Vector Field Theory\VFT Docs\bluesky_bot\direct_reply_dispatcher.py"
   python -m py_compile "e:\Vector Field Theory\VFT Docs\bluesky_bot\audit_crossref.py"
   python -m py_compile "e:\Vector Field Theory\VFT Docs\bluesky_bot\research_probe.py"
   python -m py_compile "e:\Vector Field Theory\VFT Docs\bluesky_bot\rebuild_registries.py"
   python -m py_compile "e:\Vector Field Theory\VFT Docs\bluesky_bot\rebuild_registries_son.py"
   ```
2. **Import Verification:**
   Run a short inline Python check confirming `from audit_crossref import find_audit_crossref` and `from research_probe import generate_research_probe` succeed without `ModuleNotFoundError`.
3. **Dry-Run Prompt Inspection (Zero Token API Cost):**
   Print the generated prompt string from `build_system_instruction()` and `build_output_format()` to verify:
   - Zero duplicate search dossiers.
   - Zero conflicting `item[27]` schemas.
   - Correct character limits and post sequences.
