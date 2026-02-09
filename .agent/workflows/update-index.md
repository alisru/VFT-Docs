---
description: How to synchronize the project index after adding or modifying documents
---

This workflow ensures that new documents are immediately discoverable via full-text search.

### 1. Manual Update (User)
If you have added new files manually in your file explorer:
- Run the [start_vft_index.bat](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/start_vft_index.bat).
- It automatically triggers the re-indexing script before launching the server.

### 2. AI Maintenance Protocol (Agent)
Whenever an AI agent creates a new `.md` file in `_VFT MD` or its subdirectories:
- **Mandate**: The agent SHOULD run the re-indexing script to maintain search integrity.
- **Command**:
// turbo
```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\generate_vft_index.py"
```

### 3. Verification of Inclusion
After indexing, verify the new file exists in:
1. `index_data.json` (as a new node with content).
2. `Master_Index.md` (as a new list item with a link).
3. `Master_Index.html` (viewable in the Tree View or Search).

### 4. Background Updates
To perform an update without starting the web server UI, simply run the Python generator directly.
```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\generate_vft_index.py"
```
