# Is Graph Bipartite?

[题目](https://leetcode.com/problems/is-graph-bipartite/description/)

这题要用graph coloring。遍历方式自然还是经典的bfs/dfs。

```c#
//https://leetcode.com/problems/is-graph-bipartite/solutions/115487/java-clean-dfs-solution-with-explanation/
public class Solution {
     public bool IsBipartite(int[][] g) {
        int[] colors = new int[g.Length];
        for (int i = 0; i < g.Length; i++)
            if (colors[i] == 0 && !validColor(g, colors, 1, i))
                return false;
        return true;
    }

    bool validColor(int[][] g, int[] colors, int color, int node) {
        if (colors[node] != 0)
            return colors[node] == color; //如果已经上色的话，上的色要和函数给的色一样。因为函数给的色一定是遵循“当前node与相邻node颜色不一致”的规则的。所以只要之前上的色匹配不上就是有问题
        colors[node] = color;
        foreach(int adjacent in g[node])
            if (!validColor(g, colors, -color, adjacent)) //上相反色
                return false;
        return true;
    }
}
```
```
Runtime
119 ms
Beats
81.48%
Memory
47.1 MB
Beats
61.73%
```
```c#
class Solution {
    public bool IsBipartite(int[][] graph) {
        int len = graph.Length;
        int[] colors = new int[len];
        
        for (int i = 0; i < len; i++) {
            if (colors[i] != 0) continue;
            Queue<int> queue = new();
            queue.Enqueue(i);
            colors[i] = 1;   // Blue: 1; Red: -1.
            
            while (queue.Count!=0) {
                int cur = queue.Dequeue();
                foreach(int next in graph[cur]) {
                    if (colors[next] == 0) {          // If this node hasn't been colored;
                        colors[next] = -colors[cur];  // Color it with a different color;
                        queue.Enqueue(next);
                    } else if (colors[next] != -colors[cur]) {   // If it is colored and its color is different, return false;当前node与相邻node的颜色的负数一致，那就是不能和相邻的node颜色一样
                        return false;
                    }
                }
            }
        }
        
        return true;
    }
}
```
```
Runtime
121 ms
Beats
74.7%
Memory
47.4 MB
Beats
38.27%
```
搜了一下，这个算法的原理在于：
```
This means that we can color all the vertices of the graph using two different colors such that no two adjacent vertices have the same color. If it can be 2-colored, then it is bipartite, otherwise, it is not. 
```
关键在于两个相邻的顶点不可能是一个颜色。