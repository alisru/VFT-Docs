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
       ↓
SESSION END
  └→ global_sync (save to global registry)
```

## Behavioral Rules

- **NEVER manually edit task.md** - auto-generated
- **Run preflight at session start** - mandatory
- **Run global_sync at session end** - preserves lessons
- **Tag tasks semantically** - enables auto-pitfall linking
- **Log reasoning** - enables postmortem analysis

## Commands Reference

```powershell
cd "E:\Vector Field Theory\VFT Docs"
TASK="python .agent/tools/task_manager/task_manager.py"

# Session Start
$TASK preflight       # MANDATORY: lessons, warnings, checklist
$TASK status          # Overview of project
$TASK goals           # Goal analysis with pitfalls

# Task Lifecycle
$TASK add "Desc" --tags t1,t2   # Add new task
$TASK start <idx>               # Start with context awareness
$TASK reason <idx> "Why I did X"
$TASK done <idx> --lessons "..."

# Views
$TASK next            # What to do next
$TASK current         # Current task details
$TASK lessons         # All lessons learned

# Errors
$TASK fail <idx> "Reason"
$TASK postmortem <idx> "Hypothesis"
$TASK mistake "Name" "Structure" "Example" --tags t1,t2

# Session End
$TASK global_sync     # Sync to global registry
```

## Key Files

| File | Purpose |
|------|---------|
| `tasks.json` | Source of truth |
| `task.md` | Auto-generated view |
| `goal_analysis.md` | AI goal breakdown |
| `lessons_learned.md` | Error patterns + lessons |
| `.agent/global_mistakes.json` | Cross-conversation learning |
