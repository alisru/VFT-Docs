"""
Semantic Gluon Attention Layer (PyTorch)
Generation 7 Competitor 3: PyTorch Attention Arbiter (50% Male / 50% Female)

Architecture Specification:
    Pre-softmax modified attention logit matrix:
    S_{ij} = ( (Q_i K_j^T) / sqrt(d_k) + M_{ij}^{valence} - V_Cornell(r_{ij}) - Gamma_friction(P_i, P_j) ) * exp(-tau_{ij}) + M_{ij}^{splicing}
    Attention(Q, K, V) = softmax(S) V

Components:
    1. Multi-Head Q, K, V Projections (B x N x D -> B x H x N x d_k)
    2. Ribosomal Exon Splicing Mask (M_{ij}^{splicing}):
       Excises conversational filler introns, forcing quadratic attention onto coding exons.
       Supports dynamic learned exon gating and an explicit fast sparse sub-sequence execution path.
    3. Causal Valence Shell Matrix (M_{ij}^{valence}):
       Evaluates Ingress requirements B_i and Egress obligations F_j, penalizing unclosed/dangling claims.
    4. Cornell Confinement Potential (V_Cornell(r_{ij}) = -alpha_s / (r_{ij} + eps) + sigma * r_{ij}):
       Causal distance r_{ij} = |z_i - z_j| along the causal Z-axis. Provides short-range asymptotic
       freedom and long-range string confinement, flagging string snaps at r_c >= 1.529.
    5. 7-Planes Reality Gauge Friction (Gamma_friction(P_i, P_j)):
       Bilinear form P_i G P_j^T over the 7 Q-Planes (Q1..Q7), enforcing constructive geodesics
       and penalizing inverted leaps (e.g. Q4 -> Q3, Q7 -> Q5).
    6. Optical Attenuation Field (exp(-tau_{ij})):
       Modulates logits by semantic luminescence L = exp(-tau), dampening ungrounded assertion fog.
"""

from typing import Dict, Optional, Tuple, Union
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def build_canonical_gauge_friction_matrix() -> torch.Tensor:
    """
    Constructs the canonical 7x7 Gauge Friction Matrix Gamma(Q_p, Q_q)
    for the 7 Planes of Reality:
        0: Q1 Who (Metaphysical)
        1: Q2 What (Possible / +x)
        2: Q3 Where (Physical / -x)
        3: Q4 Why (Lyrical / +y)
        4: Q5 How (Logical / -y)
        5: Q6 Cause (Historical / +z)
        6: Q7 Effect (Emotive / -z)
    """
    G = torch.zeros(7, 7, dtype=torch.float32)
    # 3D spatial mapping of planes to calculate default cross-plane coordinate distance
    plane_coords = torch.tensor([
        [0.0, 0.0, 0.0],   # Q1: Driver / Origin
        [1.0, 0.0, 0.0],   # Q2: +x Lateral
        [-1.0, 0.0, 0.0],  # Q3: -x Lateral
        [0.0, 1.0, 0.0],   # Q4: +y Longitudinal
        [0.0, -1.0, 0.0],  # Q5: -y Longitudinal
        [0.0, 0.0, 1.0],   # Q6: +z Vertical
        [0.0, 0.0, -1.0],  # Q7: -z Vertical
    ], dtype=torch.float32)

    for p in range(7):
        for q in range(7):
            if p == q:
                G[p, q] = 0.5  # Low friction for intra-plane continuity
            else:
                dist = torch.norm(plane_coords[p] - plane_coords[q], p=1).item()
                G[p, q] = 1.0 + 0.25 * dist

    # Specific canonical overrides from specification:
    # Constructive Geodesic: Q3 (Physical) -> Q5 (Logical) -> Q4 (Lyrical) -> Q1 (Metaphysical)
    G[2, 4] = 0.8  # Q3 -> Q5
    G[4, 3] = 0.8  # Q5 -> Q4
    G[3, 0] = 0.8  # Q4 -> Q1

    # Inverted Leaps:
    G[3, 2] = 2.5  # Q4 -> Q3 (Asserting physical reality from lyrical metaphor)
    G[6, 4] = 2.4  # Q7 -> Q5 (Emotional outrage posing as formal proof)

    return G


