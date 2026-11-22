"""
Fractal Polytrope Transformer Kernel: Prototype & Test Mockup
Implemented in pure Python & NumPy.
Includes: Single IS Entities, 4 Modal Derivations, Polyhedral Attention,
and IS Complex Comparison Engine.
"""

import numpy as np
import json
import time
from typing import List, Dict, Optional

class PolytropeEntity:
    def __init__(self, label, upsilon=0.0, psi=0.0, z=0.0, 
                 theta=(0.0, 0.0, 0.0), q_planes=None, radius=0.5):
        self.label = label
        self.upsilon = float(np.clip(upsilon, -2.0, 2.0))
        self.psi = float(np.clip(psi, -2.0, 2.0))
        self.z = float(np.clip(z, -2.0, 2.0))
        self.theta = np.array(theta, dtype=np.float64)
        if q_planes is None:
            self.q_planes = np.ones(7, dtype=np.float64) / 7.0
        else:
            q = np.array(q_planes, dtype=np.float64)
            self.q_planes = q / np.sum(q)
        self.radius = float(radius)
        self.cov = np.eye(3, dtype=np.float64) * (self.radius ** 2)

    @property
    def coords(self):
        return np.array([self.upsilon, self.psi, self.z], dtype=np.float64)

    def __repr__(self):
        return f"PolytropeEntity('{self.label}', υ={self.upsilon:.2f}, ψ={self.psi:.2f}, z={self.z:.2f})"

class ISComplex:
    def __init__(self, name: str, nodes: List[PolytropeEntity], edges: Optional[List[Dict]] = None):
        self.name = name
        self.nodes = nodes
        self.edges = edges or []
        
    @property
    def centroid(self):
        coords = np.array([n.coords for n in self.nodes])
        return np.mean(coords, axis=0)

    @property
    def aggregate_q(self):
        qs = np.array([n.q_planes for n in self.nodes])
        mean_q = np.mean(qs, axis=0)
        return mean_q / np.sum(mean_q)

    @property
    def bounding_cov(self):
        coords = np.array([n.coords for n in self.nodes])
        if len(coords) > 1:
            cov = np.cov(coords, rowvar=False) + np.eye(3) * 0.15
        else:
            cov = self.nodes[0].cov
        return cov

    def __repr__(self):
        c = self.centroid
        return f"ISComplex('{self.name}', {len(self.nodes)} nodes, centroid=[υ={c[0]:.2f}, ψ={c[1]:.2f}, z={c[2]:.2f}])"

class PolytropeAttentionKernel:
    def __init__(self, sigma_theta=0.5):
        self.sigma_theta = sigma_theta

    def compute_volume_overlap(self, e_i: PolytropeEntity, e_j: PolytropeEntity):
        mu_diff = e_i.coords - e_j.coords
        sigma_sum = e_i.cov + e_j.cov
        inv_sigma = np.linalg.inv(sigma_sum)
        dist_sq = mu_diff.T @ inv_sigma @ mu_diff
        det_i = np.linalg.det(e_i.cov)
        det_j = np.linalg.det(e_j.cov)
        det_sum = np.linalg.det(sigma_sum)
        prefactor = (2.0 ** 1.5) * (det_i * det_j) ** 0.25 / np.sqrt(det_sum)
        overlap = prefactor * np.exp(-0.5 * dist_sq)
        return float(np.clip(overlap, 0.0, 1.0))

    def compute_so3_alignment(self, e_i: PolytropeEntity, e_j: PolytropeEntity):
        diff = np.linalg.norm(e_i.theta - e_j.theta)
        return float(np.exp(- (diff ** 2) / (2.0 * (self.sigma_theta ** 2))))

    def compute_causal_asymmetry(self, e_query: PolytropeEntity, e_key: PolytropeEntity):
        delta_z = e_query.z - e_key.z
        if delta_z > 0:
            return float(1.0 / (1.0 + np.exp(-3.0 * (delta_z - 0.5))))
        else:
            return float(np.exp(5.0 * delta_z) * 0.001)

    def compute_substrate_conservation(self, e_i: PolytropeEntity, e_j: PolytropeEntity):
        bhattacharyya = np.sum(np.sqrt(e_i.q_planes * e_j.q_planes))
        high_plane_demand = e_j.q_planes[4]  # Q5 Logical
        phys_backing = e_j.q_planes[2]       # Q3 Physical
        if high_plane_demand > 0.6 and phys_backing < 0.05:
            penalty = 0.0
        else:
            penalty = 1.0
        return float(bhattacharyya * penalty)

    def passthrough_attention(self, query: PolytropeEntity, key: PolytropeEntity):
        vol_overlap = self.compute_volume_overlap(query, key)
        so3_align = self.compute_so3_alignment(query, key)
        causal_align = self.compute_causal_asymmetry(query, key)
        substrate_align = self.compute_substrate_conservation(query, key)
        total_passthrough = vol_overlap * so3_align * causal_align * substrate_align
        return {
            "total_passthrough": total_passthrough,
            "volume_overlap": vol_overlap,
            "so3_alignment": so3_align,
            "causal_alignment": causal_align,
            "substrate_alignment": substrate_align
        }

