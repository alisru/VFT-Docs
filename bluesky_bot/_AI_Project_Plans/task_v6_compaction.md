# Active Task List: Automated Reply Harvesting & Batch Evaluation Workflow

- [x] Workflow Registration
  - [x] Create [.agent/workflows/bsky-reply-batch.md](file:///e:/Vector%20Field%20Theory%20VFT%20Docs/.agent/workflows/bsky-reply-batch.md) to register the `/bsky-reply-batch` slash command
- [x] Candidate Harvesting & Expansion
  - [x] Modify `scratch/harvest_candidates_script.py` to increase harvest limit
  - [x] Rerun `harvest_candidates_script.py` to fetch initial verified news posts (harvested 16 posts)
  - [x] Create and run `scratch/harvest_more.py` to search standard keywords and top up the harvested candidates to exactly 20
- [x] Permanent API Block Implementation
  - [x] Modify `get_llm_client()` inside `bluesky_bot/orchestrator.py` to raise a fatal error and prevent background API calls permanently
  - [x] Modify `get_llm_client()` inside `bluesky_bot/orchestrate_batch.py` to raise a fatal error and prevent background API calls permanently
  - [x] Add clear developer warnings inside the scripts indicating that all evaluations must remain strictly offline (Bot 2 mode)
- [x] Programmatic Batch Evaluations (100% Offline)
  - [x] Perform native convergence evaluations for the first 5 stories and compile them using `write_batch_jsons.py`
  - [x] Perform native convergence evaluations for the remaining 15 stories and compile them using `write_batch_2_jsons.py`
  - [x] Programmatically draw all 20 trajectory vector graphs using local `matplotlib` scripts and save them inside `graph_png/` subfolders (0 API calls)
- [x] Registry Rebuild & Viewer Sync
  - [x] Run `scratch/rebuild_registries.py` inside `.venv` to cleanly compile separate indices and sync the JavaScript registry bundle
  - [x] Verify that all 20 new dry runs render beautifully in the HTML Portfolio control panel without warnings or console exceptions
