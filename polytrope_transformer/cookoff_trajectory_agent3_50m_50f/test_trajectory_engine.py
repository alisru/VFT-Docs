"""
Test Suite for Dynamic Trajectory Engine & Vectorized Ribosomal Reading Head
=============================================================================
Competitor 3: Arbiter (50M / 50F)
Vectorized High-Throughput Ribosomal Reading Head & Balanced Equilibrium Arbiter

Validates:
1. Grounded derivation sequence vs. ungrounded leap insolvency loss.
2. Dynamic Trajectory Integrator math invariants (||Sigma_D||, iota_D in [-1, 1]).
3. Ribosomal Reading Head Gumbel-Softmax codon transcription & prefix derivation ledger.
4. Four Colored Gluon Forces & Semantic Git pairwise contradiction shear.
5. High-throughput vectorized inference latency (tokens/sec).
6. 25-epoch AdamW training loop with 100% non-zero parameter gradient verification
   and asserted loss reduction.
"""

import sys
import time
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List

from dynamic_trajectory_engine import (
    DynamicTrajectoryIntegrator,
    RibosomalReadingHead,
    DerivationLawCompletenessLoss,
    FourColoredGluonForces,
    BalancedEquilibriumArbiterModel,
    Codon,
    ENGINE_NAMES,
    MODAL_NAMES
)


def set_seed(seed: int = 42):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def test_grounded_vs_ungrounded_derivation():
    """
    Test 1: Proves insolvency penalty is near zero for grounded derivation,
    and huge (> 1.0) for ungrounded leaps ('maths without working out').
    """
    print("\n" + "="*70)
    print("TEST 1: GROUNDED DERIVATION VS UNGROUNDED LEAP INSOLVENCY LOSS")
    print("="*70)

    loss_fn = DerivationLawCompletenessLoss(beta=0.5, will_be_weight=2.0, law2_fidelity_weight=0.5)

    B = 2
    T = 16 # 16 steps

    # --- 1. Construct Grounded Sequence ---
    # Step 0..3: Constructive ('is_like' / 'may_be')
    # Step 4..7: Reductive ('cant_be' / 'is_not')
    # Step 8..11: Regressive ('wont_be' / 'was_like')
    # Step 12..13: Productive Inner ('can_be')
    # Step 14..15: Productive Outer ('will_be')
    M_grounded = torch.zeros(B, T, 8)
    for t in range(T):
        if t < 4:
            M_grounded[:, t, 0] = 0.8 # is_like
            M_grounded[:, t, 1] = 0.2 # may_be
        elif t < 8:
            M_grounded[:, t, 4] = 0.5 # cant_be
            M_grounded[:, t, 5] = 0.5 # is_not
        elif t < 12:
            M_grounded[:, t, 6] = 0.3 # wont_be
            M_grounded[:, t, 7] = 0.7 # was_like
        elif t < 14:
            M_grounded[:, t, 2] = 0.9 # can_be (demonstrating capability first)
            M_grounded[:, t, 3] = 0.1 # will_be
        else:
            M_grounded[:, t, 2] = 0.1 # can_be
            M_grounded[:, t, 3] = 0.9 # will_be (definitive realization)

    # Engine mapping for grounded
    M2E = torch.zeros(8, 4)
    M2E[0:2, 0] = 1.0
    M2E[2:4, 1] = 1.0
    M2E[4:6, 2] = 1.0
    M2E[6:8, 3] = 1.0
    Q_grounded = torch.matmul(M_grounded, M2E)

    antecedent_g = Q_grounded[..., 0] + Q_grounded[..., 2] + Q_grounded[..., 3]
    cumsum_g = torch.cumsum(antecedent_g, dim=1)
    prior_working_g = cumsum_g - antecedent_g

    codon_grounded = Codon(
        Q=Q_grounded,
        M=M_grounded,
        iota=(Q_grounded[..., 0] + Q_grounded[..., 1] - Q_grounded[..., 2] - Q_grounded[..., 3]),
        H=torch.zeros(B, T)
    )
    ledger_grounded = {
        "antecedent_working_out": antecedent_g,
        "cumulative_working_out": prior_working_g,
        "productive_assertion": Q_grounded[..., 1],
        "will_be_activation": M_grounded[..., 3],
        "can_be_activation": M_grounded[..., 2],
    }

    res_grounded = loss_fn(codon_grounded, ledger_grounded)
    loss_grounded = res_grounded["total_loss"].item()

    # --- 2. Construct Ungrounded Sequence ---
    # Jumps immediately to 'will_be' at t=0..7 with ZERO prior derivation
    M_ungrounded = torch.zeros(B, T, 8)
    M_ungrounded[:, :, 3] = 0.95 # modal 3: will_be directly asserted throughout!
    M_ungrounded[:, :, 2] = 0.05 # can_be
    Q_ungrounded = torch.matmul(M_ungrounded, M2E)

    antecedent_u = Q_ungrounded[..., 0] + Q_ungrounded[..., 2] + Q_ungrounded[..., 3] # essentially 0.0
    cumsum_u = torch.cumsum(antecedent_u, dim=1)
    prior_working_u = cumsum_u - antecedent_u

    codon_ungrounded = Codon(
        Q=Q_ungrounded,
        M=M_ungrounded,
        iota=torch.ones(B, T),
        H=torch.zeros(B, T)
    )
    ledger_ungrounded = {
        "antecedent_working_out": antecedent_u,
        "cumulative_working_out": prior_working_u,
        "productive_assertion": Q_ungrounded[..., 1],
        "will_be_activation": M_ungrounded[..., 3],
        "can_be_activation": M_ungrounded[..., 2],
    }

    res_ungrounded = loss_fn(codon_ungrounded, ledger_ungrounded)
    loss_ungrounded = res_ungrounded["total_loss"].item()

    print(f"Grounded Derivation Loss:   {loss_grounded:.6f} (near-zero, fully substantiated)")
    print(f"Ungrounded Leap Loss:       {loss_ungrounded:.6f} (huge penalty for unsupported claims)")
    print(f"Ratio (Ungrounded/Grounded): {loss_ungrounded / max(loss_grounded, 1e-6):.2f}x")

    assert loss_grounded < 0.1, f"Expected grounded loss < 0.1, got {loss_grounded}"
    assert loss_ungrounded > 1.0, f"Expected ungrounded loss > 1.0, got {loss_ungrounded}"
    print(">> TEST 1 PASSED: Insolvency penalty strictly discriminates unsubstantiated leaps.")


