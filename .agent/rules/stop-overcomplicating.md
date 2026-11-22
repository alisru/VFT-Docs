# Stop Overcomplicating & Token Conservation Rule

## 1. Absolute Ban on Self-Invented Prep Scripts
* When the user asks to run, test, or execute something, **run the existing project command immediately**.
* You are strictly forbidden from writing intermediate setup scripts, grid-search scripts, solver scripts, inspection scripts, or helper wrappers unless the user explicitly requests one.
* Do not check "prerequisites", "environments", or "options" across multiple turns when the project already has established CLI commands.

## 2. Single-Turn Execution (One Request = One Direct Action)
* If the user says "run a test on X", execute that exact test in the very same turn.
* Never split a simple task into: Turn 1 (inspecting flags) -> Turn 2 (creating a file) -> Turn 3 (asking to run) -> Turn 4 (running).
* The 2-Line Test: Take the shortest, most direct path to the result.

## 3. Ban on Mass Batch Operations During Single-Item Tasks
* NEVER trigger whole-database rebuilds, 14,000-file crawls, or project-wide batch sweeps when working on a single story or test.
* Surgical single-file execution only.

## 4. Chat Explanations Must Be Direct
* Stop explaining your internal reasoning, excuses, or over-engineered theories.
* State what was done, show the result, and stop.
