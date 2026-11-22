"""Export Suite for Chat Context: single chat and bulk export in Markdown, JSON, HTML, TXT, and ZIP formats."""
import argparse
import datetime
import html
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from .db import ROOT, connect


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Sanitize string for safe filenames across OSes."""
    s = re.sub(r'[\\/*?:"<>|]', '_', name).strip()
    s = re.sub(r'\s+', ' ', s)
    s = s.strip('. ')
    return s[:max_len] or "untitled"


def format_timestamp(ts: Optional[str]) -> str:
    if not ts:
        return ""
    try:
        # If iso format, simplify to YYYY-MM-DD HH:MM
        clean = ts.replace('T', ' ').split('.')[0]
        return clean
    except Exception:
        return str(ts)


def chat_to_markdown(chat: Dict[str, Any]) -> str:
    """Convert chat object to high-fidelity Markdown with frontmatter."""
    cid = chat.get("id", "")
    title = chat.get("title") or "Untitled Chat"
    source = chat.get("source") or "gemini"
    url = chat.get("url") or ""
    topic = chat.get("topic_name") or "Unsorted"
    started = chat.get("started") or ""
    updated = chat.get("updated") or ""
    messages = chat.get("messages") or []
    canvases = chat.get("canvases") or []

    frontmatter = f"""---
id: "{cid}"
title: "{title.replace('"', chr(92) + '"')}"
source: "{source}"
url: "{url}"
topic: "{topic.replace('"', chr(92) + '"')}"
started: "{started}"
updated: "{updated}"
messages_count: {len(messages)}
canvases_count: {len(canvases)}
exported_at: "{datetime.datetime.now(datetime.timezone.utc).isoformat()}"
---

# {title}

- **Source:** {source.capitalize()}
- **Topic:** {topic}
- **Original URL:** {f'[{url}]({url})' if url else 'N/A'}
- **Started:** {format_timestamp(started)}
- **Updated:** {format_timestamp(updated)}
- **Messages:** {len(messages)}

