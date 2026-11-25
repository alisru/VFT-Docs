# Kanon Audit: Sourcing & Verification Redesign

Proposal, 2026-08-30. Every claim about an external source below was tested live this session, not assumed.

## The short answer to "surely someone's built this"

Partly. For **press quotes**, yes: GDELT's quotation extraction is a purpose-built "find the attributed quote" system and it works today with no API key. For **parliamentary quotes**, nobody has built the tooling, but the raw data is exceptionally good, free, complete, and current to the last sitting day. There is no MCP server for Australian Parliament (checked). The winning move is not finding a product, it is assembling free primary sources into a local index and putting a machine gate in front of the audit document.

---

## 1. Diagnosis: why the last audit had to be re-done

Three root causes. The first two are structural and were misread as search-skill problems in `Audit_Lessons_Learned.md`.

### 1.1 Half of Parliament is missing from the corpus

`corpus_1998_to_2025.parquet` is the Katz/Alexander *Australian Parliamentary Debates* dataset: **House of Representatives only**. Verified against the file:

| Probe | Result |
|---|---|
| Total speeches | 647,852 |
| Date range | 1998-03-02 to 2025-07-31 |
| Distinct speakers | 669 |
| `Hanson, Pauline` | **38 speeches, all between 1998-03-09 and 1998-07-15** |
| `Hanson-Young, Sarah` | **0** |

Pauline Hanson's entire Senate career (2016 to present) is not in the corpus. Neither is any senator. The skill names `query_hansard_corpus.py` as the "first stop for anything said in the chamber" — for the actor actually being audited, that first stop returned near-nothing, every time, by construction.

That is the mechanism that produced hallucinated quotes. The tool designated as ground truth silently had no data, the auditor fell through to generic web search, web search returned thin paraphrase, and the gap got filled from memory.

### 1.2 There is no retrieval index, only keyword filtering

Even inside the covered range, lookup is `LIKE '%term%'` over 648k full speech bodies. No BM25, no ranking, no semantic search. The Kanon's vectors describe *mechanisms*, and the skill itself correctly notes that searching the vector's poetic name returns nothing. But it offers no alternative retrieval mode — so the working pattern becomes "recall a plausible quote, then search to confirm it," which is exactly the shape that manufactures confident fabrications.

### 1.3 Nothing mechanically checks that a quote exists

"NEVER fabricate quotes" is a rule addressed to the model and enforced by the model. That is the component that failed. There is no step where a program takes a quote string and confirms it appears in a source. `verify_footnotes.py` and `find_unverified_quotes.py` exist in `Albo_Audit/drawing_board/` but are one-off scripts, not a gate.

**The fix in one line:** recall-then-verify is the right loop — it just never had anything to verify *against*. Give it a corpus, and add a gate that fails the build when a quote string isn't found in one.

### 1.4 The loop is right; two of its three branches were unreachable

The audit deliberately uses training data as a hypothesis generator: the model remembers a quote, then verifies it. That is sound — for an actor with a long public record, recall is a far better starting point than a cold search on an abstract vector name. The loop has three legitimate outcomes:

| Outcome | What should happen | What actually happened |
|---|---|---|
| **Verified** | quote is in Hansard verbatim → cite it | worked, when the actor was a post-1998 House member |
| **Near miss** | something very close is in Hansard → you were misremembering *that*; cite the real wording | **impossible** — no corpus to find the near miss in |
| **Not found** | nothing resembles it → abandon and find a different quote | collapsed into "search harder, then write it anyway" |

Only the first branch ever worked, and only for half of Parliament. The repair branch — *find what I was misremembering* — is the valuable one, because a half-remembered real quote is usually a real quote with drifted wording, not an invention. Without a corpus you cannot tell those two apart, so every unconfirmed recollection looked identical to a fabrication and got resolved by writing prose.

Both broken branches need the same thing: a local corpus and fuzzy retrieval over it. That is what Layers 1–2 deliver, and `search.py verify` implements exactly this three-way classification.

---

## 2. Layer 1 — Close the corpus hole (highest value, do first)

**OpenAustralia bulk Hansard XML.** Verified live this session:

- `https://data.openaustralia.org/scrapedxml/senate_debates/` — **1,034 files, 2006-02-07 → 2026-08-20**
- `https://data.openaustralia.org/scrapedxml/representatives_debates/` — **1,245 files, → 2026-08-20**
- Current to ten days ago. Still actively updating.
- ~800 KB average per sitting day, **~1.7 GB total**, one-time download then incremental (fetch only new dates).

Verified the XML parses cleanly with stdlib `ElementTree`, no dependencies. One Senate sitting day (2026-08-20) contains **343 speeches from 56 speakers**. Each `<speech>` element carries:

