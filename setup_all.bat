@echo off
REM ====================================================
REM Rice Mill ERP - Complete Setup Script
REM ====================================================

echo.
echo ====================================================
echo   RICE MILL ERP - COMPLETE APP SETUP
echo ====================================================
echo.
echo This script will:
echo   1. Build the executable app
echo   2. Create a desktop shortcut
echo.
pause

REM Run build script
call build_app.bat

REM Ask if user wants to create shortcut
echo.
set /p CREATE_SHORTCUT="Would you like to create a desktop shortcut? (y/n): "

if /i "%CREATE_SHORTCUT%"=="y" (
    call create_shortcut.bat
) else (
    echo Skipped shortcut creation
)

echo.
echo Setup complete! 
echo Your app is ready to use.
echo.
pause
