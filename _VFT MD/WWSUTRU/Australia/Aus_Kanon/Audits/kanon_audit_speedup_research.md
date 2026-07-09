# Kanon-Audit Token Waste: Diagnosis & Fix Proposals

## Root Cause Diagnosis

The 25%-of-context-spent-on-quotes problem has **three stacked causes**, not one:

| Cause | What happens | Token cost |
|---|---|---|
| **No pre-built corpus** | Every node triggers a fresh live search from cold | 1-3 tool calls × 49 nodes = 50-150 calls per plane |
| **Serial search fallbacks** | WebSearch fails → try OpenAustralia API → try ParlInfo browser-use → give up | Each fallback adds 2-20 extra calls |
| **No local keyword-match against the corpus** | `query_hansard_corpus.py` exists but is only used as "first stop for anything said in chamber" — it's not being used to pre-filter ALL quotes up front before the audit starts | Every Hansard lookup goes live when it could be a zero-cost local grep |

The fix is **structural, not behavioral** — the SKILL.md already says "local first" but there's no script that does it automatically and no enforcement mechanism beyond the rule text.

---

## Proposed Fix 1: Pre-Audit Corpus Build Script (new)

**Concept**: Before touching a single node, run one script that:
1. Dumps the actor's full Hansard record from the parquet → actor JSONL (already exists via `query_hansard_corpus.py`, already done for Albanese)
2. Fetches the actor's official site speech archive (e.g. `senatorhanson.com.au/category/speech/`, `anthonyalbanese.com.au`) → local `.txt` files
3. Runs the news scraper once across all major source types → `actor_news.jsonl`

**Result**: A local `Sources_Archive/` folder with ALL available primary text already on disk. The audit then reads from disk, not from the network.

**Token savings estimate**: For a 343-node audit, this converts ~200+ live web calls into 3-5 upfront calls + zero-cost local reads.

**What's missing to implement it**:
- A thin wrapper script `build_audit_corpus.py` that calls `query_hansard_corpus.py`, then fetches a configurable list of URLs (actor's speech page, party platform pages) with `requests`+`trafilatura`, then calls `news_quote_scraper.py`
- Output: `Sources_Archive/{actor_slug}/hansard.jsonl`, `sources_archive/{actor_slug}/speeches/*.txt`, `news.jsonl`

---

## Proposed Fix 2: Batch Keyword Matcher Against Local Corpus (new script)

**Concept**: Given all 49 nodes in a plane's compact JSON (which has `description`, `rationale`, `establishes`), extract the mechanism keywords for each node and run them all as duckdb ILIKE queries against the local parquet in **one pass**.

Output: a `plane_N_leads.jsonl` file where each node address maps to its top 3 matching speech excerpts. The auditor then just picks the best one.

**Why this is cheap**: duckdb runs SQL directly against the 580MB parquet with no network call. 49 keyword searches across 647,852 rows completes in a few seconds locally.

**What's missing**:
- A script `match_nodes_to_corpus.py` that:
  1. Loads the plane's compact JSON
  2. For each node, extracts 2-4 mechanism keywords from the `description` + `rationale` fields (can be done with a regex heuristic or a small lookup table)
  3. Runs `SELECT date, body, uniqueID FROM parquet WHERE displayName ILIKE ? AND body ILIKE ?` for each
  4. Writes `plane_N_leads.jsonl`

**Token savings**: This replaces the per-node search for every in-chamber quote entirely — probably ~60% of all quote-sourcing calls.

---

## Proposed Fix 3: News Quote Pre-Index (already partially built)

`news_quote_scraper.py` already exists and is incremental (skips seen URLs). The problem is it's being called per-node or ad-hoc, not upfront.

**Fix**: Add a step to SKILL.md's Pre-Audit Phase that explicitly runs `news_quote_scraper.py` for the actor once at the start, producing `actor_news.jsonl`. Then for any out-of-chamber node, `grep actor_news.jsonl` for mechanism keywords instead of calling WebSearch.

The news JSONL already contains only attributed quotes + source URLs — exactly what the audit needs. Searching it is a free local operation.

---

## Proposed Fix 4: SKILL.md Sourcing Hierarchy Rewrite

The current hierarchy says "local first" but is framed as a per-node decision:
> "1. Local Database: Use `query_hansard_corpus.py`..."

This framing makes it feel like a search waterfall to try for each node. It should be restructured to enforce a **pre-audit corpus build phase** that happens once, not a per-node decision made 343 times.

### Proposed new Phase 0 in SKILL.md:

```
## Phase 0: Build the Source Corpus (run ONCE before any node work)

Before touching any node:

1. Hansard (if actor is a federal politician, House 1998-2025):
   Run: python query_hansard_corpus.py "ActorName" --out actor_hansard.jsonl
   Result: full parquet dump to local JSONL, zero network calls, instant.

2. Official speech archive:
   Fetch: actor's own speech category page (1-3 pages of links)
   Save each speech text to Sources_Archive/actor_slug/speeches/YYYY-MM-DD_title.txt

3. News quotes:
   Run: python news_quote_scraper.py "ActorName" --source docapi
   Result: actor_news.jsonl with attributed quotes + source URLs

4. Party platform pages (if applicable):
   Fetch the top 5-10 policy pages and save as Sources_Archive/policies/*.txt

After Phase 0, the audit runs entirely from local files. Only go to network
for a gap (quote not found in any local source).
```

---

## Proposed Fix 5: Node Batch Matching Script

When a plane's compact JSON is loaded, instead of asking the model to hypothesize + search + verify per node, run:

```
python match_nodes_to_corpus.py Plane_1_Identity_compact.json \
    --hansard actor_hansard.jsonl \
    --news actor_news.jsonl \
    --out plane_1_leads.jsonl
```

Each entry in `plane_1_leads.jsonl`:
```json
{
  "address": "1.1.1",
  "vector": "The Digger",
  "top_hansard_hits": [
    {"date": "2019-05-15", "excerpt": "...", "uniqueID": "..."},
    ...
  ],
  "top_news_hits": [
    {"quote": "...", "source": "...", "url": "..."},
    ...
  ]
}
```

The model then just picks the best hit per node, fetches the URL to extract verbatim text, and writes the node. **Verification is still required** — but the candidate-finding step is zero-cost and parallel instead of serial and expensive.

---

## Implementation Priority

| Priority | Item | Effort | Token savings |
|---|---|---|---|
| 1 | `build_audit_corpus.py` wrapper | 1-2h | Eliminates ~80% of live calls |
| 2 | Phase 0 block added to SKILL.md | 30m | Enforces the pattern in workflow |
| 3 | `match_nodes_to_corpus.py` | 2-3h | Eliminates per-node Hansard searches |
| 4 | SKILL.md sourcing hierarchy rewrite | 30m | Makes the rules structural |
| 5 | `plane_N_leads.jsonl` format standard | 1h | Makes auditing parallelisable |

---

## What NOT to change

- The verification step is non-negotiable: even with a local candidate quote, you still need to fetch the specific source URL and confirm verbatim text before writing the node. The bottleneck is *finding* candidates, not *verifying* them.
- The training-data hypothesis generator step (Move 2 in SKILL.md) is still valuable as a fallback for out-of-chamber quotes where the news scraper didn't catch it.
- The `Audit_Lessons_Learned.md` point about "one archival pass + handful of gap-fills" is already the right mental model — it just hasn't been backed by actual automation.
