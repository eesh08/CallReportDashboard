@echo off
REM Call Report Dashboard - Setup and Run Script for Windows
REM This script installs dependencies and launches the dashboard

echo ================================================
echo Call Report Dashboard - Setup ^& Launch
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Check if requirements are already installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error installing dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully
) else (
    echo Dependencies already installed
)

echo.
echo Launching Call Report Dashboard...
echo.
echo The dashboard will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the dashboard
echo.
echo ================================================
echo.

REM Launch the dashboard
streamlit run dashboard.py
