# Plan 001 – Chat Context (semantic chat notebook) – 2026-10-04

Historic log. Never overwrite; add plan_002, plan_003 etc.

## Goal
Local tool that captures AI chats, links them by meaning, and lets the user
(a) browse them in a dashboard (sidebar topics > chats, big reader pane),
(b) search across all chats, (c) build a paste-ready context pack for any other AI.

## Decisions (from chat)
- Fully local. No AI Studio / cloud API calls. Embeddings run on this PC.
- Semantic linking is the core (embeddings), not keywords only.
- Chats form a graph: auto-suggested links + clusters, user can correct.
- Source 1: Antigravity transcripts (already on disk). Later: Gemini (Takeout, extension), others.
- Folder: `chat_context/` (this one).

## Stack
- Python 3.13, venv at `chat_context/.venv`
- SQLite (chats, messages, chunks, links, topics) + embeddings stored as float32 blobs, cosine via numpy
- `fastembed` (ONNX, small, no torch) with `BAAI/bge-small-en-v1.5`
- FastAPI + uvicorn, single-page HTML UI (no build step)

## Layout
- `chat_context/ctx/` – python package (db, ingest, embed, link, server)
- `chat_context/ui/index.html` – dashboard
- `chat_context/data/` – chats.sqlite (gitignore-able)
- `chat_context/inbox/` – drop folder for exports (later)
- `chat_context/plans/` – this log

## Steps
1. [ ] venv + deps
2. [ ] db schema
3. [ ] Antigravity ingest (transcript.jsonl -> chats/messages; user + model text only)
4. [ ] chunk + embed
5. [ ] link/cluster (kNN between chats, topic clusters, user rename/merge)
6. [ ] server + API: list, chat, search, related, context-pack
7. [ ] UI per wireframes (Recent/All, topic tree, reader, related panel, pack tray)
8. [ ] Gemini importer (after user picks capture method)

## Notes / run log
- 2026-10-04: 181 brain folders, 75 with transcript.jsonl. Python 3.13.3 available.
- MyChatArchive checked: no Gemini import (README saved: fetch_mychatarchive_readme_20261004.md).
