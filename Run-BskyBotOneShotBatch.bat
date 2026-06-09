@echo off
echo ==================================================
echo Aletheia Bot: One-Shot Batch Evaluator
echo ==================================================

set /p RSS_COUNT="Enter number of RSS stories to harvest (default: 5): "
if "%RSS_COUNT%"=="" set RSS_COUNT=5

set /p BSKY_COUNT="Enter number of Bluesky stories to harvest (default: 15): "
if "%BSKY_COUNT%"=="" set BSKY_COUNT=15

set /p CATEGORY="Enter category or categories (general, tech, business, politics, science, world — or CSV e.g. politics,tech) [default: general]: "


set /p TOPIC="Enter topic filter query (optional, e.g. Trump) [default: none]: "
set /p BANNED_TOPIC="Enter banned topics/keywords to exclude (optional, comma-separated) [default: travel, sport, entertainment]: "

echo.
echo Running evaluation batch (RSS: %RSS_COUNT%, Bluesky: %BSKY_COUNT%, Category: %CATEGORY%, Topic: %TOPIC%, Banned: %BANNED_TOPIC%)...
echo ==================================================

cd /d "%~dp0"

set ARGS=--rss %RSS_COUNT% --bsky %BSKY_COUNT% 
if not "%TOPIC%"=="" set ARGS=%ARGS% --topic "%TOPIC%"
if not "%BANNED_TOPIC%"=="" set ARGS=%ARGS% --banned-topic "%BANNED_TOPIC%"
if not "%CATEGORY%"=="" set ARGS=%ARGS% --category "%CATEGORY%"

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe bluesky_bot\google_ai_studio_one_shot.py %ARGS%
) else if exist "bluesky_bot\.venv\Scripts\python.exe" (
    bluesky_bot\.venv\Scripts\python.exe bluesky_bot\google_ai_studio_one_shot.py %ARGS%
) else (
    python bluesky_bot\google_ai_studio_one_shot.py %ARGS%
)

echo ==================================================
echo Batch execution complete! Refresh your Control Panel.
echo ==================================================
pause
