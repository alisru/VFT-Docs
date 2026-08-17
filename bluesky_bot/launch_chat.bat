@echo off
echo ==================================================
echo  Aletheia Chat Server & Story Studio Launcher
echo ==================================================
cd /d "%~dp0"

set PYTHON_BIN=python
if exist ".venv\Scripts\python.exe" (
    set PYTHON_BIN=.venv\Scripts\python.exe
)
if exist "..\.venv\Scripts\python.exe" (
    set PYTHON_BIN=..\.venv\Scripts\python.exe
)

echo Starting Aletheia Chat Server on localhost:8766...
start "Aletheia Chat Server" /min "%PYTHON_BIN%" chat_server.py

timeout /t 2 /nobreak >nul
start "" "http://localhost:8766/"

echo.
echo Aletheia Chat is running at: http://localhost:8766/
echo Press Ctrl+C or close this window to exit.
echo ==================================================
pause
