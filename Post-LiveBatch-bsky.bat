@echo off
cd /d "%~dp0"

echo Running pre-flight validation...
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe bluesky_bot\validate_batch.py
) else if exist "bluesky_bot\.venv\Scripts\python.exe" (
    bluesky_bot\.venv\Scripts\python.exe bluesky_bot\validate_batch.py
) else (
    python bluesky_bot\validate_batch.py
)

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
