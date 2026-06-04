@echo off
title Aletheia Bot Control Panel Server
echo ==================================================
echo Starting Aletheia Control Panel Server on port 8000
echo ==================================================
echo.
echo Opening control panel in your default browser...
start "" "http://localhost:8000/bluesky_bot/control_panel.html"
echo.
echo Server is running. Close this window to stop the server.
python -m http.server 8000
pause
