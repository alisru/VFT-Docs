import os
import sys
import re
import csv
from pathlib import Path

workspace_root = Path(r"e:\Vector Field Theory\VFT Docs")
audit_dir = workspace_root / "io" / "_drive_audit"

ignore_dirs = {".venv", ".agent", ".agents", ".vscode", ".git", "node_modules", "__pycache__", "_drive_audit"}

def clean_key(s):
    # Strip extensions
    s = Path(s).name
    s = re.sub(r"\.(md|docx|pdf|html|xlsx|pptx|py|txt|zip|tex|bib|csv)$", "", s, flags=re.I)
    s = re.sub(r"\.(md|docx|pdf|html|xlsx|pptx|py|txt|zip|tex|bib|csv)$", "", s, flags=re.I)
    # Strip common prefixes like "Canvases/", numbers, "Formal Paper N:"
    s = re.sub(r"^Formal Paper \d+:\s*", "", s, flags=re.I)
    s = re.sub(r"^Unit \d+\s*-\s*", "", s, flags=re.I)
    # Strip non-alphanumeric
    s = re.sub(r"[^a-zA-Z0-9]", "", s).lower()
    return s

# 1. Catalog ALL workspace .md files
ws_md = {}
for p in workspace_root.rglob("*.md"):
    if any(ig in p.parts for ig in ignore_dirs):
        continue
    k = clean_key(p.name)
    if k not in ws_md:
        ws_md[k] = []
    ws_md[k].append(str(p.relative_to(workspace_root)))

# Catalog ALL workspace .docx files
ws_docx = {}
for p in workspace_root.rglob("*.docx"):
    if any(ig in p.parts for ig in ignore_dirs):
        continue
    k = clean_key(p.name)
    if k not in ws_docx:
        ws_docx[k] = []
    ws_docx[k].append(str(p.relative_to(workspace_root)))

print(f"Total workspace MD distinct keys: {len(ws_md)}")
print(f"Total workspace DOCX distinct keys: {len(ws_docx)}")

# 2. Check Drive Value Physics files against workspace MD & DOCX
vp_lines = open(audit_dir / "gdrive_value_physics_raw.txt", "r", encoding="utf-8", errors="ignore").readlines()
vp_matches = []
vp_unmatched = []
seen_vp = set()

for line in vp_lines:
    m = re.match(r"^\s*(-?\d+)\s+(.*)$", line.strip())
    if not m: continue
    path = m.group(2).strip()
    if path in seen_vp: continue
    seen_vp.add(path)
    k = clean_key(path)
    has_md = ws_md.get(k)
    has_docx = ws_docx.get(k)
    if has_md or has_docx:
        vp_matches.append((path, has_md, has_docx))
    else:
        vp_unmatched.append(path)

print(f"Drive VP files matched in workspace: {len(vp_matches)} / {len(seen_vp)}")
print(f"Drive VP files completely missing: {len(vp_unmatched)}")

# 3. Check Drive IO files against workspace MD & DOCX
io_lines = open(audit_dir / "gdrive_io_raw.txt", "r", encoding="utf-8", errors="ignore").readlines()
io_matches = []
io_unmatched = []
seen_io = set()

for line in io_lines:
    m = re.match(r"^\s*(-?\d+)\s+(.*)$", line.strip())
    if not m: continue
    path = m.group(2).strip()
    if path in seen_io: continue
    seen_io.add(path)
    k = clean_key(path)
    has_md = ws_md.get(k)
    has_docx = ws_docx.get(k)
    if has_md or has_docx:
        io_matches.append((path, has_md, has_docx))
    else:
        io_unmatched.append(path)

print(f"Drive IO files matched in workspace: {len(io_matches)} / {len(seen_io)}")
print(f"Drive IO files completely missing: {len(io_unmatched)}")

# Save to CSV
with open(audit_dir / "drive_vp_workspace_matches.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Drive Path", "Has Workspace MD Copy?", "Workspace MD Location", "Has Workspace DOCX Copy?", "Workspace DOCX Location"])
    for path, has_md, has_docx in vp_matches:
        w.writerow([
            path,
            "YES" if has_md else "NO",
            "; ".join(has_md) if has_md else "",
            "YES" if has_docx else "NO",
            "; ".join(has_docx) if has_docx else ""
        ])

with open(audit_dir / "drive_io_workspace_matches.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Drive Path", "Has Workspace MD Copy?", "Workspace MD Location", "Has Workspace DOCX Copy?", "Workspace DOCX Location"])
    for path, has_md, has_docx in io_matches:
        w.writerow([
            path,
            "YES" if has_md else "NO",
            "; ".join(has_md) if has_md else "",
            "YES" if has_docx else "NO",
            "; ".join(has_docx) if has_docx else ""
        ])

print("Saved cross-workspace match CSVs.")
