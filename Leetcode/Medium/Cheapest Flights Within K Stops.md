# [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops)

看着挺难（抄之前的dijkstra）->嗯其实还好（wrong answer）->没事我改一下（意识到为什么大家都说难）->润
```c++
//https://leetcode.com/problems/cheapest-flights-within-k-stops/solutions/662812/c-bfs-bellman-ford-algo-dijkstra-algo 评论区 baman9451 评论
//dijkstra
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int K) {
          // create adjacency list
        unordered_map<int,vector<pair<int, int>>> adjList;
        for( auto f : flights )
            adjList[f[0]].push_back( { f[1], f[2] } );
        // minHeap based on cost of distance from source
        priority_queue< vector<int>, vector<vector<int>>, greater<vector<int>> > minHeap;
        minHeap.push( { 0, src, 0 } ); // cost, vertex, hops
        vector<int> dist(n+1, INT_MAX); //to avoid TLE
        while( !minHeap.empty() ) {
            auto t = minHeap.top(); minHeap.pop();
            int cost = t[0];
            int curr = t[1];
            int stop = t[2];
            if( curr == dst )
                return cost;
                //Optimization to avoid TLE
            if(dist[curr]<stop) continue;
            dist[curr]=stop; //我之前做的dijkstra题dist数组里存的是当前路径的权重，这里换成了路径长度
            if(stop >K ) continue;
                for( auto next : adjList[curr] )
                    minHeap.push( { cost+next.second, next.first, stop+1 });
        }
        return -1;
    }
};
```
其实就是普通dijkstra，只是要注意dist数组存放的数值。要是存路径权重就会wrong answer。想知道为什么的可以看这个test case：
```
4
[[0,1,1],[0,2,5],[1,2,1],[2,3,1]]
0
3
1
```
不过这题直接用bfs即可，还更快
```c++
//采样区
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) 
    {
        vector<int>distance(n+1,INT_MAX);
        //this is for setting the distance array with INT_MAX means infinity
        unordered_map<int,vector<pair<int,int>>>adj;//this is for adjacency list
        for(int i=0;i<flights.size();i++)
        {
            int u=flights[i][0];
            int v=flights[i][1];
            int wt=flights[i][2];
            adj[u].push_back({v,wt});//this is for pushing in the adjacency list
        }
        queue<pair<int,int>>q;
        q.push({src,0});//this is for pushing in the queue
        distance[src]=0;
        while(!q.empty()&&k>=0)
        {
            int n=q.size();
            while(n--)
            {
                auto it=q.front();//getting the front of the queue
                int node=it.first;//this is for node
                int dista=it.second;//this is for distance
                q.pop();
                for(auto itr:adj[node])//exploring all its neighbour
                {
                    int nod=itr.first;
                    int di=itr.second;
                    if(di+dista<distance[nod])
                    {
                        distance[nod]=di+dista;
                        q.push({nod,distance[nod]});
                    }
                }
            }
            k--;
        }
        if(distance[dst]>=INT_MAX)
        {
            return -1;
        }
        return distance[dst];
    }
};
```
似乎是多源bfs。这个算法本身就会先从最短的路径检查起，于是distance数组里记路径权重没有问题