@echo off
REM Zodiac Explorer - Setup Script for Windows
REM This script sets up the development environment for both backend and frontend

setlocal enabledelayedexpansion

echo ================================================
echo Zodiac Explorer - Setup Script
echo ================================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.7 or higher.
    exit /b 1
)
echo ✓ Python found: 
python --version
echo.

REM Check if Node.js is installed
echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed. Please install Node.js 14 or higher.
    exit /b 1
)
echo ✓ Node.js found: 
node --version
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

REM Create Python virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ✓ Backend setup completed
echo.

REM Setup Frontend
cd ..\frontend

echo Setting up Frontend...

REM Install Node.js dependencies
echo Installing Node.js dependencies...
call npm install

echo ✓ Frontend setup completed
echo.

REM Return to root directory
cd ..

echo ================================================
echo Setup completed successfully!
echo ================================================
echo.
echo Next steps:
echo.
echo 1. To start the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 2. In a new terminal, to start the frontend:
echo    cd frontend
echo    npm start
echo.
echo 3. Open your browser and go to http://localhost:3000
echo.
echo The API will be running on http://localhost:5000
echo ================================================
pause
