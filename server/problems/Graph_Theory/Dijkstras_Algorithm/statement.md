# Dijkstra's Algorithm

## Description

You are given a weighted, directed graph with `V` vertices and `E` edges. You have to find the shortest distance from a source vertex `S` to all other vertices in the graph.

## Input Format

- The first line contains two integers, `V` and `E`, representing the number of vertices and edges, respectively.
- The next `E` lines each contain three integers, `u`, `v`, and `w`, representing an edge from vertex `u` to vertex `v` with weight `w`.
- The last line contains a single integer, `S`, representing the source vertex.

## Output Format

- Print a single line containing `V` space-separated integers, where the `i`-th integer is the shortest distance from the source vertex `S` to vertex `i`. If a vertex is unreachable, print -1.

## Constraints

- 1 &le; `V` &le; 100
- 0 &le; `E` &le; `V` * `V`
- 0 &le; `u`, `v` < `V`
- 1 &le; `w` &le; 1000
- 0 &le; `S` < `V`

---

## Editorial

Dijkstra's algorithm is a greedy algorithm that finds the shortest paths between nodes in a graph. It works by maintaining a set of visited vertices and a distance array to store the shortest known distance from the source to each vertex.

Here's a high-level overview of the algorithm:
1.  Initialize a distance array `dist` with infinity for all vertices except the source, which is 0.
2.  Use a priority queue to store vertices that are being processed, prioritized by their distance.
3.  Add the source vertex to the priority queue.
4.  While the priority queue is not empty, extract the vertex `u` with the smallest distance.
5.  For each neighbor `v` of `u`, if the distance to `v` can be improved by going through `u`, update the distance and add `v` to the priority queue.

To implement this, you'll need an adjacency list of pairs to represent the graph (storing both the neighbor and the edge weight), a distance array, and a priority queue.