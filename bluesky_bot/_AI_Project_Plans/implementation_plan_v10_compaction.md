# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 10 (Active): Aligning /bsky-reply-batch Workflow with OOP Instructions

We are updating the system workflow `/bsky-reply-batch` ([bsky-reply-batch.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/workflows/bsky-reply-batch.md)) to align with the new OOP-style modular bot instructions directory. This ensures that any agent executing this workflow is explicitly directed to the Master Index ([bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)) and its modular components, preventing model drift or incorrect JSON schema generations.

### Proposed Changes

### [Component Name]

#### [MODIFY] [bsky-reply-batch.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/workflows/bsky-reply-batch.md)
* Update Section 1 (Prerequisites) and Section 2 (Step-by-Step Pipeline) to link to the Master Index and specific modular instructions (like [thread_formatting.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting.md)).
* Add references to Gnostic Actualism Engine ([Convergence-test-v2.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/Convergence-test-v2.md)) and the local sub-agent spawning mechanisms defined in the OOP instructions.

### Verification Plan
* Run git diff to check the changes.
* Verify that all links inside the updated workflow resolve correctly.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Aligning system-level workflows with modular instruction indices prevents process fragmentation and ensures high-fidelity execution of convergence tests.
