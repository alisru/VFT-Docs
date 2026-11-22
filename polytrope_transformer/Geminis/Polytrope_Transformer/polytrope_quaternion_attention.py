"""
Fractal Polytrope Sovereign LLM: Continuous 3D Unit Quaternion Manifold Attention Engine.
Cycle 15 R&D Milestone. Implements SO(3) unit quaternion kinematics, Slerp geodesic interpolation,
geodesic attention distance on S^3, and closed-loop surface alias emission.
"""

import json
import re
import time
import numpy as np

# ============================================================================
# 1. CONTINUOUS 3D UNIT QUATERNION MANIFOLD ENGINE (SO(3))
# ============================================================================

class Quaternion:
    """
    Unit Quaternion q = (w, x, y, z) representing orientation in SO(3).
    w is the scalar real part; (x, y, z) is the vector imaginary part.
    """
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        v = np.array([w, x, y, z], dtype=np.float64)
        norm = np.linalg.norm(v)
        if norm < 1e-12:
            self.q = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
        else:
            self.q = v / norm

    @property
    def w(self): return self.q[0]
    @property
    def x(self): return self.q[1]
    @property
    def y(self): return self.q[2]
    @property
    def z(self): return self.q[3]

    @classmethod
    def from_axis_angle(cls, axis, angle_rad):
        axis = np.array(axis, dtype=np.float64)
        norm = np.linalg.norm(axis)
        if norm < 1e-12:
            return cls(1.0, 0.0, 0.0, 0.0)
        u = axis / norm
        half = angle_rad / 2.0
        return cls(np.cos(half), u[0] * np.sin(half), u[1] * np.sin(half), u[2] * np.sin(half))

    @classmethod
    def from_euler_angles(cls, roll, pitch, yaw):
        """
        roll  (theta_upsilon_psi) : rotation in boundary-kinetic plane (xy)
        pitch (theta_psi_z)       : rotation in kinetic-causal plane (yz)
        yaw   (theta_upsilon_z)   : rotation in boundary-causal plane (xz)
        """
        cr, cp, cy = np.cos(roll/2.0), np.cos(pitch/2.0), np.cos(yaw/2.0)
        sr, sp, sy = np.sin(roll/2.0), np.sin(pitch/2.0), np.sin(yaw/2.0)
        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy
        return cls(w, x, y, z)

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def multiply(self, other):
        w1, x1, y1, z1 = self.q
        w2, x2, y2, z2 = other.q
        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2
        return Quaternion(w, x, y, z)

    def to_rotation_matrix(self):
        w, x, y, z = self.q
        return np.array([
            [1.0 - 2.0*(y*y + z*z), 2.0*(x*y - z*w),       2.0*(x*z + y*w)],
            [2.0*(x*y + z*w),       1.0 - 2.0*(x*x + z*z), 2.0*(y*z - x*w)],
            [2.0*(x*z - y*w),       2.0*(y*z + x*w),       1.0 - 2.0*(x*x + y*y)]
        ], dtype=np.float64)

    def rotate_vector(self, v):
        R = self.to_rotation_matrix()
        return R @ np.array(v, dtype=np.float64)

    def geodesic_distance(self, other):
        """
        Geodesic distance on S^3: d(q1, q2) = 2 * arccos(|<q1, q2>|)
        """
        inner = np.clip(np.abs(np.dot(self.q, other.q)), 0.0, 1.0)
        return float(2.0 * np.arccos(inner))

    @staticmethod
    def slerp(q1, q2, t):
        """
        Spherical Linear Interpolation between two unit quaternions on S^3.
        """
        dot = np.dot(q1.q, q2.q)
        q2_arr = q2.q.copy()
        if dot < 0.0:
            q2_arr = -q2_arr
            dot = -dot
        dot = np.clip(dot, -1.0, 1.0)
        if dot > 0.9995:
            res = (1.0 - t) * q1.q + t * q2_arr
            return Quaternion(*res)
        theta_0 = np.arccos(dot)
        theta = theta_0 * t
        q_perp = q2_arr - q1.q * dot
        q_perp /= np.linalg.norm(q_perp)
        res = q1.q * np.cos(theta) + q_perp * np.sin(theta)
        return Quaternion(*res)

    def to_list(self):
        return [round(float(c), 6) for c in self.q]

# Canonical Modal Quaternions on S^3
MODAL_QUATERNIONS = {
    "PRODUCTIVE [can be]":   Quaternion.from_axis_angle([0, 0, 1], np.pi / 4.0),
    "REDUCTIVE [is not]":    Quaternion.from_axis_angle([0, 0, 1], 3.0 * np.pi / 4.0),
    "REGRESSIVE [was like]": Quaternion.from_axis_angle([0, 0, 1], -3.0 * np.pi / 4.0),
    "CONSTRUCTIVE [is like]": Quaternion.from_axis_angle([0, 0, 1], -np.pi / 4.0),
    "SINGULARITY [IS]":      Quaternion(1.0, 0.0, 0.0, 0.0)
}

# ============================================================================
# 2. CONTINUOUS QUATERNION ATTENTION KERNEL
# ============================================================================

