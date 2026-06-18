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
echo Preferred Outlets:
echo   1: Bloomberg             2: NY Times
echo   3: The Saturday Paper    4: Reuters
echo   5: BBC News              6: SMH
echo   7: TechCrunch            8: Washington Post
echo   9: NPR                   all: All Outlets
set /p PREFER="Enter preferred outlets to prioritize (optional, e.g. 1,2,all) [default: none]: "
set /p USE_SEARCH="Enable Google Search Grounding? (y/n) [default: n]: "

echo.
echo Running evaluation batch (RSS: %RSS_COUNT%, Bluesky: %BSKY_COUNT%, Category: %CATEGORY%, Topic: %TOPIC%, Banned: %BANNED_TOPIC%, Prefer: %PREFER%, Search: %USE_SEARCH%)...
echo ==================================================

cd /d "%~dp0"

set ARGS=--rss %RSS_COUNT% --bsky %BSKY_COUNT% 
if not "%TOPIC%"=="" set ARGS=%ARGS% --topic "%TOPIC%"
if not "%BANNED_TOPIC%"=="" set ARGS=%ARGS% --banned-topic "%BANNED_TOPIC%"
if not "%CATEGORY%"=="" set ARGS=%ARGS% --category "%CATEGORY%"
if not "%PREFER%"=="" set ARGS=%ARGS% --prefer "%PREFER%"
if /i "%USE_SEARCH%"=="y" set ARGS=%ARGS% --search

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
"%PYTHON_BIN%" bluesky_bot\google_ai_studio_one_shot.py %ARGS%

echo ==================================================
echo Batch execution complete! Refresh your Control Panel.
echo ==================================================
pause
