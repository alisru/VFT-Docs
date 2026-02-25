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

    # 1. Remove old "Final Score" or "Index" links from the menus
    content = re.sub(r'<a href="index\.html"[^>]*>(Final Score|← Trump Index|Index)</a>\s*', '', content)
    
    # 2. Add "Index" to the right of the brand text.
    brand_regex = r'(<div class="flex-shrink-0[^"]*">.*?<span[^>]*>(?:TRUMP AUDIT|Trump Archetype)</span>)'
    
    index_link = '\n                        <a href="index.html" class="ml-4 px-3 py-2 rounded-md text-sm font-medium text-gray-300 border border-gray-600 hover:text-white hover:bg-gray-700 transition">Index</a>'
    
    if "href=\"index.html\" class=\"ml-4" not in content:
        content = re.sub(brand_regex, r'\1' + index_link, content, flags=re.DOTALL)
        
        # Ensure the flex-shrink container is using flex to align items horizontally
        content = content.replace('<div class="flex-shrink-0">', '<div class="flex-shrink-0 flex items-center">')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated {filename}")
