import random

def generate_tree_structure(n, type="random"):
    edges = []
    if n == 1: return []
    
    if type == "line":
        perm = list(range(n))
        random.shuffle(perm)
        for i in range(n - 1):
            edges.append([perm[i], perm[i+1]])
    elif type == "star":
        perm = list(range(n))
        random.shuffle(perm)
        center = perm[0]
        for i in range(1, n):
            edges.append([center, perm[i]])
    else:
        for i in range(1, n):
            parent = random.randint(0, i - 1)
            edges.append([parent, i])
        perm = list(range(n))
        random.shuffle(perm)
        edges = [[perm[u], perm[v]] for u, v in edges]
    return edges

def generate():
    r = random.random()
    if r < 0.1: n = 1
    elif r < 0.2: n = 2
    elif r < 0.35: n = random.randint(5, 20); mode = "line"
    elif r < 0.5: n = random.randint(5, 20); mode = "star"
    else: n = random.randint(5, 50); mode = "random"
    
    edges = generate_tree_structure(n, mode if n > 2 else "random")
    
    print(n)
    for u, v in edges:
        print(f"{u} {v}")
        
    # Colors: Edge case -> 1 color (all same), distinct colors
    rc = random.random()
    if rc < 0.2:
        # All same
        colors = [1] * n
    elif rc < 0.4:
         # All distinct
         colors = list(range(1, n + 1))
    else:
        colors = [random.randint(1, min(n, 5)) for _ in range(n)]
        
    print(*(colors))

if __name__ == "__main__":
    generate()
