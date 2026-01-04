import subprocess
import os

def run_test(input_str, expected_output):
    process = subprocess.Popen(
        ['python3', 'solution.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=input_str)
    
    actual = stdout.strip()
    if actual == expected_output:
        print(f"[PASS] Expected '{expected_output}', got '{actual}'")
        return True
    else:
        print(f"[FAIL] Expected '{expected_output}', got '{actual}'")
        print(f"Stderr: {stderr}")
        return False

# Scenario 1: Impossible
input1 = """2 5
5
aa 10
bb 9
cc 9
dd 8
jj 3
5
mm 11
nn 9
oo 8
jj 7
dd 4
"""

# Scenario 2: Alice
input2 = """2 5
5
Alice 100
Bob 10
Charlie 5
Dave 5
Eve 2
5
Alice 80
Frank 8
George 8
Harry 7
Ivy 5
"""

print("Running manual verification for Aggregating Truncated Election Results...")
pass1 = run_test(input1, "Impossible")
pass2 = run_test(input2, "Alice")

if pass1 and pass2:
    print("ALL TESTS PASSED")
else:
    print("SOME TESTS FAILED")
