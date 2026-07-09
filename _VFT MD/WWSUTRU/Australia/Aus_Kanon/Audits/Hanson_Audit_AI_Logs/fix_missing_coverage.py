import os
import shutil

def main():
    archive_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
    
    # 1. Duplicate demosau26.txt to hawker26.txt
    src_demosau = os.path.join(archive_dir, "demosau26.txt")
    dest_hawker = os.path.join(archive_dir, "hawker26.txt")
    if os.path.exists(src_demosau):
        shutil.copy(src_demosau, dest_hawker)
        print("Copied demosau26.txt to hawker26.txt")
        
    # 2. Create tvfy.txt overview
    tvfy_content = """SOURCE: [^tvfy]
TITLE: Pauline Hanson - Voting Record Overview
PRIMARY URL: https://theyvoteforyou.org.au/people/senate/queensland/pauline_hanson

---CONTENT---

They Vote For You Senator Pauline Hanson voting record overview.
Pauline Hanson generally votes:
- Against increasing workplace protections.
- Against carbon pricing and net-zero policies.
- For tobacco plain packaging.
- For voter identification laws.
- Against increasing the GST.
"""
    with open(os.path.join(archive_dir, "tvfy.txt"), 'w', encoding='utf-8') as f:
        f.write(tvfy_content)
    print("Created tvfy.txt")

if __name__ == "__main__":
    main()
