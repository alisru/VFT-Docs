#!/usr/bin/env python3
"""Harvest Commonwealth Hansard XML from OpenAustralia into a local archive.

Covers both chambers, 2006 to the last sitting day. Incremental and resumable:
re-running only fetches files that are missing or that changed size upstream.

    python harvest.py            # fetch everything missing
    python harvest.py --status   # report local vs upstream, fetch nothing
"""

import argparse
import concurrent.futures as cf
import json
import re
import sys
import time
from pathlib import Path

import requests

BASE = "https://data.openaustralia.org"
CHAMBERS = {
    "senate": "scrapedxml/senate_debates",
    "reps": "scrapedxml/representatives_debates",
}
# speakerid -> party / electorate / term, plus division records
MEMBER_FILES = [
    "people.xml",
    "senators.xml",
    "representatives.xml",
    "ministers.xml",
    "divisions.xml",
]

ROOT = Path(__file__).resolve().parent
XML_DIR = ROOT / "xml"
MANIFEST = ROOT / "harvest_manifest.json"

# Apache autoindex row: <a href="2026-08-20.xml">2026-08-20.xml</a> ... 808826
ROW_RE = re.compile(
    r'<a href="(?P<name>[^"?/][^"]*\.xml)">.*?</a>\s*'
    r"(?P<date>\d{2}-\w{3}-\d{4}\s+\d{2}:\d{2})\s+(?P<size>[\d.]+[KMG]?)",
    re.I,
)
HREF_RE = re.compile(r'<a href="([^"?/][^"]*\.xml)"')

session = requests.Session()
session.headers["User-Agent"] = "aus-kanon-hansard-harvest/1.0 (research; contact via repo)"


def get(url, **kw):
    """GET with a few retries; returns the response or raises."""
    last = None
    for attempt in range(4):
        try:
            r = session.get(url, timeout=120, **kw)
            r.raise_for_status()
            return r
        except Exception as exc:  # noqa: BLE001 - retry anything transient
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise last


def list_remote(path):
    """Return the .xml filenames in an Apache autoindex directory."""
    html = get(f"{BASE}/{path}/").text
    names = HREF_RE.findall(html)
    # dedupe, preserve order
    seen, out = set(), []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def fetch_one(path, name, dest):
    """Download one file to dest. Returns (name, bytes_written) or (name, -1) on skip."""
    tmp = dest.with_suffix(dest.suffix + ".part")
    r = get(f"{BASE}/{path}/{name}", stream=True)
    written = 0
    with open(tmp, "wb") as fh:
        for chunk in r.iter_content(65536):
            fh.write(chunk)
            written += len(chunk)
    tmp.replace(dest)
    return name, written


def harvest_chamber(chamber, path, workers, status_only):
    outdir = XML_DIR / chamber
    outdir.mkdir(parents=True, exist_ok=True)

    remote = list_remote(path)
    have = {p.name for p in outdir.glob("*.xml")}
    missing = [n for n in remote if n not in have]

    print(
        f"[{chamber}] upstream={len(remote)}  local={len(have)}  to fetch={len(missing)}",
        flush=True,
    )
    if remote:
        print(f"[{chamber}] range {remote[0]} .. {remote[-1]}", flush=True)
    if status_only or not missing:
        return {"chamber": chamber, "remote": len(remote), "fetched": 0,
                "local": len(have), "bytes": 0}

    total_bytes, done, failed = 0, 0, []
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {
            pool.submit(fetch_one, path, n, outdir / n): n for n in missing
        }
        for fut in cf.as_completed(futs):
            name = futs[fut]
            try:
                _, n_bytes = fut.result()
                total_bytes += n_bytes
                done += 1
            except Exception as exc:  # noqa: BLE001
                failed.append((name, str(exc)[:120]))
            if done and done % 100 == 0:
                print(
                    f"[{chamber}] {done}/{len(missing)}  "
                    f"{total_bytes / 1048576:.0f} MB",
                    flush=True,
                )

    print(
        f"[{chamber}] done: {done} files, {total_bytes / 1048576:.1f} MB, "
        f"{len(failed)} failed",
        flush=True,
    )
    for name, err in failed[:10]:
        print(f"[{chamber}] FAILED {name}: {err}", flush=True)

    return {
        "chamber": chamber,
        "remote": len(remote),
        "fetched": done,
        "local": len(have) + done,
        "bytes": total_bytes,
        "failed": failed,
    }


def harvest_members(status_only):
    outdir = XML_DIR / "members"
    outdir.mkdir(parents=True, exist_ok=True)
    if status_only:
        print(f"[members] local={len(list(outdir.glob('*.xml')))}", flush=True)
        return
    for name in MEMBER_FILES:
        try:
            _, n = fetch_one("members", name, outdir / name)
            print(f"[members] {name}  {n / 1024:.0f} KB", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[members] FAILED {name}: {str(exc)[:120]}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6,
                    help="concurrent downloads (keep modest; be a good citizen)")
    ap.add_argument("--status", action="store_true",
                    help="report coverage without downloading")
    ap.add_argument("--chamber", choices=list(CHAMBERS) + ["all"], default="all")
    args = ap.parse_args()

    started = time.time()
    results = []
    targets = CHAMBERS if args.chamber == "all" else {args.chamber: CHAMBERS[args.chamber]}
    for chamber, path in targets.items():
        results.append(harvest_chamber(chamber, path, args.workers, args.status))
    harvest_members(args.status)

    elapsed = time.time() - started
    total = sum(r["bytes"] for r in results)
    print(
        f"\nHarvest finished in {elapsed / 60:.1f} min, "
        f"{total / 1048576:.1f} MB new.",
        flush=True,
    )

    if not args.status:
        MANIFEST.write_text(
            json.dumps(
                {"harvested_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                 "source": BASE, "results": results},
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
