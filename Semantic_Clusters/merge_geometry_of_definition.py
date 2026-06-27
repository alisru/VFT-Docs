import os
import sys

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    # Define source paths
    file1_path = os.path.join(workspace_root, "_VFT MD", "Physics", "Geometry of Definition Paper description and geometric information clause.md")
    file2_path = os.path.join(workspace_root, "_VFT MD", "Physics", "Geometry_of_Definition_and_Totality_Event_Frame.md")
    file3_path = os.path.join(workspace_root, "_VFT MD", "Physics", "The Geometry of Definition.md")
    file4_path = os.path.join(workspace_root, "_VFT MD", "Actualism", "Truth", "The Geometry of Definition： Ancient vs Modern Cosmology.md")
    
    output_path = os.path.join(workspace_root, "_VFT MD", "Physics", "The Geometry of Definition Monograph.md")
    
    print("Reading source documents...", flush=True)
    
    with open(file1_path, 'r', encoding='utf-8') as f:
        file1_content = f.read()
    with open(file2_path, 'r', encoding='utf-8') as f:
        file2_content = f.read()
    with open(file3_path, 'r', encoding='utf-8') as f:
        file3_content = f.read()
    with open(file4_path, 'r', encoding='utf-8') as f:
        file4_content = f.read()
        
    # Clean LaTeX conversion errors in File 3
    print("Cleaning up LaTeX conversion errors...", flush=True)
    
    # Replace image1 with \Phi
    file3_content = file3_content.replace(
        '![](media/image1.png){width="9.716754155730534e-2in" height="0.25911417322834646in"}',
        '$\\Phi$'
    )
    # Replace image4 with \theta
    file3_content = file3_content.replace(
        '![](media/image4.png){width="0.23193350831146106in" height="0.2530183727034121in"}',
        '$\\theta$'
    )
    # Replace image5 with \phi
    file3_content = file3_content.replace(
        '![](media/image5.png){width="0.23193350831146106in" height="0.2530183727034121in"}',
        '$\\phi$'
    )
    # Replace image2 with \mathcal{L}
    file3_content = file3_content.replace(
        '![](media/image2.png){width="0.23193350831146106in" height="0.2530183727034121in"}',
        '$\\mathcal{L}$'
    )
    
    # Clean up double headers/titles during compilation
    # Strip main titles from sub-files so they read as consecutive sections
    file2_clean = file2_content.lstrip().replace("# The Geometry of Definition & The Totality Event Frame", "")
    file3_clean = file3_content.lstrip().replace("# The Ontology of Action and the Transmission of Will", "## Part 7: The Ontology of Action and the Transmission of Will")
    file4_clean = file4_content.lstrip().replace("# THE GEOMETRY OF TRUTH: Ancient vs. Modern Cosmology", "")
    
    print("Assembling monograph...", flush=True)
    
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("# The Geometry of Definition\n")
        out.write("### A Unified Monograph on Meaning, Time, Language, and Cosmology\n\n")
        
        # 1. Preface (File 1)
        out.write("## PREFACE & INTRODUCTORY CONTEXT\n\n")
        out.write(file1_content)
        out.write("\n\n---\n\n")
        
        # 2. Part A: The Mathematical Core (File 2)
        out.write("## CHAPTER 1: THE MATHEMATICS OF DEFIINITION & TIME\n\n")
        out.write(file2_clean.strip())
        out.write("\n\n---\n\n")
        
        # 3. Part B: Somatic Phonetics (File 3)
        out.write("## CHAPTER 2: PHONETIC ARCHITECTURES & ACOUSTIC BIOLOGY\n\n")
        out.write(file3_clean.strip())
        out.write("\n\n---\n\n")
        
        # 4. Part C: Cosmology & Hegemony Elements (File 4)
        out.write("## CHAPTER 3: ANCIENT VS. MODERN COSMOLOGY & THE ALCHEMIC MATRIX\n\n")
        out.write(file4_clean.strip())
        out.write("\n")
        
    print(f"Monograph compiled successfully at {output_path}!", flush=True)

if __name__ == "__main__":
    main()
