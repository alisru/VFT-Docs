"""
Semantic Gluon Attention Layer (PyTorch)
Generation 7 Architecture Cook-Off - Competitor 1 (75% Male / 25% Female)

Formal Neural Specification:
  S_ij = ((Q_i K_j^T / sqrt(d_k) + M_ij^valence - V_Cornell(r_ij) - Gamma_friction(P_i, P_j)) * exp(-tau_ij)) + M_ij^splicing
  Attention(Q, K, V) = softmax(S) V

Physical Invariants:
  1. Ribosomal Exon Splicing: Excises non-coding conversational introns (-inf mask).
  2. Causal Valence Shell: Directs forward obligations and backward requirements with zero valence leakage.
  3. Cornell SU(3) Confinement Potential: Suppresses attention beyond critical snapping radius r_c = 1.529.
  4. 7-Planes Gauge Friction: Directional non-commutative friction across the 7 Planes of Reality.
  5. Optical Attenuation Field: Modulates attention logits by Beer-Lambert luminescence exp(-tau).
  6. Proof-Theater Detection Loss: Penalizes ungrounded assertions, snapped strings, and valence leakage.
"""

import math
from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


class RibosomalExonSplicer(nn.Module):
    """
    Layer 1: Ribosomal Exon Splicing Mask.
    Excises conversational introns (-inf logit penalty), forcing attention
    onto invariant mathematical and semantic exons.
    
    If token i or j is an intron (exon_mask=0), M_splicing[i, j] = -1e9.
    Provides strict numerical stability to prevent all-masked row NaN in softmax.
    """
    def __init__(self, embed_dim: int = 384, mask_penalty: float = 1e9):
        super().__init__()
        self.embed_dim = embed_dim
        self.mask_penalty = mask_penalty
        # Splicer head predicts exon coding probability if ground-truth mask is not provided
        self.exon_classifier = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.LayerNorm(embed_dim // 4),
            nn.GELU(),
            nn.Linear(embed_dim // 4, 1)
        )

    def forward(
        self,
        x: torch.Tensor,
        exon_mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Args:
            x: [B, N, D] sequence embeddings
            exon_mask: Optional [B, N] boolean or float tensor (1 = exon, 0 = intron)
        Returns:
            splicing_mask: [B, 1, N, N] attention logit additive mask
            effective_exon_mask: [B, N] (1 = exon, 0 = intron)
            predicted_logits: [B, N] logits from exon classifier
        """
        B, N, _ = x.shape
        predicted_logits = self.exon_classifier(x).squeeze(-1) # [B, N]
        predicted_probs = torch.sigmoid(predicted_logits)

        if exon_mask is None:
            # Straight-through estimator (STE): discrete forward, continuous backward
            hard_mask = (predicted_probs >= 0.5).float()
            effective_exon_mask = hard_mask - predicted_probs.detach() + predicted_probs
            bool_mask = hard_mask.bool()
        else:
            if exon_mask.dtype == torch.bool:
                bool_mask = exon_mask
                effective_exon_mask = exon_mask.float()
            else:
                bool_mask = exon_mask > 0.5
                effective_exon_mask = exon_mask.float()

        # Exon-exon pair is valid only when BOTH token i and token j are coding exons
        # exon_pair: [B, N, N]
        exon_pair = bool_mask.unsqueeze(-1) & bool_mask.unsqueeze(-2)
        
        # Splicing mask: 0 where valid, -penalty where either is an intron
        splicing_mask = torch.zeros(B, 1, N, N, device=x.device, dtype=x.dtype)
        splicing_mask = splicing_mask.masked_fill(~exon_pair.unsqueeze(1), -self.mask_penalty)

        return splicing_mask, effective_exon_mask, predicted_logits


class CausalValenceShell(nn.Module):
    """
    Layer 3: Causal Valence Shell Matrix (M_ij^valence).
    Enforces backward ingress requirements (B_i) and forward egress obligations (F_j).
    Penalizes dangling open bonds and ungrounded assertions:
      M_ij^valence = alpha_v * ( (B_i F_j^T / sqrt(d_v)) * 1_{i >= j} - u_j * ||B_i|| ) - lambda_dangle * delta_open(i)
    """
    def __init__(
        self,
        embed_dim: int = 384,
        valence_dim: int = 64,
        alpha_v: float = 1.0,
        lambda_dangle: float = 0.5
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.valence_dim = valence_dim
        self.alpha_v = alpha_v
        self.lambda_dangle = lambda_dangle

        # Ingress (backward requirements) & Egress (forward obligations)
        self.ingress_proj = nn.Linear(embed_dim, valence_dim, bias=False)
        self.egress_proj = nn.Linear(embed_dim, valence_dim, bias=False)
        
        # Ungroundedness head: predicts lack of evidentiary bedrock
        self.ungrounded_head = nn.Sequential(
            nn.Linear(embed_dim, valence_dim // 2),
            nn.ReLU(),
            nn.Linear(valence_dim // 2, 1),
            nn.Sigmoid()
        )
        
        # Open bond / dangling closure head
        self.dangle_head = nn.Sequential(
            nn.Linear(embed_dim, valence_dim // 2),
            nn.ReLU(),
            nn.Linear(valence_dim // 2, 1),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """
        Args:
            x: [B, N, D]
        Returns:
            m_valence: [B, 1, N, N] valence modulation matrix
            diagnostics: dict with B_req, F_ob, ungrounded, dangle, valence_delta
        """
        B, N, _ = x.shape
        B_req = self.ingress_proj(x)   # [B, N, d_v]
        F_ob = self.egress_proj(x)     # [B, N, d_v]
        ungrounded = self.ungrounded_head(x).squeeze(-1) # [B, N]
        dangle = self.dangle_head(x).squeeze(-1)         # [B, N]

        # Bilinear ingress-egress satisfaction: B_req * F_ob^T
        satisfaction = torch.matmul(B_req, F_ob.transpose(-1, -2)) / math.sqrt(self.valence_dim) # [B, N, N]

        # Causal temporal masking (i >= j: key j precedes or is concurrent with query i)
        causal_mask = torch.tril(torch.ones(N, N, device=x.device, dtype=x.dtype)).unsqueeze(0) # [1, N, N]
        
        # Penalty for attending to ungrounded key tokens: u_j * ||B_i||
        b_norm = torch.norm(B_req, p=2, dim=-1, keepdim=True) # [B, N, 1]
        ungrounded_penalty = b_norm * ungrounded.unsqueeze(-2) # [B, N, N]

        # Dangling bond penalty on query token i
        dangle_penalty = dangle.unsqueeze(-1) # [B, N, 1]

        # Combine into M_valence
        m_valence = self.alpha_v * (satisfaction * causal_mask - ungrounded_penalty) - self.lambda_dangle * dangle_penalty
        m_valence = m_valence.unsqueeze(1) # [B, 1, N, N]

        # Valence conservation metric: Net delta between egress supplied and ingress required
        # Conservation: sum(F_ob) - sum(B_req) -> 0 across the closed argument
        valence_delta = torch.norm(F_ob.sum(dim=1) - B_req.sum(dim=1), p=2, dim=-1) # [B]

        diagnostics = {
            "ingress": B_req,
            "egress": F_ob,
            "ungrounded": ungrounded,
            "dangle": dangle,
            "valence_delta": valence_delta
        }
        return m_valence, diagnostics


class CornellConfinementPotential(nn.Module):
    """
    Layer 4: Genuine QCD SU(3) Confinement Potential.
    Models semantic confinement using the Cornell Potential:
      V_Cornell(r_ij) = -alpha_s / (r_ij + epsilon) + sigma * r_ij
    where r_ij = ||z_i - z_j|| is the causal distance along the Z-axis.
    
    If r_ij >= r_c (critical string-snapping radius r_c = 1.529),
    the causal flux tube snaps, diagnosing a non-sequitur or proof hallucination.
    """
    def __init__(
        self,
        embed_dim: int = 384,
        alpha_s: float = 0.35,
        sigma: float = 0.85,
        r_c: float = 1.529,
        epsilon: float = 0.15
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.alpha_s = alpha_s
        self.sigma = sigma
        self.r_c = r_c
        self.epsilon = epsilon

        # Causal Z-axis projection head (z < 0: Upstream Cause, z > 0: Downstream Effect)
        self.z_head = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.Tanh(),
            nn.Linear(embed_dim // 4, 1)
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """
        Args:
            x: [B, N, D]
        Returns:
            v_cornell: [B, 1, N, N] confinement potential matrix
            diagnostics: dict with z_causal, r_distance, string_snaps
        """
        B, N, _ = x.shape
        z_causal = self.z_head(x).squeeze(-1) # [B, N]

        # Pairwise causal displacement r_ij = |z_i - z_j|
        r_ij = torch.abs(z_causal.unsqueeze(-1) - z_causal.unsqueeze(-2)) # [B, N, N]

        # Cornell potential calculation (numerically bounded by epsilon)
        v_coulomb = -self.alpha_s / (r_ij + self.epsilon)
        v_linear = self.sigma * r_ij
        v_cornell = v_coulomb + v_linear # [B, N, N]

        # Clamp potential to prevent extreme logit blowout
        v_cornell = torch.clamp(v_cornell, min=-4.0, max=12.0)
        v_cornell = v_cornell.unsqueeze(1) # [B, 1, N, N]

        # String-snapping condition: r_ij >= r_c
        snaps = (r_ij >= self.r_c).float() # [B, N, N]

        diagnostics = {
            "z_causal": z_causal,
            "r_distance": r_ij,
            "string_snaps": snaps,
            "snap_count": snaps.sum(dim=(-1, -2))
        }
        return v_cornell, diagnostics


class PlaneGaugeFriction(nn.Module):
    """
    Layer 5: 7-Planes Reality & Non-Commutative Gauge Friction (Gamma_friction).
    The 7 Planes of Reality:
      Q1: Metaphysical (WHO)   - Driver / 7th Angle Axis
      Q2: Possible (WHAT)      - Lateral +x
      Q3: Physical (WHERE)     - Lateral -x
      Q4: Lyrical (WHY)        - Longitudinal +y
      Q5: Logical (HOW)        - Longitudinal -y
      Q6: Historical (CAUSE)   - Vertical +z
      Q7: Emotive (EFFECT)     - Vertical -z
      
    Canonical Friction Rules:
      - Constructive Geodesic: Q3 -> Q5 -> Q4 -> Q1 has low friction (0.8).
      - Inverted Leap: Q4 -> Q3 (physical assertion from metaphor) has friction 2.5.
      - Inverted Leap: Q7 -> Q5 (outrage posing as formal proof) has friction 2.4.
      - Standard cross-plane transition: 1.0 + 0.25 * |Delta_axis|.
    """
    def __init__(self, embed_dim: int = 384, num_planes: int = 7):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_planes = num_planes

        # Token plane classifier: predicts distribution over 7 Q-Planes
        self.plane_classifier = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.GELU(),
            nn.Linear(embed_dim // 4, num_planes)
        )

        # Build canonical 7x7 gauge friction matrix
        F_canonical = torch.ones(num_planes, num_planes) * 1.0
        
        # Intra-plane baseline friction
        for i in range(num_planes):
            F_canonical[i, i] = 0.05

        # Plane coordinate indices for axis distance computation:
        # Q1: 0 (Angle), Q2: +1x, Q3: -1x, Q4: +1y, Q5: -1y, Q6: +1z, Q7: -1z
        # Standard cross-plane distance
        axis_map = [
            torch.tensor([0.0, 0.0, 0.0, 1.0]),  # Q1
            torch.tensor([1.0, 0.0, 0.0, 0.0]),  # Q2 (+x)
            torch.tensor([-1.0, 0.0, 0.0, 0.0]), # Q3 (-x)
            torch.tensor([0.0, 1.0, 0.0, 0.0]),  # Q4 (+y)
            torch.tensor([0.0, -1.0, 0.0, 0.0]), # Q5 (-y)
            torch.tensor([0.0, 0.0, 1.0, 0.0]),  # Q6 (+z)
            torch.tensor([0.0, 0.0, -1.0, 0.0]), # Q7 (-z)
        ]
        for i in range(num_planes):
            for j in range(num_planes):
                if i != j:
                    delta_axis = torch.norm(axis_map[i] - axis_map[j], p=2).item()
                    F_canonical[i, j] = 1.0 + 0.25 * delta_axis

        # Constructive Geodesics (Q3 -> Q5 -> Q4 -> Q1): friction = 0.8
        # 0-indexed: Q1=0, Q2=1, Q3=2, Q4=3, Q5=4, Q6=5, Q7=6
        F_canonical[2, 4] = 0.8  # Q3 -> Q5
        F_canonical[4, 3] = 0.8  # Q5 -> Q4
        F_canonical[3, 0] = 0.8  # Q4 -> Q1

        # Inverted Leaps:
        F_canonical[3, 2] = 2.5  # Q4 -> Q3 (Lyrical to Physical assertion)
        F_canonical[6, 4] = 2.4  # Q7 -> Q5 (Emotive outrage to Logical proof)

        # Register as persistent buffer
        self.register_buffer("F_canonical", F_canonical)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """
        Args:
            x: [B, N, D]
        Returns:
            gamma_friction: [B, 1, N, N] gauge friction matrix
            diagnostics: dict with plane_probs, plane_indices
        """
        logits = self.plane_classifier(x) # [B, N, 7]
        plane_probs = F.softmax(logits, dim=-1) # [B, N, 7]

        # Bilinear form across sequence pairs: P_i * F_canonical * P_j^T
        # [B, N, 7] x [7, 7] x [B, 7, N] -> [B, N, N]
        gamma = torch.einsum("bip,pq,bjq->bij", plane_probs, self.F_canonical, plane_probs)
        gamma = gamma.unsqueeze(1) # [B, 1, N, N]

        diagnostics = {
            "plane_probs": plane_probs,
            "plane_preds": torch.argmax(plane_probs, dim=-1)
        }
        return gamma, diagnostics


class OpticalAttenuationField(nn.Module):
    """
    Layer 6: Semantic Optical Attenuation Field (exp(-tau)).
    Beer-Lambert optical transmission:
      tau_ij = tau_0 + 0.5 * (tau_i + tau_j)
      L_ij = exp(-tau_ij)
    Bare assertions without derivations produce high optical depth tau (opaque fog).
    Rigorous, verified derivations yield low tau and high luminescence L.
    """
    def __init__(self, embed_dim: int = 384, tau_0: float = 0.1):
        super().__init__()
        self.embed_dim = embed_dim
        self.tau_0 = tau_0
        
        # Opacity / fog estimator: higher for unverified assertion claims
        self.tau_head = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.GELU(),
            nn.Linear(embed_dim // 4, 1),
            nn.Softplus() # guarantees tau >= 0
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: [B, N, D]
        Returns:
            attenuation: [B, 1, N, N] factor exp(-tau_ij)
            tau_ij: [B, N, N] pairwise optical thickness
        """
        tau_token = self.tau_head(x).squeeze(-1) # [B, N]
        
        # Pairwise optical thickness tau_ij = tau_0 + 0.5 * (tau_i + tau_j)
        tau_ij = self.tau_0 + 0.5 * (tau_token.unsqueeze(-1) + tau_token.unsqueeze(-2)) # [B, N, N]
        
        # Optical attenuation factor: L = exp(-tau) in (0, 1]
        attenuation = torch.exp(-tau_ij).unsqueeze(1) # [B, 1, N, N]
        return attenuation, tau_ij


class SemanticGluonAttention(nn.Module):
    """
    The Complete Unified Semantic Gluon Attention Layer.
    
    Mathematical Formulation:
      S_ij = ((Q_i K_j^T / sqrt(d_k) + M_ij^valence - V_Cornell(r_ij) - Gamma_friction(P_i, P_j)) * exp(-tau_ij)) + M_ij^splicing
      Attention(Q, K, V) = softmax(S) V
    """
    def __init__(
        self,
        embed_dim: int = 384,
        num_heads: int = 6,
        dropout: float = 0.0,
        alpha_v: float = 1.0,
        lambda_dangle: float = 0.5,
        alpha_s: float = 0.35,
        sigma: float = 0.85,
        r_c: float = 1.529,
        tau_0: float = 0.1,
        mask_penalty: float = 1e9
    ):
        super().__init__()
        assert embed_dim % num_heads == 0, f"embed_dim ({embed_dim}) must be divisible by num_heads ({num_heads})"
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        # Multi-Head Q, K, V Projections
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.out_proj = nn.Linear(embed_dim, embed_dim)

        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else nn.Identity()

        # Physical Modulating Layers
        self.splicer = RibosomalExonSplicer(embed_dim=embed_dim, mask_penalty=mask_penalty)
        self.valence_shell = CausalValenceShell(embed_dim=embed_dim, alpha_v=alpha_v, lambda_dangle=lambda_dangle)
        self.confinement = CornellConfinementPotential(embed_dim=embed_dim, alpha_s=alpha_s, sigma=sigma, r_c=r_c)
        self.gauge_friction = PlaneGaugeFriction(embed_dim=embed_dim)
        self.optical_attenuation = OpticalAttenuationField(embed_dim=embed_dim, tau_0=tau_0)

    def forward(
        self,
        x: torch.Tensor,
        exon_mask: Optional[torch.Tensor] = None,
        return_diagnostics: bool = True
    ) -> Tuple[torch.Tensor, Optional[Dict[str, torch.Tensor]]]:
        """
        Args:
            x: [B, N, D] Input sequence embeddings
            exon_mask: Optional [B, N] (1 = exon, 0 = intron)
            return_diagnostics: Whether to return full physical telemetry
        Returns:
            output: [B, N, D] Layer representation
            diagnostics: Dictionary containing all physical matrices and metrics
        """
        B, N, D = x.shape
        H, d_k = self.num_heads, self.head_dim

        # 1. Multi-Head Projections: [B, H, N, d_k]
        Q = self.q_proj(x).view(B, N, H, d_k).transpose(1, 2)
        K = self.k_proj(x).view(B, N, H, d_k).transpose(1, 2)
        V = self.v_proj(x).view(B, N, H, d_k).transpose(1, 2)

        # Base Scaled Dot-Product Logits: [B, H, N, N]
        base_logits = torch.matmul(Q, K.transpose(-1, -2)) / math.sqrt(d_k)

        # 2. Evaluate Physical Modulation Fields: all [B, 1, N, N]
        m_splicing, effective_exon_mask, predicted_exon_logits = self.splicer(x, exon_mask)
        m_valence, diag_valence = self.valence_shell(x)
        v_cornell, diag_cornell = self.confinement(x)
        gamma_friction, diag_friction = self.gauge_friction(x)
        attenuation_exp, tau_ij = self.optical_attenuation(x)

        # 3. Assemble Modified Logit Matrix:
        # S_ij = ((Q K^T / sqrt(d_k) + M_valence - V_Cornell - Gamma_friction) * exp(-tau)) + M_splicing
        unattenuated_logits = base_logits + m_valence - v_cornell - gamma_friction
        attenuated_logits = unattenuated_logits * attenuation_exp
        S = attenuated_logits + m_splicing # [B, H, N, N]

        # 4. Softmax with Numerical Stability Guard:
        # If an entire row is masked by splicing (-inf), standard softmax produces NaN.
        # Guard: Detect rows that are completely masked (-inf across all keys)
        all_masked_rows = (S <= -1e8).all(dim=-1, keepdim=True) # [B, H, N, 1]
        safe_S = S.masked_fill(all_masked_rows, 0.0)
        
        # Softmax over key dimension
        attn_weights = F.softmax(safe_S, dim=-1)
        
        # Zero out weights for all-masked intron query rows
        attn_weights = attn_weights.masked_fill(all_masked_rows, 0.0)
        attn_weights = self.dropout(attn_weights)

        # 5. Output Projection
        context = torch.matmul(attn_weights, V) # [B, H, N, d_k]
        context = context.transpose(1, 2).contiguous().view(B, N, D) # [B, N, D]
        output = self.out_proj(context)

        # Zero out intron representations if masked
        if effective_exon_mask is not None:
            output = output * effective_exon_mask.unsqueeze(-1).to(output.dtype)

        if not return_diagnostics:
            return output, None

        # Calculate attention sparsity: fraction of weights < 1e-4
        attn_sparsity = (attn_weights < 1e-4).float().mean()

        diagnostics = {
            "attention_weights": attn_weights,
            "raw_logits": base_logits,
            "modified_logits": S,
            "m_valence": m_valence,
            "v_cornell": v_cornell,
            "gamma_friction": gamma_friction,
            "attenuation_exp": attenuation_exp,
            "tau_ij": tau_ij,
            "m_splicing": m_splicing,
            "effective_exon_mask": effective_exon_mask,
            "predicted_exon_logits": predicted_exon_logits,
            "attention_sparsity": attn_sparsity,
            "valence_delta": diag_valence["valence_delta"],
            "ungrounded": diag_valence["ungrounded"],
            "z_causal": diag_cornell["z_causal"],
            "string_snaps": diag_cornell["string_snaps"],
            "snap_count": diag_cornell["snap_count"],
            "plane_probs": diag_friction["plane_probs"],
            "plane_preds": diag_friction["plane_preds"]
        }
        return output, diagnostics


class ProofTheaterDetectionLoss(nn.Module):
    """
    Multi-Objective Loss Enforcing Invariant Conservation & Proof-Theater Detection:
      1. Target Task Loss (L_task): MSE or Cross-Entropy on output prediction.
      2. Causal Valence Conservation Loss (L_valence): Net delta between egress and ingress -> 0.
      3. String-Snapping Penalty (L_snaps): Suppresses attention between tokens with r_ij >= r_c.
      4. Grounding Loss (L_grounding): Penalizes ungrounded tokens asserting high valence obligations.
      5. Friction Minimization (L_friction): Penalizes inverted gauge leaps (Q4->Q3, Q7->Q5).
      6. Splicing Classification Loss (L_splicing): Trains ribosomal exon classification.
    """
    def __init__(
        self,
        w_task: float = 1.0,
        w_valence: float = 0.5,
        w_snaps: float = 0.8,
        w_grounding: float = 0.4,
        w_friction: float = 0.3,
        w_splicing: float = 0.5
    ):
        super().__init__()
        self.w_task = w_task
        self.w_valence = w_valence
        self.w_snaps = w_snaps
        self.w_grounding = w_grounding
        self.w_friction = w_friction
        self.w_splicing = w_splicing

    def forward(
        self,
        output: torch.Tensor,
        target: torch.Tensor,
        diagnostics: Dict[str, torch.Tensor]
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Args:
            output: [B, N, D] Layer output
            target: [B, N, D] Target representation
            diagnostics: Dict from SemanticGluonAttention
        """
        # 1. Target Task Loss
        l_task = F.mse_loss(output, target)

        # 2. Causal Valence Conservation Loss: ||sum(F) - sum(B)||^2
        l_valence = diagnostics["valence_delta"].mean()

        # 3. String-Snapping Penalty: Active attention across snapped flux tubes (r >= r_c)
        # attn_weights: [B, H, N, N] -> mean across heads
        attn_mean = diagnostics["attention_weights"].mean(dim=1) # [B, N, N]
        l_snaps = (attn_mean * diagnostics["string_snaps"]).sum(dim=(-1, -2)).mean()

        # 4. Proof-Theater Ungroundedness: ungrounded tokens attempting high egress assertion
        ungrounded = diagnostics["ungrounded"] # [B, N]
        # m_valence is [B, 1, N, N]. Norm across key dimension gives valence intensity per query token: [B, N]
        egress_norm = torch.norm(diagnostics["m_valence"].squeeze(1), p=2, dim=-1) # [B, N]
        l_grounding = (ungrounded * egress_norm).mean()

        # 5. Inverted Gauge Leap Friction Penalty
        # Penalty when high attention coincides with high gauge friction
        friction_grid = diagnostics["gamma_friction"].squeeze(1) # [B, N, N]
        l_friction = (attn_mean * friction_grid).sum(dim=(-1, -2)).mean()

        # 6. Splicing Exon Classification Loss
        target_exon = diagnostics["effective_exon_mask"].float()
        l_splicing = F.binary_cross_entropy_with_logits(diagnostics["predicted_exon_logits"], target_exon)

        total_loss = (
            self.w_task * l_task +
            self.w_valence * l_valence +
            self.w_snaps * l_snaps +
            self.w_grounding * l_grounding +
            self.w_friction * l_friction +
            self.w_splicing * l_splicing
        )

        details = {
            "total_loss": float(total_loss.item()),
            "task_loss": float(l_task.item()),
            "valence_loss": float(l_valence.item()),
            "snap_loss": float(l_snaps.item()),
            "grounding_loss": float(l_grounding.item()),
            "friction_loss": float(l_friction.item()),
            "splicing_loss": float(l_splicing.item())
        }
        return total_loss, details
