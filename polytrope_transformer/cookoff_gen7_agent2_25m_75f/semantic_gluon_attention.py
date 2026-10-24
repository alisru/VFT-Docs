"""
Semantic Gluon Attention (PyTorch nn.Module)
Generation 7 Competitor 2: PyTorch Attention Matriarch (25% Male / 75% Female)

Architecture Specification:
    Pre-softmax Attention Logit Matrix:
    S_ij = ((Q_i K_j^T / sqrt(d_k) + M_ij^valence - V_Cornell(r_ij) - Gamma_friction(P_i, P_j)) * exp(-tau_ij)) + M_ij^splicing
    Attention(Q, K, V) = softmax(S) V

Components:
    1. Multi-head Scaled Dot-Product Attention (Q, K, V projections).
    2. Ribosomal Exon Splicing Mask (M_ij^splicing) with continuous learned exon classification.
    3. Causal Valence Shell Matrix (M_ij^valence) modeling Ingress requirements B_i and Egress obligations F_j.
    4. Cornell Confinement Potential V_Cornell(r_ij) = -alpha_s / (r_ij + eps) + sigma * r_ij + V_snap(r_ij).
    5. 7-Planes Non-Commutative Gauge Friction Tensor Gamma_friction(P_i, P_j).
    6. Radiative Transfer Luminescence Attenuation Field exp(-tau_ij).
    7. Continuous 4-Modal Ray Projections (can_be, is_not, is_like, was_like) augmenting representation.
"""

import math
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class SemanticGluonConfig:
    """Configuration for Semantic Gluon Attention."""
    embed_dim: int = 384
    num_heads: int = 6
    head_dim: Optional[int] = None
    dropout: float = 0.1
    # Valence parameters
    valence_dim: int = 64
    alpha_valence: float = 0.75
    lambda_dangle: float = 0.25
    # Cornell Confinement parameters
    alpha_s: float = 0.35
    sigma: float = 0.85
    r_c: float = 1.529  # Critical string snapping radius
    sigma_snap: float = 4.0  # Snapping penalty stiffness
    cornell_epsilon: float = 1e-4
    # Gauge Friction parameters
    num_planes: int = 7
    friction_geodesic: float = 0.8
    friction_inverted_q4_q3: float = 2.5
    friction_inverted_q7_q5: float = 2.4
    friction_base: float = 1.0
    # Optical Attenuation / Luminescence parameters
    base_tau: float = 0.5
    max_tau: float = 4.0
    # Ribosomal Splicing parameters
    splicing_penalty: float = 1e4

    def __post_init__(self):
        if self.head_dim is None:
            assert self.embed_dim % self.num_heads == 0, (
                f"embed_dim ({self.embed_dim}) must be divisible by num_heads ({self.num_heads})"
            )
            self.head_dim = self.embed_dim // self.num_heads


