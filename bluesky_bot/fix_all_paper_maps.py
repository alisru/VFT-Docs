import os, sys, re

CANONICAL_COMPASS = """```
                                    AXIS ψ (Action of Will)
                                  ▲ +2.0 (Active / Do)
                                  │
      [PRODUCTIVE QUADRANT]       │       [REDUCTIVE QUADRANT]
      "You": [me, me]             │       "Me": [you, me]
      For You, but Only for Me    │       Me and You, but Really for Me
                                  │
      ● GREATER GOOD (+1, +1)     │       ● LESSER EVIL (-1, +1)
        The Good Truth            │         The Bad Lie (Greatest Lie)
                                  │
    +1.0 (Others)                 │       -1.0 (Me)
    +0.5 (Other Being)            │       -0.5 (My Group)
      ● THE GOOD PREFERENCE       │       ● THE BAD PREFERENCE
        (+1.0, 0.0)               │         (-1.0, 0.0)
                                  │
◄─────────────────────────────────┼─────────────────────────────────► AXIS υ (Moral Intent)
+2.0 (Everyone)                  0.0 (No-one)                     -2.0 (Only Me)
INCLUSIVE / Egalitarian           │                                EXCLUSIVE / Anti-Egalitarian
"Revelation / Altruism"           │                                "Deception / Egotism"
                                  │
      ● LESSER GOOD (+1, -1)      │       ● GREATER EVIL (-1, -1)
        Good Lie (Lesser Good)    │         The Bad Truth
                                  │
      [CONSTRUCTIVE QUADRANT]     │       [REGRESSIVE QUADRANT]
      "You": [me, you]            │       "Me": [me, you]
      For You, Me and Everyone    │       For Me, only Me, and you take
      Give to everyone            │       what I don't need / Give to me
                                  │
                                  ▼ -2.0 (Counteractive / Do Not)
```"""

CANONICAL_GEODESIC_TRAJECTORIES = """```
                             CANONICAL GEODESIC TRAJECTORIES
                                 AXIS ψ (Action of Will)
                               ▲ +2.0 (Active / Do)
                               │
            [PATH OF GRACE]    │    [PATH OF DECEPTION]
        Concordant Alignment   │    Stated Good -> Hidden Extraction
        Vs(+1,+1) ───► Vr(+1,+1)│    Vs(+1,+1) ───► Vr(-1,+1) or (-1,-1)
                               │
   +1.0 ───────────────────────┼─────────────────────── -1.0
   INCLUSIVE                   │                   EXCLUSIVE
                               │
         [PATH OF REDEMPTION]  │    [PATH OF FALL]
         Friction Overcome     │    Descent into Extraction / Chaos
         Vs(+1,0) ───► Vr(+1,-1)│    Vs(-1,+1) ───► Vr(-1,-1)
                               │
                               ▼ -2.0 (Counteractive / Do Not)
                       AXIS υ (Moral Intent)
```"""

CANONICAL_THATCHER = """```
                  THATCHER PRIVATISATION LONGITUDINAL TRAJECTORY
                             AXIS ψ (Action of Will)
                           ▲ +2.0 (Active / Do)
                           │
       Phase 1: 1984       │
       "Popular Capitalism"│
       (+1.0, +1.0)        │
             ●             │
              \\            │
               \\           │
◄───────────────\\──────────┼────────────────────────► AXIS υ (Moral Intent)
+2.0 (Inclusive) \\        0.0 (Neutral)            -2.0 (Exclusive)
                  \\        │
                   ▼       │
               Phase 2: 1989
               Utility Sell-Off & Debt Extraction
               (-0.8, +0.6)│
                    \\      │
                     ▼     │
                 Phase 3: 1990+
                 Private Monopoly Debt & Sewage Pollution
                 (-1.4, -1.2)
                           │
                           ▼ -2.0 (Counteractive / Do Not)
```"""

paper_dir = os.path.join(os.path.dirname(__file__), "paper")

# 1. Update section_1_and_3_theory_and_math.md
p1 = os.path.join(paper_dir, "section_1_and_3_theory_and_math.md")
with open(p1, "r", encoding="utf-8") as f:
    c1 = f.read()

# Replace first diagram
c1 = re.sub(r"```[\s\S]*?AXIS ψ \(Will / Kinetic Action\)[\s\S]*?```", CANONICAL_COMPASS, c1)
# Replace section 1.3 trajectory diagram
c1 = re.sub(r"```[\s\S]*?Path of\s+Deception[\s\S]*?```", CANONICAL_GEODESIC_TRAJECTORIES, c1)

# Fix axis definitions
c1 = c1.replace("#### Axis $\\upsilon$ (Morality) — *Who Does This Benefit?*", "#### Axis $\\upsilon$ (Morality) — *Who Does This Benefit? (Inclusive vs. Exclusive)*")
c1 = c1.replace("#### Axis $\\psi$ (Will / Kinetic Energy) — *What is the Energy Doing?*", "#### Axis $\\psi$ (Will / Kinetic Action) — *What is the Energy Doing? (Active vs. Counteractive)*")
c1 = c1.replace("* **$+2.0$ (Productive Justice)**:", "* **$+2.0$ (Active / Do / Systemic Creation)**:")
c1 = c1.replace("* **$-2.0$ (Active Chaos / Collapse)**: Active kinetic dismantling", "* **$-2.0$ (Counteractive / Do Not / Destruction / Collapse)**: Counteractive friction, active kinetic dismantling")

with open(p1, "w", encoding="utf-8") as f:
    f.write(c1)
print("Updated section_1_and_3_theory_and_math.md")

# 2. Update section_2_evolutionary_chronology.md
p2 = os.path.join(paper_dir, "section_2_evolutionary_chronology.md")
with open(p2, "r", encoding="utf-8") as f:
    c2 = f.read()

c2 = re.sub(r"```[\s\S]*?Canonical Geodesic Trajectories on the \(υ, ψ\) Manifold[\s\S]*?```", CANONICAL_GEODESIC_TRAJECTORIES, c2)
with open(p2, "w", encoding="utf-8") as f:
    f.write(c2)
print("Updated section_2_evolutionary_chronology.md")

# 3. Update section_4_empirical_findings.md
p4 = os.path.join(paper_dir, "section_4_empirical_findings.md")
with open(p4, "r", encoding="utf-8") as f:
    c4 = f.read()

c4 = re.sub(r"```[\s\S]*?AXIS ψ \(Will / Action\)[\s\S]*?```", CANONICAL_COMPASS, c4)
c4 = c4.replace("ranging from $+2.0$ (Productive Justice / Creating Systemic Value)", "ranging from $+2.0$ (Active / Do / Systemic Creation)")
c4 = c4.replace("to $-2.0$ (Entropic Chaos / Value Destruction)", "to $-2.0$ (Counteractive / Do Not / Value Destruction)")
with open(p4, "w", encoding="utf-8") as f:
    f.write(c4)
print("Updated section_4_empirical_findings.md")

# 4. Update section_5_next_horizons_research_probe.md
p5 = os.path.join(paper_dir, "section_5_next_horizons_research_probe.md")
with open(p5, "r", encoding="utf-8") as f:
    c5 = f.read()

c5 = re.sub(r"```[\s\S]*?Phase 1: 1979[\s\S]*?```", CANONICAL_THATCHER, c5)
with open(p5, "w", encoding="utf-8") as f:
    f.write(c5)
print("Updated section_5_next_horizons_research_probe.md")

# 5. Recompile master manuscript
import compile_paper
print("All maps updated across all sections and master manuscript recompiled!")
