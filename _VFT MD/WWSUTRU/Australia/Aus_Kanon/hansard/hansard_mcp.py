#!/usr/bin/env python3
"""hansard-mcp -- the local Commonwealth Hansard corpus as MCP tools.

Wraps the DuckDB index built by parse.py + index.py. The point is to make the
cheap, correct move also the easy one: a single tool call returns verbatim text
with speaker, party, chamber, date, debate topic and a ParlInfo permalink, so a
quote is pasted from a retrieval result rather than typed from memory.

Tools:
    corpus_coverage   what is actually in the corpus -- CHECK THIS FIRST
    verify_quote      is this remembered quote real? verified / near miss / not found
    search_hansard    BM25 search for a quote to cite
    get_speaker       a member's seats, terms and corpus coverage
    get_speech        full verbatim text of one speech

Run: python hansard_mcp.py     (stdio transport)
"""

import sys
from pathlib import Path

import duckdb
from mcp.server.fastmcp import FastMCP
from rapidfuzz import fuzz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search import (MIN_CAND_RATIO, NEAR_FLOOR, keywords,  # noqa: E402
                    norm, norm_words, quoted_span)

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "hansard.duckdb"

mcp = FastMCP("hansard")

_con = None


def con():
    """One shared read-only connection; opened lazily so import never fails."""
    global _con
    if _con is None:
        if not DB_PATH.exists():
            raise RuntimeError(
                f"{DB_PATH.name} not found. Run harvest.py, parse.py, "
                "members.py and index.py first."
            )
        _con = duckdb.connect(str(DB_PATH), read_only=True)
        _con.execute("INSTALL fts; LOAD fts;")
    return _con


def _cite(r):
    """Citation-complete record. Everything a footnote needs, nothing else."""
    date, speaker, chamber, major, minor, url, sid = r
    return {
        "speaker": speaker,
        "chamber": "Senate" if chamber == "senate" else "House of Representatives",
        "date": str(date),
        "debate": " / ".join(x for x in (major, minor) if x) or None,
        "url": url,
        "speech_id": sid,
        "openaustralia_url": (
            f"https://www.openaustralia.org.au/debates/?id={sid.split('/')[-1]}"
        ),
    }


@mcp.tool()
def corpus_coverage() -> dict:
    """What the local Hansard corpus actually contains. Call this FIRST.

    The original failure this whole tool exists to prevent was a corpus that
    silently held no data for the person being audited: the House-only dataset
    contained 38 Hanson speeches from 1998 and nothing from her Senate career,
    so every lookup came back empty and the gap got filled from memory. Check
    coverage before concluding that a quote "isn't in Hansard".
    """
    rows = con().execute("""
        SELECT chamber, min(sitting_date), max(sitting_date),
               count(DISTINCT sitting_date), count(DISTINCT speech_id), count(*)
        FROM para_search GROUP BY chamber ORDER BY chamber
    """).fetchall()
    return {
        "chambers": [
            {"chamber": r[0], "first_sitting": str(r[1]), "last_sitting": str(r[2]),
             "sitting_days": r[3], "speeches": r[4], "paragraphs": r[5]}
            for r in rows
        ],
        "caveats": [
            "Chamber proceedings only: no committee Hansard, no press "
            "conferences, doorstops, interviews, media releases or party "
            "platform pages. For those use PM Transcripts, GDELT or the "
            "actor's own site.",
            "Coverage starts 2006-02-07. Anything earlier is not here.",
            "Speaker names are as Hansard records them, which is not always "
            "the common name -- Pauline Hanson appears as 'Pauline Lee "
            "Hanson'. Use get_speaker to resolve a name before filtering.",
        ],
    }


