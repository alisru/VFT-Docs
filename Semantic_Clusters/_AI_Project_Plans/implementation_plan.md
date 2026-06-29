# Implementation Plan: Batch Uploading & Syncing Deduplicated Notebooks to NotebookLM

This plan outlines the automated, file-list-driven strategy for uploading and managing files in Google NotebookLM. It implements tracking files to selectively upload, delete, and re-upload (update) files based on state flags.

## Proposed Strategy

We will use JSON tracking manifests (`notebook-[slug]-filelist.json`) for each of the 5 notebooks. This allows both the user and the agent to edit a simple list to flag files for uploading or updating.

### Tracking Schema (`notebook-[slug]-filelist.json`)
```json
{
  "notebook_name": "Information Physics & Thermodynamics",
  "notebook_id": "UUID_or_null",
  "files": [
    {
      "relative_path": "_VFT MD/Physics/2c_Boundary_and_Phase_Fragmentation.md",
      "status": "pending", 
      "source_id": null
    }
  ]
}
```

#### Status Transitions:
* `pending`: The file has not been uploaded. The script will upload it via `notebook_add_text`, save the resulting `source_id`, and set status to `uploaded`.
* `uploaded`: The file is verified as synced. The script skips it.
* `update_requested`: The user or agent wants to push edits. The script will call `source_delete` on the stored `source_id`, perform a fresh `notebook_add_text` upload, update the `source_id`, and set the status back to `uploaded`.

## Proposed Changes

### [Semantic_Clusters]

#### [NEW] [batch_upload_notebooks.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/batch_upload_notebooks.py)
* Automatically initializes the `notebooklm-mcp` handshake.
* Reads the tracking JSONs, executes status transitions (uploading new texts, deleting and re-uploading modified files), and writes back the updated states.
* Configures a delay (e.g. 3s) to prevent API rate-limiting.

#### [NEW] `notebook-[slug]-filelist.json` files
* Generated initially from the subtraction test index, mapping pending and uploaded files to their directories.

#### [MODIFY] [implementation_plan.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/_AI_Project_Plans/implementation_plan.md)
* Updated plan version with file-list architecture.

## Verification Plan

### Automated Verification
* Run dry-runs of the script to print expected actions without committing uploads.
* Log progress file-by-file with response statuses.

### Manual Verification
* Checking the state JSONs after runs to ensure status fields transition to `uploaded` and capture valid UUIDs.
