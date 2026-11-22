"""
Fractal Polytrope Sovereign LLM: Multi-Turn Slerp Geodesic Trajectory Tracker & Spin Sieve.
Cycle 16 R&D Milestone. Implements continuous Slerp trajectory tracking on S^3,
Rhetorical Pivot Analysis, and the Deception / Spin Evasion Index across parliamentary debates.
"""

import json
import re
import time
import numpy as np

# ============================================================================
# 1. CONTINUOUS 3D UNIT QUATERNION & SLERP KINEMATICS
# ============================================================================

class Quaternion:
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        v = np.array([w, x, y, z], dtype=np.float64)
        norm = np.linalg.norm(v)
        self.q = v / norm if norm > 1e-12 else np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)

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
        if norm < 1e-12: return cls(1.0, 0.0, 0.0, 0.0)
        u = axis / norm
        half = angle_rad / 2.0
        return cls(np.cos(half), u[0] * np.sin(half), u[1] * np.sin(half), u[2] * np.sin(half))

    @classmethod
    def from_euler(cls, roll, pitch, yaw):
        cr, cp, cy = np.cos(roll/2.0), np.cos(pitch/2.0), np.cos(yaw/2.0)
        sr, sp, sy = np.sin(roll/2.0), np.sin(pitch/2.0), np.sin(yaw/2.0)
        return cls(cr*cp*cy + sr*sp*sy, sr*cp*cy - cr*sp*sy, cr*cp*cy + sr*sp*sy, cr*cp*sy - sr*sp*cy)

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def multiply(self, other):
        w1, x1, y1, z1 = self.q
        w2, x2, y2, z2 = other.q
        return Quaternion(
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        )

    def to_rotation_matrix(self):
        w, x, y, z = self.q
        return np.array([
            [1.0 - 2.0*(y*y + z*z), 2.0*(x*y - z*w),       2.0*(x*z + y*w)],
            [2.0*(x*y + z*w),       1.0 - 2.0*(x*x + z*z), 2.0*(y*z - x*w)],
            [2.0*(x*z - y*w),       2.0*(y*z + x*w),       1.0 - 2.0*(x*x + y*y)]
        ], dtype=np.float64)

    def rotate_vector(self, v):
        return self.to_rotation_matrix() @ np.array(v, dtype=np.float64)

    def geodesic_distance(self, other):
        inner = np.clip(np.abs(np.dot(self.q, other.q)), 0.0, 1.0)
        return float(2.0 * np.arccos(inner))

    @staticmethod
    def slerp(q1, q2, t):
        dot = np.dot(q1.q, q2.q)
        q2_arr = q2.q.copy()
        if dot < 0.0:
            q2_arr = -q2_arr
            dot = -dot
        dot = np.clip(dot, -1.0, 1.0)
        if dot > 0.9995:
            return Quaternion(*( (1.0 - t)*q1.q + t*q2_arr ))
        theta_0 = np.arccos(dot)
        theta = theta_0 * t
        q_perp = q2_arr - q1.q * dot
        q_perp /= np.linalg.norm(q_perp)
        return Quaternion(*( q1.q * np.cos(theta) + q_perp * np.sin(theta) ))

    def to_euler(self):
        w, x, y, z = self.q
        sinr_cosp = 2.0 * (w * x + y * z)
        cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)
        
        sinp = 2.0 * (w * y - z * x)
        pitch = np.arcsin(np.clip(sinp, -1.0, 1.0))
        
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)
        return roll, pitch, yaw

    def to_list(self):
        return [round(float(c), 6) for c in self.q]

# ============================================================================
# 2. MULTI-TURN SLERP TRAJECTORY TRACKER & DECEPTION SIEVE
# ============================================================================

