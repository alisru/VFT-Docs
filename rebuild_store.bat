@echo off
echo ==================================================
echo Rebuilding Aletheia Bot Stories Store...
echo ==================================================
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python scratch\rebuild_registries.py
) else if exist "..\.venv\Scripts\python.exe" (
    ..\.venv\Scripts\python ..\scratch\rebuild_registries.py
) else (
    python scratch\rebuild_registries.py
)

echo ==================================================
echo Rebuild complete! Refresh your Control Panel.
echo ==================================================
pause