"""
    if canvases:
        frontmatter += "## Attached Canvases\n\n"
        for cv in canvases:
            c_title = cv.get("title") or "Untitled Canvas"
            c_type = cv.get("type") or "markdown"
            frontmatter += f"- **Canvas: {c_title}** ({c_type})\n"
        frontmatter += "\n---\n\n"
    else:
        frontmatter += "---\n\n"

    blocks = []
    for m in messages:
        role = (m.get("role") or "assistant").capitalize()
        ts = format_timestamp(m.get("ts"))
        header = f"### {role}" + (f" ({ts})" if ts else "")
        text = (m.get("text") or "").strip()
        blocks.append(f"{header}\n\n{text}")

    body = "\n\n---\n\n".join(blocks)
    return frontmatter + body + "\n"


def chat_to_txt(chat: Dict[str, Any]) -> str:
    """Convert chat object to clean plain text."""
    title = chat.get("title") or "Untitled Chat"
    source = chat.get("source") or "gemini"
    url = chat.get("url") or ""
    topic = chat.get("topic_name") or "Unsorted"
    started = chat.get("started") or ""
    updated = chat.get("updated") or ""
    messages = chat.get("messages") or []

    out = [
        "=" * 70,
        f"TITLE: {title}",
        f"SOURCE: {source.upper()} | TOPIC: {topic}",
        f"URL: {url}",
        f"TIMESTAMPS: Started: {started} | Updated: {updated}",
        f"MESSAGES: {len(messages)}",
        "=" * 70,
        ""
    ]

    for m in messages:
        role = (m.get("role") or "assistant").upper()
        ts = format_timestamp(m.get("ts"))
        out.append(f"[{role}]" + (f" ({ts})" if ts else ""))
        out.append("-" * 40)
        out.append((m.get("text") or "").strip())
        out.append("")
        out.append("")

    return "\n".join(out)


def chat_to_html(chat: Dict[str, Any]) -> str:
    """Convert chat object to a beautiful, standalone dark-mode HTML document."""
    title = html.escape(chat.get("title") or "Untitled Chat")
    source = html.escape((chat.get("source") or "gemini").capitalize())
    url = chat.get("url") or ""
    topic = html.escape(chat.get("topic_name") or "Unsorted")
    started = format_timestamp(chat.get("started"))
    updated = format_timestamp(chat.get("updated"))
    messages = chat.get("messages") or []
    canvases = chat.get("canvases") or []

    msgs_html = []
    for m in messages:
        role = (m.get("role") or "assistant").lower()
        role_label = "You" if role == "user" else ("Assistant" if role == "assistant" else role.capitalize())
        ts = format_timestamp(m.get("ts"))
        raw_text = m.get("text") or ""
        escaped_text = html.escape(raw_text)

        # Highlight code blocks
        escaped_text = re.sub(
            r'```([a-zA-Z0-9_-]*)\n(.*?)```',
            r'<pre class="code-block"><code class="lang-\1">\2</code></pre>',
            escaped_text,
            flags=re.DOTALL
        )

        msgs_html.append(f"""
        <div class="message-card {role}">
          <div class="message-meta">
            <span class="role-badge {role}">{role_label}</span>
            {f'<span class="timestamp">{html.escape(ts)}</span>' if ts else ''}
          </div>
          <div class="message-body">{escaped_text}</div>
        </div>
        """)

    canvases_html = ""
    if canvases:
        cv_items = []
        for cv in canvases:
            c_title = html.escape(cv.get("title") or "Untitled Canvas")
            c_type = html.escape(cv.get("type") or "markdown")
            c_content = html.escape(cv.get("content") or "")
            cv_items.append(f"""
            <details class="canvas-item">
              <summary><strong>{c_title}</strong> <span class="badge">{c_type}</span></summary>
              <pre class="canvas-content"><code>{c_content}</code></pre>
            </details>
            """)
        canvases_html = f"""
        <section class="canvases-section">
          <h3>Attached Canvases ({len(canvases)})</h3>
          {"".join(cv_items)}
        </section>
        """

    url_html = f'<p><a href="{html.escape(url)}" target="_blank" rel="noreferrer" class="web-link">🔗 Open Original Conversation</a></p>' if url else ''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Chat Context Export</title>
<style>
  :root {{
    --bg: #0d1117;
    --card-bg: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --dim: #8b949e;
    --user-bg: #1f293d;
    --user-border: #38bdf8;
    --assistant-bg: #161b22;
    --assistant-border: #30363d;
    --acc: #38bdf8;
  }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    margin: 0;
    padding: 24px 16px;
    line-height: 1.6;
    display: flex;
    justify-content: center;
  }}
  .container {{
    max-width: 860px;
    width: 100%;
  }}
  header {{
    border-bottom: 1px solid var(--border);
    padding-bottom: 20px;
    margin-bottom: 24px;
  }}
  h1 {{
    margin: 0 0 10px 0;
    font-size: 24px;
    color: #f0f6fc;
  }}
  .meta-bar {{
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    font-size: 13px;
    color: var(--dim);
  }}
  .web-link {{
    color: var(--acc);
    text-decoration: none;
    font-size: 13px;
  }}
  .web-link:hover {{ text-decoration: underline; }}
  .canvases-section {{
    background: #111620;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 24px;
  }}
  .canvases-section h3 {{ margin-top: 0; font-size: 16px; }}
  .canvas-item {{ margin-bottom: 10px; cursor: pointer; }}
  .canvas-content {{
    background: #090d13;
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 12px;
    white-space: pre-wrap;
  }}
  .message-card {{
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 18px;
    border: 1px solid var(--border);
    background: var(--card-bg);
  }}
  .message-card.user {{
    background: var(--user-bg);
    border-color: #2e4466;
  }}
  .message-meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }}
  .role-badge {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 2px 8px;
    border-radius: 4px;
  }}
  .role-badge.user {{ background: #0369a1; color: #f0f9ff; }}
  .role-badge.assistant {{ background: #232d3d; color: #94a3b8; }}
  .timestamp {{ font-size: 11px; color: var(--dim); }}
  .message-body {{
    font-size: 14.5px;
    white-space: pre-wrap;
    word-break: break-word;
  }}
  pre.code-block {{
    background: #090d13;
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 12px;
    overflow-x: auto;
    font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
    font-size: 13px;
  }}
  @media print {{
    body {{ background: #fff; color: #000; }}
    .message-card {{ border: 1px solid #ccc; background: #fafafa; page-break-inside: avoid; }}
    .message-card.user {{ background: #f0f4f8; }}
    pre.code-block {{ background: #eee; border: 1px solid #ccc; }}
  }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>{title}</h1>
    <div class="meta-bar">
      <span><strong>Source:</strong> {source}</span>
      <span><strong>Topic:</strong> {topic}</span>
      {f'<span><strong>Started:</strong> {started}</span>' if started else ''}
      {f'<span><strong>Updated:</strong> {updated}</span>' if updated else ''}
      <span><strong>Turns:</strong> {len(messages)}</span>
    </div>
    {url_html}
  </header>
  {canvases_html}
  <main>
    {"".join(msgs_html)}
  </main>
</div>
</body>
</html>
"""