class QuaternionAttentionKernel:
    """
    Evaluates Polyhedral Attention modulated by S^3 Geodesic Alignment.
    Guarantees that antipodal orientations receive zero attention:
    Attn(q1, q2) = GaussianOverlap(s1, R(q1 q2*) s2) * cos^2(0.5 * d_S3(q1, q2))
    """
    @staticmethod
    def compute_attention(s_i, q_i, s_j, q_j, sigma=0.75):
        s_i = np.array(s_i, dtype=np.float64)
        s_j = np.array(s_j, dtype=np.float64)
        
        q_rel = q_i.multiply(q_j.conjugate())
        s_j_rotated = q_rel.rotate_vector(s_j)
        
        dist_sq = np.sum((s_i - s_j_rotated) ** 2)
        spatial_overlap = np.exp(-dist_sq / (2.0 * sigma * sigma))
        
        d_s3 = q_i.geodesic_distance(q_j)
        angular_gate = (np.cos(0.5 * d_s3)) ** 2
        
        return float(spatial_overlap * angular_gate), float(d_s3)

# ============================================================================
# 3. CLOSED-LOOP SURFACE ALIAS EMISSION ENGINE
# ============================================================================

class SurfaceAliasEmissionEngine:
    """
    Operationalizes Section 8.2 of specification:
    Maps validated continuous manifold coordinates (upsilon, psi, z, Q1..Q7)
    into fluent natural-language surface propositions via AEC invariant matching.
    """
    INVARIANT_AEC_DICTIONARY = [
        {
            "id": "AEC_GOV_GROWTH",
            "prototype_coords": [0.45, 0.55, 0.15],
            "prototype_modal": "PRODUCTIVE [can be]",
            "primary_plane": "Q1",
            "aliases": [
                "The national government will deliver economic growth and support working families",
                "Executive policy expands economic opportunity for households",
                "Federal cabinet invests in living standards and social wage"
            ]
        },
        {
            "id": "AEC_TRANSPORT_AVIATION",
            "prototype_coords": [0.25, 0.45, 0.20],
            "prototype_modal": "PRODUCTIVE [can be]",
            "primary_plane": "Q3",
            "aliases": [
                "We need to make sure we can keep our planes in the air",
                "Aviation operations maintain active domestic transport links",
                "Essential flight services connect regional runways and airports"
            ]
        },
        {
            "id": "AEC_SKILL_SHORTAGE",
            "prototype_coords": [0.20, -0.10, -0.85],
            "prototype_modal": "CONSTRUCTIVE [is like]",
            "primary_plane": "Q2",
            "aliases": [
                "The problem is training enough Australian pilots to fulfil our domestic aviation needs",
                "Long-term workforce bottlenecks require domestic training pipelines",
                "Skilled pilot pipelines require months of structured flight instruction"
            ]
        },
        {
            "id": "AEC_ROAD_TOLL_CRISIS",
            "prototype_coords": [0.15, -0.35, 0.95],
            "prototype_modal": "CONSTRUCTIVE [is like]",
            "primary_plane": "Q7",
            "aliases": [
                "More people are dying on our roads with tragic consequences for families",
                "Fatal highway collisions inflict unbearable grief on regional communities",
                "Road trauma escalates holiday casualties across rural corridors"
            ]
        },
        {
            "id": "AEC_OPPOSITION_ATTACK",
            "prototype_coords": [-0.65, 0.40, -0.30],
            "prototype_modal": "REDUCTIVE [is not]",
            "primary_plane": "Q1",
            "aliases": [
                "The opposition claims the budget is failing without proposing alternative funding",
                "Adversarial scrutiny charges the executive with fiscal failure",
                "Opposition shadow ministers attack ministerial delivery"
            ]
        },
        {
            "id": "AEC_TRIPARTITE_REBALANCE",
            "prototype_coords": [0.14, 0.53, 0.16],
            "prototype_modal": "PRODUCTIVE [can be]",
            "primary_plane": "Q3",
            "aliases": [
                "Ministers co-invest in regional airport and highway safety with crossbench audit",
                "Tripartite accord funds essential transport upgrades with independent oversight",
                "Bipartisan infrastructure compact restores regional highway resilience"
            ]
        }
    ]

    @classmethod
    def emit_surface_text(cls, target_coords, q_dist, beam_width=3):
        target = np.array(target_coords, dtype=np.float64)
        q = np.array(q_dist, dtype=np.float64) / np.sum(q_dist)
        dominant_q = f"Q{np.argmax(q)+1}"
        
        candidates = []
        for entry in cls.INVARIANT_AEC_DICTIONARY:
            proto = np.array(entry["prototype_coords"], dtype=np.float64)
            dist = np.linalg.norm(target - proto)
            plane_match = 1.0 if entry["primary_plane"] == dominant_q else 0.5
            score = float(1.0 / (1.0 + dist) * plane_match)
            
            for alias in entry["aliases"]:
                candidates.append({
                    "aec_id": entry["id"],
                    "candidate_text": alias,
                    "target_coords": [round(float(c), 4) for c in target],
                    "prototype_coords": entry["prototype_coords"],
                    "euclidean_distance": round(float(dist), 4),
                    "plane_match": round(plane_match, 2),
                    "emission_score": round(score, 4)
                })
                
        candidates.sort(key=lambda x: x["emission_score"], reverse=True)
        return candidates[:beam_width]

if __name__ == "__main__":
    q_prod = MODAL_QUATERNIONS["PRODUCTIVE [can be]"]
    q_reg = MODAL_QUATERNIONS["REGRESSIVE [was like]"]
    attn, d = QuaternionAttentionKernel.compute_attention([1, 1, 0.5], q_prod, [1, 1, 0.5], q_reg)
    print("Quaternion Antipodal Attention:", attn, "Geodesic Distance:", d)
