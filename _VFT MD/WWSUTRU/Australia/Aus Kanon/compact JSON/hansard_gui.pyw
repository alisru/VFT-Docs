#!/usr/bin/env python3
"""
Kanon Audit Sourcing GUI

Tkinter front-end with two tabs, one per scraper:
  - Hansard tab  -> drives hansard_scraper.py  (full parliamentary speech text)
  - News tab     -> drives news_quote_scraper.py (attributed quotes + source links)

Both scrapers must be in the same folder as this file.

Double-click "Launch Hansard Scraper.bat" to run this with no console
window, or double-click this .pyw file directly if .pyw is associated
with pythonw.exe on your system.
"""

import os
import sys
import json
import traceback
import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
ERROR_LOG_PATH = os.path.join(SCRIPT_DIR, "gui_error.log")


def _fatal_startup_error(exc):
    """Show a popup with the real error instead of the window silently
    vanishing (which is what happens by default under pythonw, since it
    has no console to print tracebacks to)."""
    tb = traceback.format_exc()
    try:
        with open(ERROR_LOG_PATH, "w", encoding="utf-8") as f:
            f.write(tb)
    except Exception:
        pass

    root = tk.Tk()
    root.withdraw()
    hint = ""
    msg = str(exc)
    if isinstance(exc, ModuleNotFoundError):
        missing = msg.split("'")[1] if "'" in msg else msg
        pip_name = {"bs4": "beautifulsoup4"}.get(missing, missing)
        hint = (
            f"\n\nLooks like the '{missing}' package isn't installed.\n"
            f"Open a command prompt and run:\n\n"
            f"    pip install --break-system-packages requests beautifulsoup4 trafilatura\n\n"
            f"then try launching again."
        )
    messagebox.showerror(
        "Kanon Audit Sourcing Tools failed to start",
        f"{msg}{hint}\n\nFull details saved to:\n{ERROR_LOG_PATH}",
    )
    root.destroy()
    sys.exit(1)


try:
    import hansard_scraper as hansard
    import news_quote_scraper as news
except Exception as _startup_exc:
    _fatal_startup_error(_startup_exc)


