#!/usr/bin/env python3
import sys
import sqlite3
import datetime
import argparse

DB_PATH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
VALID_STATUSES = {"verified", "paraphrased", "fabricated", "needs_hansard", "no_citation", "unchecked"}


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def cmd_list(conn, args):
    q = "SELECT node_id, plane, address, vector_name, status, fuzzy_score, citation_key FROM nodes WHERE 1=1"
    params = []
    if args.status:
        q += " AND status=?"
        params.append(args.status)
    if args.plane:
        q += " AND plane=?"
        params.append(args.plane)
    if args.citation:
        q += " AND citation_key=?"
        params.append(args.citation)
    q += " ORDER BY plane, address"
    cur = conn.execute(q, params)
    rows = cur.fetchall()
    print(f"{'id':>4} {'pl':>2} {'address':18} {'vector_name':28} {'status':13} {'score':>6} citation")
    for r in rows:
        node_id, plane, address, name, status, score, key = r
        score_s = f"{score:.2f}" if score is not None else "  -  "
        print(f"{node_id:>4} {plane:>2} {address:18} {name[:28]:28} {status:13} {score_s:>6} {key or ''}")
    print(f"\n{len(rows)} rows")


def cmd_show(conn, args):
    cur = conn.execute("SELECT * FROM nodes WHERE node_id=?", (args.node_id,))
    row = cur.fetchone()
    if not row:
        print("no such node_id")
        return
    cols = [d[0] for d in cur.description]
    for c, v in zip(cols, row):
        print(f"{c:16} {v}")


def cmd_update(conn, args):
    if args.status and args.status not in VALID_STATUSES:
        print(f"invalid status, must be one of {VALID_STATUSES}")
        sys.exit(1)
    cur = conn.execute("SELECT status FROM nodes WHERE node_id=?", (args.node_id,))
    row = cur.fetchone()
    if not row:
        print("no such node_id")
        return
    old_status = row[0]

    sets, params = [], []
    if args.status:
        sets.append("status=?")
        params.append(args.status)
    if args.verified_quote is not None:
        sets.append("verified_quote=?")
        params.append(args.verified_quote)
    if args.notes is not None:
        sets.append("notes=?")
        params.append(args.notes)
    sets.append("last_checked=?")
    params.append(now())
    params.append(args.node_id)

    conn.execute(f"UPDATE nodes SET {', '.join(sets)} WHERE node_id=?", params)
    if args.status and args.status != old_status:
        conn.execute(
            "INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at) "
            "VALUES (?,?,?,?,?,?)",
            (args.node_id, old_status, args.status, "manual", args.notes or "", now()),
        )
    conn.commit()
    print(f"node {args.node_id}: {old_status} -> {args.status or old_status}")


def cmd_history(conn, args):
    cur = conn.execute(
        "SELECT changed_at, old_status, new_status, changed_by, note FROM status_history "
        "WHERE node_id=? ORDER BY changed_at",
        (args.node_id,),
    )
    for changed_at, old, new, by, note in cur.fetchall():
        print(f"{changed_at}  {old or '(new)':12} -> {new:12}  [{by}]  {note}")


def cmd_report(conn, args):
    print("=== by status ===")
    for status, n in conn.execute("SELECT status, COUNT(*) as n FROM nodes GROUP BY status ORDER BY n DESC"):
        print(f"  {status:15} {n}")
    print("\n=== by plane / status ===")
    cur = conn.execute(
        "SELECT plane, status, COUNT(*) FROM nodes GROUP BY plane, status ORDER BY plane, status"
    )
    rows = cur.fetchall()
    planes = sorted(set(r[0] for r in rows))
    statuses = sorted(set(r[1] for r in rows))
    grid = {(p, s): 0 for p in planes for s in statuses}
    for p, s, n in rows:
        grid[(p, s)] = n
    header = "plane  " + "  ".join(f"{s:12}" for s in statuses)
    print(header)
    for p in planes:
        print(f"{p:5}  " + "  ".join(f"{grid[(p,s)]:12}" for s in statuses))
    print("\n=== nodes needing attention (fabricated) ===")
    cur = conn.execute(
        "SELECT node_id, plane, address, vector_name, citation_key, fuzzy_score FROM nodes "
        "WHERE status='fabricated' ORDER BY plane, address"
    )
    for node_id, plane, address, name, key, score in cur.fetchall():
        print(f"  [{node_id}] P{plane} {address:18} {name:28} cite=[^{key}] score={score:.2f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--status")
    p_list.add_argument("--plane", type=int)
    p_list.add_argument("--citation")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show")
    p_show.add_argument("node_id", type=int)
    p_show.set_defaults(func=cmd_show)

    p_update = sub.add_parser("update")
    p_update.add_argument("node_id", type=int)
    p_update.add_argument("--status")
    p_update.add_argument("--verified-quote", dest="verified_quote")
    p_update.add_argument("--notes")
    p_update.set_defaults(func=cmd_update)

    p_hist = sub.add_parser("history")
    p_hist.add_argument("node_id", type=int)
    p_hist.set_defaults(func=cmd_history)

    p_report = sub.add_parser("report")
    p_report.set_defaults(func=cmd_report)

    args = ap.parse_args()
    conn = sqlite3.connect(DB_PATH)
    args.func(conn, args)
    conn.close()


if __name__ == "__main__":
    main()
