# 2477. Minimum Fuel Cost to Report to the Capital

There is a tree (i.e., a connected, undirected graph with no cycles) structure country network consisting of `n` cities numbered from `0` to `n - 1` and `n - 1` roads. The capital city is city `0`.

You are given a 2D integer array `roads` where `roads[i] = [ai, bi]` denotes that there exists a bidirectional road connecting cities `ai` and `bi`.

There is a meeting for the representatives of each city. The meeting is in the capital city.
There is a car in each city. You are given an integer `seats` that indicates the number of seats in each car.

A representative can travel between cities using cars. In each city, they can change cars or ride with others.
Return the minimum number of liters of fuel to report to the capital city.

**Input:**
- `n` (implied from roads)
- `roads` (list of edges)
- `seats`

**Output:**
- Minimum fuel cost.

---

## Editorial

**Core Concept**: Traffic Volume (flow).

We are not summing path lengths here, but rather calculating "trips" needed.
However, the "Fix the Edge" mindset applies perfectly.

**The Fix**:
Consider the edge connecting a subtree $u$ to its parent $p$.
All representatives in the subtree $u$ MUST cross this edge to get to the root (Capital).

**The Traffic**:
If the subtree size is $S$ (people), how many cars are needed?
Since each car holds `seats` people:
`Cars_Needed = ceil(S / seats)`

**Algorithm**:
1. DFS to get subtree size $S$.
2. For each edge, add `ceil(S/seats)` to the total fuel cost.
   (Note: `ceil(a/b)` can be calculated as `(a + b - 1) // b` using integer division).

**Complexity**: O(N).
