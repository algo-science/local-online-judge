# 834. Sum of Distances in Tree

There is an undirected connected tree with `n` nodes labeled from `0` to `n - 1` and `n - 1` edges.

You are given the integer `n` and the array `edges` where `edges[i] = [ai, bi]` indicates that there is an edge between nodes `ai` and `bi` in the tree.

Return an array `answer` of length `n` where `answer[i]` is the sum of the distances between the `i`th node and all other nodes in the tree.

---

## Editorial

**Core Concept**: The "Toll Booth" / Contribution Technique.

Instead of calculating distances for every pair $(u, v)$, we calculate how much each **edge** contributes to the total sum.

**The Fix**:
Pick an edge connecting $u$ (child) and $p$ (parent).
Cutting this edge splits the tree into two components:
1. Subtree at $u$ (size $S$)
2. The rest of the tree (size $N - S$)

**The Traffic**:
Any path starting in the subtree and ending outside MUST cross this edge.
Total crossings = $S \times (N - S)$.

**Algorithm**:
1. Run DFS to calculate subtree size for each node.
2. For each node $u$ (except root), finding edge to parent $p$:
   `Contribution = subtree_size[u] * (N - subtree_size[u])`
3. Sum up all contributions.

This reduces the complexity from $O(N^2)$ to $O(N)$.
