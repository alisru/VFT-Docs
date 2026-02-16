
import os

file_summaries_path = r"E:\Vector Field Theory\VFT Docs\file_summaries_comprehensive.md"
part1_path = r"E:\Vector Field Theory\VFT Docs\.agent\temp\wwsutru_summary_part6.md"
part2_path = r"E:\Vector Field Theory\VFT Docs\.agent\temp\wwsutru_summary_part6.md"
output_path = r"E:\Vector Field Theory\VFT Docs\.agent\temp\wwsutru_filtered_chunk6.md"

def get_existing_paths():
    existing_paths = set()
    try:
        with open(file_summaries_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                if "**Path:**" in line:
                    path = line.split("**Path:**")[-1].strip().strip('`').lower()
                    existing_paths.add(path)
    except Exception as e:
        print(f"Error reading summaries: {e}")
    return existing_paths

def filter_summaries(source_path, existing_paths):
    filtered_lines = []
    current_item = []
    is_missing = False
    
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            if line.startswith("- **"):
                # Complete previous item
                if is_missing and current_item:
                    filtered_lines.extend(current_item)
                
                # Start new item
                current_item = [line]
                try:
                    path_part = line.split("**")[1].strip().lower()
                    path_part = path_part.rstrip(':').rstrip('.').strip()
                    
                    is_missing = path_part not in existing_paths
                    if not is_missing:
                        print(f"Skipping (already exists): {path_part}")
                except Exception:
                    is_missing = True
            elif line.strip() == "" or line.startswith("###"):
                if is_missing and current_item:
                    filtered_lines.extend(current_item)
                current_item = []
                is_missing = False
                filtered_lines.append(line)
            else:
                if current_item:
                    current_item.append(line)
        
        # Final item
        if is_missing and current_item:
            filtered_lines.extend(current_item)
            
        return filtered_lines
    except Exception as e:
        print(f"Error filtering {source_path}: {e}")
        return []

existing = get_existing_paths()
print(f"Found {len(existing)} existing summaries.")

f1 = filter_summaries(part1_path, existing)

with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(f1)

print(f"Filtered summaries saved to {output_path}")
