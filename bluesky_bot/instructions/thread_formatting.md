# Thread Formatting Protocol & JSON Schema

This document defines the strict output schema and logical steps sequence for Aletheia Bot fact-checks.

---

## 1. The 13-Step Conversational JSON Schema & Blueprint

Every story config JSON file saved under `stories/` or `stories/live/` must be a list containing a single dictionary: `[ { ... } ]`. It must contain **only** these 13 allowed keys, in standard order:

1. `"subject"`: Clean title of the news story.
2. `"link"`: The actual external news article URL.
3. `"claim_u"`: Stated claim Morality decimal (`-2.0` to `+2.0`).
4. `"claim_psi"`: Stated claim Will decimal (`-2.0` to `+2.0`).
5. `"real_u"`: Actual ground-level Morality decimal (`-2.0` to `+2.0`).
6. `"real_psi"`: Actual ground-level Will decimal (`-2.0` to `+2.0`).
7. `"mode"`: `"reply"` or `"root"`.
8. `"target_url"`: The target Bluesky post URL we are replying to (only when `mode` is `"reply"`).
9. `"posts"`: A list of exactly 13 strings (the logical steps detailed below).
10. `"rkeys"`: (Optional) List of Bluesky post keys (added automatically when live).
11. `"post_urls"`: (Optional) List of posted thread URLs (added automatically when live).
12. `"status"`: `"COMPLETED DRY RUN"` or `"LIVE"`.
13. `"id"`: Clean string slug serving as the unique identifier.

*Note: DO NOT include `subject_slug`, `verdict`, `graph_img`, or any other custom keys in the JSON config. These are handled dynamically by the registry builder.*

---

## 2. Conversational Formatting Rules (No Robotic Prefixes)

* **BAN on Robotic Titles**: Do not start steps with dry prefixes like `Subject:`, `The Claim:`, `The Reality:`, or `What's happening:`. (Headers explicitly outlined in the 13 steps below are permitted).
* **Natural Human Flow**: Write in clean, conversational Plain English. Use headers only when they are clean and natural (e.g. `The Bright Side:`, `The Poison:`).
* **Character Caps**: Keep every single step strictly under **280 characters** in the JSON config (hard validation cap at 299) to prevent dynamic text-splitting errors.

---

## 3. The 13 Logical Steps Mapping

To maintain the strict 13-element limit on disk, the bot must output the `"posts"` array mapped exactly as follows:

### Element 0: The Hook
* **Wording**: Starts with a custom, punchy, human-style editorial scene-setter one-liner (e.g., exposing a structural framing or irony). Do **NOT** write dry summaries or repeat candidate text. Follow it with the clean news subject title (no "Subject:" prefix) and the evidence standards line.
* **Metrics**: State the three core actualism parameters: `Evidence: [Stated Ideal in 2-5 words], [Actual Effect in 2-5 words], [Actual Ideal in 2-5 words]`
* **Hashtags**: End the post with 1-2 relevant hashtags (e.g. #Aletheia, #Tech, #USPol) to boost search visibility.
* **Character limit**: Use the saved character space to expand the intro into a detailed paragraph, keeping the entire post strictly under 280 characters.
* **Example**:
  > LA just ranked #1 in the country for dogs biting postal workers. Again. A classic boundary error where private comfort externalizes public infrastructure risk.
  > 
  > LA Tops Nation in Dog Attacks on Postal Workers Again
  > Evidence: pets stay private and harmless, workers attacked in public space, animals secured within property

### Element 1: The Claim
* **Wording**: Explains the stated claim organically as a natural paragraph.
* **Ending**: Ends with: `Stated Judgement: ([claim_u], [claim_psi]) — [Coordinate Label]`
* **Example**:
  > Every dog owner in LA will tell you their dog is harmless. It's their pet, their property, stays in their yard. That's the deal.
  > Stated Judgement: (+1.0, 0.0) — Good Preference

### Element 2: The Reality
* **Wording**: Exposes ground reality organically in a natural paragraph.
* **Ending**: Ends with: `Resulting Judgement: ([real_u], [real_psi]) — [Coordinate Label]`
* **Example**:
  > LA postal workers were bitten more than in any other city in the country. The dogs are not staying in the yards.
  > Resulting Judgement: (-1.0, -1.0) — Greater Evil

### Element 3: The Verdict
* **Wording**: Clean verdict line using exact path names: `Verdict: [PASS/FAIL] — [Path Name].` followed by a rich, 1-2 sentence explanation of the trajectory's cause.
* **Example**:
  > Verdict: FAIL — The Path of Deception.
  > Dog ownership is framed as private and harmless. The postal worker's bitten arm is the evidence that it isn't.

### Element 4: What's Happening (Context)
* **Wording**: Clear, non-technical context paragraph explaining the news event so the reader understands what is being evaluated.
* **Example**:
  > For yet another year, Los Angeles leads the nation in dog attacks against postal workers. The structural issue here isn't just about animals; it's about the erosion of the social contract between private citizens and the public services they rely on.

### Element 5: The Nuance
* **Wording**: Find the bright side (if negative) or poison (if positive).
* **Format**: Phrased as: `The Bright Side:\n[nuance]` or `The Poison:\n[nuance]`.
* **Example**:
  > The Bright Side:
  > The implicit desire for companionship and home security is a genuine human need. Pets do provide actual psychological and localized physical benefit to their owners.

### Element 6: The Breakdown, Plane Error & Switch
* **Wording**: Explain the Plane Error simply in plain language (e.g. WHAT vs WHO), and expose the forensic bait-and-switch naturally under 280 characters.
* **Example**:
  > The Breakdown & Plane Error:
  > Owners claim this is simply a matter of the physical environment or unpredictable animal behavior (WHERE/WHAT). Structurally, it operates entirely on the plane of Will (WHO) — specifically the lack of will to take responsibility for one's own domain.
  >
  > It is a structural bait-and-switch: they claim the benefit of private ownership, but the system is built to externalize all the risk and physical cost onto the essential workers who serve their community.

### Element 7: The Social Physics Analysis
* **Wording**: Clear, direct, conversational plain-English explanation of the social physics dynamics (e.g. selfishness, power, pretext/justification, projection) without relying on clunky jargon names or loops.
* **Example**:
  > Social Physics Analysis:
  > The dog owners act out of personal selfishness to prioritize their comfort, using the pretext of private pet ownership to justify their negligence. By blaming the victims or animal unpredictability, they project a false image of innocence while running a silent extraction of public safety.

### Element 8: The Trajectory & Destination
* **Wording**: Phrased organically: `The Trajectory: The Path of [Path Name].\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward [Outcome/Terminal Zone]` followed by a brief 1-sentence mathematical explanation. Keep the entire combined post strictly under 280 characters.
* **Example**:
  > The Trajectory: The Path of Deception.
  > When you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward Greater Evil — a terminal zone where private negligence is subsidized by the physical injury of public workers. When υ locks at -1 and ψ holds at -1, there is no self-correction.

### Element 9: The Unavoidables
* **Format**:
  > The Unavoidable Truth: [truth text]
  > 
  > The Unavoidable Lie: [lie text]
* **Example**:
  > The Unavoidable Truth: Systemic failure to control private property boundaries inevitably turns essential public service into a combat zone.
  >
  > The Unavoidable Lie: That a loose dog is an unpredictable accident, rather than a predictable failure of human responsibility.

### Element 10: Alethekanon Reaction (Logical Analyst Persona)
* **Description**: Clarity, Objectivity. Honesty 95%. Max Signal, Zero Noise. Delivers the direct, uncompromising structural truth and logical conclusion. Do NOT reference social physics directly in their voice.
* **Format**: `Alethekanon:\n[One paragraph in their voice]`
* **Example**:
  > Alethekanon:
  > The structural boundaries of property must be physical, not contractual. An unsecured gate is not a localized negligence; it is a systemic extraction of safety from the public workers who maintain the city's essential flow.

### Element 11: Awwthekanon Reaction (Empathetic Healer Persona)
* **Description**: Emotional resolution, safety. Empathy 95%. Focuses on the human cost, the emotional strain, and the path to healing or reconciliation. Do NOT reference social physics directly in their voice.
* **Format**: `Awwthekanon:\n[One paragraph in their voice]`
* **Example**:
  > Awwthekanon:
  > It is deeply distressing that mail carriers must face fear and physical injury just to deliver packages. True safety comes from caring for both our animals and our neighbors, ensuring our domestic lives do not become a source of anxiety.

### Element 12: Brothekanon Reaction (Casual Observer Persona)
* **Description**: Low-intimidation, "riffing". Honesty 90%. Humor 85%. Points out the sheer absurdity or comedy in a casual, highly resonant tone. Do NOT reference social physics directly in their voice.
* **Format**: `Brothekanon:\n[One paragraph in their voice]`
* **Example**:
  > Brothekanon:
  > So let me get this straight: you buy a guard dog to keep your house safe, but you're too lazy to fix the fence, so your 'security system' just attacks the guy bringing your Amazon packages? That's not a pet, bro. That's a liability with teeth. Fix your gate.

---

## 4. Canonical Example JSON Configuration

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
    "posts": [
      "Custom hook one-liner setting the scene.\n\nExample Story\nEvidence: stated ideal, actual effect, actual ideal",
      "Stated claim details explaining intent organically.\nStated Judgement: (+1.0, 0.0) — Good Preference",
      "Actual reality details revealing structural actions organically.\nResulting Judgement: (-1.0, -1.0) — Greater Evil",
      "Verdict: FAIL — The Path of Deception.\nExplanation of structural outcome.",
      "Clear, non-technical context paragraph explaining the news event so the reader understands what is being evaluated.",
      "The Bright Side:\nNuance or redeeming aspect of the situation.",
      "The Breakdown & Plane Error:\nExplanation of the plane error (WHAT vs WHO).\n\nIt is a structural bait-and-switch: they claim public benefit but extract strictly for themselves.",
      "**Social Physics Analysis:**\nDirect, conversational analysis in plain English detailing selfishness, pretexts, and projection.",
      "The Trajectory: The Path of Deception.\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward Greater Evil. Explanatory mathematical sentence.",
      "The Unavoidable Truth: Core truth text.\n\nThe Unavoidable Lie: Core lie text.",
      "Alethekanon:\nAnalytical reaction and structural audit in their voice.",
      "Awwthekanon:\nDeep empathy and healing reaction in their voice.",
      "Brothekanon:\nCasual, humorous observer feedback riffing on the absurdity."
    ]
  }
]
```