def test_trajectory_integrator():
    """
    Test 2: Validates mathematical invariants of the Dynamic Trajectory Integrator.
    """
    print("\n" + "="*70)
    print("TEST 2: DYNAMIC TRAJECTORY INTEGRATOR INVARIANTS")
    print("="*70)

    d_model = 64
    B = 4
    T = 24
    K = 3

    integrator = DynamicTrajectoryIntegrator(d_model=d_model, num_topics=K)
    x = torch.randn(B, T, d_model)

    out = integrator(x)

    # 1. Check non-negativity of operational charges sigma(t)
    sigma_t = out["sigma_t"]
    assert torch.all(sigma_t >= 0.0), "Operational charges must be non-negative!"
    print(f"Operational charges sigma(t) shape: {sigma_t.shape}, min value: {sigma_t.min().item():.6f} (>= 0.0)")

    # 2. Check path integration weights sum to 1.0
    weights = out["weights"]
    w_sum = weights.sum(dim=-1)
    assert torch.allclose(w_sum, torch.ones_like(w_sum), atol=1e-5), "Path weights must sum to 1.0 across sequence!"
    print(f"Attention weights w(t) normalized along sequence: {w_sum.shape} all sum to 1.0")

    # 3. Check Inclusive-Exclusive Polarity bounds [-1, +1]
    iota_D = out["iota_D"]
    assert torch.all(iota_D >= -1.0 - 1e-5) and torch.all(iota_D <= 1.0 + 1e-5), "iota_D must reside in [-1, +1]!"
    print(f"Polarity iota_D shape: {iota_D.shape}, range: [{iota_D.min().item():.4f}, {iota_D.max().item():.4f}] in [-1, +1]")

    # 4. Check Connection Magnitude ||Sigma_D|| = sqrt(C^2 + P^2 + R^2 + G^2)
    Sigma_D = out["Sigma_D"]
    mag = out["connection_magnitude"]
    manual_mag = torch.sqrt(torch.sum(Sigma_D ** 2, dim=-1) + integrator.eps)
    assert torch.allclose(mag, manual_mag, atol=1e-5), "Connection magnitude calculation mismatch!"
    print(f"Connection magnitude ||Sigma_D|| matches manual Euclidean norm: {mag.mean().item():.4f}")

    # 5. Check 50M/50F Balanced Equilibrium Arbiter metrics
    eq_dev = out["equilibrium_deviation"]
    entropy = out["arbiter_entropy"]
    assert torch.all(eq_dev >= 0.0), "Equilibrium deviation must be non-negative"
    assert torch.all(entropy >= 0.0), "Entropy must be non-negative"
    print(f"Arbiter equilibrium deviation mean: {eq_dev.mean().item():.4f}, arbiter entropy: {entropy.mean().item():.4f}")
    print(">> TEST 2 PASSED: Dynamic Trajectory Integrator math invariants fully satisfied.")


