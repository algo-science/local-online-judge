# Depth First Search

## Description

You are given a graph with `V` vertices and `E` edges. You have to implement the Depth First Search (DFS) algorithm and print the DFS traversal of the graph starting from vertex 0.

## Input Format

- The first line contains two integers, `V` and `E`, representing the number of vertices and edges, respectively.
- The next `E` lines each contain two integers, `u` and `v`, representing an edge between vertex `u` and vertex `v`.

## Output Format

- Print the DFS traversal of the graph, starting from vertex 0, as a single line of space-separated integers.

## Constraints

- 1 &le; `V` &le; 100
- 0 &le; `E` &le; `V` * (`V` - 1) / 2
- 0 &le; `u`, `v` < `V`

---

## Editorial

The Depth First Search (DFS) algorithm is a graph traversal technique that explores as far as possible along each branch before backtracking. It's often implemented using recursion or a stack.

Here's a high-level overview of the algorithm:
1.  Start at a given vertex (in this case, vertex 0).
2.  Mark the current vertex as visited.
3.  For each unvisited neighbor of the current vertex, recursively call the DFS function.

To implement this, you'll need an adjacency list to represent the graph and a boolean array to keep track of visited vertices. The adjacency list is an array of lists, where `adj[i]` contains a list of all vertices adjacent to vertex `i`. The `visited` array will store whether a vertex has been visited.