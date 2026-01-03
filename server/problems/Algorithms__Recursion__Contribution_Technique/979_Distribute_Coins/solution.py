import sys
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
        
        coins = list(map(int, sys.stdin.readline().split()))
    except ValueError:
        return

    ans = 0
    
    # helper returns (num_nodes, num_coins) in subtree
    def dfs(u, p):
        nonlocal ans
        
        c = coins[u]
        cnt = 1
        
        for v in adj[u]:
            if v == p: continue
            
            sub_cnt, sub_c = dfs(v, u)
            
            # CONTRIBUTION STEP:
            # Imbalance = excess coins or missing coins
            # Imbalance must flow through edge u-v
            ans += abs(sub_c - sub_cnt)
            
            c += sub_c
            cnt += sub_cnt
            
        return cnt, c

    dfs(0, -1)
    print(ans)

if __name__ == "__main__":
    solve()
