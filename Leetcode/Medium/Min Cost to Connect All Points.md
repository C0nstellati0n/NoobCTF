# Min Cost to Connect All Points

[题目](https://leetcode.com/problems/min-cost-to-connect-all-points)

其实这个知识点之前学过啊：[Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree](../Hard/Find%20Critical%20and%20Pseudo-Critical%20Edge.md).题目要求找连接起所有点的最短路径，这就是最小生成树。不过有个不一样的地方，题目本身没有graph，必须手动把所有点连到一起并将weight设为点之间的距离，然后再找mst。
```c#
//https://leetcode.com/problems/min-cost-to-connect-all-points/solutions/4045874/94-85-prim-kruskal-with-min-heap
//prim： https://en.wikipedia.org/wiki/Prim%27s_algorithm
public class Solution {
    public static int ManhattanDistance(int[] p1, int[] p2) {
        return Math.Abs(p1[0] - p2[0]) + Math.Abs(p1[1] - p2[1]);
    }
    public int MinCostConnectPoints(int[][] points) {
        int n = points.Length;
        bool[] visited = new bool[n];
        Dictionary<int, int> heapDict = new Dictionary<int, int>() { {0, 0} }; //记录目前连接某个node的最小weight的edge
        var minHeap = new SortedSet<(int w, int u)>() { (0, 0) }; //按weight从小到大存储所有的edge，w为edge的weight，u为edge连接的一个node
        int mstWeight = 0;
        while (minHeap.Count > 0) {
            var (w, u) = minHeap.Min; //prim是贪心算法，取出目前weight最小的edge
            minHeap.Remove(minHeap.Min);
            if (visited[u]) continue; //若该edge连接的node之前已经连接过了，跳过
            visited[u] = true;
            mstWeight += w;
            for (int v = 0; v < n; v++) {
                if (!visited[v]) { //遍历所有尚未连通的node
                    int newDistance = ManhattanDistance(points[u], points[v]); //计算当前的node u与即将连接的node v之前的edge的weight
                    if (newDistance < heapDict.GetValueOrDefault(v, int.MaxValue)) { //若weight小于之前已有的edge的weight
                        heapDict[v] = newDistance;
                        minHeap.Add((newDistance, v)); //添加新edge。由于使用sorteddict，后面添加的edge只要weight是较小的都会被有限考虑到
                    }
                }
            }
        }
        return mstWeight;
    }
}
```
```
Runtime
224 ms
Beats
61.62%
Memory
48.4 MB
Beats
75.49%
```
找了另外一个java的Kruskal，好改一点。
```c#
//https://leetcode.com/problems/min-cost-to-connect-all-points/solutions/843972/java-minimum-spanning-tree-prim-kruskal
class Solution {
    public int MinCostConnectPoints(int[][] points) {
        int n = points.Length, ans = 0;
        PriorityQueue<int[],int> pq = new(Comparer<int>.Create((x, y) => x-y)); //graph
        for(int i = 0; i < n; i++) {
            for(int j = i+1; j < n; j++) {
                int dist=findDist(points, i, j);
                pq.Enqueue(new int[]{ dist, i, j },dist); //把所有可能的edge全放进去
            }
        }
        int count = 0;
        UnionFind uf = new UnionFind(n);
        while(count < n-1) {
            int[] edge = pq.Dequeue(); //当前的edge一定是weight最小的edge
            if(uf.find(edge[1]) != uf.find(edge[2])) { //若两个node没有连接在一起
                ans += edge[0];
                count++;
                uf.union(edge[1], edge[2]); //连接node
            }
        }
        return ans;
    }
    private int findDist(int[][] points, int a, int b) {
        return Math.Abs(points[a][0] - points[b][0]) + Math.Abs(points[a][1] - points[b][1]);
    }
}
class UnionFind {   
        int[] parent;
        public UnionFind(int n) {
            this.parent = new int[n];
            for(int i = 0; i < n; i++) parent[i] = i;
        }		
        public void union(int a, int b) {
            parent[find(a)] = parent[find(b)];
        }
        public int find(int x) {
            if(parent[x] != x) parent[x] = find(parent[x]);
            return parent[x];
        }
    }
```
```
Runtime
167 ms
Beats
72.97%
Memory
73.4 MB
Beats
30.67%
```