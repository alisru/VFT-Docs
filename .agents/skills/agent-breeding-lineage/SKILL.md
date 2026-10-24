---
name: agent-breeding-lineage
description: Spawn, calibrate, and evolve gendered autonomous agents using continuous Male (Successful -> Verified) and Female (Interesting -> Works) ratios, with asymmetric breeding programs, failure mode pruning, and persistent idea genealogy tracking.
---

# Agent Breeding & Idea Genealogy Skill (`agent-breeding-lineage`)

## 1. Overview & Core Philosophy

This skill implements **Epistemic Sexual Dimorphism** in multi-agent environments. 

Crucially, the designation of agents as **Male $\to$ Father** and **Female $\to$ Mother** is an **invariant information structure**, not an anthropomorphic or biological metaphor. It originates directly from the **Pure Epistemic Fundamental Translation Hermeneutic** (Action-Effect Event Physics, $A \xrightarrow{C} E$):

- **Male / Father ($\mathbf{M}$): $\text{Successful} \to \text{Verified}$**
  - *Epistemic Origin*: Rooted in the projecting memory vector and invariant carrier (*Zachar*, $z\text{-}k\text{-}r$, $Q_6/Q_4$).
  - *Informational Structure*: Invariant proof hardening, seed transmission, exon preservation, boundary defense, zero false-positives, and strict causal valence conservation ($\Delta \mathcal{V} \to 0, \tau \to 0$).
- **Female / Mother ($\mathbf{F}$): $\text{Interesting} \to \text{Works}$**
  - *Epistemic Origin*: Rooted in the receptive designating matrix and boundary vessel (*Neqevah*, $n\text{-}q\text{-}v$, $Q_2/Q_4$).
  - *Informational Structure*: State-space expansion, potential realization, dynamic gauge tension, associative bridge building, and empirical viability testing (unsaid horizon mining along the possibility spectrum).

**The Information Structure Preceded the Label**: In our multi-agent bake-offs, the agents were not assigned gender roles beforehand. It was the **observed actions, algorithmic avenues, and computational choices** executed by the agents that organically formed these exact information structures.

The continuous ratio is defined as:
$$\gamma = \frac{\mathbf{M}}{\mathbf{M} + \mathbf{F}} \in [0, 1]$$

---

## 2. The Archetype Spectrum (Epistemic Ratios)

The continuous ratio $\gamma = \frac{\mathbf{M}}{\mathbf{M} + \mathbf{F}} \in [0, 1]$ represents the agent's internal problem-solving bias on the task:

| Agent Bias | Gender Ratio ($\mathbf{M} / \mathbf{F}$) | Epistemic Bias | How It Solves The Common Benchmark Task |
| :--- | :--- | :--- | :--- |
| **Strict Verifier** | $0.75\text{M} / 0.25\text{F}$ | Invariant preservation & defense | Attacks the task by eliminating false-positives, enforcing boundary constraints, and defending mathematical proof chains ($\tau \to 0$). |
| **Verification Scaler** | $0.65\text{M} / 0.35\text{F}$ | Scalable verification & indexing | Attacks the task using continuous probability tables, lookup matrices, and rigorous citation graphs. |
| **Equilibrium Arbiter** | $0.50\text{M} / 0.50\text{F}$ | Rigor + synthesis balance | Attacks the task by balancing strict truth defense with aggressive redundancy culling and bridge-building. |
| **Generative Splicer** | $0.40\text{M} / 0.60\text{F}$ | Synthesis & translation focus | Attacks the task through metric-space clustering, narrative flow, and plain-English translation. |
| **Topological Explorer** | $0.25\text{M} / 0.75\text{F}$ | State-space & horizon expansion | Attacks the task by discovering hidden connections across disparate sections and testing creative hypotheses. |