class RibosomalSplicingGate(nn.Module):
    """
    Predicts exon vs intron classification probabilities for each token:
      exon_prob in [0, 1]
    Allows fast dynamic pruning of conversational filler.
    """
    def __init__(self, embed_dim: int = 384):
        super().__init__()
        self.gate = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.GELU(),
            nn.Linear(embed_dim // 4, 1),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: [B, N, D]
        Returns:
            exon_probs: [B, N] in [0, 1]
        """
        return self.gate(x).squeeze(-1)


class CausalValenceHead(nn.Module):
    """
    Computes Ingress (B_i, backward requirements) and Egress (F_j, forward obligations)
    vectors to ensure causal closure and penalize dangling claims.
    """
    def __init__(self, embed_dim: int = 384, valence_dim: int = 64):
        super().__init__()
        self.valence_dim = valence_dim
        self.ingress_proj = nn.Linear(embed_dim, valence_dim, bias=False)
        self.egress_proj = nn.Linear(embed_dim, valence_dim, bias=False)
        self.dangle_penalty_scale = nn.Parameter(torch.tensor(0.2))

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        x: [B, N, D]
        Returns:
            B_ingress: [B, N, valence_dim]
            F_egress:  [B, N, valence_dim]
            M_valence: [B, N, N] causal valence affinity matrix
        """
        B_ingress = self.ingress_proj(x)
        F_egress = self.egress_proj(x)

        # Scaled dot-product affinity between ingress of i and egress of j
        # M_ij = (B_i . F_j) / sqrt(d_v)
        M_raw = torch.bmm(B_ingress, F_egress.transpose(1, 2)) / math.sqrt(self.valence_dim)

        # Directional causal modulation: egress tokens j typically precede or coincide with ingress tokens i
        # We allow a smooth causal bias where j <= i has higher affinity
        seq_len = x.size(1)
        indices = torch.arange(seq_len, device=x.device)
        # causal_prior: 0 for j <= i, -0.5 for forward unverified leaps j > i
        causal_order = (indices.unsqueeze(0) - indices.unsqueeze(1))  # i - j
        causal_mask = torch.where(causal_order >= 0, torch.zeros_like(M_raw), -0.5 * torch.ones_like(M_raw))

        # Dangling claim penalty: ungrounded ingress requirement without preceding causal root
        dangle_scale = F.softplus(self.dangle_penalty_scale)
        open_bond_penalty = torch.norm(B_ingress, dim=-1, keepdim=True) * 0.05  # [B, N, 1]

        M_valence = M_raw + causal_mask - (dangle_scale * open_bond_penalty)
        return B_ingress, F_egress, M_valence


class CornellConfinementHead(nn.Module):
    """
    Computes the Cornell Confinement Potential along the causal Z-axis:
        V_Cornell(r_{ij}) = -alpha_s / (r_{ij} + eps) + sigma * r_{ij}
    Where r_{ij} = |z_i - z_j|.
    Detects string snapping when r_{ij} >= r_critical.
    """
    def __init__(
        self,
        embed_dim: int = 384,
        alpha_s: float = 0.35,
        sigma: float = 0.85,
        r_critical: float = 1.529,
        eps: float = 1e-4
    ):
        super().__init__()
        self.z_head = nn.Linear(embed_dim, 1)
        # Learnable or fixed parameters with physical defaults
        self.alpha_s = nn.Parameter(torch.tensor(alpha_s))
        self.sigma = nn.Parameter(torch.tensor(sigma))
        self.r_critical = r_critical
        self.eps = eps

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        x: [B, N, D]
        Returns:
            z: [B, N] causal positions
            V_cornell: [B, N, N] Cornell potential
            snapped_mask: [B, N, N] boolean tensor of snapped strings (r >= r_c)
        """
        z = self.z_head(x).squeeze(-1)  # [B, N]
        r_ij = torch.abs(z.unsqueeze(2) - z.unsqueeze(1))  # [B, N, N]

        # Enforce positivity on coupling constants
        alpha = F.relu(self.alpha_s) + 1e-5
        sig = F.relu(self.sigma) + 1e-5

        # V_Cornell = -alpha / (r + eps) + sigma * r
        coulomb = -alpha / (r_ij + self.eps)
        string_tension = sig * r_ij
        V_cornell = coulomb + string_tension

        snapped_mask = (r_ij >= self.r_critical)
        return z, V_cornell, snapped_mask


class GaugeFrictionHead(nn.Module):
    """
    Maps tokens to the 7 Planes of Reality (Q1..Q7) and calculates
    non-commutative gauge friction Gamma_friction(P_i, P_j) = P_i G P_j^T.
    """
    def __init__(self, embed_dim: int = 384, num_planes: int = 7):
        super().__init__()
        self.num_planes = num_planes
        self.plane_classifier = nn.Linear(embed_dim, num_planes)
        # Initialize with canonical friction matrix
        canonical_G = build_canonical_gauge_friction_matrix()
        self.friction_tensor = nn.Parameter(canonical_G)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        x: [B, N, D]
        Returns:
            plane_probs: [B, N, 7]
            gamma_friction: [B, N, N]
        """
        plane_logits = self.plane_classifier(x)
        plane_probs = F.softmax(plane_logits, dim=-1)  # [B, N, 7]

        # Gamma_ij = P_i * G * P_j^T
        # Batch bilinear: einsum('bip,pq,bjq->bij')
        G = F.relu(self.friction_tensor)  # Friction is strictly non-negative
        gamma_friction = torch.einsum('bip,pq,bjq->bij', plane_probs, G, plane_probs)

        return plane_probs, gamma_friction


class LuminescenceAttenuationHead(nn.Module):
    """
    Calculates optical depth tau_{ij} and transmission factor exp(-tau_{ij})
    to dampen ungrounded assertion fog and amplify White Singlet proofs.
    """
    def __init__(self, embed_dim: int = 384, tau_0: float = 1.0):
        super().__init__()
        self.tau_0 = tau_0
        self.opacity_proj = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.GELU(),
            nn.Linear(embed_dim // 4, 1),
            nn.Softplus()
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        x: [B, N, D]
        Returns:
            tau_ij: [B, N, N] optical thickness
            luminescence: [B, N, N] transmission exp(-tau_ij)
        """
        # Node opacity [B, N]
        node_tau = self.opacity_proj(x).squeeze(-1)
        # Pairwise optical thickness: average of node opacities scaled by tau_0
        tau_ij = self.tau_0 * 0.5 * (node_tau.unsqueeze(2) + node_tau.unsqueeze(1))
        # Transmission / Luminescence: exp(-tau_ij) in (0, 1]
        luminescence = torch.exp(-tau_ij)
        return tau_ij, luminescence


class SemanticGluonAttention(nn.Module):
    """
    Semantic Gluon Attention Layer (nn.Module).
    Implements the full unified Gen 7 equation with Ribosomal Exon Splicing,
    Causal Valence Shells, Cornell Potential Confinement, 7-Planes Gauge Friction,
    and Optical Luminescence Attenuation.
    """
    def __init__(
        self,
        embed_dim: int = 384,
        num_heads: int = 6,
        dropout: float = 0.1,
        valence_dim: int = 64,
        alpha_s: float = 0.35,
        sigma: float = 0.85,
        r_critical: float = 1.529,
        tau_0: float = 1.0,
        splicing_threshold: float = 0.5
    ):
        super().__init__()
        assert embed_dim % num_heads == 0, f"embed_dim ({embed_dim}) must be divisible by num_heads ({num_heads})"
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.scale = 1.0 / math.sqrt(self.head_dim)
        self.splicing_threshold = splicing_threshold

        # Multi-Head Projections
        self.q_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.k_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.v_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.out_proj = nn.Linear(embed_dim, embed_dim, bias=True)
        self.attn_dropout = nn.Dropout(dropout)
        self.proj_dropout = nn.Dropout(dropout)

        # Physics Sub-Heads
        self.splicing_gate = RibosomalSplicingGate(embed_dim=embed_dim)
        self.valence_head = CausalValenceHead(embed_dim=embed_dim, valence_dim=valence_dim)
        self.confinement_head = CornellConfinementHead(
            embed_dim=embed_dim,
            alpha_s=alpha_s,
            sigma=sigma,
            r_critical=r_critical
        )
        self.gauge_head = GaugeFrictionHead(embed_dim=embed_dim, num_planes=7)
        self.luminescence_head = LuminescenceAttenuationHead(embed_dim=embed_dim, tau_0=tau_0)

        # Balancing scale parameters (learned)
        self.valence_weight = nn.Parameter(torch.tensor(0.3))
        self.cornell_weight = nn.Parameter(torch.tensor(0.5))
        self.friction_weight = nn.Parameter(torch.tensor(0.3))

    def compute_splicing_mask(
        self,
        exon_probs: torch.Tensor,
        external_exon_mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Computes the additive splicing mask M_{ij}^{splicing}:
            0.0 where both i and j are coding exons,
            -1e4 where either i or j is an intron.
        Returns:
            splicing_mask: [B, 1, N, N]
            binary_exon_mask: [B, N] (1 for exon, 0 for intron)
        """
        if external_exon_mask is not None:
            binary_mask = external_exon_mask.float()
        else:
            binary_mask = (exon_probs >= self.splicing_threshold).float()

        # Both i and j must be exons: exon_pair = binary_mask_i * binary_mask_j
        exon_pair = binary_mask.unsqueeze(2) * binary_mask.unsqueeze(1)  # [B, N, N]

        # In case an entire row or sequence is marked intron, prevent all -inf
        # by ensuring each token can at least attend to itself
        diag_identity = torch.eye(binary_mask.size(1), device=binary_mask.device).unsqueeze(0)
        valid_attend = torch.clamp(exon_pair + diag_identity, max=1.0)

        splicing_mask = torch.where(valid_attend > 0.5, 0.0, -1e4)
        return splicing_mask.unsqueeze(1), binary_mask

    def forward(
        self,
        x: torch.Tensor,
        exon_mask: Optional[torch.Tensor] = None,
        return_diagnostics: bool = True
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, Dict[str, torch.Tensor]]]:
        """
        Forward execution of SemanticGluonAttention.

        Args:
            x: Input sequence tensor of shape [B, N, D]
            exon_mask: Optional external binary/boolean mask of shape [B, N] (1=exon, 0=intron)
            return_diagnostics: If True, returns a dict of diagnostic physical tensors

        Returns:
            output: Attended representation of shape [B, N, D]
            diagnostics: (Optional) dict containing attention matrices and physical states
        """
        B, N, D = x.shape

        # 1. Standard Multi-Head Q, K, V Projections
        # [B, N, D] -> [B, N, H, d_k] -> [B, H, N, d_k]
        q = self.q_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)

        # Scaled dot-product baseline: S_base = (Q K^T) / sqrt(d_k) -> [B, H, N, N]
        s_base = torch.matmul(q, k.transpose(-2, -1)) * self.scale

        # 2. Layer 1: Ribosomal Exon Splicing Mask
        exon_probs = self.splicing_gate(x)  # [B, N]
        splicing_mask, binary_exon_mask = self.compute_splicing_mask(exon_probs, exon_mask)

        # 3. Layer 3: Causal Valence Shell Matrix
        B_ingress, F_egress, M_valence = self.valence_head(x)  # [B, N, N]
        M_valence_expanded = M_valence.unsqueeze(1)  # [B, 1, N, N]

        # 4. Layer 4: Cornell Confinement Potential
        z, V_cornell, snapped_mask = self.confinement_head(x)  # [B, N, N]
        V_cornell_expanded = V_cornell.unsqueeze(1)  # [B, 1, N, N]

        # 5. Layer 5: 7-Planes Reality Gauge Friction
        plane_probs, gamma_friction = self.gauge_head(x)  # [B, N, N]
        gamma_expanded = gamma_friction.unsqueeze(1)  # [B, 1, N, N]

        # 6. Layer 6: Optical Attenuation Field (Luminescence)
        tau_ij, luminescence = self.luminescence_head(x)  # [B, N, N]
        luminescence_expanded = luminescence.unsqueeze(1)  # [B, 1, N, N]

        # 7. Unified Logit Matrix Composition:
        # S_{ij} = ( s_base + M^{valence} - V_Cornell - Gamma_friction ) * exp(-tau) + M^{splicing}
        w_val = F.softplus(self.valence_weight)
        w_cor = F.softplus(self.cornell_weight)
        w_fric = F.softplus(self.friction_weight)

        s_physical = s_base + (w_val * M_valence_expanded) - (w_cor * V_cornell_expanded) - (w_fric * gamma_expanded)
        s_modulated = s_physical * luminescence_expanded
        s_final = s_modulated + splicing_mask

        # 8. Softmax & Output Projection
        attn_weights = F.softmax(s_final, dim=-1)
        attn_dropped = self.attn_dropout(attn_weights)

        # Context output: [B, H, N, d_k] -> [B, N, H, d_k] -> [B, N, D]
        context = torch.matmul(attn_dropped, v)
        context = context.transpose(1, 2).contiguous().view(B, N, D)
        output = self.proj_dropout(self.out_proj(context))

        if not return_diagnostics:
            return output

        diagnostics = {
            "attn_weights": attn_weights,          # [B, H, N, N]
            "s_final": s_final,                    # [B, H, N, N]
            "exon_probs": exon_probs,              # [B, N]
            "binary_exon_mask": binary_exon_mask,  # [B, N]
            "B_ingress": B_ingress,                # [B, N, d_v]
            "F_egress": F_egress,                  # [B, N, d_v]
            "M_valence": M_valence,                # [B, N, N]
            "z_causal": z,                         # [B, N]
            "V_cornell": V_cornell,                # [B, N, N]
            "snapped_mask": snapped_mask,          # [B, N, N]
            "plane_probs": plane_probs,            # [B, N, 7]
            "gamma_friction": gamma_friction,      # [B, N, N]
            "tau_ij": tau_ij,                      # [B, N, N]
            "luminescence": luminescence,          # [B, N, N]
        }
        return output, diagnostics

    def forward_sparse_spliced(
        self,
        x: torch.Tensor,
        exon_mask: torch.Tensor
    ) -> Tuple[torch.Tensor, float]:
        """
        High-efficiency Vectorized Sparse Ribosomal Splicing Forward Pass (Female Vector optimization).
        Physically extracts coding exons across the batch into a compact sub-tensor [B, K_max, D],
        runs multi-head attention in parallel over K_max <= N, and scatters outputs back.
        
        Args:
            x: Input sequence [B, N, D]
            exon_mask: Binary exon mask [B, N] (1 = coding exon, 0 = intron)

        Returns:
            output: Reconstructed sequence [B, N, D]
            theoretical_speedup: Ratio of quadratic attention pairs (N^2 / K_max^2)
        """
        B, N, D = x.shape
        device = x.device

        # Determine number of exons per sequence
        counts = (exon_mask > 0.5).sum(dim=1)  # [B]
        k_max = int(counts.max().item())

        if k_max == 0:
            return x.clone(), 1.0

        if k_max == N:
            # All tokens are exons; standard dense path
            out = self.forward(x, exon_mask=exon_mask, return_diagnostics=False)
            return out, 1.0

        # Vectorized gather of active exons into [B, K_max, D]
        # Sort mask descending to place exons at indices 0..counts[b]-1
        _, sorted_indices = torch.sort((exon_mask > 0.5).long(), dim=1, descending=True)
        exon_indices = sorted_indices[:, :k_max]  # [B, K_max]

        batch_idx = torch.arange(B, device=device).unsqueeze(1).expand(B, k_max)
        x_spliced = x[batch_idx, exon_indices]  # [B, K_max, D]

        # Sub-mask for valid exons in the compacted tensor
        compact_mask = torch.arange(k_max, device=device).unsqueeze(0).expand(B, k_max) < counts.unsqueeze(1)
        compact_mask = compact_mask.float()

        # Execute attention on the spliced compact sequence
        out_spliced = self.forward(x_spliced, exon_mask=compact_mask, return_diagnostics=False)

        # Reconstruct full sequence tensor
        output = torch.zeros_like(x)
        # Residual identity for excised non-coding introns
        output.copy_(x)
        output[batch_idx, exon_indices] = out_spliced

        theoretical_speedup = float(N * N) / max(float(k_max * k_max), 1.0)
        return output, theoretical_speedup

    def compute_auxiliary_losses(
        self,
        diagnostics: Dict[str, torch.Tensor],
        target_exons: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        Computes the balanced Gen 7 physical regularizations:
          1. valence_loss: Enforces egress claims F to be closed by downstream ingress B.
          2. confinement_loss: Penalizes attention across snapped flux strings (r >= r_c).
          3. gauge_friction_loss: Penalizes attention across high-friction inverted plane leaps.
          4. splicing_loss: Supervises exon detection if target_exons is given, or promotes sparsity.
        """
        attn = diagnostics["attn_weights"].mean(dim=1)  # Average over heads [B, N, N]
        snapped = diagnostics["snapped_mask"].float()   # [B, N, N]
        gamma = diagnostics["gamma_friction"]           # [B, N, N]
        exon_probs = diagnostics["exon_probs"]          # [B, N]

        # 1. Confinement Loss: Penalize high attention where strings snapped (hallucination suppression)
        confinement_loss = (attn * snapped).sum(dim=-1).mean()

        # 2. Gauge Friction Loss: Penalize high attention across inverted leaps (friction >= 2.0)
        high_friction_mask = (gamma >= 2.0).float()
        gauge_friction_loss = (attn * gamma * high_friction_mask).sum(dim=-1).mean()

        # 3. Causal Valence Loss: Egress obligations should be resolved
        F_norm = torch.norm(diagnostics["F_egress"], dim=-1)  # [B, N]
        # Attention received by token j from downstream tokens i >= j
        seq_len = attn.size(1)
        causal_triu = torch.triu(torch.ones(seq_len, seq_len, device=attn.device), diagonal=0)
        received_attn = (attn * causal_triu).sum(dim=1)  # [B, N]
        # Dangling penalty: large egress obligation but zero downstream attention
        valence_loss = (F_norm * torch.exp(-received_attn)).mean()

        # 4. Splicing Loss: Supervised or Sparsity
        if target_exons is not None:
            splicing_loss = F.binary_cross_entropy(exon_probs, target_exons.float())
        else:
            # Sparsity penalty: encourage identifying introns (target ~60% introns, 40% exons)
            splicing_loss = F.l1_loss(exon_probs.mean(), torch.tensor(0.4, device=exon_probs.device))

        total_aux = (
            1.5 * confinement_loss +
            1.0 * gauge_friction_loss +
            0.8 * valence_loss +
            0.5 * splicing_loss
        )

        return {
            "total_aux_loss": total_aux,
            "confinement_loss": confinement_loss,
            "gauge_friction_loss": gauge_friction_loss,
            "valence_loss": valence_loss,
            "splicing_loss": splicing_loss
        }


class SemanticGluonTransformerBlock(nn.Module):
    """
    Complete Transformer Block incorporating Semantic Gluon Attention,
    pre-LayerNorm, residual connections, and MLP feed-forward network.
    """
    def __init__(
        self,
        embed_dim: int = 384,
        num_heads: int = 6,
        mlp_ratio: float = 4.0,
        dropout: float = 0.1
    ):
        super().__init__()
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attn = SemanticGluonAttention(embed_dim=embed_dim, num_heads=num_heads, dropout=dropout)
        self.norm2 = nn.LayerNorm(embed_dim)

        hidden_dim = int(embed_dim * mlp_ratio)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, embed_dim),
            nn.Dropout(dropout)
        )

    def forward(
        self,
        x: torch.Tensor,
        exon_mask: Optional[torch.Tensor] = None,
        return_diagnostics: bool = False
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, Dict[str, torch.Tensor]]]:
        norm_x = self.norm1(x)
        if return_diagnostics:
            attn_out, diag = self.attn(norm_x, exon_mask=exon_mask, return_diagnostics=True)
            x = x + attn_out
            x = x + self.mlp(self.norm2(x))
            return x, diag
        else:
            attn_out = self.attn(norm_x, exon_mask=exon_mask, return_diagnostics=False)
            x = x + attn_out
            x = x + self.mlp(self.norm2(x))
            return x
