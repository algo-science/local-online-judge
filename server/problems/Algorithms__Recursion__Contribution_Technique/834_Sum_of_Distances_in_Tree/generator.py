import random
import sys

def generate_tree_structure(n, type="random"):
    edges = []
    if n == 1:
        return []
        
    if type == "line":
        # 0-1-2-3...
        perm = list(range(n))
        random.shuffle(perm)
        for i in range(n - 1):
            edges.append([perm[i], perm[i+1]])
    
    elif type == "star":
        # 0 is center, connected to all others
        perm = list(range(n))
        random.shuffle(perm)
        center = perm[0]
        for i in range(1, n):
            edges.append([center, perm[i]])
            
    else: # random
        for i in range(1, n):
            parent = random.randint(0, i - 1)
            edges.append([parent, i])
        
        perm = list(range(n))
        random.shuffle(perm)
        remapped_edges = [[perm[u], perm[v]] for u, v in edges]
        edges = remapped_edges
        
    return edges

if __name__ == "__main__":
    r = random.random()
    if r < 0.1:
        n = 1
        edges = []
    elif r < 0.2:
        n = 2
        edges = generate_tree_structure(n, "random")
    elif r < 0.35:
        n = random.randint(5, 50)
        edges = generate_tree_structure(n, "line")
    elif r < 0.5:
        n = random.randint(5, 50)
        edges = generate_tree_structure(n, "star")
    else:
        n = random.randint(5, 50)
        edges = generate_tree_structure(n, "random")
        
    print(n)
    for u, v in edges:
        print(f"{u} {v}")
