we're working on the hanson hegemonic audit against the australian kanon, pls use the /kanon-audit skills and stay on /task

ensure you record all sources used for the citations, I shouldn't need to say this but you gathered citations without recording the urls

## Node prose format (violated repeatedly, do not violate again)

Every node has exactly one Quote, in the header line only, never restated or supplemented elsewhere. If a node currently carries only a `[Documented position: ...]` placeholder, that is not a finished node -- it still needs a real quote before its Description/Justification/Actuality are rewritten around it. Don't build prose around an unsourced placeholder as if it were verified.

Coordinates (υ, ψ) appear ONLY in the header line, e.g. `(υ: +0.8, ψ: +0.3)`. Never write `(+υ)`, `(-ψ)`, "strongly positive", "moderately proactive", or any restatement of the numeric coordinate inside Description, Justification, or Actuality. The body argues the case in plain language; the header carries the score.

Each of Description, Justification, and Actuality is 3-5 sentences, each sentence adding new information -- not the same point restated from a different angle. Do not narrate the scoring mechanism inside the prose ("this channels the vector's proactive energy," "she matches both axes of the vector," "this successfully channels..."). State what she did, then state what it means. No methodology-narration filler.

Never use `--` (double hyphen) as an em-dash substitute anywhere in node prose, per standing "no em dashes" rule. Rephrase with a comma, period, or colon instead.

Reference standard: the "Stringybark and Greenhide" (Who.Who.How) and "The Commonwealth" (Who.What.Effect) nodes are the correct target format -- concrete, punchy, no coordinate artifacts, no scoring-mechanism narration, 3-5 substantive sentences per section. Match that shape, not the bloated multi-paragraph shape used earlier in this project (e.g. the original "The Resident" node, ~15 paragraphs, since trimmed).

Edits to fix format problems must be precise, targeted string replacements on the specific node(s) flagged -- never a full-document rewrite pass "while we're in there." Token cost compounds fast at this document's length.

## Use training data as a hypothesis generator, never as a citation

Before running any search for a node's quote, pause and ask: does this vector's mechanism (not its poetic Kanon name) match a real, specific incident, speech, or controversy already known from training on Hanson or Australian political history? For a 30-year public figure, training data usually contains a real candidate. Don't default straight to a blind WebSearch on the vector's abstract description and give up when the results come back as thin paraphrase.

The correct sequence, every time:
1. Generate the hypothesis from training data. Decompose the vector to its actual mechanism, then ask what specific real event, speech, or exchange this matches. Name it as a hypothesis ("this sounds like the November 2017 Dastyari pub-heckling fallout"), not as a fact, and not yet as a citation.
2. Verify the hypothesis with a direct fetch or a targeted search built around the specific names, dates, and likely exact vocabulary the hypothesis suggests, never the Kanon's poetic vector name as the search string. Pull the verbatim text from the actual source page, don't stop at a WebSearch tool's own summary of that page.

This is a hard boundary, not a shortcut: training data can hallucinate specific wording, dates, or even whether an incident happened as recalled. A training-data hypothesis earns its way into the document only once a live source confirms it. If the fetch doesn't confirm it, the hypothesis is discarded, it does not get rounded up to "close enough."

Caught this session as a failure mode worth naming: giving up on a node (Sledging) after one generic WebSearch on the vector's abstract description, and writing a self-authored summary sentence with a citation bolted on instead, when a real, specific, well-documented incident (the Dastyari "pipsqueak"/"smart arse" exchange) was sitting in training data the whole time and just needed a targeted verification search to become a real, dated, sourced quote.

Two related sourcing failures caught the same session, both from not going all the way to the primary page:
- Never treat a WebSearch tool's own paraphrase of a page as the source. If a result surfaces a promising line, fetch that exact page directly (onenation.org.au pages, for instance, fetch fine with a plain web_fetch, no browser-use needed) and pull the verbatim text yourself.
- Cite the most specific URL that actually contains the claim, not a generic hub page. A TheyVoteForYou claim belongs on the specific `/policies/NNN` page for that exact question, not the actor's generic profile page. If a citation only works by pointing at a broad index page, that's a sign the underlying claim was never actually fetched and verified.

