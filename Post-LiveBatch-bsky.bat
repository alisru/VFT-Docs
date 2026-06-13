@echo off
cd /d "%~dp0"

echo Running pre-flight validation...
set PYTHON_BIN=python
if exist ".venv\Scripts\python.exe" (
    set PYTHON_BIN=.venv\Scripts\python.exe
    goto :run
)
if exist "bluesky_bot\.venv\Scripts\python.exe" (
    set PYTHON_BIN=bluesky_bot\.venv\Scripts\python.exe
    goto :run
)

:run
"%PYTHON_BIN%" bluesky_bot\validate_batch.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo ==================================================
    echo ERROR: Pre-flight validation failed! Posting aborted.
    echo ==================================================
    pause
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File .\Post-LiveBatch.ps1
pause