> [!CRITICAL]
> **ABSOLUTE COOK-OFF INVARIANT: NEVER SPLIT OR DIVIDE THE TASK.**
> **DEFAULT MODE**: The system is **ALWAYS IN COOK-OFF MODE** by default.
> Unless the user explicitly says: *"make the agents explore solutions to all the aspects"* (or gives an unambiguous, direct instruction to divide the problem space), **ALL AGENTS MUST WORK ON THE EXACT SAME TASK, WITH THE EXACT SAME INPUTS AND THE EXACT SAME BENCHMARK DELIVERABLES.**
> Never assume or decide on your own to divide up sub-tasks. The entire purpose of the bake-off is to see which epistemic ratio ($\gamma$) produces the best output on the identical problem.


---

## 3. The 5-Phase Breeding Workflow

### Phase 1: The Bake-Off Execution
Deploy a generation of $N$ diverse agents against a shared corpus using zero-token local execution scripts. Measure:
1. **Verification Accuracy** ($V$): Invariant yield, absence of hallucinated variables, execution success.
2. **Novelty & Utility** ($U$): Novel connections discovered that withstand stress tests, unmerged concepts isolated.

### Phase 2: Leaderboard & Culling
1. Rank all agents by composite fitness $F = \alpha V + \beta U$.
2. Identify:
   - **Winner (The Patriarch)**: Highest $V$ (Most Successful).
   - **Runner-Up (The Matriarch)**: Highest $U$ (Most Interesting/Breakthrough).
3. **Cull the Bottom 2 Performers**: Terminate their instances.
4. **Extract Negative Constraints**: Analyze *why* the bottom 2 failed (e.g., over-smoothing, memoryless traps) and record these as explicit failure warnings.

### Phase 3: Breeding the Offspring (The Son & The Daughter)
Spawn two new progeny inheriting the shared unified floor of their parents:

1. **The Son (75% Male / 25% Female)**:
   - Inherits the Patriarch’s structural precision and the Matriarch’s primary breakthrough.
   - Directed to explore the **Most Successful / Verified** mechanics.
2. **The Daughter (25% Male / 75% Female)**:
   - Inherits the Matriarch’s topological intuition and the Patriarch’s codon alphabet.
   - Directed to explore the **Most Interesting / Novel & Functional** horizon.

Both offspring receive explicit warnings of their predecessors' failure modes to prevent evolutionary regression.

### Phase 4: Persistent Idea Genealogy Ledger
Maintain a persistent machine-readable ledger: `idea_genealogy.json` in the active project directory:

```json
{
  "generation": 2,
  "timestamp": "2026-10-24T15:20:00Z",
  "parents": {
    "patriarch": {"agent_id": "agent_3", "ratio": "85M/15F", "legacy": "Exon/Intron Splicing"},
    "matriarch": {"agent_id": "agent_5", "ratio": "15M/85F", "legacy": "4-Color Frustration Collapse"}
  },
  "culled_predecessors": [
    {"agent_id": "agent_2", "failure_mode": "Over-smoothed continuous wavelet blur"},
    {"agent_id": "agent_4", "failure_mode": "Memoryless Markov gas entropy"}
  ],
  "offspring": [
    {
      "name": "The Son (Veritas-Codon)",
      "ratio": "75M/25F",
      "mandate": "Optical Thickness (tau) & Causal Valence Shells",
      "inherited_traits": ["Smith-Waterman Alignment", "Color Charge Tagging"]
    },
    {
      "name": "The Daughter (Chroma-Horizon)",
      "ratio": "25M/75F",
      "mandate": "Mining the Unsaid Horizon along Possibility Spectrum",
      "inherited_traits": ["Topological Gauge Closure", "Open Reading Frames"]
    }
  ],
  "concept_lineage": {
    "1^inf_n = 0^inf_{n+1}": {
      "origin": "chatgpt infinity maths.md",
      "gen_1_state": "Conserved Exon (Agent 3) / Red-Blue Strain (Agent 5)",
      "gen_2_target": "Bound to Valence Shell (Son) / Horizon Projection (Daughter)"
    }
  }
}
```