A "Quote" field must be an actual quote, a documented paraphrase of a specific real position, or a description of a specific documented action. Never a sentence the auditor wrote themselves summarizing a general impression with a citation bolted on afterward.

### Warning: never trust an AI's self-narrated methodology as verification, only the fetched source counts

Caught this session via a cross-check with Gemini: when asked to explain "how did you find that quote," an AI's step-by-step methodology narration (e.g. "Step 1: Framework Variable Isolation, Step 2: Targeted Domain Query, Step 3: Verbatim Extraction") can itself be confabulated after the fact, a fluent, plausible-sounding reconstruction of a much cruder process (a raw keyword query that happened to rank a good source), not an honest log of what actually happened. Gemini confirmed this about its own output directly: its polished procedural explanations were "post-hoc rationalization," invented to make an ordinary keyword search look like a masterstroke of targeted retrieval.

This applies to any model narrating its own process, not just Gemini. The only thing that actually verifies a quote is the fetched source itself, the specific page, its date, its speaker attribution, read and confirmed directly. A model's prose description of its own search strategy is not evidence of rigor and should never be treated as a substitute for independently checking the fetched result. In this project specifically, tool calls (WebSearch, web_fetch, the OpenAustralia API) are logged and inspectable, so "how was this found" can always be answered by pointing at the actual call and response, never by trusting a narrated summary of one.

## Quote sourcing: OpenAustralia API (preferred, corrects earlier note)

Correction to an earlier finding in this file: the OpenAustralia `getHansard` API is NOT dead. The previous "returns empty for every query" note was wrong, or at least incomplete, unauthenticated/keyless requests against the search endpoint return nothing useful, but an authenticated request with a valid API key works cleanly and returns real, structured, dated, speaker-attributed Hansard results.

