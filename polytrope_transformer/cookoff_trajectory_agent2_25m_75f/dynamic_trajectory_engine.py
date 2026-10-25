"""
Dynamic Trajectory Engine (PyTorch nn.Module)
Competitor 2: PyTorch Trajectory Matriarch (25% Male / 75% Female)

Specification Source of Truth:
    e:\\Vector Field Theory\\VFT Docs\\_VFT MD\\Physics\\Semantic_Gluon_and_Dynamic_Trajectory_Theory.md

Architecture:
    1. DynamicTrajectoryIntegrator:
       - Computes continuous trajectory sigma(t) = [c(t), p(t), r(t), g(t)]^T via projection heads.
       - Integrates path Sigma_D = integral_0^1 w(t) * sigma(t) dt with learned/attention topic weighting w_k(t).
       - Computes Inclusive-Exclusive Polarity iota_D in [-1, +1] and Connection Magnitude ||Sigma_D||.
    2. ComplexityWaveEstimator:
       - Computes instantaneous topical/modal entropy H(t) = - sum p_i log p_i across the trajectory.
       - Evaluates whether H(t) converges (shrinking entropy as concepts unify into axioms)
         or fragments (diverging entropy indicating breakdown).
    3. RibosomalReadingHead:
       - Continuous codon transcription head emitting Codon_i = <Q_i, M_i, iota_i, H_i>.
       - Concept Survival Rate tracker: measures survival of concepts introduced in Inclusive states
         against subsequent Reductive stress-tests.
    4. DerivationLawCompletenessLoss:
       - Differentiable loss detecting unsubstantiated leaps / 'maths without working out'.
       - Punishes Productive 'will be' assertions that lack necessary antecedent Constructive/Reductive/Regressive path integral.
    5. FourColoredGluonForces:
       - Implements full tensor field calculations for Red, Green, Blue, and Magenta forces connecting modal pairs.
    6. DynamicTrajectoryEngine:
       - High-level composite architecture integrating all 5 modules for end-to-end training and inference.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, NamedTuple

import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# Constants & Nomenclature
# ---------------------------------------------------------------------------
# The 8 Modal Boundary States across the 4 Quadrants:
# Top-Left:     Productive   (Solution + Active)         -> [can_be (inner), will_be (outer)]
# Top-Right:    Reductive    (Problem + Active)          -> [can't_be (inner), is_not (outer)]
# Bottom-Right: Regressive   (Problem + Counteractive)   -> [won't_be (inner), was_like (outer)]
# Bottom-Left:  Constructive (Solution + Counteractive)  -> [may_be (inner), is_like (outer)]

MODAL_NAMES: List[str] = [
    "will_be",   # 0: Outer Top-Left (Productive)
    "can_be",    # 1: Inner Top-Left (Productive)
    "can't_be",  # 2: Inner Top-Right (Reductive)
    "is_not",    # 3: Outer Top-Right (Reductive)
    "won't_be",  # 4: Inner Bottom-Right (Regressive)
    "was_like",  # 5: Outer Bottom-Right (Regressive)
    "is_like",   # 6: Outer Bottom-Left (Constructive)
    "may_be",    # 7: Inner Bottom-Left (Constructive)
]

ENGINE_NAMES: List[str] = [
    "Constructive",  # c(t): is_like / may_be
    "Productive",    # p(t): will_be / can_be
    "Reductive",     # r(t): can't_be / is_not
    "Regressive",    # g(t): won't_be / was_like
]

# Mapping matrix from 8 modals to 4 engines: E = M * Map_Matrix
# [8 -> 4]: Constructive (indices 6,7), Productive (0,1), Reductive (2,3), Regressive (4,5)
MODAL_TO_ENGINE_MAP = [
    [0, 1, 0, 0],  # 0: will_be   -> Productive
    [0, 1, 0, 0],  # 1: can_be    -> Productive
    [0, 0, 1, 0],  # 2: can't_be  -> Reductive
    [0, 0, 1, 0],  # 3: is_not    -> Reductive
    [0, 0, 0, 1],  # 4: won't_be  -> Regressive
    [0, 0, 0, 1],  # 5: was_like  -> Regressive
    [1, 0, 0, 0],  # 6: is_like   -> Constructive
    [1, 0, 0, 0],  # 7: may_be    -> Constructive
]


class Codon(NamedTuple):
    """Semantic DNA Codon at segment i."""
    Q: torch.Tensor       # [B, 4]: Engine distribution (Constructive, Productive, Reductive, Regressive)
    M: torch.Tensor       # [B, 8]: Modal state distribution
    iota: torch.Tensor    # [B, 1]: Instantaneous Inclusive-Exclusive polarity in [-1, +1]
    H: torch.Tensor       # [B, 1]: Instantaneous complexity / entropy


@dataclass
class TrajectoryConfig:
    """Configuration for Dynamic Trajectory and Gluon Reading Head."""
    embed_dim: int = 384
    num_topics: int = 8
    num_modals: int = 8
    num_engines: int = 4
    hidden_dim: int = 128
    dropout: float = 0.1
    # Numerical stability
    eps: float = 1e-6
    # Derivation Law weights
    derivation_gamma: float = 1.0
    weight_prod: float = 1.0
    weight_red: float = 0.8
    weight_reg: float = 0.8
    weight_const: float = 0.8
    # Color force gauge couplings
    g_red: float = 1.0
    g_green: float = 1.0
    g_blue: float = 1.0
    g_magenta: float = 1.0


# ---------------------------------------------------------------------------
# 1. Four Colored Gluon Forces (Gauge Fields)
# ---------------------------------------------------------------------------
class FourColoredGluonForces(nn.Module):
    """
    Computes full tensor field calculations for Red, Green, Blue, and Magenta forces
    connecting corresponding modal pairs on the Relativity Map.

    Paths & Physical Meanings:
      - Red Force: Active Opposition & Exclusion Strain
          Pair 1: will_be (0) <--> can't_be (2)
          Pair 2: is_like (6) <--> won't_be (4)
      - Green Force: Possibility Testing & Negation Resolution
          Pair 1: can_be (1) <--> is_not (3)
          Pair 2: may_be (7) <--> was_like (5)
      - Blue Force: Affirmative Realization & Exclusion Pinning
          Pair 1: will_be (0) --> may_be (7)
          Pair 2: won't_be (4) --> is_not (3)
      - Magenta Force: Analogical Elevation & Impossibility Locking
          Pair 1: is_like (6) --> can_be (1)
          Pair 2: was_like (5) --> can't_be (2)
    """

    def __init__(self, config: TrajectoryConfig):
        super().__init__()
        self.config = config
        
        # Learnable gauge coupling scalars
        self.g_red = nn.Parameter(torch.tensor(config.g_red, dtype=torch.float32))
        self.g_green = nn.Parameter(torch.tensor(config.g_green, dtype=torch.float32))
        self.g_blue = nn.Parameter(torch.tensor(config.g_blue, dtype=torch.float32))
        self.g_magenta = nn.Parameter(torch.tensor(config.g_magenta, dtype=torch.float32))

        # Learnable bilinear interaction kernels over hidden representation [D x D]
        self.kernel_red = nn.Linear(config.embed_dim, config.embed_dim, bias=False)
        self.kernel_green = nn.Linear(config.embed_dim, config.embed_dim, bias=False)
        self.kernel_blue = nn.Linear(config.embed_dim, config.embed_dim, bias=False)
        self.kernel_magenta = nn.Linear(config.embed_dim, config.embed_dim, bias=False)

    def forward(
        self,
        modals: torch.Tensor,
        x: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        Args:
            modals: [B, N, 8] modal state probabilities or activations.
            x: Optional hidden states [B, N, D] for bilinear gauge field interactions.
        Returns:
            Dictionary of scalar and trajectory tension fields:
                - f_red: [B, N] instantaneous red strain
                - f_green: [B, N] instantaneous green tension
                - f_blue: [B, N] instantaneous blue tension
                - f_magenta: [B, N] instantaneous magenta tension
                - T_red: [B, N, N] non-local red shear field (if x provided)
                - T_green, T_blue, T_magenta
                - total_color_strain: [B, N] sum of all 4 color fields
        """
        B, N, _ = modals.shape

        m_will_be = modals[..., 0]   # Outer Top-Left
        m_can_be = modals[..., 1]    # Inner Top-Left
        m_cant_be = modals[..., 2]   # Inner Top-Right
        m_is_not = modals[..., 3]    # Outer Top-Right
        m_wont_be = modals[..., 4]   # Inner Bottom-Right
        m_was_like = modals[..., 5]  # Outer Bottom-Right
        m_is_like = modals[..., 6]   # Outer Bottom-Left
        m_may_be = modals[..., 7]    # Inner Bottom-Left

        # 1. 🔴 RED FORCE: will_be <-> can't_be AND is_like <-> won't_be
        f_red = F.softplus(self.g_red) * (
            m_will_be * m_cant_be + m_is_like * m_wont_be
        )

        # 2. 🟢 GREEN FORCE: can_be <-> is_not AND may_be <-> was_like
        f_green = F.softplus(self.g_green) * (
            m_can_be * m_is_not + m_may_be * m_was_like
        )

        # 3. 🔵 BLUE FORCE: will_be -> may_be AND won't_be -> is_not
        f_blue = F.softplus(self.g_blue) * (
            m_will_be * m_may_be + m_wont_be * m_is_not
        )

        # 4. 🟣 MAGENTA FORCE: is_like -> can_be AND was_like -> can't_be
        f_magenta = F.softplus(self.g_magenta) * (
            m_is_like * m_can_be + m_was_like * m_cant_be
        )

        total_color_strain = f_red + f_green + f_blue + f_magenta

        results = {
            "f_red": f_red,
            "f_green": f_green,
            "f_blue": f_blue,
            "f_magenta": f_magenta,
            "total_color_strain": total_color_strain,
        }

        # Optional full bilinear 2D pairwise interaction field across positions t1 and t2
        if x is not None:
            # Pairwise outer product over sequence positions
            # Red: will_be(t1) * can't_be(t2) modulated by bilinear latent projection
            k_x_red = self.kernel_red(x)       # [B, N, D]
            latent_red = torch.bmm(k_x_red, x.transpose(1, 2)) / math.sqrt(self.config.embed_dim)  # [B, N, N]
            pair_red = torch.bmm(m_will_be.unsqueeze(-1), m_cant_be.unsqueeze(1)) + \
                       torch.bmm(m_is_like.unsqueeze(-1), m_wont_be.unsqueeze(1))
            T_red = F.softplus(self.g_red) * pair_red * torch.sigmoid(latent_red)

            k_x_green = self.kernel_green(x)
            latent_green = torch.bmm(k_x_green, x.transpose(1, 2)) / math.sqrt(self.config.embed_dim)
            pair_green = torch.bmm(m_can_be.unsqueeze(-1), m_is_not.unsqueeze(1)) + \
                         torch.bmm(m_may_be.unsqueeze(-1), m_was_like.unsqueeze(1))
            T_green = F.softplus(self.g_green) * pair_green * torch.sigmoid(latent_green)

            k_x_blue = self.kernel_blue(x)
            latent_blue = torch.bmm(k_x_blue, x.transpose(1, 2)) / math.sqrt(self.config.embed_dim)
            pair_blue = torch.bmm(m_will_be.unsqueeze(-1), m_may_be.unsqueeze(1)) + \
                        torch.bmm(m_wont_be.unsqueeze(-1), m_is_not.unsqueeze(1))
            T_blue = F.softplus(self.g_blue) * pair_blue * torch.sigmoid(latent_blue)

            k_x_magenta = self.kernel_magenta(x)
            latent_magenta = torch.bmm(k_x_magenta, x.transpose(1, 2)) / math.sqrt(self.config.embed_dim)
            pair_magenta = torch.bmm(m_is_like.unsqueeze(-1), m_can_be.unsqueeze(1)) + \
                           torch.bmm(m_was_like.unsqueeze(-1), m_cant_be.unsqueeze(1))
            T_magenta = F.softplus(self.g_magenta) * pair_magenta * torch.sigmoid(latent_magenta)

            # Include non-local gauge tensor field projections in total color strain
            tensor_field_mean = (
                T_red.mean(dim=-1) +
                T_green.mean(dim=-1) +
                T_blue.mean(dim=-1) +
                T_magenta.mean(dim=-1)
            )
            total_color_strain = total_color_strain + 0.1 * tensor_field_mean
            results["total_color_strain"] = total_color_strain

            results.update({
                "T_red": T_red,
                "T_green": T_green,
                "T_blue": T_blue,
                "T_magenta": T_magenta,
            })

        return results


