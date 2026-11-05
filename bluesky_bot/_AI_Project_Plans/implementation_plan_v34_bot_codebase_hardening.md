# Plan 34: Bluesky Bot Codebase Hardening, Invariant Enforcement & Token Optimization

## Goal
Address the findings of the comprehensive codebase audit to resolve prompt token bloat, eliminate deterministic trajectory hallucinations, guarantee multi-source objectivity, and implement the story correction/retraction pipeline.

## 1. High-Priority Invariant & Bug Fixes
- **Programmatic Trajectory Enforcement**:
  - Integrate `get_path_name(claim_u, claim_psi, real_u, real_psi)` from `generate_graph.py` directly into `google_ai_studio_one_shot.py` (`transpose_flat_to_json`) and `rebuild_registries_son.py`.
  - Overwrite/validate the trajectory name in `posts[3]` (The Verdict) and `posts[8]` (The Trajectory) so that no prompt hallucination can violate the deterministic invariant (e.g. $(+,+) \to (-,-)$ can never be labeled "Redemption").
  - Synchronize `thread_formatting_son.md` to include the explicit Deterministic Path Invariant rule present in `potential.md`.
- **Card Alt-Text & Persona Alignment**:
  - Update `aletheia_bot.py` so image alt-text is extracted dynamically via prefix matching rather than fixed indices (`posts[4]`, etc.), fixing misalignment when `use_multi_aspect` adds post 4 and ensuring Spirithekanon is included.
- **Prevent Cascading Bleed in `pack_posts`**:
  - Refactor `pack_posts` in `aletheia_bot.py` to prevent fragments from spilling over into subsequent logical posts.

## 2. Token Optimization & Ingestion Fixes
- **De-duplicate Grounding Dossier**:
  - Remove duplicate injection of `extra_context` from `system_instruction` in `google_ai_studio_one_shot.py`, keeping it only once in `user_payload`.
- **Cap Scraped Article Payload**:
  - Limit candidate text to 2,500 characters in `harvest_candidates.py` and secondary cluster sources to 1,200 characters to prevent 50k-character raw dumps.
- **Extract Bluesky Publication Timestamps**:
  - Parse `record.created_at` or `indexed_at` in `harvest_candidates.py` for Bluesky posts and store as ISO `pub_date` so the LLM has temporal context.

## 3. Retraction & Correction Pipeline
- **Generalized Story Correction CLI**:
  - Create `retract_story.py` to enable formal thread corrections/retractions:
    - Post an errata reply directly under the target root post on Bluesky.
    - Update story state to `AMENDED` / `RETRACTED` in `stories/` and `stories_registry.js`.
    - Adjust historical hypocrisy scores.
