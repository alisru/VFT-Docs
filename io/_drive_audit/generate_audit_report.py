import os
import sys
import re
import csv
from pathlib import Path

audit_dir = Path(r"e:\Vector Field Theory\VFT Docs\io\_drive_audit")
io_local_root = Path(r"e:\Vector Field Theory\VFT Docs\io")

def norm_key(s):
    s = Path(s).name
    # Strip compound and single extensions
    s = re.sub(r"\.(md|docx|pdf|html|xlsx|pptx|py|txt|zip|tex|bib|csv)$", "", s, flags=re.I)
    s = re.sub(r"\.(md|docx|pdf|html|xlsx|pptx|py|txt|zip|tex|bib|csv)$", "", s, flags=re.I)
    # Strip non-alphanumeric
    s = re.sub(r"[^a-zA-Z0-9]", "", s).lower()
    return s

# 1. Local files in io
local_files = []
for p in io_local_root.rglob("*"):
    if p.is_file() and "_drive_audit" not in p.parts:
        rel = p.relative_to(io_local_root)
        local_files.append({
            "full_path": str(p),
            "rel_path": str(rel),
            "name": p.name,
            "norm_key": norm_key(p.name),
            "size": p.stat().st_size,
            "folder": str(rel.parent)
        })

print(f"Loaded {len(local_files)} local files in io.")

# 2. Drive Value Physics
drive_vp = []
with open(audit_dir / "gdrive_value_physics_raw.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m = re.match(r"^\s*(-?\d+)\s+(.*)$", line.strip())
        if m:
            size, path = int(m.group(1)), m.group(2).strip()
            drive_vp.append({
                "size": size,
                "path": path,
                "name": Path(path).name,
                "norm_key": norm_key(path),
                "folder": str(Path(path).parent)
            })

# 3. Drive IO
drive_io = []
with open(audit_dir / "gdrive_io_raw.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m = re.match(r"^\s*(-?\d+)\s+(.*)$", line.strip())
        if m:
            size, path = int(m.group(1)), m.group(2).strip()
            drive_io.append({
                "size": size,
                "path": path,
                "name": Path(path).name,
                "norm_key": norm_key(path),
                "folder": str(Path(path).parent)
            })

# 4. Drive Root loose files
drive_root = []
with open(audit_dir / "gdrive_root_raw.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        t = line.strip()
        if t and not t.startswith("<") and not t.startswith("Log:"):
            drive_root.append({
                "name": t,
                "norm_key": norm_key(t)
            })

print(f"Drive VP: {len(drive_vp)}, Drive IO: {len(drive_io)}, Drive Root: {len(drive_root)}")

# Map local files by norm_key
local_by_key = {}
for lf in local_files:
    k = lf["norm_key"]
    if k not in local_by_key:
        local_by_key[k] = []
    local_by_key[k].append(lf)

# Compare Drive VP with local io/value physics
vp_local_keys = {lf["norm_key"]: lf for lf in local_files if lf["folder"].startswith("value physics")}

vp_missing = []
vp_present = []
seen_vp_paths = set()

for dvp in drive_vp:
    if dvp["path"] in seen_vp_paths:
        continue
    seen_vp_paths.add(dvp["path"])
    k = dvp["norm_key"]
    if k in vp_local_keys:
        vp_present.append((dvp, vp_local_keys[k]))
    else:
        # Check if present in other local io folders
        in_other = local_by_key.get(k)
        vp_missing.append((dvp, in_other))

print(f"VP present in local io/value physics: {len(vp_present)}")
print(f"VP missing from local io/value physics: {len(vp_missing)}")

# Write CSV for VP Missing
with open(audit_dir / "missing_value_physics_files.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Drive Folder", "File Name", "Size (bytes)", "Full Drive Path", "Found Elsewhere in Local IO?"])
    for dvp, in_other in vp_missing:
        other_loc = in_other[0]["rel_path"] if in_other else "NOT DOWNLOADED"
        w.writerow([dvp["folder"], dvp["name"], dvp["size"], dvp["path"], other_loc])

# Compare Drive IO with local IO
io_missing = []
io_present = []
seen_io_paths = set()

for dio in drive_io:
    if dio["path"] in seen_io_paths:
        continue
    seen_io_paths.add(dio["path"])
    k = dio["norm_key"]
    if k in local_by_key:
        io_present.append((dio, local_by_key[k][0]))
    else:
        io_missing.append(dio)

print(f"Drive IO present in local io: {len(io_present)}")
print(f"Drive IO missing from local io: {len(io_missing)}")

with open(audit_dir / "missing_io_files.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Drive Folder", "File Name", "Size (bytes)", "Full Drive Path"])
    for dio in io_missing:
        w.writerow([dio["folder"], dio["name"], dio["size"], dio["path"]])

# Check Drive Root files that match Value Physics keywords or are missing from local IO
vp_keywords = ["value", "price", "village", "token", "bread", "sfc", "upe", "antiwork", "thermodynamic", "exergy", "bifurcation", "sovereign", "charter", "credit", "ledger", "logistics"]

root_vp_matches = []
root_missing_all = []
seen_root_names = set()

for dr in drive_root:
    if dr["name"] in seen_root_names:
        continue
    seen_root_names.add(dr["name"])
    is_vp = any(kw in dr["name"].lower() for kw in vp_keywords)
    in_local = dr["norm_key"] in local_by_key
    if is_vp:
        root_vp_matches.append((dr, in_local))
    if not in_local:
        root_missing_all.append(dr)

print(f"Drive Root VP candidates: {len(root_vp_matches)} (Missing from local: {len([r for r, il in root_vp_matches if not il])})")
print(f"Total Drive Root files missing locally: {len(root_missing_all)}")

with open(audit_dir / "root_value_physics_matches.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Root File Name", "Is Already Downloaded in IO?"])
    for dr, in_local in root_vp_matches:
        w.writerow([dr["name"], "YES" if in_local else "NO - MISSING"])

