@echo off
title VFT Master Index & Landscape Explorer
cd /d "%~dp0"

echo Checking local server status on port 8000...
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo Local server is already running!
    echo Opening http://localhost:8000/Master_Index.html ...
    start http://localhost:8000/Master_Index.html
    exit /b
)

echo Starting local server on port 8000...
start http://localhost:8000/Master_Index.html
python -m http.server 8000
