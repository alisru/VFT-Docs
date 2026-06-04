# Cumulative Project Implementation Plans Log

This document maintains the historical and active implementation plans for the Aletheia Bot project to prevent information loss across context compactions.

---

## Plan 11 (Active): Scripts & Utilities Index in Master Instructions

To reduce token usage and prevent agents from loading large python script files just to understand pipeline flow, we are adding a "Scripts & Utilities Directory" to the Master Index ([bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)). This section will provide a high-level summary of the files in `bluesky_bot/` and `scratch/` that handle harvesting, evaluation, registries, and posting.

### User Review Required
> [!NOTE]
> This change is documentation-only, adding metadata to the master index to prevent context-bloat for subsequent AI turns. No operational scripts are altered.

### Proposed Changes

### [Documentation Component]

#### [MODIFY] [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md)
* Prepend or append a new section: `## 4. Scripts & Utilities Directory` outlining:
  * `scratch/harvest_candidates_script.py` (candidate retrieval & de-duplication)
  * `bluesky_bot/orchestrate_batch.py` (Gemini API pipeline wrapper — legacy/locked)
  * `bluesky_bot/aletheia_bot.py` (the core posting CLI engine)
  * `scratch/rebuild_registries.py` (registry compiler & visual control panel indexer)
  * `bluesky_bot/generate_graph.py` (the Matplotlib trajectory graph plotter)

#### [MODIFY] [running_dialogue.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/running_dialogue.md)
* Document Intent 24 in the intentions log tracking this token optimization update.

### Verification Plan
* Verify that all links in the modified [bluesky_bot_instructions.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/bluesky_bot_instructions.md) resolve correctly.
* Run git diff to confirm only clean, expected markdown modifications have occurred.

### Moral Axis Audit
* Calculated Coordinate: `(υ=+1.0, ψ=+1.5)` -> Greater Good & Productive Action.
* Verdict: Providing a script registry in the instructions prevents incoming agents from having to open the code files, drastically reducing token consumption and processing time.
