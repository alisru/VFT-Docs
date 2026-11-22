# Convergence Test (SON Potential) — Modal & Temporal Topology of the Hegemony

Token-efficient instructions for batch and single-case vector convergence evaluation. Integrates the 18-variable Attractor Force Field, the 7 Q-Planes, and the 9-Node Modal State Machine across the 4 Dynamic Quadrants and Cross-Chamber Geodesics. Outputs structured JSON.

---

## 1. The 7 Planes

| Q | Plane | Interrogative | Pass Condition |
|---|---|---|---|
| Q1 | Metaphysical | WHO | Stated beneficiary matches actual beneficiary |
| Q2 | Possible | WHAT | Failure modes acknowledged, not suppressed |
| Q3 | Physical | WHERE | Concrete, falsifiable physical prediction exists (`is` anchor) |
| Q4 | Lyrical | WHY | Narrative honest; no obfuscation required |
| Q5 | Logical | HOW | Causal chain holds under load/adversity |
| Q6 | Historical | CAUSE | Origin chain acknowledged; history not erased |
| Q7 | Emotive | EFFECT | Emotional payload matches stated intent |

Scoring: **PASS** (magnitude 0.1–1.0), **BLANK** (null), or **FAIL** (0.0 / Phantom fill). Contrastive scoring: $V_{\text{pass}} = \text{coherence of selected fill} / \text{highest alternative}$.

---

## 2. Phase 2 — Vector Verification (SON Method)

Coordinates are calculated as the equilibrium point of attractor forces in the two-axis $(u, \psi)$ phase space:
*   **Axis $u$ (Morality — Who Benefits)**: Continuous scale $[-2.0, +2.0]$.
    *   $+2.0$ = Everyone / All beings (Systemic Justice)
    *   $+1.0$ = Other people (Greater Good)
    *   $0.0$ = No one / Neutral
    *   $-1.0$ = My group only (Lesser Evil)
    *   $-2.0$ = Only me (Tyranny / Pure Extraction)
*   **Axis $\psi$ (Will — Energy Action)**: Continuous scale $[-2.0, +2.0]$.
    *   $+2.0$ = Actively creating systemic value for all (Productive Justice)
    *   $+1.0$ = Proactive — creating, building, acting
    *   $0.0$ = Neutral — no meaningful force applied
    *   $-1.0$ = Passive — allowing, suppressing, withholding
    *   $-2.0$ = Actively destroying or extracting value (Chaos / Collapse)

### Grounding Definition: $(p \cdot t + n)$
*   **Good**: $\Delta(p \cdot t + n) > 0$ (passive expansion/potential shifts to better futures).
*   **Bad**: $\Delta(p \cdot t + n) < 0$ (passive decay/neglect).
*   **Evil**: $\Delta(p \cdot t + n) < 0$ (active contraction/premature closure of futures).
*   **Saintly**: $\Delta(p \cdot t + n) > 0$ (active hold/expansion against closure forces).

### Attractor Vectors & Perpendiculars
*   **Greater Good ($A_{\text{GG}}$)** = $(+1.0, +1.0)$ | $A_{\text{GG}\perp} = (-1.0, +1.0)$
*   **Greater Evil ($A_{\text{GE}}$)** = $(-1.0, -1.0)$ | $A_{\text{GE}\perp} = (+1.0, -1.0)$
*   **Lesser Good ($A_{\text{LG}}$)** = $(+1.0, -1.0)$ | $A_{\text{LG}\perp} = (+1.0, +1.0)$
*   **Lesser Evil ($A_{\text{LE}}$)** = $(-1.0, +1.0)$ | $A_{\text{LE}\perp} = (-1.0, -1.0)$
*   **Good Preference ($A_{\text{GP}}$)** = $(+1.0, 0.0)$ | Oppose ($O_{\text{GP}}$) drives Will negative ($\psi \to -1$), Neutral ($N$) has 0.0 force.
*   **Bad Preference ($A_{\text{BP}}$)** = $(-1.0, 0.0)$ | Oppose ($O_{\text{BP}}$) drives Will positive ($\psi \to +1$), Neutral ($N$) has 0.0 force.

