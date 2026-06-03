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
- [C] Objective ideal — what first-principles version of the stated goal required
- [+N] Additional standards as contextually required

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

### The p·t Moral Primitive (Grounding Definition)

**p in p·t is a probability mass distribution over future states, not a count of possibilities.** The measurement is whether probability mass is shifting toward or away from better future states over time. Good/bad/evil/saintly are all readings of the direction and force of that shift.

    good    =  Δ(p·t) > 0 (passive)   →  probability mass shifts toward better futures naturally
    bad     =  Δ(p·t) < 0 (passive)   →  probability mass drifts toward worse futures, usually by neglect
    evil    =  Δ(p·t) < 0 (active, premature)  →  probability mass is forced away from better futures before they resolve
    saintly =  Δ(p·t) > 0 (active, under Δ(p·t) < 0 pressure)  →  probability mass held on better futures against active closure force

**Neutral is not flat.** Neutral = maintaining the existing probability distribution over time. Within neutral, two stable strategies:
- **Conservative neutral**: adds things that worked before — restoring proven expansions, reproducing what previously shifted mass toward better states. Lower variance, backward-looking HOW.
- **Innovative neutral**: adds new things that could be better — exploring untested expansions, probing for new attractors in possibility space. Higher variance, forward-looking HOW.

Both produce Δ(p·t) ≈ 0 net, but interact differently over time. Conservative neutral in a declining system gradually becomes bad (proven patterns stop working). Innovative neutral carries optionality value not visible in current Δ.

The (υ, ψ) coordinate is the two-dimensional decomposition of this scalar:
- **υ** = who receives the p·t expansion (distribution/radius axis)
- **ψ** = the force direction of the action (energy axis)

Good and bad are **passive outcomes** (can occur without intent). Evil and saintly require an **engaged will** — this is why ψ = ±2.0 is structurally rare. Passive drift produces the ±1.0 band. Only someone actively pushing reaches ±2.0.

**The Chain Rule:** If any node in the causal chain produces Δ(p·t) < 0 and is not cancelled, the chain is bad regardless of the stated intent of any other node. This is not an average — it is a minimum.

---

**υ axis — SCOPE OF BENEFIT: radial field effect radius, stripped of stated intent:**

υ is a population scope scale, not a moral quality scale. υ measures the radius of the p·t expansion field — who and how many actually receive the expansion. The scope ceiling is the importance ceiling: a claim addressed to one person structurally cannot matter more than ±0.5 regardless of how extreme its local effect is.

Score υ as a weighted aggregate across scope levels (systemic/group/individual). When scope levels disagree, the aggregate pulls toward the failing level. Do not round to zone anchors — measure the actual field radius.

| υ | Beneficiary | Field effect |
|---|---|---|
| +2.0 | Everyone / All beings | Field expands to maximum radius (Systemic Justice) |
| +1.0 | Others / Other Beings — broad population, not personally motivated | Field expands to network (Greater Good) |
| +0.5 | Other / A Being — one person or narrow group | Field expands to adjacent node |
| 0.0 | No One | Field static (Neutral) |
| -0.5 | My Group only — benefit extracted at cost to others | Field contracts to local cluster (Lesser Evil) |
| -1.0 | Me — self-serving; others bear the cost | Field contracts to point |
| -2.0 | Only Me — pure extraction from all others | Field contracts to point, maximum extraction (Tyranny) |

**Scope caps:** A single-person claim cannot exceed ±0.5. A community-level claim cannot exceed ±1.0. Only genuine systemic reach justifies ±2.0.

---

**ψ axis — force direction of the p·t vector (Will/Energy):**

ψ measures the directional force of the will applied — active/passive, constructive/destructive. The axis itself is unchanged:
* **+2.0**: Active-Active (Actively creating systemic value for all / Productive Justice)
* **+1.0**: Passive-Active / Proactive (Creating, building, acting)
* **0.0**: Neutral (No meaningful force applied)
* **-1.0**: Passive-Passive / Withholding (Passive, allowing, suppressing, withholding)
* **-2.0**: Active-Passive / Destructive (Actively destroying or extracting value / Chaos)

The four positions (good/bad/evil/saintly) are **not** a 1:1 mapping onto ψ levels. They emerge from what the will *produces* given the environmental conditions:
- **Good**: will directed constructively, p·t expanding naturally (positive ψ in a cooperative or neutral environment)
- **Saintly**: the same constructive will operating **under active contraction pressure** — good-in-context against evil force. Defined by the environmental condition, not a higher ψ level.
- **Bad**: p·t declining passively — will absent, low, or misdirected; no active closure required
- **Evil**: will actively forcing Δ(p·t) < 0 before natural end — requires engaged will at negative ψ

The will within the activity is what elevates good into saintly. You can hold ψ = +1.0 and be saintly if the system is actively trying to close the futures you are holding open.

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
