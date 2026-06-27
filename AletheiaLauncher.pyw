import os
import sys
import subprocess
import re

# Self-relaunch inside virtual environment if not already running there
if sys.platform == "win32":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_paths = [
        os.path.join(script_dir, ".venv", "Scripts", "pythonw.exe"),
        os.path.join(script_dir, "bluesky_bot", ".venv", "Scripts", "pythonw.exe")
    ]
    venv_pyw = None
    for p in venv_paths:
        if os.path.exists(p):
            venv_pyw = os.path.abspath(p)
            break
            
    if venv_pyw and os.path.abspath(sys.executable).lower() != venv_pyw.lower():
        try:
            subprocess.Popen([venv_pyw] + sys.argv)
            sys.exit(0)
        except Exception:
            pass

# Force Windows to recognize this script as a distinct application for taskbar icon grouping
if sys.platform == "win32":
    try:
        import ctypes
        myappid = 'aletheia.judgement.launcher.v1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

# Import standard Tkinter and Pillow libraries (guaranteed to be inside .venv)
import threading
import queue
import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk

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
SUCCESS_COLOR = "#10b981"     # Emerald 500
WARNING_COLOR = "#f59e0b"     # Amber 500
DANGER_COLOR = "#ef4444"      # Red 500

class DragDropListbox(tk.Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.cur_index = None
        self.on_reorder_callback = None

    def on_click(self, event):
        self.cur_index = self.nearest(event.y)

    def on_drag(self, event):
        i = self.nearest(event.y)
        if i != self.cur_index and i >= 0:
            text = self.get(self.cur_index)
            self.delete(self.cur_index)
            self.insert(i, text)
            self.select_clear(0, tk.END)
            self.select_set(i)
            self.cur_index = i
            if self.on_reorder_callback:
                self.on_reorder_callback()


class AletheiaLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aletheia Bot Operator Console")
        self.root.geometry("1150x780")
        self.root.configure(bg=BG_COLOR)

        # Set Window Icon
        self.set_window_icon()

        # Application state for parallel processes
        self.eval_process = None
        self.post_process = None
        self.log_queue = queue.Queue()

        # Dynamically import available/default models from the one-shot script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bot_path = os.path.join(script_dir, "bluesky_bot")
        if bot_path not in sys.path:
            sys.path.append(bot_path)

        try:
            from google_ai_studio_one_shot import DEFAULT_FALLBACKS
            default_list = list(DEFAULT_FALLBACKS)
        except Exception as import_err:
            print(f"Warning: Failed to dynamically load models from bot script: {import_err}")
            default_list = [
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-3.5-flash",
                "gemini-3.1-flash-lite",
                "vertex:gemini-3.1-flash-lite",
                "gemini-3-flash-preview",
                "gemma-4-31b-it",
                "gemma-4-26b-a4b-it",
            ]

        # Available models also include custom/agnes options
        self.available_models = list(default_list)
        if "agnes-2.0-flash" not in self.available_models:
            self.available_models.append("agnes-2.0-flash")

        # Set default selection list (excluding agnes-2.0-flash unless added manually by checkbox)
        self.selected_models = [m for m in default_list if m != "agnes-2.0-flash"]
        self.model_vars = {}

        # Load RSS feeds statically from harvester script
        self.feed_definitions = self.load_rss_feeds_from_script()
        if not self.feed_definitions:
            # Fallback list of feeds if script parsing failed
            self.feed_definitions = {
                "ABC News Australia": "https://www.abc.net.au/news/feed/2942460/rss.xml",
                "9News Australia": "https://www.9news.com.au/rss",
                "SBS News": "https://www.sbs.com.au/news/feed",
                "Sydney Morning Herald": "https://www.smh.com.au/rss/feed.xml",
                "Perth Now": "https://www.perthnow.com.au/feed",
                "The Age": "https://www.theage.com.au/rss/feed.xml",
                "Brisbane Times": "https://www.brisbanetimes.com.au/rss/feed.xml",
                "WA Today": "https://www.watoday.com.au/rss/feed.xml",
                "Canberra Times": "https://www.canberratimes.com.au/rss.xml",
                "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
                "NYT Home": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
                "The Guardian UK": "https://www.theguardian.com/uk/rss",
                "The Guardian World": "https://www.theguardian.com/world/rss",
                "NPR News": "https://feeds.npr.org/1001/rss.xml",
                "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
                "Google News World": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
                "Google News Australia": "https://news.google.com/rss?hl=en-AU&gl=AU&ceid=AU:en",
                "BBC Tech": "http://feeds.bbci.co.uk/news/technology/rss.xml",
                "NYT Tech": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
                "TechCrunch": "https://techcrunch.com/feed/",
                "The Guardian Tech": "https://www.theguardian.com/technology/rss",
                "BBC Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
                "NYT Business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
                "CNBC Business": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147",
                "The Guardian Business": "https://www.theguardian.com/business/rss",
                "DW Business": "https://rss.dw.com/xml/rss-en-bus",
                "BBC Politics": "http://feeds.bbci.co.uk/news/politics/rss.xml",
                "NYT Politics": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
                "NPR Politics": "https://feeds.npr.org/1014/rss.xml",
                "The Guardian Politics": "https://www.theguardian.com/politics/rss",
                "BBC Science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
                "NYT Science": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
                "The Guardian Science": "https://www.theguardian.com/science/rss",
                "DW Science": "https://rss.dw.com/xml/rss-en-science",
            }
        self.feed_vars = {}

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

        # Initial HUD Load and start periodic refresh loop (every 3 seconds)
        self.periodic_hud_refresh()

        # Start queue reader for console logs
        self.root.after(100, self.read_log_queue)

    def get_python_bin(self):
        if os.path.exists(".venv/Scripts/python.exe"):
            return os.path.abspath(".venv/Scripts/python.exe")
        elif os.path.exists("bluesky_bot/.venv/Scripts/python.exe"):
            return os.path.abspath("bluesky_bot/.venv/Scripts/python.exe")
        return "python"

    def set_window_icon(self):
        icon_path = "bluesky_bot/alethekanon.png"
        if os.path.exists(icon_path):
            try:
                self.icon_image = Image.open(icon_path)
                self.tk_icon = ImageTk.PhotoImage(self.icon_image)
                self.root.iconphoto(True, self.tk_icon)
            except Exception as e:
                print(f"Failed to set window icon: {e}")

    def load_rss_feeds_from_script(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        harvester_path = os.path.join(script_dir, "bluesky_bot", "harvest_candidates.py")
        feeds = {}
        if os.path.exists(harvester_path):
            try:
                with open(harvester_path, "r", encoding="utf-8") as f:
                    content = f.read()
                matches = re.findall(
                    r'\{\s*["\']name["\']\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']url["\']\s*:\s*["\']([^"\']+)["\']',
                    content
                )
                for name, url in matches:
                    feeds[name] = url
            except Exception as e:
                print(f"Error statically parsing feeds: {e}")
        return feeds

    def log_eval(self, text):
        self.log_queue.put(("eval", text))

    def log_post(self, text):
        self.log_queue.put(("post", text))

    def read_log_queue(self):
        try:
            while True:
                target, msg = self.log_queue.get_nowait()
                text_widget = self.eval_text if target == "eval" else self.post_text
                if msg == '\r':
                    text_widget.delete("end-1c linestart", "end-1c")
                else:
                    text_widget.insert("end-1c", msg)
                    text_widget.see("end-1c")
        except queue.Empty:
            pass
        self.root.after(50, self.read_log_queue)

    def periodic_hud_refresh(self):
        try:
            self.refresh_hud_stats()
        except Exception:
            pass
        self.root.after(3000, self.periodic_hud_refresh)

    def read_stream(self, stream, target):
        buffer = []
        while True:
            char = stream.read(1)
            if not char:
                if buffer:
                    self.log_queue.put((target, "".join(buffer)))
                break
            if char == '\r':
                if buffer:
                    self.log_queue.put((target, "".join(buffer)))
                    buffer = []
                self.log_queue.put((target, '\r'))
            elif char == '\n':
                if buffer:
                    self.log_queue.put((target, "".join(buffer) + '\n'))
                    buffer = []
                else:
                    self.log_queue.put((target, '\n'))
            else:
                buffer.append(char)

    def build_ui(self):
        # Master padding container
        main_container = tk.Frame(self.root, bg=BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # ----------------- Left Panel (Controls - Scrollable Canvas) -----------------
        left_canvas = tk.Canvas(main_container, bg=BG_COLOR, highlightthickness=0)
        left_scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=left_canvas.yview)
        
        left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 2))
        left_scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        left_panel = tk.Frame(left_canvas, bg=BG_COLOR)
        left_canvas_window = left_canvas.create_window((0, 0), window=left_panel, anchor="nw")
        
        def on_frame_configure(event):
            left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        left_panel.bind("<Configure>", on_frame_configure)
        
        def on_canvas_configure(event):
            left_canvas.itemconfig(left_canvas_window, width=event.width)
        left_canvas.bind("<Configure>", on_canvas_configure)

        # Mousewheel scroll event handler
        def on_mousewheel(event):
            if left_canvas.winfo_exists():
                if event.delta:
                    left_canvas.yview_scroll(int(-3 * (event.delta / 120)), "units")
                elif event.num == 4:
                    left_canvas.yview_scroll(-3, "units")
                elif event.num == 5:
                    left_canvas.yview_scroll(3, "units")

        # Bind mousewheel to a widget and its children recursively (excluding scrollable components)
        def bind_mousewheel_recursive(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            widget.bind("<Button-4>", on_mousewheel)
            widget.bind("<Button-5>", on_mousewheel)
            for child in widget.winfo_children():
                if not isinstance(child, (tk.Text, tk.Entry, tk.Listbox)):
                    bind_mousewheel_recursive(child)

        # Title Card
        self.create_title_card(left_panel)

        # HUD (Pipeline Health & Stats)
        self.create_hud_card(left_panel)

        # Row 1: Actions Header Card
        self.create_actions_card(left_panel)

        # Row 2: Batch Evaluator Card
        self.create_batch_card(left_panel)

        # Row 3: Live Posting Card
        self.create_live_post_card(left_panel)

        # Apply mousewheel binding recursively
        bind_mousewheel_recursive(left_canvas)
        bind_mousewheel_recursive(left_panel)

        # ----------------- Right Panel (Dual Console Output) -----------------
        right_panel = tk.Frame(main_container, bg=BG_COLOR)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.create_eval_console_card(right_panel)
        self.create_post_console_card(right_panel)

    def create_title_card(self, parent):
        frame = tk.Frame(parent, bg=BG_COLOR)
        frame.pack(fill=tk.X, pady=(0, 12))

        # Show thumbnail next to the title if icon exists
        icon_path = "bluesky_bot/alethekanon.png"
        if os.path.exists(icon_path):
            try:
                self.icon_img_small = Image.open(icon_path).resize((48, 48), Image.Resampling.LANCZOS)
                self.tk_icon_small = ImageTk.PhotoImage(self.icon_img_small)
                lbl_icon = tk.Label(frame, image=self.tk_icon_small, bg=BG_COLOR)
                lbl_icon.pack(side=tk.LEFT, padx=(0, 12))
            except Exception as e:
                print(f"Failed to load small header icon: {e}")

        # Pack text in a sub-frame on the right of the icon
        text_frame = tk.Frame(frame, bg=BG_COLOR)
        text_frame.pack(side=tk.LEFT, fill=tk.Y)

        title = tk.Label(text_frame, text="ALETHEIA OPERATOR CONSOLE", font=("Segoe UI", 16, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        title.pack(anchor="w")

        subtitle = tk.Label(text_frame, text="Active Pipeline Control Room & Batch Runner", font=self.font_body, fg=TEXT_MUTED, bg=BG_COLOR)
        subtitle.pack(anchor="w")

    def create_hud_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.X, pady=(0, 10))

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=10)
        inner.pack(fill=tk.BOTH, expand=True)

        self.lbl_hud_bsky = tk.Label(inner, text="🦋 BSky Auth: CHECKING", font=self.font_body, bg=CARD_BG, fg=TEXT_MUTED)
        self.lbl_hud_bsky.pack(side=tk.LEFT, padx=(0, 20))

        self.lbl_hud_gemini = tk.Label(inner, text="♊ Gemini Engine: CHECKING", font=self.font_body, bg=CARD_BG, fg=TEXT_MUTED)
        self.lbl_hud_gemini.pack(side=tk.LEFT, padx=(0, 20))

        self.lbl_hud_live = tk.Label(inner, text="📂 Live Stories: --", font=self.font_body, bg=CARD_BG, fg=TEXT_MUTED)
        self.lbl_hud_live.pack(side=tk.LEFT, padx=(0, 20))

        self.lbl_hud_drafts = tk.Label(inner, text="📝 Drafts: --", font=self.font_body, bg=CARD_BG, fg=TEXT_MUTED)
        self.lbl_hud_drafts.pack(side=tk.LEFT, padx=(0, 20))

        self.lbl_hud_failed = tk.Label(inner, text="❌ Failed: --", font=self.font_body, bg=CARD_BG, fg=TEXT_MUTED)
        self.lbl_hud_failed.pack(side=tk.LEFT, padx=(0, 20))

        self.lbl_hud_queue = tk.Label(inner, text="📥 Queue: --", font=self.font_body, bg=CARD_BG, fg=TEXT_MUTED)
        self.lbl_hud_queue.pack(side=tk.LEFT)

    def refresh_hud_stats(self):
        # 1. Parse env vars
        env = {}
        env_path = "bluesky_bot/.env"
        if os.path.exists(env_path):
            try:
                with open(env_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            env[k.strip()] = v.strip()
            except Exception:
                pass
                
        bsky_ok = bool(env.get("BSKY_HANDLE") and env.get("BSKY_PASSWORD"))
        gemini_ok = bool(env.get("GEMINI_API_KEY"))
        
        # 2. Count files
        live_count = 0
        draft_count = 0
        fail_count = 0
        
        live_dir = "bluesky_bot/stories/live"
        if os.path.exists(live_dir):
            try:
                live_count = len([f for f in os.listdir(live_dir) if f.endswith(".json")])
            except Exception:
                pass
                
        stories_dir = "bluesky_bot/stories"
        if os.path.exists(stories_dir):
            try:
                # Exclude helper config files like index.json, filtered_candidates.json, harvested_candidates.json
                draft_count = len([
                    f for f in os.listdir(stories_dir) 
                    if f.endswith(".json") and (f.startswith("factcheck_") or f.startswith("story_"))
                ])
            except Exception:
                pass

        fail_dir = "bluesky_bot/stories/fail"
        if os.path.exists(fail_dir):
            try:
                fail_count = len([f for f in os.listdir(fail_dir) if f.endswith(".json")])
            except Exception:
                pass
                
        # 3. Update Labels
        if bsky_ok:
            self.lbl_hud_bsky.config(text="🦋 BSky Auth: ACTIVE", fg=SUCCESS_COLOR)
        else:
            self.lbl_hud_bsky.config(text="🦋 BSky Auth: MISSING", fg=DANGER_COLOR)
            
        if gemini_ok:
            self.lbl_hud_gemini.config(text="♊ Gemini Engine: ACTIVE", fg=SUCCESS_COLOR)
        else:
            self.lbl_hud_gemini.config(text="♊ Gemini Engine: MISSING", fg=DANGER_COLOR)
            
        self.lbl_hud_live.config(text=f"📂 Live: {live_count}", fg=ACCENT_CYAN)
        self.lbl_hud_drafts.config(text=f"📝 Drafts: {draft_count}", fg=WARNING_COLOR)
        self.lbl_hud_failed.config(text=f"❌ Failed: {fail_count}", fg=DANGER_COLOR)

        # Count harvested stories buffer (queue)
        queue_count = 0
        queue_path = "bluesky_bot/harvested_candidates.json"
        if os.path.exists(queue_path):
            try:
                with open(queue_path, "r", encoding="utf-8") as f:
                    q_data = json.load(f)
                    if isinstance(q_data, list):
                        queue_count = len(q_data)
            except Exception:
                pass
        self.lbl_hud_queue.config(text=f"📥 Queue: {queue_count}", fg=SUCCESS_COLOR)

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
            btn_frame, text="Open Control Panel (WebView)", font=self.font_body, bg=ACCENT_BLUE, fg=TEXT_COLOR,
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
        tk.Label(grid_frame, text="Categories: general, tech, business, politics, science, world (comma-separated is supported)", bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 7)).grid(row=4, column=1, columnspan=5, sticky="w")
        tk.Label(grid_frame, text="Suggested Topics: Trump, AI, Climate, Markets, AUKUS, Australia, Boeing, Space", bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 7)).grid(row=5, column=1, columnspan=5, sticky="w")

        self.val_son = tk.BooleanVar(value=False)
        self.chk_son = ttk.Checkbutton(grid_frame, text="Enable SON 6-Attractor Mode", variable=self.val_son)
        self.chk_son.grid(row=6, column=1, columnspan=2, sticky="w", pady=3)

        self.val_search = tk.BooleanVar(value=False)
        self.chk_search = ttk.Checkbutton(grid_frame, text="Enable Google Search Grounding", variable=self.val_search)
        self.chk_search.grid(row=6, column=3, columnspan=3, sticky="w", pady=3)

        # Model fallbacks selection frame with drag-and-drop ordering list
        model_frame = tk.Frame(inner, bg=CARD_BG)
        model_frame.pack(fill=tk.X, pady=(5, 5))
        
        # Split into left (checkboxes) and right (drag-and-drop listbox sequence)
        split_frame = tk.Frame(model_frame, bg=CARD_BG)
        split_frame.pack(fill=tk.X, anchor="w")
        
        chk_container = tk.Frame(split_frame, bg=CARD_BG)
        chk_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        tk.Label(chk_container, text="Active Models:", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG).pack(anchor="w", pady=(0, 4))
        for m in self.available_models:
            var = tk.BooleanVar(value=(m in self.selected_models))
            self.model_vars[m] = var
            chk = ttk.Checkbutton(chk_container, text=m, variable=var, command=lambda name=m: self.on_model_toggle(name))
            chk.pack(anchor="w", pady=2)
            
        list_container = tk.Frame(split_frame, bg=CARD_BG)
        list_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(list_container, text="Fallback Sequence (Drag & Drop items to reorder):", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG).pack(anchor="w", pady=(0, 4))
        
        self.lst_sequence = DragDropListbox(
            list_container, height=9, bg=BG_COLOR, fg=TEXT_COLOR, selectbackground=ACCENT_BLUE,
            selectforeground=TEXT_COLOR, font=self.font_body, relief="flat", borderwidth=0,
            highlightthickness=1, highlightbackground=BG_BUTTON
        )
        self.lst_sequence.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lst_sequence.on_reorder_callback = self.update_sequence_from_listbox
        
        # Populate Listbox in correct sequence
        for m in self.selected_models:
            self.lst_sequence.insert(tk.END, m)

        # RSS Feeds Selection Frame
        feeds_header = tk.Frame(inner, bg=CARD_BG)
        feeds_header.pack(fill=tk.X, pady=(10, 2))
        
        feeds_label = tk.Label(feeds_header, text="Active RSS Feeds (Deselect to exclude specific feeds):", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        feeds_label.pack(side=tk.LEFT)
        
        # Select All / Select None buttons
        def select_all_feeds():
            for var in self.feed_vars.values():
                var.set(True)
                
        def select_none_feeds():
            for var in self.feed_vars.values():
                var.set(False)
                
        btn_sel_all = tk.Button(feeds_header, text="Select All", font=("Segoe UI", 8), bg=BG_BUTTON, fg=TEXT_COLOR, relief="flat", borderwidth=0, padx=6, pady=2, cursor="hand2", command=select_all_feeds)
        btn_sel_all.pack(side=tk.RIGHT, padx=4)
        btn_sel_all.bind("<Enter>", lambda e: btn_sel_all.configure(bg=BG_BUTTON_HOVER))
        btn_sel_all.bind("<Leave>", lambda e: btn_sel_all.configure(bg=BG_BUTTON))
        
        btn_sel_none = tk.Button(feeds_header, text="Select None", font=("Segoe UI", 8), bg=BG_BUTTON, fg=TEXT_COLOR, relief="flat", borderwidth=0, padx=6, pady=2, cursor="hand2", command=select_none_feeds)
        btn_sel_none.pack(side=tk.RIGHT, padx=4)
        btn_sel_none.bind("<Enter>", lambda e: btn_sel_none.configure(bg=BG_BUTTON_HOVER))
        btn_sel_none.bind("<Leave>", lambda e: btn_sel_none.configure(bg=BG_BUTTON))

        feeds_container = tk.Frame(inner, bg=CARD_BG)
        feeds_container.pack(fill=tk.X, pady=(0, 8))
        
        canvas_frame = tk.Frame(feeds_container, bg=BG_COLOR, bd=1, relief="flat")
        canvas_frame.pack(fill=tk.X, expand=True)
        
        feeds_canvas = tk.Canvas(canvas_frame, bg=BG_COLOR, height=100, highlightthickness=0)
        feeds_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=feeds_canvas.yview)
        
        feeds_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        feeds_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        feeds_canvas.configure(yscrollcommand=feeds_scrollbar.set)
        
        scrollable_feeds_frame = tk.Frame(feeds_canvas, bg=BG_COLOR)
        feeds_canvas_window = feeds_canvas.create_window((0, 0), window=scrollable_feeds_frame, anchor="nw")
        
        def on_feeds_frame_configure(event):
            feeds_canvas.configure(scrollregion=feeds_canvas.bbox("all"))
        scrollable_feeds_frame.bind("<Configure>", on_feeds_frame_configure)
        
        def on_feeds_canvas_configure(event):
            feeds_canvas.itemconfig(feeds_canvas_window, width=event.width)
        feeds_canvas.bind("<Configure>", on_feeds_canvas_configure)
        
        # Sort feed names alphabetically
        sorted_feed_names = sorted(list(self.feed_definitions.keys()))
        self.feed_vars = {}
        
        # Layout in 3 columns
        num_cols = 3
        # Custom style for feeds checkbutton to match BG_COLOR of scroll container
        self.style.configure("Feeds.TCheckbutton", background=BG_COLOR, foreground=TEXT_COLOR, font=self.font_body)
        for idx, feed_name in enumerate(sorted_feed_names):
            row = idx // num_cols
            col = idx % num_cols
            var = tk.BooleanVar(value=True)
            self.feed_vars[feed_name] = var
            chk = ttk.Checkbutton(scrollable_feeds_frame, text=feed_name, variable=var, style="Feeds.TCheckbutton")
            chk.grid(row=row, column=col, sticky="w", padx=10, pady=2)
            
        # Mousewheel scroll event handler for feeds canvas
        def on_feeds_mousewheel(event):
            if feeds_canvas.winfo_exists():
                if event.delta:
                    feeds_canvas.yview_scroll(int(-2 * (event.delta / 120)), "units")
                elif event.num == 4:
                    feeds_canvas.yview_scroll(-2, "units")
                elif event.num == 5:
                    feeds_canvas.yview_scroll(2, "units")
                    
        def bind_feeds_mousewheel_recursive(widget):
            widget.bind("<MouseWheel>", on_feeds_mousewheel)
            widget.bind("<Button-4>", on_feeds_mousewheel)
            widget.bind("<Button-5>", on_feeds_mousewheel)
            for child in widget.winfo_children():
                bind_feeds_mousewheel_recursive(child)
                
        bind_feeds_mousewheel_recursive(feeds_canvas)

        # Additional Context Frame
        context_frame = tk.Frame(inner, bg=CARD_BG)
        context_frame.pack(fill=tk.X, pady=(5, 5))
        
        tk.Label(context_frame, text="Additional Context / Background Knowledge (injects into AI system prompt):", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG).pack(anchor="w", pady=(0, 4))
        
        ctx_txt_frame = tk.Frame(context_frame, bg=BG_COLOR)
        ctx_txt_frame.pack(fill=tk.X, expand=True)
        
        scrollbar_ctx = tk.Scrollbar(ctx_txt_frame)
        scrollbar_ctx.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.txt_context = tk.Text(
            ctx_txt_frame, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, height=3,
            font=self.font_body, relief="flat", borderwidth=0, yscrollcommand=scrollbar_ctx.set
        )
        self.txt_context.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollbar_ctx.config(command=self.txt_context.yview)

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

    def create_eval_console_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=10)
        inner.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(inner, bg=CARD_BG)
        header.pack(fill=tk.X, pady=(0, 6))

        lbl = tk.Label(header, text="Evaluator / Registry Output", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        lbl.pack(side=tk.LEFT)

        self.btn_kill_eval = tk.Button(
            header, text="Cancel Evaluator Action", font=self.font_body, bg=DANGER_COLOR, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=8, pady=2, cursor="hand2", command=self.kill_eval_process, state=tk.DISABLED
        )
        self.btn_kill_eval.pack(side=tk.RIGHT, padx=5)

        btn_clear = tk.Button(
            header, text="Clear", font=self.font_body, bg=BG_BUTTON, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=8, pady=2, cursor="hand2", command=self.clear_eval_console
        )
        btn_clear.pack(side=tk.RIGHT)

        txt_frame = tk.Frame(inner, bg=BG_COLOR)
        txt_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(txt_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.eval_text = tk.Text(
            txt_frame, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, height=13,
            font=self.font_console, relief="flat", borderwidth=0, yscrollcommand=scrollbar.set
        )
        self.eval_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.eval_text.yview)

    def create_post_console_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.BOTH, expand=True)

        inner = tk.Frame(card, bg=CARD_BG, padx=12, pady=10)
        inner.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(inner, bg=CARD_BG)
        header.pack(fill=tk.X, pady=(0, 6))

        lbl = tk.Label(header, text="Poster / Scheduler Output", font=self.font_subtitle, fg=ACCENT_CYAN, bg=CARD_BG)
        lbl.pack(side=tk.LEFT)

        self.btn_kill_post = tk.Button(
            header, text="Cancel Poster Action", font=self.font_body, bg=DANGER_COLOR, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=8, pady=2, cursor="hand2", command=self.kill_post_process, state=tk.DISABLED
        )
        self.btn_kill_post.pack(side=tk.RIGHT, padx=5)

        btn_clear = tk.Button(
            header, text="Clear", font=self.font_body, bg=BG_BUTTON, fg=TEXT_COLOR,
            relief="flat", borderwidth=0, padx=8, pady=2, cursor="hand2", command=self.clear_post_console
        )
        btn_clear.pack(side=tk.RIGHT)

        txt_frame = tk.Frame(inner, bg=BG_COLOR)
        txt_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(txt_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.post_text = tk.Text(
            txt_frame, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, height=13,
            font=self.font_console, relief="flat", borderwidth=0, yscrollcommand=scrollbar.set
        )
        self.post_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.post_text.yview)

    def ensure_local_server(self):
        PORT = 8000
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', PORT)) == 0:
                    return  # Already running
        except Exception:
            pass

        def run_server():
            import http.server
            import socketserver

            class QuietHandler(http.server.SimpleHTTPRequestHandler):
                def log_message(self, format, *args):
                    pass

            class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
                daemon_threads = True

            try:
                server = ThreadingHTTPServer(('localhost', PORT), QuietHandler)
                server.serve_forever()
            except Exception as e:
                print(f"Failed to start local HTTP server: {e}")

        t = threading.Thread(target=run_server, daemon=True)
        t.start()

    def open_control_panel(self):
        self.ensure_local_server()
        python_bin = self.get_python_bin()
        url = "http://localhost:8000/bluesky_bot/control_panel.html"
        
        # Run pywebview inside a separate background python process to avoid GUI thread deadlocks
        code = f"import webview; webview.create_window('Aletheia Control Panel', '{url}', width=1400, height=850); webview.start()"
        
        subprocess.Popen(
            [python_bin, "-c", code],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

    def clear_eval_console(self):
        self.eval_text.delete("1.0", tk.END)

    def clear_post_console(self):
        self.post_text.delete("1.0", tk.END)

    def set_eval_running(self, running):
        if running:
            self.btn_run_batch.configure(state=tk.DISABLED)
            self.btn_rebuild.configure(state=tk.DISABLED)
            self.btn_kill_eval.configure(state=tk.NORMAL)
        else:
            self.btn_run_batch.configure(state=tk.NORMAL)
            self.btn_rebuild.configure(state=tk.NORMAL)
            self.btn_kill_eval.configure(state=tk.DISABLED)
            self.root.after(1, self.refresh_hud_stats)

    def set_post_running(self, running):
        if running:
            self.btn_run_live.configure(state=tk.DISABLED)
            self.btn_kill_post.configure(state=tk.NORMAL)
        else:
            self.btn_run_live.configure(state=tk.NORMAL)
            self.btn_kill_post.configure(state=tk.DISABLED)
            self.root.after(1, self.refresh_hud_stats)

    def run_eval_subprocess_async(self, cmd_args):
        self.set_eval_running(True)
        def worker():
            try:
                self.log_eval(f"\n> Running: {' '.join(cmd_args)}\n")
                self.eval_process = subprocess.Popen(
                    cmd_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                self.read_stream(self.eval_process.stdout, "eval")
                self.eval_process.wait()
                self.log_eval(f"\n--- Process finished with exit code {self.eval_process.returncode} ---\n")
            except Exception as e:
                self.log_eval(f"\nError running process: {e}\n")
            finally:
                self.eval_process = None
                self.root.after(1, lambda: self.set_eval_running(False))
        threading.Thread(target=worker, daemon=True).start()

    def kill_eval_process(self):
        if self.eval_process:
            self.log_eval("\n*** Terminating evaluator process... ***\n")
            self.eval_process.terminate()

    def kill_post_process(self):
        if self.post_process:
            self.log_post("\n*** Terminating poster process... ***\n")
            self.post_process.terminate()

    def run_rebuild_store(self):
        python_bin = self.get_python_bin()
        self.run_eval_subprocess_async([python_bin, "-u", "bluesky_bot/rebuild_registries.py"])

    def update_sequence_from_listbox(self):
        self.selected_models = list(self.lst_sequence.get(0, tk.END))

    def on_model_toggle(self, model_name):
        var_val = self.model_vars[model_name].get()
        if var_val:
            if model_name not in self.selected_models:
                self.selected_models.append(model_name)
                self.lst_sequence.insert(tk.END, model_name)
        else:
            if model_name in self.selected_models:
                self.selected_models.remove(model_name)
                try:
                    idx = list(self.lst_sequence.get(0, tk.END)).index(model_name)
                    self.lst_sequence.delete(idx)
                except ValueError:
                    pass

    def run_one_shot_batch(self):
        python_bin = self.get_python_bin()
        args = [
            python_bin, "-u",
            "bluesky_bot/google_ai_studio_one_shot.py",
            "--rss", self.ent_rss.get().strip(),
            "--bsky", self.ent_bsky.get().strip(),
        ]
        
        enabled_feeds = [name for name, var in self.feed_vars.items() if var.get()]
        if len(enabled_feeds) < len(self.feed_definitions):
            args.extend(["--enabled-feeds", ",".join(enabled_feeds)])
            
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

        if self.val_son.get():
            args.append("--son")

        if self.val_search.get():
            args.append("--search")

        context_val = self.txt_context.get("1.0", "end-1c").strip()
        if context_val:
            args.extend(["--context", context_val])

        if self.selected_models:
            args.extend(["--model", self.selected_models[0]])
            args.extend(["--model-sequence", ",".join(self.selected_models)])

        self.run_eval_subprocess_async(args)

    def run_live_post(self):
        python_bin = self.get_python_bin()
        self.set_post_running(True)

        def posting_flow():
            try:
                # Step 1: Pre-flight validation
                self.log_post("\n> Running Pre-Flight Validation...\n")
                val_proc = subprocess.Popen(
                    [python_bin, "-u", "bluesky_bot/validate_batch.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                self.post_process = val_proc
                self.read_stream(val_proc.stdout, "post")
                val_proc.wait()

                if val_proc.returncode != 0:
                    self.log_post("\n==================================================\n")
                    self.log_post("ERROR: Pre-flight validation failed! Posting aborted.\n")
                    self.log_post("==================================================\n")
                    return

                # Step 2: Post batch
                self.log_post("\n> Validation passed! Scheduling live batch posting...\n")
                args = [python_bin, "-u", "bluesky_bot/post_batch.py", "--live"]
                
                min_delay = self.ent_min_delay.get().strip()
                if min_delay:
                    args.extend(["--min-delay", min_delay])
                    
                max_delay = self.ent_max_delay.get().strip()
                if max_delay:
                    args.extend(["--max-delay", max_delay])
                    
                if self.val_watch.get():
                    args.append("--watch")

                self.log_post(f"> Command: {' '.join(args)}\n")
                post_proc = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                self.post_process = post_proc
                self.read_stream(post_proc.stdout, "post")
                post_proc.wait()
                self.log_post(f"\n--- Live scheduler completed (exit code: {post_proc.returncode}) ---\n")

            except Exception as e:
                self.log_post(f"\nError running live posting flow: {e}\n")
            finally:
                self.post_process = None
                self.root.after(1, lambda: self.set_post_running(False))

        threading.Thread(target=posting_flow, daemon=True).start()

if __name__ == "__main__":
    # Ensure correct working directory context
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    root = tk.Tk()
    app = AletheiaLauncherApp(root)
    root.mainloop()
