# Remove Max Number of Edges to Keep Graph Fully Traversable

[题目](https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/description/)

跟昨天的有点像，又不是完全像。

```c#
//https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/solutions/3468066/image-explanation-easiest-complete-intuition-c-java-python/
class DSU {
    int[] parent;
    int[] rank;
    
    public DSU(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }
    
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    public bool union(int x, int y) {
        int xset = find(x), yset = find(y);
        if (xset != yset) {
            if (rank[xset] < rank[yset]) {
                parent[xset] = yset;
            } else if (rank[xset] > rank[yset]) {
                parent[yset] = xset;
            } else {
                parent[xset] = yset;
                rank[yset]++;
            }
            return true; //返回true：两个node没有同一个parent，需要连接
        }
        return false; //返回false：两个node有同一个parent，可以移除多余的edge
    }
}

class Solution {
    public int MaxNumEdgesToRemove(int n, int[][] edges) {
        Array.Sort(edges, (a, b) => b[0]- a[0]);
        
        DSU dsu_alice = new DSU(n+1);
        DSU dsu_bob = new DSU(n+1);
        
        int removed_edge = 0, alice_edges = 0, bob_edges = 0;
        foreach(int[] edge in edges) {
            if (edge[0] == 3) {
                if (dsu_alice.union(edge[1], edge[2])) { //检查两个node是否连着（是否有同一个parent）
                    dsu_bob.union(edge[1], edge[2]);
                    alice_edges++; //不连着的话需要增加edge的数量
                    bob_edges++;
                } else {
                    removed_edge++; //已经连着说明当前检查的edge是多余的，可以移掉
                }
            } else if (edge[0] == 2) {
                if (dsu_bob.union(edge[1], edge[2])) {
                    bob_edges++;
                } else {
                    removed_edge++;
                }
            } else {
                if (dsu_alice.union(edge[1], edge[2])) {
                    alice_edges++;
                } else {
                    removed_edge++;
                }
            }
        }
        
        return (bob_edges == n - 1 && alice_edges == n - 1) ? removed_edge : -1; //bob_edges或alice_edges大于n-1的情况说明题目给的图表就不是互相连着的，无法遍历，返回-1
    }
}
```

```
Runtime
536 ms
Beats
54.55%
Memory
66.8 MB
Beats
27.27%
```

稍微变化的解法：

```c#
//https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/solutions/3468567/day-395-dsu-100-0ms-python-java-c-explained-approach/
class Solution {
    public int MaxNumEdgesToRemove(int n, int[][] edges) {
        // Move all edges of type BOTH to the end of the array
        for (int i = 0, j = edges.Length - 1; i < j; ) {
            if (edges[i][0] == 3) {
                ++i;
                continue;
            }
            var temp = edges[i];
            edges[i] = edges[j];
            edges[j] = temp;
            --j;
        }

        // Create two UnionFind data structures, one for Alice and one for Bob
        UnionFind aliceUf = new UnionFind(n);
        UnionFind bobUf = new UnionFind(n);
        int added = 0;

        // Iterate over the edges and add them to the appropriate UnionFind data structure
        foreach(int[] edge in edges) {
            int type = edge[0];
            int u = edge[1];
            int v = edge[2];

            // Add the edge to both UnionFind data structures if it is of type BOTH
            if (type == 3) {
                added += aliceUf.union(u, v) | bobUf.union(u, v);
            } else if (type == 1) {
                added += aliceUf.union(u, v);
            } else {
                added += bobUf.union(u, v);
            }

            // If both UnionFind data structures are united, return the number of edges that were not added
            if (aliceUf.isUnited() && bobUf.isUnited())
                return edges.Length - added;
        }

        // If both UnionFind data structures are united, return the number of edges that were not added
        if (aliceUf.isUnited() && bobUf.isUnited())
            return edges.Length - added;

        // If both UnionFind data structures are not united, it is impossible to remove enough edges to make them united
        return -1;
    }
}

class UnionFind {
    int[] parent;
    int groups;

    // Initialize the UnionFind data structure with n groups
    public UnionFind(int n) {
        parent = new int[n + 1];
        groups = n;
    }

    // Union two elements and return 1 if they were not already in the same group, 0 otherwise
    public int union(int u, int v) {
        int uParent = find(u);
        int vParent = find(v);
        if (uParent == vParent)
            return 0;
        parent[uParent] = vParent;
        --groups;
        return 1;
    }

    // Find the parent of an element and perform path compression
    int find(int v) {
        if (parent[v] != 0)
            return parent[v] = find(parent[v]);
        return v;
    }

    // Check if all elements are in the same group
    public bool isUnited() {
        return groups == 1;
    }
}
```

```
Runtime
477 ms
Beats
100%
Memory
65.8 MB
Beats
54.55%
```