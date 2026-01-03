#!/bin/bash

echo "🚀 Setting up Local Online Judge..."

# 1. Check Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 could not be found. Please install Python 3.8+."
    exit 1
fi

# 2. Check C++ (g++)
if ! command -v g++ &> /dev/null
then
    echo "⚠️  g++ (C++ compiler) not found."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🍎 Detected macOS. Checking for xcode-select..."
        if ! xcode-select -p &> /dev/null; then
            echo "   Requesting install of Command Line Tools..."
            xcode-select --install
            echo "ℹ️  Please simply click 'Install' in the pop-up window and run this script again once finished."
            exit 1
        else
            echo "   Xcode tools seem to be installed, but g++ is missing from PATH."
            echo "   Try: 'brew install gcc' if you use Homebrew."
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            echo "🐧 Detected Debian/Ubuntu. Installing build-essential..."
            sudo apt-get update && sudo apt-get install -y build-essential
        else
            echo "❌ Linux detected but package manager not supported by this script."
            echo "Please install g++ manually."
            exit 1
        fi
    else
        echo "❌ OS not supported for auto-install. Please install g++ manually."
        exit 1
    fi
else
    echo "✅ g++ is installed."
fi

echo "📦 Creating virtual environment..."
cd server
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created."
else
    echo "ℹ️  Virtual environment already exists."
fi

echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "✅ Setup complete! Run './run.sh' to start the server."
