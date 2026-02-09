@echo off
REM ============================================
REM  GDrive IO Folder Sync Script
REM  1. Downloads from GDrive IO → local IO
REM  2. Moves downloaded files to GDrive "Processed" folder
REM ============================================

setlocal enabledelayedexpansion

set "GDRIVE_IO_ID=1eFfacNbz1A45n_yVH6m2l4jN7LvTBF7S"
set "LOCAL_IO=E:\Vector Field Theory\VFT Docs\_VFT MD\IO"

echo.
echo ========================================
echo   Step 1: Syncing GDrive IO Folder...
echo ========================================
echo.

REM Download all files from GDrive IO to local IO
rclone copy VFT: "%LOCAL_IO%" --drive-root-folder-id %GDRIVE_IO_ID% --progress

echo.
echo ========================================
echo   Step 2: Moving files to Processed...
echo ========================================
echo.

REM Move all files on GDrive from IO root to IO/Processed
REM This uses rclone move with the same root folder, targeting the Processed subfolder
rclone move VFT: VFT:Processed --drive-root-folder-id %GDRIVE_IO_ID% --progress

echo.
echo ========================================
echo   Step 3: Processing Local Files...
echo ========================================
echo.
echo Running conversion, sorting, and indexing...
python "E:\Vector Field Theory\VFT Docs\_AI files and chat logs\process_io_files.py"

echo.
echo ========================================
echo   Sync & Processing Complete!
echo ========================================
echo.
echo Local files processed and moved to their folders.
echo Original docs archived in: _VFT MD/_Archive/Processed_Imports
echo.
pause
