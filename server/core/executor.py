import subprocess
import os
import uuid

TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def execute_code(language, code, input_data):
    unique_id = str(uuid.uuid4())
    filename = ""
    compile_cmd = None
    run_cmd = None

    if language == "cpp":
        filename = os.path.join(TEMP_DIR, f"{unique_id}.cpp")
        exe_file = os.path.join(TEMP_DIR, unique_id)
        processed_code = code
        if "#include <bits/stdc++.h>" in code:
            headers = """
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <numeric>
// Add other headers as needed
"""
            processed_code = code.replace("#include <bits/stdc++.h>", headers)

        with open(filename, "w") as f:
            f.write(processed_code)
        
        compile_cmd = ["g++", "-std=c++17", filename, "-o", exe_file]
        run_cmd = [exe_file]
    
    elif language == "python":
        filename = os.path.join(TEMP_DIR, f"{unique_id}.py")
        with open(filename, "w") as f:
            f.write(code)
        run_cmd = ["python3", filename]
    
    elif language == "java":
        # Java requires class name to match filename. 
        # We assume public class is Main for simplicity or extract it.
        # For simplicity, let's force the user to name their class Main
        filename = os.path.join(TEMP_DIR, "Main.java") 
        # Note: Concurrency issue if multiple submissions run at once with fixed filename.
        # In a real prod env, we'd sandbox this better.
        # For local single user, this is acceptable but let's try to be better.
        # We can rename the class in the code? No, too complex for regex.
        # Let's just use a unique folder for java.
        java_dir = os.path.join(TEMP_DIR, unique_id)
        os.makedirs(java_dir)
        filename = os.path.join(java_dir, "Main.java")
        
        with open(filename, "w") as f:
            f.write(code)
        
        compile_cmd = ["javac", filename]
        run_cmd = ["java", "-cp", java_dir, "Main"]

    else:
        return {"status": "Error", "output": "Unsupported language"}

    # Compilation
    if compile_cmd:
        try:
            subprocess.run(compile_cmd, check=True, capture_output=True, text=True, timeout=10)
        except subprocess.CalledProcessError as e:
            return {"status": "Compilation Error", "output": e.stderr}
        except Exception as e:
            return {"status": "System Error", "output": str(e)}

    # Execution
    try:
        # If input_data is empty string, we might still want to pass it as stdin? 
        # Yes, subprocess handles empty input fine.
        result = subprocess.run(
            run_cmd, 
            input=input_data, 
            capture_output=True, 
            text=True, 
            timeout=5 # 5 seconds time limit
        )
        
        if result.returncode != 0:
             return {"status": "Runtime Error", "output": result.stderr}
        
        return {"status": "Success", "output": result.stdout}

    except subprocess.TimeoutExpired:
        return {"status": "Time Limit Exceeded", "output": ""}
    except Exception as e:
        return {"status": "Runtime Error", "output": str(e)}
    finally:
        # Cleanup
        files_to_remove = []
        if language == "cpp":
            files_to_remove.extend([filename, exe_file])
        elif language == "python":
            files_to_remove.append(filename)
        
        for f in files_to_remove:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except OSError as e:
                print(f"Error removing file {f}: {e}")

        if language == "java":
            try:
                import shutil
                if os.path.exists(java_dir):
                    shutil.rmtree(java_dir)
            except (ImportError, OSError) as e:
                print(f"Error removing directory {java_dir}: {e}")
