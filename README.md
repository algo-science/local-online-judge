# Local Online Judge

A lightweight, local competitive programming judge and problem manager.

## Features
- **Problem Management**: Create, edit, and categorize problems.
- **Local Judge**: Submit code (C++, Python, Java) and get immediate feedback.
- **Test Case Generation**: Auto-generate test cases using custom scripts.
- **Rich UI**: Modern interface for viewing problems and writing code.
- **Contribution Technique**: Includes a set of Tree Contribution problems.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Mac/Linux (Shell environment)

### Installation
1.  **Clone/Download** this repository.
2.  Run the setup script:
    ```bash
    ./setup.sh
    ```

### Running the App
1.  Start the server:
    ```bash
    ./run.sh
    ```
2.  Open your browser to: [http://localhost:5002](http://localhost:5002)

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