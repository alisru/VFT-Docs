# 01. Overview & Features

## What is Chat Context?

**Chat Context** is an offline personal library and search engine for AI chats. It connects directly to your web browser (**Google Gemini, Anthropic Claude, and OpenAI ChatGPT**) and local files (Antigravity conversation logs, JSON backups, and offline HTML saves), storing every turn, code snippet, and document in a single, fast local database.

Instead of your work getting buried across dozens of browser tabs and chat histories, Chat Context makes all your past conversations instantly searchable, linkable, and exportable.

---

## The Problems It Solves

| Problem | What Usually Happens | How Chat Context Solves It |
| :--- | :--- | :--- |
| **Lost Ideas** | You remember talking about a specific concept weeks ago, but search returns nothing because you don't remember the exact phrasing. | **Hybrid Semantic Search** matches the *meaning* of your question using local AI embeddings, not just keywords. |
| **Virtualization Loss** | Long Gemini chats unload earlier messages to save browser memory. If you save the page, you only get the bottom messages. | **Cumulative Non-Destructive Merging** keeps every message ever seen and only appends new turns. |
| **Scattered Documents** | Canvases, markdown tables, and plans written by AI stay trapped inside the chat UI. | **Living Canvases Engine** automatically extracts canvases into clean Markdown files and pushes them to Git and Google Drive. |
| **Context Switching** | Starting a new chat requires manually re-explaining background context and copying old notes. | **Context Packs** let you tick 2-3 past chats, enter your new goal, and generate a tight prompt excerpt ready to paste. |
| **Platform Lock-In** | Exporting your data is difficult or produces messy files. | **Export Suite** downloads any chat or all 300+ chats at once as clean Markdown, HTML, JSON, or ZIP archives. |

---

## Core Features Breakdown

### 1. Silent, Automatic Live Sync
- Runs inside Google Gemini web tabs via a lightweight Chrome Extension.
- Automatically captures user prompts and model responses as they appear.
- Shows a discreet status indicator at the bottom-right of the page:
  - **`Context`** (Gray): Extension active and ready.
  - **`Syncing...`** (Yellow): Ingesting new messages.
  - **`Synced (N)`** (Green): All turns successfully saved to your local database.
- Completely immune to page Content Security Policy (CSP) because network traffic routes through the extension's background service worker.

### 2. Guaranteed Non-Destructive History
- Built on a strict principle: **Chat data is never deleted.**
- If you scroll to the bottom of a 200-message chat where Gemini's web client unmounts turns 1 through 50 from the DOM, Chat Context does not overwrite your database with the partial view.
- It normalizes incoming turns, aligns them with existing history, and merges new messages onto the end.

### 3. Hybrid Semantic & Full-Text Search Engine
- **Full-Text Keyword Search (SQLite FTS5)**: Finds exact words, filenames, technical symbols, and specific codes instantly.
- **Semantic Meaning Search (Local Vector Embeddings)**: Uses a local MiniLM embedding model to find relevant chunks even when completely different words are used.
- **Search Controls**:
  - **Search Modes**: `Hybrid` (balanced blend), `Semantic` (pure conceptual match), or `Text` (pure exact keyword match).
  - **Grouping Modes**: Group by `Chat` (one clean card per conversation) or by `Paragraph` (individual excerpts).
  - **Sorting**: Sort results by `Relevance`, `Newest First`, or `Oldest First`.
  - **Faceted Filters**: Filter by specific Topic, by Source (Gemini, Antigravity, Claude, ChatGPT), or by mandatory required keywords (`Must contain`).

### 4. In-Page Context Drawer (Alt+C)
- Press **Alt+C** inside Gemini to slide open an offline context drawer directly on top of the web page.
- Search your local knowledge base without opening a new tab or leaving your active work.
- Click **"Inject into prompt"** to insert reference excerpts directly into Gemini's input box with properly formatted citations.

### 5. Living Canvases & Cloud Backup
- When Gemini outputs a Canvas or long-form document, Chat Context automatically pulls the raw markdown out of the DOM.
- Saves the canvas to disk in `chat_context/canvases/<Chat_Name>/<Canvas_Title>.md`.
- Cleans UI artifacts (like stray "Share & Export" buttons) from headers and titles.
- Automatically commits new canvas versions to a local Git repository and syncs them as native Google Docs to Google Drive.

### 6. Context Packs for Prompt Engineering
- Select any combination of past chats using checkboxes in the dashboard.
- Enter an optional question or research goal.
- Chat Context extracts the most relevant paragraphs from those chats and formats a dense, prompt-ready context block:
  ```
  === CONTEXT FROM PREVIOUS RESEARCH ===
  [Chat: Vector Field Theory - Genesis 1]
  ...most relevant excerpts...
  ```
- Click **Copy context pack** and paste it directly into a new chat to instantly transfer background knowledge.

### 7. Multi-Format Export Suite
- **Single Chat Export**:
  - **Markdown (`.md`)**: Complete YAML frontmatter, metadata header, attached canvases list, and role timestamps.
  - **Standalone HTML (`.html`)**: Beautiful dark-mode design with KaTeX math rendering, syntax-highlighted code blocks, and print styling (Save to PDF).
  - **JSON (`.json`)**: Raw structured export.
  - **Plain Text (`.txt`)**: Clean text transcript.
  - **ZIP Archive (`.zip`)**: Bundles the chat and all its markdown canvases into a zip file.
- **Bulk Export ("Export All")**:
  - **ZIP by Topic**: Downloads your entire conversation library into organized folders by topic name (`Topic/Chat_Title.md`).
  - **ZIP Flat**: Downloads all chats into a single flat folder.
  - **JSON Bundle**: Consolidated JSON file containing all chats and turns.
  - **Export Selected**: Tick any set of chats and download just those selected items as a ZIP archive.

### 8. 100% Offline & Private
- The server runs on `http://127.0.0.1:8765`.
- The database is a local SQLite file (`data/chats.sqlite`).
- Text embeddings run on your CPU using local Python libraries (`sentence-transformers`).
- No external cloud services or third-party APIs are required to store, search, or export your conversations.
