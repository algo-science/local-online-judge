# Local Online Judge

A lightweight, local online judge system for competitive programming enthusiasts.

## Features

*   **Problem Management:** Browse, solve, and organize programming problems.
*   **Sessions:** Group problems into sessions for practice or contests.
*   **Tagging System:** Categorize problems with tags (e.g., "graph", "dp", "easy").
*   **Search:** Quickly find problems by title or session name.
*   **Favorites:** Mark important problems as favorites for quick access.
*   **Local Execution:** Run and test your code locally against sample cases.
*   **Submissions:** Track your submission history.

## Setup

1.  **Prerequisites:** Ensure you have Python 3 installed.
2.  **Installation:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install flask
    ```
3.  **Running the Server:**
    ```bash
    python3 server/app.py
    ```
    The application will be available at `http://127.0.0.1:5002`.

## Project Structure

*   `server/`: Contains the backend Flask application and problem data.
    *   `app.py`: Main entry point for the server.
    *   `core/`: Core logic for file handling and execution.
    *   `problems/`: Directory storing problem statements and test cases.
    *   `templates/`: HTML templates for the frontend.
    *   `static/`: Static assets (images, CSS, JS).

## License

[MIT License](LICENSE)

## Adding New Problems

There are two ways to add problems to the system:

### 1. Using the Web Interface

1.  Navigate to the **Add Problem** tab in the navigation bar.
2.  Fill in the problem details:
    *   **Title:** The name of the problem.
    *   **Description:** Problem statement (supports Markdown and LaTeX).
    *   **Input/Output Format:** Describe expected IO.
    *   **Sample Cases:** Provide examples.
    *   **Test Cases:** Add IO pairs for judging.
    *   **Editorial:** Explanation of the solution.
3.  Click **Create Problem**.

### 2. Importing Problems (Manual File Creation)

You can bulk import problems by creating the directory structure in the `server/problems/` directory.

**Directory Structure:**
The system expects problems to be organized by **Category** (Session) and then by **Problem Name**.

```
server/problems/
├── Graph_Theory/              # Category / Session Name
│   ├── Breadth_First_Search/  # Problem Name (folders use underscores)
│   │   ├── statement.md       # Problem Statement & Editorial
│   │   ├── input.txt          # Test Case Inputs
│   │   └── output.txt         # Test Case Outputs
│   └── Depth_First_Search/
│       ├── ...
└── Dynamic_Programming/
    └── ...
```

**File Formats:**

*   **`statement.md`**: Contains the problem description in Markdown. You can separate the editorial at the bottom using `---` followed by `## Editorial`.
    ```markdown
    # Problem Title
    
    Detailed problem description here...
    
    **Input:** ...
    **Output:** ...
    
    ---
    ## Editorial
    
    Explanation of the solution...
    ```

*   **`input.txt`**: Contains input for all test cases, separated by `---` on a new line.
    ```text
    1 2
    ---
    10 20
    ---
    -5 5
    ```

*   **`output.txt`**: Contains expected output for all test cases, separated by `---` on a new line. Order must match `input.txt`.
    ```text
    3
    ---
    30
    ---
    0
    ```

**Importing:**
After adding the files, go to the web interface and click **"Import Problems"** in the navigation bar. This will scan the `server/problems/` directory and add any new problems to the system.