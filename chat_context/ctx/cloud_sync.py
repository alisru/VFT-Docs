"""
Background debounced cloud sync worker for Canvases:
1. Git: commits and pushes chat_context/canvases/ to origin main.
2. Google Drive: copies chat_context/canvases/ to VFT:Gemini Canvases via rclone.
"""
import re
import subprocess
import threading
import time
from pathlib import Path

from .db import CANVASES_DIR, ROOT

REPO_ROOT = ROOT.parent  # e:\Vector Field Theory\VFT Docs
SYNC_DELAY = 30  # seconds to wait after last canvas edit before pushing
GDRIVE_ROOT_FOLDER_ID = "1eFfacNbz1A45n_yVH6m2l4jN7LvTBF7S"  # VFT root folder on GDrive
GDOCS_STAGING_DIR = ROOT / "drawing_board" / "gdocs_staging"


def prepare_gdocs_staging():
    """Converts updated .md canvases into clean .docx files for Google Docs import."""
    GDOCS_STAGING_DIR.mkdir(parents=True, exist_ok=True)
    for md_file in CANVASES_DIR.rglob("*.md"):
        rel = md_file.relative_to(CANVASES_DIR)
        docx_file = GDOCS_STAGING_DIR / rel.parent / (rel.stem + ".docx")
        if docx_file.exists() and docx_file.stat().st_mtime >= md_file.stat().st_mtime:
            continue
        docx_file.parent.mkdir(parents=True, exist_ok=True)
        raw_text = md_file.read_text(encoding="utf-8", errors="replace")
        clean_text = re.sub(r"^---\n.*?\n---\n+", "", raw_text, flags=re.S)
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
        except Exception as err:
            print(f"[canvas-sync] Pandoc conversion error for {md_file.name}: {err}", flush=True)


class CanvasCloudSync:
    def __init__(self):
        self._timer = None
        self._lock = threading.Lock()
        self._changed_titles = set()
        self._is_syncing = False
        self.last_sync_time = None
        self.last_sync_status = "idle"

    def notify_change(self, canvas_title: str):
        """Called whenever a canvas file is written or updated on disk."""
        with self._lock:
            self._changed_titles.add(canvas_title)
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
            self._changed_titles.clear()

        threading.Thread(target=self._run_sync, args=(titles,), daemon=True).start()

    def _on_timer(self):
        with self._lock:
            titles = list(self._changed_titles)
            self._changed_titles.clear()
            self._timer = None

        threading.Thread(target=self._run_sync, args=(titles,), daemon=True).start()

    def _run_sync(self, titles):
        if self._is_syncing:
            print("[canvas-sync] Sync already in progress, skipping overlapping run", flush=True)
            return

        self._is_syncing = True
        self.last_sync_status = "syncing"
        print(f"[canvas-sync] Starting sync for: {titles or 'all canvases'}", flush=True)

        # --- 1. Git Auto-Commit and Push (Dedicated Repo: alisru/gemini-canvases) ---
        git_ok = False
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
                    print(f"[canvas-sync] Git committed (gemini-canvases): {commit_msg}", flush=True)
                    push_res = subprocess.run(
                        ["git", "push", "origin", "main"],
                        cwd=CANVASES_DIR,
                        capture_output=True,
                        text=True,
                        timeout=45,
                    )
                    if push_res.returncode == 0:
                        print("[canvas-sync] Git pushed to gemini-canvases origin main successfully", flush=True)
                        git_ok = True
                    else:
                        print(f"[canvas-sync] Git push failed: {push_res.stderr.strip()}", flush=True)
                else:
                    print(f"[canvas-sync] Git commit note: {commit_res.stdout.strip() or commit_res.stderr.strip()}", flush=True)
            else:
                print("[canvas-sync] Git: working tree clean for gemini-canvases, nothing to commit", flush=True)
                git_ok = True
        except Exception as e:
            print(f"[canvas-sync] Git error: {e}", flush=True)

        # --- 2. Google Drive Sync as Native Google Docs ---
        gdrive_ok = False
        try:
            if CANVASES_DIR.exists():
                prepare_gdocs_staging()
                rclone_res = subprocess.run(
                    [
                        "rclone",
                        "copy",
                        str(GDOCS_STAGING_DIR),
                        "VFT:Canvases",
                        "--drive-root-folder-id",
                        GDRIVE_ROOT_FOLDER_ID,
                        "--drive-import-formats",
                        "docx",
                        "--drive-allow-import-name-change",
                        "--tpslimit",
                        "3",
                        "--contimeout",
                        "15s",
                        "--timeout",
                        "90s",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                if rclone_res.returncode == 0:
                    print("[canvas-sync] Google Drive: canvases synced successfully as native Google Docs to 'VFT:Canvases'", flush=True)
                    gdrive_ok = True
                else:
                    print(f"[canvas-sync] Google Drive sync error: {rclone_res.stderr.strip()}", flush=True)
        except Exception as e:
            print(f"[canvas-sync] Google Drive error: {e}", flush=True)

        self._is_syncing = False
        self.last_sync_time = time.time()
        self.last_sync_status = "ok" if (git_ok and gdrive_ok) else "partial_or_error"
        self.last_sync_status = "ok" if (git_ok and gdrive_ok) else "partial_or_error"


cloud_sync = CanvasCloudSync()
