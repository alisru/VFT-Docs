import os
import csv

csv_path = r"E:\Vector Field Theory\VFT Docs\_AI files and chat logs\vft_io_database.csv"
io_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\io"

with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    csv_files = {row['Filename']: row for row in reader}

io_files = os.listdir(io_dir)

missing_in_csv = []
for f in io_files:
    if f not in csv_files and not os.path.isdir(os.path.join(io_dir, f)):
        missing_in_csv.append(f)

print(f"Total missing: {len(missing_in_csv)}")
for i, f in enumerate(sorted(missing_in_csv)):
    print(f"{i+1}: {f}")
