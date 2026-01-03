# 3786. Total Sum of Interaction Cost in Tree Groups

There is a tree with `n` nodes, and each node has a specific integer color `colors[i]`.

The interaction cost between two nodes of the SAME color is defined as the distance between them.
Return the sum of interaction costs for ALL pairs of nodes that have the same color.

**Input:**
- `n` (number of nodes)
- A list of `n-1` edges.
- A list of `n` integers representing colors.

**Output:**
- The total sum of distances between monochrome pairs.

---

## Editorial

**Core Concept**: Contribution Technique with Groups.

We want the sum of distances between all pairs of nodes with the SAME color.
We apply the "Toll Booth" logic, but filtered by color.

**The Fix**:
Pick an edge $u \to p$. This edge partitions the tree into Subtree ($S$) and Outside ($O$).

**The Traffic for Color C**:
How many paths connecting two nodes of Color $C$ pass through this edge?
It's simply: (Count of Color $C$ in Subtree) $\times$ (Count of Color $C$ Outside).

**Algorithm**:
1. Global Step: Count total occurrences of each color, `Total[color]`.
2. DFS Step: Return a map `{color: count}` from each subtree.
   (Optimized: Use Small-to-Large merging or simple recursion if $N$ small enough; for $O(N^2)$ worst case simple map is fine, but for $O(N \log^2 N)$ small-to-large is needed. Here we focus on the logic).
3. At edge $u \to p$, for each color $c$ found in $u$'s subtree:
   `Contribution += count_in_subtree[c] * (Total[c] - count_in_subtree[c])`

**Complexity**: O(N log N) or O(N^2) depending on implementation.
