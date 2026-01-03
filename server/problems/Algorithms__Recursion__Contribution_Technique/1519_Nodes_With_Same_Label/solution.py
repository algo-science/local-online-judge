import sys
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
        
        labels_line = sys.stdin.readline().strip()
        # Parse labels, allowing for potential space separated or just continuous string
        if " " in labels_line:
             # Just in case generator prints space separated
             labels = labels_line.replace(" ", "")
        else:
             labels = labels_line
             
    except ValueError:
        return

    ans = [0] * n
    
    def dfs(u, p):
        # Counts for this subtree
        counts = [0] * 26
        
        # Add self
        idx = ord(labels[u]) - ord('a')
        counts[idx] = 1
        
        for v in adj[u]:
            if v == p: continue
            child_counts = dfs(v, u)
            
            # Merge child counts
            for i in range(26):
                counts[i] += child_counts[i]
        
        # Answer for u is the total count of its own label in its subtree
        ans[u] = counts[idx]
        return counts

    dfs(0, -1)
    print(*(ans))

if __name__ == "__main__":
    solve()
