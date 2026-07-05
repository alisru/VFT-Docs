---
name: kanon-build
description: Build a 343 National Kanon -- the complete 7x7x7 semantic map of a nation's soul using the Qqci framework. Use this skill whenever the user asks to build a Kanon, generate a national analysis, create a 343 analysis, map a nation's identity, populate Kanon JSON files, add vectors to a Kanon, or research and draft compact JSON entries for any nation. Also trigger when the user asks to add First Nations perspective shadow entries, validate Kanon completeness, or continue building an in-progress Kanon.
---

# Kanon Build Workflow

Builds a 343 National Kanon -- a complete 7x7x7 semantic map of a nation's identity across 7 planes, 7 senses, and 7 vectors. Output is compact JSON files, one per plane.

## Architecture

343 vectors = 7 Planes x 7 Senses x 7 Items.

Each address is Plane.Sense.Vector e.g. Who.Where.Why.

Plane roles:
- Plane 1 WHO -- Identity (The Driver)
- Plane 2 WHAT -- Definition (+x Lateral)
- Plane 3 WHERE -- Land (-x Lateral)
- Plane 4 WHY -- Drive (+y Longitudinal)
- Plane 5 HOW -- Method (-y Longitudinal)
- Plane 6 CAUSE -- Foundation (+z Vertical)
- Plane 7 EFFECT -- Result (-z Vertical)

Deriving a vector: triangulate the three coordinates.
Example Who.Where.Why = What is the Motivation (Why) derived from the Land (Where) that shapes the Identity (Who)?
Answer for Australia: "Populate or Perish"

## Output Format -- Compact JSON Schema

Each plane is a JSON array. Each entry:

{
  "address": "Who.Where.Why",
  "plane": 1,
  "plane_name": "Identity",
  "name": "Populate or Perish",
  "canonical_quote": "The quote text.",
  "attribution": "Speaker/Author",
  "source": "Document Source, Year",
  "description": "3-5 sentences of context. Min 4-5 sentences.",
  "justification": "3-5 sentences justifying HIT or FAIL against the coordinates. Min 4-5 sentences.",
  "actuality": "3-5 sentences about actual output over time. Actively search for the most recent verified quote or documented action relevant to this vector -- do not reuse the canonical_quote. End with TENTATIVE FAIL if actuality contradicts stated score. Min 4-5 sentences.",
  "coordinates": { "v": -0.2, "psi": 0.6 },
  "zone": "Greatest Lie",
  "judgment_rationale": "Short explanation of coordinate scoring."
}

Body section minimums: description, justification, and actuality each 4-5 sentences minimum. Meet the minimum with substantive content only -- no padding.

## Coordinate System (upsilon, psi)

Axis upsilon (Morality -- who benefits):
+2.0 Everyone / All Beings (Systemic Justice)
+1.0 Other People (Greater Good)
 0.0 Neutral
-1.0 My Group Only (Lesser Evil)
-2.0 Only Me (Tyranny / Pure Extraction)

Axis psi (Will -- what the energy is doing):
+2.0 Actively creating systemic value for all (Productive Justice)
+1.0 Proactive (creating, building, acting)
 0.0 Neutral (stasis)
-1.0 Passive (allowing, suppressing, withholding)
-2.0 Actively destroying or extracting value (Chaos / Collapse)

WHERE modifies upsilon: energy injected into a structurally corrupt domain pulls upsilon negative regardless of intent.
HOW modifies psi: coercive or deceptive method forces psi negative regardless of stated purpose.

Zone classifications:
- Greater Good: (+upsilon, +psi)
- Greatest Lie: (-upsilon, +psi)
- Lesser Good: (+upsilon, -psi)
- Greater Evil: (-upsilon, -psi)
- Tension Point: mixed or contested
- Constraint: neutral / environmental fact

## Content Selection Priority

1. Founders / Originators of the concept (highest authority)
2. Deeply iconic national quotes -- embedded in national consciousness
3. High emotional voltage: pride, shame, tears, chills
4. Historical quotes with documented sourcing
5. Last resort: documentary / administrative facts only if no soul quote exists

Evidence-based only. Every vector must be anchored by a real quote, law, date, or event. No paraphrasing. No inference. No direct quote = vector left unaudited.

## Use Training Data as a Hypothesis Generator, Never as a Citation

For founders, iconic figures, and well-documented national events (the highest-priority sources in the list above), training data usually already contains the real quote or a strong lead to it. Don't skip straight to a blind search on the vector's abstract meaning ("[Item] of [Sense] of [Plane]") and settle for whatever a generic search returns.

The correct sequence:
1. Generate the hypothesis from training knowledge: given the vector's actual mechanism, what specific real speech, document, law, or event is this nation known for that matches it? Name the specific candidate (who said it, roughly when, in what document) as a hypothesis, not as a fact.
2. Verify the hypothesis with a direct fetch or targeted search built around the specific names and likely exact wording the hypothesis suggests, not the vector's poetic Kanon name. Only once a live, checkable source confirms the specific wording does it go into the JSON as the canonical_quote.

Training data can hallucinate exact wording, dates, and attribution even when it correctly identifies the right event or speech. The hypothesis step is what makes research fast and targeted, the verification step is what keeps it evidence-based. Never let the first step substitute for the second.

## First Nations Perspective Shadowing

For settler-colonial nations: where a mainstream concept has an indigenous shadow, add a second entry at the same address.
- Same address field as the primary entry
- Name includes [First Nations Perspective] e.g. Anteriority [First Nations Perspective]
- Separate quote, separate coordinates, separate judgment
- The shadow entry exposes what the mainstream entry erases

## Australian Kanon Reference

The 7 Aus Kanon compact JSON files are in references/. Read the relevant file when building or extending the Australian Kanon. These are ground truth for existing vector names, addresses, canonical quotes, coordinates, and First Nations shadow pairs.

Files: Plane_1_Identity_compact.json through Plane_7_Result_compact.json

## For Other Nations

Follow the same schema. Path convention:
[nation-root]/Kanon/compact JSON/Plane_[N]_[Name]_compact.json

## Build Process

1. Identify the plane and sense being built
2. Derive the vector meaning: [Item] of [Sense] of [Plane]
3. Research: find the best available quote/evidence using content selection priority. Before searching cold, use training data as a hypothesis generator, see below, then verify whatever it surfaces with a live fetch or targeted search before it goes in the JSON.
4. Write the compact JSON entry -- all fields populated
5. Verify quote meets evidence-based standards -- directly sourced only
6. Verify body sections each meet 4-5 sentence minimum
7. Verify coordinates follow the system including modifier rules
8. If a First Nations shadow applies, add shadow entry at same address
9. Validate completeness: 49 primary entries per plane plus shadow entries

## Validation

Before finalising any plane:
- Exactly 49 primary coordinates present
- Each shadow entry has a unique name and distinct quote/coordinates from its primary
- No establishes field (deprecated)
- All body sections min 4-5 sentences
- Coordinates within [-2.0, 2.0] on both axes
- All quotes directly sourced and attributable
