"""
Sequence-Level Semantic Gluon Transformer: Training and Verification Suite.

Demonstrates:
  1. Sequence-level token embedding via FastEmbed ONNX (384-dimensional dense vectors).
  2. Multi-Head Semantic Gluon Attention over sequences [B, N, 384].
  3. Ribosomal Exon Splicing: Strict suppression of conversational fluff introns.
  4. Physical Heads: Causal Valence, Cornell Confinement, 7-Planes Gauge Friction, Optical Luminescence.
  5. Vectorized Sparse Splicing Speedup Benchmark.
  6. Multi-epoch AdamW training with verified loss reduction.
"""

import sys
import os
import math
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

# Reconfigure stdout for utf-8
if sys.version_info >= (3, 7):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Ensure local path is accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from polytrope_layers import (
    FractalPolytropeTransformer,
    SemanticGluonAttention,
    SemanticGluonTransformerBlock
)
from fastembed import TextEmbedding

def main():
    print("=" * 80)
    print("SEQUENCE-LEVEL SEMANTIC GLUON TRANSFORMER: PYTORCH VERIFICATION SUITE")
    print("=" * 80)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device} | PyTorch Version: {torch.__version__}")

    # 1. Define synthetic document sequences with Exons (proof bedrock) vs Introns (fluff)
    documents = [
        # Document 1: Physical Water Logistics & Municipal Hydraulics
        [
            ("Municipal reservoir stores 500 megaliters behind reinforced concrete.", 1), # Exon
            ("So basically, you know, we were just chatting about water stuff.", 0),        # Intron
            ("Gravity-fed pressure drops 9.81 kilopascals per vertical meter of descent.", 1), # Exon
            ("Like, honestly, at the end of the day it is what it is.", 0),                 # Intron
            ("Pumping station consumes 450 kilowatt hours per megaliter lifted.", 1),      # Exon
            ("Well, to be fair, anyone could have guessed that would happen.", 0),          # Intron
            ("Chlorine dosing inactivates 99.99 percent of waterborne enteric pathogens.", 1), # Exon
            ("Anyway, let me just add some random filler before the conclusion.", 0),      # Intron
        ],
        # Document 2: Sovereign Energy & Synchronous Grid Dynamics
        [
            ("Turbine rotor spins at 3000 rpm synchronized to 50 hertz alternating current.", 1), # Exon
            ("I mean, honestly, it feels kind of cool to see large machinery.", 0),               # Intron
            ("Thermal inertia buffers frequency fluctuations within 0.05 hertz tolerance.", 1),   # Exon
            ("Just my personal two cents on the overall vibe of electricity.", 0),                # Intron
            ("High-voltage step-up transformer delivers 330 kilovolts onto the transmission line.", 1), # Exon
            ("Whatever you think about power grids, it is really something to ponder.", 0),      # Intron
            ("Protective circuit breakers isolate ground faults in 60 milliseconds.", 1),         # Exon
            ("Moving right along with more unnecessary conversational filler.", 0),              # Intron
        ]
    ]

    B = len(documents)
    N = len(documents[0])
    D = 384

    print(f"\n[Step 1/4] Embedding Document Tokens with FastEmbed ONNX ({B} docs x {N} tokens)...")
    embedder = TextEmbedding()

    all_texts = [text for doc in documents for text, _ in doc]
    raw_embeddings = list(embedder.embed(all_texts))
    embed_tensor = torch.tensor(np.array(raw_embeddings), dtype=torch.float32).view(B, N, D).to(device)

    # Ground truth exon mask (1 = Exon, 0 = Intron)
    exon_mask_list = [[label for _, label in doc] for doc in documents]
    exon_mask = torch.tensor(exon_mask_list, dtype=torch.float32).to(device)

    print(f"Embedding Tensor Shape: {embed_tensor.shape} (B={B}, N={N}, D={D})")
    print(f"Exon Mask Shape: {exon_mask.shape} (Active Exons: {int(exon_mask.sum().item())}/{B*N})")

    # 2. Initialize Model
    print("\n[Step 2/4] Initializing FractalPolytropeTransformer with Semantic Gluon Block...")
    model = FractalPolytropeTransformer(embed_dim=D, num_heads=6).to(device)
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total Trainable Parameters: {total_params:,}")

    # Forward pass demonstration
    outputs = model(embed_tensor, exon_mask=exon_mask, return_diagnostics=True)
    gluon_diag = outputs["gluon_diagnostics"]
    attn_weights = gluon_diag["attn_weights"] # [B, H, N, N]

    # Measure exon-to-intron attention leakage
    # Exons are at even indices (0, 2, 4, 6), Introns are at odd indices (1, 3, 5, 7)
    exon_indices = [0, 2, 4, 6]
    intron_indices = [1, 3, 5, 7]
    exon_to_intron_attn = attn_weights[:, :, exon_indices, :][:, :, :, intron_indices].mean().item()
    exon_to_exon_attn = attn_weights[:, :, exon_indices, :][:, :, :, exon_indices].mean().item()

    print(f"\nInitial Diagnostics:")
    print(f"  • Attended Embedding Shape: {outputs['attended_x'].shape}")
    print(f"  • Attention Tensor Shape:   {attn_weights.shape}")
    print(f"  • Base Coordinates Shape:   {outputs['base_coord'].shape}")
    print(f"  • Exon-to-Intron Leakage:   {exon_to_intron_attn:.8e} (Strict Zero: {exon_to_intron_attn < 1e-4})")
    print(f"  • Exon-to-Exon Attention:   {exon_to_exon_attn:.6f}")

    # 3. Vectorized Sparse Splicing Speedup Benchmark
    print("\n[Step 3/4] Vectorized Sparse Splicing Speedup Benchmark...")
    gluon_attn = model.gluon_block.attn

    # Warmup
    for _ in range(5):
        _ = gluon_attn(embed_tensor, exon_mask=exon_mask, return_diagnostics=False)
        _ = gluon_attn.forward_sparse_spliced(embed_tensor, exon_mask=exon_mask)

    # Time Dense
    t0 = time.perf_counter()
    for _ in range(50):
        dense_out = gluon_attn(embed_tensor, exon_mask=exon_mask, return_diagnostics=False)
    dense_time = (time.perf_counter() - t0) / 50 * 1000

    # Time Sparse
    t0 = time.perf_counter()
    for _ in range(50):
        sparse_out, theor_speedup = gluon_attn.forward_sparse_spliced(embed_tensor, exon_mask=exon_mask)
    sparse_time = (time.perf_counter() - t0) / 50 * 1000

    print(f"  • Dense Forward Latency:  {dense_time:.3f} ms")
    print(f"  • Spliced Sparse Latency: {sparse_time:.3f} ms")
    print(f"  • Wall-Clock Speedup:     {dense_time / max(sparse_time, 1e-5):.2f}x")
    print(f"  • Theoretical Quadratic Reduction: {theor_speedup:.2f}x")

    # 4. Multi-Epoch Training with Physical Losses
    print("\n[Step 4/4] Multi-Epoch AdamW Training on Sequence Data...")
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)

    # Target: Exons should have positive Causal Z (fruit) or negative Causal Z (root)
    # Physical target reconstruction
    target_embed = embed_tensor.clone()

    initial_loss = None
    final_loss = None

    for epoch in range(1, 16):
        optimizer.zero_grad()
        out = model(embed_tensor, exon_mask=exon_mask, return_diagnostics=True)
        diag = out["gluon_diagnostics"]

        # Reconstruction task loss on exons only
        recon_loss = F.mse_loss(out["attended_x"] * exon_mask.unsqueeze(-1), target_embed * exon_mask.unsqueeze(-1))

        # Auxiliary physical loss
        aux_losses = gluon_attn.compute_auxiliary_losses(diag, target_exons=exon_mask)
        total_loss = recon_loss + 0.5 * aux_losses["total_aux_loss"]

        total_loss.backward()

        # Check gradients
        grad_norm = nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        if epoch == 1:
            initial_loss = total_loss.item()
        final_loss = total_loss.item()

        if epoch % 3 == 0 or epoch == 1:
            print(f"  Epoch {epoch:2d}/15 | Total Loss: {total_loss.item():.4f} | Recon: {recon_loss.item():.4f} | "
                  f"Valence: {aux_losses['valence_loss'].item():.4f} | Confinement: {aux_losses['confinement_loss'].item():.4f} | "
                  f"Grad Norm: {grad_norm:.4f}")

    loss_reduction = (initial_loss - final_loss) / initial_loss * 100
    print(f"\nOptimization Trajectory:")
    print(f"  • Initial Loss:   {initial_loss:.4f}")
    print(f"  • Final Loss:     {final_loss:.4f}")
    print(f"  • Loss Reduction: -{loss_reduction:.2f}%")

    # Final Verification Assertions
    assert exon_to_intron_attn < 1e-4, f"Intron leakage detected: {exon_to_intron_attn}"
    assert loss_reduction > 10.0, f"Insufficient loss reduction: {loss_reduction}%"
    print("\n" + "=" * 80)
    print("ALL SEQUENCE-LEVEL PYTORCH TESTS PASSED: STRICT INVARIANTS CONFIRMED!")
    print("=" * 80)

if __name__ == "__main__":
    main()