def test_ribosomal_reading_head():
    """
    Test 3: Validates Ribosomal Reading Head Gumbel-Softmax transcription and codon generation.
    """
    print("\n" + "="*70)
    print("TEST 3: RIBOSOMAL READING HEAD & CODON TRANSCRIPTION")
    print("="*70)

    d_model = 64
    B = 2
    T = 12

    head = RibosomalReadingHead(d_model=d_model, temperature=0.8)
    x = torch.randn(B, T, d_model)

    codon, ledger = head(x)

    # 1. Check shapes
    assert codon.M.shape == (B, T, 8), f"Expected M shape (B, T, 8), got {codon.M.shape}"
    assert codon.Q.shape == (B, T, 4), f"Expected Q shape (B, T, 4), got {codon.Q.shape}"
    assert codon.iota.shape == (B, T), f"Expected iota shape (B, T), got {codon.iota.shape}"
    assert codon.H.shape == (B, T), f"Expected H shape (B, T), got {codon.H.shape}"
    print(f"Codon transcribed: Q={codon.Q.shape}, M={codon.M.shape}, iota={codon.iota.shape}, H={codon.H.shape}")

    # 2. Check probability conservation: sum over modals == 1.0, sum over engines == 1.0
    m_sum = codon.M.sum(dim=-1)
    q_sum = codon.Q.sum(dim=-1)
    assert torch.allclose(m_sum, torch.ones_like(m_sum), atol=1e-4), "Modal probabilities must sum to 1.0!"
    assert torch.allclose(q_sum, torch.ones_like(q_sum), atol=1e-4), "Engine probabilities must sum to 1.0!"
    print("Conservation of probability verified: sum(M) = 1.0, sum(Q) = 1.0")

    # 3. Check cumulative working out causal boundary: step 0 must have exactly 0 prior working out
    prior_working = ledger["cumulative_working_out"]
    assert torch.all(prior_working[:, 0] == 0.0), "Initial step prior working out must be 0.0!"
    print(f"Causal prefix derivation ledger confirmed: prior_working[:, 0] == 0.0")

    # 4. Check straight-through discrete mode
    codon_hard, _ = head(x, hard=True)
    # Check that hard modal states are strictly one-hot
    max_vals = codon_hard.M.max(dim=-1).values
    assert torch.allclose(max_vals, torch.ones_like(max_vals)), "Hard Gumbel-Softmax must produce one-hot codons!"
    print("Discrete codon mode confirmed: 100% one-hot modal emission.")
    print(">> TEST 3 PASSED: Ribosomal Reading Head codon transcription verified.")