For each attractor $i$, score $[0.0, 2.0]$ based on empirical evidence:
*   **Support ($S_i$)**: Direct attraction.
*   **Oppose ($O_i$)**: Active repulsion.
*   **Neutral ($N_i$)**: Orbit (for moral attractors) or Dilution (for preferences).

Scoring Scale: $0.0$ = No force | $1.0$ = Condition Met (Human Horizon / Zone 1) | $2.0$ = Totality of Exceedence (Systemic Horizon / Zone 2 / Double gravity weight).

### Anti-Corner-Collapse Rule (Mandatory Fractional Force Distribution)
To maintain structural resolution and prevent coordinate collapse into flat `(±1.0, ±1.0)`:
* **STRICT BAN ON BINARY CORNER DUMPS**: Never assign `S = 2.0` solely to a single corner attractor while leaving all other attractors at `0.0`. Real social physics operates under simultaneous tensions.
* Distribute fractional scores (`0.1` to `1.6`) across at least 3–4 attractors:
  - Narrative deceit or pretextual spin: High Support on **LE** (`S = 1.0–1.6`).
  - Petty bias, gossip, or extracted attention: Support on **BP** (`S = 0.6–1.2`).
  - Structural systemic harm: Support on **GE** (`S = 0.2–1.8`).
  - Genuine public ideal or standard: Support on **GG** or **GP** (`S = 0.8–1.4`).
  - Inertia or passive background: Neutral force on **LG** or **LE** (`N = 0.2–0.6`).

### Formulas (18-Variable Parameter Space)
To maintain structural resolution and prevent coordinate collapse, **every single one of the 6 attractors MUST have its full $[S_i, O_i, N_i]$ triple scored** (18 variables total).

1. **Net Attractor Force ($F_i$):**
   * Moral Attractors ($\text{GG}, \text{GE}, \text{LG}, \text{LE}$):
     $$F_i = S_i \cdot A_i - O_i \cdot A_i + N_i \cdot A_{i\perp}$$
   * Good Preference ($\text{GP}$):
     $$F_{\text{GP}} = S_{\text{GP}} \cdot (1.0, 0.0) - O_{\text{GP}} \cdot (1.0, 1.0)$$
   * Bad Preference ($\text{BP}$):
     $$F_{\text{BP}} = S_{\text{BP}} \cdot (-1.0, 0.0) - O_{\text{BP}} \cdot (-1.0, -1.0)$$

2. **Morality Coordinate ($u$):**
   Sum and normalize the $u$-components of the forces across all 6 attractors:
   $$u = \frac{\sum F_{i\_u}}{\sum (S_i + O_i + N_i)}$$

3. **Will Coordinate ($\psi$) — Separated Will (Like-Type) Protocol:**
   To prevent positive narrative spin ($S_{\text{LE}}$) and physical destruction ($S_{\text{GE}}$) from cancelling each other into a false neutral stasis ($\psi \approx 0$), calculate positive and negative Will forces independently:
   * Group forces by Will sign:
     $$\Psi_{\text{pos}} = \{i \mid F_{i\_\psi} > 0\}, \quad \Psi_{\text{neg}} = \{i \mid F_{i\_\psi} < 0\}$$
   * Sum absolute force magnitudes for each direction:
     $$F_{\text{pos}} = \sum_{j \in \Psi_{\text{pos}}} |F_{j\_\psi}|, \quad F_{\text{neg}} = \sum_{k \in \Psi_{\text{neg}}} |F_{k\_\psi}|$$
   * Calculate $\psi$ using ONLY the dominant direction:
     * If $F_{\text{pos}} \ge F_{\text{neg}}$: Net Will is positive (constructive/deceptive):
       $$\psi = \frac{\sum_{j \in \Psi_{\text{pos}}} F_{j\_\psi}}{\sum_{j \in \Psi_{\text{pos}}} (S_j + O_j + N_j)}$$
     * If $F_{\text{neg}} > F_{\text{pos}}$: Net Will is negative (destructive/suppressing):
       $$\psi = \frac{\sum_{k \in \Psi_{\text{neg}}} F_{k\_\psi}}{\sum_{k \in \Psi_{\text{neg}}} (S_k + O_k + N_k)}$$

