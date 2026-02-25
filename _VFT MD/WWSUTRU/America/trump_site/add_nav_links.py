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
    "Plane_7_Result.html"
]

desktop_archetype = '                        <a href="Archetype_The_American_Anomaly.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition">Archetype</a>\n'
desktop_map_about = '\n                        <a href="Trump_Hegemony_Visualization.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition">Map</a>\n                        <a href="About_Trump_Audit.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition">About</a>'

mobile_archetype = '                <a href="Archetype_The_American_Anomaly.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition block">Archetype</a>\n'
mobile_map_about = '\n                <a href="Trump_Hegemony_Visualization.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition block">Map</a>\n                <a href="About_Trump_Audit.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition block">About</a>'

for filename in files:
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Desktop Menu Injection
    # Find the start of the links array (before Plane 1)
    content = re.sub(
        r'(<div class="ml-10 flex items-baseline space-x-2">\s*)(<a href="Plane_1_Identity)', 
        r'\1' + desktop_archetype + r'\2', 
        content
    )
    
    # Find the end of the links array (after Plane 7)
    content = re.sub(
        r'(<a href="Plane_7_Result\.html"[^>]*>Effect</a>)', 
        r'\1' + desktop_map_about, 
        content
    )

    # Mobile Menu Injection
    # Find the start of the links array (before Plane 1)
    content = re.sub(
        r'(<div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-700 bg-gray-900">\s*)(<a href="Plane_1_Identity)', 
        r'\1' + mobile_archetype + r'\2', 
        content
    )
    
    # Find the end of the links array (after Plane 7)
    content = re.sub(
        r'(<a href="Plane_7_Result\.html"[^>]*>Effect</a>)', 
        r'\1' + mobile_map_about, 
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated {filename}")
