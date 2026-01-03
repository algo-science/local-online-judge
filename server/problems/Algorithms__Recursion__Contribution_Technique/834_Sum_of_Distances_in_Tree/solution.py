import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(20000)

def solve():
    try:
        line1 = sys.stdin.readline()
        if not line1: return
        n = int(line1.strip())
        
        adj = [[] for _ in range(n)]
        # Read N-1 edges
        for _ in range(n - 1):
            line = sys.stdin.readline()
            if not line: break
            u, v = map(int, line.split())
            adj[u].append(v)
            adj[v].append(u)
            
    except ValueError:
        return

    # First DFS: Compute count[] and init sum (dist from root 0)
    count = [1] * n
    ans = [0] * n
    
    def dfs(u, p):
        for v in adj[u]:
            if v == p: continue
            dfs(v, u)
            count[u] += count[v]
            ans[u] += ans[v] + count[v]
            
    dfs(0, -1)
    
    # Second DFS: Re-rooting
    def dfs2(u, p):
        for v in adj[u]:
            if v == p: continue
            # When moving root from u to v:
            # Nodes in v's subtree get 1 step closer (count[v] nodes)
            # Nodes outside v's subtree get 1 step farther (n - count[v] nodes)
            # ans[v] = ans[u] - count[v] + (n - count[v])
            ans[v] = ans[u] - count[v] + (n - count[v])
            dfs2(v, u)
            
    dfs2(0, -1)
    
    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    solve()