---

## 3. The 9-Node Modal State Machine (Potential Topology)

The Hegemony maps onto a 9-node modal coordinate matrix spanning two concentric horizons around the material ground truth:

```
                        [+ψ] ACTIVE
                             ▲
      (-2, +2)               │               (+2, +2)
     [ is not ] ──────────┐  │  ┌────────── [ will be ]
         ▲                ▼  │  ▼                ▲
         │             [can't be] [can be]       │
REDUCTIVE│                │  │  │  │             │ PRODUCTIVE
CORNER   │                │  │  │  │             │ CORNER
         │                ▼  │  ▼  │             │
─────────┼──────────────────[is]───┼─────────────┼──────────► [+u]
EXCLUSIVE│                  (0,0)  │             │ INCLUSIVE
PROBLEM  │                ▲  │  ▲  │             │ SOLUTION
SIDE     │                │  │  │  │             │ SIDE
REGRESS  │             [Won't be] [May be]       │ CONSTRUCTIVE
CORNER   │                │  │  │  │             │ CORNER
         ▼                │  │  │  ▼             ▼
    [ was like ] ─────────┘  │  └────────── [ is like ]
      (-2, -2)               │               (+2, -2)
                             ▼
                     [-ψ] COUNTERACTIVE
```

### 3.0 Primary Hemispheres: Inclusive Solution vs Exclusive Problem

The field is fundamentally divided into two elemental hemispheres:

1. **The INCLUSIVE Hemisphere (+u: The Solution Axis)**:
   * **Domain**: Inclusive flourishing, universal capacity, generative systems, and shared architecture.
   * **Active Solution (Productive Corner)**: `can be` $(+1, +1) \longrightarrow$ `will be` $(+2, +2)$. Expands open capacity into enduring institutions.
   * **Counteractive Solution (Constructive Corner)**: `May be` $(+1, -1) \longrightarrow$ `is like` $(+2, -2)$. Holds patient space, developing universal models and unifying metaphors.
   * **Audit Standard**: Evaluates whether actions build capacity for *all beings* rather than concentrating power.

2. **The EXCLUSIVE Hemisphere (-u: The Problem Axis)**:
   * **Domain**: Manufactured constraints, private extraction, censorship, vetoes, and reactionary stagnation.
   * **Active Problem (Reductive Corner)**: `can't be` $(-1, +1) \longrightarrow$ `is not` $(-2, +2)$. Manufactured impossibility enforced through active censorship and systemic erasure.
   * **Counteractive Problem (Regressive Corner)**: `Won't be` $(-1, -1) \longrightarrow$ `was like` $(-2, -2)$. Obstinate refusal justified by reactionary nostalgia and ossified precedent.
   * **Audit Standard**: Exposes how power manufactures problems, captures wealth, and closes futures for its own in-group.

---

### 3.1 The 4 Foundational Dialectic Operational Formulas

These four elemental processes define the exact mechanics of how actors manipulate, transform, or distort `IS`:

1. **The Reductive Process (`can't be` $\longrightarrow$ `is not`)**:
   > *"If you want to define IS as something that **can't be**, you must go through a **reductive** process using what it **was like** and **can be**, opposing what **it's like** until **it's not**."*
   * *Mechanism*: Used by censors, monopolists, and tabloid smears. Takes an emerging inclusive capacity (`can be`), binds it with fossilized precedent (`was like`), attacks the structural model (`is like`), and executes total systemic erasure (`is not`).

