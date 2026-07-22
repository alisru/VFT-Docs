"""
Port of PossibilityClassification.cs Main().

Same scenario, same numbers, same two experiments. Run it against the C# to
check the Python agrees.
"""

from vft import (
    FieldMath, Idea, Judgement, Optimism, Pessimism, StateVector,
    compare_states, plot_3d_axes, plot_state, process_synergy,
)

BAR = "=" * 64


def make_test_idea() -> Idea:
    """The scenario from PossibilityClassification.cs, unchanged."""
    return Idea.of(
        who=("I might be capable", 0.85),
        where=("Constraints exist", 1.15),
        what=("Maybe possible", 0.75),
        why=("Unclear purpose", 0.90),
        how=("No clear method", 1.25),
        cause=("Mixed history", 0.95),
        effect=("Some anxiety", 1.10),
    )


def run_mode(mode, label: str):
    idea = make_test_idea()
    print("\n" + "#" * 64)
    print(f"# {label}")
    print("#" * 64)
    print(f"  {mode.name}: {mode.definitive_meaning}")

    print("\n[INITIAL IDEA]")
    print(idea.report())
    print(f"  R_net = {idea.net_coherence:.4f}   "
          f"{Judgement.evaluate(idea)}")

    result = mode.apply(idea)

    print("\n" + plot_state(result["initial"], "Initial State"))
    print("\n[3-AXIS VIEW, BEFORE]")
    print(plot_3d_axes(result["initial"]))

    if "gradient" in result:
        print(f"\n[POSSIGRAVITY GRADIENT] {result['gradient']}")

    print("\n" + plot_state(result["final"], "Final State"))
    print("\n[3-AXIS VIEW, AFTER]")
    print(plot_3d_axes(result["final"]))

    print("\n" + compare_states(result["initial"], result["final"], mode.name))

    print("\n[FINAL IDEA]")
    print(idea.report())
    coherence = idea.net_coherence
    verdict = Judgement.evaluate(idea)
    print(f"\n[FINAL ANALYSIS - {mode.name.upper()}]")
    print(f"  Net Coherence (R_net): {coherence:.4f}")
    print(f"  Judgement: {verdict}")
    return coherence, verdict


def main() -> None:
    print(BAR)
    print("  REALITY CLASSIFICATION: THE POSSIBILITY PLANE")
    print("  Vector Field Theory + Full Equation Set  (Python port)")
    print(BAR)

    print("\n[ONTOLOGY]: Possibility Plane")
    print("  A 6-dimensional epistemic manifold structured by 7 functional")
    print("  planes where probability collapses into reality via gradient flows.")

    print("\n[SCENARIO]: An agent confronts an uncertain intent")
    print("  Initial State: mild perturbations from Unity")
    for line in ["Some self-doubt (WHO: 0.85)",
                 "Physical constraints (WHERE: 1.15)",
                 "Uncertain possibility (WHAT: 0.75)",
                 "Unclear purpose (WHY: 0.90)",
                 "No clear method (HOW: 1.25)",
                 "Mixed history (CAUSE: 0.95)",
                 "Some anxiety (EFFECT: 1.10)"]:
        print(f"    - {line}")

    c_opt, v_opt = run_mode(Optimism(intensity=0.8), "EXPERIMENT 1: OPTIMISM MODE")
    c_pes, v_pes = run_mode(Pessimism(seed=42), "EXPERIMENT 2: PESSIMISM MODE")

    print("\n\n" + BAR)
    print("  CONCLUSION: The Field of Chance is Geometric")
    print(BAR)
    print(f"  Optimism  -> R_net {c_opt:.4f}   {v_opt}")
    print(f"  Pessimism -> R_net {c_pes:.4f}   {v_pes}")
    print("\n  The mathematics demonstrate:")
    print("    - Optimism creates GRAVITY WELLS (steep gradients toward Unity)")
    print("    - Pessimism creates ENTROPY (flat/inverted gradients away)")
    print("    - The Possibility Plane is a manifold with measurable curvature")
    print("    - Psychological states are geometric operations on it")

    # The Belief Axiom over both outcomes.
    state = 0
    for mode_cls, seed in ((Optimism, None), (Pessimism, 42)):
        idea = make_test_idea()
        mode = mode_cls() if seed is None else mode_cls(seed=seed)
        mode.apply(idea)
        before = state
        state = process_synergy(state, idea)
        print(f"\n  [SYNERGY] {mode.name:<10} worldview {before} -> {state}"
              f"   ({'expanded' if state > before else 'rejected'})")


if __name__ == "__main__":
    main()
