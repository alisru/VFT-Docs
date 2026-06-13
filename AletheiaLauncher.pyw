import os
import sys
import subprocess
import threading
import queue
import tkinter as tk
from tkinter import ttk
import webbrowser

# Define Color Palette (Dark Mode Premium)
BG_COLOR = "#0f172a"          # Slate 900
CARD_BG = "#1e293b"           # Slate 800
TEXT_COLOR = "#f8fafc"        # Slate 50
TEXT_MUTED = "#94a3b8"        # Slate 400
ACCENT_CYAN = "#06b6d4"       # Cyan 500
ACCENT_CYAN_HOVER = "#0891b2" # Cyan 600
ACCENT_BLUE = "#3b82f6"       # Blue 500
ACCENT_BLUE_HOVER = "#2563eb" # Blue 600
BG_BUTTON = "#334155"         # Slate 700
BG_BUTTON_HOVER = "#475569"   # Slate 600
DANGER_COLOR = "#ef4444"      # Red 500

class AletheiaLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aletheia Bot Operator Console")
        self.root.geometry("1000x680")
        self.root.configure(bg=BG_COLOR)

        # Application state
        self.active_process = None
        self.log_queue = queue.Queue()

        # Set clean modern font
        self.font_title = ("Segoe UI", 12, "bold")
        self.font_subtitle = ("Segoe UI", 10, "bold")
        self.font_body = ("Segoe UI", 9)
        self.font_console = ("Consolas", 9)

        # Style TTK widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR)
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=self.font_body)
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("Card.TFrame", background=CARD_BG, relief="flat", borderwidth=0)
        self.style.configure("TCheckbutton", background=CARD_BG, foreground=TEXT_COLOR, font=self.font_body)

        # Main Layout
        self.build_ui()

        # Start queue reader for console logs
        self.root.after(100, self.read_log_queue)

    def get_python_bin(self):
        if os.path.exists(".venv/Scripts/python.exe"):
            return os.path.abspath(".venv/Scripts/python.exe")
        elif os.path.exists("bluesky_bot/.venv/Scripts/python.exe"):
            return os.path.abspath("bluesky_bot/.venv/Scripts/python.exe")
        return "python"

    def log(self, text):
        self.log_queue.put(text)

    def read_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.console_text.insert(tk.END, msg)
                self.console_text.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.read_log_queue)

    def build_ui(self):
        # Master padding container
        main_container = tk.Frame(self.root, bg=BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # ----------------- Left Panel (Controls) -----------------
        left_panel = tk.Frame(main_container, bg=BG_COLOR)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Title Card
        self.create_title_card(left_panel)

        # Row 1: Actions Header Card
        self.create_actions_card(left_panel)

        # Row 2: Batch Evaluator Card
        self.create_batch_card(left_panel)

        # Row 3: Live Posting Card
        self.create_live_post_card(left_panel)

        # ----------------- Right Panel (Console Output) -----------------
        right_panel = tk.Frame(main_container, bg=BG_COLOR)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.create_console_card(right_panel)

    def create_title_card(self, parent):
        frame = tk.Frame(parent, bg=BG_COLOR)
        frame.pack(fill=tk.X, pady=(0, 15))

        title = tk.Label(frame, text="ALETHEIA OPERATOR CONSOLE", font=("Segoe UI", 16, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        title.pack(anchor="w")

        subtitle = tk.Label(frame, text="Active Pipeline Control Room & Batch Runner", font=self.font_body, fg=TEXT_MUTED, bg=BG_COLOR)
        subtitle.pack(anchor="w")

    def create_actions_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.X, pady=(0, 10))

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=12)
        inner.pack(fill=tk.BOTH, expand=True)

        lbl = tk.Label(inner, text="Quick Actions", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        lbl.pack(anchor="w", pady=(0, 8))

        btn_frame = tk.Frame(inner, bg=CARD_BG)
        btn_frame.pack(fill=tk.X, anchor="w")

        self.btn_open_cp = tk.Button(
            btn_frame, text="Open Control Panel Viewer", font=self.font_body, bg=ACCENT_BLUE, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=12, pady=6, cursor="hand2", command=self.open_control_panel
        )
        self.btn_open_cp.pack(side=tk.LEFT, padx=(0, 8))
        self.btn_open_cp.bind("<Enter>", lambda e: self.btn_open_cp.configure(bg=ACCENT_BLUE_HOVER))
        self.btn_open_cp.bind("<Leave>", lambda e: self.btn_open_cp.configure(bg=ACCENT_BLUE))

        self.btn_rebuild = tk.Button(
            btn_frame, text="Rebuild Stories Store", font=self.font_body, bg=ACCENT_CYAN, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=12, pady=6, cursor="hand2", command=self.run_rebuild_store
        )
        self.btn_rebuild.pack(side=tk.LEFT)
        self.btn_rebuild.bind("<Enter>", lambda e: self.btn_rebuild.configure(bg=ACCENT_CYAN_HOVER))
        self.btn_rebuild.bind("<Leave>", lambda e: self.btn_rebuild.configure(bg=ACCENT_CYAN))

    def create_batch_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.X, pady=(0, 10))

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=12)
        inner.pack(fill=tk.BOTH, expand=True)

        lbl = tk.Label(inner, text="One-Shot Batch Evaluator", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        lbl.pack(anchor="w", pady=(0, 8))

        # Inputs Grid
        grid_frame = tk.Frame(inner, bg=CARD_BG)
        grid_frame.pack(fill=tk.X, pady=(0, 10))

        # Col 1
        tk.Label(grid_frame, text="RSS Count", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=3, padx=(0, 5))
        self.ent_rss = tk.Entry(grid_frame, width=8, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_rss.insert(0, "5")
        self.ent_rss.grid(row=0, column=1, sticky="w", pady=3, padx=(0, 15))

        tk.Label(grid_frame, text="BSky Count", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=2, sticky="w", pady=3, padx=(0, 5))
        self.ent_bsky = tk.Entry(grid_frame, width=8, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_bsky.insert(0, "15")
        self.ent_bsky.grid(row=0, column=3, sticky="w", pady=3, padx=(0, 15))

        tk.Label(grid_frame, text="Categories", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=4, sticky="w", pady=3, padx=(0, 5))
        self.ent_category = tk.Entry(grid_frame, width=15, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_category.insert(0, "general")
        self.ent_category.grid(row=0, column=5, sticky="w", pady=3)

        # Col 2
        tk.Label(grid_frame, text="Topic Filter", bg=CARD_BG, fg=TEXT_MUTED).grid(row=1, column=0, sticky="w", pady=3, padx=(0, 5))
        self.ent_topic = tk.Entry(grid_frame, width=15, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_topic.grid(row=1, column=1, columnspan=2, sticky="w", pady=3, padx=(0, 15))

        tk.Label(grid_frame, text="Exclude Topics", bg=CARD_BG, fg=TEXT_MUTED).grid(row=1, column=3, sticky="w", pady=3, padx=(0, 5))
        self.ent_banned = tk.Entry(grid_frame, width=22, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_banned.insert(0, "travel, sport, entertainment")
        self.ent_banned.grid(row=1, column=4, columnspan=2, sticky="ew", pady=3)

        tk.Label(grid_frame, text="Prioritize Outlets", bg=CARD_BG, fg=TEXT_MUTED).grid(row=2, column=0, sticky="w", pady=3, padx=(0, 5))
        self.ent_prefer = tk.Entry(grid_frame, width=28, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_prefer.grid(row=2, column=1, columnspan=5, sticky="ew", pady=3)
        tk.Label(grid_frame, text="(e.g., 1,2 or all — Bloomberg=1, NYT=2, SaturdayPaper=3, Reuters=4, BBC=5, SMH=6, TechCrunch=7, WaPo=8, NPR=9)", bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 7)).grid(row=3, column=1, columnspan=5, sticky="w")

        # Buttons
        self.btn_run_batch = tk.Button(
            inner, text="Run One-Shot Batch Evaluation", font=self.font_body, bg=ACCENT_CYAN, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=12, pady=5, cursor="hand2", command=self.run_one_shot_batch
        )
        self.btn_run_batch.pack(anchor="w", pady=(8, 0))
        self.btn_run_batch.bind("<Enter>", lambda e: self.btn_run_batch.configure(bg=ACCENT_CYAN_HOVER))
        self.btn_run_batch.bind("<Leave>", lambda e: self.btn_run_batch.configure(bg=ACCENT_CYAN))

    def create_live_post_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.X, pady=(0, 10))

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=12)
        inner.pack(fill=tk.BOTH, expand=True)

        lbl = tk.Label(inner, text="Live Post Scheduler", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        lbl.pack(anchor="w", pady=(0, 8))

        grid_frame = tk.Frame(inner, bg=CARD_BG)
        grid_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(grid_frame, text="Min Delay (sec)", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=3, padx=(0, 5))
        self.ent_min_delay = tk.Entry(grid_frame, width=8, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_min_delay.grid(row=0, column=1, sticky="w", pady=3, padx=(0, 20))

        tk.Label(grid_frame, text="Max Delay (sec)", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=2, sticky="w", pady=3, padx=(0, 5))
        self.ent_max_delay = tk.Entry(grid_frame, width=8, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_max_delay.grid(row=0, column=3, sticky="w", pady=3, padx=(0, 20))

        self.val_watch = tk.BooleanVar(value=False)
        self.chk_watch = ttk.Checkbutton(grid_frame, text="Continuous Watch Mode", variable=self.val_watch)
        self.chk_watch.grid(row=0, column=4, sticky="w", pady=3)

        self.btn_run_live = tk.Button(
            inner, text="Run Pre-Flight & Live Post Scheduler", font=self.font_body, bg=ACCENT_BLUE, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=12, pady=5, cursor="hand2", command=self.run_live_post
        )
        self.btn_run_live.pack(anchor="w")
        self.btn_run_live.bind("<Enter>", lambda e: self.btn_run_live.configure(bg=ACCENT_BLUE_HOVER))
        self.btn_run_live.bind("<Leave>", lambda e: self.btn_run_live.configure(bg=ACCENT_BLUE))

    def create_console_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.BOTH, expand=True)

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=12)
        inner.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(inner, bg=CARD_BG)
        header.pack(fill=tk.X, pady=(0, 8))

        lbl = tk.Label(header, text="Console Output", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        lbl.pack(side=tk.LEFT)

        self.btn_kill = tk.Button(
            header, text="Cancel Active Action", font=self.font_body, bg=DANGER_COLOR, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=8, pady=2, cursor="hand2", command=self.kill_active_process, state=tk.DISABLED
        )
        self.btn_kill.pack(side=tk.RIGHT, padx=5)

        btn_clear = tk.Button(
            header, text="Clear Log", font=self.font_body, bg=BG_BUTTON, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=8, pady=2, cursor="hand2", command=self.clear_console
        )
        btn_clear.pack(side=tk.RIGHT)

        # Text Console with Scrollbar
        txt_frame = tk.Frame(inner, bg=BG_COLOR)
        txt_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(txt_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.console_text = tk.Text(
            txt_frame, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
            font=self.font_console, relief="flat", borderwidth=0, yscrollcommand=scrollbar.set
        )
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.console_text.yview)

    def open_control_panel(self):
        cp_path = os.path.abspath("bluesky_bot/control_panel.html")
        webbrowser.open("file://" + cp_path)

    def clear_console(self):
        self.console_text.delete("1.0", tk.END)

    def set_action_running(self, running):
        if running:
            self.btn_run_batch.configure(state=tk.DISABLED)
            self.btn_run_live.configure(state=tk.DISABLED)
            self.btn_rebuild.configure(state=tk.DISABLED)
            self.btn_kill.configure(state=tk.NORMAL)
        else:
            self.btn_run_batch.configure(state=tk.NORMAL)
            self.btn_run_live.configure(state=tk.NORMAL)
            self.btn_rebuild.configure(state=tk.NORMAL)
            self.btn_kill.configure(state=tk.DISABLED)

    def run_subprocess_async(self, cmd_args):
        self.set_action_running(True)
        def worker():
            try:
                self.log(f"\n> Running: {' '.join(cmd_args)}\n")
                self.active_process = subprocess.Popen(
                    cmd_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                for line in self.active_process.stdout:
                    self.log(line)
                self.active_process.wait()
                self.log(f"\n--- Process finished with exit code {self.active_process.returncode} ---\n")
            except Exception as e:
                self.log(f"\nError running process: {e}\n")
            finally:
                self.active_process = None
                self.root.after(1, lambda: self.set_action_running(False))
        threading.Thread(target=worker, daemon=True).start()

    def kill_active_process(self):
        if self.active_process:
            self.log("\n*** Terminating active action... ***\n")
            self.active_process.terminate()

    def run_rebuild_store(self):
        python_bin = self.get_python_bin()
        self.run_subprocess_async([python_bin, "scratch/rebuild_registries.py"])

    def run_one_shot_batch(self):
        python_bin = self.get_python_bin()
        args = [
            python_bin,
            "bluesky_bot/google_ai_studio_one_shot.py",
            "--rss", self.ent_rss.get().strip(),
            "--bsky", self.ent_bsky.get().strip(),
        ]
        
        category = self.ent_category.get().strip()
        if category:
            args.extend(["--category", category])
            
        topic = self.ent_topic.get().strip()
        if topic:
            args.extend(["--topic", topic])
            
        banned = self.ent_banned.get().strip()
        if banned:
            args.extend(["--banned-topic", banned])
            
        prefer = self.ent_prefer.get().strip()
        if prefer:
            args.extend(["--prefer", prefer])

        self.run_subprocess_async(args)

    def run_live_post(self):
        python_bin = self.get_python_bin()
        self.set_action_running(True)

        def posting_flow():
            try:
                # Step 1: Pre-flight validation
                self.log("\n> Running Pre-Flight Validation...\n")
                val_proc = subprocess.Popen(
                    [python_bin, "bluesky_bot/validate_batch.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                self.active_process = val_proc
                for line in val_proc.stdout:
                    self.log(line)
                val_proc.wait()

                if val_proc.returncode != 0:
                    self.log("\n==================================================\n")
                    self.log("ERROR: Pre-flight validation failed! Posting aborted.\n")
                    self.log("==================================================\n")
                    return

                # Step 2: Post batch
                self.log("\n> Validation passed! Scheduling live batch posting...\n")
                args = [python_bin, "bluesky_bot/post_batch.py", "--live"]
                
                min_delay = self.ent_min_delay.get().strip()
                if min_delay:
                    args.extend(["--min-delay", min_delay])
                    
                max_delay = self.ent_max_delay.get().strip()
                if max_delay:
                    args.extend(["--max-delay", max_delay])
                    
                if self.val_watch.get():
                    args.append("--watch")

                self.log(f"> Command: {' '.join(args)}\n")
                post_proc = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                self.active_process = post_proc
                for line in post_proc.stdout:
                    self.log(line)
                post_proc.wait()
                self.log(f"\n--- Live scheduler completed (exit code: {post_proc.returncode}) ---\n")

            except Exception as e:
                self.log(f"\nError running live posting flow: {e}\n")
            finally:
                self.active_process = None
                self.root.after(1, lambda: self.set_action_running(False))

        threading.Thread(target=posting_flow, daemon=True).start()

if __name__ == "__main__":
    # Ensure correct working directory context
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    root = tk.Tk()
    app = AletheiaLauncherApp(root)
    root.mainloop()