class MultiTurnTrajectoryTracker:
    """
    Traces continuous ideological trajectories across multi-turn parliamentary debates,
    computing geodesic path curvature, Slerp angular velocity, and the Rhetorical Evasion Index.
    """
    @staticmethod
    def analyze_dialogue_exchange(turns):
        turn_analysis = []
        full_interpolated_trajectory = []
        
        for k in range(len(turns) - 1):
            t_curr = turns[k]
            t_next = turns[k+1]
            
            s_curr = np.array(t_curr["coords"], dtype=np.float64)
            s_next = np.array(t_next["coords"], dtype=np.float64)
            q_curr = Quaternion(*t_curr["quaternion"])
            q_next = Quaternion(*t_next["quaternion"])
            
            geo_dist = q_curr.geodesic_distance(q_next)
            delta_s = s_next - s_curr
            delta_u, delta_p, delta_z = delta_s
            
            r_c, p_c, y_c = q_curr.to_euler()
            r_n, p_n, y_n = q_next.to_euler()
            delta_roll = abs(r_n - r_c)
            delta_yaw = abs(y_n - y_c)
            
            causal_advance = max(1e-4, delta_z)
            boundary_advance = max(1e-4, delta_u)
            spin_index = float((delta_roll + delta_yaw) / (causal_advance + 0.5 * boundary_advance))
            
            if delta_z > 0.4 and delta_u > 0.2:
                pivot_type = "PRODUCTIVE_CAUSAL_PROGRESSION (+z Delivery)"
            elif spin_index > 2.5:
                pivot_type = "RHETORICAL_EVASION_DEFLECTION (Spin Pivot)"
            elif delta_u > 0.3 and delta_p < 0.0:
                pivot_type = "CONSTRUCTIVE_STABILIZATION (Boundary Broadening)"
            else:
                pivot_type = "ADVERSARIAL_FRICTION_EXCHANGE"
                
            transition_record = {
                "step": f"Turn {t_curr['turn_id']} -> Turn {t_next['turn_id']}",
                "speaker_pair": f"{t_curr['speaker']} -> {t_next['speaker']}",
                "geodesic_angular_distance_rad": round(geo_dist, 4),
                "geodesic_angular_distance_deg": round(float(np.degrees(geo_dist)), 2),
                "delta_upsilon": round(delta_u, 4),
                "delta_psi": round(delta_p, 4),
                "delta_z": round(delta_z, 4),
                "rhetorical_evasion_spin_index": round(spin_index, 4),
                "transition_type": pivot_type
            }
            turn_analysis.append(transition_record)
            
            for step_i in range(10):
                tau = step_i / 10.0
                q_interp = Quaternion.slerp(q_curr, q_next, tau)
                s_interp = (1.0 - tau) * s_curr + tau * s_next
                full_interpolated_trajectory.append({
                    "turn_segment": f"{t_curr['turn_id']}-{t_next['turn_id']}",
                    "tau": round(tau, 2),
                    "coords": [round(float(c), 4) for c in s_interp],
                    "quaternion": q_interp.to_list()
                })
                
        return turn_analysis, full_interpolated_trajectory

if __name__ == "__main__":
    dialogue = [
        {"turn_id": 1, "speaker": "Opposition", "coords": [-0.85, 0.45, -0.75], "quaternion": Quaternion.from_euler(2.45, -0.35, -0.25).to_list()},
        {"turn_id": 2, "speaker": "Minister Deflection", "coords": [-1.10, 0.65, -0.40], "quaternion": Quaternion.from_euler(2.70, 0.10, -0.70).to_list()},
        {"turn_id": 3, "speaker": "Crossbench", "coords": [0.45, -0.15, 0.10], "quaternion": Quaternion.from_euler(-0.25, 0.05, 0.15).to_list()},
        {"turn_id": 4, "speaker": "Minister Policy", "coords": [0.95, 0.65, 0.55], "quaternion": Quaternion.from_euler(0.72, 0.42, 0.68).to_list()}
    ]
    analysis, waypoints = MultiTurnTrajectoryTracker.analyze_dialogue_exchange(dialogue)
    print("Multi-Turn Slerp Tracking Completed. Analyzed transitions:", len(analysis))
