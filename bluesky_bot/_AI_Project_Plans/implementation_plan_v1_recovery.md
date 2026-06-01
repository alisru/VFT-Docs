# Implementation Plan: Restoring HTML Viewer & High-Fidelity Candidate Regeneration

We are remediating the catastrophic failure from the previous subagent run. The previous worker agents produced malformed and corrupted JSON structures containing mismatched coordinate keys (e.g. `stated_u`, `stated_coords`, etc. instead of `claim_u` and `claim_psi`), which broke the `control_panel.html` viewer.

To resolve this permanently and ensure this NEVER happens again, we are executing a strict three-phase recovery plan.

## 1. Clean-Up and Restoration (completed)
* **Delete Corrupted Files:** Identify and delete all 21 corrupted `factcheck_*.json` files inside `bluesky_bot/stories/`.
* **Clean Duplicates:** Traverse the workspace and delete root-level `factcheck_*.json` copies, and resolve any name clashes between live and dry-run subdirectories.
* **Registry Reset:** Re-run `scratch/rebuild_registries.py` to compile `stories_registry.js` from ONLY 100% valid files.

## 2. High-Fidelity Offline Regeneration (completed)
Instead of relying on subagents with ad-hoc prompts that hallucinate schemas, we are doing the evaluation programmatically using our own native model capabilities to guarantee 100% schema alignment:
* **Strict Schema Enforcement:** Use the exact keys required by `aletheia_bot.py` and `orchestrator.py` (`claim_u`, `claim_psi`, `real_u`, `real_psi`, `posts` containing exactly 14 elements).
* **Automatic Geodesic Plotting:** Generate corresponding trajectory vector graphs (`[subject_slug]_graph.png`) using the local `matplotlib` script and sync them to `bluesky_bot/` and `_Generated_Content/`.
* **Registry Integration:** Sequentially sync all 16 regenerated files into indices and JS registries to restore the portfolio.

## 3. Verification & Safety Safeguards
* **Validation Script:** Run `scratch/inspect_factchecks.py` to ensure that the file counts and structures are completely healthy.
* **Model Selection Lockdown:** Explicitly acknowledge the shift from Pro (Low) to Flash (Medium) to ensure fast, robust execution.

---
## Morality and Will Audit
* Calculated Coordinate: `(υ=+2.0, ψ=+2.0)` -> Systemic Justice & Productive Value Creation.
* Reasoning: Resolving structural bugs, recovering the integrity of the user's workspace, and restoring public visibility metrics without wasting paid resources.
