---
description: How to manage task state using the No More Fuckups Task Engine v4
---
// turbo-all

# No More Fuckups Task Engine v4

## Quick Start

When user says `/task` with no additional context, run:

```powershell
cd "E:\Vector Field Theory\VFT Docs"
python .agent/tools/task_manager/task_manager.py preflight
python .agent/tools/task_manager/task_manager.py status
python .agent/tools/task_manager/task_manager.py goals
```

This shows lessons, current status, and goal analysis in one go.

## Natural Language Interpretation

When user says `/task <something>`, interpret their intent:

| User Says | My Action |
|-----------|-----------|
| `/task` (no args) | Run preflight + status + goals |
| `/task what's next?` | Run `next` command |
| `/task current` | Run `current` command |
| `/task add <desc>` | Run `add "<desc>"` |
| `/task done` | Complete current task with `done <idx>` |
| `/task start <n>` | Start task n with `start <n>` |
| `/task <work request>` | Add as new task, then start it |
| `/task catchup` | Dump context -> Run `diagnose` -> Update state |

## Catch-Up Protocol (Retroactive Analysis)

When user says `/task catchup`:
1.  **Dump Context**: Write current chat history to `retro_catchup.log`.
2.  **Catch Up**: Run `python .agent/tools/task_manager/task_manager.py catchup retro_catchup.log`.
3.  **Cleanup**: Delete `retro_catchup.log`.
4.  **Report**: Summarize friction points found and tasks updated.

## Session Flow

```
SESSION START
  └→ preflight (lessons, warnings, checklist)
  └→ status (what's current, what's next)
  └→ goals (sub-goals, pitfalls, scope guards)
       ↓
    WORK...
       ↓
  └→ reason <idx> "..." (log decisions)
  └→ done <idx> (complete with lessons)
  └→ git commit (after every state change)
       ↓
SESSION END
  └→ global_sync (save to global registry)
  └→ git commit (final sync commit)
```

## Behavioral Rules

- **NEVER manually edit task.md** — auto-generated
- **Run preflight at session start** — mandatory
- **Run global_sync at session end** — preserves lessons
- **Tag tasks semantically** — enables auto-pitfall linking
- **Log reasoning** — enables postmortem analysis

## Project Rule Compliance

> [!IMPORTANT]
> All rules in `.agent/rules/` are **always-on**. This workflow must obey every one of them.

### 1. Git Commit After Every Edit (`git-commit.md`)
After **any** task state change (`add`, `start`, `done`, `fail`, `reason`, `mistake`, `global_sync`), immediately run:
```powershell
cd "E:\Vector Field Theory\VFT Docs"
git add -A
git commit -m "<summarise change>"
```
Do **not** run `git push`. Summarise the change in the commit message. If changes are massive, use `"Massive changes"`.

### 2. Literal Instructions Only (`literal-instructions.md`)
- Execute the user's `/task` command **exactly as interpreted** from the table above.
- Do **not** add, remove, or modify tasks, files, or content beyond what the user explicitly requested.
- If the user asks a question (e.g., `/task what's next?`), answer it and do nothing else.

### 3. No Assumptions (`no-assumptions.md`)
- Do **only** what the user asked.
- Do **not** invent side-tasks, search for files, or trigger actions the user did not request.
- If a command is ambiguous, **ask the user** before acting.

### 4. No Summarisation / Max Context (`no-summary-max-context.md`)
- All task engine outputs (`status`, `goals`, `lessons`, `postmortem`) must be presented in **full** with no summarisation, concatenation, redaction, or reduction.
- Use maximum context window. Do not truncate outputs unless the user explicitly approves.

### 5. Visible Artifacts (`visible-artifacts.md`)
- Task engine output files (`task.md`, `goal_analysis.md`, `lessons_learned.md`) are already generated in the project root — this is correct.
- If the engine or workflow generates **any new file** (report, log, analysis), save it to a **visible workspace folder** (project root, `_AI files and chat logs`, etc.), **not** only to the hidden `.gemini` directory.
- You may also create an artifact copy for version control, but the **primary deliverable must be visible**.

### 6. Scribe Protocol for Written Output (`scribe.md`)
- When generating human-readable reports (e.g., `goal_analysis.md`, postmortem summaries, lessons), apply the Scribe Protocol:
  - Simulate emotional strain before writing.
  - Use varied sentence rhythm (short, long, fragment).
  - No forbidden words: "Delve", "Tapestry", "Underscore", "Testament to", "Landscape", "Foster", "Nuanced", "Multifaceted".
  - Follow Synthesis → Mechanics → Implication flow, not intro-sentence + list dumps.

## Commands Reference

```powershell
cd "E:\Vector Field Theory\VFT Docs"
$TASK = "python .agent/tools/task_manager/task_manager.py"

# Session Start
& $TASK preflight       # MANDATORY: lessons, warnings, checklist
& $TASK status          # Overview of project
& $TASK goals           # Goal analysis with pitfalls

# Task Lifecycle
& $TASK add "Desc" --tags t1,t2   # Add new task
& $TASK start <idx>               # Start with context awareness
& $TASK reason <idx> "Why I did X"
& $TASK done <idx> --lessons "..."

# Views
& $TASK next            # What to do next
& $TASK current         # Current task details
& $TASK lessons         # All lessons learned

# Errors
& $TASK fail <idx> "Reason"
& $TASK postmortem <idx> "Hypothesis"
& $TASK mistake "Name" "Structure" "Example" --tags t1,t2

# Session End
& $TASK global_sync     # Sync to global registry

# MANDATORY after every state change above:
git add -A
git commit -m "<summarise change>"
```

## Key Files

| File | Purpose |
|------|---------|
| `tasks.json` | Source of truth |
| `task.md` | Auto-generated view |
| `goal_analysis.md` | AI goal breakdown |
| `lessons_learned.md` | Error patterns + lessons |
| `.agent/global_mistakes.json` | Cross-conversation learning |
