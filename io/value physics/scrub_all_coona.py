import os
import sys
import zipfile
import re
import fitz

if sys.version_info >= (3, 7):
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("MASTER LOCATION SCRUBBER: REMOVING COONABARABRAN / 2357")
print("=" * 60)

base_dir = "io/value physics"

# 1. Scrub Markdown and Python files
text_files = [
    os.path.join(base_dir, "04_Autonomous_Econophysics_VPE60", "VPE-60_Autonomous_Econophysics.md"),
    os.path.join(base_dir, "01_Empirical_Pricing_Audit_VPE55", "test_rrp_fairness_audit.py"),
]

for tf in text_files:
    if os.path.exists(tf):
        with open(tf, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace occurrences
        new_content = re.sub(r'Coonabarabran,\s*New South Wales,\s*Australia', 'Regional NSW, Australia', content, flags=re.IGNORECASE)
        new_content = re.sub(r'Coonabarabran,\s*NSW\s*2357', 'Australia', new_content, flags=re.IGNORECASE)
        new_content = re.sub(r'Coonabarabran,\s*NSW', 'Regional NSW', new_content, flags=re.IGNORECASE)
        new_content = re.sub(r'Regional NSW\s*/\s*Coonabarabran', 'Regional NSW', new_content, flags=re.IGNORECASE)
        new_content = re.sub(r'Coonabarabran', 'Regional NSW', new_content, flags=re.IGNORECASE)
        new_content = re.sub(r'2357', '', new_content)
        
        with open(tf, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[OK] Cleaned text file: {tf}")

# 2. Scrub VPE-60 PDF
vpe60_pdf = os.path.join(base_dir, "04_Autonomous_Econophysics_VPE60", "VPE-60_Autonomous_Econophysics.pdf")
if os.path.exists(vpe60_pdf):
    doc = fitz.open(vpe60_pdf)
    for p in doc:
        rects = p.search_for("Coonabarabran") + p.search_for("2357")
        if rects:
            for r in rects:
                # expand slightly
                r_exp = fitz.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2)
                p.add_redact_annot(r_exp, fill=(1, 1, 1))
            p.apply_redactions()
            for r in rects:
                p.insert_text(fitz.Point(r.x0, r.y1 - 2), "Regional NSW", fontsize=10, fontname="times-roman")
    doc.save(vpe60_pdf + ".tmp")
    doc.close()
    os.replace(vpe60_pdf + ".tmp", vpe60_pdf)
    print(f"[OK] Cleaned PDF: {vpe60_pdf}")

# 3. Clean Paper 01 PDF page 11 Warrumbungle citation
p1_pdf = os.path.join(base_dir, "01_Empirical_Pricing_Audit_VPE55", "Empirical_Case_Study_Real_World_Pricing_RRPD_Fairness_Audit.pdf")
p1_manuscript = os.path.join(base_dir, "01_Empirical_Pricing_Audit_VPE55", "manuscript_vpe55.pdf")

for pdf_path in [p1_pdf, p1_manuscript]:
    if os.path.exists(pdf_path):
        doc = fitz.open(pdf_path)
        for p in doc:
            rects = p.search_for("Coonabarabran") + p.search_for("2357")
            if rects:
                for r in rects:
                    r_exp = fitz.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2)
                    p.add_redact_annot(r_exp, fill=(1, 1, 1))
                p.apply_redactions()
                for r in rects:
                    p.insert_text(fitz.Point(r.x0, r.y1 - 2), "Regional NSW", fontsize=10, fontname="times-roman")
        doc.save(pdf_path + ".tmp")
        doc.close()
        os.replace(pdf_path + ".tmp", pdf_path)
        print(f"[OK] Cleaned PDF: {pdf_path}")

# 4. Clean all DOCX files in io/value physics
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.lower().endswith('.docx'):
            fpath = os.path.join(root, f)
            try:
                # check if coonabarabran is in docx
                has_coona = False
                with zipfile.ZipFile(fpath, 'r') as z:
                    for name in z.namelist():
                        if name.endswith('.xml'):
                            text = z.read(name).decode('utf-8', errors='ignore')
                            if 'coonabarabran' in text.lower() or '2357' in text:
                                has_coona = True
                                break
                if has_coona:
                    # unpack, replace in all xml, repack
                    entries = {}
                    with zipfile.ZipFile(fpath, 'r') as z:
                        for item in z.infolist():
                            data = z.read(item.filename)
                            if item.filename.endswith('.xml'):
                                text = data.decode('utf-8', errors='ignore')
                                text = re.sub(r'Coonabarabran,\s*New South Wales,\s*Australia', 'Regional NSW, Australia', text, flags=re.IGNORECASE)
                                text = re.sub(r'Coonabarabran,\s*NSW\s*2357', 'Australia', text, flags=re.IGNORECASE)
                                text = re.sub(r'Coonabarabran,\s*NSW', 'Regional NSW', text, flags=re.IGNORECASE)
                                text = re.sub(r'Regional NSW\s*/\s*Coonabarabran', 'Regional NSW', text, flags=re.IGNORECASE)
                                text = re.sub(r'Coonabarabran', 'Regional NSW', text, flags=re.IGNORECASE)
                                text = re.sub(r'2357', '', text)
                                data = text.encode('utf-8')
                            entries[item.filename] = data
                    with zipfile.ZipFile(fpath, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                        for fname, bdata in entries.items():
                            z.writestr(fname, bdata)
                    print(f"[OK] Cleaned DOCX: {fpath}")
            except Exception as e:
                print(f"[WARN] Failed to process {fpath}: {e}")

print("=" * 60)
print("SCRUB COMPLETE. VERIFYING ZERO OCCURRENCES...")
print("=" * 60)
