@echo off
echo ==================================================
echo Rebuilding Aletheia Bot Stories Store...
echo ==================================================
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python rebuild_registries.py
) else if exist "..\.venv\Scripts\python.exe" (
    ..\.venv\Scripts\python rebuild_registries.py
) else (
    python rebuild_registries.py
)

echo ==================================================
echo Rebuild complete! Refresh your Control Panel.
echo ==================================================
pause
