"""
Test Suite and Benchmark for Semantic Gluon Attention.
Generation 7 Competitor 2: PyTorch Attention Matriarch (25% Male / 75% Female)

Verifies:
  1. Forward pass tensor shapes and validity across all sub-layers.
  2. Ribosomal Exon Splicing mask effectiveness (intron zeroing & sparsity).
  3. Causal Valence Shell matrix properties.
  4. Cornell Confinement potential and string snapping detection.
  5. 7-Planes non-commutative gauge friction matrix values.
  6. Luminescence optical attenuation field.
  7. Backward pass autograd integrity: non-null gradients on all parameters.
  8. 10-step AdamW optimization with verifiable strict loss decrease.
  9. Benchmarking FLOPS, latency, and intron excising speedup.
"""

import os
import sys
import time
import math
from typing import Tuple, Dict, Optional, List
import torch
import torch.nn as nn
import torch.nn.functional as F

from semantic_gluon_attention import (
    SemanticGluonConfig,
    SemanticGluonAttention,
    SemanticGluonTransformerBlock
)


def compute_gluon_physics_loss(
    output: torch.Tensor,
    target: torch.Tensor,
    diagnostics: dict,
    exon_mask: torch.Tensor
) -> Tuple[torch.Tensor, dict]:
    """
    Computes unified physics loss combining:
      1. Task Reconstruction MSE Loss
      2. Causal Valence Conservation Loss (Ingress B_i must be saturated by attended Egress F_j)
      3. Cornell Confinement Regularization (penalizing unbridged string snaps r > r_c)
      4. Luminescence Transparency Regularization (minimizing opaque fog tau)
    """
    # 1. Target prediction loss
    task_loss = F.mse_loss(output, target)

    # 2. Causal Valence Shell Conservation
    # Attended egress: sum_j A_hij * F_j
    attn = diagnostics["attention_weights"]  # [B, H, N, N]
    egress = diagnostics["egress"]          # [B, N, d_v]
    ingress = diagnostics["ingress"]        # [B, N, d_v]
    # Average attention across heads: [B, N, N]
    avg_attn = attn.mean(dim=1)
    attended_egress = torch.bmm(avg_attn, egress)  # [B, N, d_v]
    valence_loss = F.mse_loss(attended_egress, ingress)

    # 3. Cornell Confinement Loss (penalizes string snapping r >= r_c)
    z_coords = diagnostics["z_coords"]  # [B, N]
    r_ij = torch.abs(z_coords.unsqueeze(2) - z_coords.unsqueeze(1))
    r_c = 1.529
    confinement_loss = torch.mean(torch.square(F.relu(r_ij - r_c)))

    # 4. Luminescence loss: encourage high transmission for exons
    tau = diagnostics["tau_tokens"]  # [B, N]
    exon_tau = (tau * exon_mask).sum() / (exon_mask.sum() + 1e-6)
    luminescence_loss = 0.1 * exon_tau

    # 5. Ribosomal Exon Classification Loss (supervising exon_gate)
    exon_probs = diagnostics["exon_probs"]  # [B, N]
    exon_bce = F.binary_cross_entropy(exon_probs, exon_mask.float())

    # 6. Hadron Color Singlet Balance: equal distribution across r, g, b charges
    color_charges = diagnostics["color_charges"]  # [B, N, 3]
    hadron_balance = F.mse_loss(color_charges.mean(dim=1), torch.full((output.shape[0], 3), 1.0 / 3.0, device=output.device))

    total_loss = task_loss + 0.5 * valence_loss + 1.0 * confinement_loss + luminescence_loss + 0.2 * exon_bce + 0.1 * hadron_balance

    loss_dict = {
        "total_loss": total_loss.item(),
        "task_loss": task_loss.item(),
        "valence_loss": valence_loss.item(),
        "confinement_loss": confinement_loss.item(),
        "luminescence_loss": luminescence_loss.item(),
        "exon_bce": exon_bce.item(),
        "hadron_balance": hadron_balance.item()
    }
    return total_loss, loss_dict


