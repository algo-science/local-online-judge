# 1339. Maximum Product of Splitted Binary Tree

Given the `root` of a binary tree, split the binary tree into two subtrees by removing one edge such that the product of the sums of the subtrees is maximized.

Return the maximum product of the sums of the two subtrees. Since the answer may be too large, return it modulo `10^9 + 7`.

**Input:**
- `n` (number of nodes)
- List of edges (representing binary tree structure)
- List of `n` values (node values)

**Output:**
- Start max product modulo `10^9 + 7`.

---

## Editorial

**Core Concept**: Splitting Technique (Fixing the edge).

Cutting an edge splits the tree into two parts:
1. Subtree sum $S$
2. Rest of tree sum $(Total - S)$

**The Fix**:
Iterate through EVERY edge (by visiting every node $u$ and looking at edge $u \to parent$).

**The Traffic**:
We aren't counting paths here, but the product of sums.
`Product = S * (Total - S)`

**Algorithm**:
1. First DFS: Calculate total sum of the entire tree `Total`.
2. Second DFS (or same one): For each subtree sum `S`, calculate `P = S * (Total - S)`.
3. Maximize `P`.

**Complexity**: O(N).
