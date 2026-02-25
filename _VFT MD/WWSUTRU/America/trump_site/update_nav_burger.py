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
    
    # Extract the links inside the nav
    nav_match = re.search(r'<nav.*?>.*?(<a href.*?</a>\s*)+.*?</div>\s*</div>\s*</div>\s*</div>\s*</nav>', content, re.DOTALL)
    if not nav_match:
        # try another regex
        nav_match = re.search(r'<nav.*?>.*?</nav>', content, re.DOTALL)

    if nav_match:
        nav_content = nav_match.group(0)
        
        # let's extract all <a ...>...</a> tags inside the nav
        links = re.findall(r'<a\s+href="[^"]*"\s+class="[^"]*">.*?</a>', nav_content, re.DOTALL)
        
        # the first link in Plane pages is often TRUMP AUDIT brand, but let's check what the links actually are.
        # Actually in the Plane pages, brand is just text, not a link.
        # Wait, in Archetype, the brand is <-WWSUTRU which IS a link.
        
        # Let's extract the brand text/link specifically.
        brand_match = re.search(r'<div class="flex-shrink-0">\s*(<span.*?>.*?</span>)\s*</div>', nav_content, re.DOTALL)
        brand_html = brand_match.group(1) if brand_match else '<span class="text-xl font-bold text-white tracking-widest">TRUMP AUDIT</span>'
        
        # The other links are inside "flex items-baseline" or similar
        links_container_match = re.search(r'<div class="flex items-baseline space-x-2[^"]*">\s*(.*?)\s*</div>\s*</div>', nav_content, re.DOTALL)
        if links_container_match:
            links_html = links_container_match.group(1).strip()
            # extract individual links
            individual_links = re.findall(r'<a.*?</a>', links_html, re.DOTALL)
        else:
            individual_links = []
        
        # Build desktop links
        desktop_links_html = "\n".join([f"                        {link}" for link in individual_links])
        
        # Build mobile links by adding 'block' class
        mobile_links = []
        for link in individual_links:
            mobile_link = re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} block"', link)
            mobile_links.append(f"                {mobile_link}")
        mobile_links_html = "\n".join(mobile_links)

        new_nav = f"""    <nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Branding -->
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        {brand_html}
                    </div>
                </div>

                <!-- Desktop Menu -->
                <div class="hidden md:block">
                    <div class="ml-10 flex items-baseline space-x-2">
{desktop_links_html}
                    </div>
                </div>

                <!-- Mobile Menu Button -->
                <div class="-mr-2 flex md:hidden">
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
        <div class="hidden md:hidden" id="mobile-menu">
            <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-700 bg-gray-900">
{mobile_links_html}
            </div>
        </div>
    </nav>"""

        content = content.replace(nav_content, new_nav)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
