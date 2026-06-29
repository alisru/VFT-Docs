import zipfile
import os
import sys

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    docx_path = os.path.join(workspace_root, "Physics", "The Geometry of Definition.docx")
    dest_dir = os.path.join(workspace_root, "drawing board", "docx_media")
    
    if not os.path.exists(docx_path):
        print(f"Error: Docx file not found at {docx_path}")
        return
        
    print(f"Opening zip archive: {docx_path}...", flush=True)
    
    os.makedirs(dest_dir, exist_ok=True)
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        # List all files inside docx
        namelist = z.namelist()
        
        # Find all media files
        media_files = [f for f in namelist if 'word/media/' in f]
        print(f"Found {len(media_files)} media files in the docx:", flush=True)
        
        for media in media_files:
            base = os.path.basename(media)
            dest_path = os.path.join(dest_dir, base)
            print(f"  * Extracting {media} -> {dest_path}", flush=True)
            with open(dest_path, 'wb') as out_f:
                out_f.write(z.read(media))
                
    print("\nExtraction complete! Checked drawing board/docx_media/ folder.", flush=True)

if __name__ == "__main__":
    main()