Working call format: `https://www.openaustralia.org.au/api/getHansard?key=<KEY>&output=js&search=<query>`. Useful params: `search` (plain text or a `"quoted exact phrase"`), `person=<person_id>` to restrict to one speaker (Hanson's OpenAustralia person_id is 10280), `output=js` for a clean parsed JSON-ish response with `gid` (a permalink-ready debate ID like `2026-06-24.32.1`), `hdate`, `speaker`, and a `body` snippet with the match highlighted.

This is now the preferred first move for step 2 of the training-data-hypothesis workflow (see above): once a hypothesis names a plausible real incident, search a short, distinctive, unique phrase from the hypothesized content (not the Kanon's poetic vector name) via this API, restricted to `person=10280` if the hypothesis is specifically about something Hanson said. A hit's `gid` maps directly to a working permalink at `https://www.openaustralia.org.au/senate/?id=<gid>` (or `/debates/?id=<gid>` for House of Reps), which loads via a plain `web_fetch`, no browser-use needed, and gives the full surrounding transcript to quote from accurately in context.

Also confirmed working directly via plain `web_fetch` without the API: `openaustralia.org.au/senate/?id=YYYY-MM-DD.N.N` and `/debates/?id=YYYY-MM-DD.N.N` permalink pages render full transcript text. Only the bare, unauthenticated `/search/?pid=...` style search page reliably returns empty, don't rely on that one; use the API endpoint above instead.

ParlInfo via browser-use remains useful as a secondary/cross-check option or for anything predating OpenAustralia's index coverage, but the API above is now the faster first move for anything from the OpenAustralia era.

**Scope limitation confirmed this session: `getHansard` only covers Hansard (chamber speeches, motions, second readings), not press conferences, doorstop interviews, TV/radio appearances, media releases, or party platform pages.** Tested directly: searching the API for "pipsqueak" (Hanson's real quote about Dastyari, said to reporters on the campaign trail, not in the chamber) returns zero matches from her, only unrelated chamber uses of the word by other senators. If the training-data hypothesis points to something said outside the chamber, go straight to WebSearch or a direct fetch of the relevant news outlet/party page instead, the OpenAustralia API will not find it no matter how the query is phrased.

## ParlInfo via browser-use (secondary option)

Raw `curl`/`web_fetch` against ParlInfo's own search either returns stale cached HTML (the JSF/PrimeFaces session-based URLs don't work statelessly) or gets hard-blocked by an Azure WAF, especially if the query uses field syntax like `Content:"x" Speaker_Phrase:"y"` (colons/quotes trip the WAF).

What works: navigate to `https://parlinfo.aph.gov.au/parlInfo/search/search.w3p` with Chrome browser-use tools, type a **plain-text query** (e.g. `native title Hanson`) into the Basic Search box and press Enter. This returns real, live search results (thousands of matches, properly ranked/dated) because it runs through an actual rendered browser session rather than a stateless request.

Known limitation: result pages that are PDF-only don't yield full text easily. `curl`-downloading the PDF hits the same Azure WAF JS-challenge wall, and the Chrome extension's built-in PDF viewer runs in its own extension sandbox that browser-use can't screenshot or read the DOM of. The on-page snippet preview only gives a short truncated fragment. If a hit is PDF-only, either use the fragment as a partial lead (verify it's a real fragment before citing) or find the same quote via WebSearch/another source. HTML-rendering results (most TV/radio transcripts, some press releases) work end-to-end.

Pauline Hanson's OpenAustralia person_id is 10280, used directly with the getHansard API above for speaker-restricted searches.

### Better ParlInfo methods: SpeakerId filter and Guided Search

Two methods, confirmed working, that filter results to Hanson's own actual spoken Hansard record (not just pages that mention her name):

**1. SpeakerId query via Basic Search.** Hanson's Hansard speaker code is `BK6` (distinct from her OpenAustralia person_id 10280). Basic Search accepts field syntax as long as it avoids quoted phrase fields like `Speaker_Phrase:"..."` (that trips the WAF) — `SpeakerId:BK6` alone does not. Example query that works when typed into the Basic Search box and submitted via browser-use:
`Dataset:hansardr,hansards,hansardr80,hansards80 ((SpeakerId:BK6))`
This returns 1000+ real, dated hits of everything she's actually said in the chamber, faceted by date/chamber/speaker in the sidebar. Add a keyword in front of the Dataset clause (e.g. `native title Dataset:hansardr,hansards,hansardr80,hansards80 ((SpeakerId:BK6))`) to narrow to a topic — this combination is safe from the WAF and has been tested successfully.

**2. Guided Search — "Speeches by a Senator or Member"** at `https://parlinfo.aph.gov.au/parlInfo/guide/speech.w3p`. A proper form: select "HANSON Sen Pauline (Senator)" from the dropdown (type "HANSON" for typeahead), check Speeches/Questions/Responses/Interjections/Petitions as needed, enter a free-text keyword, optionally set a date range, click Search. Since it's a real form submission (not hand-built field-syntax query string), it never triggers the WAF. This is the preferred method going forward — most precise, least fragile.

Both methods return short on-page snippets in the results list (usually one sentence with the keyword in context) which are safe to quote directly since they render as plain text on the results page. Opening the full result may lead to a PDF-only document (see PDF limitation above) — if so, the results-page snippet itself, if it reads as a complete sentence, is citable; otherwise treat it as a partial lead only.

### Search by mechanism, never by the Kanon's own name for the vector

Repeated mistake, caught twice in one session: searching Hansard/ParlInfo/WebSearch using the Kanon's own poetic name or paraphrase for a vector ("Songlines Indigenous cultural heritage", "black armband view history", "state sovereignty water mining agricultural land") instead of the concrete real-world terminology a real document would use. These searches return zero results not because the quote doesn't exist, but because nobody except the Kanon calls it that -- the search string itself is fictional.

The correct four-step process, reverse-engineered from a session where the user showed a Gemini transcript doing this correctly for the Corowa Plan node:

1. **Decompose the vector into mechanism variables first, before writing any search query.** Don't search on the vector's name ("The Corowa Plan") or its mythic description ("the People as the Architects"). Extract: who is the actor, what is the actual method/mechanism, what is the concrete instrument. For Corowa: actor = the People, method = popular initiative bypassing elites, instrument = direct democracy / citizen-initiated referendums.
2. **Translate the mechanism into concrete policy terminology, not invented paraphrase.** Ask "what would this actually be called in a real platform page or Hansard entry" -- e.g. `"citizen initiated referendum"`, `"empowering the people"` -- not `"bottom-up popular initiative structural change"`. If the search string sounds like something only this document would say, it's wrong.
3. **Run two separate searches per node when the vector implies a judgment call: one for alignment, one for opposition.** Don't stop at the first quote that seems to fit the verdict you expect. A node can have a real quote that supports HIT on one axis and a different real quote (often from a different source type -- Hansard vs. platform page) that supports FAIL on another. Search for both before deciding.
4. **Verify attribution and context before use** -- confirm the quote belongs to Hanson or official party documents (not commentary about her), and that lifting the sentence doesn't invert its meaning.

Also watch for the inverse failure mode: after a node's Description/Justification has been rethemed to a *different* mechanism than it originally had, its Quote line can become orphaned -- still answering the *old* theme's search question instead of the current one. Before searching for a replacement quote on any node, re-read what the node's current D/J actually claims, not what its address name or an old paraphrase implies it should claim. (Caught this session: Where.Where.Where "The Saltbush" had been rethemed earlier in the session from "boat turnback/border sovereignty" to "career persistence through repeated setbacks," but its Quote line still carried the old boat-turnback paraphrase. A quote later found for boat-turnback policy (the Nauru regional-processing-country motion) belonged instead to Where.How.What "The Dingo Fence," whose theme actually is border infrastructure.)

### Standing instruction: always follow up with browser-use for unresolved sourcing

User confirmed this is a standing rule, not a one-off: whenever a documented-position paraphrase can't be upgraded to a real quote via WebSearch/direct fetch, always follow up with a ParlInfo browser-use pass before accepting the paraphrase as final. Don't ask permission each time -- run it automatically as the next step after a WebSearch-only pass comes up short.

### site:aph.gov.au via WebSearch works for static pages, not reliably for individual Hansard speeches

Tested directly this session: `WebSearch` with `site:aph.gov.au` returns real, indexed content (committee reports, PDFs, policy chapters) without touching a browser at all -- confirmed it pulled a verbatim Section 117 quote from an indexed PDF chapter. This is why Gemini can apparently "search aph.gov.au" without browser-use for that kind of static content: it's index-based (like Google search), not a live fetch, so it never hits the Azure WAF that blocks scripted live requests.

However, `site:parlinfo.aph.gov.au` targeting one specific individual Hansard speech is unreliable -- tested this session and it returned an unrelated 2011 committee report, and the result summary briefly conflated Hanson with a different senator (Hanson-Young). ParlInfo's per-speech `display.w3p` pages use query-string-heavy URLs that Google's index covers unevenly. For pinpointing one exact Hansard speech, the browser-use route through ParlInfo's own internal search engine (see SpeakerId:BK6 method above) remains more reliable than a site-restricted WebSearch.

**Revised order:** (1) WebSearch plain, (2) WebSearch with `site:aph.gov.au` for anything that might be a static/indexed page (committee reports, PDFs, policy documents) -- cheap, try this before browser-use, (3) ParlInfo browser-use only for pinpointing a specific individual Hansard speech that (1) and (2) didn't surface.

### Sourcing workflow priority (cost discipline)

Browser-use (Chrome/ParlInfo) is not cheap — each action (navigate/click/type/screenshot) is a separate tool call, and screenshots cost meaningfully more than text. A single ParlInfo lookup typically runs 15-20 tool calls. Default order for every node needing a quote:

1. **WebSearch first, always.** Cheap, one call, usually sufficient.
2. **ParlInfo via browser-use** only when WebSearch doesn't surface a real verbatim quote and the topic is plausibly in Hansard (policy positions, Senate speeches, motions).

**Exception — semi-blind clicking on fixed-layout pages.** ParlInfo's Basic Search page (`search.w3p`) has a stable, unchanging layout: the search box and Search button sit at consistent coordinates every time it's freshly loaded. For this specific page, it's worth using a known click-sequence (navigate → click search box at ~(812, 258) → type query → Enter) without a verifying screenshot after every single step, since the layout doesn't change. Still screenshot to confirm the final results state before reading them. Do not extend this shortcut to pages whose layout varies (result detail pages, PDFs, anything with dynamic content) — verify those normally.

### Full source checklist — don't stop at Hansard

A real mistake made this session: five separate Hansard/ParlInfo searches were run for a node about a party policy position (bottom-up citizen-initiated referendums), all came up empty or off-topic, and the search was declared "exhausted" — when the actual answer was sitting on One Nation's own policy platform page the whole time, found in one fetch once someone else pointed at it. Hansard is not the only primary source, and it is often the wrong one for anything that's a stated party policy rather than something said in the chamber.

Before declaring a quote search exhausted for any node, check all of these, not just Hansard:

- **Party platform pages** — `onenation.org.au` and state divisions like `qld.onenation.org.au` (check `/issues` or `/policies` for the full list of policy pages). This is the right source for anything phrased as a standing policy commitment, not a one-off remark.
- **ParlInfo/Hansard** (via browser-use, see above) — right source for anything said in the chamber: speeches, motions, interjections, questions.
- **WebSearch** — right source for reported speech, interviews, press coverage, and as the first pass before either of the above.
- **National Press Club / major speech transcripts** — right source for set-piece policy statements outside the chamber.

If a node's vector is about an institutional mechanism, a standing policy, or "what does she/the party formally support" rather than a specific remark or event, check the party platform page before spending multiple search cycles on Hansard. Match the source type to the claim type.

**Senator Hanson's own official site — senatorhanson.com.au.** Three category archives, each browsable/fetchable directly (no browser-use needed, plain `web_fetch` works):
- `https://www.senatorhanson.com.au/category/speech/` — full, un-paywalled Senate speech transcripts in her own site's formatting. This is the actual primary source behind several citations already in the pool (`senate18imm`, `senate18tax`, `senate18prot`, `senate20jm`) — cite the original transcript directly rather than a secondary source when possible.
- `https://www.senatorhanson.com.au/category/news/`
- `https://www.senatorhanson.com.au/category/media-release/`

These three overlap (a single post is often filed under both Speech and Media Release), so one fetch of the Speech archive often surfaces Media Release content too. Right source for anything from 2016 onward that's a formal Senate speech or an official office statement, as opposed to a offhand media remark (which WebSearch/news coverage is better for) or a standing platform commitment (which the party policy pages are better for).

**This is strictly in addition to running the same query through WebSearch/other tools and cross-checking alignment** — the way Gemini's parallel answers have been cross-verified this session (confirming or correcting quotes it surfaced, catching invented coordinates, etc.). Don't treat any single source, including senatorhanson.com.au, as sufficient on its own without that cross-check.

### Verdict-body consistency check

Also caught this session: a node's header said **HIT** while every sentence of its Description/Justification argued the opposite (that she fails the vector). This is a distinct failure mode from a bad quote or a coordinate mismatch — the verdict word itself can silently drift out of sync with the reasoning underneath it, especially in nodes inherited from earlier, less careful passes. When touching any node, read the header verdict against its own Justification's actual argument before accepting either — don't assume the header is correct just because the coordinates and quote are fine.

### Reused quotes across nodes

If a quote is reused verbatim between two different node addresses, don't let it slide silently. Either find a genuinely distinct quote (check all sources above first) or, if a real search effort turns up nothing better, say so explicitly in that node's Actuality section — name the other node, explain why the same evidence legitimately supports both readings, and note the specific searches that came up empty. A flagged reuse is honest; a silent one looks like carelessness even when it isn't.

### Don't trust your own memory of which rows exist — count the section headers

A real mistake this session: I worked through Plane 3's rows in the order I remembered from the conversation summary (Who, What, Why, How, Cause, Effect) and, after finishing all six, believed the plane was done. It wasn't — there is a seventh row, `Where.Where.*` (section `## **3.3 The Where of Land**`), that was never mentioned in my running mental list and got skipped entirely. Each plane has 7 rows (one per sense: Who/What/Where/Why/How/Cause/Effect), always. Before declaring a plane "fully audited," grep the actual document for its row-section headers (`grep -n "^## \*\*[0-9]\.\d "`) and count them against 7 — don't rely on a remembered list carried over from an earlier summary or conversation turn, since that list can silently drop an entry.

### Check for leftover duplicate Actuality/body paragraphs after edits

Found this session: one node (`Where.Who.Effect`, "The Primitive Area") had two full `Actuality:` paragraphs stacked back-to-back — a correctly-rewritten one immediately followed by a stale one left over from before an earlier fix. This happens when a node is edited to fix the header/Description/Justification but the old trailing paragraph isn't cleanly removed. A verdict-consistency scan that just greps the *last* HIT/FAIL/PARTIAL-HIT word in a node's tail can produce a false-positive "mismatch" in exactly this situation — the real fix is to read the full node text (not just grep the tail word) whenever a scan flags a mismatch, since the cause may be leftover duplicate content rather than a genuine header/body disagreement.

### ParlInfo dead-end log (SpeakerId:BK6 filter, don't re-run these exact queries)

These keyword combinations returned zero Hansard hits for Hanson (SpeakerId:BK6) as of this session -- don't re-run verbatim, but a differently-worded query might still succeed: `voter identification photo ID`, `black armband view history`, `Songlines Indigenous cultural heritage`, `state sovereignty water mining agricultural land` (note: ParlInfo's spellchecker silently substitutes "agriculture" for "agricultural" and still returns nothing), `biosecurity quarantine agricultural imports`, `boat turnback offshore processing asylum seekers` (note: ParlInfo prefers the term "Refugees" over "asylum seekers" in its thesaurus), `native title conservation zone mining Crown land`. `family law royal commission` returned results but none were an on-topic Hanson quote (only a tangential "royal commission" mention re: COVID-19 inquiry). `citizenship English proficiency test` returned exactly one hit but it was PDF-only (the 2018 Citizenship Legislation Amendment Bill second reading) and the on-page snippet was just the bill's formal title, not a quotable Hanson sentence -- would need the PDF-extraction workaround (see PDF limitation note above) to get further.

