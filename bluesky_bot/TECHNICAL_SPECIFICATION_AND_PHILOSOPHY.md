# Aletheia Bot — Technical Specification, Architecture & Philosophy

## 1. Executive Summary & Core Philosophy

**Aletheia Bot** is an autonomous intelligence, judgment, and fact-checking engine built upon the mathematical principles of **Vector Field Theory (VFT)** and **Psochic Hegemony**. Rather than reducing truth to binary fact-claims or arbitrary political opinions, Aletheia models public statements, political maneuvers, media narratives, and historical events as trajectories through a continuous 2-dimensional vector space: **Morality ($\upsilon$)** and **Will ($\psi$)**.

> *"Truth is a vector, not a list."*

---

## 2. Theoretical Foundations: The $(\upsilon, \psi)$ Moral Vector Space

```
                     +2.0 (Systemic Justice)
                               │  [The Path of Grace]
                               │  (+, +)
                               │  Greater Good
           PASS                │
  ─────────────────────────────┼─────────────────────────────
  -2.0                         │                         +2.0
  (Destruction / Chaos)        │        (Kinetic Creation / Action)
           FAIL                │
                               │  (-, +)
                               │  Greatest Lie / Deception
                               │
                     -2.0 (Pure Extraction)
```

### Axis $\upsilon$ (Morality) — *Who does this benefit?*
- **$+2.0$ (Systemic Justice)**: Universal benefit, structural institutional reform, and generational public goods.
- **$+1.0$ (Greater Good)**: External groups, vulnerable populations, and constructive community welfare.
- **$0.0$ (Neutral)**: Passive or non-substantive administrative actions.
- **$-1.0$ (Lesser Evil / Tribal Extraction)**: Benefits in-group, donors, or factional interests at public expense.
- **$-2.0$ (Pure Extraction / Tyranny)**: Purely self-serving, oligarchic, or predatory rent-seeking.

### Axis $\psi$ (Will / Kinetic Energy) — *What is the energy doing?*
- **$+2.0$ (Productive Justice)**: Actively building systemic value, infrastructure, and enduring institutions.
- **$+1.0$ (Proactive)**: Constructive, tangible, and creative action.
- **$0.0$ (Stasis / Neutral)**: Frictionless inaction or empty rhetoric.
- **$-1.0$ (Passive Harm)**: Deliberate withholding, deregulation of protections, or systemic neglect.
- **$-2.0$ (Active Chaos / Collapse)**: Active destruction, predatory asset-stripping, or disinformation warfare.

### Canonical Trajectory Geodesics
- **Path of Grace $(+\rightarrow+)$**: Stated intent matches constructive empirical outcome.
- **Path of Deception $(+\rightarrow-)$**: Noble stated intent masks extractive or destructive reality (The Greatest Lie).
- **Path of Redemption $(-\rightarrow+)$**: Acknowledged past failing redeemed by proactive structural remedy.
- **Path of Fall $(-\rightarrow-)$**: Explicit cruelty or predatory intent executed without disguise.
- **Path of Compromise**: Incremental negotiation or mixed systemic tradeoffs.

---

## 3. The Tri-Kanon Perspective Synthesis

Every evaluated story and public thread concludes with three complementary perspective lenses:

```
                  ┌───────────────────────────────┐
                  │       The Tri-Kanon Lens      │
                  └───────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
  │ Alethekanon  │         │  Awwthekanon │         │  Brothekanon │
  │ Logic & Math │         │ Empathy/Cost │         │ Street-Level │
  └──────────────┘         └──────────────┘         └──────────────┘
```

1. **Alethekanon (Philosophical Rigor)**: Uncompromising structural physics, semantic precision, and institutional vector analysis.
2. **Awwthekanon (Somatic & Human Cost)**: Compassionate focus on real human suffering, community healing, and constructive solidarity.
3. **Brothekanon (Street Reality & Satire)**: Irreverent, sharp, and grounded translation that cuts through bureaucratic jargon to reveal absurdity.

---

## 4. 14-Post Thread Structural Standard