@mcp.tool()
def verify_quote(quote: str, speaker: str = "", limit: int = 3) -> dict:
    """Check a remembered quote against Hansard. The anti-fabrication gate.

    Returns one of:
      verified            the quote is in Hansard verbatim -> cite it
      verified_punctuation_differs
                          same words, different punctuation -> fine, cite it
      near_miss           something very close is there; you misremembered the
                          wording. The real text is returned -- cite that
      not_found           nothing resembles it. Do NOT cite. Use search_hansard
                          to find a different quote instead

    ALWAYS pass `speaker` when you know whose quote it is. Members quote each
    other constantly: searching Hanson's words unfiltered returns Sarah
    Hanson-Young quoting her in order to attack her, at 92% similarity. Citing
    that would attribute the line to the wrong senator while looking fully
    verified. Any hit whose matched text sits inside quotation marks in the
    source is flagged `is_quotation: true` -- do not cite those as the
    speaker's own words.
    """
    q = norm(quote)
    if len(q) < 12:
        return {"verdict": "error", "detail": "quote too short to verify"}

    sp = f"%{speaker.lower()}%" if speaker else None
    clause = " AND lower(speakername) LIKE ?" if sp else ""
    cols = ("sitting_date, speakername, chamber, major_heading, "
            "minor_heading, url, speech_id")

    exact = con().execute(
        f"SELECT text, {cols} FROM para_search WHERE text_norm LIKE ?{clause} "
        f"LIMIT {limit}", [f"%{q}%"] + ([sp] if sp else [])
    ).fetchall()
    if exact:
        return {"verdict": "verified",
                "matches": [{"text": r[0], **_cite(r[1:])} for r in exact]}

    qw = norm_words(quote)
    if len(qw) >= 25:
        loose = con().execute(
            f"SELECT text, {cols} FROM para_search WHERE "
            "regexp_replace(regexp_replace(text_norm, '[^\\w\\s]', ' ', 'g'), "
            f"'\\s+', ' ', 'g') LIKE ?{clause} LIMIT {limit}",
            [f"%{qw}%"] + ([sp] if sp else [])
        ).fetchall()
        if loose:
            return {"verdict": "verified_punctuation_differs",
                    "note": "Same words; only punctuation differs. Safe to cite.",
                    "matches": [{"text": r[0], **_cite(r[1:])} for r in loose]}

    terms = " ".join(keywords(quote, 14))
    if not terms:
        return {"verdict": "not_found", "best_score": 0}
    cands = con().execute(
        f"SELECT text, text_norm, {cols} FROM "
        "(SELECT *, fts_main_para_search.match_bm25(pid, ?) AS s FROM para_search) "
        f"WHERE s IS NOT NULL{clause} ORDER BY s DESC LIMIT 60",
        [terms] + ([sp] if sp else [])
    ).fetchall()

    floor = len(q) * MIN_CAND_RATIO
    scored = sorted(((fuzz.partial_ratio(q, c[1]), c)
                     for c in cands if len(c[1]) >= floor), key=lambda x: -x[0])
    if not scored:
        return {"verdict": "not_found", "best_score": 0}

    best = scored[0][0]
    if best < NEAR_FLOOR:
        return {"verdict": "not_found", "best_score": round(best, 1),
                "advice": "Do not cite this. Use search_hansard to find a "
                          "different, real quote for this vector."}

    out = []
    for score, c in scored[:limit]:
        if score < NEAR_FLOOR:
            break
        out.append({"similarity": round(score, 1), "text": c[0],
                    "is_quotation": quoted_span(c[1], q), **_cite(c[2:])})
    return {
        "verdict": "near_miss",
        "best_score": round(best, 1),
        "advice": "You misremembered the wording. Cite the real text below.",
        "speaker_filter_used": bool(speaker),
        "warning": None if speaker else
        "No speaker filter was used. Check the speaker on every hit before "
        "citing -- members quote each other constantly.",
        "matches": out,
    }


def _one_search(query, topic, speaker, chamber, date_from, date_to, limit):
    terms = " ".join(keywords(query, 20))
    if not terms:
        return []
    where, params = ["s IS NOT NULL"], [terms]
    if speaker:
        where.append("lower(speakername) LIKE ?"); params.append(f"%{speaker.lower()}%")
    if chamber:
        where.append("chamber = ?"); params.append(chamber)
    if date_from:
        where.append("sitting_date >= CAST(? AS DATE)"); params.append(date_from)
    if date_to:
        where.append("sitting_date <= CAST(? AS DATE)"); params.append(date_to)
    if topic:
        where.append("(lower(minor_heading) LIKE ? OR lower(major_heading) LIKE ?)")
        params += [f"%{topic.lower()}%"] * 2

    return con().execute(f"""
        SELECT pid, text, s, sitting_date, speakername, chamber, major_heading,
               minor_heading, url, speech_id
        FROM (SELECT *, fts_main_para_search.match_bm25(pid, ?) AS s
              FROM para_search)
        WHERE {' AND '.join(where)} ORDER BY s DESC LIMIT {limit}
    """, params).fetchall()


