# Trinary Synthesis Loop Workflow

This workflow guides the Aletheia Bot through a peer-reviewed, multi-perspective resolution loop utilizing Alethekanon, Awwthekanon, and Brothekanon. It runs sequentially during single-run cron tasks to create robust, fact-checked systemic suggestions.

---

## The 3-Phase Pipeline Architecture

```
                     [ NEWS STORY / CLAIM ]
                               │
                               ▼
               ┌───────────────────────────────┐
               │    Phase 1: Raw Baseline      │
               │ (Initial Coordinate Judgement) │
               └───────────────┬───────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
  │ [Awwthekanon]│      │[Brothekanon] │      │[Alethekanon] │
  │Ideates Ideal │      │Finds Easiest │      │Researches    │
  │Solution.     │      │Shortcut.     │      │Proven Past   │
  │              │      │              │      │Solutions.    │
  │  Fact-checks,│      │  Fact-checks,│      │  Fact-checks,│
  │  cites, and  │      │  cites, and  │      │  cites, and  │
  │  finds URL.  │      │  finds URL.  │      │  finds URL.  │
  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │ (Collects Responses)
                               ▼
               ┌───────────────────────────────┐
               │     Phase 3: The Audit        │
               │ Alethekanon reviews Bro & Aww │
               │ against its own findings,     │
               │ adjusts final coordinates.    │
               └───────────────┬───────────────┘
                               │
                               ▼
               ┌───────────────────────────────┐
               │    Synthesized Final Post     │
               │  (Appends audited suggestion  │
               │   section to the thread)      │
               └───────────────────────────────┘
```

---

## Mapped Clustered Thread Sequence (Dynamic & Sequence-Driven)

To maintain both character identity and structured resolutions, the thread is compiled into a dynamic, sequence-driven chain of posts rather than a rigid, fixed limit. The sequential flow strictly follows this order:

1. **The Original Baseline Process (Baseline Posts):** Establishes the hook, baseline coordinates, trajectory, verdict, and the breakdown critique (this matches the standard Convergence Test process).
2. **Alethekanon Cluster (Thoughts ──► Blended Resolution):**
   * **First Post:** Systemic commentary on the structural boundaries of the breakdown.
   * **Second Post (Blended Resolution):** Seamless narrative transition citing the historical policy/regulatory solution + source URL.
3. **Awwthekanon Cluster (Thoughts ──► Blended Resolution):**
   * **First Post:** Empathetic commentary on the human/community toll of the breakdown.
   * **Second Post (Blended Resolution):** Seamless narrative transition citing the care-focused ideal solution + source URL.
4. **Brothekanon Cluster (Thoughts ──► Blended Resolution):**
   * **First Post:** Pragmatic/humorous commentary on the physical absurdity of the breakdown.
   * **Second Post (Blended Resolution):** Seamless narrative transition citing the low-tech shortcut solution + source URL.
5. **The Master Synthesis Audit (Conclusion Post):** The Master Auditor (Aletheia) performs the final audit pass, compiles the Blended Path, and outputs the recalculated final coordinates.

*(Note: If dynamic text splitting occurs due to character limits, the post count expands dynamically, but the logical sequence of thoughts preceding their matching resolutions remains strictly preserved).*


---

## Phase 1: Raw Baseline
* **Goal:** Establish the baseline Convergence Test coordinates mapping the Claim vs Reality.
* **Input:** Target News Post text and URL.
* **Output:** Initial coordinates $(\upsilon_{base}, \psi_{base})$ and the canonical trajectory (Grace, Fall, Redemption, Deception).

---

## Phase 2: Concurrent Peer Exploration
Three distinct cognitive lenses execute concurrent evaluations of the baseline failure. Each persona **must fact-check, cite, and provide a real URL example** to support their resolution vector.

### 1. Awwthekanon (The Idealistic Empath)
* **Objective:** Ideate the absolute ethical and empathic north-star solution—what the system looks like when human care is completely unconstrained by corporate or systemic extraction.
* **Requirements:**
  * Fact-check current humanitarian or mutual-aid approaches.
  * Cite a real-world, highly functioning example of this ideal in action.
  * Provide a valid URL to the example.

### 2. Brothekanon (The Pragmatic Shortcut)
* **Objective:** Find the easiest, lowest-friction, and most practical physical shortcut to approximate Aww's ideal solution immediately, bypassing bureaucracy.
* **Requirements:**
  * Fact-check low-cost, decentralized, or open-source solutions.
  * Cite a real-world hack or shortcut that worked elsewhere.
  * Provide a valid URL to the example.

### 3. Alethekanon (The Systemic Auditor)
* **Objective:** Research historically proven, structured institutional or regulatory solutions that have successfully solved this structural failure before.
* **Requirements:**
  * Fact-check historical policy, engineering, or legal precedents.
  * Cite a documented historical solution.
  * Provide a valid URL to the proof.

---

## Phase 3: The Synthesis Audit
Alethekanon runs a final validation pass using the collected peer outputs from Phase 2.

### 1. Evaluation & Friction Check
Alethekanon reviews Awwthekanon's Ideal and Brothekanon's Shortcut against its own historical findings:
* Detects hidden systemic friction, cost externalization, or structural loopholes in their proposals.
* Adjusts the final coordinates $(\upsilon_{final}, \psi_{final})$ to reflect the realistic systemic potential of these blended solutions.

### 2. The Suggestion Section Draft
Alethekanon compiles the final, action-oriented Suggestion Appendix to conclude the thread:
* **The Blended Path:** A synthesized recommendation combining Aww's target, Bro's ease, and Aletheia's structural guardrails.
* **Verification URL:** The cited proof link that validates this path is empirically achievable.

---

## Programmatic Cron & Agentic Spawning Flow

For automated execution (e.g. running as a GitHub Action, local cron, or automated agentic workflow), the bot utilizes the **Agentic Spawning Protocol** to run Phase 2 concurrently without context bleed.

### 🤖 The Spawning Protocol
1. **Orchestrator Wakes Up:** The orchestrator fetches target posts using `search_bsky.py`.
2. **Phase 1 Baseline:** The orchestrator runs a fast LLM pass to establish the raw Convergence Test baseline.
3. **Phase 2 Subagent Spawning:** The orchestrator concurrently spins off three isolated specialized subagents:
   * **`Awwthekanon-Subagent`**: Spinned off with instructions to ideate the empathic ideal solution, find a real-world example, fact-check it, and return a cited URL.
   * **`Brothekanon-Subagent`**: Spinned off with instructions to identify the lowest-friction practical shortcut, find a real-world hack/shortcut, fact-check it, and return a cited URL.
   * **`Alethekanon-Subagent`**: Spinned off with instructions to research historically proven structural/regulatory solutions, fact-check them, and return a cited URL.
4. **Synchronization:** The orchestrator pauses and waits for the three subagents to complete their concurrent investigations.
5. **Phase 3 Synthesized Audit:** The orchestrator consumes the three clean subagent payloads, runs Alethekanon to audit them for systemic friction, recalculates the final coordinates, and compiles the suggestion appendix.
6. **Publish:** The orchestrator generates the graph and posts the entire thread live.

---

## Cron Execution Schedule
When deployed as a cron job, the automated pipeline follows this scheduled execution:
* **Trigger:** Run every 12 hours (or on a custom intervals schedule).
* **Keywords Filter:** Search custom verified feeds (e.g., `@aendra.com/feed/verified-news`) for top news stories containing target keywords (e.g., `US`, `Energy`, `Climate`).
* **Rate Limits:** Cap at maximum 1 complete synthesized thread analysis per execution window to ensure high-quality, manual-grade output.

