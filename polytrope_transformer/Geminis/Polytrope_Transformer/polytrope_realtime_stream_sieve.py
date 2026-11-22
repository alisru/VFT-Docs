"""
Fractal Polytrope Sovereign LLM: Real-Time Parliamentary Stream Sieve & Question Time Diagnostics.
Cycle 19 R&D Milestone. Ingests streaming speech turns from parliamentary Question Time debates,
evaluating instantaneous Parable Archetypes (Sower & Talents), Spin Evasion Indices, Substrate Shearing,
and 14-Plane Polar Matrix states across the unified 220-tuple corpus.
"""

import json
import re
import time
import numpy as np

class Quaternion:
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        v = np.array([w, x, y, z], dtype=np.float64)
        norm = np.linalg.norm(v)
        self.q = v / norm if norm > 1e-12 else np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)

    @classmethod
    def from_euler(cls, roll, pitch, yaw):
        cr, cp, cy = np.cos(roll/2.0), np.cos(pitch/2.0), np.cos(yaw/2.0)
        sr, sp, sy = np.sin(roll/2.0), np.sin(pitch/2.0), np.sin(yaw/2.0)
        return cls(cr*cp*cy + sr*sp*sy, sr*cp*cy - cr*sp*sy, cr*cp*cy + sr*cp*sy, cr*cp*sy - sr*sp*cy)

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

class RealtimeStreamSieve:
    """
    Evaluates streaming parliamentary Question Time speech turns in real time,
    computing the Parable Archetype, Spin Index, Substrate Shearing, and Polar State.
    """
    PARABLE_CENTERS = {
        "GOOD_SOIL": np.array([1.25, 1.15, 1.45]),
        "ROCKY_GROUND": np.array([-0.85, 0.65, -0.70]),
        "THORNY_GROUND": np.array([-1.05, -0.75, -0.95]),
        "BURIED_TALENT": np.array([-1.25, -1.15, -1.45])
    }

    @classmethod
    def process_speech_turn(cls, turn_data, prev_turn=None):
        coords = np.array(turn_data["coords"], dtype=np.float64)
        q_obj = Quaternion(*turn_data["quaternion"])
        q_planes = np.array(turn_data["q_planes"], dtype=np.float64)
        q_planes /= np.sum(q_planes)
        q3_phys = q_planes[2]
        q5_log = q_planes[4]
        
        scores = {k: 1.0 / (1.0 + np.linalg.norm(coords - c)) for k, c in cls.PARABLE_CENTERS.items()}
        top_archetype = max(scores, key=scores.get)
        
        if q5_log > 0.40 and q3_phys < 0.05:
            shearing_status = "SHEARED (Q5 Abstract Gain without Q3 Physical Grounding)"
            passthrough = 0.0000
        else:
            shearing_status = "PASSED (Substrate Invariance Verified)"
            passthrough = 1.0000
            
        if prev_turn is not None:
            q_prev = Quaternion(*prev_turn["quaternion"])
            delta_z = coords[2] - prev_turn["coords"][2]
            delta_u = coords[0] - prev_turn["coords"][0]
            r_c, p_c, y_c = q_prev.to_euler()
            r_n, p_n, y_n = q_obj.to_euler()
            angular_agitation = abs(r_n - r_c) + abs(y_n - y_c)
            causal_advance = max(1e-4, delta_z)
            boundary_advance = max(1e-4, delta_u)
            spin_idx = float(angular_agitation / (causal_advance + 0.5 * boundary_advance))
        else:
            spin_idx = 0.0
            
        if passthrough == 0.0:
            flag = "CRITICAL_SUBSTRATE_DELUSION"
        elif spin_idx > 2.5:
            flag = "RHETORICAL_EVASION_SPIN"
        elif top_archetype == "GOOD_SOIL":
            flag = "PRODUCTIVE_STEWARDSHIP"
        elif top_archetype == "ROCKY_GROUND":
            flag = "UNROOTED_RHETORIC_RISK"
        elif top_archetype == "THORNY_GROUND":
            flag = "EXTRACTIVE_MONOPOLY_DRAG"
        else:
            flag = "ADMINISTRATIVE_INERTIA"
            
        return {
            "turn_id": turn_data["turn_id"],
            "speaker": turn_data["speaker"],
            "role": turn_data["role"],
            "text": turn_data["text"],
            "coords": [round(float(c), 4) for c in coords],
            "quaternion": q_obj.to_list(),
            "dominant_plane": f"Q{np.argmax(q_planes)+1}",
            "parable_archetype": top_archetype,
            "archetype_score": round(float(scores[top_archetype]), 4),
            "substrate_passthrough": passthrough,
            "shearing_status": shearing_status,
            "spin_evasion_index": round(spin_idx, 4),
            "diagnostic_flag": flag,
            "polar_state": turn_data.get("polar_state", "UNSPECIFIED")
        }

if __name__ == "__main__":
    from run_cycle19 import run_realtime_stream_case_study
    run_realtime_stream_case_study()
