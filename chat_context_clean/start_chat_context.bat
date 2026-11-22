@echo off
rem Starts the Chat Context server with automatic port scanning and opens the dashboard. Close this window to stop it.
cd /d "%~dp0"
.venv\Scripts\python -m ctx.server
pause
