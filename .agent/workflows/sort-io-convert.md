---
description: How to process and sort new documents from the IO folder
---

This workflow automates the ingestion of new documents from the `IO` folder.

### Overview
1.  **Converts** `.docx` and `.pdf` files to Markdown.
2.  **Sorts** the Markdown files into the correct VFT project folders (Actualism, Analysis, Protocols, etc.).
3.  **Archives** the original input files to `_Archive/Processed_Imports` (safekeeping).
4.  **Updates** the Search Index.
5.  **Ingests** the new content into the Qdrant VDB.

### Usage

**Option 1: Full Sync (Recommended)**
Run `sync_gdrive_io.bat` in the `VFT Docs` folder. This will:
1.  Download new files from GDrive IO.
2.  Archive/Move them on GDrive.
3.  Trigger this processing workflow automatically.

**Option 2: Manual Processing**
If you dropped files manually into `_VFT MD/IO`:

```powershell
python "E:\Vector Field Theory\VFT Docs\_AI files and chat logs\process_io_files.py"
```
