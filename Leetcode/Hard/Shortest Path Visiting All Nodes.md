# Shortest Path Visiting All Nodes

[题目](https://leetcode.com/problems/shortest-path-visiting-all-nodes)

bitmask+bfs。如果之前接触过的话理解答案倒不难，问题在于真让我自己写的话bug能堆到天上去。
```c#
//https://leetcode.com/problems/shortest-path-visiting-all-nodes/solutions/549233/breadth-first-search-bfs-with-intuitive-approach-thinking-process-13-ms
class Solution {
    public int ShortestPathLength(int[][] graph) {
        Dictionary<int, List<int>> hm = new();
        int n = graph.Length;
        // Adjency list of graph
        for(int i=0;i<n;i++){
            if(!hm.ContainsKey(i)){
                hm[i]=new();
            }
            int m = graph[i].Length;
            for(int j=0;j<m;j++){
                hm[i].Add(graph[i][j]);
            }
        }
        //dist 2d array
        //row: bitmask -> visited node set bits are 1
        //column: leading node
        int row = (int)Math.Pow(2,n);
        int col = n;
        int[,] dist = new int[row,col];
        for(int i=0;i<row;i++){
            for(int j=0;j<col;j++){
                dist[i,j]=-1;
            }
        }
        //Queue: [{leading node 1, mask},{leading node 2, mask} ... ]
        Queue<int[]> q = new();
        for(int i=0;i<n;i++){
            int lead = i;
            int mask = setbit(0,i);
            q.Enqueue(new int[]{lead, mask}); //这个bfs的特殊点之一在于它的起始点不止一个，而是全部可能的node
            dist[mask,lead] = 0;
        }
        // Applying simulatneous BFS
        while(q.Count>0){  
            int size = q.Count;
            for(int i=0;i<size;i++){   
                int[] path = q.Dequeue();  
                int lead = path[0];
                int mask = path[1];
                if(mask == row-1){   //all nodes visited
                    return dist[mask,lead];
                }
                // iterate over neighbours of lead
                if(hm.ContainsKey(lead)){
                    foreach(int child in hm[lead]){
                        int newlead = child;
                        int newmask = setbit(mask, newlead);
                        // avoid cycle: intelligent bfs : checking if this set is already visited 
                        // set : lead, mask(visited nodes)
                        if(dist[newmask,newlead]!=-1){
                            continue;
                        }
                        dist[newmask,newlead] = dist[mask,lead]+1;
                        q.Enqueue(new int[]{newlead, newmask});
                    }
                }   
            }   
        }
        return -1;   
    }
    int setbit(int mask, int i){
        return mask|(1<<i);
    }
}
```
```
Runtime
73 ms
Beats
100%
Memory
44.7 MB
Beats
50%
```
可怜的bfs天天被改造，主要是普通bfs没法访问同一个node两次。巧了，这题不访问一个node两次就做不出来。要求找到连通所有node地最短路径，但是可以在任何node回头并访问同一个node多次。这样的问题见过很多遍了，只需考虑两个问题：
1. 何时允许访问同一个node多次？
2. 怎样记录node被访问的状态？

对于这题，答案如下：
1. 当mask和当前被访问的node的组合之前没出现过时
2. 用bitmask+node的组合

这题还有个特别的地方，就是起始node的选择会影响路径的长度。无论从哪个node开始都能找到一条路径，但是不是最短的可就不知道了。解决办法也很简单粗暴，反正我不知道从哪里开始，那就从任何可能的地方开始吧。contraint提示我们n最大才12，也算是个对bitmask+爆破起始点的提示。