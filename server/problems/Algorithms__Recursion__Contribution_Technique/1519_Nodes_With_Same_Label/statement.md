# 1519. Number of Nodes in the Sub-Tree With the Same Label

You are given a tree (i.e., a connected, undirected graph that has no cycles) consisting of `n` nodes numbered from `0` to `n - 1` and exactly `n - 1` edges. The root of the tree is the node `0`.

You are also given a string `labels` of length `n`, where `labels[i]` is the label of the `i`th node (matches `[a-z]`).

Return an array of size `n` where `ans[i]` is the number of nodes in the subtree of the `i`th node which have the same label as node `i`.

**Input:**
- `n` (number of nodes)
- List of edges
- String `labels`

**Output:**
- Space-separated list of counts.

---

## Editorial

**Core Concept**: Subtree Frequency Counting.

This is the precursor to the "Group Interaction" problem.
We need to count how many nodes in the subtree of $u$ have the same label as $u$.

**The Fix**:
We process one node $u$ at a time (fixing the root of the subtree).

**The Traffic**:
We need to aggregate data from children.
Since we need counts for *specific* labels, we return a frequency map (or array of size 26) from each child.

**Algorithm**:
1. DFS returning `count[26]`.
2. Merge children's counts: `count[i] += child_count[i]`.
3. Add self: `count[labels[u]]++`.
4. Answer for $u$ is `count[labels[u]]`.

**Complexity**: O(26 * N) = O(N).
