# [Find the Safest Path in a Grid](https://leetcode.com/problems/find-the-safest-path-in-a-grid)

撸了一个多小时代码结果喜提时间空间均最差，我突然释怀地笑

我的垃圾解法就不放上来了。思路跟着hint走就行，[editorial](https://leetcode.com/problems/find-the-safest-path-in-a-grid/editorial)里就是和hint同思路的解法

但更好的解法是DIJKSTRA算法
```c++
//https://leetcode.com/problems/find-the-safest-path-in-a-grid/solutions/5158873/fastest-100-easy-to-understand-clean-concise
class Solution {
public:
    vector<int> roww = {0,0,-1,1};
    vector<int> coll = {-1,1,0,0};
    //这一大段bfs只是为了初始化各个格子与thief的最近距离
    void bfs(vector<vector<int>>& grid,vector<vector<int>>& score,int n) {
        queue<pair<int, int>> q;
        for(int i = 0; i < n; i++) {
            for(int j = 0; j < n; j++){
                if(grid[i][j]) {
                    score[i][j] = 0;
                    q.push({i, j});
                }
            }
        }
        while(!q.empty()){
            auto t = q.front();
            q.pop();
            int x = t.first, y = t.second;
            int s = score[x][y];
            for(int i =0; i < 4; i++){
                int newX = x + roww[i];
                int newY = y + coll[i];
                if(newX >= 0 && newX < n && newY >= 0 && newY < n && score[newX][newY] > 1 + s) { 
                    score[newX][newY] = 1 + s;
                    q.push({newX, newY});
                }
            }
        }
    }
    int maximumSafenessFactor(vector<vector<int>>& grid) {
        int n = grid.size();
        if(grid[0][0] || grid[n - 1][n - 1]) return 0;
        //score[i][j]数组表示每个格子（i，j）与grid中和自己最近的thief的距离
        vector<vector<int>> score(n,vector<int>(n,INT_MAX));
        bfs(grid, score, n);
        vector<vector<bool>> vis(n, vector<bool>(n, false));
        priority_queue<pair<int,pair<int,int>>> pq;
        //pq默认按照从大到小顺序排序。所以优先考虑distance更大的路径
        pq.push({score[0][0], {0,0}});
        while(!pq.empty()){
            auto temp = pq.top().second;
            //safe是路径中distance最小格子的distance
            auto safe = pq.top().first;
            pq.pop();
            if(temp.first == n - 1 && temp.second == n - 1) return safe;
            vis[temp.first][temp.second] = true;
            for(int i = 0; i < 4; i++) {
                int newX = temp.first + roww[i];
                int newY = temp.second + coll[i];
                if(newX >= 0 && newX < n && newY >= 0 && newY < n && !vis[newX][newY]){
                    int s = min(safe, score[newX][newY]);
                    pq.push({s, {newX, newY}});
                    vis[newX][newY] = true;
                }
            }
        }
        return -1;
    }
};
```
我应该自己多想想的，无脑跟hint不一定是最好的。这DIJKSTRA不比bfs+binary search好撸+快？