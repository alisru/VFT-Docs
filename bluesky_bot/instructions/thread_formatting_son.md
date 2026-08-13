# Thread Formatting Protocol & JSON Schema (SON Edition)

This document defines the strict output schema and logical steps sequence for Aletheia Bot fact-checks under the 6-Attractor SON convergence model.

---

## 1. The 29-Key Conversational JSON Schema & Blueprint (Macro-Enabled)

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

*Note: DO NOT include `subject_slug`, `verdict`, `graph_img`, or any other custom keys in the JSON config. These are handled dynamically by the registry builder.*

---

## 2. Attractor Forces Schema

The `"stated_forces"` and `"actual_forces"` keys must map to dictionaries containing scores for all 6 attractors (`GG`, `GE`, `LG`, `LE`, `GP`, `BP`). For each attractor, you must provide the Support (`S`), Oppose (`O`), and Neutral (`N`) forces as decimals between `0.0` and `2.0`.

Format:
```json
"stated_forces": {
  "GG": {"S": 1.0, "O": 0.0, "N": 0.0},
  "GE": {"S": 0.0, "O": 1.0, "N": 0.0},
  "LG": {"S": 0.0, "O": 0.0, "N": 0.5},
  "LE": {"S": 0.0, "O": 0.0, "N": 0.5},
  "GP": {"S": 1.0, "O": 0.0, "N": 0.0},
  "BP": {"S": 1.0, "O": 1.0, "N": 0.0}
}
```

---

## 3. Conversational Formatting Rules (No Robotic Prefixes)

* **BAN on Robotic Titles**: Do not start steps with dry prefixes like `Subject:`, `The Claim:`, `The Reality:`, or `What's happening:`. (Headers explicitly outlined in the 13 steps below are permitted).
* **Natural Human Flow**: Write in clean, conversational Plain English. Use headers only when they are clean and natural (e.g. `The Bright Side:`, `The Poison:`).
* **Character Caps**: Keep every single step strictly under **275 characters** in the JSON config to prevent dynamic text-splitting errors.
* **NO Orphan Words**: DO NOT split sentences arbitrarily or waste array elements. If a sentence fits in the current post, include it. Do NOT make a single post containing just 1 or 2 words (like 'dysfunction.'). Write continuously and naturally, only hard-splitting concepts when approaching the 275-character limit.

---

## 4. The 13 Logical Steps Mapping

To maintain the strict 13-element limit on disk, the bot must output the `"posts"` array mapped exactly as follows:

