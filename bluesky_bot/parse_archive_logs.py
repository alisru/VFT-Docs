import os
import glob
import re
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(script_dir)
ai_logs_dir = os.path.join(workspace_dir, "_AI files and chat logs")
output_json_dir = os.path.join(script_dir, "archive_sessions_json")
os.makedirs(output_json_dir, exist_ok=True)

def classify_archive_file(filename, content_sample=""):
    fn = filename.lower()
    sample = content_sample.lower()
    if any(k in fn for k in ["math", "infinity", "tensor", "physics", "quantum", "cosmology", "dimension", "geometry", "duality of time", "6d memory"]):
        return "🌌 Physics & Cosmology"
    if any(k in fn for k in ["hegemon", "trump", "russia", "china", "iran", "catholic", "balaam", "policy", "srl", "strategic", "trade"]):
        return "🏛️ Politics & Hegemony"
    if any(k in fn for k in ["mbti", "epistemic", "faith", "belief", "greek", "deleuze", "perception", "consciousness", "fear"]):
        return "🧠 Epistemology & Mind"
    if any(k in fn for k in ["tautonic", "axiom", "kanon", "objective truth", "framework"]):
        return "📜 Axioms & Tautonics"
    return "💬 Discussion Transcripts"

def parse_chat_log(content, filename):
    # Remove UI artifacts
    lines = content.splitlines()
    clean_lines = []
    for l in lines:
        stripped = l.strip()
        if stripped in ["Skip to content", "Chat history", "New chat"]:
            continue
        clean_lines.append(l)
    text = "\n".join(clean_lines).strip()

    messages = []
    
    # Pattern 1: ## Prompt: / ## Response: (Gemini Markdown)
    if "## Prompt:" in text or "## Response:" in text:
        chunks = re.split(r'(?m)^##\s+(?:Prompt|Response):?', text)
        is_user = text.startswith("## Prompt:") or ("## Prompt:" in text[:200])
        for c in chunks:
            c = c.strip()
            if not c:
                continue
            c = re.sub(r'^######\s+Gemini\s+said\s*', '', c).strip()
            # Clean up title headers if present in first chunk
            if is_user and c.startswith("# "):
                c_lines = c.splitlines()
                c = "\n".join([l for l in c_lines if not l.startswith("#") and not l.startswith("**Exported:**") and not l.startswith("**Link:**")]).strip()
            if not c:
                continue
            role = "user" if is_user else "model"
            messages.append({"role": role, "content": c})
            is_user = not is_user

    # Pattern 2: You said: / ChatGPT said: / Gemini said: / Claude said:
    elif re.search(r'(?m)^(?:You|User|Human)\s+said:\s*$', text) or re.search(r'(?m)^(?:ChatGPT|Gemini|Claude|Assistant)\s+said:\s*$', text):
        pattern = r'(?m)^(You|User|Human|ChatGPT|Gemini|Claude|Assistant)\s+said:\s*$'
        parts = re.split(pattern, text)
        if len(parts) > 1:
            i = 1
            while i < len(parts):
                speaker = parts[i].strip().lower()
                body = parts[i+1].strip() if i+1 < len(parts) else ""
                role = "user" if speaker in ["you", "user", "human"] else "model"
                if body:
                    messages.append({"role": role, "content": body})
                i += 2

    # Pattern 3: User: / Assistant: or Human: / Claude:
    elif re.search(r'(?m)^(?:User|Human|Operator):\s*', text) and re.search(r'(?m)^(?:Assistant|Model|Claude|Gemini|ChatGPT):\s*', text):
        pattern = r'(?m)^(User|Human|Operator|Assistant|Model|Claude|Gemini|ChatGPT):\s*'
        parts = re.split(pattern, text)
        if len(parts) > 1:
            i = 1
            while i < len(parts):
                speaker = parts[i].strip().lower()
                body = parts[i+1].strip() if i+1 < len(parts) else ""
                role = "user" if speaker in ["user", "human", "operator"] else "model"
                if body:
                    messages.append({"role": role, "content": body})
                i += 2

    # Pattern 4: Claude conversation style (alternating turns)
    else:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if len(paragraphs) == 1:
            messages.append({"role": "user", "content": f"Review archive document: {filename}"})
            messages.append({"role": "model", "content": paragraphs[0]})
        elif len(paragraphs) > 1:
            # Check if there are short back-and-forth paragraphs
            is_dialogue = False
            first_short = len(paragraphs[0].split()) < 80
            if first_short and ("?" in paragraphs[0] or paragraphs[0].lower().startswith(("what", "how", "why", "can", "explain", "search", "conduct", "maybe", "i think", "i feel", "is it"))):
                is_dialogue = True

            if is_dialogue:
                # Group alternating user question vs long response
                curr_role = "user"
                curr_body = []
                for p in paragraphs:
                    is_q = len(p.split()) < 70 and ("?" in p or p.lower().startswith(("what", "how", "why", "can", "is", "so", "but", "i mean", "right")))
                    if is_q and curr_role == "model" and curr_body:
                        messages.append({"role": "model", "content": "\n\n".join(curr_body)})
                        curr_role = "user"
                        curr_body = [p]
                    elif not is_q and curr_role == "user" and curr_body:
                        messages.append({"role": "user", "content": "\n\n".join(curr_body)})
                        curr_role = "model"
                        curr_body = [p]
                    else:
                        curr_body.append(p)
                if curr_body:
                    messages.append({"role": curr_role, "content": "\n\n".join(curr_body)})
            else:
                messages.append({"role": "user", "content": f"Loaded archive discussion transcript: {filename}"})
                messages.append({"role": "model", "content": text})

    return messages

def process_all():
    files = glob.glob(os.path.join(ai_logs_dir, "*.txt")) + glob.glob(os.path.join(ai_logs_dir, "*.md"))
    converted_count = 0
    total_turns = 0

    for fpath in files:
        fname = os.path.basename(fpath)
        try:
            mtime = os.path.getmtime(fpath)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()

            cat = classify_archive_file(fname, content[:1000])
            clean_title = fname.replace(".txt", "").replace(".md", "").replace("_", " ").replace("-", " ")
            slug = re.sub(r'[^a-zA-Z0-9_-]', '_', fname.replace('.txt', '').replace('.md', ''))[:48]
            session_id = f"archive_{slug}"

            msgs = parse_chat_log(content, fname)
            total_turns += len(msgs)

            session_json = {
                "id": session_id,
                "title": f"📑 {clean_title}",
                "is_archive": True,
                "source_file": fname,
                "category": cat,
                "created_at": "2026-08-16T00:00:00",
                "updated_at": "2026-08-16T00:00:00",
                "active_thread_id": "main",
                "narrative_spine": [clean_title],
                "threads": {
                    "main": {
                        "id": "main",
                        "name": clean_title[:32],
                        "parent_thread_id": None,
                        "fork_message_index": 0,
                        "created_at": "2026-08-16T00:00:00",
                        "messages": msgs
                    }
                }
            }

            out_path = os.path.join(output_json_dir, f"session_{session_id}.json")
            with open(out_path, "w", encoding="utf-8") as out_fp:
                json.dump(session_json, out_fp, indent=2)

            converted_count += 1
        except Exception as e:
            print(f"Error converting {fname}: {e}")

    print(f"Successfully processed and converted {converted_count} archive logs into structured JSON sessions in '{output_json_dir}' (Total turns: {total_turns}).")

if __name__ == "__main__":
    process_all()
