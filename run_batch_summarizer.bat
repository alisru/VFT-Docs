@echo off
setlocal enableddelayedexpansion
title VFT Batch Document Summarizer

:MENU
cls
echo ======================================================
echo           VFT BATCH DOCUMENT SUMMARIZER
echo =====================================================
echo.
echo   [1] Custom Batch  - Choose file limit and cooling delay
echo   [2] Auto Mode     - Run continuously until all files are done
echo   [3] Open Viewer   - Launch file_summaries_viewer.html
echo   [4] Exit
echo.
echo =====================================================
set /p MODE="Select an option (1-4) [default: 1]: "
if "%MODE%"=="" set MODE=1

if "%MODE%"=="1" goto CUSTOM_BATCH
if "%MODE%"=="2" goto AUTO_MODE
if "%MODE%"=="3" goto LAUNCH_VIEWER
if "%MODE%"=="4" goto END
goto MENU

:CUSTOM_BATCH
cls
echo =====================================================
echo                   CUSTOM BATCH MODE
echo =====================================================
echo.
set /p LIMIT="How many files to process in this batch? [default: 10]: "
if "%LIMIT%"=="" set LIMIT=10

set /p MAX_TEMP="Trigger cooling if GPU reaches? [default: 68C]: "
if "%MAX_TEMP%"=="" set MAX_TEMP=68

set /p COOL_TEMP="Cool down to target temperature? [default: 48C]: "
if "%COOL_TEMP%"=="" set COOL_TEMP=48

echo.
echo Starting batch: %LIMIT% files (Pause if >=%MAX_TEMP%C, Cool to <=%COOL_TEMP%C)...
echo.
python batch_summarize_local.py --limit %LIMIT% --max-temp %MAX_TEMP% --cool-temp %COOL_TEMP%

echo.
echo ====================================================
echo                   BATCH COMPLETE
echo =====================================================
echo.
set /p AGAIN="Would you like to run another batch? (Y/N) [default: Y]: "
if "%AGAIN%"=="" set AGAIN=Y
if /i "%AGAIN%"=="Y" goto CUSTOM_BATCH
goto MENU

:AUTO_MODE
cls
echo ====================================================
echo                    AUTO RUN MODE
echo =====================================================
echo This mode will process all remaining files continuously
echo until the entire queue is completely finished.
echo.
set /p MAX_TEMP="Trigger cooling if GPU reaches? [default: 68C]: "
if "%MAX_TEMP%"=="" set MAX_TEMP=68

set /p COOL_TEMP="Cool down to target temperature? [default: 48C]: "
if "%COOL_TEMP%"=="" set COOL_TEMP=48

echo.
echo Starting auto run (Pause if >=%MAX_TEMP%C, Cool to <=%COOL_TEMP%C)...
echo (Press Ctrl+C at any time to safely stop - progress is saved per file)
echo.
python batch_summarize_local.py --limit 9999 --max-temp %MAX_TEMP% --cool-temp %COOL_TEMP%

echo.
echo ====================================================
echo           ALL FILES SUMMARIZED SUCCESSFULLY!
echo ====================================================
echo.
pause
goto MENU

:LAUNCH_VIEWER
start "" "file_summaries_viewer.html"
goto MENU

:END
echo.
echo Exiting.
endlocal
