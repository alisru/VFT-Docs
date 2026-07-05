#!/usr/bin/env python3
"""
Kanon Audit Sourcing GUI

Tkinter front-end with three tabs, one per scraper:
  - Hansard tab  -> drives hansard_scraper.py    (federal via OpenAustralia API, capped ~8000 results)
  - News tab     -> drives news_quote_scraper.py (attributed quotes + source links)
  - APH tab      -> drives aph_scraper.py        (federal direct from aph.gov.au, no result cap,
                                                    reaches all the way back through Hansard history)

All three scraper scripts must be in the same folder as this file.

Double-click "Launch Hansard Scraper.bat" to run this with no console
window, or double-click this .pyw file directly if .pyw is associated
with pythonw.exe on your system.

If the window doesn't appear, check gui_error.log next to this file --
startup errors (e.g. a missing pip package) are written there and shown
in a popup, since pythonw has no console to print tracebacks to.
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
        hint = (
            "\n\nLooks like the '" + missing + "' package isn't installed.\n"
            "Open a command prompt and run:\n\n"
            "    pip install --break-system-packages requests beautifulsoup4 trafilatura\n\n"
            "then try launching again."
        )
    messagebox.showerror(
        "Kanon Audit Sourcing Tools failed to start",
        msg + hint + "\n\nFull details saved to:\n" + ERROR_LOG_PATH,
    )
    root.destroy()
    sys.exit(1)


try:
    import hansard_scraper as hansard
    import news_quote_scraper as news
    import aph_scraper as aph
except Exception as _startup_exc:
    _fatal_startup_error(_startup_exc)


class ScraperTab(ttk.Frame):
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

        self._launch(self._worker)

    def _launch(self, target_fn):
        """Shared launcher for any background action (normal run, or a
        tab-specific extra action like Hansard's full-text upgrade)."""
        self.stop_flag.clear()
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_var.set("Running...")
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        self.worker_thread = threading.Thread(target=lambda: self._run_wrapper(target_fn), daemon=True)
        self.worker_thread.start()

    def _stop_run(self):
        self.stop_flag.set()
        self._log("[stopping after current item...]")

    def _run_wrapper(self, target_fn):
        try:
            target_fn()
        except Exception as e:
            self._log("[error] " + str(e))
            self.status_var.set("Error - see log.")
        finally:
            self.run_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

    def _worker(self):
        raise NotImplementedError


class HansardTab(ScraperTab):
    def _extra_controls(self, frm):
        self.full_text_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frm,
            text="Fetch full speech text (slower: 1 extra page fetch per speech; uncheck for a fast snippet-only pass)",
            variable=self.full_text_var,
        ).grid(row=self._extra_row, column=0, columnspan=4, sticky="w")
        self._extra_row += 1

    def _build_widgets(self):
        super()._build_widgets()
        # Second action button: backfill full text into an existing
        # snippet-only file without re-searching for speeches. Placed
        # next to Run/Stop since it's an alternative action on the same
        # output file, not part of the normal run.
        self.upgrade_btn = ttk.Button(self, text="Upgrade existing file to full text", command=self._start_upgrade)
        # Run/Stop/status live in the button row created by the base
        # class; find it and add this button there too.
        for child in self.winfo_children():
            if isinstance(child, ttk.Frame) and self.run_btn in child.winfo_children():
                self.upgrade_btn.pack(in_=child, side="left", padx=6)
                break

    def _start_upgrade(self):
        if self.worker_thread and self.worker_thread.is_alive():
            messagebox.showinfo("Already running", "Something is already in progress.")
            return
        name = self.name_var.get().strip()
        out_path = self.out_var.get().strip() or self._default_out_path(name, "_hansard.jsonl")
        self.out_var.set(out_path)
        if not os.path.exists(out_path):
            messagebox.showwarning("No file found", f"'{out_path}' doesn't exist yet -- run a scrape first.")
            return
        self._launch(lambda: self._upgrade_worker(out_path))

    def _upgrade_worker(self, out_path):
        self._log(f"Upgrading snippet-only records in {out_path} to full text...")
        upgraded = hansard.upgrade_full_text_in_file(out_path, log_fn=self._log)
        self.status_var.set(f"Done - {upgraded} record(s) upgraded to full text.")

    def _worker(self):
        name = self.name_var.get().strip()
        date_from = self.from_var.get().strip() or None
        date_to = self.to_var.get().strip() or None
        out_path = self.out_var.get().strip() or self._default_out_path(name, "_hansard.jsonl")
        self.out_var.set(out_path)
        full_rescan = self.full_rescan_var.get()

        self._log("Looking up '" + name + "'...")
        candidates = hansard.find_person(name)
        if not candidates:
            self._log("No match found for '" + name + "'.")
            self.status_var.set("No match found.")
            return

        by_id = {}
        for c in candidates:
            by_id.setdefault(c["person_id"], c["full_name"])
        self._log("Found " + str(len(by_id)) + " person_id match(es): " + str(list(by_id.keys())))

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
                self._log("Resuming: " + str(len(seen_gids)) + " speeches already saved, only fetching new ones.")

        file_mode = "w"
        if not full_rescan and seen_gids:
            file_mode = "a"

        fetch_full_text = self.full_text_var.get()
        total_written = 0
        out_handle = open(out_path, file_mode, encoding="utf-8")
        try:
            for pid, full_name in by_id.items():
                for chamber_type in ("representatives", "senate"):
                    if self.stop_flag.is_set():
                        break
                    self._log("Fetching " + chamber_type + " speeches for " + full_name + " (id=" + str(pid) + ")...")
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
                        rec = hansard.normalise_row(row, full_name, chamber_type, fetch_full_text=fetch_full_text)
                        out_handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        total_written += 1
                        # log every single new speech, not just every 10 -- with
                        # full-text fetching on, each one is its own HTTP request
                        # and can take a couple seconds, so this is the only way
                        # the log doesn't look frozen in between
                        self._log("  [" + str(total_written) + "] " + str(row.get("hdate")) + "  " + str(rec.get("debate_title"))[:70])
        finally:
            out_handle.close()

        self._log("Done. Wrote " + str(total_written) + " new speeches to " + out_path)
        self.status_var.set("Done - " + str(total_written) + " new speeches written.")


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
        seen_fingerprints = set()
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
                        if rec.get("article_fingerprint"):
                            seen_fingerprints.add(rec["article_fingerprint"])
                    except json.JSONDecodeError:
                        continue
            if seen_urls:
                self._log("Resuming: " + str(len(seen_urls)) + " article(s) already processed, skipping those.")

        self._log("Searching (" + source + ") for articles mentioning '" + name + "'...")
        if source == "bigquery":
            articles = news.gdelt_bigquery_search(name, date_from, date_to, max_articles)
            if articles is None:
                self._log("BigQuery unavailable, falling back to the free DOC API.")
                articles = news.gdelt_docapi_search(name, date_from, date_to, max_articles)
        else:
            articles = news.gdelt_docapi_search(name, date_from, date_to, max_articles)

        self._log("  Found " + str(len(articles)) + " candidate articles.")
        new_urls = [a for a in articles if a.get("url") and a["url"] not in seen_urls]
        self._log("  " + str(len(articles) - len(new_urls)) + " already processed, " + str(len(new_urls)) + " new to check.")

        file_mode = "w"
        if not full_rescan and seen_urls:
            file_mode = "a"

        total_quotes = 0
        total_dupes = 0
        out_handle = open(out_path, file_mode, encoding="utf-8")
        try:
            for i, art in enumerate(new_urls, 1):
                if self.stop_flag.is_set():
                    break
                self._log("  [" + str(i) + "/" + str(len(new_urls)) + "] " + str(art.get("domain")) + ": " + str(art.get("url")))
                try:
                    records, fingerprint, is_dup = news.scrape_article(art, name, seen_fingerprints=seen_fingerprints)
                except Exception as e:
                    self._log("    [warn] failed: " + str(e))
                    records, fingerprint, is_dup = [], None, False
                if is_dup:
                    total_dupes += 1
                    self._log("    [skip] duplicate/syndicated content of an already-kept article")
                elif fingerprint:
                    seen_fingerprints.add(fingerprint)
                for rec in records:
                    out_handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    total_quotes += 1
        finally:
            out_handle.close()

        self._log("Done. Extracted " + str(total_quotes) + " new attributed quotes -> " + out_path)
        self._log("Skipped " + str(total_dupes) + " duplicate/syndicated article(s) (same content, different outlet/URL).")
        self._log("Note: only quotes + short context + source links were saved, not full article bodies.")
        self.status_var.set("Done - " + str(total_quotes) + " new quotes, " + str(total_dupes) + " dupes skipped.")


