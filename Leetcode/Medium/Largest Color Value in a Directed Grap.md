# Largest Color Value in a Directed Graph

[题目](https://leetcode.com/problems/largest-color-value-in-a-directed-graph/description/)

又是图表题，不过是全新知识点。做法自然还是在bfs/dfs的基础上扩张，不过我没改写成功dfs的做法(c++,java不懂啊！)，所以只有bfs。

```c#
//https://leetcode.com/problems/largest-color-value-in-a-directed-graph/solutions/3396205/image-explanation-simple-bfs-complete-intuition-c-java-python/
class Solution {
    public int LargestPathValue(string colors, int[][] edges) {
        int n = colors.Length; //colors对应各个node的颜色，因此它的长度也是node的数量
        int[] indegrees = new int[n]; //记录入度：指向该顶点的边的数量；
        List<List<int>> graph = new(); //邻接表
        for (int i = 0; i < n; i++) {
            graph.Add(new());
        }
        foreach(int[] edge in edges) {
            graph[edge[0]].Add(edge[1]);
            indegrees[edge[1]]++;
        }
        Queue<int> zeroIndegree = new(); //先从入度为0的node下手
        for (int i = 0; i < n; i++) {
            if (indegrees[i] == 0) {
                zeroIndegree.Enqueue(i);
            }
        }
        int[][] counts = new int[n][]; //各个node所在路线上的各个颜色数量
        for (int i = 0; i < n; i++) {
            counts[i]=new int[26];
            counts[i][colors[i] - 'a']++;
        }
        int maxCount = 0;
        int visited = 0;
        while (zeroIndegree.Count!=0) {
            int u = zeroIndegree.Dequeue();//依次取出零度node
            visited++; //记录走了多少的点
            foreach(int v in graph[u]) {
                for (int i = 0; i < 26; i++) {
                    counts[v][i] = Math.Max(counts[v][i], counts[u][i] + (colors[v] - 'a' == i ? 1 : 0));
                }
                indegrees[v]--; //因为走到邻居了，因此度数减1
                if (indegrees[v] == 0) {
                    zeroIndegree.Enqueue(v);
                }
            }
            maxCount = Math.Max(maxCount, counts[u].Max());
        }
        return visited == n ? maxCount : -1; //如果当前图表出现了循环，visited数量会大于node数量
    }
}
```

```
Runtime
513 ms
Beats
100%
Memory
92.8 MB
Beats
100%
```

此题所用的思想叫“[拓扑排序](https://zhuanlan.zhihu.com/p/135094687)(topological sorting)”。虽然名字里有排序，该算法本身却与我们平常说的排序算法不同。它针对某一类图，找到一个可以执行的线性顺序。此算法适用于Directed acyclic graph (DAG)，有向无环图，即node之间的边有方向，且图内没有循环。如果图内有循环就会出现计数不等于真正node数量的情况。因此这个算法也可以用来判圈。