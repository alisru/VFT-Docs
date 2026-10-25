# Plan v5: Grounded PyTorch Synthesis, Causal Restoration & Dense Gluon Training
**Archive Date:** October 25, 2026  
**Status:** In Progress / Active  
**Predecessors:** 
- `PLAN_20261009_v1_Fractal_Polytrope_Transformer.md`
- `PLAN_20261009_v2_Causal_Z_Axis_Revision.md`
- `PLAN_20261018_v3_Actual_Language_Model_Pathway.md`
- `PLAN_20261018_v4_Sovereign_LM_Unified_Synthesis.md`

---

## 1. Context & Objectives
Following the Gen 7 PyTorch Attention Cook-Off, the system successfully pivoted from heuristic text-processing scripts to genuine PyTorch deep learning modules. 
This plan outlines the next critical phase:
1. **Restore the Lost Temporal Causal Accumulator (`TemporalCausalAccumulator`)**:
   Implement the sequential $5' \to 3'$ causal ledger to catch unearned assertions ("maths without working out").
2. **Dense Pairwise Training on Full 500-Word Gluon Graph**:
   Train `OrientedGluonFluxBondHead` directly across all 564 `guaranteed` pairs and 564 `forbidden` clashes from `scaled_gluon_dictionary_v2.json` to eliminate the remaining attention leaks.
3. **Port Zero-Shearing Beam Decoder to PyTorch**:
   Translate the Cycle 5 volume overlap / reality strain hallucination filter into the PyTorch inference loop.
4. **Wire 3-Color Baryon Singlet Constraint**:
   Enforce the Thesis + Context + Proof triplet requirement for stable semantic output.

---

## 2. Running Log & Implementation Status

### Step 1: Historical Timeline & Forensic Audit (Completed)
- Authored `docs/PROJECT_MASTER_TIMELINE_AND_AUDIT.md`.
- Traced the complete trajectory from Phase 1 through Phase 5 (Cycles 1–101, Generations 1–7).
- Audited all invariants: identified what made it into PyTorch vs what remained in heuristic relics.

### Step 2: Temporal Causal Accumulator (Next Up)
- Implement `TemporalCausalAccumulator(nn.Module)` in `src/polytrope_layers.py`.
- Computes $\Sigma_{\text{cause}}(t) = \sum_{\tau \le t} \mathcal{F}_\tau - \mathcal{B}_\tau$.
- Flags unsubstantiated conclusions when $\mathcal{B}_t > \Sigma_{\text{cause}}(t-1)$.

### Step 3: Dense Pairwise Graph Training (Scheduled)
- Implement `train_dense_gluon_graph.py`.
- Iterate through all 564 guaranteed links and 564 forbidden clashes.
- Target: 0.0000 attention leakage on forbidden pairs.

### Step 4: PyTorch Zero-Shearing Decoder (Scheduled)
- Integrate beam search with `BeliefStateDiagnosticHead` ($\eta \le 1.0$) and `OrientedGluonFluxBondHead` ($r < r_c$).
