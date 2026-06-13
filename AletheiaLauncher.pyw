import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
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

class AletheiaLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aletheia Launcher")
        self.root.geometry("560x450")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Set clean modern font
        self.font_title = ("Segoe UI", 12, "bold")
        self.font_subtitle = ("Segoe UI", 10, "bold")
        self.font_body = ("Segoe UI", 9)

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

    def get_python_bin(self):
        if os.path.exists(".venv/Scripts/python.exe"):
            return ".venv\\Scripts\\python.exe"
        elif os.path.exists("bluesky_bot/.venv/Scripts/python.exe"):
            return "bluesky_bot\\.venv\\Scripts\\python.exe"
        return "python"

    def build_ui(self):
        # Master padding container
        main_container = tk.Frame(self.root, bg=BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Title Card
        self.create_title_card(main_container)

        # Row 1: Actions Header Card
        self.create_actions_card(main_container)

        # Row 2: Batch Evaluator Card
        self.create_batch_card(main_container)

        # Row 3: Live Posting Card
        self.create_live_post_card(main_container)

    def create_title_card(self, parent):
        frame = tk.Frame(parent, bg=BG_COLOR)
        frame.pack(fill=tk.X, pady=(0, 10))

        title = tk.Label(frame, text="ALETHEIA OPERATOR CONSOLE", font=("Segoe UI", 14, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        title.pack(anchor="w")

        subtitle = tk.Label(frame, text="Click buttons to spawn tasks in separate terminals.", font=self.font_body, fg=TEXT_MUTED, bg=BG_COLOR)
        subtitle.pack(anchor="w")

    def create_actions_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.X, pady=(0, 10))

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=10)
        inner.pack(fill=tk.BOTH, expand=True)

        lbl = tk.Label(inner, text="Quick Actions", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        lbl.pack(anchor="w", pady=(0, 6))

        btn_frame = tk.Frame(inner, bg=CARD_BG)
        btn_frame.pack(fill=tk.X, anchor="w")

        self.btn_open_cp = tk.Button(
            btn_frame, text="Open Control Panel", font=self.font_body, bg=ACCENT_BLUE, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=12, pady=5, cursor="hand2", command=self.open_control_panel
        )
        self.btn_open_cp.pack(side=tk.LEFT, padx=(0, 8))
        self.btn_open_cp.bind("<Enter>", lambda e: self.btn_open_cp.configure(bg=ACCENT_BLUE_HOVER))
        self.btn_open_cp.bind("<Leave>", lambda e: self.btn_open_cp.configure(bg=ACCENT_BLUE))

        self.btn_rebuild = tk.Button(
            btn_frame, text="Rebuild Stories Store", font=self.font_body, bg=ACCENT_CYAN, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=12, pady=5, cursor="hand2", command=self.run_rebuild_store
        )
        self.btn_rebuild.pack(side=tk.LEFT)
        self.btn_rebuild.bind("<Enter>", lambda e: self.btn_rebuild.configure(bg=ACCENT_CYAN_HOVER))
        self.btn_rebuild.bind("<Leave>", lambda e: self.btn_rebuild.configure(bg=ACCENT_CYAN))

    def create_batch_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.X, pady=(0, 10))

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=10)
        inner.pack(fill=tk.BOTH, expand=True)

        lbl = tk.Label(inner, text="One-Shot Batch Evaluator", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        lbl.pack(anchor="w", pady=(0, 6))

        # Inputs Grid
        grid_frame = tk.Frame(inner, bg=CARD_BG)
        grid_frame.pack(fill=tk.X, pady=(0, 8))

        # Col 1
        tk.Label(grid_frame, text="RSS Count", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=2, padx=(0, 5))
        self.ent_rss = tk.Entry(grid_frame, width=6, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_rss.insert(0, "5")
        self.ent_rss.grid(row=0, column=1, sticky="w", pady=2, padx=(0, 15))

        tk.Label(grid_frame, text="BSky Count", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=2, sticky="w", pady=2, padx=(0, 5))
        self.ent_bsky = tk.Entry(grid_frame, width=6, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_bsky.insert(0, "15")
        self.ent_bsky.grid(row=0, column=3, sticky="w", pady=2, padx=(0, 15))

        tk.Label(grid_frame, text="Categories", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=4, sticky="w", pady=2, padx=(0, 5))
        self.ent_category = tk.Entry(grid_frame, width=12, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_category.insert(0, "general")
        self.ent_category.grid(row=0, column=5, sticky="w", pady=2)

        # Col 2
        tk.Label(grid_frame, text="Topic Filter", bg=CARD_BG, fg=TEXT_MUTED).grid(row=1, column=0, sticky="w", pady=2, padx=(0, 5))
        self.ent_topic = tk.Entry(grid_frame, width=12, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_topic.grid(row=1, column=1, columnspan=2, sticky="w", pady=2, padx=(0, 15))

        tk.Label(grid_frame, text="Exclude Topics", bg=CARD_BG, fg=TEXT_MUTED).grid(row=1, column=3, sticky="w", pady=2, padx=(0, 5))
        self.ent_banned = tk.Entry(grid_frame, width=20, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_banned.insert(0, "travel, sport, entertainment")
        self.ent_banned.grid(row=1, column=4, columnspan=2, sticky="ew", pady=2)

        tk.Label(grid_frame, text="Prioritize Outlets", bg=CARD_BG, fg=TEXT_MUTED).grid(row=2, column=0, sticky="w", pady=2, padx=(0, 5))
        self.ent_prefer = tk.Entry(grid_frame, width=28, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_prefer.grid(row=2, column=1, columnspan=5, sticky="ew", pady=2)

        # Buttons
        self.btn_run_batch = tk.Button(
            inner, text="Launch Batch Evaluator Terminal", font=self.font_body, bg=ACCENT_CYAN, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=12, pady=5, cursor="hand2", command=self.run_one_shot_batch
        )
        self.btn_run_batch.pack(anchor="w", pady=(6, 0))
        self.btn_run_batch.bind("<Enter>", lambda e: self.btn_run_batch.configure(bg=ACCENT_CYAN_HOVER))
        self.btn_run_batch.bind("<Leave>", lambda e: self.btn_run_batch.configure(bg=ACCENT_CYAN))

    def create_live_post_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.X, pady=(0, 10))

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=10)
        inner.pack(fill=tk.BOTH, expand=True)

        lbl = tk.Label(inner, text="Live Post Scheduler", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        lbl.pack(anchor="w", pady=(0, 6))

        grid_frame = tk.Frame(inner, bg=CARD_BG)
        grid_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(grid_frame, text="Min Delay (sec)", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=2, padx=(0, 5))
        self.ent_min_delay = tk.Entry(grid_frame, width=8, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_min_delay.grid(row=0, column=1, sticky="w", pady=2, padx=(0, 20))

        tk.Label(grid_frame, text="Max Delay (sec)", bg=CARD_BG, fg=TEXT_MUTED).grid(row=0, column=2, sticky="w", pady=2, padx=(0, 5))
        self.ent_max_delay = tk.Entry(grid_frame, width=8, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", font=self.font_body)
        self.ent_max_delay.grid(row=0, column=3, sticky="w", pady=2, padx=(0, 20))

        self.val_watch = tk.BooleanVar(value=False)
        self.chk_watch = ttk.Checkbutton(grid_frame, text="Continuous Watch Mode", variable=self.val_watch)
        self.chk_watch.grid(row=0, column=4, sticky="w", pady=2)

        self.btn_run_live = tk.Button(
            inner, text="Launch Pre-Flight & Live Scheduler Terminal", font=self.font_body, bg=ACCENT_BLUE, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=12, pady=5, cursor="hand2", command=self.run_live_post
        )
        self.btn_run_live.pack(anchor="w")
        self.btn_run_live.bind("<Enter>", lambda e: self.btn_run_live.configure(bg=ACCENT_BLUE_HOVER))
        self.btn_run_live.bind("<Leave>", lambda e: self.btn_run_live.configure(bg=ACCENT_BLUE))

    def open_control_panel(self):
        cp_path = os.path.abspath("bluesky_bot/control_panel.html")
        webbrowser.open("file://" + cp_path)

    def spawn_terminal(self, title, script_cmd):
        try:
            # Command Prompt start command:
            # cmd /k executes the command and keeps the prompt open so the user can see logs
            full_cmd = f'start cmd /k "title {title} && {script_cmd}"'
            subprocess.Popen(full_cmd, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to spawn terminal: {e}")

    def run_rebuild_store(self):
        python_bin = self.get_python_bin()
        self.spawn_terminal("Aletheia: Rebuild Registry Store", f"{python_bin} scratch\\rebuild_registries.py")

    def run_one_shot_batch(self):
        python_bin = self.get_python_bin()
        args = [
            python_bin,
            "bluesky_bot\\google_ai_studio_one_shot.py",
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

        self.spawn_terminal("Aletheia: Batch Evaluator", " ".join(args))

    def run_live_post(self):
        python_bin = self.get_python_bin()
        
        # Step 1 command: Run validator. If successful, continue to posting.
        # Step 2 command: Run posting script with delay arguments.
        post_args = [python_bin, "bluesky_bot\\post_batch.py", "--live"]
        
        min_delay = self.ent_min_delay.get().strip()
        if min_delay:
            post_args.extend(["--min-delay", min_delay])
            
        max_delay = self.ent_max_delay.get().strip()
        if max_delay:
            post_args.extend(["--max-delay", max_delay])
            
        if self.val_watch.get():
            post_args.append("--watch")

        # Combine validator and poster commands with && so validation failure aborts posting.
        cmd_chain = (
            f"echo ================================================== && "
            f"echo [1/2] Running Pre-Flight Validation... && "
            f"echo ================================================== && "
            f"{python_bin} bluesky_bot\\validate_batch.py && "
            f"echo ================================================== && "
            f"echo [2/2] Validation Passed! Starting Live Scheduler... && "
            f"echo ================================================== && "
            f"{' '.join(post_args)}"
        )

        self.spawn_terminal("Aletheia: Live Post Scheduler", cmd_chain)

if __name__ == "__main__":
    # Ensure correct working directory context
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    root = tk.Tk()
    app = AletheiaLauncherApp(root)
    root.mainloop()
