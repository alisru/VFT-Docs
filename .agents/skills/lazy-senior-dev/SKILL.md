---
name: lazy-senior-dev
description: "Diagnostic and execution protocol for applying pragmatic senior developer principles: surgical single-target changes, minimal blast radius, zero collateral damage, and best practices."
---

# Lazy Senior Dev Protocol

Use this skill when designing features, handling sync operations, performing file migrations, or debugging background tasks.

## Protocol Invariants

### 1. The Pre-Execution Checklist
Before executing any file write, sync command, or API call, verify:
1. **Target Count**: Am I targeting 1 file, or did I accidentally queue N files? If N files without an explicit bulk request -> STOP.
2. **Canonical Source**: Am I reading from the original source of truth (database/frontmatter/metadata), or am I reading an intermediate sanitized artifact?
3. **Timestamp Integrity**: Will this command update mtimes on unrelated files? If yes -> ABORT.
4. **Failure Containment**: If this fails, does it log and continue, or does it crash/delete things? (Destructive fallbacks are strictly banned).

### 2. Synchronization Guidelines
- **Local to Cloud**: Always use specific single-target commands (e.g. `rclone copyto local/file.docx remote:folder/file.docx`) rather than whole-directory syncs (`rclone sync folder remote:folder`).
- **Preserve Full Character Sets**: External APIs (Google Drive, Bluesky, Git commit messages) support full punctuation (`:`, `?`, `/`, quotes). Only sanitize for local OS file paths where legally required; do not leak OS restrictions into external systems.

### 3. Debugging Discipline
- Never write throwaway Python/PowerShell scripts for simple inspections.
- Never reconfigure user configs in response to a runtime error unless directed by the user.
