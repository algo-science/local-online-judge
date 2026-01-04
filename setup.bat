@echo off
echo Setting up Local Online Judge...

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python could not be found. Please install Python 3.8+.
    exit /b 1
)

:: 2. Check g++
g++ --version >nul 2>&1
if %errorlevel% neq 0 (
    echo g++ (C++ compiler) not found.
    echo Please install MinGW or another GCC distribution and add it to PATH.
    echo Recommendation: https://www.msys2.org/
    exit /b 1
) else (
    echo g++ is installed.
)

echo Creating virtual environment...
cd server
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo Setup complete! Run 'run.bat' to start the server.
pause
