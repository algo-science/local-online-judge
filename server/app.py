from flask import Flask, request, jsonify, render_template
from core.executor import execute_code
from core.file_handler import get_problems_from_fs, get_problem_from_fs, get_submissions_from_fs, save_submission_to_fs, get_quizzes_from_fs, read_sessions, write_sessions, read_tags, write_tags, read_favorites, write_favorites
from utils.importer import import_problems
from flask import Flask, request, jsonify, render_template
import time
import os
import json

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/problems', methods=['GET'])
def get_problems():
    return jsonify(get_problems_from_fs())

@app.route('/api/problems/<problem_id>', methods=['GET'])
def get_problem(problem_id):
    problem = get_problem_from_fs(problem_id)
    if problem is None:
        return jsonify({"error": "Problem not found"}), 404
    return jsonify(problem)

@app.route('/api/submit', methods=['POST'])
def submit_code():
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
    return jsonify(get_submissions_from_fs(problem_id))

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    return jsonify(get_quizzes_from_fs())

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    return jsonify(read_sessions())

@app.route('/api/sessions', methods=['POST'])
def add_session():
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
    result = import_problems()
    return jsonify(result)

@app.route('/api/submissions/<problem_id>/<submission_id>/editorial', methods=['POST'])
def toggle_editorial(problem_id, submission_id):
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
    data = request.get_json()
    tags = data.get('tags', [])
    
    all_tags = read_tags()
    all_tags[problem_id] = tags
    write_tags(all_tags)
    
    return jsonify({"success": True, "tags": tags})

@app.route('/api/tags', methods=['GET'])
def get_all_tags():
    tags_map = read_tags()
    unique_tags = set()
    for tags in tags_map.values():
        unique_tags.update(tags)
    return jsonify(sorted(list(unique_tags)))

@app.route('/api/problems/<problem_id>/favorite', methods=['POST'])
def toggle_favorite(problem_id):
    favorites = read_favorites()
    if problem_id in favorites:
        favorites.remove(problem_id)
    else:
        favorites.append(problem_id)
    write_favorites(favorites)
    return jsonify({"success": True, "is_favorite": problem_id in favorites})


if __name__ == '__main__':
    app.run(debug=True, port=5002)