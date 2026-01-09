import sys
import json
from typing import List
import math

# Driver Code to handle I/O and invoke the user's Solution class

if __name__ == "__main__":
    try:
        # Read all stdin
        input_data = sys.stdin.read().strip().split('\n')
        if not input_data:
            sys.exit(0)
            
        # Parse Input based on problem spec:
        # Line 1: n
        # Next n-1 lines: u v
        # Last line: seats
        
        iterator = iter(input_data)
        try:
            line = next(iterator).strip()
            if not line: sys.exit(0)
            n = int(line)
            
            roads = []
            for _ in range(n - 1):
                edge_line = next(iterator).strip()
                u, v = map(int, edge_line.split())
                roads.append([u, v])
                
            seats = int(next(iterator).strip())
            
        except StopIteration:
            sys.exit(0)

        # Invoke User Solution
        sol = Solution()
        result = sol.minimumFuelCost(roads, seats)
        print(result)
        
    except Exception as e:
        print(f"Driver Error: {e}")
