@echo off
title VFT PUSH (Local -> Google Drive)
color 0E

echo ========================================================
echo WARNING: PUSHING CHANGES TO GOOGLE DRIVE
echo ========================================================
echo Source:      E:\Vector Field Theory\VFT All Docs
echo Destination: Google Drive (VFT Folder)
echo.
echo This will OVERWRITE files on Google Drive with your local versions.
echo Any Google Docs in the cloud will be replaced by your local .docx files.
echo ========================================================
echo.

:: 1. Dry Run (Check what will happen)
rclone sync "E:\Vector Field Theory\VFT Docs" VFT:VFT --dry-run -v

echo.
echo ========================================================
echo REVIEW THE CHANGES ABOVE
echo ========================================================
echo If you see "Transferred: 0", nothing needs updating.
echo.

:: 2. Safety Pause
set /p user_input="Do you want to UPLOAD these changes to Drive? (Y/N): "

if /i "%user_input%"=="Y" (
    echo.
    echo Uploading...
    
    :: The Real Command (Local -> Remote)
    rclone sync "E:\Vector Field Theory\VFT Docs" VFT:VFT --progress
    
    echo.
    echo ---------------------------
    echo UPLOAD COMPLETE.
    echo ---------------------------
) else (
    echo.
    echo Upload Cancelled.
)

pause