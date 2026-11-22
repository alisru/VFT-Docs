# 02. User Guide

This guide walks you through installing, running, and using **Chat Context** step by step.

---

## 1. System Requirements & Hardware Footprint

Chat Context is engineered to run quietly in the background without needing a dedicated GPU or high-end workstation.

| Resource | Minimum | Recommended | Details / Operational Notes |
| :--- | :--- | :--- | :--- |
| **RAM (Idle)** | ~50 MB | ~80 MB | Bare FastAPI daemon listening on `127.0.0.1:8765`. |
| **RAM (Active)** | ~250 MB | < 450 MB peak | Active semantic search and embedding generation. Memory is capped by restricting ONNX Runtime to 2 threads (`threads=2`, `batch_size=32`), preventing core-scaling memory leaks. |
| **CPU** | Any dual-core 64-bit | Modern 4+ core CPU | Intel Core, AMD Ryzen, Apple Silicon (M1–M4), or ARM64 (Raspberry Pi 4/5). **No dedicated GPU required**. |
| **Disk Storage** | ~300 MB | ~500 MB | ~15 MB for application code + ~130 MB for the cached local ONNX embedding model (`bge-small-en-v1.5`) + ~20-50 MB for a typical 500+ conversation database. |
| **Python** | Python 3.10 | Python 3.11 / 3.12 | Standard CPython virtual environment (`venv`). |
| **Operating System** | Windows 10/11 | Windows, macOS, Linux | Cross-platform compatible. |
| **Network** | Offline-capable | One-time model download | Only requires internet once during the initial launch to cache the embedding model (~130 MB). After that, 100% offline. |
| **Web Browser** | Chromium browser | Chrome, Brave, Edge, Arc | Any Chromium-based browser supporting Manifest V3 extensions. |

---

## 2. Dependencies & Environment

Chat Context is engineered to be lightweight, fast, and local-first. All dependencies are recorded in [`requirements.txt`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/requirements.txt):

| Package | Version | Purpose |
| :--- | :--- | :--- |
| **`fastapi`** | `>=0.110.0` | Asynchronous REST API framework powering the local daemon (`http://127.0.0.1:8765`), handling live turn sync, searches, context injections, and export streams. |
| **`uvicorn`** | `>=0.28.0` | High-performance ASGI server running the FastAPI daemon locally. |
| **`fastembed`** | `>=0.2.0` | High-speed, local ONNX vector embedding engine. Runs `BAAI/bge-small-en-v1.5` offline on CPU with capped memory threads (<450MB RAM) without bulky PyTorch overhead. |
| **`numpy`** | `>=1.24.0` | Optimized vector array mathematics, L2 normalization, and cosine similarity ranking. |
| **`beautifulsoup4`** | `>=4.12.0` | Resilient HTML parser used by the offline importer (`ctx/importers.py`) to extract chat turns from raw browser page dumps (Gemini, Claude, ChatGPT). |

### Built-in Standard Library Modules Used
No extra installation required for core persistence and operating system integration:
- `sqlite3`: Local ACID database with FTS5 full-text search triggers.
- `zipfile`, `io`, `pathlib`: In-memory archive creation and cross-platform file paths for the bulk export suite.
- `re`, `urllib.parse`, `hashlib`: Canonical URL deduplication, identifier hashing, and message cleaning.

---

## 3. Installation & Setup

### Step A: Set Up the Python Environment
From the `chat_context` project directory in your terminal or PowerShell:

```powershell
# Navigate to the chat_context directory
cd "e:\Vector Field Theory\VFT Docs\chat_context"

# Create a virtual environment (if not already created)
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Install all required dependencies
pip install -r requirements.txt
```

### Step B: (Optional) Configure Cloud Sync & Backups
If you wish to automatically sync markdown canvases to Google Drive (as native Google Docs) or back them up to a private GitHub repository, run the interactive setup wizard:

```powershell
python setup_sync.py
```
The wizard will:
1. Detect whether `git`, `rclone`, and `pandoc` are installed on your machine.
2. Ask if you want to enable Git auto-backup for canvases, set your repository URL, and initialize the `canvases/` directory.
3. Ask if you want to enable Google Drive sync via `rclone`, and configure your target folder and remote.
4. Save everything to a private, git-ignored [`config.json`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/config.json).

To check your current sync status at any time, run:
```powershell
python setup_sync.py --status
```

> [!NOTE]
> Cloud sync is completely optional. If you don't run the wizard, Chat Context works fully offline on your local machine with zero external connections.

### Step C: Start the Server
Start the local server daemon:

```powershell
python -m ctx.server
```

You should see output indicating the server has started:
```text
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8765 (Press CTRL+C to quit)
```

The server runs on `http://127.0.0.1:8765`.

---

## 4. Installing the Chrome Extension

1. Open your Chromium browser (Chrome, Brave, Edge).
2. In the URL bar, go to:
   ```text
   chrome://extensions
   ```
3. In the top-right corner, turn on the **Developer mode** toggle.
4. Click the **Load unpacked** button in the top-left corner.
5. In the file picker, select the following folder:
   ```text
   chat_context\extension\chrome_extension
   ```
6. The extension **"Chat Context Sync"** will appear in your extensions list.

---

## 5. Using the In-Page Context Drawer (Gemini, Claude, ChatGPT)

