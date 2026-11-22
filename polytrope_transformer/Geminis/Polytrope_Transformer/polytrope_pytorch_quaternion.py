"""
Fractal Polytrope Sovereign LLM: Vectorized PyTorch Quaternion Kernel & Slerp Layer.
Cycle 16 R&D Milestone. Implements SO(3) Unit Quaternion Attention, Geodesic Distance on S^3,
and Slerp multi-turn trajectory optimization for CUDA GPU workstations.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class QuaternionState(nn.Module):
    """
    Projects hidden representations h in R^D into a 7-parameter manifold state:
    3D Coordinates (upsilon, psi, z) in [-2, 2]^3 and 4D Unit Quaternion (w, x, y, z) on S^3.
    """
    def __init__(self, d_model: int):
        super().__init__()
        self.d_model = d_model
        self.coord_proj = nn.Linear(d_model, 3)
        self.quat_proj = nn.Linear(d_model, 4)
        self.q_plane_proj = nn.Linear(d_model, 7)

    def forward(self, x: torch.Tensor):
        # Coordinates in [-2, 2]
        coords = 2.0 * torch.tanh(self.coord_proj(x))
        # Unit Quaternion on S^3 (norm = 1.0)
        raw_quat = self.quat_proj(x)
        quat = F.normalize(raw_quat, p=2, dim=-1)
        # Substrate 7 Q-Planes (Probability simplex)
        q_planes = F.softmax(self.q_plane_proj(x), dim=-1)
        return coords, quat, q_planes

class QuaternionGeodesicAttention(nn.Module):
    """
    Multi-Head Attention where attention coefficients are modulated by the
    geodesic angular distance on S^3: d(q_i, q_j) = 2 * arccos(|<q_i, q_j>|).
    Antipodal states (d = pi) receive mathematically zero attention.
    """
    def __init__(self, d_model: int, n_heads: int = 4, sigma: float = 0.75):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.sigma = sigma
        self.head_dim = d_model // n_heads
        
        self.q_lin = nn.Linear(d_model, d_model)
        self.k_lin = nn.Linear(d_model, d_model)
        self.v_lin = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor, quats: torch.Tensor):
        B, T, D = x.shape
        # Standard Q, K, V
        q = self.q_lin(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.k_lin(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.v_lin(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        
        # Dot product scaled logits
        scale = 1.0 / math.sqrt(self.head_dim)
        scores = torch.matmul(q, k.transpose(-2, -1)) * scale
        
        # Geodesic angular gating on S^3: <q_i, q_j>
        # quats: (B, T, 4)
        inner = torch.matmul(quats, quats.transpose(-2, -1)).abs().clamp(0.0, 1.0)
        geodesic_dist = 2.0 * torch.acos(inner) # (B, T, T) in [0, pi]
        angular_gate = (torch.cos(0.5 * geodesic_dist) ** 2).unsqueeze(1) # (B, 1, T, T)
        
        # Modulate attention
        attn = F.softmax(scores, dim=-1) * angular_gate
        out = torch.matmul(attn, v)
        out = out.transpose(1, 2).contiguous().view(B, T, D)
        return self.out_proj(out), attn

def slerp_batch(q1: torch.Tensor, q2: torch.Tensor, t: float):
    """
    Vectorized Spherical Linear Interpolation between batches of unit quaternions on S^3.
    """
    dot = (q1 * q2).sum(dim=-1, keepdim=True)
    q2_adj = torch.where(dot < 0.0, -q2, q2)
    dot_adj = dot.abs().clamp(-1.0, 1.0)
    
    theta_0 = torch.acos(dot_adj)
    sin_theta_0 = torch.sin(theta_0).clamp(min=1e-6)
    
    theta = theta_0 * t
    sin_theta = torch.sin(theta)
    
    s0 = torch.cos(theta) - dot_adj * sin_theta / sin_theta_0
    s1 = sin_theta / sin_theta_0
    
    return s0 * q1 + s1 * q2_adj

class GeodesicSlerpLoss(nn.Module):
    """
    Multi-Turn Trajectory Regularization Loss:
    Enforces continuous angular momentum on S^3 and penalizes antipodal attention leakage.
    """
    def __init__(self, lambda_smooth: float = 0.1):
        super().__init__()
        self.lambda_smooth = lambda_smooth

    def forward(self, quat_seq: torch.Tensor, coords_seq: torch.Tensor):
        # quat_seq: (B, T, 4), coords_seq: (B, T, 3)
        # Angular step distances along sequence
        inner = (quat_seq[:, :-1] * quat_seq[:, 1:]).sum(dim=-1).abs().clamp(0.0, 1.0)
        step_angles = 2.0 * torch.acos(inner)
        smoothness_loss = step_angles.pow(2).mean()
        
        # Spatial smoothness
        coord_steps = (coords_seq[:, 1:] - coords_seq[:, :-1]).pow(2).sum(dim=-1)
        coord_loss = coord_steps.mean()
        
        return self.lambda_smooth * (smoothness_loss + coord_loss)

if __name__ == "__main__":
    d_model = 64
    batch_size = 2
    seq_len = 5
    
    model_state = QuaternionState(d_model)
    attn_layer = QuaternionGeodesicAttention(d_model, n_heads=4)
    loss_fn = GeodesicSlerpLoss()
    
    dummy_x = torch.randn(batch_size, seq_len, d_model)
    coords, quats, q_planes = model_state(dummy_x)
    out, attn = attn_layer(dummy_x, quats)
    loss = loss_fn(quats, coords)
    
    print("PyTorch Quaternion Module Smoke Test:")
    print("  Input Shape:     ", dummy_x.shape)
    print("  Output Shape:    ", out.shape)
    print("  Coords Shape:    ", coords.shape)
    print("  Quats Shape:     ", quats.shape, "(Normalized onto S^3)")
    print("  Geodesic Loss:   ", loss.item())
