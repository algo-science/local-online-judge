import sys
from collections import defaultdict
sys.setrecursionlimit(20000)

def solve():
    try:
        line = sys.stdin.readline()
        if not line: return
        n = int(line.strip())
        
        adj = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, sys.stdin.readline().split())
            adj[u].append(v)
            adj[v].append(u)
            
        colors = list(map(int, sys.stdin.readline().split()))
    except ValueError:
        return

    # Count total nodes for each color
    total_count = defaultdict(int)
    for c in colors:
        total_count[c] += 1
        
    ans = 0
    
    # DFS returns a dict {color: count_in_subtree}
    def dfs(u, p):
        nonlocal ans
        # Initial map: Just self
        my_counts = defaultdict(int)
        my_counts[colors[u]] = 1
        
        for v in adj[u]:
            if v == p: continue
            
            child_counts = dfs(v, u)
            
            # CONTRIBUTION STEP:
            # For each color present in the child subtree,
            # calculate traffic over edge u-v for that color group.
            for col, count_in in child_counts.items():
                count_out = total_count[col] - count_in
                # Traffic = count_in * count_out
                ans += count_in * count_out
                
                # Merge into parent map (Small-to-Large optim not needed for small N, but good practice)
                my_counts[col] += count_in
        
        return my_counts

    dfs(0, -1)
    print(ans)

if __name__ == "__main__":
    solve()
