import os

def normalize_path(path):
    return path.replace('/', '\\').strip()

def read_batch(category_name, max_chars=2500):
    report_file = r"E:\Vector Field Theory\VFT Docs\.agent\tools\missing_files_categorized.txt"
    root_dir = r"E:\Vector Field Theory\VFT Docs"
    
    files_to_read = []
    capture = False
    output = []
    
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"[{category_name.upper()}]"):
                    capture = True
                    continue
                if capture and line.startswith("["):
                    capture = False
                    break
                if capture and line.startswith("- "):
                    file_path = line[2:].strip()
                    files_to_read.append(file_path)
                    
        print(f"Processing {len(files_to_read)} files for {category_name.upper()}...")
        output.append(f"--- BATCH CONTENT FOR {category_name.upper()} ({len(files_to_read)} files) ---")
        
        for rel_path in files_to_read:
             # The paths in the text file are relative to _VFT MD, so we need to construct the full path
            full_path = os.path.join(root_dir, "_VFT MD", rel_path)
            
            
            output.append(f"\nExample File: {rel_path}")
            output.append("="*60)
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read(max_chars)
                    output.append(content)
                    if len(content) == max_chars:
                        output.append("\n... [TRUNCATED] ...")
            except Exception as e:
                output.append(f"[ERROR READING FILE]: {e}")
            
            output.append("\n" + "="*60)

    except Exception as e:
        output.append(f"Error: {e}")
        
    with open(r"E:\Vector Field Theory\VFT Docs\.agent\temp\batch_content.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print(f"Batch content saved to .agent/temp/batch_content.txt")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        read_batch(sys.argv[1])
    else:
        print("Usage: python read_batch_content.py <CATEGORY_NAME>")
