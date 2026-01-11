import os
import json
import re
import shutil
import zipfile
import time
from datetime import datetime

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
                    
                    problem_type = "coding" # Default
                    difficulty = "Medium"
                    
                    # Try to read metadata from info.json
                    info_path = os.path.join(problem_path, 'info.json')
                    if os.path.exists(info_path):
                        try:
                            with open(info_path, 'r') as f:
                                info = json.load(f)
                                problem_type = info.get('type', problem_type)
                                difficulty = info.get('difficulty', difficulty)
                        except:
                            pass

                    all_problems.append({
                        "id": problem_id,
                        "title": title,
                        "status": status,
                        "type": problem_type,
                        "difficulty": difficulty,
                        "tags": tags_map.get(problem_id, []),
                        "is_favorite": problem_id in favorites,
                        "rating": ratings.get(problem_id, 0)
                    })

    grouped_problems = {}
    # Group by filesystem folder (Group Name)
    for problem in all_problems:
        group_name = problem['id'].split('-', 1)[0]
        if group_name not in grouped_problems:
            grouped_problems[group_name] = []
        grouped_problems[group_name].append(problem)
    
    # We can still include specific sessions if needed, but for now 
    # the main view should be the directory structure.
    # If we want to support sessions mixed in, we would add them here.

    
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

        # Check for info.json (New Format)
        info_path = os.path.join(problem_path, 'info.json')
        if os.path.exists(info_path):
            try:
                with open(info_path, 'r') as f:
                    problem_data = json.load(f)
                
                # Check for separate statement.md
                statement_file = os.path.join(problem_path, 'statement.md')
                if os.path.exists(statement_file):
                    with open(statement_file, 'r') as f:
                         problem_data['description'] = f.read()
                
                problem_data['id'] = problem_id
                problem_data["is_favorite"] = problem_id in read_favorites()
                problem_data["rating"] = read_ratings().get(problem_id, 0)
                
                # Ensure samples are present for frontend
                if 'sample_input' not in problem_data and 'test_cases' in problem_data and problem_data['test_cases']:
                     problem_data['sample_input'] = problem_data['test_cases'][0].get('input', '')
                     problem_data['sample_output'] = problem_data['test_cases'][0].get('output', '')

                return problem_data
            except Exception as e:
                print(f"Error reading info.json for {problem_id}: {e}")
                # Fallthrough or return None? Let's fallthrough to legacy in case it's mixed, or just return None.
                pass

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

def create_problem_on_fs(data):
    """
    Creates a new problem structure on the filesystem.
    data format:
    {
        "title": "Problem Title",
        "category": "Algorithm/Graph", # "/" denotes subfolders
        "description": "Markdown content...",
        "input": "Sample Input",
        "output": "Sample Output"
    }
    """
    try:
        title = data.get('title')
        category = data.get('category', 'Uncategorized')
        description = data.get('description', '')
        sample_input = data.get('input', '')
        sample_output = data.get('output', '')

        # Sanitize folder names
        safe_title = re.sub(r'[^\w\-]', '_', title)
        # Handle complex category "Group/SubGroup" -> "Group__SubGroup"
        # The frontend/user might pass "Group/SubGroup" or "Group__SubGroup"
        # We want to map it to a folder structure. 
        # But wait, our current structure is "Group__SubGroup" as a single folder name OR nested folders?
        # Looking at existing: "Algorithms__Recursion__Contribution_Technique" is ONE folder name.
        # So we should probably keep that convention for simplicity: replace "/" with "__"
        safe_category = category.replace('/', '__').replace(' ', '_')
        
        # Create directory
        problem_dir = os.path.join(PROBLEMS_DIR, safe_category, safe_title)
        os.makedirs(problem_dir, exist_ok=True)

        # Write statement.md
        with open(os.path.join(problem_dir, 'statement.md'), 'w') as f:
            f.write(description)
        
        # Write input.txt / output.txt
        with open(os.path.join(problem_dir, 'input.txt'), 'w') as f:
            f.write(sample_input)
        
        with open(os.path.join(problem_dir, 'output.txt'), 'w') as f:
            f.write(sample_output)
            
        # Write template solution.py and generator.py
        with open(os.path.join(problem_dir, 'solution.py'), 'w') as f:
            f.write("# Write your solution here\n")
            
        with open(os.path.join(problem_dir, 'generator.py'), 'w') as f:
            f.write("# Write your test case generator here\nimport random\nprint(random.randint(1, 10))\n")

        return {"success": True, "id": f"{safe_category}-{safe_title}"}

    except Exception as e:
        return {"success": False, "error": str(e)}

def export_group_as_zip(group_name):
    """
    Zips a problem group folder and returns the path to the zip file.
    """
    group_path = os.path.join(PROBLEMS_DIR, group_name)
    if not os.path.exists(group_path):
        return None
    
    # Create temp zip file
    temp_zip = os.path.join("temp", f"{group_name}.zip")
    with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(group_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Archive name should be relative to group_path
                arcname = os.path.relpath(file_path, os.path.dirname(group_path))
                zipf.write(file_path, arcname)
    
    return temp_zip

def import_bulk_zip(zip_path):
    """
    Extracts a zip file and imports problems.
    Problems are placed in 'Imported_{Timestamp}' folder.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        import_folder_name = f"Imported_{timestamp}"
        target_dir = os.path.join(PROBLEMS_DIR, import_folder_name)
        os.makedirs(target_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
            
        # Optional: Flatten if the zip contained a single top-level folder
        # But for now, let's assume the zip structure mirrors the group structure
        return {"success": True, "group": import_folder_name}
    except Exception as e:
        return {"success": False, "error": str(e)}