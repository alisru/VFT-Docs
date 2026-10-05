@echo off
rem Starts the Chat Context server and opens the dashboard. Close this window to stop it.
cd /d "%~dp0"
start "" /b cmd /c "timeout /t 4 >nul & start http://127.0.0.1:8765"
.venv\Scripts\python -m ctx.server
pause