When you visit [gemini.google.com](https://gemini.google.com), [claude.ai](https://claude.ai), or [chatgpt.com](https://chatgpt.com):

1. **Check the Status Widget**:
   Look at the bottom-right corner of the web page. You will see a small pill widget with a dot and label:
   - **`Context`** (Gray): Extension is listening.
   - **`Syncing...`** (Yellow): Saving turns to your local database.
   - **`Synced (N)`** (Green): All messages are safely stored.
2. **Open the Drawer (Alt+C)**:
   Press **Alt+C** on your keyboard (or click the widget). A dark side drawer will slide in from the right.
3. **Drawer Tabs**:
   - **Related**: Shows conversations in your library conceptually related to your current chat.
   - **Search**: Search across your entire local database without leaving the page.
   - **Canvases**: View recent markdown documents and code artifacts generated across all chats.
   - **Topics**: Browse conversations by subject cluster.
4. **Inject Context into Your Prompt**:
   In any search result inside the drawer, click **"Inject into prompt"**. The snippet will be formatted with clear citations and inserted directly into the AI prompt box.
5. **Direct Export**:
   Click the **Export** button on the bottom-right widget to instantly download the open conversation as Markdown.

---

## 6. Using the Web Dashboard

Open `http://127.0.0.1:8765` in your browser. The dashboard is divided into three panels:

### Left Panel: Navigation & Topics
- **Tabs**: Switch between **Recent** (newest chats), **All** (every conversation), and **Topics** (clustered subjects).
- **Topic Sorting**: Sort your topic clusters by **Recent** (topics with recently updated chats first), **Name** (A–Z), or **Count** (largest clusters first).
- **Checkboxes**: Tick the checkbox next to any conversation to select it for Context Packing or Bulk Export.

### Middle Panel: Chat Viewer & Actions
- Click any chat in the list to open it.
- **Actions Bar**:
  - **Move to topic**: Reassign the conversation to another topic or type a new topic name.
  - **🔗 Open on Web**: Direct link to open the live conversation on the web platform.
  - **Export Chips**: Instant 1-click download buttons:
    - **`[Markdown]`**: `.md` file with YAML frontmatter.
    - **`[HTML]`**: Standalone dark-mode HTML file (supports browser printing to PDF).
    - **`[JSON]`**: Raw structured data.
    - **`[TXT]`**: Plain text transcript.
    - **`[ZIP]`**: Zip containing the chat markdown and all attached canvases.

### Right Panel: Related Conversations
- Shows the top 5 most conceptually similar conversations from your library. Click any item to jump straight to it.

---

## 7. How to Search Like a Pro

At the top of the dashboard, enter any query and press **Enter**. A dedicated search control bar will appear:

| Control | Options | What It Does |
| :--- | :--- | :--- |
| **Search Mode** | `Hybrid`, `Semantic`, `Text` | `Hybrid` blends exact words and conceptual meaning. `Semantic` matches pure meaning. `Text` searches literal words using SQLite FTS5. |
| **Grouping** | `Chat`, `Paragraph` | `Chat` rolls all matches up into one card per conversation. `Paragraph` shows individual matching paragraphs. |
| **Sorting** | `Relevance`, `Newest`, `Oldest` | Rank by matching score, or sort chronologically to find recent research. |
| **Topic Filter** | Any Topic | Restricts your search to a specific subject cluster. |
| **Source Filter** | `Gemini`, `Claude`, `ChatGPT`, `Antigravity` | Limits search to a specific AI tool or export source. |
| **Must Contain** | Keyword string | Enforces that results *must* contain an exact word or phrase. |

---

## 8. How to Export Your Data

### Option A: Export a Single Chat
- In the Web Dashboard: Open the chat, and click any chip in the **Export:** bar (`Markdown`, `HTML`, `JSON`, `TXT`, `ZIP`).
- In the Web Interface: Click the **Export** button on the bottom-right extension widget.

### Option B: Export All Chats in One Click
1. Look at the top header of the Web Dashboard.
2. Click **`📥 Export All ▾`**.
3. Choose your preferred format:
   - **`📦 All Chats (ZIP, by Topic)`**: Creates a zip file organized by topic folders (`Topic/Chat_Title.md`).
   - **`📦 All Chats (ZIP, Flat)`**: Creates a zip file with all chats in a single directory.
   - **`📄 All Chats (JSON Bundle)`**: Creates a single comprehensive JSON file.

### Option C: Export Selected Chats
1. Tick the checkboxes next to any chats in the sidebar or search results.
2. In the bottom footer bar, click the blue button:
   ```text
   📦 Export Selected (N)
   ```
3. A zip file containing only those selected conversations will download immediately.

### Option D: Export from the Command Line (CLI)
From your terminal in `chat_context`:

```powershell
# Export all chats to a ZIP
python -m ctx.export --all --format zip --out ./exports

# Export all chats to a single JSON file
python -m ctx.export --all --format json --out ./exports/all_chats.json

# Export a single chat by its ID
python -m ctx.export --chat gemini-424c86baff31945d --format html --out ./exports
```

---

## 9. Troubleshooting FAQ

#### Q: The extension says "Server offline".
- Make sure the Python server is running in your terminal (`python -m ctx.server`).
- Visit `http://127.0.0.1:8765/api/status` in your browser. It should return a JSON status object.

#### Q: I updated the extension files, but my tab isn't updating.
- Go to `chrome://extensions` and click the circular **Reload** icon on the Chat Context card.
- Refresh your Gemini tab.

#### Q: Why didn't a newly opened conversation sync immediately?
- Gemini loads conversations dynamically. Chat Context automatically syncs 2 seconds after messages appear or when switching conversations. You can also click **"Sync Now"** on the widget.
