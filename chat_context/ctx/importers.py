"""
Multi-source Chat Importers:
Parses Gemini web exports, ChatGPT copy-pastes, Claude transcripts, JSON exports, and folder files.
"""
import json
import re
import urllib.parse
from pathlib import Path


MONTHS = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}(?:,\s*\d{4})?"


def parse_gemini_markdown(text: str, filename: str):
    """
    Parses Gemini web markdown export:
    # Title
    **Exported:** ...
    **Link:** [url](url)
    ## Prompt: ...
    ## Response: ...
    """
    lines = text.splitlines()
    title = filename.replace(".md", "").replace("Gemini-", "").strip()
    url = ""
    for l in lines[:15]:
        if l.startswith("# "):
            title = l[2:].strip()
        m = re.search(r"\*\*Link:\*\*\s*\[.*?\]\((https?://[^\)]+)\)", l)
        if m:
            url = m.group(1)

    sections = re.split(r"(?m)^##\s+(Prompt|Response):\s*", text)
    msgs = []
    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            role_type = sections[i].lower()
            content = sections[i + 1].strip()
            role = "user" if role_type == "prompt" else "assistant"
            # Strip thought/thinking headers
            content = re.sub(r"^>\s*Thinking:.*?\n\n", "", content, flags=re.S)
            msgs.append((role, None, content))
    return title, url, msgs


def parse_chatgpt_text(text: str, filename: str):
    """
    Parses standard ChatGPT copy-pastes:
    You said: ...
    ChatGPT said: ...
    """
    title = filename.replace(".txt", "").replace("chatgpt", "ChatGPT").strip()
    sections = re.split(r"(?m)^(You|ChatGPT) said:\s*", text)
    msgs = []
    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            speaker = sections[i]
            content = sections[i + 1].strip()
            role = "user" if speaker == "You" else "assistant"
            msgs.append((role, None, content))
    return title, "", msgs


def parse_claude_text(text: str, filename: str):
    """
    Parses Claude web copy-pastes where assistant turns are preceded by date stamps.
    """
    title = filename.replace(".txt", "").replace("claude", "Claude").strip()
    # Find positions of date headers
    pattern = rf"(?m)^({MONTHS})\s*$"
    splits = re.split(pattern, text)
    if len(splits) < 3:
        return title, "", []

    msgs = []
    # Preamble before first date is the first user prompt
    preamble = splits[0].strip()
    # Strip leading menu items
    clean_pre = re.sub(r"^(?:menu-icon|Improve Prompt[^\n]*\n|New chat\n)+", "", preamble).strip()
    if clean_pre:
        msgs.append(("user", None, clean_pre))

    for i in range(1, len(splits), 2):
        ts = splits[i].strip()
        body = splits[i + 1].strip()
        # In Claude exports, the body is the assistant response, followed possibly by the next user message
        # Often user messages are at the very end of the body separated by blank lines before next date
        # For simplicity, treat the block as assistant
        msgs.append(("assistant", ts, body))

    return title, "", msgs


def parse_gemini_copypaste(text: str, filename: str):
    """
    Parses Gemini raw copy-pastes (with 'Conversation with Gemini' and 'Custom Gem' / 'Alethekanon')
    """
    title = filename.replace(".txt", "").strip()
    if "Conversation with Gemini" not in text:
        return title, "", []

    parts = text.split("Conversation with Gemini", 1)
    preamble = [l.strip() for l in parts[0].splitlines() if l.strip()]
    if len(preamble) >= 2 and preamble[0].lower() == "gemini":
        title = preamble[1]

    body = parts[1].strip()
    # Split by assistant markers
    marker = r"(?m)^(?:Alethekanon|Custom Gem|Gemini)\s*$"
    blocks = re.split(marker, body)
    msgs = []
    role = "user"
    for b in blocks:
        b = b.strip()
        if not b or b == "Custom Gem":
            continue
        msgs.append((role, None, b))
        role = "assistant" if role == "user" else "user"

    return title, "", msgs


def parse_json_chat(text: str, filename: str):
    """
    Parses standard JSON chat export:
    [{"role": "user"|"assistant", "text"|"content": "..."}]
    or {"title": "...", "messages": [...]}
    or Takeout format
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None, "", []

    title = filename.replace(".json", "")
    url = ""
    msgs = []

    if isinstance(data, dict):
        title = data.get("title") or title
        url = data.get("url") or ""
        raw_msgs = data.get("messages") or data.get("conversation") or []
    elif isinstance(data, list):
        raw_msgs = data
    else:
        raw_msgs = []

    for m in raw_msgs:
        if not isinstance(m, dict):
            continue
        role = m.get("role") or ("user" if m.get("author") == "user" else "assistant")
        txt = m.get("text") or m.get("content") or ""
        ts = m.get("created_at") or m.get("timestamp") or None
        if txt and str(txt).strip():
            msgs.append((role, ts, str(txt).strip()))

    return title, url, msgs


def parse_chat_file(path: Path):
    """Auto-detect format and parse a file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    name = path.name

    if name.endswith(".json"):
        t, u, m = parse_json_chat(text, name)
        if m:
            return {"source": "json", "title": t, "url": u, "messages": m}

    if name.startswith("Gemini-") and name.endswith(".md"):
        t, u, m = parse_gemini_markdown(text, name)
        if m:
            return {"source": "gemini", "title": t, "url": u, "messages": m}

    if "You said:" in text and "ChatGPT said:" in text:
        t, u, m = parse_chatgpt_text(text, name)
        if m:
            return {"source": "chatgpt", "title": t, "url": u, "messages": m}

    if "Conversation with Gemini" in text:
        t, u, m = parse_gemini_copypaste(text, name)
        if m:
            return {"source": "gemini", "title": t, "url": u, "messages": m}

    if re.search(rf"(?m)^{MONTHS}\s*$", text) and ("claude" in name.lower() or "menu-icon" in text):
        t, u, m = parse_claude_text(text, name)
        if m:
            return {"source": "claude", "title": t, "url": u, "messages": m}

    return None
