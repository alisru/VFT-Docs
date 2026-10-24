@echo off
title VFT Master Project Index & Landscape Explorer
echo ========================================================
echo   VFT Master Project Index & Landscape Explorer
echo ========================================================
cd /d "%~dp0..\..\.."

echo.
echo [1/2] Updating Index Database across 9 Territories...
python "_AI files and chat logs\generate_master_index.py"

echo.
echo [2/2] Launching Web Interface...
echo Server running at http://localhost:8000
start http://localhost:8000/Master_Index.html
python -m http.server 8000
pause
