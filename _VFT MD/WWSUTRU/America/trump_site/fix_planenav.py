import os
import re

dir_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America\trump_site"
files = [
    ("Plane_1_Identity.html", "Who"),
    ("Plane_2_Definition.html", "What"),
    ("Plane_3_Land.html", "Where"),
    ("Plane_4_Drive.html", "Why"),
    ("Plane_5_Method.html", "How"),
    ("Plane_6_Foundation.html", "Cause"),
    ("Plane_7_Result.html", "Effect")
]

for filename, active_label in files:
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate Desktop Links
    desktop_links = []
    desktop_links.append('                        <a href="Archetype_The_American_Anomaly.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition">Archetype</a>')
    
    for fname, label in files:
        if fname == filename:
            desktop_links.append(f'                        <a href="{fname}" class="px-3 py-2 rounded-md text-sm font-medium bg-blue-800 text-white transition-colors">{label}</a>')
        else:
            desktop_links.append(f'                        <a href="{fname}" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors">{label}</a>')

    desktop_links.append('                        <a href="Trump_Hegemony_Visualization.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition">Map</a>')
    desktop_links.append('                        <a href="About_Trump_Audit.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition">About</a>')
    
    desktop_html = "\n".join(desktop_links)

    # Generate Mobile Links
    mobile_links = []
    mobile_links.append('                <a href="Archetype_The_American_Anomaly.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition block">Archetype</a>')
    
    for fname, label in files:
        if fname == filename:
            mobile_links.append(f'                <a href="{fname}" class="px-3 py-2 rounded-md text-sm font-medium bg-blue-800 text-white transition-colors block">{label}</a>')
        else:
            mobile_links.append(f'                <a href="{fname}" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors block">{label}</a>')

    mobile_links.append('                <a href="Trump_Hegemony_Visualization.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition block">Map</a>')
    mobile_links.append('                <a href="About_Trump_Audit.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition block">About</a>')

    mobile_html = "\n".join(mobile_links)

    new_nav = f"""    <nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Branding -->
                <div class="flex items-center">
                    <div class="flex-shrink-0 flex items-center">
                        <span class="text-xl font-bold text-white tracking-widest">TRUMP AUDIT</span>
                        <a href="index.html" class="ml-4 px-3 py-2 rounded-md text-sm font-medium text-gray-300 border border-gray-600 hover:text-white hover:bg-gray-700 transition">Index</a>
                    </div>
                </div>

                <!-- Desktop Menu -->
                <div class="hidden lg:block">
                    <div class="ml-10 flex items-baseline space-x-2">
{desktop_html}
                    </div>
                </div>

                <!-- Mobile Menu Button -->
                <div class="-mr-2 flex lg:hidden">
                    <button type="button" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')" class="bg-gray-800 inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" aria-controls="mobile-menu" aria-expanded="false">
                        <span class="sr-only">Open main menu</span>
                        <svg class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div class="hidden lg:hidden" id="mobile-menu">
            <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-700 bg-gray-900">
{mobile_html}
            </div>
        </div>
    </nav>"""

    # Replace the whole <nav>...</nav>
    content = re.sub(r'<nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">.*?</nav>', new_nav, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Fixed {filename}")
