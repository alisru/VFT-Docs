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

style_old = """        .font-serif { font-family: 'Merriweather', serif; }

        /* Hide scrollbar for mobile nav */
        .hide-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .hide-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
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

        @media (max-width: 640px) {
            table, thead, tbody, th, td, tr { display: block; }
            thead tr { position: absolute; top: -9999px; left: -9999px; }
            tr { border: 1px solid #e2e8f0; border-radius: 0.75rem; margin-bottom: 1.5rem; background: white; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); overflow: hidden; }
            td { 
                border: none; position: relative; padding-left: 1.25rem !important; padding-right: 1.25rem !important; padding-top: 0.75rem !important; padding-bottom: 0.75rem !important;
            }
            td:nth-of-type(1) {
                background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; padding-top: 0.5rem !important; padding-bottom: 0.5rem !important;
            }
            td:nth-of-type(2) { padding-bottom: 0.25rem !important; }
            td:nth-of-type(3) { padding-top: 0.25rem !important; padding-bottom: 0.25rem !important; display: inline-block; width: auto; margin-right: 1rem; }
            td:nth-of-type(4) { padding-top: 0.25rem !important; padding-bottom: 0.25rem !important; display: inline-block; width: auto; }
            td:nth-of-type(5) { padding-top: 1rem !important; border-top: 1px solid #f1f5f9; margin-top: 0.5rem;}
        }
    </style>"""

for f in files:
    filepath = os.path.join(dir_path, f)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace style
    content = content.replace(style_old, style_new)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

print(f"Successfully updated {len(files)} files with new CSS.")
