import os
import sys
import zipfile
import re
import shutil

# Ensure stdout uses utf-8
sys.stdout.reconfigure(encoding='utf-8')

# Configuration
list_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\image_reprocess_list.md"
output_base = r"e:\Vector Field Theory\VFT Docs\_AI files and chat logs\extracted_media"
docx_root = r"e:\Vector Field Theory\VFT Docs"  # Root to search for docx if not in same dir

def normalize_path(path):
    return os.path.normpath(path)

def find_docx(md_path):
    """
    Tries to find the corresponding .docx file.
    Strategy 1: Same directory, same basename, .docx extension.
    Strategy 2: Search in VFT Docs root (less reliable, but useful fallback).
    """
    base, _ = os.path.splitext(md_path)
    docx_candidate = base + ".docx"
    
    if os.path.exists(docx_candidate):
        return docx_candidate
    
    # Try searching by filename in the root if not found locally
    filename = os.path.basename(docx_candidate)
    for root, dirs, files in os.walk(docx_root):
        if filename in files:
            return os.path.join(root, filename)
            
    return None

def extract_media(docx_path, output_folder):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        with zipfile.ZipFile(docx_path, 'r') as docx:
            media_files = [f for f in docx.namelist() if f.startswith('word/media/')]
            if not media_files:
                return 0
                
            for file in media_files:
                docx.extract(file, output_folder)
            
            return len(media_files)
    except zipfile.BadZipFile:
        print(f"Error: Bad zip file {docx_path}")
        return 0
    except Exception as e:
        print(f"Error extracting {docx_path}: {e}")
        return 0

def main():
    if not os.path.exists(list_file):
        print(f"List file not found: {list_file}")
        return

    with open(list_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Filter lines that are actual file paths (start with - e:\)
    file_paths = []
    for line in lines:
        match = re.search(r'- (e:\\.*\.md)', line, re.IGNORECASE)
        if match:
            file_paths.append(match.group(1).strip())

    print(f"Found {len(file_paths)} markdown files in list.")
    
    success_count = 0
    fail_count = 0
    
    for md_path in file_paths:
        docx_path = find_docx(md_path)
        
        # Create a safe folder name from the filename
        doc_name = os.path.splitext(os.path.basename(md_path))[0]
        safe_name = re.sub(r'[^\w\s-]', '', doc_name).strip().replace(' ', '_')
        output_folder = os.path.join(output_base, safe_name)

        if docx_path:
            count = extract_media(docx_path, output_folder)
            if count > 0:
                print(f"[OK] {doc_name}: Extracted {count} images to {safe_name}")
                success_count += 1
            else:
                print(f"[SKIP] {doc_name}: No media found in DOCX or extraction failed.")
        else:
            print(f"[MISSING] {doc_name}: DOCX source not found.")
            fail_count += 1

    print("\n--- Summary ---")
    print(f"Processed: {len(file_paths)}")
    print(f"Successful Extractions: {success_count}")
    print(f"Missing DOCX: {fail_count}")

if __name__ == "__main__":
    main()