def fetch_full_chat(con, chat_id: str) -> Optional[Dict[str, Any]]:
    """Fetch complete chat record with topic name, messages, and canvases."""
    row = con.execute(
        """SELECT c.id, c.title, c.source, c.started, c.updated, c.url, c.topic_id,
                  t.name as topic_name
           FROM chats c
           LEFT JOIN topics t ON c.topic_id = t.id
           WHERE c.id = ?""",
        (chat_id,)
    ).fetchone()

    if not row:
        return None

    c = dict(row)
    c["messages"] = [
        dict(r)
        for r in con.execute(
            "SELECT idx, role, ts, text FROM messages WHERE chat_id=? ORDER BY idx", (chat_id,)
        ).fetchall()
    ]
    c["canvases"] = [
        dict(r)
        for r in con.execute(
            "SELECT id, title, type, file_path, updated, content FROM canvases WHERE chat_id=? ORDER BY updated DESC",
            (chat_id,)
        ).fetchall()
    ]
    return c


def fetch_all_chats(con, chat_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Fetch multiple full chat records (or all chats if chat_ids is None)."""
    if chat_ids:
        placeholders = ",".join("?" for _ in chat_ids)
        rows = con.execute(
            f"""SELECT c.id, c.title, c.source, c.started, c.updated, c.url, c.topic_id,
                       t.name as topic_name
                FROM chats c
                LEFT JOIN topics t ON c.topic_id = t.id
                WHERE c.id IN ({placeholders})
                ORDER BY COALESCE(c.updated, datetime(c.src_mtime, 'unixepoch'), c.started) DESC""",
            tuple(chat_ids)
        ).fetchall()
    else:
        rows = con.execute(
            """SELECT c.id, c.title, c.source, c.started, c.updated, c.url, c.topic_id,
                      t.name as topic_name
               FROM chats c
               LEFT JOIN topics t ON c.topic_id = t.id
               ORDER BY COALESCE(c.updated, datetime(c.src_mtime, 'unixepoch'), c.started) DESC"""
        ).fetchall()

    result = []
    for r in rows:
        c = dict(r)
        cid = c["id"]
        c["messages"] = [
            dict(m)
            for m in con.execute(
                "SELECT idx, role, ts, text FROM messages WHERE chat_id=? ORDER BY idx", (cid,)
            ).fetchall()
        ]
        c["canvases"] = [
            dict(cv)
            for cv in con.execute(
                "SELECT id, title, type, file_path, updated, content FROM canvases WHERE chat_id=? ORDER BY updated DESC",
                (cid,)
            ).fetchall()
        ]
        result.append(c)
    return result


def export_chats_to_zip(
    chats: List[Dict[str, Any]],
    format_type: str = "markdown",
    group_by_topic: bool = True
) -> bytes:
    """Pack chats into an in-memory ZIP archive with topic subfolders and manifest."""
    buf = io.BytesIO()
    seen_paths = set()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        manifest_entries = []
        ext = "md" if format_type == "markdown" else ("html" if format_type == "html" else ("json" if format_type == "json" else "txt"))

        for c in chats:
            topic_folder = sanitize_filename(c.get("topic_name") or "Unsorted", max_len=50) if group_by_topic else ""
            base_filename = sanitize_filename(c.get("title") or c.get("id") or "chat", max_len=60)
            cid = c.get("id") or "unknown"
            filename = f"{base_filename}_{cid[:8]}.{ext}"

            archive_path = f"{topic_folder}/{filename}" if topic_folder else filename
            counter = 2
            while archive_path in seen_paths:
                archive_path = f"{topic_folder}/{base_filename}_{cid[:8]}_{counter}.{ext}" if topic_folder else f"{base_filename}_{cid[:8]}_{counter}.{ext}"
                counter += 1
            seen_paths.add(archive_path)

            if format_type == "markdown":
                content = chat_to_markdown(c)
            elif format_type == "html":
                content = chat_to_html(c)
            elif format_type == "json":
                content = json.dumps(c, ensure_ascii=False, indent=2)
            else:
                content = chat_to_txt(c)

            zf.writestr(archive_path, content.encode("utf-8"))

            # Also export attached canvases into a canvases subfolder if markdown/html
            if c.get("canvases"):
                cv_folder = f"{topic_folder}/canvases" if topic_folder else "canvases"
                for cv in c["canvases"]:
                    c_title = sanitize_filename(cv.get("title") or "canvas", max_len=50)
                    cv_path = f"{cv_folder}/{c_title}_{cid[:6]}.md"
                    cv_counter = 2
                    while cv_path in seen_paths:
                        cv_path = f"{cv_folder}/{c_title}_{cid[:6]}_{cv_counter}.md"
                        cv_counter += 1
                    seen_paths.add(cv_path)
                    zf.writestr(cv_path, (cv.get("content") or "").encode("utf-8"))

            manifest_entries.append({
                "id": c.get("id"),
                "title": c.get("title"),
                "source": c.get("source"),
                "topic": c.get("topic_name") or "Unsorted",
                "messages_count": len(c.get("messages") or []),
                "canvases_count": len(c.get("canvases") or []),
                "file": archive_path
            })

        # Add manifest.json and README.md to archive root
        manifest_doc = {
            "exported_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "total_chats": len(chats),
            "format": format_type,
            "chats": manifest_entries
        }
        zf.writestr("manifest.json", json.dumps(manifest_doc, indent=2).encode("utf-8"))

        readme_doc = f"""# Chat Context Bulk Export

- **Exported At:** {datetime.datetime.now(datetime.timezone.utc).isoformat()}
- **Total Conversations:** {len(chats)}
- **Format:** {format_type.upper()}
- **Structure:** {'Grouped by Topic folders' if group_by_topic else 'Flat directory'}

Inspect `manifest.json` for a machine-readable directory of all chats in this archive.
"""
        zf.writestr("README.md", readme_doc.encode("utf-8"))

    return buf.getvalue()


def export_all_to_directory(dest_dir: Path, by_topic: bool = True) -> int:
    """Exports all chats from SQLite to a clean directory of Markdown files."""
    con = connect()
    try:
        chats = fetch_all_chats(con)
    finally:
        con.close()

    dest_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for c in chats:
        topic_name = sanitize_filename(c.get("topic_name") or "Unsorted")
        target_dir = dest_dir / topic_name if by_topic else dest_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        fname = f"{sanitize_filename(c.get('title') or c['id'])}_{c['id'][:8]}.md"
        target_file = target_dir / fname
        target_file.write_text(chat_to_markdown(c), encoding="utf-8")
        count += 1
    return count


def sync_chats_to_gdrive(source_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Exports all chats to Markdown and syncs them to Google Drive via rclone."""
    import subprocess
    from .config import get_chat_gdrive_config

    cfg = get_chat_gdrive_config()
    export_rel = cfg.get("export_dir", "exports/chats")
    target_dir = source_dir or (ROOT / export_rel)
    count = export_all_to_directory(target_dir, by_topic=True)

    rclone_remote = cfg.get("rclone_remote", "gdrive").strip(":")
    folder_name = cfg.get("folder_name", "AI_Chats").strip("/")
    target_dest = f"{rclone_remote}:{folder_name}"
    root_folder_id = cfg.get("root_folder_id", "").strip()

    cmd = [
        "rclone", "copy", str(target_dir), target_dest,
        "--tpslimit", "5", "--contimeout", "15s", "--timeout", "120s"
    ]
    if root_folder_id:
        cmd.extend(["--drive-root-folder-id", root_folder_id])

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if res.returncode == 0:
            return {
                "ok": True,
                "count": count,
                "dest": target_dest,
                "message": f"Successfully exported {count} chats and synced to Google Drive ({target_dest})"
            }
        else:
            return {
                "ok": False,
                "count": count,
                "error": res.stderr.strip() or "rclone returned non-zero exit code",
                "message": f"Exported {count} chats locally, but Google Drive sync failed: {res.stderr.strip()}"
            }
    except FileNotFoundError:
        return {
            "ok": False,
            "count": count,
            "error": "rclone CLI not found on system PATH",
            "message": f"Exported {count} chats to '{target_dir}', but rclone is not installed to sync to Google Drive."
        }
    except Exception as e:
        return {
            "ok": False,
            "count": count,
            "error": str(e),
            "message": f"Export error: {e}"
        }


def sync_chats_to_git(repo_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Exports all chats to Markdown, commits them to a local git repo, and pushes to remote."""
    import subprocess
    from .config import get_chat_git_config

    cfg = get_chat_git_config()
    export_rel = cfg.get("export_dir", "exports/chats")
    target_dir = repo_dir or (ROOT / export_rel)
    count = export_all_to_directory(target_dir, by_topic=True)

    git_remote = cfg.get("remote", "origin")
    git_branch = cfg.get("branch", "main")

    if not (target_dir / ".git").exists():
        repo_url = cfg.get("repo_url", "").strip()
        if not repo_url:
            return {
                "ok": False,
                "count": count,
                "error": "Git repository not initialized and no repo_url configured",
                "message": f"Exported {count} chats to '{target_dir}'. Configure repo_url in config.json or run 'python setup_sync.py' to initialize Git."
            }
        try:
            subprocess.run(["git", "init", "-b", git_branch], cwd=target_dir, check=True)
            subprocess.run(["git", "remote", "add", git_remote, repo_url], cwd=target_dir, check=True)
        except Exception as err:
            return {
                "ok": False,
                "count": count,
                "error": str(err),
                "message": f"Failed to initialize Git in {target_dir}: {err}"
            }

    try:
        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=target_dir,
            capture_output=True,
            text=True,
            timeout=15
        )
        has_changes = bool(status_res.stdout.strip())
        if has_changes:
            subprocess.run(["git", "add", "."], cwd=target_dir, check=True, timeout=20)
            now_label = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            commit_msg = f"auto(chats): sync {count} conversations ({now_label})"
            commit_res = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=target_dir,
                capture_output=True,
                text=True,
                timeout=20
            )
            if commit_res.returncode == 0:
                push_res = subprocess.run(
                    ["git", "push", git_remote, git_branch],
                    cwd=target_dir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if push_res.returncode == 0:
                    return {
                        "ok": True,
                        "count": count,
                        "committed": True,
                        "pushed": True,
                        "message": f"Successfully exported {count} chats, committed, and pushed to {git_remote}/{git_branch}"
                    }
                else:
                    return {
                        "ok": False,
                        "count": count,
                        "committed": True,
                        "pushed": False,
                        "error": push_res.stderr.strip(),
                        "message": f"Committed {count} chats locally, but git push failed: {push_res.stderr.strip()}"
                    }
            else:
                return {
                    "ok": False,
                    "count": count,
                    "error": commit_res.stderr.strip(),
                    "message": f"Git commit failed: {commit_res.stderr.strip()}"
                }
        else:
            return {
                "ok": True,
                "count": count,
                "committed": False,
                "pushed": False,
                "message": f"All {count} chats are already up-to-date in Git. Working tree clean."
            }
    except FileNotFoundError:
        return {
            "ok": False,
            "count": count,
            "error": "git CLI not found on system PATH",
            "message": f"Exported {count} chats to '{target_dir}', but git is not installed to push."
        }
    except Exception as e:
        return {
            "ok": False,
            "count": count,
            "error": str(e),
            "message": f"Git sync error: {e}"
        }


def cli_main():
    """CLI runner for chat exporting."""
    parser = argparse.ArgumentParser(description="Export Chat Context conversations.")
    parser.add_argument("--chat", type=str, help="Specific chat ID to export.")
    parser.add_argument("--all", action="store_true", help="Export all chats in the database.")
    parser.add_argument("--format", type=str, choices=["markdown", "json", "html", "txt", "zip"], default="markdown", help="Export format.")
    parser.add_argument("--out", type=str, default="./exports", help="Output directory or target zip file.")
    parser.add_argument("--flat", action="store_true", help="Do not group into topic subfolders.")
    parser.add_argument("--sync-git", action="store_true", help="Export all chats and sync/push to configured Git repository.")
    parser.add_argument("--sync-gdrive", action="store_true", help="Export all chats and sync to configured Google Drive folder via rclone.")

    args = parser.parse_args()

    if args.sync_git:
        print("Exporting chats and pushing to Git...")
        res = sync_chats_to_git()
        print(res.get("message"))
        sys.exit(0 if res.get("ok") else 1)

    if args.sync_gdrive:
        print("Exporting chats and syncing to Google Drive...")
        res = sync_chats_to_gdrive()
        print(res.get("message"))
        sys.exit(0 if res.get("ok") else 1)

    con = connect()
    out_path = Path(args.out)

    if args.chat:
        c = fetch_full_chat(con, args.chat)
        if not c:
            print(f"Error: Chat '{args.chat}' not found.")
            sys.exit(1)

        out_path.mkdir(parents=True, exist_ok=True)
        fname = sanitize_filename(c.get("title") or c["id"])
        if args.format == "markdown":
            p = out_path / f"{fname}.md"
            p.write_text(chat_to_markdown(c), encoding="utf-8")
        elif args.format == "html":
            p = out_path / f"{fname}.html"
            p.write_text(chat_to_html(c), encoding="utf-8")
        elif args.format == "json":
            p = out_path / f"{fname}.json"
            p.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
        elif args.format == "txt":
            p = out_path / f"{fname}.txt"
            p.write_text(chat_to_txt(c), encoding="utf-8")
        elif args.format == "zip":
            p = out_path / f"{fname}.zip"
            p.write_bytes(export_chats_to_zip([c], format_type="markdown", group_by_topic=False))

        print(f"Successfully exported 1 chat to: {p.resolve()}")

    elif args.all:
        chats = fetch_all_chats(con)
        print(f"Found {len(chats)} chats in database.")

        if args.format == "zip" or out_path.suffix.lower() == ".zip":
            target_zip = out_path if out_path.suffix.lower() == ".zip" else out_path / f"chat_context_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            target_zip.parent.mkdir(parents=True, exist_ok=True)
            data = export_chats_to_zip(chats, format_type="markdown", group_by_topic=not args.flat)
            target_zip.write_bytes(data)
            print(f"Successfully exported {len(chats)} chats to ZIP: {target_zip.resolve()}")

        elif args.format == "json":
            out_path.parent.mkdir(parents=True, exist_ok=True)
            target_file = out_path if out_path.suffix.lower() == ".json" else out_path / "all_chats.json"
            target_file.write_text(json.dumps(chats, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Successfully exported {len(chats)} chats to JSON: {target_file.resolve()}")

        else:
            # Multi-file directory export
            out_path.mkdir(parents=True, exist_ok=True)
            ext = "md" if args.format == "markdown" else ("html" if args.format == "html" else "txt")
            for c in chats:
                topic_dir = out_path / (sanitize_filename(c.get("topic_name") or "Unsorted") if not args.flat else "")
                topic_dir.mkdir(parents=True, exist_ok=True)
                fname = f"{sanitize_filename(c.get('title') or c['id'])}_{c['id'][:8]}.{ext}"
                target_file = topic_dir / fname

                if args.format == "markdown":
                    target_file.write_text(chat_to_markdown(c), encoding="utf-8")
                elif args.format == "html":
                    target_file.write_text(chat_to_html(c), encoding="utf-8")
                else:
                    target_file.write_text(chat_to_txt(c), encoding="utf-8")

            print(f"Successfully exported {len(chats)} files to directory: {out_path.resolve()}")

    else:
        parser.print_help()


if __name__ == "__main__":
    cli_main()

