import sys
import shutil
import zipfile
import fitz

def sanitize_paper_01():
    print("--- Sanitizing Paper 01 ---")
    src = "01_Empirical_Pricing_Audit_VPE55/Empirical_Case_Study_Real_World_Pricing_RRPD_Fairness_Audit_v1_archive.pdf"
    doc = fitz.open(src)
    
    # Page 2: affiliation line 2
    p2 = doc[1]
    # Line 2 bbox was (206.65, 307.65, 388.66, 318.57)
    p2.add_redact_annot(fitz.Rect(180, 305, 410, 321), fill=(1, 1, 1))
    p2.apply_redactions()
    l2_text = "Australia"
    w2 = fitz.get_text_length(l2_text, fontname="times-roman", fontsize=10.91)
    p2.insert_text(fitz.Point((p2.rect.width - w2) / 2, 316.18), l2_text, fontname="times-roman", fontsize=10.91, color=(0, 0, 0))
    
    # Page 11: bibliography Warrumbungle Shire Council
    p11 = doc[10]
    # Line bbox: (83.71, 312.22, 477.53, 324.18) 'Technical report, Warrumbungle Shire Council, Coonabarabran, NSW, 2025.'
    p11.add_redact_annot(fitz.Rect(80, 310, 485, 326), fill=(1, 1, 1))
    p11.apply_redactions()
    ref_text = "Technical report, Warrumbungle Shire Council, Regional NSW, 2025."
    p11.insert_text(fitz.Point(83.71, 322.2), ref_text, fontname="times-roman", fontsize=11.96, color=(0, 0, 0))
    
    out_pdf1 = "01_Empirical_Pricing_Audit_VPE55/Empirical_Case_Study_Real_World_Pricing_RRPD_Fairness_Audit.pdf"
    out_pdf2 = "01_Empirical_Pricing_Audit_VPE55/manuscript_vpe55.pdf"
    doc.save(out_pdf1)
    doc.close()
    shutil.copyfile(out_pdf1, out_pdf2)
    print("Saved Paper 01 PDFs successfully")

def sanitize_paper_02():
    print("--- Sanitizing Paper 02 ---")
    src = "02_Physics_of_Economic_Value_VPE21/The_Physics_of_Economic_Value_v1_preaudit.pdf"
    doc = fitz.open(src)
    
    # Page 2: affiliation line
    p2 = doc[1]
    # Line bbox was (128.32, 281.16, 467.00, 292.07)
    p2.add_redact_annot(fitz.Rect(120, 275, 475, 295), fill=(1, 1, 1))
    p2.apply_redactions()
    new_text = "Alethekanon Research Institute, Australia"
    w = fitz.get_text_length(new_text, fontname="times-roman", fontsize=10.91)
    p2.insert_text(fitz.Point((p2.rect.width - w) / 2, 289.68), new_text, fontname="times-roman", fontsize=10.91, color=(0, 0, 0))
    
    out_pdf1 = "02_Physics_of_Economic_Value_VPE21/The_Physics_of_Economic_Value.pdf"
    out_pdf2 = "02_Physics_of_Economic_Value_VPE21/manuscript_vpe21.pdf"
    doc.save(out_pdf1)
    doc.close()
    shutil.copyfile(out_pdf1, out_pdf2)
    print("Saved Paper 02 PDFs successfully")

def sanitize_paper_03():
    print("--- Sanitizing Paper 03 ---")
    src = "03_Thermodynamic_State_Space_VPE49/Thermodynamic_Work_Antiwork_State_Space_Dynamics_v1_preaudit.pdf"
    doc = fitz.open(src)
    
    # Page 2: affiliation line 2
    p2 = doc[1]
    # Line bbox: (206.65, 319.61, 388.66, 330.52)
    p2.add_redact_annot(fitz.Rect(180, 317, 410, 333), fill=(1, 1, 1))
    p2.apply_redactions()
    l2_text = "Australia"
    w2 = fitz.get_text_length(l2_text, fontname="times-roman", fontsize=10.91)
    p2.insert_text(fitz.Point((p2.rect.width - w2) / 2, 328.14), l2_text, fontname="times-roman", fontsize=10.91, color=(0, 0, 0))
    
    # Page 26: Heavy Vehicle National Law line
    p26 = doc[25]
    p26.add_redact_annot(fitz.Rect(70, 145, 550, 160), fill=(1, 1, 1))
    p26.apply_redactions()
    new_p26_line = "Australian Heavy Vehicle National Law, triggering staging swaps at regional NSW crossroads."
    p26.insert_text(fitz.Point(72.0, 156.185), new_p26_line, fontname="times-roman", fontsize=11.96, color=(0, 0, 0))
    
    out_pdf1 = "03_Thermodynamic_State_Space_VPE49/Thermodynamic_Work_Antiwork_State_Space_Dynamics.pdf"
    out_pdf2 = "03_Thermodynamic_State_Space_VPE49/manuscript_vpe49.pdf"
    doc.save(out_pdf1)
    doc.close()
    shutil.copyfile(out_pdf1, out_pdf2)
    print("Saved Paper 03 PDFs successfully")

def update_zip_archives():
    print("--- Updating Zip Packages ---")
    zip_path = "01_Empirical_Pricing_Audit_VPE55/vpe55_latex_package.zip"
    pdf_to_add = "01_Empirical_Pricing_Audit_VPE55/manuscript_vpe55.pdf"
    
    # Read existing entries except manuscript_vpe55.pdf
    entries = {}
    with zipfile.ZipFile(zip_path, 'r') as z:
        for item in z.infolist():
            if item.filename != "manuscript_vpe55.pdf":
                entries[item.filename] = z.read(item.filename)
                
    with open(pdf_to_add, 'rb') as f:
        entries["manuscript_vpe55.pdf"] = f.read()
        
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for fname, data in entries.items():
            z.writestr(fname, data)
    print(f"Updated {zip_path} with pristine sanitized PDF")

def verify_all():
    print("--- Final Verification of All PDFs ---")
    targets = [
        ("01_Empirical_Pricing_Audit_VPE55/Empirical_Case_Study_Real_World_Pricing_RRPD_Fairness_Audit.pdf", 11),
        ("01_Empirical_Pricing_Audit_VPE55/manuscript_vpe55.pdf", 11),
        ("02_Physics_of_Economic_Value_VPE21/The_Physics_of_Economic_Value.pdf", 15),
        ("02_Physics_of_Economic_Value_VPE21/manuscript_vpe21.pdf", 15),
        ("03_Thermodynamic_State_Space_VPE49/Thermodynamic_Work_Antiwork_State_Space_Dynamics.pdf", 36),
        ("03_Thermodynamic_State_Space_VPE49/manuscript_vpe49.pdf", 36),
    ]
    all_clean = True
    for path, expected_pages in targets:
        doc = fitz.open(path)
        pages = len(doc)
        matches = []
        q_count = 0
        for i, page in enumerate(doc):
            text = page.get_text()
            if "Coonabarabran" in text or "2357" in text:
                matches.append(i + 1)
        print(f"  {path}: {pages} pages (expected {expected_pages}), matches: {matches}")
        if matches or pages != expected_pages:
            all_clean = False
        doc.close()
    print("All clean:", all_clean)

if __name__ == "__main__":
    sanitize_paper_01()
    sanitize_paper_02()
    sanitize_paper_03()
    update_zip_archives()
    verify_all()
