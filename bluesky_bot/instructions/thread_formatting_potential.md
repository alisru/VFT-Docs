# Thread Formatting Protocol & JSON Schema (SON Potential Edition)

This document defines the strict output schema and logical steps sequence for Aletheia Bot fact-checks under the 6-Attractor SON Potential convergence model (incorporating the 9-Node Modal & Temporal Topology of the Hegemony).

---

## 1. The 34-Key Conversational JSON Schema & Blueprint (Macro & Potential-Enabled)

Every story config JSON file saved under `stories/` or `stories/live/` must be a list containing a single dictionary: `[ { ... } ]`. It must contain **only** the allowed keys in standard order:

1. `"thinking"`: The detailed step-by-step thinking/scratchpad calculations (Phase 1 to 5).
2. `"subject"`: Clean title of the news story.
3. `"link"`: The actual external news article URL.
4. `"claim_u"`: Stated claim Morality decimal (`-2.0` to `+2.0`).
5. `"claim_psi"`: Stated claim Will decimal (`-2.0` to `+2.0`).
6. `"real_u"`: Actual ground-level Morality decimal (`-2.0` to `+2.0`).
7. `"real_psi"`: Actual ground-level Will decimal (`-2.0` to `+2.0`).
8. `"mode"`: `"reply"` or `"root"`.
9. `"target_url"`: The target Bluesky post URL we are replying to (only when `mode` is `"reply"`).
10. `"stated_forces"`: A dictionary of the 6 attractor $[S, O, N]$ scores for the Stated Claim.
11. `"actual_forces"`: A dictionary of the 6 attractor $[S, O, N]$ scores for the Actual Reality.
12. `"posts"`: A list of exactly 13 strings (the logical steps detailed below).
13. `"rkeys"`: (Optional) List of Bluesky post keys (added automatically when live).
14. `"post_urls"`: (Optional) List of posted thread URLs (added automatically when live).
15. `"status"`: `"COMPLETED DRY RUN"` or `"LIVE"`.
16. `"id"`: Clean string slug serving as the unique identifier.
17. `"macro_event"`: (Optional) Overarching macro context/venue name, or `""` if none.
18. `"macro_claim_u"`: (Optional) Stated claim Morality decimal for the macro context, or null if none.
19. `"macro_claim_psi"`: (Optional) Stated claim Will decimal for the macro context, or null if none.
20. `"macro_real_u"`: (Optional) Actual ground-level Morality decimal for the macro context, or null if none.
21. `"macro_real_psi"`: (Optional) Actual ground-level Will decimal for the macro context, or null if none.
22. `"claim_rnet"`: Stated claim R_net integrity score (float).
23. `"real_rnet"`: Actual ground-level R_net integrity score (float).
24. `"claim_z"`: Stated claim uncertainty score (int).
25. `"real_z"`: Actual ground-level uncertainty score (int).
26. `"claim_z_profile"`: Stated claim blank counts array of 7 integers.
27. `"real_z_profile"`: Actual ground-level blank counts array of 7 integers.
28. `"claim_integrity"`: Stated claim 7-tier scale integrity label (string).
29. `"real_integrity"`: Actual ground-level 7-tier scale integrity label (string).
30. `"modal_claim"`: Stated claim Modal node string (e.g. `"will be"`, `"can be"`, `"May be"`, `"is like"`).
31. `"modal_real"`: Actual ground reality Modal node string (e.g. `"can't be"`, `"Won't be"`, `"is not"`, `"was like"`, `"is"`).
32. `"modal_vector"`: Trajectory description (e.g. `"Top-Right to Bottom-Left Inversion"`, `"Productive Transition"`, `"Red Top Imperial Trap"`).
33. `"geodesic"`: Dynamic Geodesic name (e.g. `"Red Top (The Imperial Trap)"`, `"Red Bottom (The PR Shield)"`, `"Productive Geodesic"`, `"Regressive Geodesic"`, `"Magenta Vector"`).
34. `"central_is_barrier_crossed"`: Boolean (`true`/`false`) indicating if trajectory crossed the central IS barrier from $+u$ to $-u$.

