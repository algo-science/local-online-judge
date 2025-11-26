# Breadth First Search

## Description

You are given a graph with `V` vertices and `E` edges. You have to implement the Breadth First Search (BFS) algorithm and print the BFS traversal of the graph starting from vertex 0.

## Input Format

- The first line contains two integers, `V` and `E`, representing the number of vertices and edges, respectively.
- The next `E` lines each contain two integers, `u` and `v`, representing an edge between vertex `u` and vertex `v`.

## Output Format

- Print the BFS traversal of the graph, starting from vertex 0, as a single line of space-separated integers.

## Constraints

- 1 &le; `V` &le; 100
- 0 &le; `E` &le; `V` * (`V` - 1) / 2
- 0 &le; `u`, `v` < `V`

---

## Editorial

The Breadth First Search (BFS) algorithm is a graph traversal technique that explores the neighbor nodes first before moving to the next level neighbors. It's often implemented using a queue.

Here's a high-level overview of the algorithm:
1.  Start at a given vertex (in this case, vertex 0) and add it to a queue.
2.  Mark the starting vertex as visited.
3.  While the queue is not empty, dequeue a vertex and for each of its unvisited neighbors, mark them as visited and enqueue them.

To implement this, you'll need an adjacency list to represent the graph, a boolean array to keep track of visited vertices, and a queue to manage the traversal. The adjacency list is an array of lists, where `adj[i]` contains a list of all vertices adjacent to vertex `i`. The `visited` array will store whether a vertex has been visited.