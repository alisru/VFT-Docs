@echo off
echo ==================================================
echo Rebuilding Aletheia Bot Stories Store...
echo ==================================================
cd /d "%~dp0"

set PYTHON_BIN=python
if exist ".venv\Scripts\python.exe" (
    set PYTHON_BIN=.venv\Scripts\python.exe
    goto :run
)
if exist "..\.venv\Scripts\python.exe" (
    set PYTHON_BIN=..\.venv\Scripts\python.exe
    goto :run
)

:run
"%PYTHON_BIN%" scratch\rebuild_registries.py

echo ==================================================
echo Rebuild complete! Refresh your Control Panel.
echo ==================================================
pause
