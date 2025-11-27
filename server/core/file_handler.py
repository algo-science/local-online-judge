import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")
SUBMISSIONS_DIR = os.path.join(BASE_DIR, "submissions")
QUIZZES_DIR = os.path.join(BASE_DIR, "quizzes")
SESSIONS_FILE = os.path.join(os.path.dirname(__file__), 'sessions.json')
TAGS_FILE = os.path.join(os.path.dirname(__file__), 'tags.json')
FAVORITES_FILE = os.path.join(os.path.dirname(__file__), 'favorites.json')
RATINGS_FILE = os.path.join(os.path.dirname(__file__), 'ratings.json')

os.makedirs(PROBLEMS_DIR, exist_ok=True)
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
os.makedirs(QUIZZES_DIR, exist_ok=True)

def read_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return []
    with open(SESSIONS_FILE, 'r') as f:
        return json.load(f)

def write_sessions(data):
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def read_tags():
    if not os.path.exists(TAGS_FILE):
        return {}
    with open(TAGS_FILE, 'r') as f:
        return json.load(f)

def write_tags(data):
    with open(TAGS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def read_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, 'r') as f:
        return json.load(f)

def write_favorites(data):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def read_ratings():
    if not os.path.exists(RATINGS_FILE):
        return {}
    with open(RATINGS_FILE, 'r') as f:
        return json.load(f)

def write_ratings(data):
    with open(RATINGS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_problems_from_fs():
    sessions = read_sessions()
    tags_map = read_tags()
    favorites = read_favorites()
    ratings = read_ratings()
    all_problems = []
    for group_folder in os.listdir(PROBLEMS_DIR):
        group_path = os.path.join(PROBLEMS_DIR, group_folder)
        if os.path.isdir(group_path):
            for problem_folder in os.listdir(group_path):
                problem_path = os.path.join(group_path, problem_folder)
                if os.path.isdir(problem_path):
                    problem_id = f"{group_folder}-{problem_folder}"
                    title = problem_folder.replace('_', ' ').title()
                    # Check for solved status
                    submission_dir = os.path.join(SUBMISSIONS_DIR, problem_id)
                    status = "Not Solved"
                    if os.path.exists(submission_dir):
                        for submission_file in os.listdir(submission_dir):
                            if submission_file.endswith('.json'):
                                with open(os.path.join(submission_dir, submission_file), 'r') as f:
                                    submission = json.load(f)
                                    if submission.get('status') == 'Accepted':
                                        status = "Solved"
                                        break
                    
                    all_problems.append({
                        "id": problem_id,
                        "title": title,
                        "status": status,
                        "tags": tags_map.get(problem_id, []),
                        "is_favorite": problem_id in favorites,
                        "rating": ratings.get(problem_id, 0)
                    })

    grouped_problems = {}
    for session in sessions:
        session_name = session['name']
        grouped_problems[session_name] = []
        for problem_id in session['problems']:
            problem = next((p for p in all_problems if p['id'] == problem_id), None)
            if problem:
                grouped_problems[session_name].append(problem)
    
    # Add uncategorized problems
    uncategorized_problems = []
    categorized_ids = {pid for s in sessions for pid in s['problems']}
    for problem in all_problems:
        if problem['id'] not in categorized_ids:
            uncategorized_problems.append(problem)
    
    if uncategorized_problems:
        grouped_problems['Uncategorized'] = uncategorized_problems
    
    # Attach documentation content to groups if available
    grouped_problems_with_docs = {}
    for group_name, problems in grouped_problems.items():
        doc_content = ""
        # Assuming directory structure matches group name
        # This might need refinement if group name != folder name
        # For now, we'll search for a folder in PROBLEMS_DIR that matches the group name
        # Note: 'Uncategorized' is virtual and won't have a folder
        group_path = os.path.join(PROBLEMS_DIR, group_name)
        if os.path.isdir(group_path):
            docs_file = os.path.join(group_path, 'docs.md')
            if os.path.exists(docs_file):
                with open(docs_file, 'r') as f:
                    doc_content = f.read()
        
        grouped_problems_with_docs[group_name] = {
            "problems": problems,
            "docs": doc_content
        }
            
    return grouped_problems_with_docs

def get_problem_from_fs(problem_id):
    try:
        group_folder, problem_folder = problem_id.split('-', 1)
        problem_path = os.path.join(PROBLEMS_DIR, group_folder, problem_folder)

        if not os.path.isdir(problem_path):
            return None

        statement_file = os.path.join(problem_path, 'statement.md')
        input_file = os.path.join(problem_path, 'input.txt')
        output_file = os.path.join(problem_path, 'output.txt')

        with open(statement_file, 'r') as f:
            content = f.read()
        
        parts = re.split(r'---\s*## Editorial', content, flags=re.IGNORECASE)
        description = parts[0].strip()
        editorial = parts[1].strip() if len(parts) > 1 else "No editorial provided."

        with open(input_file, 'r') as f:
            input_text = f.read()
        
        with open(output_file, 'r') as f:
            output_text = f.read()
            
        inputs = [i.strip() for i in re.split(r'---\s*', input_text.strip()) if i.strip()]
        outputs = [o.strip() for o in re.split(r'---\s*', output_text.strip()) if o.strip()]

        problem_data = {
            "id": problem_id,
            "title": problem_folder.replace('_', ' ').title(),
            "description": description,
            "editorial": editorial,
            "sample_input": inputs[0] if inputs else "",
            "sample_output": outputs[0] if outputs else "",
            "is_favorite": problem_id in read_favorites(),
            "rating": read_ratings().get(problem_id, 0)
        }
        return problem_data
    except Exception as e:
        print(f"Error reading problem {problem_id}: {e}")
        return None

def get_submissions_from_fs(problem_id):
    sub_prob_dir = os.path.join(SUBMISSIONS_DIR, str(problem_id))
    submissions = []
    
    if os.path.exists(sub_prob_dir):
        for filename in sorted(os.listdir(sub_prob_dir), reverse=True):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(sub_prob_dir, filename), 'r') as f:
                        submissions.append(json.load(f))
                except:
                    pass
    return submissions

def save_submission_to_fs(submission_data):
    problem_id = submission_data['problem_id']
    submission_id = submission_data['id']
    sub_prob_dir = os.path.join(SUBMISSIONS_DIR, str(problem_id))
    os.makedirs(sub_prob_dir, exist_ok=True)
    
    with open(os.path.join(sub_prob_dir, f"{submission_id}.json"), 'w') as f:
        json.dump(submission_data, f, indent=4)

def get_quizzes_from_fs():
    # Placeholder for quiz functionality
    return []

def get_categories_from_fs():
    # This function is now managed directly in app.py for simplicity
    return []