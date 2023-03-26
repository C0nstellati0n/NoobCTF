# Count Unreachable Pairs of Nodes in an Undirected Graph

[题目](https://leetcode.com/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/description/)

这题的关键点在于计算答案的公式。第一个方法将初始情况设为最大值，然后根据每组node的数量减出答案：

```
If all nodes were disconnected, pairs would be
nC2 === n*(n-1)/2.

Now store this in a long long var called ans.

Now if you found that one component have k connected nodes in it, we need to subtract the pairs formed by these connected k component from our ans, so the modified ans would be

ans = ans - k*(k-1)/2

In this way keep subtracting for all components of graph and at the end you will be left with the required ans.
```

第二个方法正好相反，将初始情况设为最小值，然后加出答案：

```
ans=0
find total no nodes in each component
ans = ans + (countNodes * (n - countNodes));
n = n - countNodes;
```

不难看出，无论哪种方法，重点都在“将node根据连接情况分组，每组中的node的数量”。或者说，连在一起的node是一组，可是有多少个node连在一起？这个问题的答案很简单，在基础的dfs/bfs/union find上加个计数器。

```c#
//https://leetcode.com/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/solutions/3337574/image-explanation-3-approaches-dfs-c-java-python/
//dfs
class Solution {
    List<List<int>> x = new();
    public long CountPairs(int n, int[][] edges) {
        for(int i=0; i<n; i++)
            x.Add(new());
        foreach(int [] edge in edges){
            x[edge[0]].Add(edge[1]);
            x[edge[1]].Add(edge[0]);
        }

        long sum = ((long)n*(n-1))/2;
        bool[] visited = new bool[n];
        for(int i=0; i<n; i++)
            if(!visited[i]){
                int cnt = dfs(i, visited, new int[1]);//这里用数组是因为直接传数字就不是引用类型了，需要在dfs方法内部初始化返回值（其实也可以这么做）
                sum -= ((long)(cnt) * (cnt-1))/2;
            }
        return sum;
    }

    int dfs(int node, bool[] visited, int[] count){ 
        if(visited[node]) return count[0];
        visited[node] = true;
        count[0]++;
        foreach(int curr in x[node])
            dfs(curr, visited, count);
        return count[0];
    }
}
```

```
Runtime
579 ms
Beats
90%
Memory
76 MB
Beats
90%
```

```c#
//https://leetcode.com/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/solutions/3337954/java-easy-bfs/
//bfs
class Solution {
    public long CountPairs(int n, int[][] edges) {
        List<List<int>> adj=new();
        for(int i=0;i<n;i++){
            adj.Add(new());
        }
        for(int i=0;i<edges.Length;i++){
            adj[edges[i][0]].Add(edges[i][1]);
            adj[edges[i][1]].Add(edges[i][0]);
        }
        long sum=n;
        long res=0;
        bool[] vis=new bool[n];
        for(int i=0;i<n;i++){
            if(!vis[i]){
                vis[i]=true;
                int count=bfs(i,vis,adj,0);
                sum-=count;
                res+=(sum*count);
            }
        }
        return res;
    }
    public int bfs(int i,bool[] vis,List<List<int>> adj,int count){
        Queue<int> qu=new();
        qu.Enqueue(i);
        count++;
        while(qu.Count!=0){
            int curr=qu.Dequeue();
            foreach(int adjnode in adj[curr]){
                if(!vis[adjnode]){
                    qu.Enqueue(adjnode);
                    count++;
                    vis[adjnode]=true;
                }
            }
        }
        return count;
    }
}
```

```
Runtime
596 ms
Beats
90%
Memory
70.5 MB
Beats
100%
```

发现在这种连接图表的题里面，union find的综合表现一般比dfs/bfs都高。

```c#
//https://leetcode.com/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/solutions/3339777/image-explanation-from-tle-to-100-union-find/
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
        return;
    }
    public long CountPairs(int n, int[][] edges) {
        parent = new int[n];
        rank = new int[n];
        for(int i=0; i<n; i++){
            parent[i] = i;
        }
        foreach(int[] edge in edges){
            makeUnion(edge[0], edge[1]);
        }
        long[] componentMembers = new long[n];
        for(int i=0; i<n; i++){
            int par = find(i);
            componentMembers[par]++;
        }
        long pairs = 0;
        long remainingMemebers = n;
        for(int i=0; i<n; i++){
            if(componentMembers[i]==0){
                continue;
            }
            long currentComponents = componentMembers[i];
            remainingMemebers -= currentComponents;
            long currentPairs = currentComponents * remainingMemebers;
            pairs+=currentPairs;
        }
        return pairs;
    }
}
```

```
Runtime
530 ms
Beats
100%
Memory
68.1 MB
Beats
100%
```