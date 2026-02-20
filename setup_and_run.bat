@echo off
REM Quick Setup Script for ImageSense Analyzer (Windows)
REM Run this to install and run the application

echo ==========================================
echo ImageSense Analyzer - Quick Setup
echo ==========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python is not installed!
    echo Please install Python 3.9 or higher from python.org
    pause
    exit /b 1
)
echo √ Python found
echo.

REM Check for API key
echo Checking for OpenAI API key...
if "%OPENAI_API_KEY%"=="" (
    echo Warning: OPENAI_API_KEY not set!
    echo.
    echo Please set your API key:
    echo   setx OPENAI_API_KEY "your-key-here"
    echo.
    echo Then restart this script.
    echo.
    set /p API_KEY="Enter your OpenAI API key (or press Enter to exit): "
    if "%API_KEY%"=="" (
        echo.
        echo X Cannot proceed without API key
        pause
        exit /b 1
    )
    setx OPENAI_API_KEY "%API_KEY%"
    echo.
    echo √ API key saved
    echo Please restart this script for changes to take effect.
    pause
    exit /b 0
) else (
    echo √ API key found
)
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)
echo √ Dependencies installed successfully
echo.

REM Run the application
echo ==========================================
echo Starting ImageSense Analyzer...
echo ==========================================
echo.

python image_analyzer_app.py

pause
