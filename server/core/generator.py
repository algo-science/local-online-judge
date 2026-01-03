import os
import subprocess
import shutil

def generate_test_cases(problem_id, count=10):
    """
    Generates test cases for a given problem using generator.py and solution.py.
    
    Args:
        problem_id: The ID of the problem (e.g., "Group-ProblemName").
        count: The number of test cases to generate (default 10).
    
    Returns:
        dict: Result status {"success": bool, "message": str, "error": str}
    """
    
    # Resolve problem path
    try:
        group_folder, problem_folder = problem_id.split('-', 1)
        problem_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'problems', group_folder, problem_folder)
    except ValueError:
         return {"success": False, "error": "Invalid problem ID format. Expected 'Group-ProblemName'."}

    if not os.path.exists(problem_path):
        return {"success": False, "error": f"Problem directory not found: {problem_path}"}

    generator_script = os.path.join(problem_path, 'generator.py')
    solution_script = os.path.join(problem_path, 'solution.py')

    if not os.path.exists(generator_script):
        return {"success": False, "error": "generator.py not found in problem directory."}
    
    if not os.path.exists(solution_script):
        return {"success": False, "error": "solution.py not found in problem directory."}

    generated_inputs = []
    generated_outputs = []

    try:
        for i in range(count):
            # 1. Run generator.py to specific input
            gen_process = subprocess.run(
                ['python3', generator_script],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            input_data = gen_process.stdout.strip()
            
            # 2. Run solution.py with that input to get expected output
            sol_process = subprocess.run(
                ['python3', solution_script],
                input=input_data,
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            output_data = sol_process.stdout.strip()

            generated_inputs.append(input_data)
            generated_outputs.append(output_data)

    except subprocess.CalledProcessError as e:
        error_msg = f"Script execution failed.\nCommand: {e.cmd}\nStderr: {e.stderr}"
        return {"success": False, "error": error_msg}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Script execution timed out."}
    except Exception as e:
        return {"success": False, "error": str(e)}

    # Write to files
    try:
        input_file_path = os.path.join(problem_path, 'input.txt')
        output_file_path = os.path.join(problem_path, 'output.txt')

        with open(input_file_path, 'w') as f:
            f.write('\n---\n'.join(generated_inputs))
        
        with open(output_file_path, 'w') as f:
            f.write('\n---\n'.join(generated_outputs))
            
    except IOError as e:
        return {"success": False, "error": f"Failed to write file: {e}"}

    return {"success": True, "message": f"Successfully generated {count} test cases."}
