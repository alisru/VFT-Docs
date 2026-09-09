# Trackable File Operations & IDE Diff Logging

## Core Requirement: Mandatory Use of IDE File Tools
All file creations, updates, overwrites, and content generations within the workspace MUST be performed using Antigravity's native IDE tools:
* `write_to_file` — for creating new files or full overwrites.
* `replace_file_content` — for modifying or patching existing files.

## Absolute Ban on Scripted File Writing
* **NEVER** use Python scripts (e.g. `with open(..., 'w')`, `f.write()`), PowerShell commands (e.g. `Out-File`, `Set-Content`, `Add-Content`, `>`, `>>`), or shell redirects to create, generate, or modify workspace files.
* **NEVER** generate deliverables, markdown documents, audit reports, or code files by executing one-off shell scripts that write directly to the filesystem.

## Rationale
Writing directly to disk via background shell commands or Python scripts bypasses Antigravity's IDE change-tracking layer:
1. It prevents visual diffs from appearing in the user's editor.
2. It breaks the IDE checkpoint and history system.
3. It deprives the user of the ability to inspect diffs and click **Undo / Revert** on changes.