class RibosomalExonSplicer(nn.Module):
    """
    Layer 1: Ribosomal Exon Splicing & De-Duplication.
    Distinguishes invariant mathematical/formal exons (coding) from conversational filler introns (non-coding).
    Produces splicing mask M_ij^splicing:
        M_ij = 0 if both i and j are exons, else -splicing_penalty.
    """
    def __init__(self, config: SemanticGluonConfig):
        super().__init__()
        self.config = config
        # Exon gating network: predicts continuous exon probability e_i in [0, 1]
        self.exon_gate = nn.Sequential(
            nn.Linear(config.embed_dim, config.embed_dim // 2),
            nn.GELU(),
            nn.Linear(config.embed_dim // 2, 1),
            nn.Sigmoid()
        )

    def forward(
        self,
        x: torch.Tensor,
        exon_mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: [B, N, D] token embeddings.
            exon_mask: Optional explicit ground truth / prior binary mask [B, N] (1 = exon, 0 = intron).
        Returns:
            splicing_mask: [B, 1, N, N] attention logit additive mask.
            exon_probs: [B, N] predicted exon probabilities.
        """
        B, N, _ = x.shape
        exon_probs = self.exon_gate(x).squeeze(-1)  # [B, N]

        if exon_mask is not None:
            # Gated combination: maintains gradient flow to exon_gate while enforcing hard prior
            effective_mask = exon_probs * exon_mask.float()
        else:
            effective_mask = exon_probs

        # Joint pair coding status: exon_pair[b, i, j] = mask[b, i] * mask[b, j]
        exon_pair = effective_mask.unsqueeze(2) * effective_mask.unsqueeze(1)  # [B, N, N]
        
        # When either token is an intron (pair close to 0), apply heavy negative penalty
        splicing_mask = (1.0 - exon_pair) * (-self.config.splicing_penalty)
        return splicing_mask.unsqueeze(1), exon_probs  # [B, 1, N, N], [B, N]


class CausalValenceShell(nn.Module):
    """
    Layer 3: Causal Valence Shell Matrix M_ij^valence.
    Enforces Ingress Requirements B_i and Egress Obligations F_j:
        M_ij^valence = alpha_v * (B_i^T F_j / sqrt(d_v)) * causal_factor - lambda_dangle * ungrounded_penalty
    """
    def __init__(self, config: SemanticGluonConfig):
        super().__init__()
        self.config = config
        self.valence_dim = config.valence_dim
        # Ingress Requirement projection (what token i needs from the past)
        self.ingress_proj = nn.Linear(config.embed_dim, self.valence_dim)
        # Egress Obligation projection (what token j promises to future tokens)
        self.egress_proj = nn.Linear(config.embed_dim, self.valence_dim)
        # Bond closure detector
        self.closure_gate = nn.Linear(config.embed_dim, 1)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Args:
            x: [B, N, D] sequence representations.
        Returns:
            valence_matrix: [B, 1, N, N] pre-softmax modulation matrix.
            ingress_vecs: [B, N, valence_dim]
            egress_vecs: [B, N, valence_dim]
        """
        B, N, _ = x.shape
        ingress = self.ingress_proj(x)  # B_i [B, N, d_v]
        egress = self.egress_proj(x)    # F_j [B, N, d_v]

        # Scaled dot-product between ingress requirements and egress obligations
        # [B, N, d_v] x [B, d_v, N] -> [B, N, N]
        valence_couplings = torch.bmm(ingress, egress.transpose(1, 2)) / math.sqrt(self.valence_dim)

        # Causal temporal decay / directionality:
        # A claim i can only be grounded by past assertions j <= i
        idx = torch.arange(N, device=x.device)
        causal_rel = (idx.unsqueeze(1) - idx.unsqueeze(0)).float()  # i - j
        causal_mask = (causal_rel >= 0).float().unsqueeze(0)  # [1, N, N]

        # Open bond penalty from closure gate: delta_open_bond(i) = 1.0 - sigmoid(closure_gate(x_i))
        closure_prob = torch.sigmoid(self.closure_gate(x)).squeeze(-1)  # [B, N]
        open_bond = (1.0 - closure_prob).unsqueeze(2)  # [B, N, 1]

        # Penalize reverse non-causal claims looking into ungrounded future
        dangling_penalty = F.relu(-causal_rel).unsqueeze(0) * self.config.lambda_dangle + open_bond * self.config.lambda_dangle

        valence_matrix = (
            self.config.alpha_valence * valence_couplings * causal_mask - dangling_penalty
        )
        return valence_matrix.unsqueeze(1), ingress, egress  # [B, 1, N, N]


class CornellConfinementPotential(nn.Module):
    """
    Layer 4: Genuine QCD Gluon SU(3) Confinement & Cornell Potential.
        V_Cornell(r_ij) = -alpha_s / (r_ij + eps) + sigma * r_ij + V_snap(r_ij)
    Where r_ij = |z_i - z_j| is causal distance along the Z-axis.
    When r_ij > r_c (1.529), string snaps, generating a restorative confinement barrier.
    """
    def __init__(self, config: SemanticGluonConfig):
        super().__init__()
        self.config = config
        # Causal Z-coordinate estimator: maps embedding to continuous causal depth z in R
        self.z_projector = nn.Sequential(
            nn.Linear(config.embed_dim, config.embed_dim // 4),
            nn.Tanh(),
            nn.Linear(config.embed_dim // 4, 1)
        )
        # Learnable hadron color charges: Quark triplets (Red, Green, Blue)
        self.color_charge_proj = nn.Linear(config.embed_dim, 3)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Args:
            x: [B, N, D]
        Returns:
            v_cornell: [B, 1, N, N] confinement logit penalty.
            z_coords: [B, N] causal Z-depth values.
            string_snaps: [B, N, N] boolean indicator of snapped strings (r > r_c).
        """
        z_coords = self.z_projector(x).squeeze(-1)  # [B, N]
        color_charges = F.softmax(self.color_charge_proj(x), dim=-1)  # [B, N, 3] (r, g, b)
        
        # Pairwise causal Euclidean distance: r_ij = |z_i - z_j|
        r_ij = torch.abs(z_coords.unsqueeze(2) - z_coords.unsqueeze(1))  # [B, N, N]

        # 1. Asymptotic Freedom at short range: -alpha_s / (r_ij + eps)
        v_coulomb = -self.config.alpha_s / (r_ij + self.config.cornell_epsilon)

        # 2. Linear String Tension at medium range: sigma * r_ij
        v_linear = self.config.sigma * r_ij

        # 3. String Snapping Barrier for r_ij > r_c (r_c = 1.529)
        overshoot = F.relu(r_ij - self.config.r_c)
        v_snap = self.config.sigma_snap * torch.pow(overshoot, 2)

        # 4. Color Factor mediation: attractive binding between complementary color charges
        # [B, N, 3] x [B, 3, N] -> [B, N, N]
        color_coupling = torch.bmm(color_charges, color_charges.transpose(1, 2))
        v_color = -0.25 * color_coupling

        v_cornell = v_coulomb + v_linear + v_snap + v_color
        string_snaps = (r_ij >= self.config.r_c)

        return v_cornell.unsqueeze(1), z_coords, string_snaps, color_charges


class GaugeFrictionMatrix(nn.Module):
    """
    Layer 5: 7 Planes of Reality & Non-Commutative Gauge Friction Matrix.
    Computes directional friction Gamma_friction(P_i, P_j) between the 7 Q-Planes:
        Q1: Who (Metaphysical)     - Idx 0
        Q2: What (Possible)        - Idx 1 (+x lateral)
        Q3: Where (Physical)       - Idx 2 (-x lateral)
        Q4: Why (Lyrical)          - Idx 3 (+y longitudinal)
        Q5: How (Logical)          - Idx 4 (-y longitudinal)
        Q6: Cause (Historical)     - Idx 5 (+z vertical)
        Q7: Effect (Emotive)       - Idx 6 (-z vertical)

    Transition rules:
        - Constructive Geodesic (Q3 -> Q5 -> Q4 -> Q1): friction = 0.8
        - Inverted Leap (Q4 -> Q3): friction = 2.5 (Asserting physical reality from lyrical metaphor)
        - Inverted Leap (Q7 -> Q5): friction = 2.4 (Emotional outrage posing as formal proof)
        - Standard cross-plane transitions: 1.0 + 0.25 * |Delta_axis|
        - Intra-plane resonance: 0.3
    """
    def __init__(self, config: SemanticGluonConfig):
        super().__init__()
        self.config = config
        self.num_planes = config.num_planes

        # Soft continuous plane classifier: maps token to plane probability simplex Delta^6
        self.plane_gate = nn.Sequential(
            nn.Linear(config.embed_dim, config.embed_dim // 2),
            nn.LayerNorm(config.embed_dim // 2),
            nn.GELU(),
            nn.Linear(config.embed_dim // 2, self.num_planes)
        )

        # Build constant 7x7 gauge friction tensor
        F_gauge = torch.zeros(self.num_planes, self.num_planes)
        # Axis coordinates in 42-structure:
        # Q1: 0, Q2: +1, Q3: -1, Q4: +2, Q5: -2, Q6: +3, Q7: -3
        axis_coords = [0, 1, -1, 2, -2, 3, -3]
        for a in range(self.num_planes):
            for b in range(self.num_planes):
                if a == b:
                    F_gauge[a, b] = 0.3  # Intra-plane alignment
                else:
                    d_axis = abs(axis_coords[a] - axis_coords[b])
                    F_gauge[a, b] = config.friction_base + 0.25 * d_axis

        # Canonical Constructive Geodesic (Q3 -> Q5 -> Q4 -> Q1)
        F_gauge[2, 4] = config.friction_geodesic  # Q3 (Where) -> Q5 (How)
        F_gauge[4, 3] = config.friction_geodesic  # Q5 (How) -> Q4 (Why)
        F_gauge[3, 0] = config.friction_geodesic  # Q4 (Why) -> Q1 (Who)

        # Inverted Leaps (Heavily penalized)
        F_gauge[3, 2] = config.friction_inverted_q4_q3  # Q4 (Why) -> Q3 (Where) = 2.5
        F_gauge[6, 4] = config.friction_inverted_q7_q5  # Q7 (Effect) -> Q5 (How) = 2.4

        self.register_buffer("F_gauge", F_gauge)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: [B, N, D]
        Returns:
            gamma_friction: [B, 1, N, N]
            plane_probs: [B, N, 7] continuous plane assignments.
        """
        plane_logits = self.plane_gate(x)
        plane_probs = F.softmax(plane_logits, dim=-1)  # [B, N, 7]

        # Bilinear gauge expectation: Gamma_ij = P_i^T F_gauge P_j
        # [B, N, 7] x [7, 7] -> [B, N, 7]
        pf = torch.matmul(plane_probs, self.F_gauge)
        # [B, N, 7] x [B, 7, N] -> [B, N, N]
        gamma_friction = torch.bmm(pf, plane_probs.transpose(1, 2))

        return gamma_friction.unsqueeze(1), plane_probs


class RadiativeTransferLuminescence(nn.Module):
    """
    Layer 6: Radiative Transfer & Luminescence Field.
    Modulates attention by Beer-Lambert optical attenuation:
        L_ij = exp(-tau_ij)
    Where tau_ij is the optical thickness (opacity / fog).
    Rigorous, grounded White-Singlet assertions have low tau (high luminescence L >= 0.58).
    Unbacked assertions have high tau (tau >= 2.5, L <= 0.08).
    """
    def __init__(self, config: SemanticGluonConfig):
        super().__init__()
        self.config = config
        # Opacity / Epistemic Density Head
        self.tau_head = nn.Sequential(
            nn.Linear(config.embed_dim, config.embed_dim // 4),
            nn.GELU(),
            nn.Linear(config.embed_dim // 4, 1),
            nn.Softplus()
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: [B, N, D]
        Returns:
            luminescence: [B, 1, N, N] values in (0, 1].
            tau_tokens: [B, N] optical opacity per token.
        """
        tau_tokens = self.tau_head(x).squeeze(-1) + self.config.base_tau  # [B, N]
        tau_tokens = torch.clamp(tau_tokens, min=0.05, max=self.config.max_tau)

        # Pairwise optical thickness along the ray: tau_ij = 0.5 * (tau_i + tau_j)
        tau_ij = 0.5 * (tau_tokens.unsqueeze(2) + tau_tokens.unsqueeze(1))  # [B, N, N]
        luminescence = torch.exp(-tau_ij)  # [B, N, N]

        return luminescence.unsqueeze(1), tau_tokens


class ModalRayResonance(nn.Module):
    """
    Continuous 4-Modal Ray Projections (Female Generative Dimension):
        - can_be   (Productive:   +υ, +ψ, roll ≈ π/4)
        - is_not   (Reductive:    -υ, +ψ, roll ≈ 3π/4)
        - is_like  (Constructive: +υ, -ψ, roll ≈ 7π/4)
        - was_like (Regressive:   -υ, -ψ, roll ≈ 5π/4)
    Computes continuous resonant cross-modal representations that augment attention values.
    """
    def __init__(self, config: SemanticGluonConfig):
        super().__init__()
        self.config = config
        self.proj_can_be = nn.Linear(config.embed_dim, config.embed_dim)
        self.proj_is_not = nn.Linear(config.embed_dim, config.embed_dim)
        self.proj_is_like = nn.Linear(config.embed_dim, config.embed_dim)
        self.proj_was_like = nn.Linear(config.embed_dim, config.embed_dim)
        self.modal_gate = nn.Linear(config.embed_dim, 4)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Returns:
            modal_augmented: [B, N, D]
            modal_weights: [B, N, 4]
        """
        weights = F.softmax(self.modal_gate(x), dim=-1)  # [B, N, 4]
        r1 = torch.tanh(self.proj_can_be(x))
        r2 = torch.tanh(self.proj_is_not(x))
        r3 = torch.tanh(self.proj_is_like(x))
        r4 = torch.tanh(self.proj_was_like(x))
        
        # Linear combination of the 4 modal rays
        stacked = torch.stack([r1, r2, r3, r4], dim=-1)  # [B, N, D, 4]
        modal_aug = torch.einsum('bndk,bnk->bnd', stacked, weights)
        return modal_aug, weights


class SemanticGluonAttention(nn.Module):
    """
    PyTorch Semantic Gluon Attention Layer.
    
    Formula:
        S_ij = ((Q_i K_j^T / sqrt(d_k) + M_ij^valence - V_Cornell(r_ij) - Gamma_friction(P_i, P_j)) * exp(-tau_ij)) + M_ij^splicing
        Attention(Q, K, V) = softmax(S) V
    """
    def __init__(self, config: Optional[SemanticGluonConfig] = None):
        super().__init__()
        self.config = config or SemanticGluonConfig()
        D = self.config.embed_dim
        H = self.config.num_heads
        d_k = self.config.head_dim

        # Multi-Head Q, K, V projections
        self.q_proj = nn.Linear(D, D)
        self.k_proj = nn.Linear(D, D)
        self.v_proj = nn.Linear(D, D)
        self.out_proj = nn.Linear(D, D)

        self.dropout = nn.Dropout(self.config.dropout)

        # Core Physical Sub-Layers
        self.ribosomal_splicer = RibosomalExonSplicer(self.config)
        self.causal_valence = CausalValenceShell(self.config)
        self.cornell_confinement = CornellConfinementPotential(self.config)
        self.gauge_friction = GaugeFrictionMatrix(self.config)
        self.luminescence = RadiativeTransferLuminescence(self.config)
        self.modal_resonance = ModalRayResonance(self.config)

    def forward(
        self,
        x: torch.Tensor,
        exon_mask: Optional[torch.Tensor] = None,
        return_diagnostics: bool = True
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """
        Args:
            x: [B, N, D] input sequence tensor.
            exon_mask: [B, N] optional ground truth exon (1) vs intron (0) mask.
            return_diagnostics: Whether to return full diagnostic dictionary.
        Returns:
            output: [B, N, D] attended representations.
            diagnostics: Dict containing all intermediate physics tensors.
        """
        B, N, D = x.shape
        H = self.config.num_heads
        d_k = self.config.head_dim

        # 1. Multi-head Q, K, V projections
        # [B, N, D] -> [B, N, H, d_k] -> [B, H, N, d_k]
        Q = self.q_proj(x).view(B, N, H, d_k).transpose(1, 2)
        K = self.k_proj(x).view(B, N, H, d_k).transpose(1, 2)
        V = self.v_proj(x).view(B, N, H, d_k).transpose(1, 2)

        # 2. Modal Ray Resonance on Values (25M/75F generative enrichment)
        modal_aug, modal_weights = self.modal_resonance(x)
        V_aug = V + 0.1 * modal_aug.view(B, N, H, d_k).transpose(1, 2)

        # 3. Base Scaled Dot-Product Similarity: Q K^T / sqrt(d_k)
        # [B, H, N, d_k] x [B, H, d_k, N] -> [B, H, N, N]
        base_logits = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)

        # 4. Physical Modulating Fields (each [B, 1, N, N] broadcasting over heads H)
        splicing_mask, exon_probs = self.ribosomal_splicer(x, exon_mask=exon_mask)
        valence_matrix, ingress, egress = self.causal_valence(x)
        v_cornell, z_coords, string_snaps, color_charges = self.cornell_confinement(x)
        gamma_friction, plane_probs = self.gauge_friction(x)
        luminescence_field, tau_tokens = self.luminescence(x)

        # 5. Core Modified Attention Logit Equation:
        # S_confined = base_logits + M_valence - V_Cornell - Gamma_friction
        S_confined = base_logits + valence_matrix - v_cornell - gamma_friction

        # S_attenuated = S_confined * exp(-tau_ij)
        S_attenuated = S_confined * luminescence_field

        # Final Logits S = S_attenuated + M_splicing
        S = S_attenuated + splicing_mask

        # 6. Softmax & Ribosomal Intron Excising
        attn_weights = F.softmax(S, dim=-1)

        # Zero out ghost attention from non-coding intron queries
        # (Introns have all -inf logits; multiplying by exon_gate ensures pure zero attention)
        if exon_mask is not None:
            query_mask = exon_mask.unsqueeze(1).unsqueeze(-1).float()  # [B, 1, N, 1]
            attn_weights = attn_weights * query_mask
        else:
            query_mask = exon_probs.unsqueeze(1).unsqueeze(-1)
            attn_weights = attn_weights * query_mask

        attn_weights_dropped = self.dropout(attn_weights)

        # 7. Weighted Sum: [B, H, N, N] x [B, H, N, d_k] -> [B, H, N, d_k]
        context = torch.matmul(attn_weights_dropped, V_aug)

        # Re-assemble heads: [B, H, N, d_k] -> [B, N, H, d_k] -> [B, N, D]
        context = context.transpose(1, 2).contiguous().view(B, N, D)
        output = self.out_proj(context)

        diagnostics = {}
        if return_diagnostics:
            diagnostics = {
                "attention_weights": attn_weights,
                "pre_softmax_logits": S,
                "base_logits": base_logits,
                "valence_matrix": valence_matrix.squeeze(1),
                "v_cornell": v_cornell.squeeze(1),
                "gamma_friction": gamma_friction.squeeze(1),
                "luminescence_field": luminescence_field.squeeze(1),
                "splicing_mask": splicing_mask.squeeze(1),
                "exon_probs": exon_probs,
                "z_coords": z_coords,
                "string_snaps": string_snaps,
                "color_charges": color_charges,
                "plane_probs": plane_probs,
                "tau_tokens": tau_tokens,
                "modal_weights": modal_weights,
                "ingress": ingress,
                "egress": egress
            }

        return output, diagnostics


class SemanticGluonTransformerBlock(nn.Module):
    """
    Complete Semantic Gluon Transformer Block with Pre-LN and SwiGLU / MLP feedforward.
    """
    def __init__(self, config: Optional[SemanticGluonConfig] = None):
        super().__init__()
        self.config = config or SemanticGluonConfig()
        D = self.config.embed_dim

        self.ln1 = nn.LayerNorm(D)
        self.attn = SemanticGluonAttention(self.config)
        self.ln2 = nn.LayerNorm(D)

        # Feedforward MLP
        ffn_dim = int(D * 8 / 3)  # LLaMA-style expansion
        self.ffn = nn.Sequential(
            nn.Linear(D, ffn_dim),
            nn.SiLU(),
            nn.Linear(ffn_dim, D),
            nn.Dropout(self.config.dropout)
        )

    def forward(
        self,
        x: torch.Tensor,
        exon_mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        # Residual connection 1: Attention
        normed = self.ln1(x)
        attn_out, diag = self.attn(normed, exon_mask=exon_mask)
        x = x + attn_out

        # Residual connection 2: Feedforward
        x = x + self.ffn(self.ln2(x))
        return x, diag
