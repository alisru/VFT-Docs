@echo off
echo ==================================================
echo  Aletheia Control Panel Launcher
echo ==================================================
cd /d "%~dp0"

set PYTHON_BIN=python
if exist ".venv\Scripts\python.exe" (
    set PYTHON_BIN=.venv\Scripts\python.exe
)
if exist "..\.venv\Scripts\python.exe" (
    set PYTHON_BIN=..\.venv\Scripts\python.exe
)

echo [1/3] Starting source server on localhost:8765...
start "Source Server" /min "%PYTHON_BIN%" source_server.py

echo [2/3] Starting panel server on localhost:8080...
start "Panel Server" /min "%PYTHON_BIN%" -m http.server 8080

echo [3/3] Opening Control Panel in browser...
timeout /t 2 /nobreak >nul
start "" "http://localhost:8080/control_panel.html"

echo.
echo Both servers are running in the background.
echo Close this window to shut them down, or press Ctrl+C.
echo ==================================================
pause
