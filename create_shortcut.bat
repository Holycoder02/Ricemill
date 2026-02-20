@echo off
REM ====================================================
REM Rice Mill ERP - Create Desktop Shortcut
REM ====================================================

echo.
echo Creating desktop shortcut for RiceMill ERP...
echo.

REM Check if executable exists
if not exist "dist\RiceMill ERP.exe" (
    echo ERROR: RiceMill ERP.exe not found in dist folder
    echo Please run build_app.bat first to create the executable
    pause
    exit /b 1
)

REM Get current directory
for /f "tokens=*" %%A in ('cd') do set CURRENT_DIR=%%A

REM Create shortcut using PowerShell
powershell -Command ^
"$WshShell = New-Object -ComObject WScript.Shell; ^
$shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\RiceMill ERP.lnk'); ^
$shortcut.TargetPath = '%CURRENT_DIR%\dist\RiceMill ERP.exe'; ^
$shortcut.WorkingDirectory = '%CURRENT_DIR%'; ^
$shortcut.IconLocation = '%CURRENT_DIR%\dist\RiceMill ERP.exe'; ^
$shortcut.Save()"

if errorlevel 1 (
    echo ERROR: Failed to create shortcut
    pause
    exit /b 1
)

echo.
echo ====================================================
echo   SHORTCUT CREATED SUCCESSFULLY!
echo ====================================================
echo.
echo Desktop shortcut created: RiceMill ERP.lnk
echo You can now click it to launch the app
echo.
pause
