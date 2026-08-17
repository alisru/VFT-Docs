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

echo [1/4] Starting source server on localhost:8765...
start "Source Server" /min "%PYTHON_BIN%" source_server.py

echo [2/4] Starting chat & story engine on localhost:8766...
start "Chat Server" /min "%PYTHON_BIN%" chat_server.py

echo [3/4] Starting panel server on localhost:8080...
start "Panel Server" /min "%PYTHON_BIN%" -m http.server 8080

echo [4/4] Opening Control Panel in browser...
timeout /t 2 /nobreak >nul
start "" "http://localhost:8080/control_panel.html"

echo.
echo All Aletheia servers are running:
echo - Control Panel: http://localhost:8080/control_panel.html
echo - Aletheia Chat:  http://localhost:8766/
echo - Source Server:  http://localhost:8765/
echo ==================================================
pause
