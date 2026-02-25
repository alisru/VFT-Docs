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

nav_start_new = """    <nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col md:flex-row items-center justify-between py-3 md:h-16">
                <!-- Brand / Home Link -->
                <div class="flex w-full md:w-auto items-center justify-between mb-3 md:mb-0">
                    <div class="flex-shrink-0">
                        <span class="text-xl font-bold text-white tracking-widest">TRUMP AUDIT</span>
                    </div>
                </div>
                <!-- Navigation Links (Scrollable on Mobile) -->
                <div class="w-full md:w-auto overflow-x-auto pb-2 md:pb-0 hide-scrollbar -mx-4 px-4 md:mx-0 md:px-0">
                    <div class="flex items-baseline space-x-2 whitespace-nowrap">"""

nav_end_new = """
                    </div>
                </div>
            </div>
        </div>
    </nav>"""

style_old = """        .font-serif { font-family: 'Merriweather', serif; }
    </style>"""

style_new = """        .font-serif { font-family: 'Merriweather', serif; }

        /* Hide scrollbar for mobile nav */
        .hide-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .hide-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
    </style>"""

for f in files:
    filepath = os.path.join(dir_path, f)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace style
    content = content.replace(style_old, style_new)
    
    # Replace nav start
    nav_start_regex = re.compile(
        r'<nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">\s*<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">\s*<div class="flex items-center justify-between h-16">\s*<div class="flex items-center">\s*<div class="flex-shrink-0">\s*<span class="text-xl font-bold text-white tracking-widest">TRUMP AUDIT</span>\s*</div>\s*<div class="hidden md:block">\s*<div class="ml-10 flex items-baseline space-x-2">',
        re.MULTILINE
    )
    content = nav_start_regex.sub(nav_start_new, content)
    
    # Replace nav end
    nav_end_regex = re.compile(
        r'</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</nav>',
        re.MULTILINE
    )
    content = nav_end_regex.sub(nav_end_new, content)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

print(f"Successfully updated {len(files)} files.")
