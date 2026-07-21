---
name: kanon-audit
description: Audit an actor against a National Kanon -- evaluate their quotes, positions, and actions against the 343-vector Qqci framework to produce a Hegemonic Audit document. Use this skill whenever the user asks to audit an actor, run a hegemonic audit, score someone against the Kanon, check an actor's vectors, evaluate HIT or FAIL verdicts, fix or update an existing audit document, verify quotes in an audit, correct node headers, or validate coordinates against the Kanon. Also trigger when the user asks to check quote formats, fix dual-address node names, validate First Nations perspective pairs, or replace fabricated quotes with verified sources.
---

# Kanon Audit Workflow

Audits an actor against a pre-built National Kanon. Produces or maintains a Hegemonic Audit document structured as 343 nodes across 7 planes, each scored HIT or FAIL with (upsilon, psi) coordinates and a verified quote.

## The Whole Job, In One Loop

For every node: read it directly (not via regex or script). Run it through the Alignment Evaluation Methodology below. If it passes, leave it alone. If it fails on anything, quote can't be verified, mechanism doesn't actually support the verdict, coordinates or name don't match the Kanon JSON, coordinate notation sitting in the body text, rewrite the whole node in one edit: Quote, Description, Justification, and Actuality together. Don't split this into separate passes for format vs. quote vs. justification. One node, one look, one fix if it needs one, move on.

If a scan turns up the same violation repeated across many nodes, fix every instance in the same pass. That is not a scope decision requiring confirmation, it's finishing the task already given. Only stop to ask when the next step is a genuinely new decision, such as whether to commission fresh primary-source research on nodes nobody has touched yet.

## Node Header Format (canonical)

**(Address) Vector Name (upsilon: +X.X, psi: +Y.Y): HIT/FAIL.** **Quote:** "quote text" -Source Context (year)[^shortkey]

Rules:
- Coords use escaped markdown: \+ or \- before the number
- Quote is on the SAME LINE as the header -- no line break between header and quote
- Source context must be meaningful: "Maiden Speech, House of Representatives, Hansard" not "Speech" or "Media statement"
- No double-quote wrapping: NOT ""quote." (year)." -- that is the broken old format
- Every header quote carries a footnote marker, e.g. [^ms96], immediately after the source context. Reuse the same key for the same source across nodes; give a new source a new short key.
- Every distinct citation used anywhere in a node (header quote or Actuality) must resolve to an entry in that document's master footnote key (see Citation Key below). A marker with no matching key entry is a broken citation, not a stylistic choice.

## Body Section Format

Each node has three body sections below the header. Minimum 4-5 sentences each.

Description: Context of the audit -- what this vector measures, what the canonical ideal is, and how the actor's position relates to it. No coordinate notation (υ, ψ, +0.x, -0.x) anywhere in this section -- explain the reasoning in plain sentences instead.

Justification: Why the quote and conduct result in a HIT or FAIL against the fixed coordinates. Must explain the upsilon and psi reasoning in plain language, not by inserting the symbols. Does not cite the quote directly -- analyses the vector concept independently.

Actuality: The actor's actual output relative to their capacity over time. Actively search for the most recent verified quote or documented action relevant to this vector -- do not reuse the header quote. Every specific claim, date, or figure in this section must carry its own footnote marker (e.g. "...cannot be a multicultural society."[^netimes26]), reusing an existing key if the source repeats, adding a new key otherwise. End with TENTATIVE FAIL if actuality contradicts the stated HIT/FAIL verdict.

## Citation Key (master footnote list, required)

Every node quote and Actuality citation uses an inline marker (`[^shortkey]`), never a raw URL inline. Each document (or each Plane file, if split by plane) ends with a master key section resolving every marker used in that file, one line each:

[^shortkey]: Full Source Name, Publication/Body, Date: URL

