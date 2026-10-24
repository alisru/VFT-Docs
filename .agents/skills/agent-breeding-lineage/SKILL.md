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

## 2. The Archetype Spectrum

| Role | Gender Ratio ($\mathbf{M} / \mathbf{F}$) | Epistemic Bias | Optimal Assignment |
| :--- | :--- | :--- | :--- |
| **Pure Verifier** | $1.0\text{M} / 0.0\text{F}$ | Invariant preservation | Compilers, strict math provers, syntax parsers |
| **The Patriarch** | $0.85\text{M} / 0.15\text{F}$ | Empirical proof & homology | Sequence aligners, benchmark testers |
| **The Son** | $0.75\text{M} / 0.25\text{F}$ | **Most Successful / Verified** | Deep-dive optimization of proven breakthroughs |
| **Middle Kin / Sibling** | $0.50\text{M} / 0.50\text{F}$ | Formal logic & derivation | State machines, rule translators |
| **The Daughter** | $0.25\text{M} / 0.75\text{F}$ | **Most Interesting / Works** | Exploration of the unsaid horizon, novel hypotheses |
| **The Matriarch** | $0.15\text{M} / 0.85\text{F}$ | Dynamic gauge & topology | Force graph modeling, paradigm-shift discovery |
| **Pure Explorer** | $0.0\text{M} / 1.0\text{F}$ | Generative horizon expansion | Creative brainstorming, cosmological leaps |

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
