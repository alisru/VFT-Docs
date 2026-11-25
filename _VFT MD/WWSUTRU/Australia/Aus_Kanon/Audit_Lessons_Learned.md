# Kanon Audit: Lessons Learned (read before starting any new audit)

Short, practical rules from real mistakes made during the Pauline Hanson audit. Not a repeat of `/kanon-audit`'s methodology, this is the "don't do the dumb thing again" list. Applies to auditing any actor against any Kanon, not just Hanson vs. Australia.

## 1. Build the actor's source corpus BEFORE starting node work, not node-by-node

The single biggest time/token sink this audit: searching per-node, live, mid-edit, every time a quote was needed. Fix for next time, do this first, before touching a single node:

- Pull the actor's full official archive up front: speech transcripts, press releases, party platform/policy pages, voting record. Most politicians have one canonical site (e.g. `senatorX.com.au/category/speech/`) that's directly fetchable and covers years of material in a handful of fetches.
- Pull their Hansard/parliamentary record via the relevant API or search tool if one exists (see #2), not one WebSearch per topic.
- Archive the fetched text locally (a `Sources_Archive/` folder of plain `.txt` files, one per source, tagged) so re-reading a source later costs zero tool calls.
- Only after that corpus exists, start walking the 343/353 nodes and match evidence to vectors from what's already on hand. Go back to live search only for genuine gaps.

This turns "343 searches" into "one archival pass + a handful of gap-fills."

## 2. Don't default to generic LLM web search, it's weak and expensive here

Plain WebSearch tends to return thin paraphrase of a page rather than the page itself, costs a full round trip per query, and repeatedly failed to find quotes that were sitting in training data the whole time. Prefer, in this order:

1. **Training data as a hypothesis, always first.** For any actor with a real public record, ask "what specific real incident/speech does this vector's mechanism describe" before searching anything. Name the hypothesis, then verify it, don't search cold on the vector's abstract/poetic name.
2. **A dedicated structured API if the domain has one** (e.g. OpenAustralia's `getHansard` for Australian federal speeches, `person=<id>` to restrict to one speaker). Structured, dated, speaker-attributed, cheap.
3. **Direct fetch of the actor's own official site/archive.** Fastest path to primary text once you know roughly what you're looking for.
4. **WebSearch with a `site:` restriction to a specific static/indexed domain** (party platform pages, .gov.au, committee reports) for anything document-like.
5. **Browser-based search of a site's own internal search engine** (e.g. ParlInfo) only as a last resort for pinpointing one specific record that nothing else surfaced, this is the most expensive option (15-20 tool calls per lookup), don't reach for it first.

Never treat a WebSearch tool's own summary of a page as the citation. If it surfaces a promising line, fetch that exact page and pull the verbatim text yourself.

## 3. Match source type to claim type

- A **standing policy position** → the party's own platform/policy page, not Hansard.
- Something **said in the chamber** → Hansard/parliamentary record, not a press summary.
- **Reported speech, interviews, controversies** → press coverage / WebSearch.
- A **set-piece formal speech** outside the chamber → National Press Club or the actor's own site, not generic search.

Don't declare a search "exhausted" after failing on the wrong source type, check whether the claim is even the kind of thing that source covers.

## 4. Sourcing hygiene

- Cite the most specific URL that actually contains the claim (a `/policies/NNN` page, not the generic `/policies` hub). If a citation only works by pointing at a broad index page, the claim was probably never actually verified.
- Search by the actor's real-world terminology and the mechanism, never by the Kanon's own poetic vector name, nobody but the Kanon calls it that, so that search returns nothing.
- Re-read what a node's Description/Justification *currently* claims before searching for its quote. If a node was rethemed earlier, the old quote is often still attached and now answers the wrong question.

## 5. Score math and consistency discipline

- Alignment % and average coordinates are **verdict-weighted**: `avg = sum(coord * (1 if HIT else -1)) / count`. Never a raw unweighted average.
- Never hardcode a total vector count anywhere (in scripts or prose), always compute it from the data. A hardcoded total silently goes stale the moment a node count changes.
- After any pass, check the header verdict (HIT/FAIL) against what the node's own Justification/Actuality actually argues, they can silently drift out of sync, especially in nodes inherited from earlier passes.
- Watch for leftover duplicate paragraphs after an edit (an old Actuality left stapled behind a newly-rewritten one), read the whole node, not just the tail, when a consistency check flags something.

## 6. Structural bookkeeping

- Each plane has exactly 7 rows (Who/What/Where/Why/How/Cause/Effect). Don't rely on a remembered list of which rows you've done, grep the actual section headers and count against 7 before declaring a plane finished.
- Don't trust an AI's own narrated methodology ("Step 1: I isolated the framework variable...") as evidence a quote is verified. Only the actually-fetched source page counts. Narrated process can be fluent post-hoc rationalization of a much cruder search.

## 7. Editing discipline

- Fix format violations with precise, targeted string replacements on the flagged node(s) only, never a full-document rewrite pass "while we're in there." Token cost compounds fast at full-audit length.
- If a violation repeats across many nodes, fix every instance in the same pass once you're already in there, that's finishing the task, not scope creep.
