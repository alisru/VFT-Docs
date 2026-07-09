import re

filepath = "Plane_2_Definition_Albanese.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the duplicate block using regex split to handle \r\n and \n transparently
parts = re.split(r'## \*\*2\.4 The Why of Definition \(What\.Why\)\*\*?\r?\n', content)
if len(parts) >= 3:
    # parts[0] is everything before first 2.4
    # parts[1] is the duplicate 2.4 and duplicate 2.5
    # parts[2:] is the correct 2.4, 2.5, etc.
    new_content = parts[0] + "## **2.4 The Why of Definition (What.Why)**\n" + "## **2.4 The Why of Definition (What.Why)**\n".join(parts[2:])
    print("Successfully removed the duplicate sections using regex split!")
else:
    print(f"Warning: Expected at least 3 parts when splitting by 2.4 header, got {len(parts)}.")
    # Let's try splitting without newlines
    parts_simple = content.split("## **2.4 The Why of Definition (What.Why)")
    if len(parts_simple) >= 3:
        new_content = parts_simple[0] + "## **2.4 The Why of Definition (What.Why)" + "## **2.4 The Why of Definition (What.Why)".join(parts_simple[2:])
        print("Successfully removed the duplicate sections using simple split!")
    else:
        print(f"Warning: Simple split also failed. Got {len(parts_simple)} parts.")
        new_content = content

# 2. Correct the 6 specific footnotes
replacements = {
    r'\[\^hansard25penalty\]: Anthony Albanese, House of Representatives Hansard, 24 July 2025: https://www.openaustralia.org.au/debates/\?d=2025-07-24':
        r'[^hansard25penalty]: Anthony Albanese, House of Representatives Hansard, 24 July 2025, APH Display: https://www.aph.gov.au/Parliamentary_Business/Hansard/Hansard_Display?bid=chamber/hansardr/28811/&sid=0111',
        
    r'\[\^hansard19defend\]: Anthony Albanese, House of Representatives Hansard, 28 November 2019: https://www.openaustralia.org.au/debates/\?d=2019-11-28':
        r'[^hansard19defend]: Anthony Albanese, House of Representatives Hansard, 28 November 2019, APH Display: https://www.aph.gov.au/Parliamentary_Business/Hansard/Hansard_Display?bid=chamber/hansardr/d70fa2ae-1caf-4548-a026-9f8c47bf03ee/&sid=0189',
        
    r'\[\^hansard25ack\]: Anthony Albanese, House of Representatives Hansard, 10 February 2025: https://www.openaustralia.org.au/debates/\?d=2025-02-10':
        r'[^hansard25ack]: Anthony Albanese, House of Representatives Hansard, 10 February 2025, APH Display: https://www.aph.gov.au/Parliamentary_Business/Hansard/Hansard_Display?bid=chamber/hansardr/28685/&sid=0209',
        
    r'\[\^hansard20future\]: Anthony Albanese, House of Representatives Hansard, 8 October 2020: https://www.openaustralia.org.au/debates/\?d=2020-10-08':
        r'[^hansard20future]: Anthony Albanese, House of Representatives Hansard, 8 October 2020, APH Display: https://www.aph.gov.au/Parliamentary_Business/Hansard/Hansard_Display?bid=chamber/hansardr/a28c39ce-4e49-4b78-914d-ccca686a471e/&sid=0183',
        
    r'\[\^hansard22climate\]: Anthony Albanese, House of Representatives Hansard, 31 March 2022: https://www.openaustralia.org.au/debates/\?d=2022-03-31':
        r'[^hansard22climate]: Anthony Albanese, House of Representatives Hansard, 31 March 2022, APH Display: https://www.aph.gov.au/Parliamentary_Business/Hansard/Hansard_Display?bid=chamber/hansardr/25472/&sid=0420',
        
    r'\[\^voterintegrity21\]: Anthony Albanese, Electoral Legislation Amendment \(Voter Integrity\) Bill 2021 Second Reading Speech, House of Representatives Hansard, 24 November 2021: https://www.openaustralia.org.au/debates/\?d=2021-11-24':
        r'[^voterintegrity21]: Anthony Albanese, Electoral Legislation Amendment (Voter Integrity) Bill 2021 Second Reading Speech, House of Representatives Hansard, 24 November 2021, APH Display: https://www.aph.gov.au/Parliamentary_Business/Hansard/Hansard_Display?bid=chamber/hansardr/25172/&sid=0169',
}

for pattern, replacement in replacements.items():
    new_content, count = re.subn(pattern, replacement, new_content)
    print(f"Footnote replacement count for {pattern[:25]}: {count}")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Saved fixed content back to Plane_2_Definition_Albanese.md")
