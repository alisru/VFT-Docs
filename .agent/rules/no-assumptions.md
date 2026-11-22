---
trigger: always_on
glob:
description: Mandatory Codebase Hygiene, Exhaustive Context Discovery, Zero Assumptions, and Anti-Littering Protocol.
---

# MANDATORY CODEBASE HYGIENE, EXHAUSTIVE CONTEXT DISCOVERY & ZERO ASSUMPTIONS

## 1. Absolute Ban on Wild Assumptions & Lazy Guesses
- You are strictly prohibited from making wild guesses, assumptions, or improvisations about:
  - How any script, module, or pipeline operates.
  - What keys, fields, or schemas an object contains.
  - What data is "safe" to drop, truncate, or fall back to.
  - What directory structure or naming convention to use.
- **The Golden Rule**: If you do not know something with 100% certainty from verified evidence, you **MUST STOP**.
  1. Inspect the authoritative files and real records on disk.
  2. Search and read the project's documentation, instructions, and schemas.
  3. **ASK the user directly** if ambiguity remains. Never invent an answer to move fast.

## 2. Read First, Act Second (Mandatory Context Familiarization)
- Never start writing code or transforming data based on surface impressions or function parameter names.
- Before touching any project subsystem:
  - Read the project's instruction files (e.g., `README.md`, `*_instructions.md`, `SKILL.md`).
  - Trace the end-to-end pipeline: where data comes from, what depends on it, and what will break if a field is omitted or altered.
  - Print and inspect an actual, complete, populated record on disk to see what the ground truth looks like.

## 3. Zero Scattered Litter (Workspace Hygiene)
- **Never litter the workspace**:
  - Do NOT create ad-hoc directories (e.g., `drafts/`, `backup_drafts/`, `requeued_to_harvest/`, `temp/`, `scratch/`).
  - Adhere strictly to the established, canonical project folder structure.
  - If a temporary script is required to perform a data migration or fix, execute it and **clean it up immediately**. Never leave orphaned scripts or junk files behind.

## 4. Root-Level Engineering (Make It Actually Work)
- Never deliver half-assed, lossy patches, hollow placeholders, or superficial transformations.
- Understand the root cause completely before writing the solution.
- Verify the solution end-to-end against real data, ensuring zero payload loss, zero schema degradation, and full compatibility with all upstream and downstream consumers.
