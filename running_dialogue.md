# Project Scope: Bluesky Judgement Bot

This document serves as an external memory tracker. It records the project scope, past achievements, current intentions, and specific user requirements. **Always consult this file upon waking from a context wipe.**

## Core Objective
Create a bot that pulls current news stories, judges them using the 5-Phase Convergence Test (Actualism Framework), plots the results on the Psochic Hegemony grid, and posts the results as a conversational, threaded post on Bluesky.

## Past Achievements
- Successfully built `generate_graph.py` to plot dual coordinates (Claim vs Reality) with dashed trajectory lines and canonical geodesic labels (Grace, Fall, Redemption, Deception).
- Configured secure posting via `atproto` using environment variables (`os.environ.get('BSKY_PASSWORD')`).
- Implemented dynamic text chunking to keep posts under Bluesky's 300-char limit while preserving thread flow.
- Successfully posted threaded assessments of NASA rocket delays and US/Iran diplomacy.
- Transitioned the bot's public output from hyper-technical jargon (Q1q5c4, z-profiles) to conversational **Plain English**.

## Formatting Rules & Constraints
1. **Plain English**: Public output must explain structural findings without jargon. (e.g., call a Plane Error a "bait-and-switch" or "saying it's about logic, but actually about will").
2. **Dynamic Splitting**: Use `split_text()` to ensure no post exceeds 300 chars.
3. **Evidence Standards**: The output MUST explicitly state the evidence standards used for the test.
4. **Dual Judgements**: The output MUST explicitly state both the "Stated Claim's Judgement" (coordinates + label) and the "Resulting Judgement" (coordinates + label).
5. **Nuance (Bright Side / Poison)**:
    - For negative/bad stories: Actively look for and state a "bright side" or something good within the story.
    - For positive/good stories: Actively look for and state the "poison" or flaw within the story.
6. **Coordinate Labels Update**:
    - `+1,0` MUST be identified as **'Good Preference'**.
    - `-1,0` MUST be identified as **'Bad Preference'**.

## Intention Log

### [2024-05-29] Intent 1: Initial Dry Run
*Status: Completed*
Ran a dry run on an LA Times article about dog attacks on postal workers using the Plain English format.

### [2024-05-29] Intent 2: Implement Nuance and Format Updates
*Status: Completed*
- Added `running_dialogue.md` (this file).
- Updated the public template (`bluesky_bot_instructions.md`) and scripts to mandate Nuance (bright side/poison), explicit Evidence Standards, explicit Stated vs Actual judgements, and the updated coordinate labels (`+1,0` = Good Preference, `-1,0` = Bad Preference).
- Excluded sensitive chat logs (`Log for review/`) containing plaintext passwords from git history to ensure repository security.

### [2024-05-29] Intent 3: Trinary Perspective & Graph Polishing
*Status: In Progress (Current Task)*
- **Thread Reordering:** Move "The Claim" and "The Reality" (along with their explicit judgements) to immediately follow the Hook, placing them before "The Verdict" and "What's happening".
- **Trinary Perspective:** Append a final "Post 11+" structure to the thread that provides a brief, one-paragraph assessment from three distinct Alethekanon personas derived from the Core Directive: Alethekanon (Logical Analyst), Awwthekanon (Empathetic Healer), and Brothekanon (Creative Observer).
- **Graph Updates:** Ensure `Good Preference (+1.0, 0.0)` and `Bad Preference (-1.0, 0.0)` have explicit text labels drawn onto the `generate_graph.py` output. Move the "Stated Claim" and "Actual Reality" text labels into a proper map legend to reduce graph clutter.

---
*Note to Self: Always append new intentions at the bottom of the log. When receiving new instructions, read them carefully and add them to the Intent Log before executing.*