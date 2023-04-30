# Checking Existence of Edge Length Limited Paths

[题目](https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/description/)

此题为[并查集](https://zhuanlan.zhihu.com/p/93647900)（DSU）。我以为我不认识它，其实内部是union find。哦老朋友了啊，虽然并没有我想象的那么熟。

```c#
//https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/solutions/3464929/image-explanation-easiest-complete-intuition-c-java-python/
class DSU {
    private int[] parent;
    private int[] rank;

    public DSU(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i; //初始化时每个node的parent都是自己
        }
    }

    public int find(int x) {
        if (parent[x] == x) {
            return x;
        }
        return parent[x] = find(parent[x]);
    }

    public bool union(int x, int y) {
        int xset = find(x), yset = find(y);
        if (xset != yset) {
            if (rank[xset] < rank[yset]) {
                parent[xset] = yset;
            } else {
                parent[yset] = xset;
            }
            if (rank[xset] == rank[yset]) {
                rank[xset]++;
            }
            return true;
        }
        return false;
    }
}

class Solution {
    public bool[] DistanceLimitedPathsExist(int n, int[][] edgeList, int[][] queries) {
        DSU dsu = new DSU(n);
        int i=0; //把i放在外面是因为下面也用了i。如果下面用j就没事，但是也用i的话在for循环里赋值会报错
        for (; i < queries.Length; i++) {
            queries[i] = new int[] { queries[i][0], queries[i][1], queries[i][2], i }; //多增加的那个i方便后续标注i号query是否为true
        }

        Array.Sort(queries, (a, b) => a[2]-b[2]); //可以用lambda函数做比较器，不过必须是两个参数的
        Array.Sort(edgeList, (a, b) => a[2]-b[2]);

        i = 0;
        bool[] res = new bool[queries.Length];
        foreach(int[] q in queries) {
            while (i < edgeList.Length && edgeList[i][2] < q[2]) { //这里是与普通union find不同的关键处。仅当两个node之间的距离小于query时才union，更大的就算是连着的也不用管。而且因为上面排序了，一个i自增就能搞定，不用再考虑后续的
                dsu.union(edgeList[i][0], edgeList[i][1]);
                i++;
            }

            if (dsu.find(q[0]) == dsu.find(q[1])) { //那么如果后续两个node find到同一个parent，说明之间肯定有小于query长度的路径
                res[q[3]] = true;
            }
        }

        return res;
    }
}
```

```
Runtime
556 ms
Beats
100%
Memory
67.6 MB
Beats
88.89%
```

看起来逻辑没有上一种那么清晰不过本质差不多的解法。

```c#
//https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/solutions/3465024/day-394-custom-union-find-100-0ms-python-java-c-explained-approach/
public class Solution {
 public bool[] DistanceLimitedPathsExist(int length, int[][] adjList, int[][] queries) {
        int[] parent = Enumerable.Range(0, length).ToArray();
        int[] rank = new int[length];
        int[] weight = new int[length];

        Array.Sort(adjList, (a, b) => a[2].CompareTo(b[2]));
        foreach (int[] edge in adjList) {
            Union(edge[0], edge[1], edge[2], parent, rank, weight);
        }

        bool[] answer = new bool[queries.Length];
        for (int i = 0; i < queries.Length; i++) {
            answer[i] = IsConnectedAndWithinLimit(queries[i][0], queries[i][1], queries[i][2], parent, weight);
        }

        return answer;
    }

    private bool IsConnectedAndWithinLimit(int p, int q, int limit, int[] parent, int[] weight) {
        return Find(p, limit, parent, weight) == Find(q, limit, parent, weight);
    }

    private int Find(int x, int limit, int[] parent, int[] weight) {
        while (x != parent[x]) {
            if (weight[x] >= limit) { //该种解法处理大于query的长度的路径时，会直接断掉，就找不到同一个parent了
                break;
            }
            x = parent[x];
        }
        return x;
    }

    private void Union(int x, int y, int limit, int[] parent, int[] rank, int[] weight) {
        int xRef = Find(x, int.MaxValue, parent, weight);
        int yRef = Find(y, int.MaxValue, parent, weight);
        if (xRef == yRef) {
            return;
        }
        if (rank[xRef] < rank[yRef]) {
            parent[xRef] = yRef;
            weight[xRef] = limit;
        } else {
            parent[yRef] = xRef;
            weight[yRef] = limit;
            if (rank[xRef] == rank[yRef]) {
                rank[xRef]++;
            }
        }
    }
}
```

```
Runtime
565 ms
Beats
100%
Memory
67.7 MB
Beats
88.89%
```