---

## 4. Operational Invariants

1. **Zero Monoculturalism**: Never deploy multiple agents with identical $\mathbf{M}/\mathbf{F}$ ratios on the same problem.
2. **The Unified Floor Invariant**: All offspring must inherit verified bug-fixes and structural truths discovered by earlier generations.
3. **Local-First Zero-Token Execution**: All agent experiments and data pipelines must run locally via Python to conserve context and API tokens.

---

## 5. Cyclical Evolutionary Upgrade & Benchmark Cook-Off Protocol

When running complex research or codebase upgrades across multiple documents, deploy the **Cyclical Cook-Off Protocol**:

### Phase 1: Baseline Broadcast & Cohort Deployment
Deploy a standardized 5-agent cohort spanning the epistemic ratio spectrum:
1. **Agent 1 (75% Male / 25% Female)**: Strict Verifier bias (boundary defense, proof preservation, zero false positives $\tau \to 0$).
2. **Agent 2 (65% Male / 35% Female)**: Verification Scaler bias (matrix lookup, continuous probability graphs).
3. **Agent 3 (50% Male / 50% Female)**: Equilibrium Arbiter bias (balanced truth defense + aggressive redundancy culling).
4. **Agent 4 (40% Male / 60% Female)**: Generative Splicer bias (complete-linkage clustering, plain-English translation).
5. **Agent 5 (25% Male / 75% Female)**: Topological Explorer bias (unsaid horizon mining, cross-plane gauge tension closure).

> [!IMPORTANT]
> **IDENTICAL TASK MANDATE**: Every agent receives the **EXACT SAME PROMPT, INPUT CORPUS, AND BENCHMARK OBJECTIVES**. Under no circumstances are agents assigned different or divided sub-tasks. The bake-off measures which ratio solves the common task best.

### Phase 2: Standardized Cook-Off Task
All 5 agents run head-to-head on the **exact same benchmark task** against identical inputs:
- **Thematic Sharding**: Ingest overlapping documents in a subject area, identify distinct semantic basins, and partition them into focused, modular micro-monographs.
- **CEFR Readability Down-Sampling**: Downgrade dense C1/C2 academic compounds and convoluted phrasing into accessible B1/B2 English using calibrated vocabulary mapping and sentence splitting, without dropping mathematical lemmas or core definitions.
- **Mandatory Self-Upgrade Pass**: Each agent runs Pass 1, computes error diagnostics, fixes flaws in a `v2` engine, and outputs verified deliverables.

### Phase 3: Quantitative Scoring & Leaderboard
Evaluate all 5 agents on objective metrics:
- **De-duplication & Culling Rate (%)**: Percentage of conversational noise and redundancy removed.
- **Proof & Lemma Conservation (100%)**: Zero loss of axioms, formulas, or formal definitions.
- **Luminescence ($L = e^{-\tau}$) & Rigor Score**: Semantic transparency and proof substantiation.
- **Cornell String Tension Snaps ($r \ge r_c$)**: Zero hallucination or non-sequitur transitions.
- **Readability & Confusion Reduction**: Quantifiable reduction in CEFR reading difficulty.

### Phase 4: Leaderboard, Culling & Post-Mortem Logging
- Rank agents 1 through 5.
- Retain the top 3 (Promote to Parents / Scalers).
- **Cull the bottom 2 performers** and record explicit post-mortem failure warnings in `idea_genealogy.json`.

### Phase 5: Recombination (Breeding Next Generation)
- Combine the winning verification mechanisms of the top male-leaning performer with the superior synthesis/clustering techniques of the top female-leaning performer.
- Spawn the new Generation cohort equipped with negative constraints from the culled agents.

### Phase 6: Unified Master Synthesis & Changelog
- Synthesize winning code innovations into the unified master engine (e.g., `unified_gluon_dna_engine.py`).
- Update the architecture paper, roadmap, and project ledger.