```
speakername, speakerid (stable person ID), time, talktype,
approximate_wordcount, approximate_duration,
id  (stable, e.g. uk.org.publicwhip/lords/2026-08-20.3.3),
url (ParlInfo permalink)
```

plus full paragraph text, the debate topic from enclosing `<major-heading>`/`<minor-heading>`, and `<bill>` IDs. That tuple *is* a complete citation — speaker, date, chamber, topic, permalink, verbatim text. There is nothing left to invent.

Speaker metadata for `speakerid` → party/electorate/term lives at `https://data.openaustralia.org/members/`: `people.xml`, `senators.xml`, `representatives.xml`, `ministers.xml`, `divisions.xml`.

**Pre-2006 and pre-1998:** `github.com/wragge/hansard-xml` — House **and** Senate, **1901–2005**, complete reharvest October 2024, folders `hofreps/` and `senate/`. Note 1981–1997 files use uppercase variant tags and need a separate parse branch.

Combining these with the existing parquet gives an **unbroken both-chamber record from 1901 to the last sitting week**, roughly 1.2M+ speeches. Hanson's Senate career goes from 0 rows to complete.

Licence on all of it: CC-BY-NC-ND, Commonwealth of Australia. Fine for citation; do not redistribute the corpus.

## 3. Layer 2 — Make it searchable by mechanism, not just keyword

**DuckDB FTS (Okapi BM25).** Benchmarked on the actual corpus this session:

| Step | Measured |
|---|---|
| Index 50,000 speeches | 14.9 s |
| → extrapolated, full ~1.2M speech corpus | ~5–6 min, one time |
| BM25 query | **0.13 s** |

```sql
INSTALL fts; LOAD fts;
PRAGMA create_fts_index('speeches', 'sid', 'body', overwrite=1);
SELECT fts_main_speeches.match_bm25(sid, 'immigration multicultural society') AS s, ...
```

Test query returned correctly ranked, real, verbatim hits. Note FTS indexes do not auto-update — rebuild after each incremental harvest.

**Add a semantic layer for the Kanon's abstract vectors.** BM25 still fails when the query is a mechanism rather than a keyword — which is most of the 343 nodes. Embed at **paragraph** granularity, not speech (a single speech ran 13,513 characters; that is far too coarse to cite from). Qdrant skills are already installed in this environment; DuckDB's VSS extension is the lower-friction alternative if you want to stay single-file. Run hybrid: BM25 for named things, vectors for "who benefits / what energy" mechanism matching, fuse the two result sets.

The search function must always return the full tuple — verbatim paragraph, speaker, party, date, chamber, ParlInfo URL, speech ID. The auditor pastes from that. They never type a quote.

## 4. Layer 3 — Non-chamber quotes (where the hallucinations actually lived)

The chamber is the easy half. Interviews, doorstops, press controversies and party platforms are where the last audit broke down.

### GDELT Context 2.0 API — `isquote=1` — **verified working, no API key**

```
https://api.gdeltproject.org/api/v2/context/context
  ?query="Pauline Hanson"&mode=artlist&format=json&isquote=1
  &maxrecords=5&sourcecountry=australia
```

Live test returned real Australian articles with `seendate` of 2026-08-30 — same-day coverage — each with the matched sentence, surrounding context, article URL, domain and date. This is the closest thing that exists to a purpose-built politician-quote finder. For quotes spanning several sentences, GDELT's **Global Quotation Graph** returns the full quote rather than Context 2.0's single-sentence window.

### PM Transcripts — **verified live (HTTP 200)**

`pmtranscripts.pmc.gov.au` — the official archive of Prime Ministerial transcripts: speeches, doorstops, radio and TV interviews, press conferences, 1940 to present. Non-negotiable for any PM-level actor. Directly fetchable, stable `/release/transcript-NNNNN` URLs.

### Wayback CDX API — **verified**, and this one fixes a named failure mode

Party policy pages get silently rewritten. Citing a live URL that later changes is how a verified claim decays into an unverifiable one — which is exactly the "citation only works by pointing at a hub page" problem in the lessons doc.

```
http://web.archive.org/cdx/search/cdx?url=onenation.org.au/policies*
  &output=json&collapse=urlkey&filter=statuscode:200
```

Returns dated snapshots of every One Nation policy sub-page back to 2017-02-21. **Cite the snapshot, not the live page.** The citation then becomes permanent and independently checkable forever.

### They Vote For You API

`https://theyvoteforyou.org.au/api/v1/people.json?key=...`, plus divisions endpoints filterable by house and date. Free key on signup, JSON. This is the right source for the "description of a specific documented action" evidence tier, and for the specific `/policies/NNN` sub-page URLs the skill already (correctly) demands.

