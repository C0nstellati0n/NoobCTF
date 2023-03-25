# Reorder Routes to Make All Paths Lead to the City Zero

[题目](https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/)

题型稍微变化一下我直接寄。不说了，来看大佬的炸裂答案。

```c#
//https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/solutions/3334159/image-explanation-complete-intuition-dfs-c-java-python/
class Solution {
    int dfs(List<List<int>> al, bool[] visited, int from) {
        int change = 0;
        visited[from] = true;
        foreach(var to in al[from])
            if (!visited[Math.Abs(to)])
                change += dfs(al, visited, Math.Abs(to)) + (to > 0 ? 1 : 0);
        return change;   
    }
    public int MinReorder(int n, int[][] connections) {
        List<List<int>> al = new();
        for(int i = 0; i < n; ++i) 
            al.Add(new());
        foreach(var c in connections) {
            al[c[0]].Add(c[1]);
            al[c[1]].Add(-c[0]);
        }
        return dfs(al, new bool[n], 0);
    }
}
```

```
Runtime
308 ms
Beats
100%
Memory
61.8 MB
Beats
93.33%
```

这道题的其实还是图表，然而是有向图表。之前做的题都是无向的，dfs/bfs无脑遍历就完事了。这题有两种连接方向：0是根节点，子节点指向根节点，或者根节点指向子节点。要找出根节点指向子节点的路径数量。首先图表题，很自然地想到用[邻接表](https://zh.wikipedia.org/wiki/%E9%82%BB%E6%8E%A5%E8%A1%A8)（adjacency list）来记录节点间的连接关系。此题的关键点：怎么记录才能体现方向的概念？大佬给出的解答是：用负号。题目给出的connections的顺序是connection[0]->connection[1]，于是我们将connection[1]的连接情况用-connection[0]表示。这么一改，自然dfs也要改。从0开始，沿着这条路往下访问节点。负数的作用体现在`(to > 0 ? 1 : 0)`，表示自己是否算在changes内。大于0，表示方向错误，要加上自己；小于0则正确。