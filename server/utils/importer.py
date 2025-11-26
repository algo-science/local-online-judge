import os
import json
import re
import time
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")
SOURCE_DIR = os.path.join(BASE_DIR, "source_problems") # New directory for problem sources

def import_problems():
    """
    Imports problems from the SOURCE_DIR.
    Each problem should have its own directory with the following structure:
    - statement.md
    - input.txt
    - output.txt
    - editorial.md (optional)
    - user_editorials/ (optional)
        - user1.md
        - user1.cpp
        - user2.md
        - user2.py
    - solutions/ (optional)
        - solution.py
        - solution.cpp
    """
    if not os.path.exists(SOURCE_DIR):
        return {"status": "error", "message": "Source directory not found."}

    for problem_name in os.listdir(SOURCE_DIR):
        source_problem_path = os.path.join(SOURCE_DIR, problem_name)
        if not os.path.isdir(source_problem_path):
            continue

        # Create problem directory
        target_problem_path = os.path.join(PROBLEMS_DIR, "Imported", problem_name)
        os.makedirs(target_problem_path, exist_ok=True)

        # Copy essential files
        for filename in ["statement.md", "input.txt", "output.txt", "editorial.md"]:
            src_file = os.path.join(source_problem_path, filename)
            if os.path.exists(src_file):
                shutil.copy(src_file, target_problem_path)
        
        # TODO: Handle user editorials and solutions.
        # This will require a more complex parsing and storage mechanism.
        # For now, we are just copying the core files.

    return {"status": "success", "message": f"Imported problems from {SOURCE_DIR}."}
