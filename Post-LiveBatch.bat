@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File .\Post-LiveBatch.ps1
pause
