import os
import re

dir_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America\trump_site"
files = [
    "Plane_1_Identity.html",
    "Plane_2_Definition.html",
    "Plane_3_Land.html",
    "Plane_4_Drive.html",
    "Plane_5_Method.html",
    "Plane_6_Foundation.html",
    "Plane_7_Result.html",
    "Archetype_The_American_Anomaly.html"
]

for filename in files:
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the desktop menu and remove index.html link
    def remove_index_link_from_menu(match):
        menu_content = match.group(0)
        # remove any link that goes to index.html from inside these menu blocks
        clean_menu = re.sub(r'<a\s+href="index\.html"[^>]*>.*?</a>\s*', '', menu_content, flags=re.DOTALL)
        return clean_menu

    # Desktop menu
    content = re.sub(r'<div class="ml-10 flex items-baseline space-x-2">.*?</div>', remove_index_link_from_menu, content, flags=re.DOTALL)
    
    # Mobile menu
    content = re.sub(r'<div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-700 bg-gray-900">.*?</div>', remove_index_link_from_menu, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Cleaned {filename}")
