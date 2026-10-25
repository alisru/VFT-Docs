r"""
Dynamic Trajectory Engine & Ribosomal Reading Head (PyTorch)
Generation 7 Trajectory Cook-Off - Competitor 1 (Patriarch: 75% Male / 25% Female)
Strict Proof Invariants & Derivation Law Defense

Theoretical Source of Truth:
  e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\Semantic_Gluon_and_Dynamic_Trajectory_Theory.md

Physical & Operational Invariants:
  1. Instantaneous Gluon State Vector sigma(t) = [c(t), p(t), r(t), g(t)]^T in Delta^3 (4-simplex).
  2. Document Trajectory Path Integral Sigma_D = int_0^1 w(t) sigma(t) dt.
  3. Inclusive-Exclusive Polarity iota_D = ((C + P) - (R + G)) / (C + P + R + G + eps) in [-1, +1].
  4. Connection Magnitude ||Sigma_D|| = sqrt(C^2 + P^2 + R^2 + G^2).
  5. Ribosomal Reading Head Codon transcription: Codon_i = <Q_i, M_i, iota_i, H_i>.
  6. Derivation Law II Defense (Productive Law):
     "If you want to define IS as something that will be you must go through a productive process
      using what is not and is like opposing what it was like until it can be."
     Sharp differentiable insolvency detector: L_insolvency = ReLU(P_target - W_antecedent).
  7. Four Colored Gluon Force Gauges (Red, Green, Blue, Magenta).
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


# ==============================================================================
# MODAL & ENGINE CONSTANTS (The Relativity Map v5.0)
# ==============================================================================

# 4 Operational Engines (Tier 2 Inner Loop)
ENGINES = ["Constructive", "Productive", "Reductive", "Regressive"]
ENGINE_TO_IDX = {name: i for i, name in enumerate(ENGINES)}

# 8 Modal Boundary States (Tier 3 Dual Corner Nodes)
# [0] Constructive Outer: 'is like'
# [1] Constructive Inner: 'may be'
# [2] Productive Inner:   'can be'
# [3] Productive Outer:   'will be'
# [4] Reductive Inner:    'can't be'
# [5] Reductive Outer:    'is not'
# [6] Regressive Inner:   'won't be'
# [7] Regressive Outer:   'was like'
MODALS = [
    "is like",   # 0: C outer
    "may be",    # 1: C inner
    "can be",    # 2: P inner
    "will be",   # 3: P outer
    "can't be",  # 4: R inner
    "is not",    # 5: R outer
    "won't be",  # 6: G inner
    "was like",  # 7: G outer
]
MODAL_TO_IDX = {name: i for i, name in enumerate(MODALS)}

# Mapping from 8 Modals to 4 Engines:
MODAL_TO_ENGINE_MATRIX = torch.tensor([
    [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Constructive (C)
    [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # Productive (P)
    [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0],  # Reductive (R)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0],  # Regressive (G)
], dtype=torch.float32)


@dataclass
class SemanticCodon:
    """
    Semantic Codon emitted by the Ribosomal Reading Head at step i.
    Codon_i = <Q_i, M_i, iota_i, H_i>
    """
    step: int
    engine: str
    modal: str
    polarity: float
    entropy: float
    engine_probs: List[float]
    modal_probs: List[float]


class DynamicTrajectoryIntegrator(nn.Module):
    """
    Section 5: Dynamic Document Trajectories & Path Integral.
    
    Transforms token sequence representations X in R^[B, N, D] into:
      1. Instantaneous operational state sigma(t) = [c(t), p(t), r(t), g(t)]^T in R^[B, N, 4]
      2. Attention weights w(t) in R^[B, N] where sum_t w(t) = 1
      3. Path integral Sigma_D = sum_t w(t) * sigma(t) in R^[B, 4]
      4. Inclusive-Exclusive Polarity iota_D in [-1, +1]
      5. Connection Magnitude ||Sigma_D|| in R^+
      6. Spectral Phase hat(Sigma)_D in S^3
    """
    def __init__(
        self,
        embed_dim: int = 256,
        hidden_dim: Optional[int] = None,
        eps: float = 1e-7,
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim or embed_dim // 2
        self.eps = eps

        # Modal projection head (8 modal states)
        self.modal_head = nn.Sequential(
            nn.Linear(embed_dim, self.hidden_dim),
            nn.LayerNorm(self.hidden_dim),
            nn.GELU(),
            nn.Linear(self.hidden_dim, 8),
        )

        # Direct 4-engine projection head (working in tandem with modal pooling)
        self.engine_head = nn.Sequential(
            nn.Linear(embed_dim, self.hidden_dim),
            nn.LayerNorm(self.hidden_dim),
            nn.GELU(),
            nn.Linear(self.hidden_dim, 4),
        )

        # Instantaneous topical attention weight head w(t)
        self.attn_weight_head = nn.Sequential(
            nn.Linear(embed_dim, self.hidden_dim),
            nn.Tanh(),
            nn.Linear(self.hidden_dim, 1),
        )

        # Register modal-to-engine pooling buffer
        self.register_buffer("modal_to_engine", MODAL_TO_ENGINE_MATRIX)

    def forward(
        self,
        x: torch.Tensor,
        weights_override: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        B, N, D = x.shape

        # 1. Compute 8 modal probabilities
        modal_logits = self.modal_head(x)  # [B, N, 8]
        modal_probs = F.softmax(modal_logits, dim=-1)  # [B, N, 8]

        # 2. Derive instantaneous engine state sigma(t) = [c(t), p(t), r(t), g(t)]
        # Combines canonical modal pooling with direct engine projection
        pooled_engine = torch.matmul(modal_probs, self.modal_to_engine.t())  # [B, N, 4]
        direct_engine = F.softmax(self.engine_head(x), dim=-1)               # [B, N, 4]
        sigma_t = 0.5 * (pooled_engine + direct_engine)                      # [B, N, 4]

        # Instantaneous Inclusive-Exclusive Polarity iota(t)
        inc_t = sigma_t[..., 0] + sigma_t[..., 1]  # c + p
        exc_t = sigma_t[..., 2] + sigma_t[..., 3]  # r + g
        instantaneous_polarity = (inc_t - exc_t) / (inc_t + exc_t + self.eps)  # [B, N]

        # 3. Compute continuous attention weights w(t)
        if weights_override is not None:
            weights = weights_override / (weights_override.sum(dim=-1, keepdim=True) + self.eps)
        else:
            raw_weights = self.attn_weight_head(x).squeeze(-1)  # [B, N]
            weights = F.softmax(raw_weights, dim=-1)  # sum_t w(t) = 1.0

        # 4. Compute Path Integral: Sigma_D = sum_t w(t) * sigma(t)
        sigma_integrated = torch.bmm(weights.unsqueeze(1), sigma_t).squeeze(1)  # [B, 4]

        C = sigma_integrated[:, 0]
        P = sigma_integrated[:, 1]
        R = sigma_integrated[:, 2]
        G = sigma_integrated[:, 3]

        # 5. Global Inclusive-Exclusive Polarity:
        inc_total = C + P
        exc_total = R + G
        polarity = (inc_total - exc_total) / (inc_total + exc_total + self.eps)  # [B]

        # 6. Connection Magnitude: ||Sigma_D|| = sqrt(C^2 + P^2 + R^2 + G^2)
        magnitude = torch.sqrt(torch.sum(sigma_integrated ** 2, dim=-1) + self.eps)  # [B]

        # 7. Spectral Phase: unit operational direction
        spectral_phase = sigma_integrated / (magnitude.unsqueeze(-1) + self.eps)  # [B, 4]

        return {
            "modal_logits": modal_logits,
            "modal_probs": modal_probs,
            "sigma_t": sigma_t,
            "weights": weights,
            "sigma_integrated": sigma_integrated,
            "polarity": polarity,
            "magnitude": magnitude,
            "spectral_phase": spectral_phase,
            "instantaneous_polarity": instantaneous_polarity,
        }


class RibosomalReadingHead(nn.Module):
    """
    Section 6: Semantic DNA & The Ribosomal Reading Head.
    
    Steps sequentially across the token trajectory, transcribing:
      Codon_i = <Q_i, M_i, iota_i, H_i>
    
    Maintains the cumulative working-out ledger across time:
      Tracks cumulative antecedent coverage required by Derivation Law II:
        Productive tokens ('will be') MUST be preceded by:
          - Reductive ('is not')
          - Constructive ('is like')
          - Regressive ('was like')
    """
    def __init__(
        self,
        embed_dim: int = 256,
        eps: float = 1e-7,
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.eps = eps

        # Local complexity estimator head for Shannon entropy modulation H_i
        self.entropy_gate = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.GELU(),
            nn.Linear(embed_dim // 4, 1),
            nn.Sigmoid(),
        )

    def forward(
        self,
        trajectory_output: Dict[str, torch.Tensor],
        x: torch.Tensor,
    ) -> Dict[str, torch.Tensor]:
        modal_probs = trajectory_output["modal_probs"]  # [B, N, 8]
        sigma_t = trajectory_output["sigma_t"]          # [B, N, 4]
        polarity_t = trajectory_output["instantaneous_polarity"] # [B, N]
        B, N, _ = modal_probs.shape

        # 1. Compute Shannon entropy of modal distribution modulated by learned complexity gate:
        modal_log_probs = torch.log(modal_probs + self.eps)
        base_entropy = -torch.sum(modal_probs * modal_log_probs, dim=-1)  # [B, N]
        gate = self.entropy_gate(x).squeeze(-1)  # [B, N]
        shannon_entropy = base_entropy * (1.0 + 0.1 * gate)

        # 2. Build cumulative working-out ledger (causal / antecedent)
        # Shift by 1 step so token t only sees antecedent history s < t
        sigma_cumsum = torch.cumsum(sigma_t, dim=1)  # [B, N, 4]
        
        zeros_step = torch.zeros(B, 1, 4, device=sigma_t.device, dtype=sigma_t.dtype)
        antecedent_cumsum = torch.cat([zeros_step, sigma_cumsum[:, :-1, :]], dim=1)  # [B, N, 4]

        # Engine antecedents:
        C_prev = antecedent_cumsum[..., 0]  # Constructive
        P_prev = antecedent_cumsum[..., 1]  # Productive
        R_prev = antecedent_cumsum[..., 2]  # Reductive
        G_prev = antecedent_cumsum[..., 3]  # Regressive

        # Law II Antecedent Working-Out Coverage:
        # Balanced coverage of Constructive, Reductive, and Regressive antecedents
        antecedent_coverage_law2 = torch.minimum(
            torch.minimum(C_prev, R_prev),
            G_prev
        )  # [B, N]

        # Law I Antecedent Working-Out Coverage:
        antecedent_coverage_law1 = torch.minimum(
            torch.minimum(G_prev, P_prev),
            C_prev
        )  # [B, N]

        # Pack continuous codon tensor: [B, N, 14]
        codons_tensor = torch.cat([
            sigma_t,
            modal_probs,
            polarity_t.unsqueeze(-1),
            shannon_entropy.unsqueeze(-1),
        ], dim=-1)

        return {
            "codons_tensor": codons_tensor,
            "cumulative_working_out": antecedent_cumsum,
            "shannon_entropy": shannon_entropy,
            "antecedent_coverage_law2": antecedent_coverage_law2,
            "antecedent_coverage_law1": antecedent_coverage_law1,
        }

    @staticmethod
    def transcribe_discrete_codons(
        trajectory_output: Dict[str, torch.Tensor],
        reading_head_output: Dict[str, torch.Tensor],
        batch_idx: int = 0,
    ) -> List[SemanticCodon]:
        modal_probs = trajectory_output["modal_probs"][batch_idx].detach().cpu().numpy()
        sigma_t = trajectory_output["sigma_t"][batch_idx].detach().cpu().numpy()
        polarity = trajectory_output["instantaneous_polarity"][batch_idx].detach().cpu().numpy()
        entropy = reading_head_output["shannon_entropy"][batch_idx].detach().cpu().numpy()

        codons = []
        seq_len = modal_probs.shape[0]
        for t in range(seq_len):
            engine_idx = int(sigma_t[t].argmax())
            modal_idx = int(modal_probs[t].argmax())
            codon = SemanticCodon(
                step=t,
                engine=ENGINES[engine_idx],
                modal=MODALS[modal_idx],
                polarity=float(polarity[t]),
                entropy=float(entropy[t]),
                engine_probs=[float(v) for v in sigma_t[t]],
                modal_probs=[float(v) for v in modal_probs[t]],
            )
            codons.append(codon)
        return codons


class FourColoredGluonForces(nn.Module):
    """
    Section 4: The Four Colored Force Vectors (Gluon Gauge Fields).
    
    Calculates the 4 cross-quadrant binding forces mediating interactions:
      1. 🔴 Red Force (Active Opposition & Exclusion Strain):
         - Path A: 'will be' <---> 'can't be'
         - Path B: 'is like' <---> 'won't be'
      2. 🟢 Green Force (Possibility Testing & Negation Resolution):
         - Path A: 'can be' <---> 'is not'
         - Path B: 'may be' <---> 'was like'
      3. 🔵 Blue Force (Affirmative Realization & Exclusion Pinning):
         - Path A: 'will be' ---> 'may be'
         - Path B: 'won't be' ---> 'is not'
      4. 🟣 Magenta Force (Analogical Elevation & Impossibility Locking):
         - Path A: 'is like' ---> 'can be'
         - Path B: 'was like' ---> 'can't be'
    """
    def __init__(self, eps: float = 1e-7):
        super().__init__()
        self.eps = eps
        # Learnable coupling weights for the 4 gauge fields
        self.gauge_couplings = nn.Parameter(torch.ones(4))

    def forward(
        self,
        trajectory_output: Dict[str, torch.Tensor],
    ) -> Dict[str, torch.Tensor]:
        modal_probs = trajectory_output["modal_probs"]  # [B, N, 8]
        B, N, _ = modal_probs.shape

        m_is_like   = modal_probs[..., 0]  # C outer
        m_may_be    = modal_probs[..., 1]  # C inner
        m_can_be    = modal_probs[..., 2]  # P inner
        m_will_be   = modal_probs[..., 3]  # P outer
        m_cant_be   = modal_probs[..., 4]  # R inner
        m_is_not    = modal_probs[..., 5]  # R outer
        m_wont_be   = modal_probs[..., 6]  # G inner
        m_was_like  = modal_probs[..., 7]  # G outer

        def pair_field(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
            return torch.bmm(a.unsqueeze(-1), b.unsqueeze(1))

        # 1. 🔴 RED VECTORS
        red_pair = 0.5 * (
            pair_field(m_will_be, m_cant_be) + pair_field(m_cant_be, m_will_be) +
            pair_field(m_is_like, m_wont_be) + pair_field(m_wont_be, m_is_like)
        )  # [B, N, N]

        # 2. 🟢 GREEN VECTORS
        green_pair = 0.5 * (
            pair_field(m_can_be, m_is_not) + pair_field(m_is_not, m_can_be) +
            pair_field(m_may_be, m_was_like) + pair_field(m_was_like, m_may_be)
        )  # [B, N, N]

        # 3. 🔵 BLUE VECTORS
        blue_pair = 0.5 * (
            pair_field(m_will_be, m_may_be) + pair_field(m_wont_be, m_is_not)
        )  # [B, N, N]

        # 4. 🟣 MAGENTA VECTORS
        magenta_pair = 0.5 * (
            pair_field(m_is_like, m_can_be) + pair_field(m_was_like, m_cant_be)
        )  # [B, N, N]

        forces_pairwise = torch.stack([red_pair, green_pair, blue_pair, magenta_pair], dim=1)

        # Modulate by positive gauge couplings: F.softplus(gauge_couplings)
        couplings = F.softplus(self.gauge_couplings).view(1, 4, 1, 1)
        forces_modulated = forces_pairwise * couplings

        # Global integrated force across the sequence
        forces_global = torch.mean(forces_modulated, dim=(-2, -1))  # [B, 4]

        return {
            "forces_global": forces_global,
            "forces_pairwise": forces_modulated,
            "red_tension": forces_global[:, 0],
            "green_testing": forces_global[:, 1],
            "blue_realization": forces_global[:, 2],
            "magenta_elevation": forces_global[:, 3],
        }


class DerivationLawCompletenessLoss(nn.Module):
    """
    Section 3 & 6: Mathematical Detector of 'Maths Without Working Out'.
    
    Law II Defense (Productive Law):
      "If you want to define IS as something that will be you must go through a productive process
       using what is not and is like opposing what it was like until it can be."
      L_insolvency_law2(t) = ReLU(P_target(t) - kappa * antecedent_coverage_law2(t))
    
    Law I Defense (Reductive Law):
      "If you want to define IS as something that can't be you must go through a reductive process
       using what it was like and can be opposing what its like until it's not."
      L_insolvency_law1(t) = ReLU(R_target(t) - kappa * antecedent_coverage_law1(t))
    """
    def __init__(
        self,
        kappa: float = 1.0,
        alpha_law1: float = 0.0,
        use_modal_target: bool = True,
        reduction: str = "mean",
    ):
        super().__init__()
        self.kappa = kappa
        self.alpha_law1 = alpha_law1
        self.use_modal_target = use_modal_target
        self.reduction = reduction

    def forward(
        self,
        trajectory_output: Dict[str, torch.Tensor],
        reading_head_output: Dict[str, torch.Tensor],
    ) -> Dict[str, torch.Tensor]:
        sigma_t = trajectory_output["sigma_t"]          # [B, N, 4]
        modal_probs = trajectory_output["modal_probs"]  # [B, N, 8]
        coverage_law2 = reading_head_output["antecedent_coverage_law2"]  # [B, N]
        coverage_law1 = reading_head_output["antecedent_coverage_law1"]  # [B, N]

        effective_kappa = self.kappa

        if self.use_modal_target:
            p_target = modal_probs[..., 3] + 0.5 * modal_probs[..., 2]  # 'will be' + 0.5 * 'can be'
            r_target = modal_probs[..., 4] + 0.5 * modal_probs[..., 5]  # 'can't be' + 0.5 * 'is not'
        else:
            p_target = sigma_t[..., 1]
            r_target = sigma_t[..., 2]

        violation_law2 = F.relu(p_target - effective_kappa * coverage_law2)  # [B, N]
        violation_law1 = F.relu(r_target - effective_kappa * coverage_law1)  # [B, N]

        if self.reduction == "mean":
            loss_law2 = torch.mean(violation_law2)
            loss_law1 = torch.mean(violation_law1)
        elif self.reduction == "sum":
            loss_law2 = torch.sum(violation_law2)
            loss_law1 = torch.sum(violation_law1)
        else:
            loss_law2 = violation_law2
            loss_law1 = violation_law1

        total_loss = loss_law2 + self.alpha_law1 * loss_law1

        return {
            "loss_total": total_loss,
            "loss_law2_productive": loss_law2,
            "loss_law1_reductive": loss_law1,
            "token_violations_law2": violation_law2,
            "token_violations_law1": violation_law1,
        }


class UnifiedDynamicTrajectorySystem(nn.Module):
    """
    Unified end-to-end neural system orchestrating:
      1. DynamicTrajectoryIntegrator
      2. RibosomalReadingHead
      3. FourColoredGluonForces
      4. DerivationLawCompletenessLoss
    """
    def __init__(
        self,
        embed_dim: int = 256,
        kappa: float = 1.0,
        alpha_law1: float = 0.0,
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.integrator = DynamicTrajectoryIntegrator(embed_dim=embed_dim)
        self.reading_head = RibosomalReadingHead(embed_dim=embed_dim)
        self.gluon_forces = FourColoredGluonForces()
        self.insolvency_loss_fn = DerivationLawCompletenessLoss(
            kappa=kappa,
            alpha_law1=alpha_law1,
        )

    def forward(
        self,
        x: torch.Tensor,
        weights_override: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        traj_out = self.integrator(x, weights_override=weights_override)
        reading_out = self.reading_head(traj_out, x=x)
        forces_out = self.gluon_forces(traj_out)
        loss_out = self.insolvency_loss_fn(traj_out, reading_out)

        return {
            "trajectory": traj_out,
            "reading_head": reading_out,
            "gluon_forces": forces_out,
            "insolvency_loss": loss_out,
        }
