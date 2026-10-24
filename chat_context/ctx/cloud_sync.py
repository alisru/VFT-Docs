"""
Background debounced cloud sync worker for Canvases:
1. Git: commits and pushes chat_context/canvases/ to configured remote/branch.
2. Google Drive: copies chat_context/canvases/ to configured rclone remote as native Google Docs.
Settings are loaded dynamically from config.json via ctx.config.
"""
import re
import subprocess
import threading
import time
from pathlib import Path

from .config import get_git_config, get_gdrive_config
from .db import CANVASES_DIR, ROOT

SYNC_DELAY = 30  # seconds to wait after last canvas edit before pushing
GDOCS_STAGING_DIR = ROOT / "drawing_board" / "gdocs_staging"


def prepare_gdocs_staging():
    """Converts updated .md canvases into clean .docx files for Google Docs import, pruning deleted/renamed ones."""
    GDOCS_STAGING_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Clean up stale staging docx files whose corresponding markdown canvas no longer exists
    current_docx_targets = set()
    for md_file in CANVASES_DIR.rglob("*.md"):
        rel = md_file.relative_to(CANVASES_DIR)
        current_docx_targets.add((GDOCS_STAGING_DIR / rel.parent / (rel.stem + ".docx")).resolve())

    for existing_docx in GDOCS_STAGING_DIR.rglob("*.docx"):
        if existing_docx.resolve() not in current_docx_targets:
            try:
                existing_docx.unlink(missing_ok=True)
            except Exception as err:
                print(f"[canvas-sync] Note: could not remove stale staging docx {existing_docx.name}: {err}", flush=True)

    # 2. Convert markdown to docx for updated canvases
    for md_file in CANVASES_DIR.rglob("*.md"):
        rel = md_file.relative_to(CANVASES_DIR)
        docx_file = GDOCS_STAGING_DIR / rel.parent / (rel.stem + ".docx")
        if docx_file.exists() and docx_file.stat().st_mtime >= md_file.stat().st_mtime:
            continue
        docx_file.parent.mkdir(parents=True, exist_ok=True)
        raw_text = md_file.read_text(encoding="utf-8", errors="replace")
        clean_text = re.sub(r"^---\s*\n.*?\n---\s*\n+", "", raw_text, flags=re.S) if raw_text.startswith("---") else raw_text
        try:
            p = subprocess.Popen(
                ["pandoc", "-f", "markdown", "-t", "docx", "-o", str(docx_file)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )
            p.communicate(input=clean_text, timeout=20)
        except FileNotFoundError:
            print("[canvas-sync] Note: 'pandoc' not found on system PATH. Install pandoc for native Google Docs conversion.", flush=True)
            break
        except Exception as err:
            print(f"[canvas-sync] Pandoc conversion error for {md_file.name}: {err}", flush=True)


class CanvasCloudSync:
    def __init__(self):
        self._timer = None
        self._lock = threading.Lock()
        self._changed_titles = set()
        self._changed_paths = set()
        self._pending_titles = set()
        self._pending_paths = set()
        self._is_syncing = False
        self.last_sync_time = None
        self.last_sync_status = "idle"

    def add_change(self, canvas_title: str, rel_path: str = ""):
        """Register a changed canvas without starting a debounced timer."""
        with self._lock:
            self._changed_titles.add(canvas_title)
            if rel_path:
                self._changed_paths.add(rel_path)

    def notify_change(self, canvas_title: str, rel_path: str = ""):
        """Called whenever a canvas file is written or updated on disk."""
        with self._lock:
            self._changed_titles.add(canvas_title)
            if rel_path:
                self._changed_paths.add(rel_path)
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(SYNC_DELAY, self._on_timer)
            self._timer.daemon = True
            self._timer.start()
            print(f"[canvas-sync] Scheduled auto-sync in {SYNC_DELAY}s for '{canvas_title}'", flush=True)

    def trigger_immediate(self):
        """Triggers an immediate sync, cancelling any pending debounced timer."""
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
            titles = list(self._changed_titles)
            paths = list(self._changed_paths)
            self._changed_titles.clear()
            self._changed_paths.clear()

        if titles or paths:
            threading.Thread(target=self._run_sync, args=(titles, paths), daemon=True).start()

    def _on_timer(self):
        with self._lock:
            titles = list(self._changed_titles)
            paths = list(self._changed_paths)
            self._changed_titles.clear()
            self._changed_paths.clear()
            self._timer = None

        if titles or paths:
            threading.Thread(target=self._run_sync, args=(titles, paths), daemon=True).start()

    def _run_sync(self, titles, paths=None):
        with self._lock:
            if self._is_syncing:
                self._pending_titles.update(titles or [])
                if paths:
                    self._pending_paths.update(paths)
                print(f"[canvas-sync] Sync already in progress, queued {len(titles or [])} canvas(es) for follow-up", flush=True)
                return
            self._is_syncing = True

        self.last_sync_status = "syncing"
        print(f"[canvas-sync] Starting sync for: {titles or 'all canvases'}", flush=True)

        git_ok = True
        gdrive_ok = True

        try:
            git_cfg = get_git_config()
            gdrive_cfg = get_gdrive_config()

            # --- 1. Git Auto-Commit and Push ---
            if git_cfg.get("enabled", False):
                git_remote = git_cfg.get("remote", "origin")
                git_branch = git_cfg.get("branch", "main")
                if not (CANVASES_DIR / ".git").exists():
                    print("[canvas-sync] Git sync is enabled, but canvases/ is not a git repo. Run 'python setup_sync.py' to initialize.", flush=True)
                    git_ok = False
                else:
                    try:
                        status_res = subprocess.run(
                            ["git", "status", "--porcelain"],
                            cwd=CANVASES_DIR,
                            capture_output=True,
                            text=True,
                            timeout=15,
                        )
                        has_changes = bool(status_res.stdout.strip())
                        if has_changes:
                            subprocess.run(
                                ["git", "add", "."],
                                cwd=CANVASES_DIR,
                                check=True,
                                timeout=15,
                            )
                            if titles:
                                title_summary = titles[0] if len(titles) == 1 else f"{len(titles)} canvases ({', '.join(titles[:2])})"
                                commit_msg = f"auto(canvas): update {title_summary}"
                            else:
                                commit_msg = "auto(canvas): sync canvases"

                            commit_res = subprocess.run(
                                ["git", "commit", "-m", commit_msg],
                                cwd=CANVASES_DIR,
                                capture_output=True,
                                text=True,
                                timeout=20,
                            )
                            if commit_res.returncode == 0:
                                print(f"[canvas-sync] Git committed: {commit_msg}", flush=True)
                                push_res = subprocess.run(
                                    ["git", "push", git_remote, git_branch],
                                    cwd=CANVASES_DIR,
                                    capture_output=True,
                                    text=True,
                                    timeout=45,
                                    )
                                if push_res.returncode == 0:
                                    print(f"[canvas-sync] Git pushed to {git_remote}/{git_branch} successfully", flush=True)
                                    git_ok = True
                                else:
                                    print(f"[canvas-sync] Git push failed: {push_res.stderr.strip()}", flush=True)
                                    git_ok = False
                            else:
                                print(f"[canvas-sync] Git commit note: {commit_res.stdout.strip() or commit_res.stderr.strip()}", flush=True)
                        else:
                            print(f"[canvas-sync] Git: working tree clean for {git_remote}/{git_branch}, nothing to commit", flush=True)
                            git_ok = True
                    except FileNotFoundError:
                        print("[canvas-sync] Git CLI not found on system PATH. Install git or run 'python setup_sync.py'.", flush=True)
                        git_ok = False
                    except Exception as e:
                        print(f"[canvas-sync] Git error: {e}", flush=True)
                        git_ok = False
            else:
                print("[canvas-sync] Git sync is disabled in config.json. Skipping.", flush=True)

            # --- 2. Google Drive Sync as Native Google Docs (ONLY changed files) ---
            if gdrive_cfg.get("enabled", False):
                if CANVASES_DIR.exists():
                    rclone_remote = gdrive_cfg.get("rclone_remote", "gdrive").strip(":")
                    folder_name = gdrive_cfg.get("folder_name", "Canvases").strip("/")
                    target_dest = f"{rclone_remote}:{folder_name}"
                    root_folder_id = gdrive_cfg.get("root_folder_id", "").strip()

                    # If specific file paths were changed, convert and upload only those specific files
                    target_paths = paths or []
                    if target_paths:
                        GDOCS_STAGING_DIR.mkdir(parents=True, exist_ok=True)
                        files_to_sync = []
                        for rel_p in target_paths:
                            md_file = CANVASES_DIR / rel_p
                            if not md_file.exists():
                                continue
                            rel = md_file.relative_to(CANVASES_DIR)
                            docx_file = GDOCS_STAGING_DIR / rel.parent / (rel.stem + ".docx")
                            docx_file.parent.mkdir(parents=True, exist_ok=True)
                            raw_text = md_file.read_text(encoding="utf-8", errors="replace")
                            clean_text = re.sub(r"^---\s*\n.*?\n---\s*\n+", "", raw_text, flags=re.S) if raw_text.startswith("---") else raw_text
                            # Extract authentic metadata title: check .meta.json sidecar first
                            real_title = ""
                            meta_file = md_file.with_name(md_file.stem + ".meta.json")
                            if meta_file.exists():
                                try:
                                    meta_data = json.loads(meta_file.read_text(encoding="utf-8"))
                                    real_title = (meta_data.get("title") or "").strip()
                                except Exception:
                                    pass

                            # Fallback to legacy frontmatter if sidecar not present
                            if not real_title:
                                fm = re.search(r"^---\s*\n(.*?)\n---", raw_text, flags=re.S)
                                if fm:
                                    tm = re.search(r"^title:\s*[\"']?(.*?)[\"']?$", fm.group(1), flags=re.M)
                                    if tm:
                                        real_title = tm.group(1).strip()
                            if not real_title:
                                real_title = rel.stem

                            try:
                                p = subprocess.Popen(
                                    ["pandoc", "-f", "markdown", "-t", "docx", "-o", str(docx_file)],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    encoding="utf-8",
                                )
                                p.communicate(input=clean_text, timeout=20)
                                files_to_sync.append((docx_file, real_title))
                            except Exception as err:
                                print(f"[canvas-sync] Pandoc conversion error for {md_file.name}: {err}", flush=True)

                        for d_file, real_title in files_to_sync:
                            rel_in_staging = d_file.relative_to(GDOCS_STAGING_DIR)
                            folder_part = rel_in_staging.parent.as_posix() if rel_in_staging.parent.name else ""
                            file_dest = f"{target_dest}/{folder_part}" if folder_part else target_dest
                            
                            # Google Drive supports colons, slashes, and full punctuation in doc names
                            gdrive_filename = f"{real_title}.docx" if real_title else d_file.name
                            # Only sanitize slashes so rclone does not treat them as nested directories
                            safe_gdrive_filename = gdrive_filename.replace("/", " ∕ ").replace("\\", " ∖ ")
                            target_remote_file = f"{file_dest}/{safe_gdrive_filename}"

                            cmd = [
                                "rclone",
                                "copyto",
                                str(d_file),
                                target_remote_file,
                                "--drive-import-formats",
                                "docx",
                                "--contimeout",
                                "15s",
                                "--timeout",
                                "60s",
                                "--retries",
                                "2",
                                "--low-level-retries",
                                "3",
                                "--tpslimit",
                                "5",
                            ]
                            if root_folder_id:
                                cmd.extend(["--drive-root-folder-id", root_folder_id])
                            try:
                                res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                                if res.returncode == 0:
                                    print(f"[canvas-sync] Synced changed canvas to Google Drive: '{real_title}'", flush=True)
                                else:
                                    print(f"[canvas-sync] Error syncing '{real_title}': {res.stderr.strip()}", flush=True)
                                    gdrive_ok = False
                            except Exception as e:
                                print(f"[canvas-sync] Failed to sync '{real_title}': {e}", flush=True)
                                gdrive_ok = False
                    else:
                        # No specific paths passed, nothing to blindly bulk-touch
                        print("[canvas-sync] No specific canvas path queued, skipping Google Drive bulk touch.", flush=True)
            else:
                print("[canvas-sync] Google Drive sync is disabled in config.json. Skipping.", flush=True)

        finally:
            with self._lock:
                self._is_syncing = False
                has_pending = bool(self._pending_titles or self._pending_paths)
                if has_pending:
                    next_titles = list(self._pending_titles)
                    next_paths = list(self._pending_paths)
                    self._pending_titles.clear()
                    self._pending_paths.clear()

            self.last_sync_time = time.time()
            self.last_sync_status = "ok" if (git_ok and gdrive_ok) else "partial_or_error"

            if has_pending:
                print(f"[canvas-sync] Running queued follow-up sync for {len(next_titles)} canvas(es)...", flush=True)
                threading.Thread(target=self._run_sync, args=(next_titles, next_paths), daemon=True).start()


cloud_sync = CanvasCloudSync()
