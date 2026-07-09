# Quote Verification DB

Replaces `Nodes_Verification_Checklist.md` and `Sources_Verification_Checklist.md` (both moved to `../archive full/` — not deleted, kept for history). This is now the single source of truth for per-node and per-citation verification state on the Hanson audit.

## Why a DB instead of flat markdown

The old checklists could only say "verified" or "not yet" per node/source, split across two files, with no way to distinguish "real quote, slightly reworded" from "not in any source" from "source never fetched." A SQLite DB gives queryable state per node with full history, and the fuzzy checker below re-derives status independently instead of trusting a stale hand-written mark.

## Two access paths — read this before you're confused why a query fails

**For you, opening this on your own machine:** `quote_verification.db` in this folder is a normal, complete, valid SQLite file — open it directly with [DB Browser for SQLite](https://sqlitebrowser.org/) (free), DBeaver, or the SQLite VS Code extension. It'll work exactly like any other file, because on your Windows machine it's real local disk with real file locking. Verified byte-identical to the working copy via md5sum before being written here.

**For Claude, working inside the sandbox each session:** SQLite cannot open a `.db` file on the mounted E: drive from *inside this sandbox* — every attempt raises `disk I/O error`, because the bridge between the sandbox and your E: drive doesn't support SQLite's file-locking requirements. This is a limitation of that specific bridge, not of the file itself (confirmed: copying the raw bytes across and md5-summing both sides gives an identical hash — the data moves fine, only opening-with-locks-from-the-sandbox fails). So inside a session, Claude works against a copy at `/tmp/quote_verification.db`, and `quote_verification_dump.sql` in this folder is the real persisted artifact (plain text, a full `sqlite3 .dump`) used to carry state between sessions.

**Practical implication:** if you edit `quote_verification.db` directly on your machine (e.g. fix a status by hand in DB Browser), tell Claude what you changed — the next session restores from `quote_verification_dump.sql`, not from `quote_verification.db`, so a direct edit to the `.db` file alone won't carry forward unless the dump is regenerated from it and pushed back through this folder.

**At the start of any session (Claude's side):**
```
cp "Hanson_Audit/quote_db/quote_verification_dump.sql" /tmp/
cp "Hanson_Audit/quote_db/schema.sql" /tmp/
python3 restore_db.py /tmp/quote_verification_dump.sql
```

**Whenever you've changed data** (ran fuzzy_check.py again, or used `db_cli.py update`):
```
python3 dump_db.py
cp /tmp/quote_verification_dump.sql "Hanson_Audit/quote_db/"
```
If you forget this step, the next session's restore will not see your changes — the dump file is what persists, not the `.db`.

## Files

- `schema.sql` — table definitions: `nodes`, `sources`, `status_history`
- `build_db.py` — parses `Plane_1..7.md` header lines into `nodes`, pulls each node's canonical ideal from the Kanon compact JSON into `og_node_ideal`. Idempotent (re-running updates existing rows rather than duplicating).
- `migrate_legacy.py` — one-time pull of the old checklists' ✅/🔧/⚠️/🚩/⬜ marks into `legacy_status`/`legacy_note`, so prior verification work isn't lost. Only Plane 4 had node-level marks (52 nodes); the sources checklist covered all planes (52 of 63 citation keys matched — 11 keys are body-text-only citations not currently tracked at node level, since only header quotes are parsed).
- `fuzzy_check.py` — for every node with an archived source, checks whether the quote's words appear in `Sources_Archive/{citation_key}.txt` **in any order** (bag-of-words multiset overlap, so "ordered like this" and "this ordered like" score identically). Sets `status` + `fuzzy_score`. Non-literal quotes (documented paraphrases, no `"..."` in the original doc) are floored at `paraphrased` rather than auto-labelled `fabricated`, since word-overlap isn't a valid fabrication test for a summary sentence.
- `db_cli.py` — query/update/report from the command line (see below)
- `dump_db.py` / `restore_db.py` — the persistence workaround described above

## Status values

- `verified` — quote's words found in the archived source (ratio ≥ 0.85)
- `paraphrased` — partial word overlap (0.50–0.85), or any non-literal quote scoring below that
- `fabricated` — literal quote, low word overlap (< 0.50) against its cited archive
- `needs_hansard` — citation key exists but no archive file found for it
- `no_citation` — node header has no `[^key]` marker at all
- `unchecked` — seeded but not yet fuzzy-checked (should not occur after a full `fuzzy_check.py` run)

## CLI usage

```
python3 db_cli.py report                              # full summary + fabricated list
python3 db_cli.py list --status fabricated             # or --plane 4, --citation tvfy
python3 db_cli.py show 92                              # full row detail for node_id 92
python3 db_cli.py update 92 --status verified \
    --verified-quote "actual confirmed text" \
    --notes "re-fetched 2026-07-09, genuine"
python3 db_cli.py history 92                           # full status-change log for that node
```

Every `update` call and every `fuzzy_check.py` status change is logged to `status_history` with who/what changed it (`seed` / `migration` / `fuzzy_check` / `manual`) — nothing is silently overwritten.

## Current state (last full run: 2026-07-09)

353 nodes seeded, 343 Kanon-JSON ideals matched.

| status | count |
|---|---|
| verified | 298 |
| paraphrased | 34 |
| fabricated | 20 |
| no_citation | 1 |

**20 fabricated nodes need attention.** Run `python3 db_cli.py report` for the full list with node_id/address/citation. Notably, 15 of the 20 cite `[^tvfy]` (TheyVoteForYou, a voting-record aggregator) or `[^onenation]` (the confirmed-thin hub page per the old Sources checklist) with header text formatted as a literal quote — these sources cannot structurally contain first-person Hanson speech, so these are very likely quote-marked paraphrases that need reformatting to match Quote Standards (documented paraphrase, not literal quote), not necessarily fabricated content.

**1 no_citation node:** `Plane_1_Identity.md:917`, address `Who.Cause.How`, "Survival [First Nations Perspective]" — header has a quote and a source name (Lowitja O'Donoghue, Australian of the Year Address, 1984) but no `[^key]` footnote marker at all, so it resolves to nothing in the citation key list. Needs a citation key added.

**11 citation keys in the old Sources checklist are not yet tracked at node level** (they only support body/Actuality text, not header quotes): `theconv_ensuringintegrity`, `roymorgan26`, `aim26`, `antiworker`, `demosau26`, `hawker26`, `austlii03`, `conversation17`, `tvfy_plainpack`, `onenation_senategrowth25`. These carry legacy status in the old checklist but this DB currently only parses header-line citations — extending to body-text citations would need a separate parser pass over the Actuality sections.
