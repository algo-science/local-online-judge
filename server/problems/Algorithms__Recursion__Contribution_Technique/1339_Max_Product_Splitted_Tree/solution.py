import sys
sys.setrecursionlimit(20000)
MOD = 10**9 + 7

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
            
        values = list(map(int, sys.stdin.readline().split()))
    except ValueError:
        return

    total_sum = sum(values)
    subtree_sums = []
    
    def dfs(u, p):
        s = values[u]
        for v in adj[u]:
            if v == p: continue
            s += dfs(v, u)
        subtree_sums.append(s)
        return s

    dfs(0, -1)
    
    max_prod = 0
    for s in subtree_sums:
        other = total_sum - s
        max_prod = max(max_prod, s * other)
        
    print(max_prod % MOD)

if __name__ == "__main__":
    solve()
