"""
Neural Network Modules for the Fractal Polytrope Transformer (PyTorch).

Implements:
  1. QPlaneIntentGate: The 42-cell (7 Q-Planes x 6 Intent Vectors) routing tensor.
  2. ModalRayProjectionHead: Parameterized transformation operators for the 4 modal rays:
       - T_can_be   (Productive:   +υ, +ψ, θ_roll ≈ π/4)
       - T_is_not   (Reductive:    -υ, +ψ, θ_roll ≈ 3π/4)
       - T_is_like  (Constructive: +υ, -ψ, θ_roll ≈ 7π/4)
       - T_was_like (Regress:       -υ, -ψ, θ_roll ≈ 5π/4)
  3. CausalProjectionHead: The "IS ALSO" Z-axis head:
       - z < 0: Upstream Cause / Origin (A)
       - z > 0: Downstream Effect / Fruit (E)
  4. GeodesicLoss: Multi-objective geometric loss enforcing quadrant alignment,
     antipodal negation, and causal directionality.
"""

import math
from typing import Dict, Optional, Tuple, Union
import torch
import torch.nn as nn
import torch.nn.functional as F

class QPlaneIntentGate(nn.Module):
    """
    42-Cell Routing Tensor:
    7 Q-Planes x 6 Intent Vectors = 42 specialized attention matrices.
    """
    def __init__(self, embed_dim=384, num_planes=7, num_intents=6):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_planes = num_planes
        self.num_intents = num_intents
        
        # Plane gate classifier (which of the 7 reality levels is dominant)
        self.plane_gate = nn.Linear(embed_dim, num_planes)
        
        # Intent gate classifier (which of the 6 intent directions is dominant)
        self.intent_gate = nn.Linear(embed_dim, num_intents)
        
        # 42 transformation matrices (one per cell Q_i ⊗ I_j)
        # Stored compactly as a 42-channel projection
        self.cell_projections = nn.Parameter(
            torch.randn(num_planes * num_intents, embed_dim, embed_dim) * 0.02
        )

    def forward(self, x):
        """
        x: [batch_size, embed_dim]
        Returns:
          routed_x: [batch_size, embed_dim]
          plane_probs: [batch_size, num_planes]
          intent_probs: [batch_size, num_intents]
        """
        plane_logits = self.plane_gate(x)
        intent_logits = self.intent_gate(x)
        
        plane_probs = F.softmax(plane_logits, dim=-1)   # [batch, 7]
        intent_probs = F.softmax(intent_logits, dim=-1) # [batch, 6]
        
        # Outer product to get 42-cell joint weights: [batch, 42]
        cell_weights = torch.bmm(
            plane_probs.unsqueeze(2), 
            intent_probs.unsqueeze(1)
        ).view(x.size(0), -1)
        
        # Weighted mixture of the 42 cell transformation manifolds
        # cell_projections: [42, dim, dim] -> [batch, dim, dim]
        mixed_weights = torch.einsum('bc,cde->bde', cell_weights, self.cell_projections)
        routed_x = torch.bmm(x.unsqueeze(1), mixed_weights).squeeze(1) + x
        
        return routed_x, plane_probs, intent_probs

class ModalRayProjectionHead(nn.Module):
    """
    Projects the base representation of 'IS' into the 4 relative modal rays:
      can_be, is_not, is_like, was_like
    """
    def __init__(self, embed_dim=384):
        super().__init__()
        # 4 specialized projection operators
        self.proj_can_be = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.Tanh(),
            nn.Linear(embed_dim, 3) # outputs target (υ, ψ, z) for CAN_BE
        )
        self.proj_is_not = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.Tanh(),
            nn.Linear(embed_dim, 3) # outputs target (υ, ψ, z) for IS_NOT
        )
        self.proj_is_like = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.Tanh(),
            nn.Linear(embed_dim, 3) # outputs target (υ, ψ, z) for IS_LIKE
        )
        self.proj_was_like = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.Tanh(),
            nn.Linear(embed_dim, 3) # outputs target (υ, ψ, z) for WAS_LIKE
        )
        
        # Base state coordinate estimator for the input sentence itself
        self.base_coord_head = nn.Linear(embed_dim, 3) # (υ, ψ, z)
        # Angular orientation estimator: θ_roll, θ_pitch, θ_yaw in [-π, π]
        self.angle_head = nn.Linear(embed_dim, 3)

    def forward(self, x):
        """
        x: [batch, embed_dim]
        Returns:
          base_coord: [batch, 3] (υ, ψ, z)
          angles: [batch, 3] (θ_roll, θ_pitch, θ_yaw)
          rays: dict of [batch, 3] coordinates for each modal ray
        """
        base_coord = self.base_coord_head(x)
        angles = torch.tanh(self.angle_head(x)) * math.pi
        
        rays = {
            "can_be": self.proj_can_be(x),
            "is_not": self.proj_is_not(x),
            "is_like": self.proj_is_like(x),
            "was_like": self.proj_was_like(x)
        }
        return base_coord, angles, rays

class CausalProjectionHead(nn.Module):
    """
    The 'IS ALSO' Causal Head:
    Computes upstream causal lineage (z < 0) and downstream consequences (z > 0).
    """
    def __init__(self, embed_dim=384):
        super().__init__()
        self.cause_head = nn.Linear(embed_dim, embed_dim)
        self.effect_head = nn.Linear(embed_dim, embed_dim)
        self.z_scalar = nn.Linear(embed_dim, 1)

    def forward(self, x):
        """
        Returns:
          cause_vec: representation of upstream antecedent causes
          effect_vec: representation of downstream consequences
          z_val: causal displacement score (z < 0 = cause, z > 0 = effect)
        """
        cause_vec = F.relu(self.cause_head(x))
        effect_vec = F.relu(self.effect_head(x))
        z_val = self.z_scalar(x).squeeze(-1)
        return cause_vec, effect_vec, z_val

