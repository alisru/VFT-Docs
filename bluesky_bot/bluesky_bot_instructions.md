# Aletheia Bot System - Master Index & Instructions Map

This file serves as the master index, entry point, and directory map for the Aletheia Bot evaluation instructions. All operational, framework, formatting, and sub-agent protocols are split into modular files to conserve token budget and isolate context.

---

## 1. Operating Rules & Constraints

* **NEVER POST LIVE BY DEFAULT**: Always default to a dry run. The publishing script must only send threads live when explicitly run with the `--live` flag after manual portfolio review.
* **Character Caps & Bounds**: Every single step in the JSON posts list must be kept strictly under **250 characters** to guarantee it loads cleanly and prevents dynamic text-splitting errors.
* **No Numbering**: Never prefix any step with `1/`, `2/`, `1/14` or any numerical indices. The thread must read as a seamless, organic story.
* **Clean URLs**: Always strip tracking query parameters (e.g. `?utm_source=...`) from URLs to save character space.

---

## 2. Core Modules & Instructions

Any agent or sub-agent executing tasks in this repository must load the specific file linked below relevant to their task:

### A. Gnostic Actualism Engine
* **Purpose**: Technical details of the 5-Phase Convergence Test, coordinate mappings, plane calculations, and paths.
* **File Link**: [Convergence-test-v2.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/.agent/tools/convergence-test/Convergence-test-v2.md)
* *Note: The final public output translates these highly technical calculations into elegant, conversational Plain English, stripping hyper-technical jargon like "z-profiles," "Helxis," or "R_net."*

### B. Thread Formatting & JSON Schema
* **Purpose**: Details JSON keys schema, conversational formatting rules, the canonical 14 logical steps mapping, and the canonical JSON example.
* **File Link**: [thread_formatting.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/thread_formatting.md)

### C. Operational Processes & Pipelines
* **Purpose**: Division of labor between Finder and Evaluator sub-agents, mathematical batch bounds (5 stories per evaluator), and local execution scripts (`orchestrate_batch_local.py`, `rebuild_registries.py`, `post_batch.py`).
* **File Link**: [operational_pipelines.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/operational_pipelines.md)

### D. Sub-Agent Spawning Prompts
* **Purpose**: Stateless templates and role prompt specifications for spawning `Batch Finder Worker` and `Batch Evaluator Worker` instances.
* **File Link**: [subagent_spawning.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/subagent_spawning.md)

---

## 3. Bluesky Profile Bio & Custom Persona Text
* **Profile Description Wording:**
  "Hegemonic Analyst running 5-Phase Convergence Tests on reality.
  Alethekanon = Uncompromising logic & truth.
  Awwthekanon = Empathy, human cost & healing.
  Brothekanon = Pointing out the sheer absurdity of it all.
  (Truth is a vector, not a list.)"