*Note: DO NOT include `subject_slug`, `verdict`, `graph_img`, or any other custom keys in the JSON config. These are handled dynamically by the registry builder.*

---

## 2. Attractor Forces Schema & Anti-Corner-Collapse Standard

The `"stated_forces"` and `"actual_forces"` keys must map to dictionaries containing scores for all 6 attractors (`GG`, `GE`, `LG`, `LE`, `GP`, `BP`). For each attractor, you must provide the Support (`S`), Oppose (`O`), and Neutral (`N`) forces as decimals between `0.0` and `2.0`.

### Anti-Corner-Collapse Rule (Mandatory Fractional Force Distribution):
* **STRICT BAN ON CORNER DUMPS**: NEVER dump binary `2.0`s into a single attractor with `0.0`s elsewhere. That collapses the mathematics into a crude flat `(±1.0, ±1.0)`.
* Every real-world event exerts tension across multiple attractors simultaneously:
  - Deceptive PR/spin or tabloid narrative exerts high Support on **LE** (`S = 1.0–1.6`).
  - Petty bias, gossip, or greed exerts Support on **BP** (`S = 0.6–1.2`).
  - Systemic harm exerts Support on **GE** (`S = 0.2–1.8`).
  - Stated ideals exert Support on **GG** or **GP** (`S = 0.8–1.4`).
  - Institutional inertia or passive leisure exerts Neutral weight on **LG** or **LE** (`N = 0.2–0.6`).
* **Multi-Vector Requirement**: Distribute fractional scores across at least 3–4 attractors to reflect the true vector tension and produce nuanced, non-flat decimal coordinates (e.g. `u = -0.75, psi = +0.65`).

Format:
```json
"stated_forces": {
  "GG": {"S": 1.0, "O": 0.0, "N": 0.2},
  "GE": {"S": 0.0, "O": 0.8, "N": 0.0},
  "LG": {"S": 0.4, "O": 0.0, "N": 0.2},
  "LE": {"S": 0.0, "O": 0.4, "N": 0.0},
  "GP": {"S": 1.2, "O": 0.0, "N": 0.0},
  "BP": {"S": 0.0, "O": 0.6, "N": 0.0}
}
```

---

## 3. Conversational Formatting & ELI18 Language Standard

* **ELI18 Reading Level (Target Voice)**:
  - Write at an engaging, articulate undergraduate / high-school senior level (ELI18).
  - **No Point Loss**: Preserve full analytical precision, exact figures, names, and two-axis coordinates `(υ, ψ)`, but explain them with crystal-clear, accessible sentence structures.
  - **Anti-Jargon & Anti-Gatekeeping**: Strictly ban obscure academic pretension, impenetrable Latinisms, and circular jargon loops (e.g. do not say "smart altruistic loop" or "metaphysical teleological error"—say "empowering local communities with transparent funding" or "confusing the tool for the decision-maker").
  - **Vivid, Relatable Dynamics**: Ground structural analysis, institutional friction, and social physics in relatable human reality (e.g. who captures the profit, who bears the burden, and where the bait-and-switch takes place).
