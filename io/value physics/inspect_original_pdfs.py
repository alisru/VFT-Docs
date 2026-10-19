import sys
import fitz

targets = [
    ("01_Empirical_Pricing_Audit_VPE55/Empirical_Case_Study_Real_World_Pricing_RRPD_Fairness_Audit_v1_archive.pdf", [2, 11]),
    ("02_Physics_of_Economic_Value_VPE21/The_Physics_of_Economic_Value_v1_preaudit.pdf", [2]),
    ("03_Thermodynamic_State_Space_VPE49/Thermodynamic_Work_Antiwork_State_Space_Dynamics_v1_preaudit.pdf", [2, 26])
]

for p, pages in targets:
    doc = fitz.open(p)
    print("=" * 50)
    print(f"File: {p}")
    for page_num in pages:
        page = doc[page_num - 1]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    line_text = "".join(s["text"] for s in l["spans"])
                    if "Coonabarabran" in line_text or "2357" in line_text:
                        print(f"  Page {page_num}: '{line_text}'")
                        print(f"    Line bbox: {l['bbox']}")
                        for s in l["spans"]:
                            print(f"      Span: '{s['text']}' | Font: {s['font']} | Size: {s['size']:.2f} | Bbox: {s['bbox']}")