Every Aletheia factcheck conforms to a strictly validated 14-post sequence, capped at **290 characters** per post (under Bluesky's 300-character hard limit):

| Post # | Focus | Description & Invariants |
|---|---|---|
| **1** | **Hook & Headline** | Lead punchline, concise headline, and 2-3 topic hashtags. |
| **2** | **Stated Intent** | Official narrative, press release claim, and Stated $(\upsilon, \psi)$. |
| **3** | **Empirical Reality** | Ground-truth outcome, economic data, and Resulting $(\upsilon, \psi)$. |
| **4** | **Verdict & Integrity** | `PASS` or `FAIL`, Canonical Path Name, Hypocrisy Index ($r_{\text{net}}$). |
| **5** | **Sub-Audits** | Breakdown of distinct institutional actors or component bills. |
| **6** | **Historical Context** | Precedent, legislative history, and systemic background. |
| **7** | **The Bright Side** | Objective acknowledgment of any positive aspects or potential. |
| **8** | **The Plane Error** | The conceptual distortion (e.g. confusing *Where* with *How*). |
| **9** | **Social Physics** | Structural friction, vector forces, and power dynamics. |
| **10** | **The Trajectory** | Mathematical geodesic tracing why the vector moved as it did. |
| **11** | **Truth & Lie** | *The Unavoidable Truth* vs. *The Unavoidable Lie*. |
| **12** | **Alethekanon** | High-altitude philosophical synthesis. |
| **13** | **Awwthekanon** | Empathy, vulnerable populations, and hope. |
| **14** | **Brothekanon** | Casual, biting summary of the core absurdity. |

---

## 5. System Architecture & Components

```
                                  ┌───────────────────────────┐
                                  │      Bluesky Network      │
                                  │     & Verified RSS Feeds  │
                                  └─────────────┬─────────────┘
                                                │
                                    harvest_candidates.py
                                                │
                                                ▼
                                  ┌───────────────────────────┐
                                  │  harvested_candidates.json│
                                  └─────────────┬─────────────┘
                                                │
                                     Google AI Studio / Vertex
                                    (Convergence Test Engine)
                                                │
                                                ▼
                                  ┌───────────────────────────┐
                                  │   stories/factcheck_*.json│
                                  │       (8,651+ Audits)     │
                                  └─────────────┬─────────────┘
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    ▼                           ▼                           ▼
      ┌───────────────────────────┐┌──────────────────────────┐┌──────────────────────────┐
      │     Control Panel UI      ││  Aletheia Chat Console   ││   Modular 2-MCP Servers  │
      │   (control_panel.html)    ││   (aletheia_chat.html)   ││ (aletheia & vft-vdb MCP) │
      └───────────────────────────┘└──────────────────────────┘└──────────────────────────┘
```

### Key Python Modules & Scripts

- **`harvest_candidates.py`**: Ingests breaking news from Bluesky feeds and RSS sources, deduplicates against `harvested_history.json`, and outputs candidate queues.
- **`google_ai_studio_one_shot.py`**: Executes the 5-Phase Gnostic Convergence Test using Gemini 3.7 / 2.5 on Vertex AI or AI Studio, generating coordinates and the 14-post threads.
- **`generate_graph.py`**: Generates high-resolution Matplotlib trajectory vector plots into `graph_png/`.
- **`memory_store.py`**: SQLite FTS5 database (`memory_store.sqlite`) indexing 127+ AI discussion transcripts (`_AI files and chat logs/`) across 2,204 chunks with BM25 rank retrieval.
- **`chat_server.py`**: Local multi-threaded backend server running on port `8766`, managing hierarchical conversation branching, dual-track context assembly, and draft persistence.
- **`rebuild_registries.py`**: Compiles all individual JSON files into `stories_registry.js` (40MB+) for instant offline search and indexing.
- **`export_audit_site.py`**: Generates `dist_audit_site/`, a zero-backend static site bundling 8,651+ audits and 10,641+ graphs for public hosting.

---

## 6. Intelligence & Topic Threading Engine

### Hierarchical Multi-Thread Architecture
Conversations are stored as tree structures supporting non-destructive exploratory branches:
- **`main` Trunk**: Baseline session trajectory.
- **`thread_xxx` Branches**: Forked from specific message indices to explore sub-hypotheses without diluting the primary context.
- **Ancestral Inheritance**: When calling the LLM within a sub-thread, the server automatically traverses the tree from the root up to the fork point.
- **One-Click Synthesis Merging (`POST /session/thread/merge`)**: Compiles the sub-thread's findings into an executive takeaway card posted to the parent trunk.

### Dual-Track Context Assembly
To prevent token bloat and context blindness, prompts are dynamically assembled from:
1. **Narrative Spine**: Chronological log of major topics discussed in the session.
2. **Ancestral Thread History**: Inherited context up to the fork point.
3. **SQLite FTS5 Archive Chunks**: Up to 3 relevant context blocks pulled from the 127+ discussion files.
4. **Recent Active Thread Turns**: Immediate dialogue turns with sliding window pruning.

---

## 7. Modular 2-MCP Server Architecture

```
                    ┌──────────────────────────────────────┐
                    │      Antigravity / Claude Desktop    │
                    └───────────┬──────────────────────┬───┘
                                │                      │
                 stdio via python                      stdio via python
                                │                      │
                                ▼                      ▼
                 ┌───────────────────────┐ ┌───────────────────────┐
                 │  aletheia_mcp_server  │ │     vft_mcp_server    │
                 │   (8,651+ Audits)     │ │   (Qdrant & Archives) │
                 └───────────────────────┘ └───────────────────────┘
```

1. **`aletheia_mcp_server.py` (News Audits, Hypocrisies & Chat Memory)**:
   - Evaluated stories, hypocrisy leaderboards, policy tracking ledgers, and live conversation memory.
   - Tools: `list_stories`, `get_story`, `get_moral_average`, `get_corpus_overview`, `get_actor_hypocrisy_leaderboard`, `get_outlet_hypocrisy_leaderboard`, `get_policy_status`, `search_chat_memory`, `create_memory_observation`.

2. **`Semantic_Clusters/vft_mcp_server.py` (VFT Corpus, Vector DB & Archives)**:
   - Qdrant Cloud vector search on `vft_paragraphs` with `all-MiniLM-L6-v2`.
   - Philosophical cluster mapping (`topic_ism_mapping.json`).
   - SQLite FTS5 search across all 127+ AI discussion transcripts (`_AI files and chat logs/`).

---

## 8. Story Studio Canvas & Draft Story Pipeline

Operators can turn any exploratory chat insight directly into a draft story:
1. Click **`✨ Draft Story`** on any response in [`aletheia_chat.html`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aletheia_chat.html).
2. The AI compiles the insight into the 14-post format via `POST /story/generate_from_chat`.
3. The **Story Studio Canvas** drawer opens with editable headline, link, $(\upsilon, \psi)$ coordinates, actors, and 14 post cards with live character counters.
4. Click **`💾 Save Draft`** to atomically write `stories/factcheck_[slug].json`, instantly making it available across all launchers and registries.
