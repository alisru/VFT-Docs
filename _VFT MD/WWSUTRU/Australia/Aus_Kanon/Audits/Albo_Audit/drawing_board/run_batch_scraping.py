import json
import os
import subprocess

CHECKLIST_PATH = "e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit/unscraped_checklist.json"
TSV_PATH = "e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit/drawing_board/temp_sources.tsv"

# Load the checklist
with open(CHECKLIST_PATH, "r", encoding="utf-8") as f:
    checklist = json.load(f)

unscraped = checklist.get("unscraped", {})

# Generate the TSV file for fetch_archive.py
with open(TSV_PATH, "w", encoding="utf-8") as f:
    for tag, info in sorted(unscraped.items()):
        url = info.get("url", "")
        citation = info.get("citation", "").replace("\t", " ").replace("\n", " ")
        if url:
            f.write(f"{tag}\t{url}\t{citation}\n")

print(f"Generated TSV at {TSV_PATH} with {len(unscraped)} entries.")
print("To run the scrape, execute:")
print("python fetch\\fetch_archive.py drawing_board\\temp_sources.tsv")
