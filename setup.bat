@echo off
echo Setting up Local Online Judge...

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 goto NoPython

:: 2. Check g++
g++ --version >nul 2>&1
if %errorlevel% neq 0 goto NoGPP
echo g++ is installed.

goto CreateVenv

:NoPython
echo Python could not be found. Please install Python 3.8+.
pause
exit /b 1

:NoGPP
echo g++ (C++ compiler) not found.
echo Please install MinGW or another GCC distribution and add it to PATH.
echo Recommendation: https://www.msys2.org/
pause
exit /b 1

:CreateVenv
echo Creating virtual environment...
cd server
if exist "venv" goto VenvExists
python -m venv venv
echo Virtual environment created.
goto InstallDeps

:VenvExists
echo Virtual environment already exists.

:InstallDeps
echo Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo Setup complete! Run 'run.bat' to start the server.
pause
