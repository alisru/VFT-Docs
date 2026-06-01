# Active Task List: Graph PNG Consolidation & Syncing

- [x] Graph PNG Consolidation & Relocation
  - [x] Create directory `graph_png/` inside `bluesky_bot/` and `_Generated_Content/`
  - [x] Relocate all loose `*_graph.png` files to their respective subfolders
  - [x] Clean loose duplicates to ensure 100% directory hygiene
- [x] System Directives Patches
  - [x] Update `aletheia_bot.py` to draw and copy new graphs to `graph_png/` subfolders programmatically
  - [x] Update `orchestrate_batch.py` to save batch synthesized graphs inside `graph_png/` folders
  - [x] Update `bluesky_bot_instructions.md` to document `graph_png/` subdirectory structures
- [x] Frontend Viewer Integration
  - [x] Patch `control_panel.html` in both locations to automatically check and prepend `graph_png/` prefix to `graph_img` properties
  - [x] Rebuild registries by running `rebuild_registries.py` inside `.venv`
- [x] Verification & Validation
  - [x] Verify that background task `task-3113` compiled registries with updated prefixes successfully
  - [x] Double check that no broken images or warnings exist in the HTML Viewer control panel