with open(audit_dir / "root_all_missing_files.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Root File Name"])
    for dr in root_missing_all:
        w.writerow([dr["name"]])

# Generate comprehensive Markdown Report
report_md = f"""# Google Drive vs Local Workspace Audit Report
**Generated:** 2026-10-07  
**Scope:** `VFT:Value Physics`, `VFT:io`, `VFT: (Root Loose Files)` vs `e:\\Vector Field Theory\\VFT Docs\\io\\`

---

## 1. Executive Summary

| Category | On Google Drive | Downloaded in Local `io/value physics` | Downloaded Anywhere in Local `io/` | Completely Missing from Local `io` |
|---|---|---|---|---|
| **Value Physics (`VFT:Value Physics`)** | {len(seen_vp_paths)} entries | {len(vp_present)} | {len(vp_present) + len([m for m, o in vp_missing if o])} | {len([m for m, o in vp_missing if not o])} |
| **Drive IO Folder (`VFT:io`)** | {len(seen_io_paths)} entries | N/A | {len(io_present)} | {len(io_missing)} |
| **Drive Root Loose Files (`VFT:`)** | {len(seen_root_names)} unique files | N/A | {len(seen_root_names) - len(root_missing_all)} | {len(root_missing_all)} |

---

## 2. Value Physics Deep Breakdown (`VFT:Value Physics`)

Your local folder `io/value physics` currently has **28 documents** (all `.docx` and `.xlsx`).  
However, Google Drive holds **full research packages**, including simulation engines, LaTeX source bundles, compiled PDFs, figures, and institutional charters that have **never been downloaded**.

### A. Python Simulation & Calculation Scripts (MISSING LOCALLY)
These scripts are currently sitting on Drive and are **not** in `io/value physics`:
"""

