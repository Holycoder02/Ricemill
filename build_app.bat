@echo off
REM ====================================================
REM Rice Mill ERP - Build Executable Script
REM ====================================================

echo.
echo ====================================================
echo   RICE MILL ERP - APP BUILDER
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo [1/5] Checking Python installation... OK

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [2/5] Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo [2/5] PyInstaller installed successfully
) else (
    echo [2/5] PyInstaller already installed... OK
)

REM Install requirements
echo [3/5] Installing dependencies...
python -m pip install -r requirements.txt >nul 2>&1
echo [3/5] Dependencies installed... OK

REM Clean old build files
echo [4/5] Cleaning old build files...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
echo [4/5] Cleaned successfully

REM Build the executable
echo [5/5] Building executable (this may take 1-2 minutes)...
echo.

pyinstaller --onefile --windowed --name "RiceMill ERP" ^
    --add-data "db;db" ^
    --add-data "auth;auth" ^
    --add-data "ui;ui" ^
    --add-data "utils;utils" ^
    --hidden-import "db" ^
    --hidden-import "db.connection" ^
    --hidden-import "db.schema" ^
    --hidden-import "db.models" ^
    --hidden-import "auth" ^
    --hidden-import "auth.password" ^
    --hidden-import "ui" ^
    --hidden-import "ui.theme" ^
    --hidden-import "ui.components" ^
    --hidden-import "ui.login" ^
    --hidden-import "ui.dashboard" ^
    --hidden-import "ui.invoice" ^
    --hidden-import "utils" ^
    --hidden-import "utils.validators" ^
    --hidden-import "utils.formatters" ^
    app.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

REM Success message
echo.
echo ====================================================
echo   BUILD SUCCESSFUL!
echo ====================================================
echo.
echo Your executable is ready:
echo Location: dist\RiceMill ERP.exe
echo.
echo You can now:
echo   - Double-click the .exe to run the app
echo   - Share it with others (no Python needed)
echo   - Create a desktop shortcut
echo.
pause