def test_four_colored_gluon_forces():
    """
    Test 4: Validates the 4 colored force vectors (Red, Green, Blue, Magenta) and Semantic Git.
    """
    print("\n" + "="*70)
    print("TEST 4: FOUR COLORED GLUON FORCES & SEMANTIC GIT INTERACTION")
    print("="*70)

    gluon = FourColoredGluonForces()

    B = 2
    T = 8
    # Test case: High Red Tension sequence where step 0 has both will_be (3) and cant_be (4)
    modal_dist = torch.zeros(B, T, 8)
    modal_dist[:, 0, 3] = 0.8 # will_be
    modal_dist[:, 0, 4] = 0.8 # cant_be (direct collision!)

    out = gluon(modal_dist)
    inst_forces = out["instantaneous_forces"]
    total_forces = out["total_forces"]

    assert inst_forces.shape == (B, T, 4), f"Unexpected shape {inst_forces.shape}"
    assert total_forces.shape == (B, 4), f"Unexpected shape {total_forces.shape}"

    red_step0 = inst_forces[:, 0, 0] # Red force at step 0
    assert torch.all(red_step0 > 0.6), "Red contradiction force must trigger on will_be <-> cant_be collision!"
    print(f"Red force on direct collision: {red_step0.mean().item():.4f} (strong contradiction signal)")

    # Test Semantic Git pairwise cross-document conflict
    # Doc A asserts 'will_be'
    doc_A = torch.zeros(1, 8)
    doc_A[0, 3] = 1.0 # will_be

    # Doc B asserts 'cant_be'
    doc_B = torch.zeros(1, 8)
    doc_B[0, 4] = 1.0 # cant_be

    git_res = gluon.compute_pairwise_git_interaction(doc_A, doc_B)
    conflict = git_res["conflict_score"]
    assert conflict.item() > 0.9, f"Semantic Git must flag collision between Doc A and Doc B, got {conflict.item()}"
    print(f"Semantic Git Cross-Document Conflict Score (Red Shear): {conflict.item():.4f}")
    print(">> TEST 4 PASSED: Four Colored Gluon Forces & Semantic Git interaction verified.")


def test_throughput_benchmark():
    """
    Test 5: Measures vectorized inference latency and throughput in tokens/second.
    """
    print("\n" + "="*70)
    print("TEST 5: HIGH-THROUGHPUT VECTORIZED BENCHMARK")
    print("="*70)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running benchmark on device: {device}")

    d_model = 128
    B = 32
    T = 256
    num_tokens = B * T

    model = BalancedEquilibriumArbiterModel(d_model=d_model).to(device)
    model.eval()

    x = torch.randn(B, T, d_model, device=device)

    # Warmup
    with torch.no_grad():
        for _ in range(10):
            _ = model(x)
    if device.type == "cuda":
        torch.cuda.synchronize()

    # Timed runs
    num_runs = 50
    t0 = time.perf_counter()
    with torch.no_grad():
        for _ in range(num_runs):
            _ = model(x)
    if device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - t0

    total_tokens = num_tokens * num_runs
    tokens_per_sec = total_tokens / elapsed
    ms_per_batch = (elapsed / num_runs) * 1000.0

    print(f"Batch configuration: Batch={B}, Sequence Length={T} ({num_tokens} tokens/batch)")
    print(f"Evaluated {num_runs} batches ({total_tokens:,} tokens) in {elapsed:.3f} s")
    print(f"Inference Latency:   {ms_per_batch:.2f} ms per batch")
    print(f"Throughput:          {tokens_per_sec:,.0f} tokens / second")

    assert tokens_per_sec > 5000, f"Expected throughput > 5,000 tokens/sec, got {tokens_per_sec:.0f}"
    print(">> TEST 5 PASSED: High-throughput vectorized execution confirmed.")
    return tokens_per_sec, ms_per_batch