class FractalPolytropeTransformer(nn.Module):
    """
    Full (7x6+n) Fractal Polytrope Transformer Model.
    Integrates:
      1. Sequence-level Semantic Gluon Attention block with oriented 5' -> 3' flux bonds.
      2. Token-level 42-cell Q-Plane intent router.
      3. Modal ray projection heads (can_be, is_not, is_like, was_like).
      4. Causal Z-axis projection (IS ALSO cause vs effect).
      5. Belief State Diagnostic Head (Operational Vector V, Cognitive Assumption A,
         Reality Strain eta, Framework Sanity Verdicts, and Worldview Scope E = mc^2).
      6. Dynamic Document Trajectory Integrator (Path integral Sigma_D, polarity iota_D).
      7. Ribosomal Reading Head (Codon emission, cumulative working-out ledger).
      8. Derivation Law Completeness Loss (Mathematical detector of maths without working out).
      9. Four Colored Gluon Gauge Forces (Red, Green, Blue, Magenta).
    """
    def __init__(self, embed_dim=384, num_heads=6):
        super().__init__()
        self.embed_dim = embed_dim
        self.gluon_block = SemanticGluonTransformerBlock(embed_dim=embed_dim, num_heads=num_heads)
        self.router = QPlaneIntentGate(embed_dim=embed_dim)
        self.modal_heads = ModalRayProjectionHead(embed_dim=embed_dim)
        self.causal_head = CausalProjectionHead(embed_dim=embed_dim)
        self.belief_head = BeliefStateDiagnosticHead(embed_dim=embed_dim)

        # Dynamic Trajectory & Ribosomal Reading Head Suite
        self.trajectory_integrator = DynamicTrajectoryIntegrator(embed_dim=embed_dim)
        self.reading_head = RibosomalReadingHead(embed_dim=embed_dim)
        self.color_forces = FourColoredGluonForces(embed_dim=embed_dim)
        self.insolvency_loss_fn = DerivationLawCompletenessLoss()

    def forward(self, x, exon_mask=None, return_diagnostics=True):
        """
        Supports both 2D token batches [B, D] and 3D sequence tensors [B, N, D].
        """
        is_sequence = (x.dim() == 3)
        if is_sequence:
            B, N, D = x.shape
            attended_x, gluon_diag = self.gluon_block(x, exon_mask=exon_mask, return_diagnostics=True)
            flat_x = attended_x.contiguous().view(B * N, D)
            routed_flat, plane_probs_flat, intent_probs_flat = self.router(flat_x)
            base_coord_flat, angles_flat, rays_flat = self.modal_heads(routed_flat)
            cause_flat, effect_flat, z_val_flat = self.causal_head(routed_flat)

            # Reshape back to sequence dimensionality
            routed_x = routed_flat.view(B, N, D)
            plane_probs = plane_probs_flat.view(B, N, -1)
            intent_probs = intent_probs_flat.view(B, N, -1)
            base_coord = base_coord_flat.view(B, N, -1)
            angles = angles_flat.view(B, N, -1)
            rays = {k: v.view(B, N, -1) for k, v in rays_flat.items()}
            cause_vec = cause_flat.view(B, N, -1)
            effect_vec = effect_flat.view(B, N, -1)
            z_val = z_val_flat.view(B, N)

            res = {
                "attended_x": attended_x,
                "routed_embed": routed_x,
                "plane_probs": plane_probs,
                "intent_probs": intent_probs,
                "base_coord": base_coord,
                "angles": angles,
                "rays": rays,
                "cause_vec": cause_vec,
                "effect_vec": effect_vec,
                "z_causal": z_val
            }
            if return_diagnostics:
                res["gluon_diagnostics"] = gluon_diag
                res["belief_diagnostics"] = self.belief_head(attended_x)

                # Dynamic Trajectory & Ribosomal Reading Diagnostics
                traj_diag = self.trajectory_integrator(attended_x)
                reading_diag = self.reading_head(attended_x, traj_diag)
                forces_diag = self.color_forces(traj_diag["modal_probs"], traj_diag["topic_weights"])
                insolvency_diag = self.insolvency_loss_fn(traj_diag, reading_diag)

                res["trajectory_diagnostics"] = {
                    "trajectory": traj_diag,
                    "reading_head": reading_diag,
                    "color_forces": forces_diag,
                    "derivation_completeness": insolvency_diag
                }
            return res
        else:
            routed_x, plane_probs, intent_probs = self.router(x)
            base_coord, angles, rays = self.modal_heads(routed_x)
            cause_vec, effect_vec, z_val = self.causal_head(routed_x)
            
            res = {
                "routed_embed": routed_x,
                "plane_probs": plane_probs,
                "intent_probs": intent_probs,
                "base_coord": base_coord,
                "angles": angles,
                "rays": rays,
                "cause_vec": cause_vec,
                "effect_vec": effect_vec,
                "z_causal": z_val
            }
            if return_diagnostics:
                res["belief_diagnostics"] = self.belief_head(routed_x)
            return res

class GeodesicLoss(nn.Module):
    """
    Multi-Objective Geometric Loss:
      1. Quadrant Loss: Forces can_be into (+υ, +ψ), is_not into (-υ, +ψ), etc.
      2. Antipodal Negation Loss: Forces is_not to oppose IS along the boundary axis.
      3. Causal Loss: Enforces z < 0 for causes and z > 0 for effects.
      4. Angular Shearing Loss: Penalizes misalignment with target SO(3) roll/pitch/yaw.
    """
    def __init__(self):
        super().__init__()

    def forward(self, outputs, target_quadrant, target_z):
        """
        outputs: dictionary from FractalPolytropeTransformer
        target_quadrant: int tensor [0..3]
        target_z: float tensor representing causal ground truth
        """
        base_coord = outputs["base_coord"] # [batch, 3] -> (υ, ψ, z)
        rays = outputs["rays"]
        z_causal = outputs["z_causal"]
        
        # 1. Target anchors for the 4 rays
        # can_be:   υ > 0, ψ > 0
        # is_not:   υ < 0, ψ > 0
        # is_like:  υ > 0, ψ < 0
        # was_like: υ < 0, ψ < 0
        loss_can_be = F.relu(0.5 - rays["can_be"][:, 0]).mean() + F.relu(0.5 - rays["can_be"][:, 1]).mean()
        loss_is_not = F.relu(0.5 + rays["is_not"][:, 0]).mean() + F.relu(0.5 - rays["is_not"][:, 1]).mean()
        loss_is_like = F.relu(0.5 - rays["is_like"][:, 0]).mean() + F.relu(0.5 + rays["is_like"][:, 1]).mean()
        loss_was_like = F.relu(0.5 + rays["was_like"][:, 0]).mean() + F.relu(0.5 + rays["was_like"][:, 1]).mean()
        
        quadrant_loss = loss_can_be + loss_is_not + loss_is_like + loss_was_like
        
        # 2. Antipodal Negation: IS and IS_NOT must have negative dot product along υ
        antipodal_loss = F.relu(0.5 + (base_coord[:, 0] * rays["is_not"][:, 0])).mean()
        
        # 3. Causal Loss: match target_z
        causal_loss = F.mse_loss(z_causal, target_z)
        
        total_loss = quadrant_loss + 2.0 * antipodal_loss + causal_loss
        return total_loss, {
            "quadrant_loss": float(quadrant_loss.item()),
            "antipodal_loss": float(antipodal_loss.item()),
            "causal_loss": float(causal_loss.item())
        }


