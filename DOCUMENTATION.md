# Application Documentation

## High-Level Architecture

The application is a single-page web application (SPA) with a Python Flask backend and a vanilla JavaScript frontend.

-   **Backend:** The Flask server handles all business logic, including problem management, code execution, and data storage.
-   **Frontend:** The frontend is responsible for rendering the user interface and interacting with the backend through API calls.
-   **Data Storage:** All data, including problems, submissions, and user information, is stored on the filesystem in JSON format.

## Project Structure

-   **`server/`**: Contains the Flask backend.
    -   **`app.py`**: The main application file.
    -   **`core/`**: Core application logic.
    -   **`problems/`**: Contains problem statements and test cases.
    -   **`static/`**: Static assets for the frontend.
    -   **`templates/`**: HTML templates for the frontend.
-   **`client/`**: Contains the frontend source code (if applicable).
-   **`docker-compose.yml`**: Defines the Docker services.
-   **`Dockerfile`**: Defines the Docker image for the application.

## Running with Docker

To run the application with Docker, use the following command:

```bash
docker compose up -d --build
```

The application will be available at `http://localhost:5002`.

## API Endpoint Documentation

All API endpoints are prefixed with `/api`.

### Problems

-   **`GET /api/problems`**: Retrieves a list of all problems, grouped by category.
-   **`GET /api/problems/<problem_id>`**: Retrieves a single problem by its ID.
-   **`POST /api/problems/<problem_id>/tags`**: Updates the tags for a specific problem.
-   **`POST /api/problems/<problem_id>/favorite`**: Toggles the favorite status of a problem.
-   **`POST /api/problems/<problem_id>/rating`**: Updates the rating for a specific problem.

### Submissions

-   **`POST /api/submit`**: Submits code for a problem. The server executes the code against test cases and returns the results.
-   **`GET /api/submissions/<problem_id>`**: Retrieves all submissions for a specific problem.
-   **`POST /api/submissions/<problem_id>/<submission_id>/editorial`**: Toggles the editorial status of a submission.

### AI Review

-   **`POST /api/review`**: Sends code to the AI for a review and returns the feedback.

### Sessions

-   **`GET /api/sessions`**: Retrieves all problem sessions.
-   **`POST /api/sessions`**: Creates a new, empty session.
-   **`POST /api/sessions/assign`**: Assigns a problem to a specific session.
-   **`POST /api/sessions/rename`**: Renames an existing session.

### Tags

-   **`GET /api/tags`**: Retrieves a list of all unique tags used across all problems.

### Quizzes

-   **`GET /api/quizzes`**: Retrieves a list of all available quizzes.

### Calendar

-   **`GET /api/calendar/<date_str>`**: Retrieves all tasks for a specific date from the calendar.
-   **`POST /api/calendar/<date_str>`**: Adds a new task to the calendar for a specific date.
-   **`PUT /api/calendar/<date_str>/<int:task_id>`**: Updates the status of a calendar task.
-   **`DELETE /api/calendar/<date_str>/<int:task_id>`**: Deletes a task from the calendar.

### Import

-   **`POST /api/import`**: Scans the filesystem for new problems and imports them.