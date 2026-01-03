import sys
import math
sys.setrecursionlimit(20000)

def solve():
    try:
        line = sys.stdin.readline()
        if not line: return
        n = int(line.strip())
        
        adj = [[] for _ in range(n)]
        # Read n-1 edges
        for _ in range(n - 1):
            line = sys.stdin.readline()
            if not line: break
            u, v = map(int, line.split())
            adj[u].append(v)
            adj[v].append(u)
            
        seats = int(sys.stdin.readline().strip())
    except ValueError:
        return

    ans = 0
    
    def dfs(u, p):
        nonlocal ans
        size = 1
        for v in adj[u]:
            if v == p: continue
            child_size = dfs(v, u)
            
            # CONTRIBUTION STEP:
            # Traffic on edge v->u is exactly 'child_size' people.
            # Cars needed = ceil(child_size / seats)
            cars_needed = math.ceil(child_size / seats)
            ans += cars_needed
            
            size += child_size
        return size

    dfs(0, -1)
    print(ans)

if __name__ == "__main__":
    solve()
