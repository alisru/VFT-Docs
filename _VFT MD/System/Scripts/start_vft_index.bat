@echo off
title VFT Project Index Server
echo Starting Psochic Hegemony Project Index Server...
cd /d "%~dp0"
echo.
echo [1/2] Updating Index Database...
python "..\_AI files and chat logs\generate_vft_index.py"
echo.
echo [2/2] Starting Local Server...
echo Server running at http://localhost:8000
echo Opening browser...
start http://localhost:8000/Master_Index.html
python -m http.server 8000
pause
