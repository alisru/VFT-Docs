# Active Task List: Bluesky Bot Codebase Hardening, Invariants & Optimization

- [/] **Codebase Audit & Vulnerability Diagnosis**:
  - [x] Complete subagent audit of `bluesky_bot` pipeline files.
  - [x] Save comprehensive report to `bluesky_bot/bluesky_bot_audit_report.md`.
- [ ] **Deterministic Trajectory Invariant Enforcement**:
  - [ ] Import `get_path_name` into `google_ai_studio_one_shot.py` and `rebuild_registries_son.py`.
  - [ ] Automatically calculate and overwrite trajectory lines in Post 3 (Verdict) and Post 8 (The Trajectory) based on $(u, \psi)$ deltas.
  - [ ] Add explicit Deterministic Trajectory Invariant text to `instructions/thread_formatting_son.md`.
- [ ] **Prompt Efficiency & Token Optimization**:
  - [ ] Remove duplicate `extra_context` from `system_instruction` in `google_ai_studio_one_shot.py` (keep once in `user_payload`).
  - [ ] Cap candidate text body at 2,500 characters in `harvest_candidates.py` and cluster secondary snippets at 1,200 characters.
  - [ ] Extract Bluesky `created_at` / `indexed_at` timestamps into `pub_date` in `harvest_candidates.py`.
- [ ] **Card Alt-Text & Cascading Post Fixes**:
  - [ ] Fix `aletheia_bot.py` alt-text generation to use persona prefix matching instead of fixed `posts[4..12]` array indices.
  - [ ] Fix `pack_posts` carry-over logic to prevent text fragments bleeding into subsequent steps.
- [ ] **Story Retraction & Correction Pipeline**:
  - [ ] Implement `retract_story.py` CLI to post an errata reply, update story status to `AMENDED`/`RETRACTED`, and re-index registries.
