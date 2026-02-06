import os

SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"
OUTPUT_FILE = os.path.join(SOURCE_DIR, "American_Kanon_Full_343.md")

PLANES = [
    "American_Kanon_Plane_1_Identity.md",
    "American_Kanon_Plane_2_Definition.md",
    "American_Kanon_Plane_3_Land.md",
    "American_Kanon_Plane_4_Drive.md",
    "American_Kanon_Plane_5_Method.md",
    "American_Kanon_Plane_6_Cause.md",
    "American_Kanon_Plane_7_Effect.md",
]

def update_full_matrix():
    full_content = []
    
    print(f"Starting matrix update...")
    
    for filename in PLANES:
        filepath = os.path.join(SOURCE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            return
            
        print(f"Reading {filename}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            full_content.append(content)
            
    # Join with newlines to ensure separation between planes
    combined_text = "\n\n".join(full_content)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(combined_text)
        
    print(f"Successfully wrote {len(full_content)} planes to {OUTPUT_FILE}")
    print(f"Total size: {len(combined_text)} bytes")

if __name__ == "__main__":
    update_full_matrix()
