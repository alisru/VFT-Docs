# Active Task List: Strict Curated Actor Extraction and Backfill

- [x] Analyze the corpus proper nouns and filenames to build an expanded, comprehensive map of political actors, individuals, and nations.
- [x] Rewrite `actor_extract.py` to prioritize strict dictionary matching using `ACTOR_MAP` and completely remove the heuristic fallback (preventing garbage entities).
- [x] Create and run the backfill script `scratch/backfill_curated_actors.py` to re-tag all 1,565 story JSONs on disk, clearing out the old heuristic-generated trash.
- [x] Rebuild the registries using `python rebuild_registries.py` to compile the cleaned actors list into `stories_registry.js`.
- [x] Verify that the control panel's Actor/Entity sidebar is fully updated and free of garbage.