# ==============================================================================
# SEMANTIC GLUON ATTENTION ARCHITECTURE (Gen 7 Master Synthesis)
# Pre-softmax modified attention logit matrix:
# S_{ij} = ( (Q_i K_j^T) / sqrt(d_k) + M_{ij}^{valence} - V_Cornell(r_{ij}) - Gamma_friction(P_i, P_j) ) * exp(-tau_{ij}) + M_{ij}^{splicing}
# Attention(Q, K, V) = softmax(S) V
# ==============================================================================

def build_canonical_gauge_friction_matrix() -> torch.Tensor:
    """
    Constructs the canonical 7x7 Gauge Friction Matrix Gamma(Q_p, Q_q)
    for the 7 Planes of Reality:
        0: Q1 Who (Metaphysical) - Driver / 7th Angle Axis
        1: Q2 What (Possible / +x)
        2: Q3 Where (Physical / -x)
        3: Q4 Why (Lyrical / +y)
        4: Q5 How (Logical / -y)
        5: Q6 Cause (Historical / +z)
        6: Q7 Effect (Emotive / -z)
    """
    G = torch.zeros(7, 7, dtype=torch.float32)
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
                G[p, q] = 0.5  # Intra-plane resonance
            else:
                dist = torch.norm(plane_coords[p] - plane_coords[q], p=1).item()
                G[p, q] = 1.0 + 0.25 * dist

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
    Allows fast dynamic pruning of conversational filler and strict zero leakage.
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