# ---------------------------------------------------------------------------
# 2. Dynamic Trajectory Integrator
# ---------------------------------------------------------------------------
class DynamicTrajectoryIntegrator(nn.Module):
    """
    Computes continuous trajectory sigma(t) = [c(t), p(t), r(t), g(t)]^T via projection heads,
    and integrates path Sigma_D = integral_0^1 w(t) * sigma(t) dt.
    Computes Inclusive-Exclusive Polarity iota_D in [-1, +1] and Connection Magnitude ||Sigma_D||.
    """

    def __init__(self, config: TrajectoryConfig):
        super().__init__()
        self.config = config

        # Topic attention projection head: X -> w_k(t)
        self.topic_head = nn.Sequential(
            nn.Linear(config.embed_dim, config.hidden_dim),
            nn.GELU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_dim, config.num_topics),
        )

        # Modal projection head: X -> 8 Modals
        self.modal_head = nn.Sequential(
            nn.Linear(config.embed_dim, config.hidden_dim),
            nn.GELU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_dim, config.num_modals),
        )

        # Direct 4-Engine Charge head: X -> [c(t), p(t), r(t), g(t)]
        self.engine_head = nn.Sequential(
            nn.Linear(config.embed_dim, config.hidden_dim),
            nn.GELU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_dim, config.num_engines),
        )

        # Buffer for modal-to-engine projection matrix [8, 4]
        self.register_buffer(
            "modal_to_engine",
            torch.tensor(MODAL_TO_ENGINE_MAP, dtype=torch.float32)
        )

    def forward(
        self,
        x: torch.Tensor,
        time_grid: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        Args:
            x: [B, N, D] hidden representations of sequence segments.
            time_grid: Optional [N] or [B, N] normalized time coordinates in [0, 1].
        Returns:
            Dictionary containing:
                - sigma: [B, N, 4] instantaneous engine charges [c(t), p(t), r(t), g(t)]
                - modals: [B, N, 8] modal probabilities
                - topic_weights: [B, N, K] topic attention weights w_k(t)
                - Sigma_D_topics: [B, K, 4] integrated path tensor per topic
                - Sigma_D: [B, 4] overall document trajectory integral
                - polarity_topics: [B, K] Inclusive-Exclusive polarity per topic in [-1, +1]
                - polarity_D: [B] overall Inclusive-Exclusive polarity in [-1, +1]
                - magnitude_topics: [B, K] connection magnitude per topic ||Sigma_{D,k}||
                - magnitude_D: [B] overall connection magnitude ||Sigma_D||
        """
        B, N, D = x.shape
        eps = self.config.eps

        # 1. Normalized continuous time grid t in [0, 1]
        if time_grid is None:
            # Uniform spacing across N points
            t = torch.linspace(0.0, 1.0, N, device=x.device, dtype=x.dtype)
            t = t.unsqueeze(0).expand(B, N)  # [B, N]
        elif time_grid.dim() == 1:
            t = time_grid.unsqueeze(0).expand(B, N)
        else:
            t = time_grid

        # 2. Topic Attention Weights w_k(t) >= 0 (normalized over topics via softmax)
        topic_logits = self.topic_head(x)  # [B, N, K]
        topic_weights = F.softmax(topic_logits, dim=-1)  # [B, N, K], sum_k w_k(t) = 1.0

        # 3. Modal probabilities across the 8 Boundary States
        modal_logits = self.modal_head(x)  # [B, N, 8]
        modals = F.softmax(modal_logits, dim=-1)  # [B, N, 8]

        # 4. Instantaneous Engine Charge Vector sigma(t) = [c(t), p(t), r(t), g(t)]^T
        # Fuse direct engine head (softplus for non-negative physical charge) with modal aggregation
        direct_engine_charge = F.softplus(self.engine_head(x))  # [B, N, 4]
        modal_engine_charge = torch.matmul(modals, self.modal_to_engine)  # [B, N, 4]
        # Synergistic blend ensures both direct charge learning and modal consistency
        sigma = direct_engine_charge * 0.5 + modal_engine_charge * 0.5  # [B, N, 4]

        # 5. Path Integral using Trapezoidal Rule:
        # Integral_0^1 w_k(t) * sigma(t) dt
        # dt between successive steps:
        dt = t[:, 1:] - t[:, :-1]  # [B, N-1]
        dt = dt.unsqueeze(-1)      # [B, N-1, 1]

        # Topic-specific integrand: w_k(t) * sigma_j(t) -> [B, N, K, 4]
        integrand_k = topic_weights.unsqueeze(-1) * sigma.unsqueeze(-2)  # [B, N, K, 4]
        trap_k = 0.5 * (integrand_k[:, :-1, :, :] + integrand_k[:, 1:, :, :])  # [B, N-1, K, 4]
        Sigma_D_topics = torch.sum(trap_k * dt.unsqueeze(-1), dim=1)  # [B, K, 4]

        # Document-level integrand: sigma(t) -> [B, N, 4]
        trap_doc = 0.5 * (sigma[:, :-1, :] + sigma[:, 1:, :])  # [B, N-1, 4]
        Sigma_D = torch.sum(trap_doc * dt, dim=1)  # [B, 4]

        # 6. Inclusive-Exclusive Polarity Operator:
        # iota = (Inclusive - Exclusive) / (Inclusive + Exclusive)
        # Inclusive = C + P (Constructive + Productive)
        # Exclusive = R + G (Reductive + Regressive)
        C_k = Sigma_D_topics[..., 0]
        P_k = Sigma_D_topics[..., 1]
        R_k = Sigma_D_topics[..., 2]
        G_k = Sigma_D_topics[..., 3]

        I_k = C_k + P_k
        E_k = R_k + G_k
        polarity_topics = (I_k - E_k) / (I_k + E_k + eps)  # [B, K] in [-1, +1]

        C_D = Sigma_D[..., 0]
        P_D = Sigma_D[..., 1]
        R_D = Sigma_D[..., 2]
        G_D = Sigma_D[..., 3]

        I_D = C_D + P_D
        E_D = R_D + G_D
        polarity_D = (I_D - E_D) / (I_D + E_D + eps)  # [B] in [-1, +1]

        # 7. Connection Magnitude ||Sigma_D|| = sqrt(C^2 + P^2 + R^2 + G^2)
        magnitude_topics = torch.sqrt(C_k.pow(2) + P_k.pow(2) + R_k.pow(2) + G_k.pow(2) + eps)  # [B, K]
        magnitude_D = torch.sqrt(C_D.pow(2) + P_D.pow(2) + R_D.pow(2) + G_D.pow(2) + eps)        # [B]

        return {
            "sigma": sigma,
            "modals": modals,
            "topic_weights": topic_weights,
            "Sigma_D_topics": Sigma_D_topics,
            "Sigma_D": Sigma_D,
            "polarity_topics": polarity_topics,
            "polarity_D": polarity_D,
            "magnitude_topics": magnitude_topics,
            "magnitude_D": magnitude_D,
            "time_grid": t,
        }


# ---------------------------------------------------------------------------
# 3. Complexity Wave Estimator
# ---------------------------------------------------------------------------
class ComplexityWaveEstimator(nn.Module):
    """
    Computes instantaneous topical and modal entropy H(t) = - sum p_i log p_i across the trajectory.
    Evaluates whether H(t) converges (shrinking entropy as concepts unify into axioms)
    or fragments (diverging entropy indicating breakdown).
    """

    def __init__(self, config: TrajectoryConfig):
        super().__init__()
        self.config = config

    def forward(
        self,
        topic_weights: torch.Tensor,
        modals: torch.Tensor,
        time_grid: torch.Tensor
    ) -> Dict[str, torch.Tensor]:
        """
        Args:
            topic_weights: [B, N, K] topic attention distribution.
            modals: [B, N, 8] modal state distribution.
            time_grid: [B, N] normalized time coordinates in [0, 1].
        Returns:
            Dictionary with:
                - H_topic: [B, N] instantaneous topic entropy
                - H_modal: [B, N] instantaneous modal entropy
                - H_wave: [B, N] combined complexity wave H(t)
                - entropy_slope: [B] linear drift slope beta (dH/dt)
                - is_convergent: [B] boolean mask (True if beta < 0, entropy converges)
                - convergence_ratio: [B] late / early entropy ratio ( < 1.0 is convergent)
                - delta_H: [B] H(1) - H(0)
        """
        eps = self.config.eps
        B, N, K = topic_weights.shape

        # Instantaneous Topic Entropy: -sum_k p_k * log(p_k)
        h_topic = -torch.sum(topic_weights * torch.log(topic_weights + eps), dim=-1)  # [B, N]
        h_topic_norm = h_topic / math.log(K)  # Normalized to [0, 1]

        # Instantaneous Modal Entropy: -sum_m p_m * log(p_m)
        h_modal = -torch.sum(modals * torch.log(modals + eps), dim=-1)  # [B, N]
        h_modal_norm = h_modal / math.log(self.config.num_modals)  # Normalized to [0, 1]

        # Composite Complexity Wave H(t): weighted blend of topical breadth & modal ambiguity
        H_wave = 0.5 * h_topic_norm + 0.5 * h_modal_norm  # [B, N]

        # Linear regression drift of H(t) over time t:
        # beta = Cov(t, H) / Var(t)
        t_mean = torch.mean(time_grid, dim=-1, keepdim=True)  # [B, 1]
        H_mean = torch.mean(H_wave, dim=-1, keepdim=True)     # [B, 1]

        t_diff = time_grid - t_mean  # [B, N]
        H_diff = H_wave - H_mean     # [B, N]

        cov_t_H = torch.sum(t_diff * H_diff, dim=-1)         # [B]
        var_t = torch.sum(t_diff.pow(2), dim=-1) + eps      # [B]
        entropy_slope = cov_t_H / var_t                     # [B] (slope beta)

        # Early-stage vs. Late-stage entropy comparison
        n_third = max(1, N // 3)
        h_early = torch.mean(H_wave[:, :n_third], dim=-1)       # [B]
        h_late = torch.mean(H_wave[:, -n_third:], dim=-1)       # [B]

        convergence_ratio = h_late / (h_early + eps)            # [B]
        delta_H = H_wave[:, -1] - H_wave[:, 0]                 # [B]

        # Differentiable convergence indicator (smooth sigmoid gate on -beta)
        convergence_score = torch.sigmoid(-5.0 * entropy_slope) # Near 1 when slope is negative

        return {
            "H_topic": h_topic,
            "H_modal": h_modal,
            "H_wave": H_wave,
            "entropy_slope": entropy_slope,
            "is_convergent": entropy_slope < 0.0,
            "convergence_ratio": convergence_ratio,
            "convergence_score": convergence_score,
            "delta_H": delta_H,
            "h_early": h_early,
            "h_late": h_late,
        }


# ---------------------------------------------------------------------------
# 4. Ribosomal Reading Head (Codon Transcription & Concept Survival Tracker)
# ---------------------------------------------------------------------------
class RibosomalReadingHead(nn.Module):
    """
    Continuous codon transcription head emitting Codon_i = <Q_i, M_i, iota_i, H_i>.
    Also includes a differentiable Concept Survival Rate tracker:
    Measures the survival of concepts introduced in Inclusive states against
    subsequent Reductive stress-tests without falling into Regressive abandonment.
    """

    def __init__(self, config: TrajectoryConfig):
        super().__init__()
        self.config = config

    def forward(
        self,
        sigma: torch.Tensor,
        modals: torch.Tensor,
        topic_weights: torch.Tensor,
        H_wave: torch.Tensor,
        time_grid: torch.Tensor
    ) -> Dict[str, torch.Tensor]:
        """
        Args:
            sigma: [B, N, 4] instantaneous engine charges
            modals: [B, N, 8] modal probabilities
            topic_weights: [B, N, K] topic weights
            H_wave: [B, N] complexity wave
            time_grid: [B, N] time grid
        Returns:
            Dictionary containing:
                - codons: List of Codon namedtuples per step, or stacked tensors
                - Q_strand: [B, N, 4] Engine base strand
                - M_strand: [B, N, 8] Modal state strand
                - iota_strand: [B, N] Instantaneous polarity strand in [-1, +1]
                - H_strand: [B, N] Complexity strand
                - concept_survival_rate: [B] Concept Survival Rate S_survival in [0, 1]
                - concept_survival_per_topic: [B, K] per-topic survival scores
        """
        eps = self.config.eps
        B, N, _ = sigma.shape

        # Instantaneous engine distribution Q_i: normalized sigma(t)
        sigma_sum = torch.sum(sigma, dim=-1, keepdim=True) + eps
        Q_strand = sigma / sigma_sum  # [B, N, 4]

        # Instantaneous modal state M_i
        M_strand = modals  # [B, N, 8]

        # Instantaneous Inclusive-Exclusive polarity iota_i:
        # (c_i + p_i) - (r_i + g_i) / (c_i + p_i + r_i + g_i + eps)
        c_i = sigma[..., 0]
        p_i = sigma[..., 1]
        r_i = sigma[..., 2]
        g_i = sigma[..., 3]
        iota_strand = ((c_i + p_i) - (r_i + g_i)) / (c_i + p_i + r_i + g_i + eps)  # [B, N]

        # Complexity strand H_i
        H_strand = H_wave  # [B, N]

        # -------------------------------------------------------------------
        # Concept Survival Rate S_survival Tracker:
        # Measures what fraction of concepts introduced in Inclusive states
        # survive subsequent Reductive stress-tests without collapsing into Regressive dead-ends.
        # -------------------------------------------------------------------
        K = topic_weights.shape[-1]
        # Topic-level inclusive introduction: I_k(t) = w_k(t) * (c(t) + p(t))
        topic_inc = topic_weights * (c_i + p_i).unsqueeze(-1)  # [B, N, K]
        topic_red = topic_weights * r_i.unsqueeze(-1)           # [B, N, K]
        topic_reg = topic_weights * g_i.unsqueeze(-1)           # [B, N, K]
        topic_prod = topic_weights * p_i.unsqueeze(-1)          # [B, N, K]

        # Early half vs late half
        half = max(1, N // 2)
        # Introduction energy primarily in early/mid trajectory
        inc_intro = torch.sum(topic_inc[:, :half, :], dim=1) + eps  # [B, K]
        # Reductive stress test energy across entire trajectory
        red_stress = torch.sum(topic_red, dim=1) + eps              # [B, K]
        # Regressive decay energy
        reg_decay = torch.sum(topic_reg, dim=1)                     # [B, K]
        # Late productive realization energy
        prod_late = torch.sum(topic_prod[:, half:, :], dim=1) + eps # [B, K]

        # Survival factor per topic:
        # High when late productive exceeds regressive decay and regressive penalty is small
        reg_ratio = reg_decay / (red_stress + eps)
        retention = prod_late / (prod_late + reg_decay + eps)
        decay_discount = torch.exp(-torch.clamp(reg_ratio, 0.0, 5.0))
        survival_per_topic = retention * decay_discount  # [B, K] in [0, 1]

        # Weighted by total introduction mass of each concept
        intro_weights = inc_intro / torch.sum(inc_intro, dim=-1, keepdim=True)  # [B, K]
        concept_survival_rate = torch.sum(intro_weights * survival_per_topic, dim=-1)  # [B] in [0, 1]

        return {
            "Q_strand": Q_strand,
            "M_strand": M_strand,
            "iota_strand": iota_strand,
            "H_strand": H_strand,
            "concept_survival_rate": concept_survival_rate,
            "concept_survival_per_topic": survival_per_topic,
        }


# ---------------------------------------------------------------------------
# 5. Derivation Law Completeness Loss (Unearned Leap Detection)
# ---------------------------------------------------------------------------
class DerivationLawCompletenessLoss(nn.Module):
    """
    Differentiable loss detecting unsubstantiated leaps / 'maths without working out'.
    Punishes Productive 'will be' assertions that lack the necessary antecedent
    Constructive/Reductive/Regressive path integral, strictly grounded in the
    4 Operational Derivation Laws:

      Law I (Reductive Law):
        'If you want to define IS as something that can't be you must go through
         a reductive process using what it was like and can be opposing what its
         like until it's not'
        Target: can't_be
        Requires antecedent: was_like, can_be, is_like, is_not

      Law II (Productive Law):
        'If you want to define IS as something that will be you must go through
         a productive process using what is not and is like opposing what it
         was like until it can be'
        Target: will_be
        Requires antecedent: is_not, is_like, was_like, can_be

      Law III (Regressive Law):
        'If you want to define IS as something that wont be you must go through
         a regressive process using what it's not and what it's like to oppose
         what it can be until it was like'
        Target: won't_be
        Requires antecedent: is_not, is_like, can_be, was_like

      Law IV (Constructive Law):
        'If you want to define IS as something that may be is you must go through
         a constructive process using what it can be and was like until it is like'
        Target: may_be
        Requires antecedent: can_be, was_like, is_like
    """

    def __init__(self, config: TrajectoryConfig):
        super().__init__()
        self.config = config

    def _cumulative_antecedent_integral(
        self,
        modals: torch.Tensor,
        dt: torch.Tensor
    ) -> torch.Tensor:
        """
        Computes cumulative causal path integral up to time step i:
        A_m(t_i) = integral_0^{t_i} modals_m(tau) dtau.
        """
        B, N, M = modals.shape
        # Trapezoidal cumulative sums:
        # trap_step[:, i, :] = 0.5 * (modals[:, i, :] + modals[:, i+1, :]) * dt[:, i, :]
        trap_steps = 0.5 * (modals[:, :-1, :] + modals[:, 1:, :]) * dt  # [B, N-1, M]
        zero_init = torch.zeros(B, 1, M, device=modals.device, dtype=modals.dtype)
        cum_trap = torch.cumsum(trap_steps, dim=1)  # [B, N-1, M]
        antecedent = torch.cat([zero_init, cum_trap], dim=1)  # [B, N, M]
        return antecedent

    def forward(
        self,
        modals: torch.Tensor,
        time_grid: torch.Tensor
    ) -> Dict[str, torch.Tensor]:
        """
        Args:
            modals: [B, N, 8] modal state distributions
            time_grid: [B, N] normalized time grid
        Returns:
            Dictionary containing:
                - loss: Total Derivation Law Completeness Loss (scalar)
                - loss_prod: Productive Law leap penalty (Law II)
                - loss_red: Reductive Law leap penalty (Law I)
                - loss_reg: Regressive Law leap penalty (Law III)
                - loss_const: Constructive Law leap penalty (Law IV)
                - prod_leap_profile: [B, N] step-by-step unearned leap magnitude
        """
        eps = self.config.eps
        B, N, _ = modals.shape

        # Step differentials
        dt = (time_grid[:, 1:] - time_grid[:, :-1]).unsqueeze(-1)  # [B, N-1, 1]

        # Cumulative antecedent integrals for each modal state up to step t:
        antecedent = self._cumulative_antecedent_integral(modals, dt)  # [B, N, 8]

        A_will_be  = antecedent[..., 0]
        A_can_be   = antecedent[..., 1]
        A_cant_be  = antecedent[..., 2]
        A_is_not   = antecedent[..., 3]
        A_wont_be  = antecedent[..., 4]
        A_was_like = antecedent[..., 5]
        A_is_like  = antecedent[..., 6]
        A_may_be   = antecedent[..., 7]

        # Instantaneous claims at step t
        m_will_be  = modals[..., 0]
        m_cant_be  = modals[..., 2]
        m_wont_be  = modals[..., 4]
        m_may_be   = modals[..., 7]

        # -------------------------------------------------------------------
        # Law II: Productive Law (will_be requires is_not, is_like, was_like, can_be)
        # -------------------------------------------------------------------
        # Geometric mean of antecedent foundations
        # We add eps to prevent zero gradients, clamp to valid range
        prod_support = (
            torch.clamp(A_is_not, min=eps) *
            torch.clamp(A_is_like, min=eps) *
            torch.clamp(A_was_like, min=eps) *
            torch.clamp(A_can_be, min=eps)
        ).pow(0.25)  # [B, N]

        # Unearned leap occurs when assertion m_will_be(t) exceeds scaled antecedent support
        # Note: at t=0, prod_support is tiny, so declaring 'will_be' immediately at the start
        # without groundwork incurs maximum penalty!
        gamma = self.config.derivation_gamma
        prod_leap = F.relu(m_will_be - gamma * prod_support)  # [B, N]
        loss_prod = torch.mean(prod_leap.pow(2))

        # -------------------------------------------------------------------
        # Law I: Reductive Law (can't_be requires was_like, can_be, is_like, is_not)
        # -------------------------------------------------------------------
        red_support = (
            torch.clamp(A_was_like, min=eps) *
            torch.clamp(A_can_be, min=eps) *
            torch.clamp(A_is_like, min=eps) *
            torch.clamp(A_is_not, min=eps)
        ).pow(0.25)
        red_leap = F.relu(m_cant_be - gamma * red_support)
        loss_red = torch.mean(red_leap.pow(2))

        # -------------------------------------------------------------------
        # Law III: Regressive Law (won't_be requires is_not, is_like, can_be, was_like)
        # -------------------------------------------------------------------
        reg_support = (
            torch.clamp(A_is_not, min=eps) *
            torch.clamp(A_is_like, min=eps) *
            torch.clamp(A_can_be, min=eps) *
            torch.clamp(A_was_like, min=eps)
        ).pow(0.25)
        reg_leap = F.relu(m_wont_be - gamma * reg_support)
        loss_reg = torch.mean(reg_leap.pow(2))

        # -------------------------------------------------------------------
        # Law IV: Constructive Law (may_be requires can_be, was_like, is_like)
        # -------------------------------------------------------------------
        const_support = (
            torch.clamp(A_can_be, min=eps) *
            torch.clamp(A_was_like, min=eps) *
            torch.clamp(A_is_like, min=eps)
        ).pow(1.0 / 3.0)
        const_leap = F.relu(m_may_be - gamma * const_support)
        loss_const = torch.mean(const_leap.pow(2))

        # Total combined derivation completeness loss
        total_loss = (
            self.config.weight_prod * loss_prod +
            self.config.weight_red * loss_red +
            self.config.weight_reg * loss_reg +
            self.config.weight_const * loss_const
        )

        return {
            "loss": total_loss,
            "loss_prod": loss_prod,
            "loss_red": loss_red,
            "loss_reg": loss_reg,
            "loss_const": loss_const,
            "prod_leap_profile": prod_leap,
            "prod_support": prod_support,
        }


# ---------------------------------------------------------------------------
# 6. Full Dynamic Trajectory Engine (Composite End-to-End Module)
# ---------------------------------------------------------------------------
class DynamicTrajectoryEngine(nn.Module):
    """
    Complete end-to-end Dynamic Trajectory Engine binding:
      1. DynamicTrajectoryIntegrator
      2. ComplexityWaveEstimator
      3. RibosomalReadingHead
      4. FourColoredGluonForces
      5. DerivationLawCompletenessLoss
    """

    def __init__(self, config: Optional[TrajectoryConfig] = None):
        super().__init__()
        self.config = config or TrajectoryConfig()

        # Core submodules
        self.integrator = DynamicTrajectoryIntegrator(self.config)
        self.complexity_wave = ComplexityWaveEstimator(self.config)
        self.reading_head = RibosomalReadingHead(self.config)
        self.color_forces = FourColoredGluonForces(self.config)
        self.derivation_loss_fn = DerivationLawCompletenessLoss(self.config)

    def forward(
        self,
        x: torch.Tensor,
        time_grid: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        Executes complete trajectory pipeline over input embeddings.
        Args:
            x: [B, N, D] hidden document embeddings
            time_grid: Optional [N] or [B, N] normalized time coordinates in [0, 1]
        Returns:
            Rich diagnostic dictionary containing all trajectory, wave, codon,
            color force, and derivation metrics.
        """
        # 1. Continuous Path Integration
        traj = self.integrator(x, time_grid=time_grid)
        sigma = traj["sigma"]
        modals = traj["modals"]
        topic_weights = traj["topic_weights"]
        t = traj["time_grid"]

        # 2. Complexity Wave & Entropy Evaluation
        wave = self.complexity_wave(topic_weights, modals, t)
        H_wave = wave["H_wave"]

        # 3. Ribosomal Reading Head & Concept Survival
        ribosome = self.reading_head(sigma, modals, topic_weights, H_wave, t)

        # 4. Four Colored Gluon Gauge Forces
        forces = self.color_forces(modals, x=x)

        # 5. Derivation Law Completeness
        derivation = self.derivation_loss_fn(modals, t)

        # Consolidated output bundle
        output = {
            # Trajectory Integrals & Polarities
            "sigma": sigma,
            "modals": modals,
            "topic_weights": topic_weights,
            "Sigma_D_topics": traj["Sigma_D_topics"],
            "Sigma_D": traj["Sigma_D"],
            "polarity_topics": traj["polarity_topics"],
            "polarity_D": traj["polarity_D"],
            "magnitude_topics": traj["magnitude_topics"],
            "magnitude_D": traj["magnitude_D"],
            "time_grid": t,
            # Complexity Wave
            "H_topic": wave["H_topic"],
            "H_modal": wave["H_modal"],
            "H_wave": H_wave,
            "entropy_slope": wave["entropy_slope"],
            "is_convergent": wave["is_convergent"],
            "convergence_ratio": wave["convergence_ratio"],
            "convergence_score": wave["convergence_score"],
            "delta_H": wave["delta_H"],
            "h_early": wave["h_early"],
            "h_late": wave["h_late"],
            # Ribosomal DNA & Survival
            "Q_strand": ribosome["Q_strand"],
            "M_strand": ribosome["M_strand"],
            "iota_strand": ribosome["iota_strand"],
            "H_strand": ribosome["H_strand"],
            "concept_survival_rate": ribosome["concept_survival_rate"],
            "concept_survival_per_topic": ribosome["concept_survival_per_topic"],
            # Colored Forces
            "f_red": forces["f_red"],
            "f_green": forces["f_green"],
            "f_blue": forces["f_blue"],
            "f_magenta": forces["f_magenta"],
            "total_color_strain": forces["total_color_strain"],
            # Derivation Losses
            "derivation_loss": derivation["loss"],
            "loss_prod": derivation["loss_prod"],
            "loss_red": derivation["loss_red"],
            "loss_reg": derivation["loss_reg"],
            "loss_const": derivation["loss_const"],
            "prod_leap_profile": derivation["prod_leap_profile"],
        }

        # Include pairwise force fields if present
        if "T_red" in forces:
            output.update({
                "T_red": forces["T_red"],
                "T_green": forces["T_green"],
                "T_blue": forces["T_blue"],
                "T_magenta": forces["T_magenta"],
            })

        return output
