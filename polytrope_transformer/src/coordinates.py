"""
Coordinates and geometric tensor primitives for the Fractal Polytrope Transformer.

Tracks semantic units in (υ, ψ, z, θ_xyz):
  - υ (Upsilon): Morality / Boundary Inclusivity [-2.0 to +2.0]
      +υ = Inclusive (absorptive, shared carrying capacity, systemic justice)
      -υ = Exclusive (demarcating, privatizing, extractive boundary)
  - ψ (Psi): Will / Kinetic Latency [-2.0 to +2.0]
      +ψ = Latent Active (proactive, creating, building, kinetic drive)
      -ψ = Latent Counteractive (passive drag, friction, resistance floor)
  - z (Zeta): The "IS ALSO" Causal & Co-Presence Dimension [-2.0 to +2.0]
      |z| = Coupling strength / similarity deviation from immediate state (0)
      z < 0 = "To Cause Of" (upstream antecedent, physical seed, energetic origin)
      z > 0 = "To Effect Of" (downstream consequence, resultant fruit, yield)
      z = 0 = Immediate focal state in isolation ('IS')
  - θ_xyz: 3D Angular Orientation Tensor in SO(3) [roll, pitch, yaw]
      θ_υψ (Roll):  4-phase cyclic loop (productive -> reductive -> regress -> constructive)
      θ_ψz (Pitch): Causal tilt between energetic will and physical fruit/cause
      θ_υz (Yaw):   Inclusivity-to-causal alignment
"""

from dataclasses import dataclass
from enum import Enum
import math
import numpy as np

class ModalRay(Enum):
    IS = "is"             # Center Ground State (0, 0, 0.0)
    CAN_BE = "can_be"     # Productive Ray (+υ, +ψ) -> Forward Modal Potential
    IS_NOT = "is_not"     # Reductive Ray (-υ, +ψ) -> Active Demarcation / Boundary Negation
    IS_LIKE = "is_like"   # Constructive Ray (+υ, -ψ) -> Structural Analogy / Invariant Morphism
    WAS_LIKE = "was_like" # Regress Ray (-υ, -ψ) -> Historical Trace / Debt Floor

class QPlane(Enum):
    Q1_PHYSICAL = 1       # Joules, exergy, mass, physical logistics
    Q2_BIOPHYSICAL = 2     # Biological reproduction, caloric survival, tissue
    Q3_PHENOMENOLOGICAL = 3# Conscious experience, felt stress, cognitive load
    Q4_SOCIETAL = 4       # Cohesion, language consensus, interpersonal trust
    Q5_INSTITUTIONAL = 5  # Law, contracts, balance sheets, nominal debt
    Q6_IDEOLOGICAL = 6    # Paradigms, political dogmas, worldviews
    Q7_ONTOLOGICAL = 7    # Invariant mathematical physics, actualist truth

class IntentVector(Enum):
    I1_EXPANSION = 1      # Boundary expanding (+υ)
    I2_CONTRACTION = 2    # Boundary contracting (-υ)
    I3_KINETIC_PUSH = 3   # Proactive generation (+ψ)
    I4_RESISTIVE_DRAG = 4 # Passive friction floor (-ψ)
    I5_FORWARD_EFFECT = 5 # Driving downstream consequences (+z, "to effect of")
    I6_CAUSAL_ORIGIN = 6  # Rooted in upstream physical antecedents (-z, "to cause of")

