# Minimum Score of a Path Between Two Cities

[题目](https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/)

找到城市之间最短的路径。本来一个Min函数直接就出来了，然而有一种特殊情况：有些城市不跟主干道（城市1-n的路线）连着，所以它们不能考虑在内。常规做法是bfs，另外还有一种非常巧妙的做法。

```c#
//https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/solutions/3326775/image-explanation-both-bfs-dfs-approaches-c-java-python-union-find-is-overrated/
class Solution {
    public int MinScore(int n, int[][] roads) {
        int ans = Int32.MaxValue;
        List<List<Tuple<int, int>>> gr = new();
        for(int i = 0; i < n+1; i++) {
            gr.Add(new List<Tuple<int, int>>());
        }

        foreach(int[] edge in roads) { 
            gr[edge[0]].Add(new Tuple<int,int>(edge[1], edge[2])); // u-> {v, dis}
            gr[edge[1]].Add(new Tuple<int,int>(edge[0], edge[2])); // v-> {u, dis}
        }

        int[] vis = new int[n+1]; //vis数组记录已访问过的节点
        Array.Fill(vis, 0);
        Queue<int> q = new();
        q.Enqueue(1);
        vis[1] = 1;
        while(q.Count!=0) {
            int node = q.Dequeue();
            foreach(Tuple<int, int> tuple in gr[node]) {
                int v= tuple.Item1;
                int dis = tuple.Item2;
                ans = Math.Min(ans, dis);
                if(vis[v]==0) {
                    vis[v] = 1;
                    q.Enqueue(v);
                }
            }
        }
        return ans;
    }
}
```

```
Runtime
459 ms
Beats
66.67%
Memory
69.4 MB
Beats
58.33%
```

我们把所有节点的连接关系记录下来，就能知道哪个节点不在主干道上了。

```c#
//https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/solutions/3327539/with-images-and-hints-beats-94-dsu-union-find/
class Solution {
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
    public int MinScore(int n, int[][] roads) {
        parent = new int[n+1];
        rank = new int[n+1];
        for(int i=1; i<n+1; i++){
            parent[i] = i;
        }
        int minPath = Int32.MaxValue;
        foreach(int[] road in roads){
            makeUnion(road[0], road[1]);
        }

        // start is always node 1
        int xPar = find(1);
        foreach(int[] road in roads){
            // end can be any node from the roads array
            int yPar = find(road[0]);
            if(xPar == yPar) { //xPar是节点1，yPar是任意节点连接到的位置。如果两者不相同，说明当前查看的节点不和主干道连着
                minPath = Math.Min(minPath, road[2]);
            }
        }

        return minPath;
    }
}
```

```
Runtime
401 ms
Beats
100%
Memory
69.7 MB
Beats
58.33%
```