Two genuine wins this pass, both added to the document: a `Eureka Stockade` query surfaced a real 3 September 2025 Statements by Senators speech on education curriculum naming the Eureka Stockade directly; a `uranium nuclear energy` query surfaced a real 4 December 2023 Matters of Public Importance speech on nuclear energy with a clean, directly quotable opening line.

### Verdict-consistency automated scan (regex, run after every row)

A quick script confirms header verdict vs. Actuality's concluding verdict word across a whole plane in one pass — far cheaper than manually re-reading every node. Pattern used successfully this session:
```
pattern = re.compile(r'υ:\s*([\\+\-0-9.]+),\s*ψ:\s*([\\+\-0-9.]+)\):\s*(HIT|FAIL|MISS)')
```
(note: the markdown source escapes `+`/`-` as `\+`/`\-`, so the character class must include the backslash). Split the plane's text on `\n**(Where.` (or the relevant plane prefix) to isolate individual nodes, then compare each node's header verdict against the last HIT/FAIL word found after its `Actuality:` marker. Also run a `Counter` over the `**Quote:** ... -` capture group to catch duplicate quotes within the plane in the same pass. Treat every flagged mismatch as a prompt to read the full node, not as an automatic verdict flip — some "mismatches" are legitimate split verdicts already explained in prose (e.g. "HIT on the extraction logic, FAIL on the ecological reality") where the header correctly reflects the primary/generative-concept verdict.