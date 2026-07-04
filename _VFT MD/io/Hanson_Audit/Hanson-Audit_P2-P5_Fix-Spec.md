# Hegemonic Audit -- Pauline Hanson -- P2-P5 Fix Specification

**File:** `Hegemonic-Audit_Pauline Hanson_fixed.md`
**Scope:** Planes 2, 3, 4, 5 only. P1, P6, P7 already complete.
---

## Ground Rules (non-negotiable)

1. NEVER fabricate quotes. Never present unverified text as objective fact. This applies to every single node, no exceptions.
2. VALIDATE every quote before keeping it. If a quote cannot be verified against the source corpus below, replace it.
3. Quote priority order: real verified Hanson quote > closely documented paraphrase of a real position > description of documented action. No invented or composite quotes under any circumstances.
4. Body text (Description, Justification, Actuality) is NOT rewritten unless a quote replacement (not a format-only change) causes a clear topic mismatch with the Justification section. In that case: minimum edit to Justification only, document exactly what changed and why.
5. When updating any node: report to user in chat -- address, what changed, before/after. Nothing goes in the doc except the fix itself.
6. For dual-address (FN perspective) nodes: anchor ALL replacements to the body Description line text. NEVER use address pattern alone -- it will corrupt the other node at the same address.
7. Never delete nodes.
8. Never rename a node unless the Kanon JSON confirms the name is wrong.
9. All coord values come from Kanon JSON only, never from judgment.
10. After any name fix on a dual-address node: immediately verify coords also match Kanon. Name corruption and coord inheritance are always paired bugs.

---

## Node Header Format (canonical)

```
**(Address) Vector Name (υ: +X.X, ψ: +Y.Y): HIT/FAIL.** **Quote:** "quote text" -Source Context (year)
```

- Coords use `\+` or `\-` escaped in markdown
- Quote is on the SAME line as the header, no line break between
- Source context must be meaningful (e.g. "Maiden Speech, House of Representatives, Hansard" not just "Speech")
- No double-quote wrapping: NOT `""quote." (year)."` -- that is the OLD broken format

---

## Verified Source Abbreviations

| Code | Full Source |
|------|-------------|
| MS96 | Maiden Speech, House of Representatives, Hansard, 10 September 1996 |
| MS16 | Senate Maiden Speech, Hansard, 14 September 2016 |
| WTC22 | Senate interjection during Acknowledgement of Country, Hansard, 27 July 2022 |
| ENR04 | Enough Rope, ABC Television, 20 September 2004 |
| SON18a | Senate speech "Protect Our Australian Way of Life", Hansard, 19 September 2018 |
| SON18b | Senate speech "Immigration Debate Cannot Be Silenced", Hansard, 22 August 2018 |
| CTX18 | Senate speech on corporate tax cuts, Hansard, 22 August 2018 |
| JMF20 | Senate speech on JobMaker, Hansard, 10 November 2020 |
| TODAY19 | Today Show, Nine Network, 14 July 2019 |
| V22 | One Nation media release on Voice to Parliament, July 2022 |
| TR23 | One Nation media release on Indigenous treaty, November 2023 |

If no verified Hanson quote exists for a node, use a documented paraphrase or description of documented action. Format:
`[Paraphrase: description of documented position/action] -Source (year)`

---

## Kanon JSON -- Ground Truth Files

| Plane | File |
|-------|------|
| P2 | `WWSUTRU/Australia/Aus Kanon/compact JSON/Plane_2_Definition_compact.json` |
| P3 | `WWSUTRU/Australia/Aus Kanon/compact JSON/Plane_3_Land_compact.json` |
| P4 | `WWSUTRU/Australia/Aus Kanon/compact JSON/Plane_4_Drive_compact.json` |
| P5 | `WWSUTRU/Australia/Aus Kanon/compact JSON/Plane_5_Method_compact.json` |

Each entry has: `address`, `name`, `coordinates.v`, `coordinates.psi`, `description`, `establishes`

---

## Dual-Address (FN Perspective) Nodes -- Known Pairs

### Plane 2
| Address | Node 1 Name | Node 2 Name |
|---------|-------------|-------------|
| What.Why.Where | A Bulwark | Connection [First Nations Perspective] |
| What.Effect.Cause | The Great Silence | Voice [First Nations Perspective] |

### Plane 3
| Address | Node 1 Name | Node 2 Name |
|---------|-------------|-------------|
| Where.How.Who | The Overland Telegraph | Songlines [First Nations Perspective] |