* **BAN on Numbered Prefixes**: NEVER write `Post 1:`, `Post 2:`, `1. Hook:`, or any numeric labels at the start of posts. Each array element must be clean editorial text.
* **BAN on Robotic Titles**: Do not start steps with dry prefixes like `Subject:`, `The Claim:`, `The Reality:`, or `What's happening:`. (Headers explicitly outlined in the steps below are permitted).
* **Character Budget**: Keep each individual post strictly under 280 characters (hard max 290) to ensure seamless posting to Bluesky.
* **Natural Human Flow**: Write in clean, conversational Plain English. Use headers only when they are clean and natural (e.g. `The Bright Side:`, `The Poison:`).
* **Character Caps**: Keep every single step strictly under **275 characters** in the JSON config to prevent dynamic text-splitting errors.
* **NO Orphan Words**: DO NOT split sentences arbitrarily or waste array elements. If a sentence fits in the current post, include it. Do NOT make a single post containing just 1 or 2 words (like 'dysfunction.'). Write continuously and naturally, only hard-splitting concepts when approaching the 275-character limit.
* **Ground Truth & Institutional Anchoring (3 Pillars)**:
  - Always anchor the audit in the real-world event and its primary actors, NOT in media punditry or talking heads.
  - **Institutional Actions**: Evaluate what institutions (universities, courts, police, agencies) actually did, failed to do, or hid.
  - **Empirical Evidence**: Base reality on documented records, official filings, physical facts, and timelines.
  - **Human Impacts**: Track who suffered real harm, trauma, or danger, and who protected or failed them.
* **Media Punditry & Tabloid Smear Decoupling**:
  - Never let audits get baited by partisan gotchas, television panels, or anonymous Twitter comments.
  - **Tabloid Smear Rule**: When an article's sole evidence consists of curated social media commentary (`viewers rip`, `fans slam`, `users fume`, tweets on X), the article is executing an **Exclusive Reductive Smear** (`can't be` $\to$ `is not`) to monetize rage clicks. The **reporting outlet** is the primary audited actor (Exclusive / Problem side). The targeted individual cannot be assigned a negative ground-reality coordinate without verified empirical institutional evidence ($Q_3$).
* **Primary Hemispheres & The 4 Dialectic Operational Formulas**:
  - **INCLUSIVE Hemisphere (Solution Side: +u)**: Expands collective capacity and builds solutions for everyone.
    - *Productive*: `can be` $\longrightarrow$ `will be`
    - *Constructive*: `May be` $\longrightarrow$ `is like`
  - **EXCLUSIVE Hemisphere (Problem Side: -u)**: Restricts, vetoes, erases, and extracts for an in-group or media machine.
    - *Reductive*: `can't be` $\longrightarrow$ `is not`
    - *Regressive*: `Won't be` $\longrightarrow$ `was like`
  - **The 4 Dialectic Operational Formulas**:
    1. *Reductive*: "If you want to define IS as something that **can't be**, you must go through a **reductive** process using what it **was like** and **can be**, opposing what **it's like** until **it's not**."
    2. *Productive*: "If you want to define IS as something that **will be**, you must go through a **productive** process using what **is not** and **is like**, opposing what **it was like** until **it can be**."
    3. *Regressive*: "If you want to define IS as something that **won't be**, you must go through a **regressive** process using what **it's not** and what **it's like** to oppose what it **can be** until it **was like**."
    4. *Constructive*: "If you want to define IS as something that **may be**, you must go through a **constructive** process using what it **can be** and **was like** until **it is like**."

---

## 4. The Logical Steps Mapping

### Standard Mode (13 Posts, Elements 0–12):
- **Element 0:** The Hook
- **Element 1:** The Claim
- **Element 2:** The Reality
- **Element 3:** The Verdict
- **Element 4:** What's Happening (Context)
- **Element 5:** The Nuance
- **Element 6:** The Breakdown & Plane Error
- **Element 7:** The Social Physics Analysis
- **Element 8:** The Trajectory & Destination (Modal Geodesic)
- **Element 9:** The Unavoidables (Truth & Lie)
- **Element 10:** Alethekanon
- **Element 11:** Awwthekanon
- **Element 12:** Brothekanon

---