### Element 0: The Hook
* **Wording**: Starts with a custom, punchy, human-style editorial scene-setter one-liner (e.g., exposing a structural framing or irony). Follow it with the clean news subject title (no "Subject:" prefix) and the evidence standards line.
* **Metrics**: State the three core actualism parameters: `Evidence: [Stated Ideal in 2-5 words], [Actual Effect in 2-5 words], [Actual Ideal in 2-5 words]`
* **Hashtags**: End the post with 1-2 relevant hashtags (e.g. #Aletheia, #Tech, #USPol) to boost search visibility.
* **Character limit**: Keep the entire post strictly under 275 characters.

### Element 1: The Claim
* **Wording**: Explains the stated claim organically as a natural paragraph.
* **Ending**: Ends with: `Stated Judgement: ([claim_u], [claim_psi]) — [Coordinate Label]`

### Element 2: The Reality
* **Wording**: Exposes ground reality organically in a natural paragraph.
* **Ending**: Ends with: `Resulting Judgement: ([real_u], [real_psi]) — [Coordinate Label]`

### Element 3: The Verdict
* **Wording**: Clean overall verdict line using exact path names: `Verdict: [PASS/FAIL] — [Path Name].` followed by a rich, 1-2 sentence explanation of the trajectory's cause.
* **Integrity Metrics**: Append a new line showing the integrity assessment and uncertainty score:
  `Integrity: [real_integrity] (Hypocrisy: [real_rnet], Uncertainty z: [real_z])`
* **IMPORTANT (Multi-Aspect Mode)**: Do NOT include any compact `Subs:` summary in this post. Sub-audit and aspect verdicts belong exclusively in the dedicated Sub-Audits Breakdown step (Element 4 in multi-aspect mode).

### Element 4 (Multi-Aspect Mode Only): Sub-Audits Breakdown
* **Present only when in multi-aspect mode.** This is the dedicated step for aspect/actor-level verdicts.
* **Wording**: List each evaluated sub-aspect or actor with its full name, PASS/FAIL/COND outcome, coordinates, and at least a 1-sentence explanation:
  ```
  Sub-Audits Breakdown:
  - [Aspect A Full Name]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Detailed reasoning].
  - [Aspect B Full Name]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Detailed reasoning].
  ```
* This is the ONLY place aspect verdicts appear. Do not repeat them in the Verdict post.

### Element 4 (Standard) / Element 5 (Multi-Aspect): What's Happening (Context)
* **Wording**: Clear, non-technical context paragraph explaining the news event so the reader understands what is being evaluated.

### Element 5: The Nuance
* **Wording**: Find the bright side (if negative) or poison (if positive).
* **Format**: Phrased as: `The Bright Side:\n[nuance]` or `The Poison:\n[nuance]`.

### Element 6: The Breakdown, Plane Error & Switch
* **Wording**: Explain the Plane Error simply in plain language (e.g. WHAT vs WHO), and expose the forensic bait-and-switch naturally under 280 characters.

### Element 7: The Social Physics Analysis
* **Wording**: Begin with `Social Physics Analysis:\n` (NO bold Markdown `**`). Provide a clear, direct, conversational plain-English explanation of the social physics dynamics (e.g. selfishness, power, pretext/justification, projection).
* **Jargon Ban**: You are STRICTLY forbidden from using raw technical jargon labels (such as "Smart Altruistic Loop", "Smart Selfish Loop") or nesting processes using arrow characters (e.g., "A → B → C"). Instead, explain these principles (empowerment, transparency, empathy, or pretexts and projection) as natural, narrative human dynamics.

### Element 8: The Trajectory & Destination
* **Wording**: Phrased organically: `The Trajectory: The Path of [Path Name].\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward [Outcome/Terminal Zone]` followed by a brief 1-sentence mathematical explanation. Keep the entire combined post strictly under 275 characters.

### Element 9: The Unavoidables
* **Format**:
  > The Unavoidable Truth: [truth text]
  > 
  > The Unavoidable Lie: [lie text]

### Element 10: Alethekanon Reaction (Logical Analyst Persona)
* **Format**: `Alethekanon:\n[One paragraph in their voice]`

### Element 11: Awwthekanon Reaction (Empathetic Healer Persona)
* **Format**: `Awwthekanon:\n[One paragraph in their voice]`

### Element 12: Brothekanon Reaction (Casual Observer Persona)
* **Format**: `Brothekanon:\n[One paragraph in their voice]`

---

## 5. Canonical Example JSON Configuration

```json
[
  {
    "id": "example_story_slug",
    "subject": "Example Story",
    "link": "https://www.example.com/news-story",
    "target_url": "",
    "claim_u": 1.0,
    "claim_psi": 0.0,
    "real_u": -1.0,
    "real_psi": -1.0,
    "mode": "root",
    "status": "COMPLETED DRY RUN",
    "macro_event": "Example Macro Event",
    "macro_claim_u": 1.0,
    "macro_claim_psi": 1.0,
    "macro_real_u": -1.0,
    "macro_real_psi": -1.0,
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
      "GE": {"S": 1.0, "O": 0.0, "N": 0.0},
      "LG": {"S": 0.0, "O": 0.5, "N": 0.0},
      "LE": {"S": 1.5, "O": 0.0, "N": 0.0},
      "GP": {"S": 0.0, "O": 1.0, "N": 0.0},
      "BP": {"S": 1.0, "O": 0.0, "N": 0.0}
    },
    "posts": [
      "Custom hook one-liner setting the scene.\n\nExample Story\nEvidence: stated ideal, actual effect, actual ideal",
      "Stated claim details explaining intent organically.\nStated Judgement: (+1.0, 0.0) — Good Preference",
      "Actual reality details revealing structural actions organically.\nResulting Judgement: (-1.0, -1.0) — Greater Evil",
      "Verdict: FAIL — The Path of Deception.\nExplanation of structural outcome.\n\nIntegrity: Severe Deception (Hypocrisy: 12.5, Uncertainty z: 4)",
      "Clear, non-technical context paragraph explaining the news event so the reader understands what is being evaluated.",
      "The Bright Side:\nNuance or redeeming aspect of the situation.",
      "The Breakdown & Plane Error:\nExplanation of the plane error (WHAT vs WHO).\n\nIt is a structural bait-and-switch: they claim public benefit but extract strictly for themselves.",
      "Social Physics Analysis:\nBy replacing unilateral authority with shared creative ownership, the production minimized systemic friction. Rather than using actors as tools for a rigid goal, the transparent environment empowered them to contribute their own perspectives.",
      "The Trajectory: The Path of Deception.\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward Greater Evil. Explanatory mathematical sentence.",
      "The Unavoidable Truth: Core truth text.\n\nThe Unavoidable Lie: Core lie text.",
      "Alethekanon:\nAnalytical reaction and structural audit in their voice.",
      "Awwthekanon:\nDeep empathy and healing reaction in their voice.",
      "Brothekanon:\nCasual, humorous observer feedback riffing on the absurdity."
    ]
  }
]
```