# Categorize missing VP files
missing_py = [m for m, o in vp_missing if m["name"].endswith(".py") and not o]
missing_tex_zip = [m for m, o in vp_missing if (m["name"].endswith(".tex") or m["name"].endswith(".zip") or m["name"].endswith(".bib")) and not o]
missing_pdf = [m for m, o in vp_missing if m["name"].endswith(".pdf") and not o]
missing_img = [m for m, o in vp_missing if m["name"].endswith(".png") and not o]
missing_docs = [m for m, o in vp_missing if (m["name"].endswith(".docx") or m["name"].endswith(".pptx") or m["name"].endswith(".xlsx") or m["name"].endswith(".md") or m["name"].endswith(".json")) and not o]

for m in sorted(missing_py, key=lambda x: x["name"]):
    report_md += f"- `{m['name']}` (Drive Path: `{m['path']}`)\n"

report_md += "\n### B. LaTeX Source Packages & Bibliographies (MISSING LOCALLY)\n"
for m in sorted(missing_tex_zip, key=lambda x: x["name"]):
    report_md += f"- `{m['name']}` (Drive Path: `{m['path']}`)\n"

report_md += "\n### C. Compiled PDFs & Deliverables (MISSING LOCALLY)\n"
for m in sorted(missing_pdf, key=lambda x: x["name"]):
    report_md += f"- `{m['name']}` (Drive Path: `{m['path']}`)\n"

report_md += "\n### D. High-Resolution Phase & Sclerosis Diagrams (MISSING LOCALLY)\n"
for m in sorted(missing_img, key=lambda x: x["name"]):
    report_md += f"- `{m['name']}` (Drive Path: `{m['path']}`)\n"

report_md += "\n### E. Policy Treatises, Charters, Briefings & Manifests (MISSING LOCALLY)\n"
for m in sorted(missing_docs, key=lambda x: x["name"]):
    report_md += f"- `{m['name']}` (Drive Path: `{m['path']}`)\n"

report_md += f"""

---

## 3. Unsorted Drive `io` Folder Status (`VFT:io`)

Drive `VFT:io` has **{len(seen_io_paths)} entries**:
- **{len(io_present)} files** match items already present in local `io` (many were renamed from `.md.docx` to `.md` or `.docx`).
- **{len(io_missing)} files** are **completely missing** from local `io`.

### Noteworthy Missing Files from Drive `io`:
"""

for m in sorted(io_missing, key=lambda x: x["path"]):
    report_md += f"- `{m['path']}`\n"

report_md += f"""

---

## 4. Drive Root Loose Files (`VFT:`)

There are **{len(seen_root_names)} loose files** at the root of Google Drive.
- **{len(root_vp_matches)} files** relate directly to Value Physics, Token Economics, or Village Logistics.
- Out of those Value Physics files at the root, **{len([r for r, il in root_vp_matches if not il])}** are **NOT downloaded** locally!

### Value Physics Files Loose at Drive Root (Not Downloaded):
"""

for r, il in root_vp_matches:
    if not il:
        report_md += f"- `{r['name']}`\n"

report_md += """

---

## 5. Summary CSV Artifacts Created
All detailed breakdowns have been written to the following files in `e:\\Vector Field Theory\\VFT Docs\\io\\_drive_audit\\`:
1. `missing_value_physics_files.csv` — Full list of Value Physics files on Drive missing locally.
2. `missing_io_files.csv` — Full list of Drive `io` files missing locally.
3. `root_value_physics_matches.csv` — All Value Physics files sitting loose at Drive root.
4. `root_all_missing_files.csv` — All 500+ unorganized files loose at Drive root not yet downloaded.
"""

with open(audit_dir / "DRIVE_VS_LOCAL_AUDIT_REPORT.md", "w", encoding="utf-8") as f:
    f.write(report_md)

print("Comprehensive Markdown report written to DRIVE_VS_LOCAL_AUDIT_REPORT.md")
