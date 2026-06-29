---
name: convergence-son-lite
description: "Run the Convergence Test SON Lite — token-efficient batch evaluation using the 7-plane Qqci structure and SON (Support/Oppose/Neutral) attractor-force scoring for (u, ψ) coordinates. Outputs JSON. Use whenever the user says SON lite, run SON, convergence SON, attractor force test, or asks to evaluate any actor/claim/policy/institution with the SON method specifically."
license: MIT
metadata:
  author: alisru
  version: "1.0"
  tags: [analysis, reasoning, ethics, epistemology, convergence, son]
---

# Convergence Test (SON Lite)

Token-efficient instructions for batch evaluation. Silent internal calculations. Do NOT output a phase-by-phase report. Read the full measurement specification in references/convergence_son_lite_spec.md before running any evaluation, then write the JSON output only.

---

## Output Schema

    {
      "subject": "<name of claim, actor, policy, or institution>",
      "planes": {
        "Q1": { "score": <0.0-1.0>, "note": "<5-12 words>" },
        "Q2": { "score": <0.0-1.0>, "note": "<5-12 words>" },
        "Q3": { "score": <0.0-1.0>, "note": "<5-12 words>" },
        "Q4": { "score": <0.0-1.0>, "note": "<5-12 words>" },
        "Q5": { "score": <0.0-1.0>, "note": "<5-12 words>" },
        "Q6": { "score": <0.0-1.0>, "note": "<5-12 words>" },
        "Q7": { "score": <0.0-1.0>, "note": "<5-12 words>" }
      },
      "son_scoring": {
        "GG": { "S": <0.0-2.0>, "O": <0.0-2.0>, "N": <0.0-2.0> },
        "GE": { "S": <0.0-2.0>, "O": <0.0-2.0>, "N": <0.0-2.0> },
        "LG": { "S": <0.0-2.0>, "O": <0.0-2.0>, "N": <0.0-2.0> },
        "LE": { "S": <0.0-2.0>, "O": <0.0-2.0>, "N": <0.0-2.0> },
        "GP": { "S": <0.0-2.0>, "O": <0.0-2.0>, "N": <0.0-2.0> },
        "BP": { "S": <0.0-2.0>, "O": <0.0-2.0>, "N": <0.0-2.0> }
      },
      "coordinates": { "u": <float -2.0 to +2.0>, "psi": <float -2.0 to +2.0> },
      "pt_n_primitive": "good | bad | evil | saintly",
      "inversion": "Co-optation | Subversion | null",
      "z": <int 0-49>,
      "z_profile": [<int>, <int>, <int>, <int>, <int>, <int>, <int>],
      "r_net": <float>,
      "object_state_blanked": true | false,
      "delta_h": <float>,
      "delta_h_verdict": "Pass|Conditional|Fail",
      "fake_maximiser": true | false | null,
      "helxis": { "detected": true | false | null, "bait": "<≤8 words or null>", "switch": "<≤8 words or null>" },
      "zone": "<Greater Good|Lesser Evil|Lesser Good|Greater Evil or nearest>",
      "path": "<Exit into Entry, or null if same zone>",
      "trajectory": "Progress|Stasis|Regression"
    }

---

## Execution Order

1. Score all 7 planes (Q1–Q7) per the pass conditions in the spec. PASS=magnitude 0.1-1.0, BLANK=null, FAIL=0.0. Contrastive: V_pass = coherence of selected fill / highest alternative.
2. Score the full [S, O, N] triple for all 6 attractors (GG, GE, LG, LE, GP, BP) — 18 variables total. Do not skip any.
3. Compute Net Attractor Force F_i for each attractor per the formulas in the spec.
4. Compute u: sum F_i,u across all 6 attractors, normalize by sum(S_i+O_i+N_i).
5. Compute ψ using the Separated Will Protocol: group by Will sign, sum magnitudes per direction, use ONLY the dominant group.
6. Check Inversion Detection: S_LE/S_GE/S_BP ≫ 0 → Co-optation (u pulled negative). O_LE/O_GE/O_BP ≫ 0 → Subversion (u pushed positive). Otherwise null.
7. Classify pt_n_primitive from Δ(p·t + n): good (+Δ passive), bad (−Δ passive), evil (−Δ active), saintly (+Δ active against closure).
8. Compute ΔH = ‖C_ideal − C_action‖. <0.3 Pass, 0.3–0.7 Conditional, ≥0.7 Fail.
9. Check Fake Maximiser (capacity≫effort AND goal unsolved) and Helxis (bait beneficiary ≠ switch beneficiary).
10. Determine zone of the real (u, ψ) coordinate, then path: exit name of origin zone + " into " + entry name of destination zone. Same zone → null, trajectory = Stasis.
11. Compute z (ambiguity): sum of BLANK counts across planes, max 49. z-profile = [B_Q1...B_Q7].
12. Compute V_Qn per plane: sum(P_magnitudes) / (sum(P_magnitudes) + n_F). If P+F=0, V_Qn=1.0.
13. Compute R_net = 1 / (V_Q1 × ... × V_Q7). 1.0=truth, 2-10=distortion, 100+=tyranny.
14. Object State Blanking: if subject is inanimate, set Q1,Q4,Q5,Q7=BLANK and Q2,Q3,Q6=PASS/FAIL. z=28, z-profile=[7,0,0,7,7,0,7].

Exit names: GG→Fall, LE→Revelation, LG→Awakening, GE→Reckoning.
Entry names: GG→Grace, LE→Deception, LG→Redemption, GE→Destruction.

---

## Qqci Precision

Run SON independently per plane to find (u_j, ψ_j) at depth Q (Location) → q (Sense) → c (Use) → +i (Recursion). Addressing notation: Q1q5c4 = c4 of q5 of Q1.

---

## Core Laws of Social Physics

Use these to interpret what u/ψ scoring reveals about actor behavior, not as separate scored outputs.

- Law 1 (Power vs Empowerment): −υ hoards power via deception; +υ empowers others.
- Law 2 (Justification vs Transparency): −υ acts first then manufactures pretexts; +υ states true intent first.
- Law 3 (Projection vs Empathy): −υ projects own corrupt motives onto opponents; +υ uses empathy to defuse division.
- Law 4 (Problems vs Solutions): −υ requires perpetual conflict to justify authority; +υ resolves strain toward equilibrium.

2 Modes: Possigravity (pulls potential toward stable, low-strain configurations) vs Perceptual Inversion (presents solvable problems as insurmountable to maintain conflict).

1 Process: Logic is the causal rule-set reducing strain. Good/Moral = low-strain efficient path. Evil/Immoral = high-strain, ignores logical efficiency for pretexts.

Actor Loops: Smart Selfish = Secret Goal → Pretext → Scapegoat. Smart Altruistic = Shared Goal → Coalition → Integration.