class OrientedGluonFluxBondHead(nn.Module):
    """
    Oriented Gluon Flux Bond Head:
    Unifies the 5' -> 3' directional phosphodiester causal backbone with
    the QCD Cornell Confinement potential.
    
    The Gluon Flux Tube forms between:
      - 5' Egress Source (Token j, F_j in R^{d_v})
      - 3' Ingress Sink   (Token i, B_i in R^{d_v})
    
    Governed by:
      G_{ij}^{flux} = ( (B_i . F_j) / sqrt(d_v) ) * Theta(5' -> 3') - V_Cornell(r_{ij}) - Delta_snap
    
    Where:
      - Theta(5' -> 3'): 0.0 for causal forward/coincident flow (i >= j), -2.0 for reverse unphysical leaps (j > i)
      - V_Cornell(r_ij) = -alpha_s / (r_ij + eps) + sigma * r_ij along the causal Z-axis (|z_i - z_j|)
      - Delta_snap: sharp repulsive barrier when r_ij >= r_critical (1.529), severing the flux bond
      - Open Bond Penalty: penalizes unclosed ingress B_i (dangling 3' bond without 5' root)
    """
    def __init__(
        self,
        embed_dim: int = 384,
        valence_dim: int = 64,
        alpha_s: float = 0.35,
        sigma: float = 0.85,
        r_critical: float = 1.529,
        eps: float = 1e-4
    ):
        super().__init__()
        self.valence_dim = valence_dim
        self.r_critical = r_critical
        self.eps = eps

        # 5' Egress & 3' Ingress projections
        self.ingress_proj = nn.Linear(embed_dim, valence_dim, bias=False)
        self.egress_proj = nn.Linear(embed_dim, valence_dim, bias=False)
        
        # Causal Z-axis projection for Cornell potential
        self.z_head = nn.Linear(embed_dim, 1)
        self.alpha_s = nn.Parameter(torch.tensor(alpha_s))
        self.sigma = nn.Parameter(torch.tensor(sigma))
        self.dangle_penalty_scale = nn.Parameter(torch.tensor(0.2))

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        x: [B, N, D]
        Returns:
            B_ingress: [B, N, valence_dim]
            F_egress:  [B, N, valence_dim]
            z_causal:  [B, N]
            V_cornell: [B, N, N]
            snapped_mask: [B, N, N]
            G_flux_bond: [B, N, N] unified oriented gluon bond matrix
        """
        B, N, D = x.shape
        B_ingress = self.ingress_proj(x)
        F_egress = self.egress_proj(x)
        z = self.z_head(x).squeeze(-1)

        # 1. Scaled dot-product color-anticolor pairing: (B_i . F_j) / sqrt(d_v)
        M_color = torch.bmm(B_ingress, F_egress.transpose(1, 2)) / math.sqrt(self.valence_dim)

        # 2. 5' -> 3' Directional backbone orientation
        indices = torch.arange(N, device=x.device)
        causal_order = (indices.unsqueeze(0) - indices.unsqueeze(1))  # i - j
        chiral_mask = torch.where(causal_order >= 0, torch.zeros_like(M_color), -2.0 * torch.ones_like(M_color))

        # 3. Cornell Confinement along causal Z (bounded regulator to prevent Coulomb singularity)
        r_ij = torch.abs(z.unsqueeze(2) - z.unsqueeze(1))  # [B, N, N]
        r_bounded = torch.clamp(r_ij, min=0.1)
        alpha = F.relu(self.alpha_s) + 1e-5
        sig = F.relu(self.sigma) + 1e-5
        coulomb = -alpha / (r_bounded + self.eps)
        string_tension = sig * r_ij
        V_cornell = coulomb + string_tension

        # 4. String Snapping at r_critical (1.529)
        snapped_mask = (r_ij >= self.r_critical)
        snap_barrier = torch.where(snapped_mask, 5.0 * (r_ij - self.r_critical).pow(2) + 2.0, torch.zeros_like(r_ij))

        # 5. Dangling Bond Penalty (unclosed 3' ingress without preceding 5' root)
        dangle_scale = F.softplus(self.dangle_penalty_scale)
        open_bond_penalty = torch.norm(B_ingress, dim=-1, keepdim=True) * 0.05

        # Unified Oriented Gluon Flux Bond (smooth physical scaling)
        G_flux_bond = (M_color + chiral_mask) - (0.2 * V_cornell) - snap_barrier - (dangle_scale * open_bond_penalty)

        return B_ingress, F_egress, z, V_cornell, snapped_mask, G_flux_bond


class CausalValenceHead(nn.Module):
    """
    Computes Ingress (B_i) and Egress (F_j) vectors for backward compatibility.
    """
    def __init__(self, embed_dim: int = 384, valence_dim: int = 64):
        super().__init__()
        self.gluon_bond = OrientedGluonFluxBondHead(embed_dim=embed_dim, valence_dim=valence_dim)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        B_ingress, F_egress, z, V_cornell, snapped_mask, G_flux = self.gluon_bond(x)
        return B_ingress, F_egress, G_flux


class CornellConfinementHead(nn.Module):
    """
    Computes Cornell Confinement along causal Z for backward compatibility.
    """
    def __init__(self, embed_dim: int = 384, alpha_s: float = 0.35, sigma: float = 0.85, r_critical: float = 1.529):
        super().__init__()
        self.gluon_bond = OrientedGluonFluxBondHead(embed_dim=embed_dim, alpha_s=alpha_s, sigma=sigma, r_critical=r_critical)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        B_ingress, F_egress, z, V_cornell, snapped_mask, G_flux = self.gluon_bond(x)
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
        plane_probs = F.softmax(plane_logits, dim=-1)
        G = F.relu(self.friction_tensor)
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
        node_tau = self.opacity_proj(x).squeeze(-1)
        tau_ij = self.tau_0 * 0.5 * (node_tau.unsqueeze(2) + node_tau.unsqueeze(1))
        luminescence = torch.exp(-tau_ij)
        return tau_ij, luminescence


class BeliefStateDiagnosticHead(nn.Module):
    """
    Belief State Diagnostic Head:
    Tracks the assumed belief state held within documents and sentences,
    derived from 'The Unbelievable Truth: A Reader's Guide' and the VFT Cognitive Framework.
    
    Evaluates:
      1. Operational Vector (V in [0, 1]): Physical possibility / empirical constraint (Q3 Physical).
      2. Cognitive Assumption (A in [0, 1]): Worldview expectation / modeled possibility (Q2 What).
      3. Assertion State (S in [0, 1]): Declared truth polarity (1 = Asserted True, 0 = Asserted False).
      4. Reality Strain: eta = |V - A|
           - eta < 0.2: Igneous Stone (reality-hardened coherence)
           - eta > 0.6: Fired Brick (brittle dogma / delusion)
      5. 4 Framework Verdicts:
           - Sane (Progressive): V=1, A=1 (Productive execution; work succeeds)
           - Sane (Calibrated):  V=0, A=0 (Accurate boundary awareness; energy preserved)
           - Insane (Delusional): V=0, A=1 (Collapse against physical constraints; perpetual motion fallacy)
           - Insane (Dogmatic):   V=1, A=0 (Orthodoxy denies functional anomalies to preserve doctrine)
      6. Worldview Scope & Resistance (The E = mc^2 Psychological Field):
           - Scientific Knowledge (SK) vs Spiritual Knowledge (SpK)
           - Resistance = (SK / SpK) + (SpK / SK)
           - Scope = 1 / Resistance in (0, 0.5] (Maximum Scope = 0.5 at SK = SpK)
           - Answer = Idea Mass (m) * Scope:
               Answer == 1.0 -> Truth (The "Click" / Amazing)
               Answer < 1.0  -> Lie / Miss (or Funny near-miss paradox)
               Answer > 1.0  -> Insult / Attack (High emotional energy collision)
      7. 6 Personal Belief States:
           - Truth (=), Will to Know (+?), Lie (<), Indifferent (~?), Insult (>), Will Not to Know (-?)
    """
    def __init__(self, embed_dim: int = 384):
        super().__init__()
        self.embed_dim = embed_dim

        # Operational Vector Head (V: physical possibility from Q3 grounding)
        self.v_head = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.GELU(),
            nn.Linear(embed_dim // 4, 1),
            nn.Sigmoid()
        )

        # Cognitive Assumption Head (A: modeled possibility from Q2 expectation)
        self.a_head = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.GELU(),
            nn.Linear(embed_dim // 4, 1),
            nn.Sigmoid()
        )

        # Assertion Polarity Head (S: asserted true vs asserted false)
        self.assertion_head = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.GELU(),
            nn.Linear(embed_dim // 4, 1),
            nn.Sigmoid()
        )

        # Scientific Knowledge (SK) vs Spiritual Knowledge (SpK) heads for Worldview Scope
        self.sk_head = nn.Linear(embed_dim, 1)
        self.spk_head = nn.Linear(embed_dim, 1)

        # Idea Mass Head (m)
        self.mass_head = nn.Linear(embed_dim, 1)

        # 6 Personal Belief States classifier
        # 0: Truth (=), 1: Will to Know (+?), 2: Lie (<), 3: Indifferent (~?), 4: Insult (>), 5: Will Not to Know (-?)
        self.belief_state_classifier = nn.Linear(embed_dim, 6)

    def forward(self, x: torch.Tensor) -> Dict[str, Union[torch.Tensor, Dict[str, torch.Tensor]]]:
        """
        x: [B, D] or [B, N, D]
        """
        v = self.v_head(x).squeeze(-1)
        a = self.a_head(x).squeeze(-1)
        s = self.assertion_head(x).squeeze(-1)

        # Reality Strain eta = |V - A|
        eta = torch.abs(v - a)

        # 4 Framework Verdict Probabilities
        p_sane_progressive = v * a
        p_sane_calibrated = (1.0 - v) * (1.0 - a)
        p_insane_delusional = (1.0 - v) * a
        p_insane_dogmatic = v * (1.0 - a)

        # Worldview Scope & Resistance: E = mc^2
        sk = F.softplus(self.sk_head(x).squeeze(-1)) + 0.1
        spk = F.softplus(self.spk_head(x).squeeze(-1)) + 0.1
        resistance = (sk / spk) + (spk / sk)
        scope = 1.0 / resistance
        mass = F.softplus(self.mass_head(x).squeeze(-1)) + 0.1
        answer_energy = mass * scope

        # 6 Personal Belief States logits & probabilities
        belief_logits = self.belief_state_classifier(x)
        belief_probs = F.softmax(belief_logits, dim=-1)

        return {
            "operational_vector_v": v,
            "cognitive_assumption_a": a,
            "assertion_polarity_s": s,
            "reality_strain_eta": eta,
            "verdict_probs": {
                "sane_progressive": p_sane_progressive,
                "sane_calibrated": p_sane_calibrated,
                "insane_delusional": p_insane_delusional,
                "insane_dogmatic": p_insane_dogmatic
            },
            "worldview": {
                "sk": sk,
                "spk": spk,
                "resistance": resistance,
                "scope": scope,
                "mass": mass,
                "answer_energy": answer_energy
            },
            "belief_state_probs": belief_probs
        }


class SemanticGluonAttention(nn.Module):
    """
    Semantic Gluon Attention Layer (nn.Module).
    Implements the full unified Gen 7 equation with Ribosomal Exon Splicing,
    Oriented 5' -> 3' Gluon Flux Bonds (Causal Valence + Cornell Confinement),
    7-Planes Reality Gauge Friction, and Optical Luminescence Attenuation.
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
        # Unified Oriented 5' -> 3' Gluon Flux Bond Head
        self.gluon_bond_head = OrientedGluonFluxBondHead(
            embed_dim=embed_dim,
            valence_dim=valence_dim,
            alpha_s=alpha_s,
            sigma=sigma,
            r_critical=r_critical
        )
        self.gauge_head = GaugeFrictionHead(embed_dim=embed_dim, num_planes=7)
        self.luminescence_head = LuminescenceAttenuationHead(embed_dim=embed_dim, tau_0=tau_0)

        # Balancing scale parameters (learned)
        self.gluon_bond_weight = nn.Parameter(torch.tensor(0.4))
        self.friction_weight = nn.Parameter(torch.tensor(0.3))

    def compute_splicing_mask(
        self,
        exon_probs: torch.Tensor,
        external_exon_mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        if external_exon_mask is not None:
            binary_mask = external_exon_mask.float()
        else:
            binary_mask = (exon_probs >= self.splicing_threshold).float()

        exon_pair = binary_mask.unsqueeze(2) * binary_mask.unsqueeze(1)
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
        B, N, D = x.shape

        q = self.q_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)

        s_base = torch.matmul(q, k.transpose(-2, -1)) * self.scale

        exon_probs = self.splicing_gate(x)
        splicing_mask, binary_exon_mask = self.compute_splicing_mask(exon_probs, exon_mask)

        # Oriented 5' -> 3' Gluon Flux Bond (Valence + Cornell Confinement)
        B_ingress, F_egress, z, V_cornell, snapped_mask, G_flux_bond = self.gluon_bond_head(x)
        G_flux_expanded = G_flux_bond.unsqueeze(1)

        plane_probs, gamma_friction = self.gauge_head(x)
        gamma_expanded = gamma_friction.unsqueeze(1)

        tau_ij, luminescence = self.luminescence_head(x)
        luminescence_expanded = luminescence.unsqueeze(1)

        w_gluon = F.softplus(self.gluon_bond_weight)
        w_fric = F.softplus(self.friction_weight)

        s_physical = s_base + (w_gluon * G_flux_expanded) - (w_fric * gamma_expanded)
        s_modulated = s_physical * luminescence_expanded
        s_final = s_modulated + splicing_mask

        attn_weights = F.softmax(s_final, dim=-1)
        attn_dropped = self.attn_dropout(attn_weights)

        context = torch.matmul(attn_dropped, v)
        context = context.transpose(1, 2).contiguous().view(B, N, D)
        output = self.proj_dropout(self.out_proj(context))

        if not return_diagnostics:
            return output

        diagnostics = {
            "attn_weights": attn_weights,
            "s_final": s_final,
            "exon_probs": exon_probs,
            "binary_exon_mask": binary_exon_mask,
            "B_ingress": B_ingress,
            "F_egress": F_egress,
            "M_valence": G_flux_bond,
            "G_flux_bond": G_flux_bond,
            "z_causal": z,
            "V_cornell": V_cornell,
            "snapped_mask": snapped_mask,
            "plane_probs": plane_probs,
            "gamma_friction": gamma_friction,
            "tau_ij": tau_ij,
            "luminescence": luminescence,
        }
        return output, diagnostics

    def forward_sparse_spliced(
        self,
        x: torch.Tensor,
        exon_mask: torch.Tensor
    ) -> Tuple[torch.Tensor, float]:
        """
        High-efficiency Vectorized Sparse Ribosomal Splicing Forward Pass.
        Extracts coding exons across the batch into a compact sub-tensor [B, K_max, D],
        runs multi-head attention in parallel over K_max <= N, and scatters outputs back.
        """
        B, N, D = x.shape
        device = x.device

        counts = (exon_mask > 0.5).sum(dim=1)
        k_max = int(counts.max().item())

        if k_max == 0:
            return x.clone(), 1.0

        if k_max == N:
            out = self.forward(x, exon_mask=exon_mask, return_diagnostics=False)
            return out, 1.0

        _, sorted_indices = torch.sort((exon_mask > 0.5).long(), dim=1, descending=True)
        exon_indices = sorted_indices[:, :k_max]

        batch_idx = torch.arange(B, device=device).unsqueeze(1).expand(B, k_max)
        x_spliced = x[batch_idx, exon_indices]

        compact_mask = torch.arange(k_max, device=device).unsqueeze(0).expand(B, k_max) < counts.unsqueeze(1)
        compact_mask = compact_mask.float()

        out_spliced = self.forward(x_spliced, exon_mask=compact_mask, return_diagnostics=False)

        output = torch.zeros_like(x)
        output.copy_(x)
        output[batch_idx, exon_indices] = out_spliced

        theoretical_speedup = float(N * N) / max(float(k_max * k_max), 1.0)
        return output, theoretical_speedup

    def compute_auxiliary_losses(
        self,
        diagnostics: Dict[str, torch.Tensor],
        target_exons: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        attn = diagnostics["attn_weights"].mean(dim=1)
        snapped = diagnostics["snapped_mask"].float()
        gamma = diagnostics["gamma_friction"]
        exon_probs = diagnostics["exon_probs"]

        # 1. Confinement Loss: Penalize attention across snapped flux strings
        confinement_loss = (attn * snapped).sum(dim=-1).mean()

        # 2. Gauge Friction Loss: Penalize attention across high-friction inverted plane leaps
        high_friction_mask = (gamma >= 2.0).float()
        gauge_friction_loss = (attn * gamma * high_friction_mask).sum(dim=-1).mean()

        # 3. Causal Valence Loss: Egress obligations should be resolved downstream
        F_norm = torch.norm(diagnostics["F_egress"], dim=-1)
        seq_len = attn.size(1)
        causal_triu = torch.triu(torch.ones(seq_len, seq_len, device=attn.device), diagonal=0)
        received_attn = (attn * causal_triu).sum(dim=1)
        valence_loss = (F_norm * torch.exp(-received_attn)).mean()

        # 4. Splicing Loss: Supervised or Sparsity
        if target_exons is not None:
            splicing_loss = F.binary_cross_entropy(exon_probs, target_exons.float())
        else:
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


# ==============================================================================
# DYNAMIC TRAJECTORY & RIBOSOMAL READING HEAD SYNTHESIS (Cook-Off Master Synthesis)
# Operationalizing Sections 2, 3, 4, 5, 6 of:
# Semantic_Gluon_and_Dynamic_Trajectory_Theory.md
# ==============================================================================

class DynamicTrajectoryIntegrator(nn.Module):
    """
    Section 5 of Semantic Gluon & Dynamic Trajectory Theory:
    Models continuous document motion through topic space via path integral:
        Sigma_D = integral_0^1 w(t) * sigma(t) dt ≈ sum_t w(t) * sigma(t)
    
    Instantaneous operational charge vector:
        sigma(t) = [c(t), p(t), r(t), g(t)]^T in Delta^3
        - c(t): Constructive (Solution + Counteractive: is like / may be)
        - p(t): Productive   (Solution + Active:        will be / can be)
        - r(t): Reductive    (Problem + Active:         can't be / is not)
        - g(t): Regressive   (Problem + Counteractive:  won't be / was like)

    Outputs:
        - Sigma_D: Integrated operational charge [B, 4]
        - magnitude_D: ||Sigma_D|| = sqrt(C^2 + P^2 + R^2 + G^2)
        - polarity_iota: ((C + P) - (R + G)) / (C + P + R + G + eps) in [-1, +1]
        - arbiter_entropy: Shannon entropy across the 4 engines
        - sigma_t: Instantaneous charge tensor [B, N, 4]
        - modal_probs: 8-modal probabilities [B, N, 8]
        - topic_weights: Continuous attention weights w(t) [B, N]
    """
    def __init__(self, embed_dim: int = 384, num_modals: int = 8, num_engines: int = 4):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_modals = num_modals
        self.num_engines = num_engines

        # Direct engine projection head
        self.engine_head = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 2),
            nn.GELU(),
            nn.Linear(embed_dim // 2, num_engines)
        )

        # 8-Modal boundary state head:
        # 0: will_be, 1: can_be, 2: can't_be, 3: is_not,
        # 4: won't_be, 5: was_like, 6: may_be, 7: is_like
        self.modal_head = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 2),
            nn.GELU(),
            nn.Linear(embed_dim // 2, num_modals)
        )

        # Continuous topical attention weight head w(t)
        self.attn_head = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 4),
            nn.Tanh(),
            nn.Linear(embed_dim // 4, 1)
        )

        # Invariant mapping matrix from 8 Modals to 4 Engines [8, 4]:
        # Productive:   will_be (0), can_be (1)
        # Reductive:    can't_be (2), is_not (3)
        # Regressive:   won't_be (4), was_like (5)
        # Constructive: may_be (6), is_like (7)
        mapping = torch.zeros(num_modals, num_engines)
        mapping[0, 1] = 1.0  # will_be -> P
        mapping[1, 1] = 1.0  # can_be  -> P
        mapping[2, 2] = 1.0  # can't_be -> R
        mapping[3, 2] = 1.0  # is_not   -> R
        mapping[4, 3] = 1.0  # won't_be -> G
        mapping[5, 3] = 1.0  # was_like -> G
        mapping[6, 0] = 1.0  # may_be   -> C
        mapping[7, 0] = 1.0  # is_like  -> C
        self.register_buffer("modal_to_engine", mapping)

    def forward(
        self,
        x: torch.Tensor,
        time_grid: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        x: [B, N, D] sequence tensor
        time_grid: optional [B, N] normalized sequence timestamps in [0, 1]
        """
        B, N, D = x.shape
        device = x.device

        # 1. Instantaneous 8-modal probabilities
        modal_logits = self.modal_head(x)  # [B, N, 8]
        modal_probs = F.softmax(modal_logits, dim=-1)

        # 2. Instantaneous 4-engine operational charges
        engine_logits = self.engine_head(x)  # [B, N, 4]
        engine_direct = F.softmax(engine_logits, dim=-1)
        engine_from_modals = torch.einsum('bni,ie->bne', modal_probs, self.modal_to_engine)
        sigma_t = 0.5 * (engine_direct + engine_from_modals)  # [B, N, 4] in Delta^3

        # 3. Path integral attention weights w(t)
        attn_scores = self.attn_head(x).squeeze(-1)  # [B, N]
        topic_weights = F.softmax(attn_scores, dim=-1)  # [B, N]

        # 4. Total Bond Tensor Path Integral Sigma_D = sum_t w(t) * sigma(t)
        Sigma_D = torch.einsum('bn,bne->be', topic_weights, sigma_t)  # [B, 4]
        C, P, R, G = Sigma_D[:, 0], Sigma_D[:, 1], Sigma_D[:, 2], Sigma_D[:, 3]

        # 5. Connection Magnitude ||Sigma_D|| = sqrt(C^2 + P^2 + R^2 + G^2)
        magnitude_D = torch.sqrt(torch.sum(Sigma_D.pow(2), dim=-1) + 1e-8)  # [B]

        # 6. Inclusive-Exclusive Polarity iota_D in [-1, +1]
        # Inclusive: C + P; Exclusive: R + G
        inclusive = C + P
        exclusive = R + G
        polarity_iota = (inclusive - exclusive) / (inclusive + exclusive + 1e-8)  # [B]

        # 7. Arbiter Entropy across 4 engines
        arbiter_entropy = -torch.sum(Sigma_D * torch.log(Sigma_D + 1e-8), dim=-1)  # [B]

        return {
            "Sigma_D": Sigma_D,
            "magnitude_D": magnitude_D,
            "polarity_iota": polarity_iota,
            "arbiter_entropy": arbiter_entropy,
            "sigma_t": sigma_t,
            "modal_probs": modal_probs,
            "topic_weights": topic_weights,
            "C": C, "P": P, "R": R, "G": G
        }


class ComplexityWaveEstimator(nn.Module):
    """
    Section 6.3 of Semantic Gluon & Dynamic Trajectory Theory:
    Measures document complexity wave H(t) and entropy convergence vs fragmentation:
        H(t) = -sum_k p_k(t) log(p_k(t) + eps)
    Calculates:
        - linear drift slope beta = Cov(t, H) / Var(t) = dH/dt
        - convergence ratio rho = H_late / H_early
        - distinguishes axiomatic condensation (beta < 0, rho < 1.0)
          from chaotic fragmentation (beta > 0, rho > 1.0).
    """
    def __init__(self):
        super().__init__()

    def forward(
        self,
        probs: torch.Tensor,
        time_grid: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        probs: [B, N, K] probability distribution across topics or modals
        time_grid: [B, N] normalized timestamps in [0, 1]
        """
        B, N, K = probs.shape
        device = probs.device

        if time_grid is None:
            time_grid = torch.linspace(0.0, 1.0, N, device=device).unsqueeze(0).expand(B, N)

        # Instantaneous entropy H(t)
        H_t = -torch.sum(probs * torch.log(probs + 1e-8), dim=-1)  # [B, N]

        # Linear regression drift slope: beta = Cov(t, H) / Var(t)
        t_mean = time_grid.mean(dim=-1, keepdim=True)
        H_mean = H_t.mean(dim=-1, keepdim=True)

        cov_t_H = torch.sum((time_grid - t_mean) * (H_t - H_mean), dim=-1)  # [B]
        var_t = torch.sum((time_grid - t_mean).pow(2), dim=-1) + 1e-8       # [B]
        entropy_slope = cov_t_H / var_t                                     # [B]

        # Early vs Late entropy split (first third vs last third)
        split_idx = max(N // 3, 1)
        h_early = H_t[:, :split_idx].mean(dim=-1)
        h_late = H_t[:, -split_idx:].mean(dim=-1)
        delta_H = h_late - h_early
        convergence_ratio = h_late / (h_early + 1e-8)

        is_convergent = (entropy_slope < 0.0) & (convergence_ratio < 1.0)

        return {
            "H_t": H_t,
            "entropy_slope": entropy_slope,
            "h_early": h_early,
            "h_late": h_late,
            "delta_H": delta_H,
            "convergence_ratio": convergence_ratio,
            "is_convergent": is_convergent
        }


class RibosomalReadingHead(nn.Module):
    """
    Section 6 of Semantic Gluon & Dynamic Trajectory Theory:
    Biological ribosome analogy: scans sequentially through token representations,
    transcribing text into continuous and discrete Semantic DNA Codons:
        Codon_i = <Q_i in {C,P,R,G}, M_i in {8 Modals}, iota_i in [-1, +1], H_i>

    Maintains the causal cumulative working-out ledger with O(1) prefix sums:
        A_{<t} = sum_{s < t} sigma(s) (1-step causal shift)
    Computes antecedent working-out coverage:
        W_antecedent(t) = min(C_{<t}, R_{<t}, G_{<t}) (strict three-pillar requirement)
    Tracks Concept Survival Rate S_survival in [0, 1].
    """
    def __init__(self, embed_dim: int = 384, temperature: float = 1.0):
        super().__init__()
        self.embed_dim = embed_dim
        self.temperature = temperature
        self.complexity_estimator = ComplexityWaveEstimator()

    def forward(
        self,
        x: torch.Tensor,
        trajectory_outputs: Dict[str, torch.Tensor],
        hard_discrete: bool = False
    ) -> Dict[str, torch.Tensor]:
        """
        x: [B, N, D]
        trajectory_outputs: output dict from DynamicTrajectoryIntegrator
        """
        B, N, D = x.shape
        sigma_t = trajectory_outputs["sigma_t"]          # [B, N, 4]
        modal_probs = trajectory_outputs["modal_probs"]  # [B, N, 8]

        # 1. Discrete / Soft Codon Transcription via Gumbel-Softmax
        if self.training:
            modal_codons = F.gumbel_softmax(
                torch.log(modal_probs + 1e-8),
                tau=self.temperature,
                hard=hard_discrete,
                dim=-1
            )
        else:
            if hard_discrete:
                idx = torch.argmax(modal_probs, dim=-1)
                modal_codons = F.one_hot(idx, num_classes=8).float()
            else:
                modal_codons = modal_probs

        # Instantaneous Inclusive-Exclusive Polarity per codon
        # Inclusive: C (0) + P (1); Exclusive: R (2) + G (3)
        c_i = sigma_t[..., 0]
        p_i = sigma_t[..., 1]
        r_i = sigma_t[..., 2]
        g_i = sigma_t[..., 3]
        iota_codon = ((c_i + p_i) - (r_i + g_i)) / ((c_i + p_i + r_i + g_i) + 1e-8)  # [B, N]

        # Codon Shannon Entropy
        wave = self.complexity_estimator(modal_probs)
        h_codon = wave["H_t"]  # [B, N]

        # 2. Vectorized Causal Cumulative Working-Out Ledger A_{<t}
        # 1-step causal shift: token t cannot consume its own derivation
        cum_sigma = torch.cumsum(sigma_t, dim=1)  # [B, N, 4]
        zeros = torch.zeros(B, 1, 4, device=x.device)
        A_prior = torch.cat([zeros, cum_sigma[:, :-1, :]], dim=1)  # [B, N, 4]

        C_prior = A_prior[..., 0]
        P_prior = A_prior[..., 1]
        R_prior = A_prior[..., 2]
        G_prior = A_prior[..., 3]

        # Law II three-pillar antecedent working out: min(C, R, G)
        W_antecedent = torch.min(torch.min(C_prior, R_prior), G_prior)  # [B, N]

        # 3. Concept Survival Rate S_survival in [0, 1]
        # Concepts introduced in early inclusive phases that survive reductive stress
        # and emerge into productive realization
        split_idx = max(N // 2, 1)
        early_intro = (c_i[:, :split_idx] + p_i[:, :split_idx]).mean(dim=-1)
        late_prod = p_i[:, -split_idx:].mean(dim=-1)
        late_regress = g_i[:, -split_idx:].mean(dim=-1)

        concept_survival = (late_prod / (late_prod + late_regress + 1e-8)) * torch.clamp(early_intro, 0.0, 1.0)
        concept_survival = torch.clamp(concept_survival, 0.0, 1.0)  # [B]

        return {
            "modal_codons": modal_codons,
            "iota_codon": iota_codon,
            "h_codon": h_codon,
            "complexity_wave": wave,
            "A_prior": A_prior,
            "W_antecedent": W_antecedent,
            "C_prior": C_prior,
            "P_prior": P_prior,
            "R_prior": R_prior,
            "G_prior": G_prior,
            "concept_survival_rate": concept_survival
        }


class DerivationLawCompletenessLoss(nn.Module):
    """
    Sections 3 & 6 of Semantic Gluon & Dynamic Trajectory Theory:
    Mathematical detector of "Maths Without Working Out".
    
    Operational Derivation Law II (The Productive Law):
      "If you want to define IS as something that will be you must go through a productive process
       using what is not and is like opposing what it was like until it can be."
      L_insolvency_law2(t) = ReLU(P_target(t) - kappa * W_antecedent(t))

    Operational Derivation Law I (The Reductive Law):
      "If you want to define IS as something that can't be you must go through a reductive process
       using what it was like and can be opposing what its like until it's not."
      L_insolvency_law1(t) = ReLU(R_target(t) - kappa * min(C_{<t}, P_{<t}, G_{<t}))
    """
    def __init__(self, kappa: float = 1.0, alpha_law1: float = 0.0):
        super().__init__()
        self.kappa = nn.Parameter(torch.tensor(kappa, dtype=torch.float32))
        self.alpha_law1 = alpha_law1

    def forward(
        self,
        trajectory_outputs: Dict[str, torch.Tensor],
        reading_head_outputs: Dict[str, torch.Tensor]
    ) -> Dict[str, torch.Tensor]:
        modal_probs = trajectory_outputs["modal_probs"]  # [B, N, 8]
        W_antecedent = reading_head_outputs["W_antecedent"]  # [B, N]
        C_prior = reading_head_outputs["C_prior"]
        P_prior = reading_head_outputs["P_prior"]
        G_prior = reading_head_outputs["G_prior"]

        effective_kappa = F.softplus(self.kappa)

        # Law II: Productive Target = will_be (0) + 0.5 * can_be (1)
        p_target = modal_probs[..., 0] + 0.5 * modal_probs[..., 1]  # [B, N]
        insolvency_law2 = F.relu(p_target - effective_kappa * W_antecedent)  # [B, N]

        # Law I: Reductive Target = can't_be (2) + 0.5 * is_not (3)
        r_target = modal_probs[..., 2] + 0.5 * modal_probs[..., 3]  # [B, N]
        W_law1 = torch.min(torch.min(C_prior, P_prior), G_prior)
        insolvency_law1 = F.relu(r_target - effective_kappa * W_law1)

        loss_law2 = insolvency_law2.mean()
        loss_law1 = insolvency_law1.mean()
        total_insolvency = loss_law2 + self.alpha_law1 * loss_law1

        return {
            "total_insolvency_loss": total_insolvency,
            "law2_loss": loss_law2,
            "law1_loss": loss_law1,
            "insolvency_map": insolvency_law2,
            "p_target": p_target,
            "W_antecedent": W_antecedent
        }


class FourColoredGluonForces(nn.Module):
    """
    Section 4 of Semantic Gluon & Dynamic Trajectory Theory:
    Four distinct colored cross-vectors acting as gluon force carriers mediating
    quadrant interactions:
        1. 🔴 Red Force:     will be <-> can't be  and  is like <-> won't be
           (Active Opposition & Exclusion Strain - Critical Contradiction Flagger)
        2. 🟢 Green Force:   can be <-> is not  and  may be <-> was like
           (Possibility Testing & Negation Resolution - Research Gap Flagger)
        3. 🔵 Blue Force:    will be -> may be  and  won't be -> is not
           (Affirmative Realization Gap & Exclusion Pinning - Execution Maturity)
        4. 🟣 Magenta Force: is like -> can be  and  was like -> can't be
           (Analogical Elevation & Impossibility Locking - Rule Learning)
    """
    def __init__(self, embed_dim: int = 384):
        super().__init__()
        self.embed_dim = embed_dim

    def forward(
        self,
        modal_probs: torch.Tensor,
        topic_weights: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        modal_probs: [B, N, 8]
        8 Modals:
          0: will_be,  1: can_be,   2: can't_be, 3: is_not,
          4: won't_be, 5: was_like, 6: may_be,   7: is_like
        """
        m_will_be  = modal_probs[..., 0]
        m_can_be   = modal_probs[..., 1]
        m_cant_be  = modal_probs[..., 2]
        m_is_not   = modal_probs[..., 3]
        m_wont_be  = modal_probs[..., 4]
        m_was_like = modal_probs[..., 5]
        m_may_be   = modal_probs[..., 6]
        m_is_like  = modal_probs[..., 7]

        # 1. 🔴 Red Force (Active Opposition & Exclusion Strain)
        red_force = 0.5 * (
            (m_will_be * m_cant_be) +
            (m_is_like * m_wont_be)
        )  # [B, N]

        # 2. 🟢 Green Force (Possibility Testing & Negation Resolution)
        green_force = 0.5 * (
            (m_can_be * m_is_not) +
            (m_may_be * m_was_like)
        )  # [B, N]

        # 3. 🔵 Blue Force (Affirmative Realization Gap & Exclusion Pinning)
        blue_force = 0.5 * (
            (m_will_be * m_may_be) +
            (m_wont_be * m_is_not)
        )  # [B, N]

        # 4. 🟣 Magenta Force (Analogical Elevation & Impossibility Locking)
        magenta_force = 0.5 * (
            (m_is_like * m_can_be) +
            (m_was_like * m_cant_be)
        )  # [B, N]

        forces_tensor = torch.stack([red_force, green_force, blue_force, magenta_force], dim=1)  # [B, 4, N]

        if topic_weights is not None:
            # Integrate across document sequence
            integrated_forces = torch.einsum('bn,bcn->bc', topic_weights, forces_tensor)  # [B, 4]
        else:
            integrated_forces = forces_tensor.mean(dim=-1)  # [B, 4]

        return {
            "forces_tensor": forces_tensor,
            "integrated_forces": integrated_forces,
            "red_opposition": integrated_forces[:, 0],
            "green_testing": integrated_forces[:, 1],
            "blue_realization": integrated_forces[:, 2],
            "magenta_elevation": integrated_forces[:, 3]
        }

    def compute_semantic_git_shear(
        self,
        doc_a_modals: torch.Tensor,
        doc_b_modals: torch.Tensor
    ) -> torch.Tensor:
        """
        Section 7 (Case C: Semantic Merge Conflict):
        Measures contradiction shear between Document A and Document B.
        High shear when Doc A asserts 'will be' while Doc B asserts 'can't be'.
        """
        m_a_will = doc_a_modals[..., 0].mean(dim=-1)
        m_b_cant = doc_b_modals[..., 2].mean(dim=-1)
        m_b_will = doc_b_modals[..., 0].mean(dim=-1)
        m_a_cant = doc_a_modals[..., 2].mean(dim=-1)

        shear = (m_a_will * m_b_cant) + (m_b_will * m_a_cant)
        return shear


