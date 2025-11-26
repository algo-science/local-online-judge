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