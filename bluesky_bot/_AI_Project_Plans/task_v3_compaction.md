# Task List: True Directory Separation and Programmatic Indexing

- [x] Clean up duplicates and separate dry-runs vs live stories
  - [x] Copy the 5 dry-run files from `_Generated_Content/stories/` to `bluesky_bot/stories/`
  - [x] Delete duplicate live files from roots of `bluesky_bot/`, `_Generated_Content/`, `bluesky_bot/stories/`, and `_Generated_Content/stories/`
- [x] Rebuild registries and clean index.json files
  - [x] Update `rebuild_registries.py` to delete index files before rebuilding
  - [x] Run `rebuild_registries.py` to recreate clean separate index files
- [x] Update HTML Viewer programmatic indexing
  - [x] Modify `control_panel.html` to load both `stories/index.json` and `stories/live/index.json`
  - [x] Merge and dynamically sort loaded stories in `control_panel.html`
- [x] Verification and validation
  - [x] Verify using local HTTP server that both dry-runs and live runs render perfectly side-by-side
