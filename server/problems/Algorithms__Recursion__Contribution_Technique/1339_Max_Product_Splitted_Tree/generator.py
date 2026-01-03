import random

def generate():
    # 1339 requires splitting an edge, so N >= 2
    r = random.random()
    if r < 0.1: n = 2 # Minimal case
    elif r < 0.2: n = 3
    elif r < 0.35: n = random.randint(5, 20) # Line-like logic handled below
    else: n = random.randint(5, 50)
    
    print(n)
    
    edges = []
    # Force line or star sometimes
    struct_type = "random"
    if n > 3:
        rr = random.random()
        if rr < 0.2: struct_type = "line"
        elif rr < 0.4: struct_type = "star"

    if struct_type == "line":
        perm = list(range(n))
        random.shuffle(perm)
        for i in range(n - 1):
             edges.append([perm[i], perm[i+1]])
    elif struct_type == "star":
        perm = list(range(n))
        random.shuffle(perm)
        center = perm[0]
        for i in range(1, n):
             edges.append([center, perm[i]])
    else:
        # Pseudo-binary tree construction (ensure max degree <= 3, specifically max children 2)
        # It's tricky to enforce strictly binary with random edges but let's try strict parent method
        children = [[] for _ in range(n)]
        available_parents = [0]
        node_count = 1
        
        # This creates edges 0-(1), 0-(2), 1-(3)...
        # Since 1339 says "Binary Tree", nodes have max 2 children (degree <= 3)
        # Standard "parent to i"
        edge_pairs = []
        for i in range(1, n):
            p = random.choice(available_parents)
            edge_pairs.append([p, i])
            children[p].append(i)
            if len(children[p]) == 2:
                available_parents.remove(p)
            available_parents.append(i)
            
        # Shuffle labels
        perm = list(range(n))
        random.shuffle(perm)
        edges = [[perm[u], perm[v]] for u, v in edge_pairs]

    for u, v in edges:
        print(f"{u} {v}")

    # Values
    # Edge case: all 0 (if allowed?), large values
    values = [random.randint(1, 1000) for _ in range(n)]
    print(*(values))

if __name__ == "__main__":
    generate()
