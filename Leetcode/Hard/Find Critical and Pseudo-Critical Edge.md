# Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree

[题目](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/description/)

当一道题目描述+hint提到的概念我完全没听过时，我就知道该放弃了。
```c#
//https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/editorial/
class Solution {
    public IList<IList<int>> FindCriticalAndPseudoCriticalEdges(int n, int[][] edges) {
        // Add index to edges for tracking
        int m = edges.Length;
        int[][] newEdges = new int[m][];

        for (int i = 0; i < m; i++) {
            newEdges[i]=new int[4]; //newEdge[i]记录的是：newEdge[0]=node1,newEdge[1]=node2,newEdge[2]=weight,newEdge[3]=edge index
            for (int j = 0; j < 3; j++) {
                newEdges[i][j] = edges[i][j];
            }
            newEdges[i][3] = i;
        }

        // Sort edges based on weight
        Array.Sort(newEdges, (x,y) => x[2]-y[2]); //Kruskal算法是一种贪心算法，优先考虑那些weight较低的edge。所以排序

        // Find MST weight using union-find
        UnionFind ufStd = new UnionFind(n);
        int stdWeight = 0;
        foreach(int[] edge in newEdges) {
            if (ufStd.union(edge[0], edge[1])) { //若true，说明这次添加的edge能够将原本不连着的node连在一起，是MST的一部分。false说明在这条edge之前两个node就已经连在一次了，不需要它
                stdWeight += edge[2];
            }
        }

        List<IList<int>> result = new();
        for (int i = 0; i < 2; i++) {
            result.Add(new List<int>());
        }
        // Check each edge for critical and pseudo-critical
        for (int i = 0; i < m; i++) {
            // Ignore this edge and calculate MST weight
            UnionFind ufIgnore = new UnionFind(n);
            int ignoreWeight = 0;
            for (int j = 0; j < m; j++) {
                if (i != j && ufIgnore.union(newEdges[j][0], newEdges[j][1])) {
                    ignoreWeight += newEdges[j][2];
                }
            }
            // If the graph is disconnected or the total weight is greater, 
            // the edge is critical
            if (ufIgnore.maxSize < n || ignoreWeight > stdWeight) {
                result[0].Add(newEdges[i][3]);
            } else {
                // Force this edge and calculate MST weight
                UnionFind ufForce = new UnionFind(n);
                ufForce.union(newEdges[i][0], newEdges[i][1]);
                int forceWeight = newEdges[i][2];
                for (int j = 0; j < m; j++) {
                    if (i != j && ufForce.union(newEdges[j][0], newEdges[j][1])) {
                        forceWeight += newEdges[j][2];
                    }
                }
                // If total weight is the same, the edge is pseudo-critical
                if (forceWeight == stdWeight) {
                    result[1].Add(newEdges[i][3]);
                }
            }
        }

        return result;
    }

    class UnionFind {
        int[] parent;
        int[] size;
        public int maxSize;

        public UnionFind(int n) {
            parent = new int[n];
            size = new int[n];
            maxSize = 1;
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                size[i] = 1;
            }
        }

        public int find(int x) {
            // Finds the root of x
            if (x != parent[x]) {
                parent[x] = find(parent[x]);
            }
            return parent[x];
        }

        public bool union(int x, int y) { //将node x和y连接起来，并返回布尔值。true表示两个node union之前没有连着，false表示在此次union之前两者已经连着了
            // Connects x and y
            int rootX = find(x);
            int rootY = find(y);
            if (rootX != rootY) {
                if (size[rootX] < size[rootY]) {
                    int temp = rootX;
                    rootX = rootY;
                    rootY = temp;
                }
                parent[rootY] = rootX;
                size[rootX] += size[rootY];
                maxSize = Math.Max(maxSize, size[rootX]);
                return true;
            }
            return false;
        }
    }
}
```
```
Runtime
165 ms
Beats
100%
Memory
52.1 MB
Beats
50%
```
其实挺好理解的（？），editorial已经讲的很清楚了。这边再补充几个关键概念链接。
- [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- [Minimum spanning tree(MST)](https://en.wikipedia.org/wiki/Minimum_spanning_tree)
- [Disjoint-set data structure(union-find data structure)](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)