#!/usr/bin/env python3
"""Non-chamber source archive and quote verification.

The Hansard corpus covers the chamber. It does not cover press conferences,
doorstops, interviews, media releases, party platform pages or set-piece
speeches outside parliament -- which is where most of an audit's quotes
actually come from (76 of 118 in the Albanese audit) and where the last round
of fabrications lived.

This does three things:

  archive   fetch a URL once, extract its readable text, cache it forever
  check     is this quote actually on that page, verbatim?
  wayback   find a dated snapshot, because party policy pages get rewritten
            and a live URL that changes turns a verified claim into an
            unverifiable one

The cache is the point. A source fetched once costs nothing to re-read, and
"the cited URL must be in the cache" is what stops a citation being written
for a page nobody ever opened.

    python sources.py archive <url> [<url> ...]
    python sources.py check "quote text" <url>
    python sources.py wayback <url-pattern>
    python sources.py audit <plane.md> [--sources Sources.md]
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import requests
from rapidfuzz import fuzz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search import norm, norm_words  # noqa: E402

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parent / "Sources_Archive"
MANIFEST = ARCHIVE / "manifest.json"

NEAR_FLOOR = 88
UA = "aus-kanon-source-archive/1.0 (research; quote verification)"
URL_RE = re.compile(r"https?://[^\s)\]<>\"]+")
# Footnote keys often pack two sources separated by "; ", and sentences end in
# a full stop, so a raw URL match drags trailing punctuation in with it and the
# fetch 404s on a URL that is actually fine.
URL_TRAIL = ";,.:"


def urls_in(text):
    return [u.rstrip(URL_TRAIL) for u in URL_RE.findall(text or "")]


def load_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def save_manifest(m):
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, indent=1, sort_keys=True), encoding="utf-8")


def key_for(url):
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def extract_text(html, url):
    """Readable body text. trafilatura first, BeautifulSoup as the fallback."""
    try:
        import trafilatura
        got = trafilatura.extract(html, url=url, include_comments=False,
                                  include_tables=True, favor_recall=True)
        if got and len(got) > 200:
            return got
    except Exception:  # noqa: BLE001
        pass
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    return re.sub(r"\n{3,}", "\n\n", soup.get_text("\n")).strip()


# A WAF block is the dangerous failure, because it is not an error. pm.gov.au
# sits behind Incapsula and returns "Request unsuccessful" with HTTP 200, so a
# naive fetch succeeds, extracts a block page, and the checker then reports
# NOT ON PAGE -- falsely accusing a real citation of being fabricated. Detect
# these and fall back to a Wayback snapshot rather than reporting a verdict.
BLOCK_MARKERS = (
    "request unsuccessful", "incapsula incident", "access denied",
    "attention required", "checking your browser", "enable javascript",
    "just a moment", "403 forbidden", "are you a robot",
)
MIN_USABLE_CHARS = 300


def looks_blocked(text):
    if len(text.strip()) < MIN_USABLE_CHARS:
        return True
    head = text[:600].lower()
    return any(marker in head for marker in BLOCK_MARKERS)


def _fetch_text(url):
    r = requests.get(url, timeout=90, headers={"User-Agent": UA})
    r.raise_for_status()
    return extract_text(r.text, url), r.status_code, r.url


def archive(url, refetch=False):
    """Fetch a URL once and cache its extracted text. Returns a manifest entry.

    If the live page is blocked or empty, retries via the most recent Wayback
    snapshot before giving up, and records which source the text came from.
    """
    m = load_manifest()
    k = key_for(url)
    if k in m and not refetch and (ARCHIVE / m[k]["file"]).exists():
        return m[k]

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    text, status, final = _fetch_text(url)
    via = "live"

    if looks_blocked(text):
        snaps = []
        try:
            snaps = wayback(url, limit=40, collapse=False)
        except Exception:  # noqa: BLE001
            pass
        # CDX returns oldest first; newest snapshot is the closest match to
        # the page as cited, so walk backwards.
        for s in sorted(snaps, key=lambda x: x["timestamp"], reverse=True):
            try:
                alt, _, _ = _fetch_text(s["snapshot_url"])
            except Exception:  # noqa: BLE001
                continue
            if not looks_blocked(alt):
                text, via, final = alt, f"wayback:{s['timestamp'][:8]}", s["snapshot_url"]
                break
    fname = f"{k}.txt"
    (ARCHIVE / fname).write_text(text, encoding="utf-8")

    entry = {"url": url, "file": fname, "chars": len(text),
             "fetched": time.strftime("%Y-%m-%dT%H:%M:%S"),
             "status": status, "final_url": final, "via": via,
             "blocked": looks_blocked(text)}
    m[k] = entry
    save_manifest(m)
    return entry


# An audit "Quote" is allowed to be a description of a documented action
# rather than words spoken. Those begin "Documented action:" and testing them
# for verbatim text on a page is simply the wrong test -- it reports NOT ON
# PAGE for citations that are perfectly correct.
ACTION_PREFIX = ("documented action", "[documented position")

# A quote split by an internal ellipsis is two fragments from one source, not
# one string. Neither the page nor Hansard contains it as written, so checking
# it whole always fails. Check the fragments.
INNER_SPLIT = re.compile(r"\s*(?:\.\.\.|…)\s*")


def check(quote, url, refetch=False):
    """Is `quote` actually on the page at `url`? Same three verdicts as Hansard."""
    if quote.strip().lower().startswith(ACTION_PREFIX):
        return {"verdict": "NOT A VERBATIM QUOTE (documented action)", "url": url,
                "advice": "This entry describes an action rather than quoting "
                          "words, so there is nothing to match verbatim. Check "
                          "the cited page supports the action claim instead."}

    inner = [f for f in INNER_SPLIT.split(quote.strip()) if len(f.strip()) >= 25]
    if len(inner) > 1:
        parts = [check(f, url, refetch) for f in inner]
        ok = [p for p in parts if p["verdict"].startswith("VERIFIED")]
        return {
            "verdict": ("VERIFIED (spliced)" if len(ok) == len(parts)
                        else "SPLICE: not all fragments found"),
            "url": url, "fragments": len(parts), "fragments_verified": len(ok),
            "detail": [{"fragment": f[:70], "verdict": p["verdict"],
                        "score": p.get("score")} for f, p in zip(inner, parts)],
            "advice": None if len(ok) == len(parts) else
            "A spliced quote must have every fragment on the cited page. "
            "Split it into separate quotes or drop the unverified fragment.",
        }

    try:
        entry = archive(url, refetch=refetch)
    except Exception as exc:  # noqa: BLE001
        return {"verdict": "FETCH FAILED", "detail": str(exc)[:160], "url": url}

    if entry.get("blocked"):
        return {"verdict": "UNREADABLE (blocked or empty)", "url": url,
                "via": entry.get("via"), "chars": entry["chars"],
                "advice": "The page could not be read (WAF block, JS-only, or "
                          "empty) and no usable Wayback snapshot was found. "
                          "This is NOT evidence against the quote -- verify it "
                          "another way before changing anything."}

    body = (ARCHIVE / entry["file"]).read_text(encoding="utf-8")
    q, qw = norm(quote), norm_words(quote)
    bn, bw = norm(body), norm_words(body)

    if q and q in bn:
        return {"verdict": "VERIFIED", "url": url, "cached": entry["file"]}
    if len(qw) >= 25 and qw in bw:
        return {"verdict": "VERIFIED (punctuation differs)", "url": url,
                "cached": entry["file"]}

    # Fuzzy: slide over the page in windows about the quote's size.
    best, where = 0.0, ""
    step = max(60, len(q) // 2)
    for i in range(0, max(1, len(bn) - len(q)), step):
        win = bn[i:i + int(len(q) * 1.5)]
        s = fuzz.partial_ratio(q, win)
        if s > best:
            best, where = s, body[i:i + int(len(q) * 1.5)]
    if best >= NEAR_FLOOR:
        return {"verdict": "NEAR MISS", "score": round(best, 1), "url": url,
                "page_text": where.strip()[:400], "cached": entry["file"]}
    return {"verdict": "NOT ON PAGE", "score": round(best, 1), "url": url,
            "cached": entry["file"],
            "advice": "The cited page does not contain this quote. Either the "
                      "citation points at the wrong page, or the quote is not "
                      "real. Do not leave it as-is."}


def wayback(url_pattern, limit=12, collapse=True):
    """Dated snapshots from the Wayback CDX API.

    Party policy pages are edited in place. Citing the live URL means the
    citation silently stops supporting the claim; citing a dated snapshot
    means it never does.
    """
    r = requests.get(
        "http://web.archive.org/cdx/search/cdx",
        params={"url": url_pattern, "output": "json", "limit": limit,
                "filter": "statuscode:200",
                **({"collapse": "urlkey"} if collapse else {})},
        timeout=90, headers={"User-Agent": UA},
    )
    r.raise_for_status()
    rows = r.json()
    if not rows:
        return []
    cols = rows[0]
    return [
        {**dict(zip(cols, row)),
         "snapshot_url": f"https://web.archive.org/web/{dict(zip(cols,row))['timestamp']}/"
                         f"{dict(zip(cols,row))['original']}"}
        for row in rows[1:]
    ]


def audit_file(path, sources_path=None):
    """Check every non-Hansard quote in a plane file against its cited URL."""
    from verify_quotes import KEY_RE, extract_quotes, is_hansard

    text = Path(path).read_text(encoding="utf-8")
    keys = {m.group("key"): m.group("body") for m in KEY_RE.finditer(text)}
    if sources_path:
        for m in KEY_RE.finditer(Path(sources_path).read_text(encoding="utf-8")):
            keys.setdefault(m.group("key"), m.group("body"))

    results = []
    for rec in extract_quotes(text):
        if not rec["quote"] or not rec["key"]:
            continue
        body = keys.get(rec["key"])
        if not body or is_hansard(rec["context"], body):
            continue
        urls = urls_in(body)
        if not urls:
            results.append({"line": rec["line"], "key": rec["key"],
                            "verdict": "NO URL IN CITATION"})
            continue
        res = check(rec["quote"], urls[0])
        results.append({"line": rec["line"], "key": rec["key"],
                        "quote": rec["quote"][:70], **res})
    return results


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("archive"); a.add_argument("urls", nargs="+")
    a.add_argument("--refetch", action="store_true")
    c = sub.add_parser("check"); c.add_argument("quote"); c.add_argument("url")
    c.add_argument("--refetch", action="store_true")
    w = sub.add_parser("wayback"); w.add_argument("pattern")
    w.add_argument("--limit", type=int, default=12)
    f = sub.add_parser("audit"); f.add_argument("file")
    f.add_argument("--sources")

    args = ap.parse_args()

    if args.cmd == "archive":
        for u in args.urls:
            try:
                e = archive(u, args.refetch)
                print(f"  {e['chars']:>7,} chars  {e['file']}  {u[:70]}")
            except Exception as exc:  # noqa: BLE001
                print(f"  FAILED  {u[:70]}: {str(exc)[:90]}")
    elif args.cmd == "check":
        print(json.dumps(check(args.quote, args.url, args.refetch), indent=1))
    elif args.cmd == "wayback":
        for s in wayback(args.pattern, args.limit):
            print(f"  {s['timestamp'][:8]}  {s['snapshot_url']}")
    else:
        rows = audit_file(args.file, args.sources)
        tally = {}
        for r in rows:
            tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
            flag = "" if r["verdict"].startswith("VERIFIED") else "  <<<"
            print(f"  L{r['line']:<5} {r['verdict']:<30} [^{r['key']}]{flag}")
        print("\nSummary:")
        for k, v in sorted(tally.items(), key=lambda x: -x[1]):
            print(f"  {k:34s} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