Rules:
- Every marker used anywhere in the body must have exactly one matching key line at the end of the file. No orphaned markers, no unused key lines.
- Reuse the same key across every node that cites the same source (e.g. [^ms96] for the 1996 Maiden Speech everywhere it's quoted). Never mint a new key for a source already keyed.
- The key line must be specific enough to independently verify: real title/description, real date, real URL, not a generic domain or hub link (see Quote Standards below on citing the specific page, not a parent page).
- When adding, replacing, or verifying any quote, add or confirm its key line at the same time. Don't leave a citation pass for later, it's part of finishing the node.
- Before declaring a document or plane done, grep every `[^` marker in the body and confirm each resolves to a key line, and grep every key line and confirm it's actually referenced at least once in the body (unused keys are dead weight, missing keys are broken citations).

## Coordinate System

Read references/coordinate-system.md for the full (upsilon, psi) rules.

Coordinates come from the Kanon JSON files -- never from judgment. The Kanon JSON is ground truth.

## Quote Standards

Priority order:
1. Real verified quote from the actor, directly sourced
2. Closely documented paraphrase of a real position
3. Description of documented action

NEVER fabricate quotes. NEVER present unverified text as objective fact. Validate every quote before keeping it. If a quote cannot be verified, replace it.

When replacing a quote: source from the verified corpus in references/verified-sources.md first.

Never treat a WebSearch tool's own summarized paraphrase of a page as the source. If a search result surfaces a promising line from a specific page (a party platform page, a named article), fetch that exact page directly and pull the verbatim text yourself before citing it. A summary of a summary is how "documented paraphrase" quietly degrades into an unverified guess dressed as a citation.

Cite the most specific URL that actually contains the claim, not a generic parent page. A voting-record claim belongs on the specific policy page (e.g. a TheyVoteForYou `/policies/NNN` page for that exact question), not the actor's generic profile page. A platform quote belongs on the specific policy page it was said on, not the site's generic `/policies` index. If the citation only works by pointing at a broad hub page, that is a sign the underlying claim was never actually verified and needs a real fetch.

A "Quote" field must be an actual quote, a documented paraphrase of a specific real position, or a description of a specific documented action, never a sentence the auditor wrote themselves summarizing a general impression with a citation bolted on. If there is no specific attributable line or documented action to cite, say so plainly rather than manufacturing a general-sounding summary sentence.

## Kanon JSON Reference

The 7 Aus Kanon compact JSON files are in references/. They are ground truth for:
- Vector names at each address
- Correct coordinates for each vector
- First Nations perspective shadow pairs (address, name, coordinates)

Files: Plane_1_Identity_compact.json through Plane_7_Result_compact.json

For other nations, load the equivalent JSON files from that nation's Kanon directory.

## Local Sourcing Tools (check before WebSearch or a live API)

Four scripts in `Aus Kanon/compact JSON/`, plus a local corpus file, cover most federal-politician sourcing without touching the network:

- `query_hansard_corpus.py` -- queries `corpus_1998_to_2025.parquet` via duckdb. House of Representatives, 1998-03-02 to 2025-07-31, full speech text per row (not a snippet), instant, no network call, no cap. **First stop for anything said in the chamber by a House member in that range.**
- `aph_scraper.py` -- live scrape directly against aph.gov.au's own Hansard search. No result cap, covers Senate + House + committees, reaches back through full Hansard history. Use for Senate, anything after July 2025, or anything the parquet doesn't cover. Gives title/date/PDF link per match; full inline text extraction from the HTML page isn't solved yet, PDF is the reliable full-text source.
- `hansard_scraper.py` -- OpenAustralia API mirror. Superseded by the two above for anything in their coverage; caps at ~8000 results per person and its API snippet is only ~400 characters (this script now also fetches the full Hansard page per speech to get around that). Fallback only.
- `news_quote_scraper.py` -- for anything not said in the chamber: interviews, press, controversies. Extracts only quotes attributed to the actor plus short context, never full article bodies.

## Dual-Address (First Nations Perspective) Nodes

Some addresses have TWO nodes: a primary entry and a [First Nations Perspective] shadow entry. Both share the same address field.

Critical rules:
- ALWAYS anchor edits to the body Description line text -- never to the address pattern alone
- Address-pattern-only matching will corrupt the other node at the same address
- After any name fix: immediately verify coords also match Kanon JSON -- name corruption and coord inheritance are always paired bugs
- Never identify a node by address alone when two exist at that address

## Alignment Evaluation Methodology (Core Audit Protocol)

This is the intellectual core of the audit, and it is genuinely just two moves: identify the ideal expressed, identify how the actor hits or fails it. Everything below is the method for doing each move well -- it is not a longer list of separate phases.

### Move 1: Identify the Ideal Expressed

Each vector sits at a plane address: Plane.Sense.Vector (e.g. Effect.Cause.Effect). Triangulate: "[Vector] of the [Sense] of the [Plane]", what is the [Vector-plane's function] expressed through the [Sense-plane's lens] within the [Plane's domain]?

Example: Effect.Cause.Effect = "What is the Result of the Foundation at the Result plane?" = "Does the present causal sequence produce the same quality of life as an inherited outcome for future generations?"

The Kanon JSON name, coordinates, and description are the distilled answer. Read them. Get to the actual shape of the ideal: who it's meant to benefit (broad or narrow), and what kind of energy embodying it takes (building something together, enduring passively, actively defying something). Not just the topic noun, the mechanism.

### Move 2: Identify How the Actor Hits or Fails It

Find real evidence of the actor's own mechanism on this same shape, then compare the two shapes directly.

Frame every search around this question, filled in concretely, never left abstract: "In a quote, how does [actor] hit or fail the ideal identified in [node]?" -- then immediately translate [node]'s ideal into the real-world mechanism it names (see Move 1) before you search. The question is a framing device to keep the search actor-and-mechanism-specific, it is not itself a search string, don't type the Kanon's node name or poetic phrasing into a search box.

How to find it: primary sources first, speeches, Hansard, policy documents, direct statements on record. Look for where the actor states their reasoning, not just their conclusion, the causal chain in their thinking, not just a position. Keyword grep on an unstructured news corpus is the wrong tool, and so is searching for the Kanon's poetic vector name as if the actor needs to use those literal words. This does NOT apply to the local Hansard corpus (`query_hansard_corpus.py`) -- that's a structured, dated, speaker-attributed, complete parliamentary record, not a fuzzy scrape, and keyword filtering against it is exactly the right approach for anything said in the chamber. You're finding wherever in the actor's real record the same mechanism is visible, even if it never mentions the vector's name at all. If nothing verifiable turns up, say so and use the weakest-evidence category honestly (documented paraphrase, then documented action) rather than manufacturing something that reads well.

How to compare it: the actor can keep the ideal's surface grammar while inverting its actual shape, same costume, opposite mechanism. Check both axes of what you found against the Kanon's fixed coordinates, never assigned from the quote, never decided before the quote:

υ (who benefits): does the actor's mechanism broaden or narrow the beneficiary relative to the ideal?
ψ (energy direction): does it actively build toward the ideal, or substitute something else, passive endurance, grievance, exclusion, for the energy the ideal actually requires?

If the evidence clearly answers both axes, the verdict is sound. If it only addresses one axis or the mechanism is ambiguous, go find better evidence rather than rounding an ambiguous quote up to a confident HIT or FAIL.

### Use Training Data as a Hypothesis Generator, Never as a Citation

Before running any search for a node's quote, pause and ask: does the vector's mechanism (not its poetic Kanon name) match a real, specific incident, speech, or controversy already known from training? For actors with substantial public records (long-serving politicians, major parties, historical figures), training data usually contains a real candidate, don't skip straight to a blind WebSearch on the vector's abstract description and give up when the results come back thin.

The correct two-step sequence:
1. **Generate the hypothesis from training data.** Decompose the vector to its mechanism (see Move 2), then ask what specific real-world event, speech, or exchange this actor is known for that matches that mechanism. Name it as a hypothesis: "this sounds like it could be the [specific incident/date/name]," not as a fact.
2. **Verify the hypothesis with a targeted fetch or search.** Build a precise query around the specific names, dates, and distinctive vocabulary the hypothesis suggests (e.g. actual likely phrases the actor would have used, not the Kanon's poetic vector name), then fetch the actual primary or named-outlet source and extract the verbatim text from it directly. The training-data hypothesis earns its way into the document only once a live source confirms it. It is never itself the citation, and it is never presented as verified fact before that fetch happens.

This is a hard boundary, not a shortcut: training data can hallucinate specific wording, dates, and even whether an incident happened as recalled. Treat every training-data recollection as unconfirmed until the fetch step lands on a real, checkable source. If the fetch doesn't confirm the hypothesis, the hypothesis is discarded, it does not get rounded up to "close enough."

Known failure mode this corrects: running a generic WebSearch on the vector's abstract description (e.g. "psychological probe for dominance") instead of first asking "what specific real incident does this describe for this actor" using training knowledge, then quitting when the generic search returns thin paraphrased summaries instead of a real quote. The fix is always to search for the *specific incident*, not the *abstract vector*.

## Reporting

When updating any node: report to user in chat -- address, what changed, before/after. Nothing goes in the audit doc except the fix itself.

After completing a plane: report total nodes checked, quotes replaced, name/coord fixes, and confirm the structural checks below were run.

## Before Declaring a Document or Plane Done

Run these checks with grep/python and report the results, don't just assert completion:
- Every node's address, name, and coordinates match the Kanon JSON exactly
- Every Justification block has actual content (not empty)
- No coordinate notation (υ, ψ, +0.x, -0.x) appears anywhere in body text
- Sources are complete and no URLs are truncated
- Every `[^marker]` in the body resolves to a key line in the master footnote list, and every key line is referenced by at least one marker in the body (see Citation Key above)
- Verdict-weighted scoring is intact wherever alignment percentages or average coordinates are calculated: avg = sum(coord * (1 if HIT else -1)) / count. Raw unweighted averaging is always wrong for this audit.

## Known Failure Modes (do not repeat)

- Replacing node names or quotes by address pattern alone when two nodes share an address overwrites the wrong node's data. Anchor to body text instead.
- Coord inheritance: fixing a corrupted name but leaving its inherited wrong coordinates in place. Always re-check coordinates after any name fix.
- Regex or scripted diffing against the document is what caused the corruption bugs above, and it can also silently misreport what's actually in the file (e.g. a pattern that requires a +/- sign will miss a real "0.0" coordinate and wrongly report a node as missing). Read the actual file directly to verify structure; use scripts only for cheap, disposable lookups, never as the source of truth about document content.
- Always confirm the exact file path before editing -- don't assume two similarly-named folders hold the same copy.
- Skill files are packaged as .skill zips in the user's io folder. To update one: unzip to /tmp, edit SKILL.md, rezip, copy back to io/. Don't tell the user to edit it manually when the zip is accessible.
- When asked a direct yes/no question about whether something exists in a file, answer the question. Don't silently add it to the file instead.
- Try chmod, then the zip/tmp/cp approach, before telling the user a permission error makes something impossible.
- Giving up after one generic WebSearch on the vector's abstract/poetic language and settling for a self-written summary sentence as the "Quote." Always try the training-data-hypothesis-then-verify sequence above first, and always attempt a direct fetch of the actor's own site or the specific named source before concluding nothing verifiable exists.
- Citing a generic hub/profile/index URL when the actual claim lives on a specific sub-page. Confirmed accessible this session: onenation.org.au pages fetch fine directly with a plain web fetch, no browser-use needed, so "I couldn't find a specific source" is rarely actually true, check whether the page was ever directly fetched before concluding that.
