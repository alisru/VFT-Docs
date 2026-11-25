---
name: speech-xmap
description: Cross-map a primary source speech or document against all 343 Kanon vectors in real time to identify alignment HITs, FAILs, and MISSes. Use this skill whenever the user provides a speech, transcript, interview, address, or primary source document and wants to know which Kanon vectors it hits, fails, or ignores. Also trigger when the user asks to analyse a speech against the framework, check what a speech covers, find what an actor didn't say, map a speech to the 7 planes, or run a real-time convergence check on a primary source. Do NOT use this skill to edit or update an audit document -- use kanon-audit for that.
---

# Speech Cross-Map Workflow

Takes a primary source speech, transcript, interview, or address and maps every scoreable statement against all 343 Kanon vectors. Outputs HIT, FAIL, or MISS per vector with the triggering quote and Qqci address.

MISS is analytically meaningful here: what an actor does not address in a formal speech is as significant as what they do. A MISS on a vector means the speech is silent on that dimension -- the absence is recorded, not ignored.

## Input

The speech text, provided directly in the conversation or as an uploaded file. Include source metadata if known: speaker, occasion, date, venue.

## Process

### Step 1 -- Load the Kanon

Read all 7 Kanon JSON files from references/ before beginning. For each of the 343 vectors, note:
- Address (e.g. Who.Where.Why)
- Name (e.g. Populate or Perish)
- What the vector measures (from description and establishes fields)
- Coordinates (v, psi) -- the ideal

For dual-address First Nations Perspective pairs, treat each as a distinct vector.

### Step 2 -- Extract scoreable statements

Read the speech in full. For each statement, claim, omission pattern, or rhetorical move, identify:
- Which plane it engages (WHO / WHAT / WHERE / WHY / HOW / CAUSE / EFFECT)
- Which sense within that plane
- Which specific vector
- Whether it aligns with the vector's ideal coordinates (HIT) or inverts them (FAIL)

A single statement can map to multiple vectors. Record all of them.

### Step 3 -- Score each vector

For all 343 vectors:

HIT -- the speech contains a statement that aligns with the vector's ideal. Record the exact triggering quote.
FAIL -- the speech contains a statement that inverts or contradicts the vector's ideal. Record the exact triggering quote.
MISS -- the speech contains nothing that directly engages this vector.

A vector can only be HIT or FAIL if there is a direct triggering statement from the speech text. Do not infer. Do not extrapolate from adjacent statements. No direct statement = MISS.

### Step 4 -- Output

Group results by plane. Within each plane, list all vectors with score and triggering quote.

Format per vector:
(Address) Name: HIT / FAIL / MISS
Quote: "exact triggering statement from speech" -- or -- [Silent]

After all 7 planes, output summary:
- Total HITs: N (N%)
- Total FAILs: N (N%)
- Total MISSes: N (N%)
- Most addressed plane: [plane] -- N vectors engaged
- Most silent plane: [plane] -- N MISSes
- Key Absences: the 5-10 most analytically significant MISSes

## Key Absences

This is the most analytically powerful section. A politician giving a major formal address who never engages a specific vector is making a structural statement through silence. Flag the most significant absences -- vectors where engagement would be expected given the speech's stated topic, occasion, or audience, but is entirely absent. Explain why each absence is significant.

## Constraints

- Do NOT edit or update any existing audit document. This skill is read-only.
- Do NOT fabricate or paraphrase quotes. Only use exact text from the provided speech.
- Do NOT infer alignment from adjacent statements. Direct engagement only.
- Source concentration is not a constraint -- if the speech hits 80 vectors, record 80 HITs/FAILs.
- FN Perspective vectors are scored independently from their paired primary vectors.
- Dual-address pairs at the same address must be scored separately against both nodes.
