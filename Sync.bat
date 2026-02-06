@echo off
title VFT Folder Sync (Google Drive -> Local)

echo ========================================================
echo CHECKING FOR CHANGES...
echo (This is a dry run. No files will be moved yet.)
echo ========================================================
echo.

:: 1. Run Rclone in Dry Run mode (--dry-run) with Verbose (-v) output
:: This lists files that are "New", "Modified", or "Deleted"
rclone sync VFT:VFT "E:\Vector Field Theory\VFT Docs" --drive-export-formats docx --dry-run -v

echo.
echo ========================================================
echo REVIEW THE CHANGES ABOVE
echo ========================================================
echo.
echo If you see "Transferred: 0", your files are already up to date.
echo.

:: 2. Wait for user input
set /p user_input="Do you want to apply these changes? (Y/N): "

:: 3. Check input. If Y, run the real sync.
if /i "%user_input%"=="Y" (
    echo.
    echo Syncing now...
    echo.
    
    :: The ACTUAL command (No --dry-run)
    rclone sync VFT:VFT "E:\Vector Field Theory\VFT Docs" --drive-export-formats docx --progress
    
    echo.
    echo ---------------------------
    echo SYNC COMPLETE.
    echo ---------------------------
) else (
    echo.
    echo Sync Cancelled by user.
)

:: 4. Keep window open so you can read the final status
pause