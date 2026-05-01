---
description: How to process and sort new documents from the IO folder with GDrive sync and LaTeX remediation
---

This workflow automates the ingestion of new documents from the `IO` folder, including syncing from Google Drive and cleaning up Gemini-generated images into LaTeX.

### Step 1: Sync from Google Drive
Run the sync batch file to pull new documents into the local `IO` folder.

// turbo
```powershell
cmd /c "e:\Vector Field Theory\VFT Docs\sync_gdrive_io.bat"
```

### Step 2: Convert and Sort Documents
Convert `.docx` and `.pdf` files to Markdown and move them to their respective folders based on thematic content.

// turbo
```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\process_io_files.py"
```

### Step 3: Remediate LaTeX (Automatic)
Run the remediation script to replace known image dimensions with LaTeX/Unicode.

// turbo
```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\remediate_latex.py" --write
```

### Step 4: AI OCR for Unmatched Images (Agent Task)
If `remediate_latex.py` reports "Unmatched" images (Gemini-generated images without known dimensions), you must:
1.  **Scan** the `_VFT MD` folder for Markdown files containing `media/imageN.png`.
2.  **View** the image files using the `view_file` tool.
3.  **Transcribe** the image content to LaTeX.
4.  **Replace** the image tag in the Markdown file with the LaTeX code.
5.  **Update** the `DIMENSION_LOOKUP` in `remediate_latex.py` so the next sync is automatic.

### Step 5: Final Index Synchronization
Synchronize the master index and search database.

// turbo
```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\generate_vft_index.py"
```
