import os
import sys

def read_batch_chunk(category_name, start_index, limit, max_chars=2000):
    report_file = r"E:\Vector Field Theory\VFT Docs\.agent\tools\missing_files_categorized.txt"
    root_dir = r"E:\Vector Field Theory\VFT Docs"
    output_file = r"E:\Vector Field Theory\VFT Docs\.agent\temp\batch_content.txt"
    
    files_to_read = []
    capture = False
    
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
                    
        total_files = len(files_to_read)
        start_index = int(start_index)
        limit = int(limit)
        end_index = min(start_index + limit, total_files)
        
        chunk_files = files_to_read[start_index:end_index]
        
        print(f"Processing chunk {start_index}-{end_index} of {total_files} files for {category_name.upper()}...")
        
        output = []
        output.append(f"--- BATCH CONTENT FOR {category_name.upper()} (Chunk {start_index}-{end_index}) ---")
        
        for rel_path in chunk_files:
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
            
        with open(output_file, 'w', encoding="utf-8") as f:
            f.write("\n".join(output))
        print(f"Batch chunk saved to {output_file}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 3:
        read_batch_chunk(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python read_batch_chunk.py <CATEGORY> <START_INDEX> <LIMIT>")
