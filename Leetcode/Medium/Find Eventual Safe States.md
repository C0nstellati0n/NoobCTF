# Find Eventual Safe States

[题目](https://leetcode.com/problems/find-eventual-safe-states/description/)

尝试靠自己想出一个dfs做法，但是发现了个问题。dfs有个visited对吧，但是这题要求遍历全部的路线，那visited怎么记，遇到路线上重复的node我是记还是不记？那要是我统一不记，这题又可能有环，那不无限递归了？要是我统一记，怎么遍历全部路线？要是我看情况记或者不记，那个情况是啥？快去看editorial。
```c#
//https://leetcode.com/problems/find-eventual-safe-states/editorial/
class Solution {
    public IList<int> EventualSafeNodes(int[][] graph) {
        int n = graph.Length;
        int[] indegree = new int[n];
        List<List<int>> adj = new();

        for(int i = 0; i < n; i++) {
            adj.Add(new());
        }

        for (int i = 0; i < n; i++) {
            foreach(int node in graph[i]) {
                adj[node].Add(i); //虽然已经有邻接表graph了，但是graph记录的是一个node向外的edge数量，或者说“出度”；然而拓补排序需要看“入度”，一个node有多少edge指向它的数量
                indegree[i]++; //说实话这我有点不懂，按照题目对graph的描述，foreach里的每个node应该都为i->node,那入度加的应该是node的吧？所以这里加的应该是出度。不过是对的，因为这题要求找的terminal node是出度为0的node，而不是入度为0。评论区有人提到这点了，有人觉得是写错了，有人觉得是 “nodes are added in reverse order , so outdegree becomes indegree in this case”。看editorial的解析图可能是因为把edge反过来了
            }
        }

        Queue<int> q = new();
        // Push all the nodes with indegree zero in the queue.
        for (int i = 0; i < n; i++) {
            if (indegree[i] == 0) {
                q.Enqueue(i);
            }
        }

        bool[] safe = new bool[n];
        while (q.Any()) {
            int node = q.Dequeue();
            safe[node] = true; //所有出度为0的node会被加进queue，等于就是terminal node，可以放心加进safe里

            foreach(int neighbor in adj[node]) {
                // Delete the edge "node -> neighbor".
                indegree[neighbor]--;
                if (indegree[neighbor] == 0) {
                    q.Enqueue(neighbor);
                }
            }
        }

        List<int> safeNodes = new();
        for (int i = 0; i < n; i++) {
            if (safe[i]) {
                safeNodes.Add(i);
            }
        }
        return safeNodes;
    }
}
```
```
Runtime
286 ms
Beats
83.72%
Memory
62.6 MB
Beats
27.91%
```
不对，这是bfs，而且咋又扯到拓扑排序了？这题要求找出所有的safe node， A node is a safe node if every possible path starting from that node leads to a terminal node (or another safe node). 要是这题没有那个括号，只看terminal node，或许会简单一点。我怎么知道什么node是safe node？就是这点加上上面说的dfs让我懵了好久。editorial的重点在于这句话：

```
If there is no path from the node that enters a cycle, we will always be able to reach a terminal node. As a result, such a node is a safe node and should be added to our answer array.

The problem is reduced to finding the nodes that do not have any paths that lead to a cycle.
```

所以要判环。那这又有拓扑什么事？假如一个node的所有路径都导向一个terminal或safe node，它应该是类似a->b->c->d这样的。意味着，它所有path的出度都是很清晰的一条，可以从一个有限的终点倒着推回去。假如node在一个环里，那么环里的node都是头尾相接的，没法从任何一个node那里倒着推回去。这里用的拓扑为[Topological Sort Using Kahn's Algorithm](https://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/)，从入度（出度）为零的node出发，慢慢削减，环里的node因为入度与环里的node密切相关，而环里的node永远没法入队列，故拓扑算法永远不会走到它们上面。走到的node一定是safe或者terminal node。

当然dfs也能做啊。
```c#
//采样最佳，editorial里也有介绍
public class Solution {
    public IList<int> EventualSafeNodes(int[][] graph) {
        //Dettect Cycle in a DIrected Graph
        // If cycle is present mark those nodes as true and then remove those nodes and add remaining
        // to the list and return.

        bool[] visited = new bool[graph.Length]; //上面提到的dfs问题就用两个visited解决，一个记录走过的node，一个记录dfs走过的node
        bool[] dfsVisited = new bool[graph.Length];

        bool[] cyclePresent = new bool[graph.Length];

        for(int i =0;i<graph.Length;i++){
            if(!visited[i])
            DFSRec(i,graph,visited,dfsVisited,cyclePresent);
        }

        IList<int> result = new List<int>();

       for(int i =0;i<graph.Length;i++){
            if(!cyclePresent[i]){
                result.Add(i);
            }
        }

        return result;
    }

    public bool  DFSRec(int s,int[][] graph, bool[] visited, bool[] dfsVisited, bool[] cyclePresent){
        
        visited[s] = true;
        dfsVisited[s] = true;

        foreach(var t in graph[s]){
            if(!visited[t]){
                if(DFSRec(t,graph,visited,dfsVisited,cyclePresent)){
                    return cyclePresent[s] = true;
                }
            }
            else if(visited[t] && dfsVisited[t]){ //没有环的话是不会走重复的
                return cyclePresent[s] = true;
            }
        }
        dfsVisited[s] = false; //关于s的path走完后就取消，其他node还要用
        return false;
    }
}
```
```
Runtime
266 ms
Beats
100%
Memory
62.1 MB
Beats
74.42%
```