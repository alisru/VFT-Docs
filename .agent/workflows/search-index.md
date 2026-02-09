---
description: How to perform a deep full-text search across the _VFT MD project using the Master Index
---

This workflow directs the AI to use the `index_data.json` as a high-speed search engine for the project substrate.

### 1. Load the Index
Always start by reading the `index_data.json` file. This file contains the full content and structure of the `_VFT MD` folder.
- Path: `e:\Vector Field Theory\VFT Docs\_VFT MD\index_data.json`

### 2. Search Strategy
When asked to find information on a topic (e.g., "plane", "vector", "hegemony"):
1. **Keyword Search**: Scan the `name` and `content` fields of all file entries in the JSON.
2. **Relevance Ranking**: Prioritize files where:
    - The keyword appears in the `name`.
    - The keyword appears frequently in the `content`.
    - The file is in a relevant subdirectory (e.g., `Theory`, `Philosophy`).

### 3. Execution (The Search Tool)
Do not write custom search logic. Use the definitive search tool provided in the project.

// turbo
```powershell
python "_AI files and chat logs\search_vft_index.py" "YOUR_TOPIC_HERE"
```

#### Parameters:
- **query**: The word or phrase to search for (required).
- **--limit**: Number of results to show (default: 10).

### 4. Verification
After identifying the top candidates from the script's output:
1. Review the **context snippets** provided in the terminal.
2. Use `view_file` on the actual `.md` files to confirm details before reporting to the user.
