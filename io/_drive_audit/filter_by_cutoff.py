import os
import sys
import re
import csv
from datetime import datetime
from pathlib import Path

workspace_root = Path(r"e:\Vector Field Theory\VFT Docs")
audit_dir = workspace_root / "io" / "_drive_audit"

ignore_dirs = {".venv", ".agent", ".agents", ".vscode", ".git", "node_modules", "__pycache__", "_drive_audit"}

def clean_key(s):
    s = Path(s).name
    s = re.sub(r"\.(md|docx|pdf|html|xlsx|pptx|py|txt|zip|tex|bib|csv)$", "", s, flags=re.I)
    s = re.sub(r"\.(md|docx|pdf|html|xlsx|pptx|py|txt|zip|tex|bib|csv)$", "", s, flags=re.I)
    s = re.sub(r"^Formal Paper \d+:\s*", "", s, flags=re.I)
    s = re.sub(r"^Unit \d+\s*-\s*", "", s, flags=re.I)
    s = re.sub(r"[^a-zA-Z0-9]", "", s).lower()
    return s

# 1. Catalog ALL workspace .md and .docx files
ws_md = {}
for p in workspace_root.rglob("*.md"):
    if any(ig in p.parts for ig in ignore_dirs):
        continue
    k = clean_key(p.name)
    if k not in ws_md:
        ws_md[k] = []
    ws_md[k].append(str(p.relative_to(workspace_root)))

ws_docx = {}
for p in workspace_root.rglob("*.docx"):
    if any(ig in p.parts for ig in ignore_dirs):
        continue
    k = clean_key(p.name)
    if k not in ws_docx:
        ws_docx[k] = []
    ws_docx[k].append(str(p.relative_to(workspace_root)))

# 2. Parse gdrive_root_dated.txt
cutoff_dt = datetime(2026, 1, 21, 0, 0, 0)

root_dated = []
with open(audit_dir / "gdrive_root_dated.txt", "r", encoding="utf-16", errors="ignore") as f:
    for line in f:
        line_str = line.strip()
        parts = line_str.split(None, 3)
        if len(parts) == 4 and re.match(r"^\d{4}-\d{2}-\d{2}$", parts[1]):
            size_str, dt_date, dt_time, name = parts[0], parts[1], parts[2], parts[3]
            dt_str = f"{dt_date} {dt_time}"
            dt_parsed = datetime.strptime(f"{dt_date} {dt_time[:8]}", "%Y-%m-%d %H:%M:%S")
            if dt_parsed >= cutoff_dt:
                root_dated.append({
                    "name": name,
                    "date": dt_str,
                    "dt": dt_parsed,
                    "size": int(size_str),
                    "norm_key": clean_key(name)
                })

print(f"Total post-Jan 21 root files: {len(root_dated)}")

# 3. Categorize research vs clutter/chat-prompts
chat_prompt_patterns = [
    r"^add in review format",
    r"^add some indirect reasoning",
    r"^add that to the doc",
    r"^add that whole reasoning",
    r"^also add a column",
    r"^can you check",
    r"^could you also",
    r"^give me that in canvas",
    r"^give me the phase reading",
    r"^how to export this chat",
    r"^include that in the document",
    r"^is there a way to change the model",
    r"^make that clarification",
    r"^now whats the ratio",
    r"^oh there\'s also the framing",
    r"^ok, add all these",
    r"^only in this section",
    r"^pls remove the unused",
    r"^pretty sure we lost",
    r"^probably a good time",
    r"^redo your entire research",
    r"^so i proved it on",
    r"^specifically due to the fact",
    r"^update the table",
    r"^welcome to the universe",
    r"^what is the mass of the",
    r"^where\'s the original lyrics",
    r"^yeah no you didn't",
    r"^Untitled document",
    r"^Untitled spreadsheet",
    r"^test\.",
    r"^test_doc",
    r"^\s*$"
]

def is_chat_prompt_or_temp(name):
    for pat in chat_prompt_patterns:
        if re.search(pat, name, re.IGNORECASE):
            return True
    return False

# 4. Check matches in workspace
post_jan21_downloaded_md = []
post_jan21_downloaded_docx = []
post_jan21_missing_research = []
post_jan21_missing_clutter = []

for item in root_dated:
    k = item["norm_key"]
    name = item["name"]
    in_md = ws_md.get(k)
    in_docx = ws_docx.get(k)
    
    if in_md:
        post_jan21_downloaded_md.append((item, in_md))
    elif in_docx:
        post_jan21_downloaded_docx.append((item, in_docx))
    else:
        if is_chat_prompt_or_temp(name):
            post_jan21_missing_clutter.append(item)
        else:
            post_jan21_missing_research.append(item)

print(f"Post-Jan 21 files already downloaded as MD: {len(post_jan21_downloaded_md)}")
print(f"Post-Jan 21 files already downloaded as DOCX: {len(post_jan21_downloaded_docx)}")
print(f"Post-Jan 21 genuine research files MISSING: {len(post_jan21_missing_research)}")
print(f"Post-Jan 21 chat prompt/temp files missing: {len(post_jan21_missing_clutter)}")

# Save CSVs
with open(audit_dir / "post_jan21_missing_research.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Date", "File Name", "Size (bytes)"])
    for item in sorted(post_jan21_missing_research, key=lambda x: x["dt"], reverse=True):
        w.writerow([item["date"], item["name"], item["size"]])

with open(audit_dir / "post_jan21_downloaded_as_md.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Drive File Name", "Local MD Path(s)"])
    for item, md_paths in sorted(post_jan21_downloaded_md, key=lambda x: x[0]["dt"], reverse=True):
        w.writerow([item["date"], item["name"], "; ".join(md_paths)])

# Generate summary markdown report
report_path = audit_dir / "POST_JAN21_FILTERED_AUDIT_REPORT.md"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("# Filtered Google Drive Audit (Jan 21, 2026 Onwards)\n")
    f.write("**Cutoff Anchor:** `mover` / `Vector Analysis: Political Distraction` (Jan 21, 2026)\n\n")
    f.write(f"- **Total files evaluated (>= Jan 21, 2026):** {len(root_dated)}\n")
    f.write(f"- **Files older than Jan 21, 2026 (Discounted):** 393 files\n")
    f.write(f"- **Already Downloaded & Converted to Markdown (.md):** {len(post_jan21_downloaded_md)}\n")
    f.write(f"- **Already Downloaded as Word Documents (.docx):** {len(post_jan21_downloaded_docx)}\n")
    f.write(f"- **Genuine Research Documents NOT Downloaded:** {len(post_jan21_missing_research)}\n")
    f.write(f"- **Temporary / Chat Prompt / Clutter files NOT Downloaded:** {len(post_jan21_missing_clutter)}\n\n")
    
    f.write("## 1. Genuine Research Documents Missing Locally (Post-Jan 21, 2026)\n\n")
    f.write("| Date | File Name |\n|---|---|\n")
    for item in sorted(post_jan21_missing_research, key=lambda x: x["dt"], reverse=True):
        f.write(f"| {item['date'][:10]} | `{item['name']}` |\n")
        
    f.write("\n## 2. Temporary / Prompt Snippets Discountable (Post-Jan 21, 2026)\n\n")
    for item in sorted(post_jan21_missing_clutter, key=lambda x: x["dt"], reverse=True):
        f.write(f"- `{item['name']}` ({item['date'][:10]})\n")

print(f"Report written to {report_path}")
