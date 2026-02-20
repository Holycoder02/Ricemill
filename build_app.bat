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

echo [1/4] Checking Python installation... OK

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [2/4] Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo [2/4] PyInstaller installed successfully
) else (
    echo [2/4] PyInstaller already installed... OK
)

REM Clean old build files
echo [3/4] Cleaning old build files...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec
echo [3/4] Cleaned successfully

REM Build the executable
echo [4/4] Building executable (this may take 1-2 minutes)...
echo.

pyinstaller --onefile --windowed --name "RiceMill ERP" create.py

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
