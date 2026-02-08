---
description: How to harvest conversation chains and VFT insights from the Vector Database (storage.sqlite)
---

This workflow automates the "Harvest & Decay" protocol to reconstruct context from the VDB.

### 1. Identify the Database Path
The VDB is typically located at:
`_AI files and chat logs\vdb_data\collection\vft_rcp_lexicon\storage.sqlite`

### 2. Search for a Topic
// turbo
Use the `vdb_harvest.py` tool to find a "Seed" sentence and extract its context.
```powershell
python "_AI files and chat logs\vdb_harvest.py" --db "_AI files and chat logs\vdb_data\collection\vft_rcp_lexicon\storage.sqlite" --query "YOUR_TOPIC_HERE" --depth 4
```

### 3. Direct ID Extraction
If you already have a specific message ID (e.g., from a previous harvest):
// turbo
```powershell
python "_AI files and chat logs\vdb_harvest.py" --db "_AI files and chat logs\vdb_data\collection\vft_rcp_lexicon\storage.sqlite" --id "msg_id_here" --depth 6
```

### 4. Integration
1. Review the harvested output in the terminal.
2. If satisfied, pipe the output to a new markdown file in `_VFT MD`:
```powershell
python "_AI files and chat logs\vdb_harvest.py" [args] > "_VFT MD\Conversations\topic_extraction.md"
```

### 5. Advanced Navigation
For manual inspection of table structures or raw payloads, refer to:
`_AI files and chat logs\VDB_Navigation_Protocol.md`
