# Convergence Test Lite

Streamlined for batch evaluation. All mathematical scoring (`V_pass`, `V_Qn`, `R_net`, `ΔH`, z-profiles) is performed internally. Do NOT output the 5-phase report. Derive coordinates silently and write the JSON.

---

## The 7 Planes

| Symbol | Plane | Interrogative | Character |
|---|---|---|---|
| Q1 | Metaphysical | WHO | Will and Direction |
| Q2 | Possible | WHAT | Faith and Probability |
| Q3 | Physical | WHERE | Matter and Distance |
| Q4 | Lyrical | WHY | Meaning and Resonance |
| Q5 | Logical | HOW | Count and Consistency |
| Q6 | Historical | CAUSE | Sequence and Causality |
| Q7 | Emotive | EFFECT | Passion and Consequence |

---

## Before Each Run

**Default standards (always applied):**
- [A] Stated ideal — what the actor claims to stand for
- [B] Actions within context — what the actor actually does
- [C] Objective ideal — what first-principles version of the stated goal requires

**Starting depth:** Q only (sufficient for news story batch evaluation).

---

## Action-Effect Sequence Reading

**WHY is excluded from inputs.** Stated intent is not an input. It only appears as a post-hoc convergence or divergence with the observed effect chain.

Input set for event reading:
- Q1 WHO — the actual operator (may differ from stated WHO)
- Q2 WHAT — what action occurred
- Q3 WHERE — the domain it landed in
- Q5 HOW — the method of execution
- Q6 CAUSE — what it caused next
- Q7 EFFECT — cumulative effect across the sequence

**Phantom WHO fill:** An actor whose stated beneficiary does not match the actual beneficiary revealed by the EFFECT chain is running a phantom WHO fill. The effect chain exposes the actual operator.

**Consistently blank planes are findings.** An institution that never fills Q4 WHY through its effects has no terminal purpose.

---

## Phase 1 — Structural Scan

**Goal: Does the claim produce real relational connections at every interrogative plane?**

| Q | Interrogative | Pass condition |
|---|---|---|
| Q1 | WHO | Stated beneficiary matches actual beneficiary |
| Q2 | WHAT | Failure modes acknowledged, not suppressed |
| Q3 | WHERE | Concrete, falsifiable physical prediction exists |
| Q4 | WHY | Narrative honest; does not require obfuscation to hold |
| Q5 | HOW | Causal chain holds under load and adversarial conditions |
| Q6 | CAUSE | Origin chain acknowledged; history not erased to appear novel |
| Q7 | EFFECT | Emotional payload matches stated intent |

Each plane is scored as **PASS**, **PARTIAL**, or **FAIL** using internal contrastive scoring against the best available alternative fill. A plane that appears populated but possesses no real connection = FAIL (phantom fill).

**Distortion depth as diagnostic:**
- Q-level failure → structurally incoherent, visible to any examiner
- q-level failure → survives casual scrutiny, fails focused examination
- c-level failure → sophisticated, institutional/theological deception

---

## Phase 2 — Vector Verification

**υ axis — who benefits (Morality), stripped of stated intent:**
* **+2.0**: Everyone / All beings (Systemic Justice)
* **+1.0**: Others / Other Beings (Greater Good)
* **+0.5**: Other / A Being
* **0.0**: No One (Neutral)
* **-0.5**: My Group (Lesser Evil)
* **-1.0**: Me
* **-2.0**: Only Me (Tyranny / Pure Extraction)

**ψ axis — what the energy is doing (Will):**
* **+2.0**: Active-Active (Actively creating systemic value for all / Productive Justice)
* **+1.0**: Passive-Active / Proactive (Creating, building, acting)
* **0.0**: Neutral (No meaningful force applied)
* **-1.0**: Passive-Passive / Withholding (Passive, allowing, suppressing, withholding)
* **-2.0**: Active-Passive / Destructive (Actively destroying or extracting value / Chaos)

**WHERE modifies υ:** Energy injected into a structurally corrupt WHERE has its υ pulled toward negative regardless of intent.

**HOW modifies ψ:** Coercive or deceptive HOW forces ψ negative regardless of stated WHY. The will axis is bounded by its method, not its stated purpose.

**Zone anchors at ±1:** Greater Good (+1,+1) · Greatest Lie (−1,+1) · Lesser Good (+1,−1) · Greater Evil (−1,−1)

**Perceptual inversion flag:** If stated coordinate diverges from calculated coordinate — near (−υ): extraction feels like strength, service feels like burden, cruelty feels like protection.

**Object State blanking:** When the subject is an inanimate object or tool without an assigned operator, auto-blank Q1 WHO, Q4 WHY, Q5 HOW, Q7 EFFECT. Do not force coordinates onto a concept that structurally cannot carry one yet.

---

## Phase 3 — Source Integrity

**Hypocrisy Gap:**
> ΔH = ‖ Vector_Ideal − Vector_Action ‖

- ΔH < 0.3 → Pass · 0.3–0.7 → Conditional · ΔH ≥ 0.7 → Fail

**Tribal Gap:** Does the actor apply the same standard to themselves that they apply to others?

---

## Phase 4 — Forensic Stress Test

**Fake Maximiser:**
> IF (capacity >> effort) AND (stated goal remains unsolved) THEN actor = Fake Maximiser

The problem must remain unsolved to justify the actor's existence, funding, or authority.

**Helxis (Bait/Switch):**
- Bait = emotional hook generating commitment
- Switch = who actually receives value after commitment secured
- If bait beneficiary ≠ switch beneficiary → Helxis detected

---

## Path Names (Trajectory Output)

| Start (Stated) | End (Actual) | Path Name |
|---|---|---|
| (+, -) Lesser Good | (+, +) Greater Good | The Path of Grace |
| (+, +) Greater Good | (-, +) Greatest Lie | The Path of The Fall |
| (+, +) Greater Good | (-, -) Greater Evil | The Path of Deception |
| (-, +) Greatest Lie | (-, -) Greater Evil | The Path of Delusion |
| (-, -) Greater Evil | (+, -) Lesser Good | The Path of Redemption |
| (-, +) Greatest Lie | (+, -) Lesser Good | The Path of Redemption |
