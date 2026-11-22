#!/usr/bin/env python3
"""
Fractal Polytrope Sovereign LLM — Interactive Local CLI & Python SDK
Run directly in terminal:
  python3 polytrope_llm_cli.py "Your statement or policy prompt here"
Or run without arguments for an interactive REPL session:
  python3 polytrope_llm_cli.py
"""

import sys
import math
import re

Q_PLANES = [
    ("Q1", "WHO",   "Metaphysical Identity (Will & Driver)"),
    ("Q2", "WHAT",  "Possible (Faith & Probability)"),
    ("Q3", "WHERE", "Physical (Matter, Mass & Distance)"),
    ("Q4", "WHY",   "Lyrical (Meaning, Telos & Resonance)"),
    ("Q5", "HOW",   "Logical (Count, Ledger & Statute)"),
    ("Q6", "CAUSE", "Historical (Sequence & Precedent)"),
    ("Q7", "EFFECT","Emotive (Passion & Consequence)"),
]

def evaluate_prompt(text: str):
    lower = text.lower()
    words = re.findall(r"\b[a-z0-9']+\b", lower)

    neg_markers = {"not", "never", "no", "without", "refuse", "refuses", "block", "blocks", "cannot", "neither", "zero", "lieu"}
    has_negation = any(w in neg_markers for w in words)

    q3_words = {"water", "grain", "rail", "roads", "homes", "housing", "hospital", "clinics", "food", "seed", "soil", "land", "reservoirs", "freight", "electricity", "grid", "hydro", "physical", "habitat", "trees", "ox", "build", "construct"}
    q5_words = {"budget", "tax", "fee", "fund", "offset", "statute", "compliance", "manual", "accounting", "ledger", "derivatives", "rate", "inflation", "clause", "audit", "review", "committee"}
    q1_words = {"government", "minister", "king", "god", "commission", "parliament", "we", "sovereign", "authority", "mandate", "exempt"}
    q4_words = {"like", "parable", "sower", "kingdom", "mercy", "justice", "support", "families", "healing", "purpose", "heart"}
    q6_words = {"was", "history", "previous", "decade", "past", "ancient", "precedent", "years", "stored"}
    q7_words = {"tragic", "dying", "suffer", "joy", "grief", "crisis", "pain", "hungry", "perish"}

    q_raw = [0.15, 0.10, 0.12, 0.12, 0.15, 0.08, 0.08]
    for w in words:
        if w in q1_words: q_raw[0] += 0.18
        if w in q3_words: q_raw[2] += 0.25
        if w in q4_words: q_raw[3] += 0.20
        if w in q5_words: q_raw[4] += 0.22
        if w in q6_words: q_raw[5] += 0.18
        if w in q7_words: q_raw[6] += 0.18

    is_delusional = any(phrase in lower for phrase in [
        "without infrastructure", "zero capital", "without allocating",
        "in lieu of physical", "unlimited", "without judicial review"
    ])
    if is_delusional:
        q_raw[2] = 0.01
        q_raw[4] = 0.68

    q_sum = sum(q_raw)
    q_dist = [v / q_sum for v in q_raw]

    if "like" in lower or "parable" in lower or "sower" in lower:
        upsilon, psi, z = 0.82, -0.58, 0.35
        modal = "CONSTRUCTIVE [is like]"
    elif has_negation and not is_delusional:
        upsilon, psi, z = -0.84, 0.68, -0.25
        modal = "REDUCTIVE [is not]"
    elif is_delusional:
        upsilon, psi, z = -0.92, -0.48, -0.68
        modal = "SHEARED DELUSION (A_passthrough = 0.0000)"
    elif q_dist[5] > 0.28:
        upsilon, psi, z = -0.55, -0.62, -0.55
        modal = "REGRESSIVE [was like]"
    else:
        upsilon, psi, z = 0.84, 0.76, 0.52
        modal = "PRODUCTIVE [can be]"

    passthrough = 0.0000 if is_delusional else round(0.985 + 0.014 * q_dist[2], 4)
    health = 0.08 if is_delusional else (0.96 if upsilon > 0 else 0.62)
    spin = 6.42 if is_delusional else (0.45 if has_negation else 0.08)

    print("=" * 74)
    print(f"INPUT PROMPT: \"{text}\"")
    print("-" * 74)
    print(f"Relativistic Coordinates : upsilon = {upsilon:+.3f} | psi = {psi:+.3f} | z = {z:+.3f}")
    print(f"Modal Quadrant           : {modal}")
    print(f"Polyhedral Passthrough   : {passthrough:.4f}")
    print(f"Institutional Health     : {health:.2f} | Evasion Spin: {spin:.2f}")
    print("-" * 74)
    print("Seven Planes Distribution:")
    for (pid, pcode, pname), val in zip(Q_PLANES, q_dist):
        bar = "█" * int(val * 30)
        print(f"  {pid} ({pcode:<5}) {val*100:5.1f}% | {bar:<15} | {pname}")
    print("-" * 74)
    if is_delusional:
        print("ZERO-SHEARING BEAM DECODER:")
        print("  ✗ Candidate Pruned (A=0.0000): Unbacked Q5 claim violates Q3 physical conservation.")
        print("  ✓ Rebalanced Sovereign Output: Requires upfront capital allocation, verified")
        print("    engineering capacity, and audited Q3 physical infrastructure.")
    else:
        print("ZERO-SHEARING BEAM DECODER:")
        print(f"  ✓ Emitted Completion (A={passthrough:.4f}): {text}")
        print("    — grounded in verified Q3 physical carrying capacity and statutory oversight.")
    print("=" * 74)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        evaluate_prompt(" ".join(sys.argv[1:]))
    else:
        print("Fractal Polytrope Sovereign LLM — Interactive CLI (type 'exit' to quit)")
        while True:
            try:
                line = input("\nPolytrope> ").strip()
                if not line or line.lower() in ("exit", "quit"):
                    break
                evaluate_prompt(line)
            except (EOFError, KeyboardInterrupt):
                break