class ComplexComparisonKernel:
    def __init__(self, node_kernel: Optional[PolytropeAttentionKernel] = None):
        self.node_kernel = node_kernel or PolytropeAttentionKernel()

    def compare(self, c_A: ISComplex, c_B: ISComplex) -> Dict:
        nA, nB = len(c_A.nodes), len(c_B.nodes)
        attention_matrix = np.zeros((nA, nB), dtype=np.float64)
        for i, node_A in enumerate(c_A.nodes):
            for j, node_B in enumerate(c_B.nodes):
                res = self.node_kernel.passthrough_attention(node_A, node_B)
                attention_matrix[i, j] = res["total_passthrough"]
                
        delta_coords = c_B.centroid - c_A.centroid
        delta_upsilon = float(delta_coords[0])
        delta_psi = float(delta_coords[1])
        delta_z = float(delta_coords[2])
        
        mu_diff = c_A.centroid - c_B.centroid
        sigma_sum = c_A.bounding_cov + c_B.bounding_cov
        inv_sigma = np.linalg.inv(sigma_sum)
        dist_sq = mu_diff.T @ inv_sigma @ mu_diff
        det_A = np.linalg.det(c_A.bounding_cov)
        det_B = np.linalg.det(c_B.bounding_cov)
        det_sum = np.linalg.det(sigma_sum)
        prefactor = (2.0 ** 1.5) * (det_A * det_B) ** 0.25 / np.sqrt(det_sum)
        aggregate_overlap = float(np.clip(prefactor * np.exp(-0.5 * dist_sq), 0.0, 1.0))
        
        edge_match_count = 0
        total_checks = max(len(c_A.edges), len(c_B.edges), 1)
        if c_A.edges and c_B.edges:
            for e_A in c_A.edges:
                for e_B in c_B.edges:
                    if e_A.get("type") == e_B.get("type"):
                        edge_match_count += 1
            morphic_score = float(min(1.0, edge_match_count / total_checks))
        else:
            coord_corr = np.corrcoef(c_A.centroid, c_B.centroid)[0, 1]
            morphic_score = float(max(0.0, coord_corr) if not np.isnan(coord_corr) else 0.5)

        q_bhattacharyya = float(np.sum(np.sqrt(c_A.aggregate_q * c_B.aggregate_q)))
        
        if aggregate_overlap > 0.6 and morphic_score > 0.6:
            relationship = "ISOMORPHIC_CONSTRUCTIVE ([is like])"
        elif delta_upsilon < -1.0 or aggregate_overlap < 0.05:
            relationship = "CONTRADICTORY_EXCLUSIVE ([is not])"
        elif delta_z > 0.8:
            relationship = "CAUSAL_PROGRESSION (A causes B)"
        else:
            relationship = "SYSTEMIC_PERTURBATION"

        return {
            "complex_A": c_A.name,
            "complex_B": c_B.name,
            "relationship_classification": relationship,
            "aggregate_polyhedral_overlap": aggregate_overlap,
            "morphic_isomorphism_score": morphic_score,
            "substrate_alignment_q": q_bhattacharyya,
            "delta_vector": {
                "delta_upsilon": delta_upsilon,
                "delta_psi": delta_psi,
                "delta_z": delta_z
            },
            "node_attention_matrix": attention_matrix.tolist()
        }

class ModalDerivationEngines:
    @staticmethod
    def reductive_engine(can_be, was_like, is_like):
        return can_be + was_like - is_like

    @staticmethod
    def productive_engine(is_not, is_like, was_like):
        return is_not + is_like - was_like

    @staticmethod
    def regressive_engine(is_not, is_like, can_be):
        return is_not + is_like - can_be

    @staticmethod
    def constructive_engine(can_be, was_like, is_not):
        return can_be + was_like - is_not

class AdamOptimizer:
    def __init__(self, params, lr=0.02, beta1=0.9, beta2=0.999, eps=1e-8):
        self.params = params
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]
        self.t = 0

    def step(self, grads):
        self.t += 1
        for i in range(len(self.params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (grads[i] ** 2)
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            self.params[i] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

class TrainableGeometricHead:
    def __init__(self, d_in=16, d_hidden=32):
        np.random.seed(42)
        self.W1 = np.random.randn(d_in, d_hidden) * 0.15
        self.b1 = np.zeros(d_hidden)
        self.W2 = np.random.randn(d_hidden, 3) * 0.15
        self.b2 = np.zeros(3)
        self.params = [self.W1, self.b1, self.W2, self.b2]
        self.opt = AdamOptimizer(self.params, lr=0.03)

    def forward(self, X):
        self.X = X
        self.H = np.tanh(X @ self.W1 + self.b1)
        self.out = self.H @ self.W2 + self.b2
        return self.out

    def train_step(self, X, y_true, lambda_modal=0.5):
        pred = self.forward(X)
        mse_loss = np.mean((pred - y_true) ** 2)
        grad_pred = 2.0 * (pred - y_true) / len(X)
        
        if len(pred) >= 4:
            can_be = pred[0, :2]
            was_like = pred[1, :2]
            is_not = pred[2, :2]
            is_like = pred[3, :2]
            modal_loss = float(np.sum((can_be + was_like) ** 2) + np.sum((is_not + is_like) ** 2))
            grad_modal = np.zeros_like(pred)
            grad_modal[0, :2] += 2.0 * (can_be + was_like)
            grad_modal[1, :2] += 2.0 * (can_be + was_like)
            grad_modal[2, :2] += 2.0 * (is_not + is_like)
            grad_modal[3, :2] += 2.0 * (is_not + is_like)
            total_loss = mse_loss + lambda_modal * modal_loss
            grad_out = grad_pred + lambda_modal * grad_modal
        else:
            total_loss = mse_loss
            grad_out = grad_pred

        grad_W2 = self.H.T @ grad_out
        grad_b2 = np.sum(grad_out, axis=0)
        grad_H = grad_out @ self.W2.T
        grad_pre_H = grad_H * (1.0 - self.H ** 2)
        dW1 = self.X.T @ grad_pre_H
        db1 = np.sum(grad_pre_H, axis=0)
        self.opt.step([dW1, db1, grad_W2, grad_b2])
        return total_loss