### Parallel Search — keep, but last

Already wired into this environment. Use it only for the residual gap after the four sources above, not as a first move.

### What I would skip

- **Google Fact Check Tools API** — Google is phasing out ClaimReview support in Search, political entities' own sites are ineligible for the markup, and it indexes *fact-checks*, not quotes. Wrong shape for this job.
- **Trove** — full-text newspaper coverage largely stops at 1954 for copyright reasons. Low yield for living politicians.
- **ParlInfo browser scraping as a primary path** — the lessons doc measured it at 15–20 tool calls per lookup. Once the OA XML corpus lands, it is only needed for committee Hansard, which OA does not carry.

## 5. Layer 4 — The verification gate (this is what ends the re-do cycle)

Everything above only reduces the *pressure* to fabricate. This is the part that makes fabrication *fail loudly* instead of surviving into a finished document.

`verify_quotes.py`, run over a plane file:

1. Extract every `**Quote:** "..."` string and every `[^key]` marker.
2. Normalise both sides: unicode quotes → ASCII, en/em dashes, `&apos;` entities, collapse whitespace, casefold.
3. Look for the normalised quote in (a) the local Hansard index, (b) the cached fetch of its cited URL.
4. Classify:
   - **exact substring → VERIFIED**
   - **rapidfuzz `partial_ratio` ≥ 95 → NEAR** (transcription drift; print the character-level diff for a human call)
   - **< 95 → UNVERIFIED** (blocks)
5. Structural checks in the same pass: every marker resolves to exactly one key line; every key line is referenced; the cited URL exists in the fetch cache (i.e. was actually retrieved at least once); the URL is a specific page, not a bare domain or `/policies` hub.
6. **Exit non-zero on any UNVERIFIED.**

Wire it two ways: as a `/kanon-verify` slash command, and as a Claude Code `PostToolUse` hook on edits to `Plane_*.md` so a bad quote is caught at the moment it is written rather than at the end of a 343-node pass. This consolidates and hardens what `verify_footnotes.py` and `find_unverified_quotes.py` were reaching for.

The rule that failed was addressed to a model. Its replacement is addressed to an interpreter.

## 6. Layer 5 — Packaging

**Build `hansard-mcp`, a local MCP server.** I searched; no MCP server exists for Australian Parliament. One Python file over the DuckDB index exposing four tools:

- `search_hansard(query, speaker=, chamber=, date_from=, date_to=, mode=bm25|semantic|hybrid)`
- `get_speech(speech_id)` — full verbatim text
- `get_speaker(name)` — party, electorate, terms, chamber, speech count
- `verify_quote(text, speaker=)` — returns VERIFIED/NEAR/UNVERIFIED plus the matching source row

This converts a 15–20 call ParlInfo browser hunt into one call returning citation-complete rows. It is the single change that most reduces per-node cost.

**Skill changes to `kanon-audit`:**

- Replace the "Local Sourcing Tools" section with the new stack, and state the chamber/date coverage of each source explicitly so the "first stop" is never silently empty again.
- Add a hard rule: *the Quote field is pasted from a retrieval result. If you typed it, it is not a quote.*
- Add `verify_quotes.py` to "Before Declaring a Document or Plane Done" as a blocking check, not an assertion.
- Add the corpus-coverage table so any future audit can tell at a glance whether the actor is even in range.

**Cache discipline:** a `Sources_Archive/` with a `manifest.json` mapping URL → local file → fetch date. The lessons doc already asks for this; nothing enforces it. The verification gate enforcing "cited URL must be in the cache" makes it self-maintaining.

## 7. Build order

| # | Step | Effort | Unblocks |
|---|---|---|---|
| 1 | Harvest OA XML both chambers + wragge 1901–2005 → parquet | half a day | ends the Senate blind spot entirely |
| 2 | DuckDB FTS index + search CLI | ~1 hour | measured: 6 min build, 0.13 s queries |
| 3 | `verify_quotes.py` + hook | ~2 hours | **this is what stops the re-do cycle** |
| 4 | `hansard-mcp` server | ~2 hours | collapses per-node tool cost |
| 5 | GDELT + Wayback + PM Transcripts fetchers into `Sources_Archive/` | ~2 hours | fixes the non-chamber half |
| 6 | Hybrid embedding layer | half a day | mechanism-level search; do after 1–5 prove out |
| 7 | Rewrite the `kanon-audit` sourcing section | ~1 hour | locks it in |

Steps 1 and 3 alone address both root causes. Everything after that is cost reduction.
