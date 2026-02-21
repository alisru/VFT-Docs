@echo off
REM v4 Psochic Hegemony Grid Launcher (Windows)
REM Launches the standalone HTML file in your default browser

echo ========================================
echo  v4 Psochic Hegemony Grid Launcher
echo  650 Political Spectrum Statements
echo ========================================
echo.
echo Opening grid in your default browser...
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Launch the HTML file
start "" "%SCRIPT_DIR%v4_Hegemony-Grid_650-Statements_COMPLETE.html"

echo.
echo Grid launched successfully!
echo Close this window when done.
echo.
pause