class ScraperTab(ttk.Frame):
    """Base layout shared by both tabs: name, date range, output file,
    run/stop buttons, status line, scrolling log. Subclasses implement
    _worker() for the actual scrape logic and _extra_controls() for any
    tab-specific fields."""

    def __init__(self, parent):
        super().__init__(parent)
        self.log_queue = queue.Queue()
        self.worker_thread = None
        self.stop_flag = threading.Event()
        self._build_widgets()
        self.after(100, self._poll_log_queue)

    def _build_widgets(self):
        pad = {"padx": 8, "pady": 6}

        frm = ttk.Frame(self)
        frm.pack(fill="x", **pad)

        ttk.Label(frm, text="Actor name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.name_var, width=40).grid(row=0, column=1, columnspan=3, sticky="we")

        ttk.Label(frm, text="From (YYYY-MM-DD, optional):").grid(row=1, column=0, sticky="w")
        self.from_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.from_var, width=15).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="To (YYYY-MM-DD, optional):").grid(row=1, column=2, sticky="w")
        self.to_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.to_var, width=15).grid(row=1, column=3, sticky="w")

        ttk.Label(frm, text="Output file:").grid(row=2, column=0, sticky="w")
        self.out_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.out_var, width=40).grid(row=2, column=1, columnspan=2, sticky="we")
        ttk.Button(frm, text="Browse...", command=self._choose_output).grid(row=2, column=3, sticky="we")

        frm.columnconfigure(1, weight=1)
        self._extra_row = 3
        self._extra_frame = frm
        self._extra_controls(frm)

        opts_frm = ttk.Frame(self)
        opts_frm.pack(fill="x", **pad)
        self.full_rescan_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opts_frm, text="Full rescan (ignore existing progress, start clean)",
                         variable=self.full_rescan_var).pack(side="left")

        btn_frm = ttk.Frame(self)
        btn_frm.pack(fill="x", **pad)
        self.run_btn = ttk.Button(btn_frm, text="Run", command=self._start_run)
        self.run_btn.pack(side="left")
        self.stop_btn = ttk.Button(btn_frm, text="Stop", command=self._stop_run, state="disabled")
        self.stop_btn.pack(side="left", padx=6)
        self.status_var = tk.StringVar(value="Idle.")
        ttk.Label(btn_frm, textvariable=self.status_var).pack(side="left", padx=12)

        log_frm = ttk.Frame(self)
        log_frm.pack(fill="both", expand=True, **pad)
        self.log_text = tk.Text(log_frm, wrap="word", state="disabled", height=18)
        self.log_text.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(log_frm, command=self.log_text.yview)
        scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scroll.set)

    def _extra_controls(self, frm):
        """Override in subclasses to add tab-specific fields under the shared ones."""
        pass

    def _choose_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".jsonl",
            filetypes=[("JSON Lines", "*.jsonl"), ("All files", "*.*")],
        )
        if path:
            self.out_var.set(path)

    def _log(self, msg):
        self.log_queue.put(msg)

    def _poll_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.configure(state="normal")
                self.log_text.insert("end", msg + "\n")
                self.log_text.see("end")
                self.log_text.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(100, self._poll_log_queue)

    def _default_out_path(self, name, suffix):
        return name.lower().replace(" ", "_") + suffix

    def _start_run(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Enter an actor name first.")
            return
        if self.worker_thread and self.worker_thread.is_alive():
            messagebox.showinfo("Already running", "A scrape is already in progress.")
            return

        self.stop_flag.clear()
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_var.set("Running...")
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        self.worker_thread = threading.Thread(target=self._run_wrapper, daemon=True)
        self.worker_thread.start()

    def _stop_run(self):
        self.stop_flag.set()
        self._log("[stopping after current item...]")

    def _run_wrapper(self):
        try:
            self._worker()
        except Exception as e:
            self._log(f"[error] {e}")
            self.status_var.set("Error — see log.")
        finally:
            self.run_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

    def _worker(self):
        raise NotImplementedError


class HansardTab(ScraperTab):
    def _worker(self):
        name = self.name_var.get().strip()
        date_from = self.from_var.get().strip() or None
        date_to = self.to_var.get().strip() or None
        out_path = self.out_var.get().strip() or self._default_out_path(name, "_hansard.jsonl")
        self.out_var.set(out_path)
        full_rescan = self.full_rescan_var.get()

        self._log(f"Looking up '{name}'...")
        candidates = hansard.find_person(name)
        if not candidates:
            self._log(f"No match found for '{name}'.")
            self.status_var.set("No match found.")
            return

        by_id = {}
        for c in candidates:
            by_id.setdefault(c["person_id"], c["full_name"])
        self._log(f"Found {len(by_id)} person_id match(es): {list(by_id.keys())}")

        seen_gids = set()
        if not full_rescan and os.path.exists(out_path):
            with open(out_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        if rec.get("gid"):
                            seen_gids.add(rec["gid"])
                    except json.JSONDecodeError:
                        continue
            if seen_gids:
                self._log(f"Resuming: {len(seen_gids)} speeches already saved, only fetching new ones.")

        file_mode = "w" if full_rescan or not seen_gids else "a"
        total_written = 0
        with open(out_path, file_mode, encoding="utf-8") as f:
            for pid, full_name in by_id.items():
                for chamber_type in ("representatives", "senate"):
                    if self.stop_flag.is_set():
                        break
                    self._log(f"Fetching {chamber_type} speeches for {full_name} (id={pid})...")
                    for row in hansard.fetch_all_debates(
                        pid, chamber_type, date_from, date_to,
                        known_gids=seen_gids, stop_on_known_page=not full_rescan
                    ):
                        if self.stop_flag.is_set():
                            break
                        gid = row.get("gid")
                        if gid in seen_gids:
                            continue
                        seen_gids.add(gid)
                        rec = hansard.normalise_row(row, full_name, chamber_type)
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        total_written += 1
                        if total_written % 10 == 0:
                            self._log(f"  ...{total_written} new speeches so far")

        self._log(f"\nDone. Wrote {total_written} new speeches to {out_path}")
        self.status_var.set(f"Done — {total_written} new speeches written.")


class NewsTab(ScraperTab):
    def _extra_controls(self, frm):
        ttk.Label(frm, text="Source:").grid(row=self._extra_row, column=0, sticky="w")
        self.source_var = tk.StringVar(value="bigquery")
        source_row = ttk.Frame(frm)
        source_row.grid(row=self._extra_row, column=1, columnspan=3, sticky="w")
        ttk.Radiobutton(source_row, text="BigQuery (deeper, needs GCP auth)",
                         variable=self.source_var, value="bigquery").pack(side="left")
        ttk.Radiobutton(source_row, text="Free DOC API (no setup)",
                         variable=self.source_var, value="docapi").pack(side="left", padx=10)

        self._extra_row += 1
        ttk.Label(frm, text="Max articles to check:").grid(row=self._extra_row, column=0, sticky="w")
        self.max_articles_var = tk.StringVar(value="200")
        ttk.Entry(frm, textvariable=self.max_articles_var, width=10).grid(row=self._extra_row, column=1, sticky="w")

    def _worker(self):
        name = self.name_var.get().strip()
        date_from = self.from_var.get().strip() or None
        date_to = self.to_var.get().strip() or None
        out_path = self.out_var.get().strip() or self._default_out_path(name, "_news.jsonl")
        self.out_var.set(out_path)
        full_rescan = self.full_rescan_var.get()
        source = self.source_var.get()
        try:
            max_articles = int(self.max_articles_var.get().strip() or "200")
        except ValueError:
            max_articles = 200

        seen_urls = set()
        if not full_rescan and os.path.exists(out_path):
            with open(out_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        if rec.get("source_url"):
                            seen_urls.add(rec["source_url"])
                    except json.JSONDecodeError:
                        continue
            if seen_urls:
                self._log(f"Resuming: {len(seen_urls)} article(s) already processed, skipping those.")

        self._log(f"Searching ({source}) for articles mentioning '{name}'...")
        if source == "bigquery":
            articles = news.gdelt_bigquery_search(name, date_from, date_to, max_articles)
            if articles is None:
                self._log("BigQuery unavailable, falling back to the free DOC API.")
                articles = news.gdelt_docapi_search(name, date_from, date_to, max_articles)
        else:
            articles = news.gdelt_docapi_search(name, date_from, date_to, max_articles)

        self._log(f"  Found {len(articles)} candidate articles.")
        new_urls = [a for a in articles if a.get("url") and a["url"] not in seen_urls]
        self._log(f"  {len(articles) - len(new_urls)} already processed, {len(new_urls)} new to check.")

        file_mode = "w" if full_rescan or not seen_urls else "a"
        total_quotes = 0
        with open(out_path, file_mode, encoding="utf-8") as f:
            for i, art in enumerate(new_urls, 1):
                if self.stop_flag.is_set():
                    break
                self._log(f"  [{i}/{len(new_urls)}] {art.get('domain')}: {art.get('url')}")
                try:
                    records = news.scrape_article(art, name)
                except Exception as e:
                    self._log(f"    [warn] failed: {e}")
                    records = []
                for rec in records:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    total_quotes += 1

        self._log(f"\nDone. Extracted {total_quotes} new attributed quotes -> {out_path}")
        self._log("Note: only quotes + short context + source links were saved, not full article bodies.")
        self.status_var.set(f"Done — {total_quotes} new quotes written.")


class KanonAuditGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kanon Audit Sourcing Tools")
        self.geometry("700x560")
        self.resizable(True, True)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        hansard_tab = HansardTab(notebook)
        news_tab = NewsTab(notebook)

        notebook.add(hansard_tab, text="Hansard")
        notebook.add(news_tab, text="News")


if __name__ == "__main__":
    try:
        app = KanonAuditGUI()
        app.mainloop()
    except Exception as _runtime_exc:
        _fatal_startup_error(_runtime_exc)
