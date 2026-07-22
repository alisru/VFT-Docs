"""
Faithful Python port of the existing C# project.

Sources, ported field-for-field and formula-for-formula:
    {Idea}.cs                PlaneOfReality, MoralVectorDef, MoralVectors,
                             MoralScore, Belief, Idea, CalculateFractalRatio
    StateVector.cs           StateVector, FromIdea, DistanceFromUnity,
                             GetShapeSignature
    FieldMath.cs             all 14 static methods
    IOperationMode.cs        the mode interface
    Optimism.cs              Possigravity mode
    Pessimism.cs             Perceptual Inversion mode
    {Meaning}.cs             Polarity, Word, Judgement, ProcessSynergy

Nothing here is invented. Where the C# had a formula, the formula is copied,
including its quirks (learning rate 0.1, potential floor 100.0, gradient
half-step 0.5, DistanceFromUnity's paired-axis differencing).

WHY THIS FILE EXISTS
--------------------
The earlier Python work reinvented several of these structures under different
names and, in two places, with different mathematics:

  invented "SignedSpan poles"   ->  MoralVectorDef already defines the poles:
                                    Sovereignty/Tyranny, Thriving/Mere Survival,
                                    Stewardship/Greed, Truth-Telling/Delusion,
                                    Wisdom/Sophistry, Redemption/Revisionism,
                                    Love-Unity/Parasitism.
  invented "spans on Meaning"   ->  Idea already IS the 7-vector.
  dropped TruthScore            ->  it is Belief.Score, the per-vector distance
                                    from Unity. It was load-bearing.
  used mean for coherence       ->  WRONG. R_net = 1 / product(scores).
                                    The mean cannot go to infinity; the
                                    fractal ratio can, and that is the point.
  theorised "carve a hole and
  let material fall in"         ->  Possigravity. Already implemented as
                                    potential Phi = -log P with force
                                    -grad Phi and gradient flow toward Unity.

The last one matters most: the excavation/accretion mechanism developed at
length in conversation already existed here as a working potential field.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence


# ---------------------------------------------------------------------------
# {Idea}.cs  --  the 7 vectors configuration
# ---------------------------------------------------------------------------

class PlaneOfReality(Enum):
    METAPHYSICAL = "MetaPhysical"
    PHYSICAL = "Physical"
    POSSIBLE = "Possible"
    LYRICAL = "Lyrical"
    LOGICAL = "Logical"
    HISTORICAL = "Historical"
    EMOTIVE = "Emotive"


class Polarity(Enum):
    """Kept from {Meaning}.cs."""
    NEUTRAL = "Neutral"
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    MIXED = "Mixed"


@dataclass(frozen=True)
class MoralVectorDef:
    interrogative: str
    plane: PlaneOfReality
    virtue: str
    sin: str
    domain: str          # Identity, Soul, Body, Mind
    axis_name: str       # Driver, Vertical, Lateral, Longitudinal
    axis_direction: str  # 7th Angle, +z, -z, ...
    description: str     # "Will and Direction"
    dynamics: str        # "Expansion" (+) or "Contraction" (-)


class MoralVectors:
    """The 42-Structure. These are the real poles: virtue at +, sin at both
    extremes (excess above Unity, deficit below)."""

    # THE DRIVER (The Emergent Axis)
    WHO = MoralVectorDef("Who", PlaneOfReality.METAPHYSICAL,
                         "Sovereignty", "Tyranny",
                         "Identity", "Driver", "7th Angle",
                         "Will and Direction", "Expansion")

    # THE LATERAL AXIS (Definition and Space: +/- x) -> Body
    WHERE = MoralVectorDef("Where", PlaneOfReality.PHYSICAL,
                           "Thriving", "Mere Survival",
                           "Body", "Lateral", "-x",
                           "Matter and Distance", "Contraction")
    WHAT = MoralVectorDef("What", PlaneOfReality.POSSIBLE,
                          "Stewardship", "Greed",
                          "Body", "Lateral", "+x",
                          "Faith and Probability", "Expansion")

    # THE LONGITUDINAL AXIS (Function and Meaning: +/- y) -> Mind
    WHY = MoralVectorDef("Why", PlaneOfReality.LYRICAL,
                         "Truth-Telling", "Delusion",
                         "Mind", "Longitudinal", "+y",
                         "Meaning and Resonance", "Expansion")
    HOW = MoralVectorDef("How", PlaneOfReality.LOGICAL,
                         "Wisdom", "Sophistry",
                         "Mind", "Longitudinal", "-y",
                         "Count and Consistency", "Contraction")

    # THE VERTICAL AXIS (Temporal Link: +/- z) -> Soul
    CAUSE = MoralVectorDef("Cause", PlaneOfReality.HISTORICAL,
                           "Redemption", "Revisionism",
                           "Soul", "Vertical", "+z",
                           "Sequence and Causality", "Expansion")
    EFFECT = MoralVectorDef("Effect", PlaneOfReality.EMOTIVE,
                            "Love/Unity", "Parasitism",
                            "Soul", "Vertical", "-z",
                            "Passion and Consequence", "Contraction")

    ALL = [WHO, WHERE, WHAT, WHY, HOW, CAUSE, EFFECT]


class MoralScore:
    """
    1.0 = Truth/Virtue. Above = Excess of the sin. Below = Deficit of it.
    Truth is the ratio of 1, so both directions away from Unity are failure
    modes of the SAME sin, which a signed span cannot express and this can.
    """

    def __init__(self, value: float, vector_def: MoralVectorDef):
        self.value = value
        self.vector_def = vector_def
        if abs(value - 1.0) < 0.001:
            self.alignment = vector_def.virtue
        elif value > 1.0:
            self.alignment = f"Excess: {vector_def.sin}"
        else:
            self.alignment = f"Deficit: {vector_def.sin}"

    def __repr__(self) -> str:
        return f"{self.value:.3f} ({self.alignment})"


@dataclass
class Belief:
    vector_type: MoralVectorDef
    answer_word: str
    truth_score: float = 1.0
    moral_alignment: Optional[MoralScore] = None

    def __post_init__(self):
        self.moral_alignment = MoralScore(self.truth_score, self.vector_type)

    @property
    def score(self) -> float:
        return self.truth_score

    def set_score(self, v: float) -> None:
        self.truth_score = v
        self.moral_alignment = MoralScore(v, self.vector_type)


class Idea:
    """The 7-Vector Structure. This is the fractal stack."""

    def __init__(self, who: Belief, where: Belief, what: Belief, why: Belief,
                 how: Belief, cause: Belief, effect: Belief):
        self.who, self.where, self.what = who, where, what
        self.why, self.how = why, how
        self.cause, self.effect = cause, effect
        self.vectors: List[Belief] = [who, where, what, why, how, cause, effect]

    @staticmethod
    def of(**kw) -> "Idea":
        """Idea.of(who=("I might be capable", 0.85), where=(...), ...)"""
        defs = {"who": MoralVectors.WHO, "where": MoralVectors.WHERE,
                "what": MoralVectors.WHAT, "why": MoralVectors.WHY,
                "how": MoralVectors.HOW, "cause": MoralVectors.CAUSE,
                "effect": MoralVectors.EFFECT}
        beliefs = {k: Belief(defs[k], w, s) for k, (w, s) in kw.items()}
        return Idea(**beliefs)

    @property
    def net_coherence(self) -> float:
        """
        The Fractal Ratio Protocol:
            R_net = 1 / (Who * Where * What * Why * How * Cause * Effect)

        Recomputed on access, because the operation modes mutate the beliefs
        in place. The C# cached it at construction, which meant NetCoherence
        went stale the moment ApplyMode ran, and PossibilityClassification
        worked around that by recomputing via FieldMath. This removes the
        workaround rather than porting the staleness.
        """
        return FieldMath.fractal_ratio([v.score for v in self.vectors])

    def report(self) -> str:
        lines = []
        for v in self.vectors:
            lines.append(
                f"  {v.vector_type.interrogative:<7} {v.score:6.3f}  "
                f"{v.moral_alignment.alignment:<24} "
                f"[{v.vector_type.domain}/{v.vector_type.axis_direction}] "
                f"{v.answer_word}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# {Meaning}.cs  --  Judgement and the Belief Axiom
# ---------------------------------------------------------------------------

class Judgement:
    """The Coherence Gate Axiom:  [Q|A / A|Q] === { Y=1; N!=1; Insult > 1 }"""

    @staticmethod
    def evaluate(idea: Idea, tolerance: float = 0.1) -> str:
        ratio = idea.net_coherence
        if (1.0 - tolerance) <= ratio <= (1.0 + tolerance):
            return "Y=1 (TRUTH)"
        if ratio > (1.0 + tolerance):
            return "INSULT > 1 (CHAOS/TYRANNY)"
        return "N != 1 (LIE/ENTROPY)"


def process_synergy(worldview_state: int, new_truth: Idea) -> int:
    """The Belief Axiom: Belief = 1 + 1 = 2. Consciousness expands only on
    gated truth; a rejected idea leaves the worldview unchanged."""
    return (worldview_state + 1
            if "TRUTH" in Judgement.evaluate(new_truth)
            else worldview_state)


# ---------------------------------------------------------------------------
# StateVector.cs
# ---------------------------------------------------------------------------

@dataclass
class StateVector:
    """A point in the possibility space. Six coordinates on three axes, plus
    Who as the observer parameter standing outside the pairs."""
    who: float
    where: float
    what: float
    why: float
    how: float
    cause: float
    effect: float

    @staticmethod
    def from_idea(idea: Idea) -> "StateVector":
        return StateVector(idea.who.score, idea.where.score, idea.what.score,
                           idea.why.score, idea.how.score, idea.cause.score,
                           idea.effect.score)

    @staticmethod
    def unity() -> "StateVector":
        return StateVector(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)

    def as_list(self) -> List[float]:
        return [self.who, self.where, self.what, self.why, self.how,
                self.cause, self.effect]

    def distance_from_unity(self) -> float:
        """
        Total strain. Note the paired differencing: deviation is measured
        BETWEEN the two ends of each axis, not from Unity per coordinate, so
        a state that is equally wrong on both ends of an axis reads as
        balanced. Who, having no pair, is measured directly.
        """
        dx = (self.what - 1.0) - (self.where - 1.0)
        dy = (self.why - 1.0) - (self.how - 1.0)
        dz = (self.cause - 1.0) - (self.effect - 1.0)
        dw = (self.who - 1.0)
        return math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)

    def shape_signature(self) -> str:
        lateral = "Expansion" if self.what > self.where else "Contraction"
        longitudinal = ("Meaning-Driven" if self.why > self.how
                        else "Method-Driven")
        vertical = ("Past-Anchored" if self.cause > self.effect
                    else "Future-Oriented")
        return f"[{lateral} | {longitudinal} | {vertical}]"

    def __str__(self) -> str:
        return (f"S({self.who:.2f}, {self.where:.2f}, {self.what:.2f}, "
                f"{self.why:.2f}, {self.how:.2f}, {self.cause:.2f}, "
                f"{self.effect:.2f})")


# ---------------------------------------------------------------------------
# FieldMath.cs  --  The Field of Chance
# ---------------------------------------------------------------------------

class FieldMath:

    # --- 1. Resolution time and convergence ---
    @staticmethod
    def resolution_time(current_certainty: float, target_certainty: float,
                        variance: float, efficiency: float) -> float:
        if efficiency <= 0.001:
            efficiency = 0.001
        return abs(target_certainty - current_certainty) * variance / efficiency

    # --- 2. Bayesian inference ---
    @staticmethod
    def posterior(prior: float, likelihood: float,
                  learning_rate: float = 0.1) -> float:
        return prior + (likelihood - prior) * learning_rate

    # --- 3. Possigravity: the potential field ---
    @staticmethod
    def potential(probability: float) -> float:
        """Phi(S) = -log P(S | Data). Floor of 100 stands in for the infinite
        barrier at zero probability."""
        if probability <= 0:
            return 100.0
        return -math.log(probability)

    @staticmethod
    def possigravity(probability: float, target_probability: float) -> float:
        """F = -grad(Phi). Positive F pulls toward higher probability.

        THIS IS THE CARVED HOLE. The well is a potential minimum, the pull is
        the negative gradient, and material 'falling in' is gradient flow.
        """
        return -(FieldMath.potential(target_probability)
                 - FieldMath.potential(probability))

    # --- 4. Entropy and resistance ---
    @staticmethod
    def vft_entropy(vector_score: float) -> float:
        """Truth is the ratio of 1; entropy is distance from 1."""
        return abs(vector_score - 1.0)

    @staticmethod
    def fractal_ratio(vector_scores: Sequence[float]) -> float:
        """R_net = 1 / product(vectors). Infinite when any vector is zero:
        one collapsed plane collapses the whole idea, which a mean cannot
        express."""
        product = 1.0
        for s in vector_scores:
            product *= s
        if product == 0:
            return math.inf
        return 1.0 / product

    # --- 5. Vector operations ---
    @staticmethod
    def gradient_vector(current: StateVector, target: StateVector
                        ) -> StateVector:
        return StateVector(
            (target.who - current.who) * 0.5,
            (target.where - current.where) * 0.5,
            (target.what - current.what) * 0.5,
            (target.why - current.why) * 0.5,
            (target.how - current.how) * 0.5,
            (target.cause - current.cause) * 0.5,
            (target.effect - current.effect) * 0.5,
        )

    @staticmethod
    def apply_gradient_flow(current: StateVector, gradient: StateVector,
                            learning_rate: float = 0.1) -> StateVector:
        return StateVector(
            current.who + gradient.who * learning_rate,
            current.where + gradient.where * learning_rate,
            current.what + gradient.what * learning_rate,
            current.why + gradient.why * learning_rate,
            current.how + gradient.how * learning_rate,
            current.cause + gradient.cause * learning_rate,
            current.effect + gradient.effect * learning_rate,
        )

    # --- 6. Bayesian update over a state ---
    @staticmethod
    def bayesian_update(prior: StateVector, evidence: Sequence[float],
                        learning_rate: float = 0.1) -> StateVector:
        posterior = StateVector(*prior.as_list())
        for e in evidence:
            posterior.what = posterior.what + (e - posterior.what) * learning_rate
        return posterior

    # --- 7. The 7-plane bending mechanics ---
    @staticmethod
    def bend_toward_unity(current_value: float, intensity: float = 0.8
                          ) -> float:
        return current_value + (1.0 - current_value) * intensity

    @staticmethod
    def invert_coordinate(current_value: float,
                          rng: Optional[random.Random] = None) -> float:
        """Pessimism: push a near-Unity value to an extreme, making either a
        mountain (excess) or a deficit."""
        rng = rng or random.Random()
        if 0.5 < current_value < 1.5:
            if rng.random() > 0.5:
                return current_value * 0.5
            return current_value + 1.0 + rng.random()
        return current_value

    # --- 8. Information measures ---
    @staticmethod
    def shannon_entropy(probabilities: Sequence[float]) -> float:
        return -sum(p * math.log(p) for p in probabilities if p > 0)

    @staticmethod
    def system_entropy(state: StateVector) -> float:
        return state.distance_from_unity()


# ---------------------------------------------------------------------------
# IOperationMode.cs / Optimism.cs / Pessimism.cs
# ---------------------------------------------------------------------------

class OperationMode:
    """Psychological operation modes as geometric operations on the field."""
    name: str = "mode"
    definitive_meaning: str = ""
    polarity: Polarity = Polarity.NEUTRAL

    def apply(self, idea: Idea) -> Dict[str, object]:
        raise NotImplementedError

    def gradient_profile(self, current_prob: float) -> float:
        raise NotImplementedError


class Optimism(OperationMode):
    name = "Optimism"
    definitive_meaning = ("Possigravity: The generation of mass/certainty. "
                          "Bends the 7 planes toward the intended outcome "
                          "(Convergence).")
    polarity = Polarity.POSITIVE

    def __init__(self, intensity: float = 0.8):
        self.intensity = intensity

    def apply(self, idea: Idea) -> Dict[str, object]:
        initial = StateVector.from_idea(idea)
        gradient = FieldMath.gradient_vector(initial, StateVector.unity())
        final = FieldMath.apply_gradient_flow(initial, gradient, self.intensity)
        for b, v in zip(idea.vectors,
                        [final.who, final.where, final.what, final.why,
                         final.how, final.cause, final.effect]):
            b.set_score(v)
        return {"initial": initial, "gradient": gradient, "final": final,
                "entropy_before": FieldMath.system_entropy(initial),
                "entropy_after": FieldMath.system_entropy(final)}

    def gradient_profile(self, current_prob: float) -> float:
        return FieldMath.possigravity(current_prob, 1.0)


class Pessimism(OperationMode):
    name = "Pessimism"
    definitive_meaning = ("Perceptual Inversion: The generation of entropy. "
                          "Distorts the planes creating infinite strain "
                          "(Divergence).")
    polarity = Polarity.NEGATIVE

    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)

    def apply(self, idea: Idea) -> Dict[str, object]:
        initial = StateVector.from_idea(idea)
        d = StateVector(*[FieldMath.invert_coordinate(v, self.rng)
                          for v in initial.as_list()])
        # Variance jamming on the physical and logical planes:
        # "constraints are impossible", "method is too complex".
        d.where += 1.0 + self.rng.random()
        d.how += 1.0 + self.rng.random()
        # Deficits on possibility and meaning:
        # "unlikely to succeed", "pointless anyway".
        d.what *= 0.5
        d.why *= 0.5
        for b, v in zip(idea.vectors,
                        [d.who, d.where, d.what, d.why, d.how, d.cause,
                         d.effect]):
            b.set_score(v)
        return {"initial": initial, "final": d,
                "entropy_before": FieldMath.system_entropy(initial),
                "entropy_after": FieldMath.system_entropy(d)}

    def gradient_profile(self, current_prob: float) -> float:
        return -FieldMath.possigravity(current_prob, 1.0)


# ---------------------------------------------------------------------------
# GeometryVisualizer.cs
# ---------------------------------------------------------------------------

def plot_state(state: StateVector, label: str = "State") -> str:
    rows = [f"  {label}", f"  {state}  {state.shape_signature()}"]
    names = ["Who", "Where", "What", "Why", "How", "Cause", "Effect"]
    for n, v in zip(names, state.as_list()):
        # Unity sits at column 20; bar extends to the coordinate's position.
        pos = int(round(v * 20))
        pos = max(0, min(pos, 44))
        bar = [" "] * 45
        bar[20] = "|"
        bar[pos] = "#" if pos != 20 else "@"
        rows.append(f"  {n:<7}{''.join(bar)} {v:6.3f}  "
                    f"(entropy {FieldMath.vft_entropy(v):.3f})")
    rows.append("  " + " " * 7 + " " * 20 + "^ Unity")
    return "\n".join(rows)


def compare_states(before: StateVector, after: StateVector,
                   transformation: str) -> str:
    eb, ea = (FieldMath.system_entropy(before), FieldMath.system_entropy(after))
    arrow = "decreased" if ea < eb else ("increased" if ea > eb else "unchanged")
    return (f"  {transformation}\n"
            f"    before : {before}  entropy {eb:.4f}  {before.shape_signature()}\n"
            f"    after  : {after}  entropy {ea:.4f}  {after.shape_signature()}\n"
            f"    system entropy {arrow}: {eb:.4f} -> {ea:.4f}")


def plot_3d_axes(state: StateVector) -> str:
    return (
        f"    Lateral      (Body)  What {state.what:.2f} <--+x  -x--> "
        f"Where {state.where:.2f}\n"
        f"    Longitudinal (Mind)  Why  {state.why:.2f} <--+y  -y--> "
        f"How   {state.how:.2f}\n"
        f"    Vertical     (Soul)  Cause{state.cause:.2f} <--+z  -z--> "
        f"Effect{state.effect:.2f}\n"
        f"    Driver   (Identity)  Who  {state.who:.2f}  (7th Angle)")
