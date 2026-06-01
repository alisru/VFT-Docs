# Rule Capture Protocol

When the user defines, corrects, establishes, or refines ANY rule, constraint, or standard during a session:

1. IMMEDIATELY write it as a `.md` file in the appropriate rules folder.
   - Project-specific rules go in the project's own rules folder if one exists.
   - Global/cross-project rules go in `.agent/rules/`.
2. If a rule already exists that covers the same area, UPDATE that file — do not create a duplicate.
3. Confirm in chat that the file was written or updated, and which file was affected.
4. Do NOT just acknowledge a rule verbally and move on. Unwritten rules do not persist across sessions. Verbal acknowledgement alone = TASK FAILURE.

## What counts as a rule being set
- User corrects the AI's output against a standard ("that's wrong, it should be X")
- User defines a format, constraint, or workflow step explicitly
- User says "always do X" or "never do Y"
- User refines or overrides a previous instruction

## This applies to all projects
Every project the user works in. Every session.