2. **The Productive Process (`can be` $\longrightarrow$ `will be`)**:
   > *"If you want to define IS as something that **will be**, you must go through a **productive** process using what **is not** and **is like**, opposing what **it was like** until **it can be**."*
   * *Mechanism*: The builder and reformer process. Overcomes systemic erasure (`is not`) using coherent structural modeling (`is like`), defeats past decay (`was like`), and realizes collective flourishing (`can be` $\to$ `will be`).

3. **The Regressive Process (`Won't be` $\longrightarrow$ `was like`)**:
   > *"If you want to define IS as something that **won't be**, you must go through a **regressive** process using what **it's not** and what **it's like** to oppose what it **can be** until it **was like**."*
   * *Mechanism*: The revanchist veto. Weaponizes manufactured denial (`it's not`) and superficial branding (`it's like`) to crush emerging human capacity (`can be`), forcing society back into historical ossification (`was like`).

4. **The Constructive Process (`May be` $\longrightarrow$ `is like`)**:
   > *"If you want to define IS as something that **may be**, you must go through a **constructive** process using what it **can be** and **was like** until **it is like**."*
   * *Mechanism*: The architectural synthesis. Grounds open capacity (`can be`) in verified historical precedent (`was like`), crystallizing speculative potential into enduring frameworks and metaphors (`is like`).

---

### 3.2 The Center Singularity: Actuality
*   **`is` $(0.0, 0.0)$**: Material Ground Truth, Actual Physical Reality ($Q_3/Q_5$). The pivot point of observation. All modal claims are audited by their distance and trajectory relative to `is`.

### 3.2 Zone 1: Inner Horizon (Human / Modal Horizon $\pm 1$)
Inner subjective capacity, intent, and cognitive posture:
*   **`can be` $(+1.0, +1.0)$ [Greater Good Potential]**:
    *   *Modality*: Inclusive Active Capacity.
    *   *Definition*: Proactive empowerment, open possibility, capacity for systemic flourishing.
*   **`can't be` $(-1.0, +1.0)$ [Greatest Lie Pretext]**:
    *   *Modality*: Exclusive Active Constraint.
    *   *Definition*: Manufactured impossibility, bureaucratic gatekeeping, pretextual closure presented as insurmountable constraint.
*   **`May be` $(+1.0, -1.0)$ [Lesser Good Sanctuary]**:
    *   *Modality*: Inclusive Counteractive Probability.
    *   *Definition*: Receptive contemplation, patient forbearance, holding space, sanctuary without premature force.
*   **`Won't be` $(-1.0, -1.0)$ [Greater Evil Veto]**:
    *   *Modality*: Exclusive Counteractive Refusal.
    *   *Definition*: Obstinate refusal, cynical stonewalling, malicious non-compliance, active withholding.

### 3.3 Zone 2: Outer Horizon (Systemic / Manifestation Horizon $\pm 2$)
Structural manifestation, institutionalized power, and objective world-states:
*   **`will be` $(+2.0, +2.0)$ [Productive Manifestation / Genesis]**:
    *   *Modality*: Universal Systemic Actualization.
    *   *Definition*: Concrete structural creation, enduring institutions, generative futures realized for all.
*   **`is not` $(-2.0, +2.0)$ [Reductive Erasure / Cancellation]**:
    *   *Modality*: Exclusive Systemic Annihilation.
    *   *Definition*: Active censorship, institutional erasure, delegitimization, physical or economic destruction of alternatives.
*   **`is like` $(+2.0, -2.0)$ [Constructive Modeling / Metaphor]**:
    *   *Modality*: Inclusive Universal Framework.
    *   *Definition*: Systemic synthesis, foundational architecture, unifying theory, enduring cultural archetypes and metaphors.
