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
        
    # Seats: Edge cases 1, large
    rs = random.random()
    if rs < 0.2: seats = 1
    elif rs < 0.4: seats = n # Everyone can fit in one car potentially (if at same node)
    else: seats = random.randint(1, 10)
    print(seats)

if __name__ == "__main__":
    generate()