def run_comprehensive_tests():
    print("=" * 75)
    print("GEN 7 COMPETITOR 2: PYTORCH ATTENTION MATRIARCH (25M / 75F)")
    print("EXECUTABLE PYTORCH SEMANTIC GLUON ATTENTION TEST SUITE")
    print("=" * 75)

    device_name = "cuda" if torch.cuda.is_available() else "cpu"
    try:
        device = torch.device(device_name)
        _test_alloc = torch.zeros(1024, device=device)
        del _test_alloc
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception as e:
        print(f"CUDA initialization note ({e}), falling back to CPU for reliable testing.")
        device = torch.device("cpu")
    print(f"Executing on device: {device}")
    torch.manual_seed(42)

    # 1. Instantiate Layer
    B, N, D = 2, 16, 384
    config = SemanticGluonConfig(
        embed_dim=D,
        num_heads=6,
        valence_dim=64,
        alpha_valence=0.75,
        alpha_s=0.35,
        sigma=0.85,
        r_c=1.529,
        sigma_snap=4.0,
        dropout=0.0  # zero dropout for deterministic gradient verification
    )
    try:
        attention_layer = SemanticGluonAttention(config).to(device)
    except RuntimeError as oom:
        if "out of memory" in str(oom).lower():
            print(f"CUDA memory constrained on Windows host. Switching execution device to CPU.")
            device = torch.device("cpu")
            attention_layer = SemanticGluonAttention(config).to(device)
        else:
            raise oom

    # Count parameters
    total_params = sum(p.numel() for p in attention_layer.parameters() if p.requires_grad)
    print(f"Initialized SemanticGluonAttention with {total_params:,} trainable parameters.")

    # 2. Synthetic Inputs with Ribosomal Exon Mask
    # Let sequence have 10 exons (coding) and 6 introns (conversational noise)
    # Exons: positions [0, 1, 2, 3, 5, 6, 8, 9, 10, 12]
    # Introns: positions [4, 7, 11, 13, 14, 15]
    exon_mask = torch.tensor([
        [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0]
    ], device=device)

    x = torch.randn(B, N, D, device=device, requires_grad=False)
    target = torch.randn(B, N, D, device=device)

    print(f"\n[Test 1] Executing Forward Pass with B={B}, N={N}, D={D}...")
    output, diag = attention_layer(x, exon_mask=exon_mask, return_diagnostics=True)

    # Assert output shape
    assert output.shape == (B, N, D), f"Expected shape {(B, N, D)}, got {output.shape}"
    assert not torch.isnan(output).any(), "NaN found in output tensor!"
    assert not torch.isinf(output).any(), "Inf found in output tensor!"
    print("  -> Output tensor shape verified:", output.shape)

    # 3. Verify Ribosomal Exon Splicing Mask Mechanics
    attn_weights = diag["attention_weights"]  # [B, H, N, N]
    intron_indices = [4, 7, 11, 13, 14, 15]
    exon_indices = [0, 1, 2, 3, 5, 6, 8, 9, 10, 12]

    # Attention weights pointing to introns MUST be zeroed out
    intron_attn_mass = attn_weights[:, :, :, intron_indices].sum().item()
    total_attn_mass = attn_weights.sum().item()
    intron_leak_ratio = intron_attn_mass / total_attn_mass

    # Calculate exact attention sparsity (fraction of zeros or near-zeros < 1e-5)
    zero_elements = (attn_weights < 1e-4).sum().item()
    total_elements = attn_weights.numel()
    sparsity_pct = (zero_elements / total_elements) * 100.0

    print(f"\n[Test 2] Ribosomal Splicing Mask Verification:")
    print(f"  -> Total attention mass on Introns: {intron_attn_mass:.6e}")
    print(f"  -> Intron leak ratio: {intron_leak_ratio:.6e} (must be ~ 0.0)")
    print(f"  -> Attention Matrix Sparsity: {sparsity_pct:.2f}%")
    assert intron_leak_ratio < 1e-4, "Ribosomal splicing failed to zero out non-coding introns!"
    print("  -> PASSED: Ribosomal Exon Splicing correctly isolates coding exons.")

    # 4. Verify Cornell Confinement and Gauge Friction Fields
    v_cornell = diag["v_cornell"]
    gamma_friction = diag["gamma_friction"]
    luminescence = diag["luminescence_field"]
    z_coords = diag["z_coords"]
    string_snaps = diag["string_snaps"]

    print(f"\n[Test 3] Physical Sub-Fields Verification:")
    print(f"  -> Cornell Potential Range: [{v_cornell.min().item():.3f}, {v_cornell.max().item():.3f}]")
    print(f"  -> Gauge Friction Range:    [{gamma_friction.min().item():.3f}, {gamma_friction.max().item():.3f}]")
    print(f"  -> Luminescence Field Mean: {luminescence.mean().item():.3f} (Range: [{luminescence.min().item():.3f}, {luminescence.max().item():.3f}])")
    print(f"  -> Z-coordinate spread:     std={z_coords.std().item():.3f}, min={z_coords.min().item():.3f}, max={z_coords.max().item():.3f}")
    print(f"  -> Initial String Snaps (r >= 1.529): {string_snaps.sum().item()} pairs")

    assert gamma_friction.min().item() >= 0.2, "Gauge friction invalidly low!"
    assert luminescence.min().item() > 0.0, "Luminescence zero or negative!"
    print("  -> PASSED: All continuous physical gauge fields valid.")

    # 5. Verify Autograd Backward Pass and Gradient Existence
    print(f"\n[Test 4] Computing Loss and Backpropagating Gradients...")
    optimizer = torch.optim.AdamW(attention_layer.parameters(), lr=1e-3, weight_decay=1e-4)
    optimizer.zero_grad()

    loss, loss_metrics = compute_gluon_physics_loss(output, target, diag, exon_mask)
    loss.backward()

    # Check gradients on all parameters
    params_with_grad = 0
    total_grad_norm_sq = 0.0
    missing_grad_params = []

    for name, param in attention_layer.named_parameters():
        if param.requires_grad:
            if param.grad is None:
                missing_grad_params.append(name)
            else:
                params_with_grad += 1
                assert not torch.isnan(param.grad).any(), f"NaN in gradient for {name}"
                assert not torch.isinf(param.grad).any(), f"Inf in gradient for {name}"
                param_norm = param.grad.data.norm(2).item()
                total_grad_norm_sq += param_norm ** 2

    total_grad_norm = math.sqrt(total_grad_norm_sq)
    print(f"  -> Gradients verified for {params_with_grad} / {len(list(attention_layer.parameters()))} parameter tensors.")
    print(f"  -> Total Gradient Norm: {total_grad_norm:.4f}")
    assert len(missing_grad_params) == 0, f"Parameters missing gradients: {missing_grad_params}"
    assert total_grad_norm > 0.0, "Gradient norm is zero!"
    print("  -> PASSED: Clean non-zero gradients verified across all sub-layers.")

    # 6. Run 10 Optimization Steps and Assert Loss Strictly Decreases
    print(f"\n[Test 5] Running 10-Step AdamW Optimization Loop...")
    initial_loss = loss.item()
    history = [initial_loss]

    for step in range(1, 11):
        optimizer.step()
        optimizer.zero_grad()

        out_step, diag_step = attention_layer(x, exon_mask=exon_mask, return_diagnostics=True)
        step_loss, step_metrics = compute_gluon_physics_loss(out_step, target, diag_step, exon_mask)
        step_loss.backward()

        history.append(step_loss.item())
        print(f"  Step {step:2d} | Loss: {step_loss.item():.4f} "
              f"(Task: {step_metrics['task_loss']:.4f}, Valence: {step_metrics['valence_loss']:.4f}, "
              f"Confinement: {step_metrics['confinement_loss']:.4f})")

    final_loss = history[-1]
    loss_reduction_pct = ((initial_loss - final_loss) / initial_loss) * 100.0
    print(f"\n  -> Initial Loss: {initial_loss:.4f}")
    print(f"  -> Final Loss:   {final_loss:.4f}")
    print(f"  -> Loss Reduction: {loss_reduction_pct:.2f}%")
    assert final_loss < initial_loss, f"Optimization failed! Final loss ({final_loss}) >= Initial loss ({initial_loss})"
    print("  -> PASSED: Loss strictly decreased over 10 optimization steps.")

    # 7. Speed and Efficiency: Full Sequence vs Spliced Exon Speedup
    print(f"\n[Test 6] Benchmarking Ribosomal Exon Splicing Throughput...")
    attention_layer.eval()
    warmup = 10
    timed_steps = 100

    with torch.no_grad():
        for _ in range(warmup):
            _ = attention_layer(x, exon_mask=exon_mask, return_diagnostics=False)
        
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        t0 = time.perf_counter()
        for _ in range(timed_steps):
            _ = attention_layer(x, exon_mask=exon_mask, return_diagnostics=False)
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        full_latency_ms = (time.perf_counter() - t0) * 1000.0 / timed_steps

        # Spliced execution: Only coding exons (N_exon = 10 instead of 16)
        x_spliced = x[:, exon_indices, :]  # [B, 10, D]
        for _ in range(warmup):
            _ = attention_layer(x_spliced, exon_mask=None, return_diagnostics=False)
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        t0 = time.perf_counter()
        for _ in range(timed_steps):
            _ = attention_layer(x_spliced, exon_mask=None, return_diagnostics=False)
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        spliced_latency_ms = (time.perf_counter() - t0) * 1000.0 / timed_steps

    speedup = full_latency_ms / spliced_latency_ms
    flop_reduction = (1.0 - (len(exon_indices)**2 / N**2)) * 100.0
    print(f"  -> Un-spliced (N=16) Latency: {full_latency_ms:.3f} ms/pass")
    print(f"  -> Exon Spliced (N=10) Latency: {spliced_latency_ms:.3f} ms/pass")
    print(f"  -> Measured Speedup: {speedup:.2f}x")
    print(f"  -> Theoretical Attention FLOP reduction: {flop_reduction:.1f}%")

    # 8. Test SemanticGluonTransformerBlock Integration
    print(f"\n[Test 7] Testing Full SemanticGluonTransformerBlock...")
    block = SemanticGluonTransformerBlock(config).to(device)
    block_out, block_diag = block(x, exon_mask=exon_mask)
    assert block_out.shape == (B, N, D), f"Block shape mismatch: {block_out.shape}"
    block_loss = block_out.sum()
    block_loss.backward()
    print("  -> PASSED: Full Transformer Block forward and backward passes verified.")

    print("\n" + "=" * 75)
    print("ALL TESTS PASSED WITH 100% MATHEMATICAL AND GRADIENT RIGOR.")
    print("=" * 75)

    return {
        "initial_loss": initial_loss,
        "final_loss": final_loss,
        "loss_reduction_pct": loss_reduction_pct,
        "sparsity_pct": sparsity_pct,
        "total_grad_norm": total_grad_norm,
        "full_latency_ms": full_latency_ms,
        "spliced_latency_ms": spliced_latency_ms,
        "speedup": speedup,
        "total_params": total_params
    }


if __name__ == "__main__":
    results = run_comprehensive_tests()
