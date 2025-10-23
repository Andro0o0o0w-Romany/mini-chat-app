@echo off
REM Mini Chat System Setup Script for Windows
REM This script sets up both backend and frontend

echo ======================================
echo Mini Chat System - Setup Script
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed
    exit /b 1
)

echo [OK] Python and Node.js are installed
echo.

REM ====================================
REM Backend Setup
REM ====================================
echo ======================================
echo Setting up Backend...
echo ======================================
echo.

cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo SECRET_KEY=django-insecure-dev-key-change-this-in-production
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
        echo USE_MEMORY_CHANNELS=True
    ) > .env
    echo [OK] Created .env file
)

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create demo data
echo Creating demo data...
python create_demo_data.py

echo [OK] Backend setup complete!
echo.

cd ..

REM ====================================
REM Frontend Setup
REM ====================================
echo ======================================
echo Setting up Frontend...
echo ======================================
echo.

cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo REACT_APP_API_URL=http://localhost:8000/api
        echo REACT_APP_WS_URL=localhost:8000
    ) > .env
    echo [OK] Created .env file
)

echo [OK] Frontend setup complete!
echo.

cd ..

REM ====================================
REM Final Instructions
REM ====================================
echo ======================================
echo Setup Complete! [SUCCESS]
echo ======================================
echo.
echo To start the application:
echo.
echo Backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Frontend:
echo   cd frontend
echo   npm start
echo.
echo Demo Login:
echo   Username: demo
echo   Password: demo123
echo.
echo Open http://localhost:3000 in your browser
echo.
echo Happy Chatting!
echo.

pause