def test_25_epoch_adamw_training():
    """
    Test 6: 25-epoch AdamW training loop proving:
    - 100% of parameters receive non-zero gradients.
    - Loss reduction is verified and asserted.
    """
    print("\n" + "="*70)
    print("TEST 6: 25-EPOCH AdamW TRAINING LOOP & GRADIENT VERIFICATION")
    print("="*70)

    set_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    d_model = 64
    B = 16
    T = 32

    model = BalancedEquilibriumArbiterModel(d_model=d_model, beta=0.5).to(device)
    model.train()

    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=1e-4)

    # Target: A synthetic corpus with mixed groundings and desired topic alignment
    # Training objective: Minimize Insolvency + Arbitrate Equilibrium (|iota|) + Maximize Entropy
    target_data = torch.randn(B, T, d_model, device=device)

    losses: List[float] = []

    print(f"{'Epoch':<8}{'Total Loss':<14}{'Insolvency':<14}{'Law2 Loss':<14}{'Red Force':<14}{'Equil Dev':<14}")
    print("-" * 78)

    for epoch in range(1, 26):
        optimizer.zero_grad()

        out = model(target_data)
        comp_loss = out["completeness_loss"]
        loss_insolv = comp_loss["loss_insolvency"]
        loss_law2 = comp_loss["loss_law2"]
        forces = out["forces"]

        # Trajectory equilibrium regularization (50M/50F arbiter goal):
        # 1. Penalize extreme one-sided polar drift: |iota_D|
        loss_equil = out["trajectory"]["equilibrium_deviation"].mean()
        # 2. Reward balanced operational exploration: negative entropy
        loss_entropy = -0.1 * out["trajectory"]["arbiter_entropy"].mean()
        # 3. Penalize contradictory red force tension
        loss_red = 0.5 * forces["red"].mean()

        total_loss = loss_insolv + loss_law2 + 0.2 * loss_equil + loss_entropy + loss_red

        total_loss.backward()

        # Check gradients on 100% of parameters in every epoch
        zero_grad_params = []
        none_grad_params = []
        for name, param in model.named_parameters():
            if param.requires_grad:
                if param.grad is None:
                    none_grad_params.append(name)
                elif torch.all(param.grad == 0):
                    zero_grad_params.append(name)

        assert len(none_grad_params) == 0, f"Epoch {epoch}: Parameters with None grad: {none_grad_params}"
        assert len(zero_grad_params) == 0, f"Epoch {epoch}: Parameters with zero grad: {zero_grad_params}"

        optimizer.step()
        loss_val = total_loss.item()
        losses.append(loss_val)

        if epoch % 5 == 0 or epoch == 1:
            print(f"{epoch:<8}{loss_val:<14.5f}{loss_insolv.item():<14.5f}{loss_law2.item():<14.5f}{loss_red.item():<14.5f}{loss_equil.item():<14.5f}")

    initial_loss = losses[0]
    final_loss = losses[-1]
    pct_reduction = ((initial_loss - final_loss) / abs(initial_loss)) * 100.0

    print("-" * 64)
    print(f"Initial Loss (Epoch 1):  {initial_loss:.5f}")
    print(f"Final Loss (Epoch 25):    {final_loss:.5f}")
    print(f"Loss Reduction:          {pct_reduction:.2f}%")

    assert final_loss < initial_loss, f"Training failed to reduce loss: initial={initial_loss}, final={final_loss}"
    assert pct_reduction > 20.0, f"Expected loss reduction > 20%, got {pct_reduction:.2f}%"

    # Verify 100% parameter gradient flow
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total trainable parameters: {total_params} (100% verified active gradients)")
    print(">> TEST 6 PASSED: 25-epoch AdamW training successful with verified gradient propagation.")


def run_all_tests():
    print("\n" + "#"*70)
    print("STARTING COMPETITOR 3 TRAJECTORY & RIBOSOMAL ENGINE TEST SUITE")
    print("#"*70)

    test_grounded_vs_ungrounded_derivation()
    test_trajectory_integrator()
    test_ribosomal_reading_head()
    test_four_colored_gluon_forces()
    tokens_per_sec, ms_per_batch = test_throughput_benchmark()
    test_25_epoch_adamw_training()

    print("\n" + "#"*70)
    print("ALL TESTS PASSED SUCCESSFULLY! (EXIT CODE 0)")
    print("#"*70 + "\n")


if __name__ == "__main__":
    run_all_tests()
    sys.exit(0)
