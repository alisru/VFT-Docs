# Chat Context — Complete Documentation Pack

> A fast, private, offline-first personal search engine and context management system for AI conversations (Gemini, Claude, ChatGPT, Antigravity).

---

## Welcome to Chat Context

**Chat Context** is a personal software tool that automatically captures, organizes, and searches your AI conversations completely locally on your own computer.

If you use AI assistants like Google Gemini, Claude, or ChatGPT for serious work, research, coding, or writing, you quickly run into major problems:
- **Lost knowledge**: Conversations vanish into massive sidebars where you can't search them properly.
- **Surface-level search**: Standard search only finds exact words, missing ideas, concepts, and related thoughts.
- **Vanishing history**: Gemini Web virtualizes long conversations, meaning earlier messages get hidden or unmounted.
- **Context fragmentation**: When you want to bring knowledge from an older chat into a new conversation, you have to scroll, copy, paste, and reformat manually.
- **Data lock-in**: Exporting your conversations in clean Markdown, HTML, JSON, or ZIP archives is either clumsy or impossible.

**Chat Context solves all of this.** It runs quietly on your machine, syncs your conversations as you chat, indexes every paragraph with local AI embeddings and full-text search, organizes chats into dynamic topics, and lets you export or inject context anywhere in one click.

---

## Documentation Pack Directory

This pack contains four detailed guides covering every aspect of the project:

| Guide | Description |
| :--- | :--- |
| [**01. Overview & Features**](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/docs/01_OVERVIEW_AND_FEATURES.md) | What Chat Context does, who it's for, and complete breakdown of core features. |
| [**02. User Guide**](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/docs/02_USER_GUIDE.md) | How to install, run the server, load the Chrome extension, use the dashboard, and export chats. |
| [**03. Architecture & How It Works**](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/docs/03_ARCHITECTURE_AND_HOW_IT_WORKS.md) | Technical architecture: database design, hybrid vector + keyword search, extension mechanics, and data flow. |
| [**04. How It Was Made**](file:///e:/Vector%20Field%20Theory/VFT%20Docs/chat_context/docs/04_HOW_IT_WAS_MADE.md) | The engineering journey: solving DOM virtualization, fixing SQLite FTS5 bugs, and building non-destructive cumulative sync. |

---

## Quick Summary

- **100% Local & Private**: All data is saved in a local SQLite database (`data/chats.sqlite`). No chat data ever leaves your computer.
- **Zero-Friction Live Sync**: The browser extension silently captures chats as you type and read. You never have to manually click save.
- **Never Deletes History**: Even if Google unmounts earlier turns in long chats, Chat Context merges new turns cumulatively without erasing history.
- **Smart Semantic & Keyword Search**: Search across 300+ chats using exact phrases or conceptual meaning. Sort by relevance or recency.
- **Living Canvases Repository**: Extracts markdown artifacts and canvases into clean markdown files and syncs them automatically to Git and Google Drive.
- **Complete Export Suite**: Export individual chats or your entire conversation library into Markdown, standalone HTML, JSON, Plain Text, or structured ZIP archives.

---

## System Requirements & Resource Footprint

Chat Context is engineered to run quietly in the background on low-power laptops, development workstations, or home servers without needing a dedicated GPU or heavy cloud infrastructure:

| Resource | Minimum | Recommended | Operational Profile |
| :--- | :--- | :--- | :--- |
| **RAM (Idle)** | ~50 MB | ~80 MB | Lightweight FastAPI daemon listening on localhost (`127.0.0.1:8765`). |
| **RAM (Active)** | ~250 MB | < 450 MB peak | Semantic search & embedding queries. Memory is strictly capped by limiting ONNX Runtime to 2 worker threads (`threads=2`, `batch_size=32`) to eliminate thread arena bloat. |
| **CPU** | Any dual-core 64-bit | Modern 4+ core CPU | Intel, AMD, Apple Silicon (M1/M2/M3/M4), or ARM64 (Raspberry Pi 4/5). **No dedicated GPU required**. |
| **Disk Storage** | ~300 MB | ~500 MB | ~15 MB codebase + ~130 MB one-time cached ONNX embedding model (`bge-small-en-v1.5`) + ~20-50 MB for typical SQLite conversation library (500+ chats). |
| **Python** | Python 3.10 | Python 3.11 / 3.12 | Standard CPython virtual environment. |
| **Operating System** | Windows 10/11 | Windows, macOS, Linux | Cross-platform POSIX and Windows compatible paths. |
| **Network** | Offline | One-time model fetch | Only requires internet once during the initial run to cache the embedding model weights from Hugging Face (~130 MB). After that, 100% offline. |
| **Browser** | Chromium browser | Chrome, Brave, Edge, Arc | Any modern Chromium browser supporting Manifest V3 extensions. |

---

## Quick Start (3 Steps)

1. **Install dependencies & start the local server**:
   ```powershell
   cd "chat_context"
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt

   # (Optional) Run the Cloud Sync Setup Wizard for Google Drive / Git backups
   python setup_sync.py

   # Start the daemon
   python -m ctx.server
   ```
2. **Load the extension**:
   Open Chrome, go to `chrome://extensions`, enable **Developer mode**, click **Load unpacked**, and choose `chat_context/extension/chrome_extension`.
3. **Open the Dashboard**:
   Visit `http://127.0.0.1:8765` in your browser. All your chats, topics, and search tools are right there.

---

## Project Origins & Collaborative Partnership

Chat Context is the product of an intensive, real-time pair programming partnership between a human researcher/engineer and **Antigravity** (Google DeepMind's agentic AI assistant).

### How We Built This Together
- **The Human Partner**:
  - Defined the core architectural principles (zero data deletion, offline-first local ownership, and anti-overengineering).
  - Subjected the system to brutal real-world stress tests with massive research chat logs across Gemini, Claude, and ChatGPT.
  - Extracted live DOM checkpoints, memory state dumps, and SQLite snapshots when edge cases occurred.
  - Demanded absolute reliability: ensuring the engine works as an intuitive extension of thought rather than a fragile toy.
- **Antigravity (The AI Partner)**:
  - Co-architected the dual-engine search pipeline (blending SQLite FTS5 BM25 with local 384-dimensional dense vectors).
  - Reverse-engineered frontend DOM virtualization across Gemini, Claude, and ChatGPT to build sequence-aligned cumulative ingestion.
  - Diagnosed and resolved low-level SQLite FTS5 trigger corruptions and foreign key execution order deadlocks.
  - Carved lost message turns directly from the SQLite database's unallocated binary freelist after early virtualization bugs.
  - Built the multi-format export suite, CLI tools, automated documentation pack, and test harnesses.
