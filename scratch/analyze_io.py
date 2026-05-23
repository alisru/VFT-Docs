import csv
import os

csv_path = r"E:\Vector Field Theory\VFT Docs\_AI files and chat logs\vft_io_database.csv"
io_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\io"

with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows in CSV: {len(rows)}")

# Let's see all rows that have paths starting with io\
io_rows = [row for row in rows if row.get('Path', '').startswith('io\\')]
print(f"Rows with path starting with 'io\\': {len(io_rows)}")

for i, row in enumerate(io_rows[:30]):
    print(f"{i+1}. Filename: {row['Filename']} | Path: {row['Path']} | Plane: {row.get('PlaneCategory')} | Node: {row.get('NodeCategory')} | Tags: {row.get('DetailedTags')}")
