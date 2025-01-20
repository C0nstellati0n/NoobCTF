# [Minimum Obstacle Removal to Reach Corner](https://leetcode.com/problems/minimum-obstacle-removal-to-reach-corner)

这题的hint可能是最有用的hint之一。立刻把毫无头绪的hard转换成medium
```c++
class Solution {
public:
    int minimumObstacles(vector<vector<int>>& grid) {
        vector<vector<int>> d(grid.size(),vector<int>(grid[0].size(),2*1e5));
        vector<vector<int>> adj{{0,1},{1,0},{0,-1},{-1,0}};
        d[0][0] = 0;
        deque<pair<int, int>> q;
        q.push_front({0,0});
        while (!q.empty()) {
            auto [i,j] = q.front();
            q.pop_front();
            for (const auto& edge : adj) {
                int u = i+edge[0];
                int w = j+edge[1];
                if(u<0||u>=grid.size()||w<0||w>=grid[0].size()) continue;
                if (d[i][j] + grid[u][w] < d[u][w]) {
                    d[u][w] = d[i][j] + grid[u][w];
                    if (grid[u][w] == 1)
                        q.push_back({u,w});
                    else
                        q.push_front({u,w});
                }
            }
        }
        return d[grid.size()-1][grid[0].size()-1];
    }
};
```
hint提到了0-1 Breadth-First Search，于是在网上搜了相关内容。将 https://cp-algorithms.com/graph/01_bfs.html 里的算法改动一下即可

原理和Dijkstra一样，优先考虑当前最佳edge，即权重最小的edge。不过相比于Dijkstra使用的priority queue，这里一个deque就够了。因为面对的graph只有0和1两种权重，把0权重的放前面，1权重的放后面，这样同样可以做到“先考虑低权重的edge”。priority queue的排序在这里毫无意义。这样看来，只要图中只有两种权重，都可以这么用

最后是采样区里一种更快的写法
```c++
class Solution {
public:
    int minimumObstacles(vector<vector<int>>& grid) {
        int n = grid.size(),m=grid[0].size();
        int dp[n][m];
        memset(dp,-1,sizeof(dp));
        dp[0][0] = grid[0][0];
        int dx[] ={1,-1,0,0};
        int dy[] ={0,0,1,-1};
        queue<pair<int,int>> q,q1; //看来两个queue要比单独deque快
        q.push({0,0});
        while(!q.empty()){
            pair<int,int> p = q.front();
            q.pop();
            for(int i=0;i<4;i++){
                int x = p.first+dx[i],y=p.second+dy[i];
                if(x>=0&&x<n&&y>=0&&y<m&&dp[x][y]==-1){ //注意这个写法不适用于全部题目，仅在这道题内每个坐标(x,y)第一次访问时就是最佳路径。其他时候还是要用类似 d[i][j] + grid[u][w] < d[u][w] 的判断
                    dp[x][y] = dp[p.first][p.second] + grid[x][y];
                    if(grid[x][y]){ //模拟deque的操作
                        //q1装优先级较低的edge
                        q1.push({x,y});
                    }
                    else
                    {
                        //q装优先级较高的edge
                        q.push({x,y});
                    }
                }
            }
            if(q.empty()){
                swap(q,q1);
            }
        }
        return dp[n-1][m-1];
    }
};
```