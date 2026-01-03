#!/bin/bash

echo "🚀 Starting Local Online Judge..."

cd server
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run './setup.sh' first."
    exit 1
fi

source venv/bin/activate

# Check if port 5002 is already in use
if lsof -Pi :5002 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 5002 is busy. Killing existing process..."
    kill -9 $(lsof -Pi :5002 -sTCP:LISTEN -t)
fi

echo "🟢 Server starting on http://localhost:5002"
python3 app.py
