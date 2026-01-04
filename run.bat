@echo off
echo Starting Local Online Judge...

cd server
if not exist "venv" (
    echo Virtual environment not found. Please run 'setup.bat' first.
    exit /b 1
)

call venv\Scripts\activate
echo Server starting on http://localhost:5002
python app.py