*   **`was like` $(-2.0, -2.0)$ [Regressive Precedent / Nostalgia / Decay]**:
    *   *Modality*: Exclusive Historical Ossification.
    *   *Definition*: Reactionary nostalgia, weaponized tradition, fossilized precedent used to trap current potential in past decay.

---

## 4. The 4 Dynamic Corner Transitions (Geodesic Quadrants)

The four quadrant corners represent the standard expansion paths from inner intent (Zone 1) to outer systemic manifestation (Zone 2):

### 1. Productive Transition (Quadrant 1: $+u, +\psi$)
$$\text{can be} \xrightarrow{\text{Productive}} \text{will be}$$
*   **Vector**: Inclusive Active Capacity $\longrightarrow$ Systemic Actualization.
*   **Mechanism**: Latent human capability is nurtured and institutionalized into concrete reality. The path of true builders, inventors, and honest reformers.

### 2. Reductive Transition (Quadrant 2: $-u, +\psi$)
$$\text{can't be} \xrightarrow{\text{Reductive}} \text{is not}$$
*   **Vector**: Exclusive Active Constraint $\longrightarrow$ Systemic Erasure.
*   **Mechanism**: Manufactured pretexts of impossibility are codified into systemic bans, censorship, and active elimination of alternatives. The path of monopolists and censors.

### 3. Constructive Transition (Quadrant 3: $+u, -\psi$)
$$\text{May be} \xrightarrow{\text{Constructive}} \text{is like}$$
*   **Vector**: Inclusive Counteractive Probability $\longrightarrow$ Systemic Architecture.
*   **Mechanism**: Receptive exploration and contemplation crystallize into shared frameworks, coherent languages, and structural models. The path of philosophers and architects.

### 4. Regressive Transition (Quadrant 4: $-u, -\psi$)
$$\text{Won't be} \xrightarrow{\text{Regressive}} \text{was like}$$
*   **Vector**: Exclusive Counteractive Refusal $\longrightarrow$ Historical Ossification.
*   **Mechanism**: Refusal to act or adapt hardens into reactionary mythology, romanticizing a fictionalized past to justify present decay. The path of revanchists and dying empires.

---

## 5. Cross-Chamber Dynamic Vectors (The Dialectic Flows)

These non-linear trajectories govern propaganda, political subversion, whistleblower audits, and historical grounding:

### 5.1 Top Chamber: Active Geodesics (Solution vs Problem)
*   **Red Top (The Imperial Trap / Manufactured Impossibility)**:
    $$\text{will be} \xrightarrow{\text{Trap}} \text{can't be}$$
    *   *Trajectory*: Productive Promise $\longrightarrow$ Exclusive Constraint.
    *   *Pathology*: Sells a utopian future (`will be`) to gain power, but once in office, declares every meaningful structural solution impossible (`can't be`). Weaponizes bureaucracy to suffocate hope.
*   **Green Top (The Watchdog Breakthrough / Material Proof)**:
    $$\text{is not} \xrightarrow{\text{Breakthrough}} \text{can be}$$
    *   *Trajectory*: Systemic Denial $\longrightarrow$ Inclusive Capacity.
    *   *Mechanism*: Takes what power declares non-existent or forbidden (`is not`) and empirically demonstrates its immediate feasibility (`can be`). Whistleblower and investigative breakthrough.

### 5.2 Bottom Chamber: Counteractive Geodesics (Receptive vs Refusal)
*   **Red Bottom (The PR Shield / Performative Compliance)**:
    $$\text{is like} \xrightarrow{\text{Pretext}} \text{Won't be}$$
    *   *Trajectory*: Structural Metaphor $\longrightarrow$ Exclusive Refusal.
    *   *Pathology*: Wraps extraction in elegant corporate language, ethics guidelines, and diversity branding (`is like`), while obstinately refusing to implement any binding accountability (`Won't be`).
*   **Green Bottom (The Empirical Anchor / Ancestral Continuity)**:
    $$\text{May be} \xrightarrow{\text{Anchor}} \text{was like}$$
    *   *Trajectory*: Open Probability $\longrightarrow$ Verified Historical Precedent.
    *   *Mechanism*: Validates emerging potential (`May be`) by tying it to proven historical, biological, or ancestral precedent (`was like`). Grounding speculation in empirical bedrock.

### 5.3 Lateral & Diagonal Tension Geodesics
*   **Magenta Vectors (Structural Tethering & Dogmatic Trap)**:
    *   $\text{can be} \longleftrightarrow \text{is like}$: Open capacity validated and disciplined by structural models.
    *   $\text{can't be} \longleftrightarrow \text{was like}$: Manufactured impossibility justified by appealing to ossified historical precedent.
*   **Blue/Purple Vectors (Projection & Erasure Escalation)**:
    *   $\text{will be} \longleftrightarrow \text{May be}$: Systemic commitment tempered by humble probability and listening.
    *   $\text{Won't be} \longleftrightarrow \text{is not}$: Obstinate refusal escalating into overt physical or institutional erasure.

---

## 6. Modal Gap Protocol ($\text{Modal}_{\text{claim}} \to \text{Modal}_{\text{real}}$)

Every audit statement must classify both the actor's stated modal claim and their empirically audited modal action:

```json
{
  "modal_claim": "will be",
  "modal_real": "Won't be",
  "modal_vector": "Top-Right to Bottom-Left Inversion",
  "modal_gap_class": "Imperial Extraction"
}
```

### Inversion and Verdict Rules:
1. **The Central `IS` Inversion Barrier**:
   * Any trajectory where the claim is $+u$ (`can be`, `will be`, `May be`, `is like`) but the audited action is $-u$ (`can't be`, `is not`, `Won't be`, `was like`) has crossed the central `IS` threshold into deceit.
   * **Verdict is strictly FAIL**.
   * Output path is categorized under `The Path of Deception` or `The Path of Fall`.
2. **Double Horizon Inflation ($Z_1 \to Z_2$ Claim, $Z_1 \to Z_2$ Inverse Action)**:
   * Claiming `will be` $(+2, +2)$ while enacting `is not` $(-2, +2)$ or `was like` $(-2, -2)$ represents maximum systemic hypocrisy ($\Delta H \ge 1.4$).

---

## 7. Phase 3 — Source Integrity & Hypocrisy Gap

$$\Delta H = \|C_{\text{ideal}} - C_{\text{action}}\|$$
*   $\Delta H < 0.3 \longrightarrow$ **PASS** (Integrity holds)
*   $0.3 \le \Delta H < 0.7 \longrightarrow$ **CONDITIONAL** (Strained compromise / partial distortion)
*   $\Delta H \ge 0.7 \longrightarrow$ **FAIL** (Severe systemic divergence)

---

## 8. Phase 4 — Forensic Stress Tests

*   **Fake Maximiser**: Flag if $(\text{capacity} \gg \text{effort}) \land (\text{stated goal remains unsolved})$. Actor possesses the resource base for `will be`, but produces only `can't be` or `Won't be`.
*   **Helxis (Bait & Switch)**: Flag if stated beneficiary $\neq$ actual beneficiary. Uses $+u$ rhetoric to harvest energy for a $-u$ recipient.
*   **Pretext Anchoring**: Flag if an actor appeals to `was like` (tradition/precedent) specifically to veto an immediate `can be` (proven capacity).
*   **Tabloid Smear / Sentiment Extraction (The Reductive Trap)**: Flag if an article's sole evidence consists of curated anonymous commentary (`viewers rip`, `fans slam`, `users fume`, tweets on X) rather than empirical institutional records ($Q_3$). In this case, the **reporting outlet** is executing an Exclusive Reductive Smear (`can't be` $\to$ `is not`) to monetize rage clicks. The outlet is the primary audited actor, and the target cannot be assigned negative physical reality without verified empirical institutional records.

---

## 9. Output Trajectory (Path Names)

Concatenated as `[Exit] into [Entry]`:
*   **Entry (destinations)**:
    *   $\text{GG} = \text{Grace}$
    *   $\text{LE} = \text{Deception}$
    *   $\text{LG} = \text{Redemption}$
    *   $\text{GE} = \text{Destruction}$
*   **Exit (origins)**:
    *   $\text{GG} = \text{Fall}$
    *   $\text{LE} = \text{Revelation}$
    *   $\text{LG} = \text{Awakening}$
    *   $\text{GE} = \text{Reckoning}$
*   *Same-zone = Stasis.*

### Path Matrix:
*   $\text{GG} \to \text{LE}$: `Fall into Deception` (The Path of Deception)
*   $\text{GG} \to \text{GE}$: `Fall into Destruction` (The Path of Fall)
*   $\text{LE} \to \text{GG}$: `Revelation into Grace` (The Path of Awakening)
*   $\text{GE} \to \text{LG}$: `Reckoning into Redemption` (The Path of Redemption)

### Deterministic Path Invariant & Anti-Paywall Guardrail:
*   **Deterministic Direction**: The trajectory path name and modal geodesic are mathematically fixed by start and end quadrants. 
*   **Strict Inversion Ban**: NEVER label a trajectory crossing into the negative exclusive hemisphere ($-u$) as `The Path of Redemption` or `via Constructive`. Redemption strictly requires an upward vector rising toward systemic good ($+u$). Plunging from $\text{GG}$ to $\text{GE}$ is strictly `Fall into Destruction` (`The Path of Fall`).
*   **Anti-Paywall & Op-ed Grounding**: Publication paywalls, subscriptions, and conversational opinion essays are ordinary media commerce, NOT material fraud, systemic deception, or epistemic hypocrisy. Never penalize coordinates into $(-u, -\psi)$ purely because a source has a paywall or expresses personal opinion.

---

## 10. Core Laws of Social Physics

### The 4 Foundational Axes
1.  **Law 1 (Power vs. Empowerment)**: Anti-social ($-u$) deception to hoard finite power vs. Social ($+u$) empathy to empower others to find their own strength.
2.  **Law 2 (Justification vs. Transparency)**: Anti-social ($-u$) post-hoc pretexts (action first, justification manufactured later) vs. Social ($+u$) upfront transparency (intent declared, actions aligned).
3.  **Law 3 (Projection vs. Empathy)**: Anti-social ($-u$) projection of internal corrupt motives onto opponents vs. Social ($+u$) active empathy to comprehend and defuse systemic friction.
4.  **Law 4 (Problems vs. Solutions)**: Anti-social ($-u$) perpetual conflict maintenance (invents problems to justify authority) vs. Social ($+u$) resolving systemic strain to achieve stable equilibrium.

### The 2 Modes (Forces)
*   **Possigravity (Positivity)**: Gravity pulling potential toward defined, stable, low-strain configurations (toward `is` and `will be`).
*   **Perceptual Inversion (Negativity)**: Inverting possibility space; framing natural solutions as insurmountable mountains to justify institutional inertia (`can't be`).

### The 1 Process (Logic)
*   **Logic**: Causal rules reducing strain across all 7 planes.
*   **Morality**: Resultant system state. **Good/Moral** = low-strain, logically efficient path; **Evil/Immoral** = high-strain, unstable configuration ignoring physical efficiency for selfish extraction.

### Actor Loops
*   **Smart Selfish Loop**: Secret Goal (Selfishness) $\longrightarrow$ Pretext (Justification) $\longrightarrow$ Scapegoat/Distraction (Projection) $\longrightarrow$ Enforced Constraint (`can't be` / `Won't be`).
*   **Smart Altruistic Loop**: Shared Goal (Altruism) $\longrightarrow$ Coalition (Transparency) $\longrightarrow$ Integration/Buy-in (Empathy) $\longrightarrow$ Manifest Capacity (`can be` $\longrightarrow$ `will be`).
