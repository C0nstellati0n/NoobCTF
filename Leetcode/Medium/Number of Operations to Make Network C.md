# Number of Operations to Make Network Connected

[题目](https://leetcode.com/problems/number-of-operations-to-make-network-connected/description/)

这题和昨天做的一道题非常像，于是我改动了一下昨天的代码，一次过。

```c#
public class Solution {
    int[] parent;
    int[] rank;
    int find(int x){
        while(parent[x]!=x){
            x = parent[parent[x]];
        }
        return x;
    }
    void makeUnion(int x, int y){
        int xPar = find(x);
        int yPar = find(y);
        if(xPar == yPar){
            return;
        }
        else if(rank[xPar]<rank[yPar]){
            parent[xPar] = yPar;
        }
        else if(rank[xPar]>rank[yPar]){
            parent[yPar] = xPar;
        }
        else{
            parent[yPar] = xPar;
            rank[xPar]++;
        }
    }
    public int MakeConnected(int n, int[][] connections) {
        if(n-1>connections.Length){
            return -1;
        }
        parent = new int[n+1];
        rank = new int[n+1];
        for(int i=0; i<n+1; i++){
            parent[i] = i;
        }
        foreach(int[] connection in connections){
            makeUnion(connection[0], connection[1]);
        }
        int xPar = find(0);
        List<int> diffs=new();
        for(int i=1;i<=n;i++){
            int yPar = find(i);
            if(yPar!=xPar&&!diffs.Contains(yPar)){
                diffs.Add(yPar);
            }
        }
        return diffs.Count-1;
    }
}
```

```
Runtime
253 ms
Beats
19.67%
Memory
56.5 MB
Beats
54.10%
```

去看了一下，还真有这种做法，更高效的写法如下：

```c#
//https://leetcode.com/problems/number-of-operations-to-make-network-connected/solutions/3331562/from-75-to-100-union-find-with-images-java-c/
class Solution {
    int[] parent;
    int[] rank;
    int find(int x){
        while(parent[x]!=x){
            x = parent[parent[x]];
        }
        return x;
    }
    int makeUnion(int x, int y){
        int parX = find(x);
        int parY = find(y);
        if(parX == parY){
            return 0;
        }
        else if(rank[parX]<rank[parY]){
            parent[parX] = parY;
        }
        else if(rank[parX]>rank[parY]){
            parent[parY] = parX;
        }
        else{
            parent[parY] = parX;
            rank[parX]++;
        }
        return 1;
    }
    public int MakeConnected(int n, int[][] connections) {
        int edges = connections.Length;
        if(edges<n-1){
            return -1;
        }
        parent = new int[n];
        rank = new int[n];
        for(int i=0; i<n; i++){
            parent[i] = i;
        }
        int components = n;
        foreach(int[] con in connections){
            components -= makeUnion(con[0], con[1]);
        }
        return components-1;
    }
}
```

```
Runtime
179 ms
Beats
93.44%
Memory
56.2 MB
Beats
63.93%
```

或者使用经典的dfs。

```c#
//https://leetcode.com/problems/number-of-operations-to-make-network-connected/solutions/3330446/image-explanation-easiest-dfs-c-java-python/
class Solution {
    int dfs(int u, List<int>[] graph, bool[] visited) {
        if (visited[u]) return 0;
        visited[u] = true;
        foreach (int v in graph[u]) dfs(v, graph, visited);
        return 1;
    }

    public int MakeConnected(int n, int[][] connections) {
        if (connections.Length < n - 1) return -1;
        List<int>[] graph = new List<int>[n];
        for (int i = 0; i < n; i++) graph[i] = new();
        foreach(int[] c in connections) {
            graph[c[0]].Add(c[1]);
            graph[c[1]].Add(c[0]);
        }
        
        int components = 0;
        bool[] visited = new bool[n];
        for (int v = 0; v < n; v++) components += dfs(v, graph, visited);
        return components - 1;
    }
}
```

```
Runtime
180 ms
Beats
91.80%
Memory
59.2 MB
Beats
13.12%
```

前两种做法基于union find，都是从图表本身入手。我的做法将0号点作为固定的点，任何不和0号点连在一起的点都被视为剩下的点，需要用线连接。遍历全部的点，利用find方法找到这些点连接的父辈，如果不是1，就是需要用线连接的。第二种方法是优化版本。为什么要一个一个点遍历？把所有连在一起的点作为整体不就好了吗？比如这里3台连在一次，那里5台连在一起，就是两块区域需要连接，一条线。dfs就不用考虑这么多了，把n台电脑全走一遍，自然需要n-1条线了。