@mcp.tool()
def search_hansard(query: str, variants: list[str] = [], topic: str = "",
                   speaker: str = "", chamber: str = "", date_from: str = "",
                   date_to: str = "", limit: int = 8) -> dict:
    """BM25 search for a real quote to cite.

    Search the actor's own real-world vocabulary and the mechanism, never a
    Kanon vector's poetic name -- nobody but the Kanon uses those words, so
    that search returns noise.

    Two things make this work much better than a single plain query:

    `topic` filters to debates whose heading matches, and it is usually the
    single highest-value narrowing available. BM25 over 3.1M paragraphs buries
    good material under high-scoring noise; restricting to the right debate
    surfaces quotes that would never rank top-10 otherwise. Use `list_topics`
    first to see what the actor actually spoke in.

    `variants` runs additional phrasings of the same idea and unions the
    results, deduplicated, keeping each paragraph's best score. This covers
    vocabulary mismatch -- the actor said "the doors of opportunity" and you
    searched "social mobility". Pass 3-5 genuinely different phrasings, not
    synonyms of one word. Each query costs about a second.

    chamber: "senate" or "reps". Dates are ISO (YYYY-MM-DD).
    """
    per = max(4, min(limit, 25))
    seen, out = {}, []
    for i, q in enumerate([query] + [v for v in variants if v and v.strip()]):
        for r in _one_search(q, topic, speaker, chamber, date_from, date_to, per):
            pid, score = r[0], r[2]
            if pid in seen:
                if score > seen[pid]["bm25"]:
                    seen[pid]["bm25"] = round(score, 1)
                    seen[pid]["matched_query"] = q
                continue
            rec = {"text": r[1], "bm25": round(score, 1), "matched_query": q,
                   **_cite(r[3:])}
            seen[pid] = rec
            out.append(rec)

    out.sort(key=lambda x: -x["bm25"])
    return {
        "queries_run": 1 + len([v for v in variants if v and v.strip()]),
        "topic_filter": topic or None,
        "matches": out[:min(limit, 25)],
        "hint": None if topic else
        "No topic filter used. Call list_topics to find the relevant debates "
        "and re-run -- it typically surfaces material BM25 buries.",
    }


@mcp.tool()
def list_topics(speaker: str = "", contains: str = "", chamber: str = "",
                limit: int = 30) -> dict:
    """Which debates did this person actually speak in?

    Hansard tags every paragraph with its debate heading (53,355 distinct
    minor headings, present on 98% of the corpus). Picking the real debate
    before searching beats guessing at vocabulary: use this to find the topic,
    then pass it to search_hansard's `topic` argument.
    """
    where, params = ["minor_heading IS NOT NULL"], []
    if speaker:
        where.append("lower(speakername) LIKE ?"); params.append(f"%{speaker.lower()}%")
    if chamber:
        where.append("chamber = ?"); params.append(chamber)
    if contains:
        where.append("(lower(minor_heading) LIKE ? OR lower(major_heading) LIKE ?)")
        params += [f"%{contains.lower()}%"] * 2

    rows = con().execute(f"""
        SELECT minor_heading, major_heading, count(*) AS n,
               min(sitting_date), max(sitting_date)
        FROM para_search WHERE {' AND '.join(where)}
        GROUP BY minor_heading, major_heading
        ORDER BY n DESC LIMIT {min(limit, 100)}
    """, params).fetchall()

    return {"topics": [
        {"minor_heading": r[0], "major_heading": r[1], "paragraphs": r[2],
         "first": str(r[3]), "last": str(r[4])} for r in rows
    ]}


@mcp.tool()
def get_speaker(name: str) -> dict:
    """Resolve a person to their seats, terms and actual corpus coverage.

    Use this before filtering by speaker. Hansard's recorded name is often not
    the common one, and `speakerid` is an office id rather than a person, so a
    politician who changes chamber holds several -- Pauline Hanson has both a
    1996-98 House seat and a 2016- Senate seat.
    """
    seats = con().execute("""
        SELECT DISTINCT person_name, house, party, division, fromdate, todate
        FROM members WHERE lower(person_name) LIKE ? OR lower(lastname) LIKE ?
        ORDER BY fromdate
    """, [f"%{name.lower()}%"] * 2).fetchall()

    corpus = con().execute("""
        SELECT speakername, chamber, min(sitting_date), max(sitting_date),
               count(DISTINCT speech_id), count(*)
        FROM para_search WHERE lower(speakername) LIKE ?
        GROUP BY speakername, chamber ORDER BY speakername, chamber
    """, [f"%{name.lower()}%"]).fetchall()

    return {
        "seats": [{"person": r[0], "house": r[1], "party": r[2],
                   "electorate": r[3], "from": r[4], "to": r[5]} for r in seats],
        "hansard_names": sorted({r[0] for r in corpus if r[0]}),
        "corpus": [{"speakername": r[0], "chamber": r[1], "first": str(r[2]),
                    "last": str(r[3]), "speeches": r[4], "paragraphs": r[5]}
                   for r in corpus],
        "note": "If `corpus` is empty the person may predate 2006 or sit in a "
                "chamber/name variant not matched -- widen the name and retry "
                "before concluding a quote is not in Hansard.",
    }


@mcp.tool()
def get_speech(speech_id: str) -> dict:
    """Full verbatim text of one speech, paragraph by paragraph."""
    rows = con().execute("""
        SELECT para_no, text, sitting_date, speakername, chamber,
               major_heading, minor_heading, url, speech_id
        FROM para_search WHERE speech_id = ? ORDER BY para_no
    """, [speech_id]).fetchall()
    if not rows:
        return {"error": f"no speech with id {speech_id}"}
    r = rows[0]
    return {**_cite(r[2:]),
            "paragraphs": [{"para_no": p[0], "text": p[1]} for p in rows]}


if __name__ == "__main__":
    mcp.run()