NOTE: The Overland Telegraph node is MISSING from the doc. Kanon has 50 nodes, doc has 49. Must investigate before adding -- check if it was intentionally omitted or is a doc error.

### Plane 4
| Address | Node 1 Name | Node 2 Name |
|---------|-------------|-------------|
| Why.Cause.Who | The Stain | Guilt [First Nations Perspective] |
| Why.Cause.Where | The Bush | Abundance [First Nations Perspective] |
| Why.Cause.Why | The War | Resistance [First Nations Perspective] |

### Plane 5
No dual-address pairs.

---

## Per-Plane Fix Checklist

### Pre-flight for each plane
- [ ] Load Kanon JSON for that plane
- [ ] Extract all node names + coords from doc
- [ ] Cross-reference: name mismatches, coord mismatches, missing nodes
- [ ] List all dual-address pairs and verify both names match Kanon

### Phase 1 -- Quote format normalisation
Applies to P3, P4, P5 (P2 already clean).

Old format: `**Quote:** ""Some text." (year)."`
New format: `**Quote:** "Some text" -Source (year)`

Regex to find old format: `\*\*Quote:\*\*\s*""`
Replace entire `**Quote:**[^\n]*` to end of line.

Do NOT touch body text below the header line.

### Phase 2 -- Dual-address name + coord verification
For each dual-address pair:
1. Confirm both node names exist in doc
2. Confirm both coords match Kanon JSON exactly
3. If name wrong: fix using body Description line as anchor (never address pattern alone)
4. If coords wrong: fix using Kanon JSON as source of truth

### Phase 3 -- Quote verification
For every node in the plane:
1. Is the quote real and verifiable? If yes, keep it (fix format only if needed).
2. If unverifiable or fabricated: replace with verified Hanson quote from corpus above, or paraphrase.
3. Does the quote topic align with the body's analytical focus? If not, flag for Phase 4.

### Phase 4 -- Justification alignment
For any node where quote was replaced:
- Read the body (Description / Justification / Actuality sections)
- Confirm the new quote's topic is compatible with what the body is analysing
- The body does NOT need to cite the quote directly -- it analyses the vector concept independently
- If there is a clear topic mismatch (e.g. quote is about immigration, body is about land rights), flag and source a better quote

### Body section length standard (from kanon-build.md)
Description: min 4-5 sentences
Justification: min 4-5 sentences
Actuality: min 4-5 sentences

If a body section falls below 4 sentences due to editing, flag it. Do not pad artificially -- only flag so it can be addressed.

---

## Execution Order

1. P2 -- name/coord audit only (format already clean), then quote verification
2. P3 -- format fix first, then missing node investigation, then quote verification
3. P4 -- format fix first, then quote verification
4. P5 -- format fix first, then quote verification

Each plane: complete all 4 phases before moving to next plane.

---

## Python Replacement Pattern (canonical)

For single-address nodes:
```python
pattern = re.compile(
    rf'(\*\*\({escaped_addr}[^)]*\)[^*]*\*\*)\s*\*\*Quote:\*\*[^\n]*'
)
clean_quote = new_quote.replace('\n', ' ')
repl = rf'\g<1> **Quote:** {clean_quote}'
new_section, count = pattern.subn(repl, section, count=1)
```

For dual-address nodes -- anchor to Description line:
```python
old = '**(Address) Name (υ: ..., ψ: ...): HIT/FAIL.** **Quote:** "..." \n\nDescription: [first ~8 words of description]'
new = '**(Address) Name (υ: ..., ψ: ...): HIT/FAIL.** **Quote:** "new quote" -Source (year)\n\nDescription: [first ~8 words of description]'
content = content.replace(old, new, 1)
```

NEVER use address pattern alone for dual-address nodes. ALWAYS include enough of the Description line to be unique.

---

## Error History (learn from these)

- Replacing node names by address pattern alone overwrote the FIRST node with the SECOND node's name when both share the same address. Fix: body-content anchoring.
- Coord inheritance: when a node name is restored after being wrongly overwritten, the coords may still be wrong (inherited from the FN node). Always cross-check coords against Kanon after any name fix.
- count=1 in regex does NOT protect against multiple passes overwriting the same node. Use string replace anchored to unique body text instead.
- P1 had 4 non-FN node names corrupted to FN names: The First Fleet, Populate or Perish, White Australia Policy, Federation. Check P2-P5 carefully for the same pattern.
