# [Design Graph With Shortest Path Calculator](https://leetcode.com/problems/design-graph-with-shortest-path-calculator)

c++ priority_queue不会用，于是又跑回了c#
```c#
//非常炸裂的运行时间：2077ms
public class Graph {
    Dictionary<int,List<int>> graph=new();
    Dictionary<string,int> costs=new();
    int n;
    public Graph(int n, int[][] edges) {
        this.n=n;
        foreach(int[] edge in edges){
            AddEdge(edge);
        }
    }
    public void AddEdge(int[] edge) {
        if(!graph.ContainsKey(edge[0]))
            graph[edge[0]]=new();
        graph[edge[0]].Add(edge[1]);
        costs[$"{edge[0]}.{edge[1]}"]=edge[2];
    }
    public int ShortestPath(int node1, int node2) {
        int[] ans=new int[n];
        Array.Fill(ans,int.MaxValue);
        ans[node1]=0;
        PriorityQueue<int,int> pq = new PriorityQueue<int,int>();
        pq.Enqueue(node1, 0);
        while(pq.Count>0){
            int cur = pq.Dequeue();
            if(graph.ContainsKey(cur)){
                foreach(int neighbour in graph[cur]){
                    int comp=ans[cur]+costs[$"{cur}.{neighbour}"];
                    if(ans[neighbour] > comp){
                        ans[neighbour] = comp;
                        pq.Enqueue(neighbour, comp);
                    }
                }
            }
        }
        return ans[node2]==int.MaxValue?-1:ans[node2];
    }
}
```
discussion提到了dijkstra，我就去之前的笔记那里改了个写法：[Path With Minimum Effort](../Medium/Path%20With%20Minimum%20Effort.md)。没有TLE我是没想到的。这边建议用采样区的做法，思路大差不差，但是具体实现细节使这个做法只需323ms
```c#
public class Graph 
{
    private readonly int n;
    private readonly List<int[]>[] adj;
    public Graph(int n, int[][] edges)
    {
        this.n = n;
        adj = new List<int[]>[n];
        for (int i = 0; i < n; i++)
        {
            adj[i] = new List<int[]>();
        }
        foreach (int[] edge in edges)
        {
            AddEdge(edge);
        }
    }
    public void AddEdge(int[] edge)
    {
        adj[edge[0]].Add(new int[] { edge[1], edge[2] });
    }
    public int ShortestPath(int node1, int node2)
    {
        int[] dist = new int[n];
        for (int i = 0; i < n; i++)
        {
            dist[i] = int.MaxValue;
        }
        dist[node1] = 0;
        PriorityQueue<int[], int> pq = new PriorityQueue<int[], int>();
        pq.Enqueue(new int[] { node1, 0 }, 0); //{node,cost},cost。第一个effor用于走到node后直接返回，第二个cost用于priorityQueue的比较
        while (pq.Count > 0)
        {
            int[] curr = pq.Dequeue();
            int u = curr[0];
            int d = curr[1];
            if (u == node2) //关键在于这点，到了这个node就直接返回，省了好多时间
            {
                return d;
            }
            foreach (int[] edge in adj[u])
            {
                int v = edge[0];
                int w = edge[1];
                if (dist[u] + w < dist[v])
                {
                    dist[v] = dist[u] + w;
                    pq.Enqueue(new int[] { v, dist[v] }, dist[v]);
                }
            }
        }
        return -1;
    }
}
```
另外我是来学c++的，所以c++做法：
```c++
//采样区。也是dijkstra，不过比editorial的做法快了不少
class Graph {
public:
    vector<vector<pair<int, int>>> adj_list;
    Graph(int n, vector<vector<int>>& edges) {
        adj_list.resize(n);
        for (auto& e: edges)
            adj_list[e[0]].push_back(make_pair(e[1], e[2]));
    }
    void addEdge(vector<int> e) {
        adj_list[e[0]].push_back(make_pair(e[1], e[2]));
    }
    int shortestPath(int node1, int node2) {
        int n = adj_list.size();
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq; //greater是一个内置函数，可用于比较。greater的template填的是pair<int, int>，于是就比较pair
        vector<int> dist(n, INT_MAX);
        dist[node1] = 0;
        pq.push(make_pair(0, node1));
        while (!pq.empty()) {
            int d = pq.top().first, node = pq.top().second; pq.pop();
            if (node == node2) return d;
            if (d > dist[node]) continue;
            for (auto& neighbor : adj_list[node]) {
                int new_dist = d + neighbor.second;
                if (new_dist < dist[neighbor.first]) {
                    dist[neighbor.first] = new_dist;
                    pq.push(make_pair(new_dist, neighbor.first));
                }
            }
        }
        return -1;
    }
};
```