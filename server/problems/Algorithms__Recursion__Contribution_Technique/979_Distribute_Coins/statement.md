# 979. Distribute Coins in Binary Tree

You are given the `root` of a binary tree with `n` nodes where each node in the tree has `node.val` coins. There are `n` coins in total throughout the whole tree.

In one move, we may choose two adjacent nodes and move one coin from one node to another. A move may be from parent to child, or from child to parent.

Return the minimum number of moves required to make every node have exactly one coin.

**Input:**
- `n` (number of nodes)
- List of edges
- List of `n` values (coins at each node)

**Output:**
- Minimum moves.

---

## Editorial

**Core Concept**: Flow / Net Balance.

We need to move coins so every node has 1 coin.
Instead of asking "Where does this specific coin go?", asking "How many coins must flow through this edge?".

**The Fix**:
Pick an edge connecting subtree $u$ to parent $p$.

**The Traffic**:
Coins inside subtree: $C$.
Nodes inside subtree: $S$.
Effect: The subtree needs $S$ coins total. It has $C$.
The difference $(C - S)$ MUST flow through the edge $u \to p$.
- If $C > S$, excess coins flow OUT.
- If $C < S$, missing coins flow IN.
- Traffic = `abs(C - S)`.

**Algorithm**:
1. DFS returning a pair `{subtree_size, subtree_coins}`.
2. At each node, calculate `balance = coins - size`.
3. `Total_Moves += abs(balance)`.

**Complexity**: O(N).
