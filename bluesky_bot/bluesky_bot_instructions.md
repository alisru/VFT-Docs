# Aletheia Bot System - Master Index & Instructions Map

This file is the master index and entry point for the Aletheia Bot. All operational, framework, formatting, and sub-agent protocols are split into modular files to conserve token budget and isolate context.

---

> [!CAUTION]
> ## ⚠️ STOP — Read This Before Opening Any Files
>
> **You are the Parent Agent. You DO NOT need to load the evaluation modules yourself.**
>
> * **DO NOT open** Module A (Convergence Test), Module B (Thread Formatting), or Module C (Operational Pipelines).
> * These are **for sub-agents only**. Loading them into your context will pollute the chat history and waste tokens on every subsequent turn.
> * **Your only job** is to run the harvest script, read Module D to get the sub-agent prompt templates, spawn the workers, wait, then run the registry rebuild script.
> * **Sub-agents** receive Modules A, B, and C inside their isolated prompts. Their context is discarded when they terminate.

---

## 1. Operating Rules & Constraints

* **NEVER POST LIVE BY DEFAULT**: Always default to a dry run. The publishing script must only send threads live when explicitly run with the `--live` flag after manual portfolio review.
* **Character Caps & Bounds**: Every single step in the JSON posts list must be kept strictly under **250 characters** to guarantee it loads cleanly and prevents dynamic text-splitting errors.
* **No Numbering**: Never prefix any step with `1/`, `2/`, `1/14` or any numerical indices. The thread must read as a seamless, organic story.
* **Clean URLs**: Always strip tracking query parameters (e.g. `?utm_source=...`) from URLs to save character space.

---

## 2. Scripts & Utilities Directory (Parent Agent Navigation)

Run these scripts in order. You do not need to open the script files — the descriptions below are sufficient.

* **`scratch/harvest_candidates_script.py`**: Logs into Bluesky, fetches fresh English news posts from verified feeds, de-duplicates against historical stories, and writes up to 25 candidates to `scratch/harvested_candidates.json`. Run this first.
* **`scratch/rebuild_registries.py`**: Clears old registries and recompiles all `factcheck_*.json` files in `bluesky_bot/stories/` into `stories_registry.js` and updates control panel indexes. Run this after sub-agents finish.
* **`bluesky_bot/aletheia_bot.py`**: The core CLI posting engine. Validates character limits, uploads graphs, and posts threads live (`--live`) or dry-run (`--dry-run`). Used for individual story posting, not batch runs.
* **`bluesky_bot/generate_graph.py`**: Matplotlib module called by sub-agents to draw trajectory graphs. Sub-agents call this directly — you do not need to touch it.
* **`bluesky_bot/orchestrate_batch.py`**: **LOCKED. Do not use.** Legacy API wrapper with hardcoded `sys.exit(1)` to prevent external Gemini API token usage.

---

## 3. Module Directory (Sub-Agent Reading Only)

The modules below are **not for the parent agent**. They are listed here so you know what to point sub-agents to in their spawning prompts.

### A. Gnostic Actualism Engine — *Sub-Agents Only*
* **Purpose**: 5-Phase Convergence Test, coordinate mappings, plane calculations, canonical path names.
* **File**: [Convergence-test-v2.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/Convergence-test-v2.md)

### B. Thread Formatting & JSON Schema — *Sub-Agents Only*
* **Purpose**: 13-key JSON schema, 14 logical steps, character rules, canonical example.
* **File**: [thread_formatting.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting.md)

### C. Operational Processes & Pipelines — *Sub-Agents Only*
* **Purpose**: Evaluator step-by-step task execution, graph saving, registry syncing.
* **File**: [operational_pipelines.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/operational_pipelines.md)

### D. Sub-Agent Spawning Prompts — *Parent Agent Reads This*
* **Purpose**: Prompt templates for spawning `Batch Finder Worker` and `Batch Evaluator Worker` instances. **This is the only module the parent needs to open.**
* **File**: [subagent_spawning.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/subagent_spawning.md)

---

## 4. Bluesky Profile Bio & Custom Persona Text

* **Profile Description Wording:**
  "Hegemonic Analyst running 5-Phase Convergence Tests on reality.
  Alethekanon = Uncompromising logic & truth.
  Awwthekanon = Empathy, human cost & healing.
  Brothekanon = Pointing out the sheer absurdity of it all.
  (Truth is a vector, not a list.)"