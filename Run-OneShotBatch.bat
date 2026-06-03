@echo off
echo ==================================================
echo Aletheia Bot: One-Shot Batch Evaluator
echo ==================================================

set /p RSS_COUNT="Enter number of RSS stories to harvest (default: 5): "
if "%RSS_COUNT%"=="" set RSS_COUNT=5

set /p BSKY_COUNT="Enter number of Bluesky stories to harvest (default: 15): "
if "%BSKY_COUNT%"=="" set BSKY_COUNT=15

echo.
echo Running evaluation batch (RSS: %RSS_COUNT%, Bluesky: %BSKY_COUNT%)...
echo ==================================================

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe bluesky_bot\google_ai_studio_one_shot.py --rss %RSS_COUNT% --bsky %BSKY_COUNT%
) else if exist "bluesky_bot\.venv\Scripts\python.exe" (
    bluesky_bot\.venv\Scripts\python.exe bluesky_bot\google_ai_studio_one_shot.py --rss %RSS_COUNT% --bsky %BSKY_COUNT%
) else (
    python bluesky_bot\google_ai_studio_one_shot.py --rss %RSS_COUNT% --bsky %BSKY_COUNT%
)

echo ==================================================
echo Batch execution complete! Refresh your Control Panel.
echo ==================================================
pause