class APHTab(ScraperTab):
    def _extra_controls(self, frm):
        ttk.Label(frm, text="Chamber:").grid(row=self._extra_row, column=0, sticky="w")
        self.chamber_var = tk.StringVar(value="all")
        ttk.Combobox(
            frm, textvariable=self.chamber_var, state="readonly", width=18,
            values=list(aph.CHAMBER_OPTIONS.keys()),
        ).grid(row=self._extra_row, column=1, sticky="w")

        ttk.Label(frm, text="Context:").grid(row=self._extra_row, column=2, sticky="w")
        self.context_var = tk.StringVar(value="all")
        ttk.Combobox(
            frm, textvariable=self.context_var, state="readonly", width=22,
            values=list(aph.CONTEXT_OPTIONS.keys()),
        ).grid(row=self._extra_row, column=3, sticky="w")
        self._extra_row += 1

        self.role_var = tk.StringVar(value="speaker")
        role_row = ttk.Frame(frm)
        role_row.grid(row=self._extra_row, column=0, columnspan=4, sticky="w")
        ttk.Radiobutton(role_row, text="Their own speeches only (recommended)",
                         variable=self.role_var, value="speaker").pack(side="left")
        ttk.Radiobutton(role_row, text="All roles (noisier: author/questioner/etc too)",
                         variable=self.role_var, value="all").pack(side="left", padx=10)
        self._extra_row += 1

        self.keep_procedural_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frm, text="Keep bare procedural entries (e.g. 'BUSINESS - <date>' with no real subject)",
            variable=self.keep_procedural_var,
        ).grid(row=self._extra_row, column=0, columnspan=4, sticky="w")
        self._extra_row += 1

        self.download_pdf_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frm, text="Download each result's official PDF (safety-capped at "
                       + str(aph.DEFAULT_PDF_CAP) + " unless confirmed)",
            variable=self.download_pdf_var,
        ).grid(row=self._extra_row, column=0, columnspan=4, sticky="w")
        self._extra_row += 1

    def _worker(self):
        name = self.name_var.get().strip()
        date_from = self.from_var.get().strip() or None
        date_to = self.to_var.get().strip() or None
        out_path = self.out_var.get().strip() or self._default_out_path(name, "_aph_hansard.jsonl")
        self.out_var.set(out_path)

        self._log("Searching aph.gov.au Hansard for '" + name + "'...")
        self._log("(no result cap on this source -- reaches back through full Hansard history)")

        results = list(aph.search_all(
            name, date_from, date_to,
            chamber=self.chamber_var.get(), context=self.context_var.get(), role=self.role_var.get(),
            drop_generic=not self.keep_procedural_var.get(),
        ))
        self._log("Found " + str(len(results)) + " matching Hansard entries.")

        do_pdf = self.download_pdf_var.get()
        pdf_dir = self._default_out_path(name, "_pdfs")
        if do_pdf and len(results) > aph.DEFAULT_PDF_CAP:
            proceed = messagebox.askyesno(
                "Large PDF download",
                f"This would download {len(results)} individual PDFs from aph.gov.au, well past the "
                f"safety default of {aph.DEFAULT_PDF_CAP}. That's a lot of individual requests against "
                f"a government server in one run.\n\nContinue anyway?",
            )
            if not proceed:
                self._log("Skipping PDF downloads (declined). Writing JSONL index only.")
                do_pdf = False

        total = 0
        out_handle = open(out_path, "w", encoding="utf-8")
        try:
            for r in results:
                if self.stop_flag.is_set():
                    break
                total += 1
                rec = {
                    "speaker_name": name,
                    "source": "aph.gov.au",
                    "title": r["title"],
                    "date_display": r["date_display"],
                    "hansard_display_url": r["hansard_display_url"],
                    "pdf_url": r["pdf_url"],
                    "pdf_local_path": None,
                }
                if do_pdf and r["pdf_url"]:
                    import re as _re
                    fname = _re.sub(r"[^A-Za-z0-9_.-]", "_", r["title"])[:100] + ".pdf"
                    rec["pdf_local_path"] = aph.download_pdf(r["pdf_url"], pdf_dir, fname)
                out_handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
                self._log("  [" + str(total) + "] " + str(r["date_display"]) + "  " + r["title"][:70])
        finally:
            out_handle.close()

        self._log("Done. Wrote " + str(total) + " entries to " + out_path)
        if do_pdf:
            self._log("PDFs saved to: " + pdf_dir + "/")
        self.status_var.set("Done - " + str(total) + " entries" + (", PDFs downloaded" if do_pdf else "."))


class KanonAuditGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kanon Audit Sourcing Tools")
        self.geometry("760x600")
        self.resizable(True, True)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        hansard_tab = HansardTab(notebook)
        news_tab = NewsTab(notebook)
        aph_tab = APHTab(notebook)

        notebook.add(hansard_tab, text="Hansard (OpenAustralia)")
        notebook.add(news_tab, text="News")
        notebook.add(aph_tab, text="APH (no cap)")


if __name__ == "__main__":
    try:
        app = KanonAuditGUI()
        app.mainloop()
    except Exception as _runtime_exc:
        _fatal_startup_error(_runtime_exc)
