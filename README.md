# Local Online Judge

A lightweight, local competitive programming judge and problem manager.

## Features
- **Problem Management**: Create, edit, and categorize problems.
- **Local Judge**: Submit code (C++, Python, Java) and get immediate feedback.
- **Test Case Generation**: Auto-generate test cases using custom scripts.
- **Rich UI**: Modern interface for viewing problems and writing code.
- **Contribution Technique**: Includes a set of Tree Contribution problems.

## 🚀 Quick Start

### General Prerequisites
- **Python 3.8+** (Must be in your system PATH).
- **C++ Compiler**:
    - **macOS**: `clang` / `g++` (Install via `xcode-select --install`).
    - **Linux**: `g++` (Install via `sudo apt install build-essential`).
    - **Windows**: `g++` (Install MinGW or similar and add to PATH).

---

### 🍎 macOS / 🐧 Linux

1.  **Setup**:
    Open a terminal in the project root and run:
    ```bash
    ./setup.sh
    ```
    *This creates the virtual environment and installs dependencies.*

2.  **Run**:
    Start the server:
    ```bash
    ./run.sh
    ```
    Open [http://localhost:5002](http://localhost:5002) in your browser.

---

### 🪟 Windows

1.  **Setup**:
    Double-click `setup.bat` or run in Command Prompt:
    ```cmd
    setup.bat
    ```
    *This checks for Python/g++, creates a virtual environment, and installs dependencies.*

2.  **Run**:
    Double-click `run.bat` or run in Command Prompt:
    ```cmd
    run.bat
    ```
    Open [http://localhost:5002](http://localhost:5002) in your browser.

---

## 📁 Directory Structure
- `server/`: Backend Flask app and problem data.
    - `problems/`: Stores problem statements, generators, and test cases.
- `client/`: Frontend assets (served by Flask).
- `temp/`: Temporary execution directory.

## 🛠️ Advanced Usage
- **Add New Problem**: Use the UI or create folders in `server/problems`.
- **Generate Tests**: Use the "Generate Tests" API or the UI (if implemented).
- **Edge Cases**: The current problem set includes generators with support for edge cases (Line, Star, Small N).

## 🤝 Contributing
Feel free to add more problems by creating new directories in `server/problems` following the existing structure.