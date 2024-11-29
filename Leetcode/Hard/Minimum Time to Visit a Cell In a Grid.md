# [Minimum Time to Visit a Cell In a Grid](https://leetcode.com/problems/minimum-time-to-visit-a-cell-in-a-grid)

```c++
//采样区
class Solution {
public:
    int minimumTime(vector<vector<int>>& grid) {     
        int m = grid.size();
        int n = grid[0].size();
        vector<int> visited(m * n, -1);
        //和多源bfs差不多，只是queue变成priority_queue
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> q; //自己写的时候忘记加greater了，直接从“优先考虑时间最短路径”变成“优先考虑时间最长路径”……反向优化了属于是
        q.push({0,0});
        visited[0] = 0;
        vector<int> dir = {0, -1, 0, 1, 0};
        if(grid[1][0] > 1 && grid[0][1] > 1)
            return -1;
        while(q.size() > 0){ 
            auto node = q.top();
            q.pop();
            int row = node.second / n; //这样应该比直接储存坐标更快
            int col = node.second % n;
            int val = node.second;
            int t = node.first;        
            if(row == m - 1 && col == n-1)
            {
                return t;
            }
            for(int j = 0 ; j < 4 ; j++){
                int new_row = row + dir[j];
                int new_col = col + dir[j + 1];
                if(new_row < 0 || new_row >= m || new_col < 0 || new_col >= n)
                    continue;  
                int val = new_row * n + new_col;
                if(visited[val] != -1)
                    continue;
                if(grid[new_row][new_col] <= t + 1)
                    visited[val] = t + 1;
                else if((t + 1) % 2 != grid[new_row][new_col] % 2)
                    visited[val] = grid[new_row][new_col] + 1;
                else
                    visited[val] = grid[new_row][new_col];
                q.push({visited[val], val});  
            }
        }
        return -1; 
    }
};
```
会发现这个dijkstra没有dist，一个visited就足够了。和之前见过的“原版”dijkstra比对了一下，发现两者的不同点是，原版适用于任意graph，这个则是针对grid做的优化。感觉也能看出来，grid+priority_queue的情况下，第一次走到某个格子的路径一定是最短的。不像普通graph这样：假设a到b有两条路径；路径一由较小权重的edge拼成，路径二只有一条edge，但这条edge的权重比组成路径一的各个edge的权重都大。priority_queue会先考虑路径一，但并不意味着路径一的权重和就小于路径二