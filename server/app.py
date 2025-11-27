from flask import Flask, request, jsonify, render_template
from core.executor import execute_code
from core.file_handler import get_problems_from_fs, get_problem_from_fs, get_submissions_from_fs, save_submission_to_fs, get_quizzes_from_fs, read_sessions, write_sessions, read_tags, write_tags, read_favorites, write_favorites, read_ratings, write_ratings
from core.ai_review import get_ai_review
from utils.importer import import_problems
from core import calendar_handler
from flask import Flask, request, jsonify, render_template
import time
import os
import json

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def index():
    """Renders the main application page."""
    return render_template('index.html')

@app.route('/api/problems', methods=['GET'])
def get_problems():
    """Retrieves a list of all problems, grouped by category."""
    return jsonify(get_problems_from_fs())

@app.route('/api/problems/<problem_id>', methods=['GET'])
def get_problem(problem_id):
    """
    Retrieves a single problem by its ID.
    Args:
        problem_id: The ID of the problem to retrieve.
    Returns:
        A JSON object containing the problem details, or a 404 error if not found.
    """
    problem = get_problem_from_fs(problem_id)
    if problem is None:
        return jsonify({"error": "Problem not found"}), 404
    return jsonify(problem)

@app.route('/api/submit', methods=['POST'])
def submit_code():
    """
    Receives code submitted by a user, executes it against test cases,
    and returns the results.
    """
    data = request.get_json()
    problem_id = data.get('problem_id')
    language = data.get('language')
    code = data.get('code')

    problem = get_problem_from_fs(problem_id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    # This is a simplified way to get test cases. In a real scenario, this might be stored more securely.
    group_folder, problem_folder = problem_id.split('-', 1)
    problem_path = os.path.join(os.path.dirname(__file__), 'problems', group_folder, problem_folder)
    with open(os.path.join(problem_path, 'input.txt'), 'r') as f:
        input_text = f.read()
    with open(os.path.join(problem_path, 'output.txt'), 'r') as f:
        output_text = f.read()
    
    import re
    inputs = [i.strip() for i in re.split(r'---\s*', input_text.strip()) if i.strip()]
    outputs = [o.strip() for o in re.split(r'---\s*', output_text.strip()) if o.strip()]
    test_cases = [{"input": i, "output": o} for i, o in zip(inputs, outputs)]


    final_status = "Accepted"
    final_output = ""
    passed_count = 0
    total_count = len(test_cases)
    details = []

    for i, case in enumerate(test_cases):
        input_data = case['input']
        expected_output = case['output'].strip()
        
        result = execute_code(language, code, input_data)
        
        case_result = {
            "id": i + 1, "status": "Passed", "input": input_data,
            "expected": expected_output, "actual": "", "error": ""
        }

        if result['status'] != "Success":
            final_status = result['status']
            final_output = result['output']
            case_result["status"] = result["status"]
            case_result["error"] = result["output"]
            details.append(case_result)
            break
        
        actual_output = result['output'].strip()
        case_result["actual"] = actual_output
        
        if actual_output != expected_output:
            if final_status == "Accepted":
                final_status = "Wrong Answer"
                final_output = f"Test Case {i+1} Failed"
            
            case_result["status"] = "Wrong Answer"
        else:
            passed_count += 1
        details.append(case_result)

    submission_id = int(time.time() * 1000)
    submission_data = {
        "id": submission_id, "problem_id": problem_id, "language": language,
        "code": code, "status": final_status, "output": final_output,
        "passed_count": passed_count, "total_count": total_count,
        "details": details, "timestamp": submission_id
    }
    
    save_submission_to_fs(submission_data)
    return jsonify(submission_data)

@app.route('/api/submissions/<problem_id>', methods=['GET'])
def get_submissions(problem_id):
    """
    Retrieves all submissions for a specific problem.
    Args:
        problem_id: The ID of the problem.
    Returns:
        A JSON array of submission objects.
    """
    return jsonify(get_submissions_from_fs(problem_id))

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    """Retrieves a list of all available quizzes."""
    return jsonify(get_quizzes_from_fs())

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Retrieves all problem sessions."""
    return jsonify(read_sessions())

@app.route('/api/sessions', methods=['POST'])
def add_session():
    """Creates a new, empty session."""
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "Session name is required"}), 400
    
    sessions = read_sessions()
    if any(s['name'] == name for s in sessions):
        return jsonify({"error": "Session already exists"}), 400
    
    sessions.append({"name": name, "problems": []})
    write_sessions(sessions)
    return jsonify({"success": True}), 201

@app.route('/api/sessions/assign', methods=['POST'])
def assign_to_session():
    """Assigns a problem to a specific session."""
    data = request.get_json()
    session_name = data.get('session_name')
    problem_id = data.get('problem_id')

    if not session_name or not problem_id:
        return jsonify({"error": "Session name and problem ID are required"}), 400

    sessions = read_sessions()
    session_found = False
    for session in sessions:
        if session['name'] == session_name:
            if problem_id not in session['problems']:
                session['problems'].append(problem_id)
            session_found = True
            break
    
    if not session_found:
        return jsonify({"error": "Session not found"}), 404
        
    write_sessions(sessions)
    return jsonify({"success": True})

@app.route('/api/sessions/rename', methods=['POST'])
def rename_session():
    """Renames an existing session."""
    data = request.get_json()
    old_name = data.get('old_name')
    new_name = data.get('new_name')

    if not old_name or not new_name:
        return jsonify({"error": "Old and new session names are required"}), 400

    sessions = read_sessions()
    session_found = False
    if any(s['name'] == new_name for s in sessions):
        return jsonify({"error": "Session name already exists"}), 400

    for session in sessions:
        if session['name'] == old_name:
            session['name'] = new_name
            session_found = True
            break
    
    if not session_found:
        return jsonify({"error": "Session not found"}), 404
        
    write_sessions(sessions)
    return jsonify({"success": True})

@app.route('/api/import', methods=['POST'])
def import_all_problems():
    """Scans the filesystem for new problems and imports them."""
    result = import_problems()
    return jsonify(result)

@app.route('/api/submissions/<problem_id>/<submission_id>/editorial', methods=['POST'])
def toggle_editorial(problem_id, submission_id):
    """
    Marks or unmarks a submission as an editorial.
    Args:
        problem_id: The ID of the problem.
        submission_id: The ID of the submission.
    """
    sub_prob_dir = os.path.join(os.path.dirname(__file__), 'submissions', str(problem_id))
    submission_file = os.path.join(sub_prob_dir, f"{submission_id}.json")

    if not os.path.exists(submission_file):
        return jsonify({"error": "Submission not found"}), 404

    with open(submission_file, 'r+') as f:
        submission = json.load(f)
        submission['is_editorial'] = not submission.get('is_editorial', False)
        f.seek(0)
        json.dump(submission, f, indent=4)
        f.truncate()

    return jsonify({"success": True})

@app.route('/api/problems/<problem_id>/tags', methods=['POST'])
def update_tags(problem_id):
    """
    Updates the tags for a specific problem.
    Args:
        problem_id: The ID of the problem.
    """
    data = request.get_json()
    tags = data.get('tags', [])
    
    all_tags = read_tags()
    all_tags[problem_id] = tags
    write_tags(all_tags)
    
    return jsonify({"success": True, "tags": tags})

@app.route('/api/tags', methods=['GET'])
def get_all_tags():
    """Retrieves a list of all unique tags used across all problems."""
    tags_map = read_tags()
    unique_tags = set()
    for tags in tags_map.values():
        unique_tags.update(tags)
    return jsonify(sorted(list(unique_tags)))

@app.route('/api/problems/<problem_id>/favorite', methods=['POST'])
def toggle_favorite(problem_id):
    """
    Toggles the favorite status of a problem.
    Args:
        problem_id: The ID of the problem.
    """
    favorites = read_favorites()
    if problem_id in favorites:
        favorites.remove(problem_id)
    else:
        favorites.append(problem_id)
    write_favorites(favorites)
    return jsonify({"success": True, "is_favorite": problem_id in favorites})

@app.route('/api/problems/<problem_id>/rating', methods=['POST'])
def update_rating(problem_id):
    """
    Updates the rating for a specific problem.
    Args:
        problem_id: The ID of the problem.
    """
    data = request.get_json()
    rating = data.get('rating')
    
    if rating is None:
        return jsonify({"error": "Rating is required"}), 400
        
    ratings = read_ratings()
    ratings[problem_id] = int(rating)
    write_ratings(ratings)
    
    return jsonify({"success": True, "rating": rating})

@app.route('/api/review', methods=['POST'])
def review_code():
    """
    Sends code to an AI for a review and returns the feedback.
    """
    data = request.get_json()
    code = data.get('code')
    problem_id = data.get('problem_id')

    if not code or not problem_id:
        return jsonify({"error": "Code and problem ID are required"}), 400

    problem = get_problem_from_fs(problem_id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    # Simplified problem context for the AI
    problem_context = f"Title: {problem['title']}\n\nDescription:\n{problem['description']}"

    review_result = get_ai_review(code, problem_context)
    return jsonify(review_result)

# Calendar routes
@app.route('/api/calendar/<date_str>', methods=['GET'])
def get_calendar_tasks(date_str):
    """
    Retrieves all tasks for a specific date from the calendar.
    Args:
        date_str: The date in YYYY-MM-DD format.
    """
    tasks = calendar_handler.get_tasks_for_date(date_str)
    return jsonify(tasks)

@app.route('/api/calendar/<date_str>', methods=['POST'])
def add_calendar_task(date_str):
    """
    Adds a new task to the calendar for a specific date.
    Args:
        date_str: The date in YYYY-MM-DD format.
    """
    data = request.get_json()
    description = data.get('description')
    if not description:
        return jsonify({"error": "Task description is required"}), 400
    task = calendar_handler.add_task(date_str, description)
    return jsonify(task), 201

@app.route('/api/calendar/<date_str>/<int:task_id>', methods=['PUT'])
def update_calendar_task(date_str, task_id):
    """
    Updates the status of a calendar task.
    Args:
        date_str: The date of the task.
        task_id: The ID of the task to update.
    """
    data = request.get_json()
    completed = data.get('completed')
    if completed is None:
        return jsonify({"error": "Completed status is required"}), 400
    task = calendar_handler.update_task_status(date_str, task_id, bool(completed))
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/calendar/<date_str>/<int:task_id>', methods=['DELETE'])
def delete_calendar_task(date_str, task_id):
    """
    Deletes a task from the calendar.
    Args:
        date_str: The date of the task.
        task_id: The ID of the task to delete.
    """
    if calendar_handler.delete_task(date_str, task_id):
        return jsonify({"success": True})
    return jsonify({"error": "Task not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5002)