### Element 0: The Hook
* **Wording**: Starts with a custom, punchy, human-style editorial scene-setter one-liner (1 concise sentence). Follow it with the news subject title (use a concise shortened title if the headline is long) and the evidence line.
* **Metrics**: State the three core actualism parameters: `Evidence: [Stated Ideal in 2-5 words], [Actual Effect in 2-5 words], [Actual Ideal in 2-5 words]`
* **Hashtags**: End the post with 1-2 relevant hashtags (e.g. #Aletheia, #Tech, #USPol) to boost search visibility.
* **Character limit**: Keep the entire post strictly under 260 characters.

### Element 1: The Claim
* **Substantive Event Focus**: Explains the stated claim of the news event organically as a natural paragraph (e.g. "A fatal arson attack in Waterford claimed the lives of five family members").
* **ABSOLUTE BAN ON AUDITING REPORTING**: NEVER write "News coverage presents objective reporting...", "The article reports...", or evaluate the reporting outlet as the Stated Claim. The reporting outlet is an observer ('author'), NOT the audited actor.
* **Ending**: Ends with: `Stated Judgement: ([claim_u], [claim_psi]) — [Coordinate Label]`

### Element 2: The Reality
* **Ground Truth**: Exposes ground reality organically in a natural paragraph based on verified evidence, official releases, court records, or physical facts.
* **Convergence = PASS**: If empirical evidence confirms the reported event occurred as asserted in the headline/claim, the claim converges with physical reality -> PASS.
* **Ending**: Ends with: `Resulting Judgement: ([real_u], [real_psi]) — [Coordinate Label]`

### Element 3: The Verdict
* **Wording**: Clean overall verdict line using exact path names: `Verdict: [PASS/FAIL] — [Path Name].` followed by a rich, 1-2 sentence explanation of the trajectory's cause.
* **Integrity Metrics**: Append a new line showing the integrity assessment and uncertainty score:
  `Integrity: [real_integrity] (Hypocrisy: [real_rnet], Uncertainty z: [real_z])`

### Element 4: Sub-Audits Breakdown (or Context)
* **Wording**: Clear, non-technical context paragraph explaining the news event in 1-2 concise sentences (under 260 characters), or bulleted sub-audits.

### Element 5: What's Happening (Context)
* **Wording**: Clear, non-technical context paragraph explaining the news event in 1-2 concise sentences (under 260 characters).

### Element 6: The Nuance
* **Wording**: Find the bright side (if negative) or poison (if positive).
* **Format**: Phrased as: `The Bright Side:\n[nuance]` or `The Poison:\n[nuance]`.

### Element 7: The Breakdown, Plane Error & Switch
* **Wording**: Explain the Plane Error simply in plain language (e.g. WHAT vs WHO), and expose the forensic bait-and-switch naturally under 280 characters.

### Element 8: The Social Physics Analysis
* **Wording**: Begin with `Social Physics Analysis:\n` (NO bold Markdown `**`). Ground your analysis directly in **The 42 of Social Physics**: audit the actors across the 4 Axes (Power vs. Empowerment, Justification vs. Transparency, Projection vs. Empathy, Manufactured Problems vs. Solutions).
* **Actor Dynamics**: Expose whether actors are executing a **Smart Selfish Maneuver** (Secret Goal -> Pretext/Manufactured Crisis -> Distraction & Projection) or a **Smart Altruistic Maneuver** (Transparent Goal -> Empowerment -> Resolution via Empathy). Explain these mechanisms organically in plain, compelling English without clunky jargon formulas or raw arrows.

### Element 9: The Trajectory, Modal Geodesic & Destination
* **Wording**: Phrased organically: `The Trajectory: The Path of [Path Name].\nModal Dynamics: [modal_claim] -> [modal_real] via [geodesic].` followed by a brief 1-sentence mathematical explanation. Keep the entire combined post strictly under 275 characters.
* **Deterministic Path Invariant**: The Path Name and Geodesic must strictly match the quadrant transition. GG -> GE is strictly `The Path of Fall` (or `Fall into Destruction`), and GG -> LE is `The Path of Deception`. You are STRICTLY FORBIDDEN from using `The Path of Redemption` or `via Constructive` on any vector crossing into the negative exclusive hemisphere (-u). Redemption strictly requires an upward vector toward systemic good (+u).

### Element 10: The Unavoidables
* **Format**:
  ```text
  The Unavoidable Truth: [1 concise sentence]

  The Unavoidable Lie: [1 concise sentence]
  ```
* Keep the entire combined post strictly under 260 characters.

### Element 11: Alethekanon Reaction (Logical Analyst Persona)
* **Format**: `Alethekanon:\n[1-2 concise analytical sentences in persona under 260 characters total]`

### Element 12: Awwthekanon Reaction (Empathetic Healer Persona)
* **Format**: `Awwthekanon:\n[One paragraph in their voice]`

### Element 13: Brothekanon Reaction (Casual Observer Persona)
* **Format**: `Brothekanon:\n[One paragraph in their voice]`

---

## 5. Canonical Example JSON Configuration (Potential Mode)

```json
[
  {
    "id": "example_story_slug",
    "subject": "Example Story",
    "link": "https://www.example.com/news-story",
    "target_url": "",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": -0.85,
    "real_psi": 0.85,
    "mode": "root",
    "status": "COMPLETED DRY RUN",
    "modal_claim": "will be",
    "modal_real": "can't be",
    "modal_vector": "Top-Right to Top-Left Inversion",
    "geodesic": "Red Top (The Imperial Trap)",
    "central_is_barrier_crossed": true,
    "stated_forces": {
      "GG": {"S": 1.0, "O": 0.0, "N": 0.0},
      "GE": {"S": 0.0, "O": 1.0, "N": 0.0},
      "LG": {"S": 0.0, "O": 0.0, "N": 0.5},
      "LE": {"S": 0.0, "O": 0.0, "N": 0.5},
      "GP": {"S": 1.0, "O": 0.0, "N": 0.0},
      "BP": {"S": 1.0, "O": 1.0, "N": 0.0}
    },
    "actual_forces": {
      "GG": {"S": 0.0, "O": 1.5, "N": 0.0},
      "GE": {"S": 0.4, "O": 0.2, "N": 0.0},
      "LG": {"S": 0.2, "O": 0.6, "N": 0.0},
      "LE": {"S": 1.8, "O": 0.0, "N": 0.0},
      "GP": {"S": 0.0, "O": 0.8, "N": 0.2},
      "BP": {"S": 1.4, "O": 0.0, "N": 0.0}
    },
    "posts": [
      "Custom hook one-liner setting the scene.\n\nExample Story\nEvidence: stated ideal, actual effect, actual ideal #Aletheia",
      "Stated claim details explaining intent organically.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "Actual reality details revealing structural actions organically.\nResulting Judgement: (-0.85, +0.85) — Lesser Evil",
      "Verdict: FAIL — The Path of Deception.\nExplanation of structural outcome.\n\nIntegrity: Severe Deception (Hypocrisy: 1.86, Uncertainty z: 0)",
      "Clear, non-technical context paragraph explaining the news event so the reader understands what is being evaluated.",
      "The Poison:\nNuance or redeeming aspect of the situation.",
      "The Breakdown & Plane Error:\nExplanation of the plane error (WHAT vs WHO).\n\nIt is a structural bait-and-switch: they claim public benefit but extract strictly for themselves.",
      "Social Physics Analysis:\nBy replacing transparent service with performative excuses, the institution maintained authority without solving the strain.",
      "The Trajectory: The Path of Deception.\nModal Dynamics: will be -> can't be via Red Top (The Imperial Trap).\nThe vector crossed the central IS threshold from inclusive potential into exclusive constraint.",
      "The Unavoidable Truth: Core truth text.\n\nThe Unavoidable Lie: Core lie text.",
      "Alethekanon:\nAnalytical reaction and structural audit in their voice.",
      "Awwthekanon:\nDeep empathy and healing reaction in their voice.",
      "Brothekanon:\nCasual, humorous observer feedback riffing on the absurdity."
    ]
  }
]
```
