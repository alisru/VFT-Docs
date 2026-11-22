# AITA Reddit Scraper & VFT Verdict Engine (Side Mode) — Plan (2026-11-18)

Tracked in Semantic Gluon under `PRJ-BSKY-BOT` (`DES-033`, `ANTI-031`).

See artifact `implementation_plan.md` for full technical design:
- Isolated `bluesky_bot/aita_evaluator.py` (Reddit `.json` scraper for `r/AmItheAsshole` & `r/AITAH`, VFT `(υ, ψ)` + 0.5-Zone inversion + 7-Plane Q1–Q7 + cognitive/fallacy checks, deterministic 7-verdict mapping `YTA/YWBTA/NTA/YWNBTA/ESH/NAH/INFO`, and actionable `(+, +)` resolution).
- Output strictly isolated to `bluesky_bot/aita/` (never `stories/` or `stories_registry.js`).
- `AletheiaLauncher.pyw` button + controls sharing the active Thinking Level, Timeout (s), and Model Fallback Queue.
- Unit tests in `bluesky_bot/tests/test_aita_verdict_mapping.py`.
