import json

path = r"E:\Vector Field Theory\VFT Docs\_VFT MD\index_data.json"
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

def print_tree(node, depth=0):
    if depth > 3:
        return
    print("  " * depth + f"- {node['name']} ({node['type']})")
    if 'children' in node:
        for child in node['children']:
            print_tree(child, depth + 1)

print_tree(data)
