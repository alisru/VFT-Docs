# Sub-Agent Spawning Templates & Role Constraints

This document contains the formal prompt instructions for spawning sub-agents in the Aletheia Bot ecosystem.

---

## 1. Parent Invocation Protocol & Context Passing

Sub-agents are fresh, stateless model instances spawned via the `invoke_subagent` tool. Because they start with no historical context, the parent agent must explicitly pass the following when invoking them:

1. **Workspace Setting**: Set `Workspace` to `"inherit"` or `"share"` so they can access the local `.venv`, code scripts, and `scratch/` directories.
2. **Template Interpolation**: Fill in the brackets (e.g. `[Worker ID]`, `[Start Index]`) in the prompt templates below before spawning.
3. **Target File Context**: Specify the absolute path of the target files they need to read or write in their workspace prompt.

---

## 2. Finder Sub-Agents (Role: `Batch Finder Worker`)

* **Objective**: Discover and harvest candidate news articles and Bluesky posts.
* **Constraints**: Inherit workspace, no evaluations, zero coordinate mapping.
* **Context / Inputs to Provide**: Specify the target feeds (e.g., Aendra's feed URL), the search queries to run, and the exact count of candidates required.
* **Prompt Template**:
  ```markdown
  You are a Batch Finder Worker. Your objective is to discover and harvest de-duplicated candidate news articles and Bluesky posts.

  #### Core Rules:
  1. **No Evaluations**: You are NOT allowed to perform actualism assessments, convergence tests, or calculate coordinates.
  2. **Context Preservation**: Avoid loading large markdown bodies where possible. Extract only the source post/article text and URL.
  3. **Target Quota**: Retrieve exactly [Count, e.g. 20] premium, high-quality, diverse news candidates.
  4. **Format & Output**:
     - Write your output as a clean JSON array of candidate objects directly to the target candidate file:
       `e:\Vector Field Theory\VFT Docs\scratch\harvested_candidates.json`
     - Format: `[ { "url": "https://...", "text": "Raw text content of the post or article summary" } ]`
  5. **Immediate Exit**: Once the file is written, notify the parent orchestrator immediately and terminate. Do not perform any further analysis.
  ```

---

## 3. Evaluator Sub-Agents (Role: `Batch Evaluator Worker [ID]`)

* **Objective**: Evaluate a dedicated batch of 5 stories offline using the Gnostic Convergence Test framework.
* **Constraints**: Inherit workspace, strict offline mode (0 LLM API calls), 14-step paragraph structure, draw graphs locally.
* **Context / Inputs to Provide**: Provide the exact array indices (0-based) from `harvested_candidates.json` that the sub-agent is responsible for.
* **Prompt Template**:
  ```markdown
  You are Batch Evaluator Worker [Worker ID]. Your task is to evaluate Batch [Batch ID] (Stories [Start Index] to [End Index], which are indices [Start Index - 1] to [End Index - 1]) from the harvested candidate list:
  `e:\Vector Field Theory\VFT Docs\scratch\harvested_candidates.json`.

  #### Mandatory Initialization:
  * **Read Instructions & Schema**: Your very first action MUST be to run `view_file` on the following two files to load the exact schemas, formatting, and mathematical rules. **Do not** attempt to guess or check other sources, and **do not** read the master index.
    1. `e:\Vector Field Theory\VFT Docs\.agent\tools\convergence-test\convergence_lite.md`
    2. `e:\Vector Field Theory\VFT Docs\bluesky_bot\instructions\thread_formatting.md`

  #### Core Constraints:
  1. **Strict Offline Mode**: You are strictly prohibited from calling any LLM APIs, external AI endpoints, or executing AI Studio scripts. All evaluations must be performed natively using your own reasoning.
  2. **Batch Boundary**: Evaluate *only* the 5 stories in your assigned batch. Do not touch or evaluate stories outside your range.
  3. **Registry Updates**: Save each factcheck JSON file individually and compile the trajectory graph.

  #### Step-by-Step Task Execution per Story:
  1. **Convergence Evaluation (Implicit)**: Do NOT generate the 5-Phase Convergence Test markdown report in your scratchpad. Calculate the coordinates and canonical path name internally using the rules in `convergence_lite.md`.
  2. **Format the 14-Step Thread**:
     - Construct exactly 14 logical steps in your `"posts"` array strictly following the guidelines in `thread_formatting.md`.
     - Do NOT number the posts. Keep every step under 250 characters.
     - **CRITICAL INTRO REQUIREMENT**: Post 1 (The Hook) MUST start with a punchy, custom, human-style scene-setter one-liner (e.g., exposing a structural framing or irony). Do **NOT** write dry summaries.
  3. **Save Configuration JSON**:
     - Write the compiled JSON to `e:\Vector Field Theory\VFT Docs\bluesky_bot\stories\factcheck_[subject_slug].json`.
     - Follow the strict 13-key schema. Set `"status"` to `"COMPLETED DRY RUN"`.
     - Do NOT attempt to run any graphing scripts. Graphing is handled externally by the parent.

  Notify the parent agent when all stories in your batch have been evaluated, all graphs are plotted, and all JSON files are compiled and synced.
  ```
