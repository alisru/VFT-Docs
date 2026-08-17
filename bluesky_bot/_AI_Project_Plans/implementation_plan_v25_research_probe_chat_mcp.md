# Live Multimodal Actualism Chatbot, Vertex AI Integration, Persistent Memory, Upload Tools & Research Probe (Intent 77)

## Overview

This implementation adds full live LLM conversational reasoning, Google Cloud Vertex AI support, multi-session persistent memory, multimodal document/file uploads, and automated policy ledger tracking to the Aletheia Bot ecosystem:

1. **Live Gemini & Vertex AI Chatbot (`chat_server.py`)**:
   - Executes live API calls with Google GenAI SDK.
   - Supports AI Studio (`gemini-3.7-flash`, `gemini-3.5-flash`, `gemini-2.5-flash`, `gemini-2.5-pro`) and Vertex AI (`vertex:gemini-3.7-flash`, `vertex:gemini-3.5-flash`, `vertex:gemini-2.5-flash`, `vertex:gemini-3.1-flash-lite`).
   - Injected with in-memory RAG grounding over all 8,640+ evaluated stories and the 21-domain policy ledger.
   - Google Search Grounding enabled for live web verification.

2. **Persistent Multi-Session Memory (`chat_sessions/` & `memory_profile.json`)**:
   - Saves conversations to `bluesky_bot/chat_sessions/session_<id>.json`.
   - Multi-session sidebar in `aletheia_chat.html` allowing `+ New Chat`, switching between historical conversations, and deleting old sessions.
   - Maintains long-term memory notes and key operator preferences across chats.

3. **Multimodal Upload Tools (`chat_uploads/`)**:
   - Supports uploading PDF, Markdown, Text, CSV, JSON, and Images directly into the chat.
   - Drag-and-drop overlay on the chat window or `📎` attachment button.
   - Backend extracts document content or passes image bytes to Gemini/Vertex vision for live Actualism auditing and $(υ, \psi)$ coordinate estimation.

4. **Research Probe Mode (`research_probe.py` / `--probe` CLI)**:
   - Evaluates historical events and specific policy moments (e.g. `"Hitler 1933"`, `"Thatcher privatisation"`).
   - Searches Wikipedia REST summaries and DuckDuckGo HTML scraping.

5. **Deterministic Policy Ledger (`policy_extract.py` / `policy_ledger.json`)**:
   - Auto-detects 20+ policy domains from story subjects and post content.
   - Automatically maintains running coordinate averages (`avg_real_u`, `avg_real_psi`) in `policy_ledger.json` on every registry rebuild.
   - CLI report tool via `google_ai_studio_one_shot.py --policy-report`.

6. **FastMCP Server (`aletheia_mcp_server.py`)**:
   - Python FastMCP server exposing story search, story fetching, moral averages, trajectory breakdowns, policy reports, and resources (`aletheia://registry`, `aletheia://policy-ledger`, `aletheia://moral-report`) via stdio.

7. **Aletheia Launcher Integration (`AletheiaLauncher.pyw`)**:
   - "🔍 Research Probe & Historical Audits" card.
   - "💬 Open Chat UI" and "📋 Policy Ledger" quick action buttons.

---

## File Architecture

| File | Status | Description |
|---|---|---|
| `bluesky_bot/chat_server.py` | UPGRADED | Live LLM API server (Gemini + Vertex) with persistent memory & uploads |
| `bluesky_bot/aletheia_chat.html` | UPGRADED | Dark-mode chat UI with session history, upload tools, model select |
| `bluesky_bot/chat_sessions/` | NEW DIR | Persistent JSON storage for multi-turn chat sessions |
| `bluesky_bot/chat_uploads/` | NEW DIR | Staging directory for uploaded multimodal files |
| `bluesky_bot/research_probe.py` | NEW | Wikipedia + DuckDuckGo historical/topic harvester |
| `bluesky_bot/policy_extract.py` | NEW | Deterministic regex policy domain extractor and ledger manager |
| `bluesky_bot/policy_ledger.json` | NEW | Persistent JSON ledger tracking policy coordinate averages |
| `bluesky_bot/aletheia_mcp_server.py` | NEW | Stdio FastMCP server exposing Aletheia tools and resources |
| `bluesky_bot/rebuild_registries.py` | MODIFIED | Auto-extracts policies and updates ledger on registry build |
| `bluesky_bot/rebuild_registries_son.py` | MODIFIED | Auto-extracts policies and updates ledger on SON registry build |
| `bluesky_bot/google_ai_studio_one_shot.py` | MODIFIED | Added `--probe`, `--probe-year`, and `--policy-report` CLI flags |
| `AletheiaLauncher.pyw` | MODIFIED | Added Research Probe card and Chat/Policy launcher buttons |
| `bluesky_bot/running_dialogue.md` | MODIFIED | Documented Intent 77 with (υ=+1.8, ψ=+1.9) audit |