@dataclass
class PolytropeCoordinate:
    upsilon: float       # Morality / Boundary Inclusivity [-2.0, +2.0]
    psi: float           # Will / Kinetic Latency [-2.0, +2.0]
    z: float             # "Is Also" Causal Axis [-2.0, +2.0] (z < 0 cause, z > 0 effect)
    theta_roll: float    # θ_υψ: Phase in the 4-phase cycle [0, 2π)
    theta_pitch: float   # θ_ψz: Causal tilt [-π, +π]
    theta_yaw: float     # θ_υz: Inclusion-causality alignment [-π, +π]
    modal_ray: ModalRay = ModalRay.IS
    plane: QPlane = QPlane.Q1_PHYSICAL

    @property
    def causal_role(self) -> str:
        """Returns human-readable causal role along the 'Is Also' Z-axis."""
        if abs(self.z) < 1e-4:
            return "Immediate State (IS)"
        elif self.z > 0:
            return f"To Effect Of (Yield/Fruit, strength={abs(self.z):.2f})"
        else:
            return f"To Cause Of (Root/Seed, strength={abs(self.z):.2f})"

    def to_vector(self) -> np.ndarray:
        """Returns 6D state vector: [υ, ψ, z, θ_roll, θ_pitch, θ_yaw]."""
        return np.array([
            self.upsilon,
            self.psi,
            self.z,
            self.theta_roll,
            self.theta_pitch,
            self.theta_yaw
        ], dtype=np.float64)

    @classmethod
    def from_modal_ray(cls, ray: ModalRay, z_causal: float = 0.0, plane: QPlane = QPlane.Q1_PHYSICAL) -> "PolytropeCoordinate":
        """
        Generates coordinates for a modal ray on the (υ, ψ) plane, with optional causal Z offset.
        """
        if ray == ModalRay.IS:
            return cls(upsilon=0.0, psi=0.0, z=z_causal, 
                       theta_roll=0.0, theta_pitch=0.0, theta_yaw=0.0, 
                       modal_ray=ray, plane=plane)
        elif ray == ModalRay.CAN_BE:
            # Productive: Inclusive (+υ), Active (+ψ) -> Generative Potential
            return cls(upsilon=1.0, psi=1.0, z=z_causal, 
                       theta_roll=math.pi / 4.0, theta_pitch=math.pi / 6.0, theta_yaw=0.0, 
                       modal_ray=ray, plane=plane)
        elif ray == ModalRay.IS_NOT:
            # Reductive: Exclusive (-υ), Active (+ψ) -> Active Demarcation / Boundary Negation
            return cls(upsilon=-1.0, psi=1.0, z=z_causal, 
                       theta_roll=3.0 * math.pi / 4.0, theta_pitch=0.0, theta_yaw=math.pi / 2.0, 
                       modal_ray=ray, plane=plane)
        elif ray == ModalRay.IS_LIKE:
            # Constructive: Inclusive (+υ), Passive (-ψ) -> Structural Analogy / Morphism
            return cls(upsilon=1.0, psi=-1.0, z=z_causal, 
                       theta_roll=7.0 * math.pi / 4.0, theta_pitch=-math.pi / 6.0, theta_yaw=0.0, 
                       modal_ray=ray, plane=plane)
        elif ray == ModalRay.WAS_LIKE:
            # Regress: Exclusive (-υ), Passive (-ψ) -> Historical Precedent Trace / Drag Floor
            return cls(upsilon=-1.0, psi=-1.0, z=z_causal, 
                       theta_roll=5.0 * math.pi / 4.0, theta_pitch=-math.pi / 3.0, theta_yaw=-math.pi / 4.0, 
                       modal_ray=ray, plane=plane)
        raise ValueError(f"Unknown modal ray: {ray}")

    def compute_angular_shear(self, other: "PolytropeCoordinate") -> float:
        """
        Computes rotational shear between two states in SO(3).
        """
        d_roll = math.atan2(math.sin(self.theta_roll - other.theta_roll), math.cos(self.theta_roll - other.theta_roll))
        d_pitch = self.theta_pitch - other.theta_pitch
        d_yaw = self.theta_yaw - other.theta_yaw
        return float(math.sqrt(d_roll**2 + d_pitch**2 + d_yaw**2))

    def compute_causal_distance(self, other: "PolytropeCoordinate") -> float:
        """
        Measures the directional causal displacement along the Z axis (Cause -> Effect).
        Positive when moving from Cause to Effect; negative if regressing against causal flow.
        """
        return self.z - other.z
