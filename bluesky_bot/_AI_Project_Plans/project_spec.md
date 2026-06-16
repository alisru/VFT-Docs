# Aletheia Bot - Project Specification

This document is the unified project specification and single source of truth for the Aletheia Bot project. It defines the bot's system architecture, folder structures, thread formats, trajectory paths, and core rules. 

---

## 1. System Directory & Files

All project files are organized in the following locations within the workspace:

```
bluesky_bot/
├── stories/                    # Fact-check story JSON configs
│   └── live/                   # JSON configs of posted stories
├── graph_png/                  # Story trajectory graphs (PNG)
├── scripts/                    # Maintenance & administrative scripts
│   ├── gen_story_graphs.py     # Generates graphs for draft stories
│   ├── check_filenames.py
│   └── ...
├── tests/                      # Testing & validation scripts
│   ├── test_slew.py            # Generates 32 test case graphs
│   ├── test_counts.py
│   └── ...
├── instructions/               # Modular bot instructions
│   ├── thread_formatting.md
│   ├── operational_pipelines.md
│   └── subagent_spawning.md
├── _AI_Project_Plans/          # Plans, audits, specs, and logs
│   ├── project_spec.md         # This specification
│   ├── implementation_plan.md  # Historic plans log
│   └── walkthrough.md          # Completed task summaries
├── aletheia_bot.py             # Core CLI posting engine
├── rebuild_registries.py       # Registry compiler (stories_registry.js)
└── generate_graph.py           # Matplotlib graph drawing utility
```

---

## 2. Convergence Test Lite (Gnostic Actualism)

Every news story is evaluated using the streamlined **Convergence Test Lite** guidelines defined in `.agent/tools/convergence-test/convergence_lite.md`.

### Default Evidence Standards (Step 1 Hook)
Every story must explicitly list the three evidence elements in Post 1 (Hook) formatted as:
`Evidence: [A in 2-5 words], [B in 2-5 words], [C in 2-5 words]`

*   **[A] Stated Ideal**: What the actor claims to stand for (their stated claim).
*   **[B] Actions within Context**: The observable, physical impact on the ground (what actually happened).
*   **[C] Objective Ideal**: What a structurally coherent version of the stated goal would physically require.

*Constraint*: Every evidence line item must be strictly **2 to 5 words** and describe concrete, physical events (no academic abstractions or jargon).

---

## 3. Trajectory Paths & Graphing

Graphs are plotted on the 2D **Psochic Hegemony Grid** spanning Morality ($u$, horizontal axis) and Will ($\psi$, vertical axis).

### Zone Anchors
*   **Greater Good (+1, +1)** (Top-Left)
*   **Greatest Lie (-1, +1)** (Top-Right)
*   **Lesser Good (+1, -1)** (Bottom-Left)
*   **Greater Evil (-1, -1)** (Bottom-Right)

### Compositional Path Names
Paths are calculated compositionally from the exit name of the stated/claim zone (origin) and the entry name of the actual/real zone (destination), formatted as:
`[Exit Name] into [Entry Name]`

If origin zone == destination zone, the trajectory is **Stasis**.

#### Entry Names (Destination Zone)
*   Greater Good $\to$ **Grace**
*   Greatest Lie $\to$ **Deception**
*   Lesser Good $\to$ **Redemption**
*   Greater Evil $\to$ **Destruction**

#### Exit Names (Origin Zone)
*   Greater Good $\to$ **Fall**
*   Greatest Lie $\to$ **Revelation**
*   Lesser Good $\to$ **Awakening**
*   Greater Evil $\to$ **Reckoning**

#### Examples:
*   Greater Good $\to$ Greater Evil = **"Fall into Destruction"**
*   Greatest Lie $\to$ Greater Good = **"Revelation into Grace"**
*   Greater Evil $\to$ Lesser Good = **"Reckoning into Redemption"**
*   Lesser Good $\to$ Greatest Lie = **"Awakening into Deception"**

---

## 4. Thread & Post Architecture

Stories are stored as JSON files containing a `"posts"` array of **exactly 14 steps** in this logical sequence:

1.  **Hook (Post 1)**: Human-style punchy scene-setter + Subject Title + External Source Link + Evidence Line. *(Note: Must NOT contain robotic prefixes like "Subject:").*
2.  **Claim (Post 2)**: Stated claim and its stated coordinates zone anchor.
3.  **Reality (Post 3)**: Ground-level observed reality and its actual coordinates zone anchor.
4.  **Verdict (Post 4)**: PASS/FAIL verdict + Canonical path name + plain English explanation.
5.  **Context (Post 5)**: Broader contextual details of the event.
6.  **Nuance (Post 6)**: The "poison" (flaw) of a good story, or the "bright side" (hope) of a bad story.
7.  **Breakdown (Post 7)**: Structural explanation of where the logic or process broke down.
8.  **Switch (Post 8)**: Identification of the bait/switch (who actually benefited).
9.  **Trajectory (Post 9)**: The path name + narrative description of the vector.
10. **Destination (Post 10)**: The ultimate systemic outcome if the trajectory continues.
11. **Unavoidables (Post 11)**: The core unavoidable truth vs. the core unavoidable lie of the event.
12. **Trinary Persona Reaction (Post 12)**: Combined reactions from Alethekanon, Awwthekanon, and Brothekanon.
13. **Aletheia Synthesis (Post 13)**: The synthesis of the three perspectives into a unified worldview.
14. **Resolution Vector (Post 14)**: The final constructive action needed to resolve the strain.

### Post Length Constraints
*   Every post in the JSON array must be strictly under **290 characters** (well within Bluesky's 300 hard limit) to prevent validation errors and dynamic text-splitting.

---

## 5. Execution Flow

1.  **Harvest Candidates**: Run `python harvest_candidates.py` to scrape news and output candidates to `bluesky_bot/harvested_candidates.json`.
2.  **Evaluate Stories**: Run evaluations using modular guidelines and prompts. Write individual `factcheck_[id].json` configurations directly to `bluesky_bot/stories/`.
3.  **Generate Graphs**: Run `python scripts/gen_story_graphs.py` to draw the trajectories for draft stories and save them directly in `_AI files and chat logs/test_runs/`.
4.  **Compile Registry**: Run `python rebuild_registries.py` to compile `stories_registry.js` and update control panel files.
5.  **Post Threads**: Run `python aletheia_bot.py` or `python post_batch.py` (dry-run by default; `--live` for live Bluesky posting).
