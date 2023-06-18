# Number of Increasing Paths in a Grid

[题目](https://leetcode.com/problems/number-of-increasing-paths-in-a-grid/description/)

我是如何判断一道hard题有多难的：抄的答案多久能看懂。根据这个评判标准，这题属于相对没那么难的hard题。
```c#
//https://leetcode.com/problems/number-of-increasing-paths-in-a-grid/solutions/3650111/java-c-python-solution-easy-to-understand/
class Solution {
    int mod = (int)(1e9+7);
    public int CountPaths(int[][] grid) {
        int n = grid.Length;
        int m = grid[0].Length;
        
        int[][] dp = new int[n][];
        for(int i=0;i<n;i++){
            int[] temp=new int[m];
            Array.Fill(temp, -1);
            dp[i]=temp;
        }
        int paths = 0;
        for(int i=0; i<n; i++){
            for(int j=0; j<m; j++){
                paths = (paths+solve(grid, i, j, -1, dp))%mod;
            }
        }
        
        return paths;
    }
    
    public int solve(int[][] grid, int i, int j, int prev, int[][] dp){
        if(i<0 || j<0 || i>=grid.Length || j>=grid[0].Length || grid[i][j]<=prev){
            return 0;
        }
        
        if(dp[i][j]!=-1){
            return dp[i][j];
        }
        
        int left = solve(grid, i, j-1, grid[i][j], dp);
        int right = solve(grid, i, j+1, grid[i][j], dp);
        int up = solve(grid, i-1, j, grid[i][j], dp);
        int down = solve(grid, i+1, j, grid[i][j], dp);
        
        return dp[i][j] = (1+left+right+up+down)%mod;
    }
}
```
```
Runtime
293 ms
Beats
80%
Memory
72.5 MB
Beats
40%
```
最开始看了hint后知道要用dfs+dp。但是hint对dp的提示把我看懵了。
```
Define f(i, j) as the number of increasing paths starting from cell (i, j). Try to find how f(i, j) is related to each of f(i, j+1), f(i, j-1), f(i+1, j) and f(i-1, j).
```
假如跟着hint思路走的话，f(i, j)与f(i, j+1), f(i, j-1), f(i+1, j) 和 f(i-1, j)的关系肯定是它们加起来后再加1。然后我就被自己绕晕了。假如我从f(i, j)开始，我怎么知道f(i, j+1)等还没遍历到的方格里的值？而且dp+递归肯定有个初始值或者base case吧，是啥？最开始想的是dp初始为1，因为题目允许有长度为1的路径，那从每个方格开始都至少有1。总之最后也没实现成功，就是想不出来怎么知道还没遍历到的方格里的值。事实证明我真的不懂dp和递归，它就是自己递归到那里就出来了，因为最后的return一句默认加了个1，也就是说已经有有初始值（dp也不用全初始化为1了）了。把每个i和j都遍历一次，然后加在一起自然就是答案了。

接下来是采样里稍微快点的dp+dfs。
```c#
public class Solution {
    int[][] dp;
    int[][] directions = { new int[] { 0, 1 }, new int[] { 0, -1 }, new int[] { 1, 0 }, new int[] { -1, 0 } };
    int mod = 1_000_000_007;
    int DFS(int[][] grid, int i, int j)
    {
        if (dp[i][j] != 0) return dp[i][j];
        int answer = 1;
        foreach (int[] d in directions) {
            int prevI = i + d[0], prevJ = j + d[1];
            if (0 <= prevI && prevI < grid.Length && 0 <= prevJ &&
                prevJ < grid[0].Length && grid[prevI][prevJ] < grid[i][j]) {
                answer += DFS(grid, prevI, prevJ);
                answer %= mod;
            }
        }
        dp[i][j] = answer;
        return answer;
    }
    public int CountPaths(int[][] grid) {
        int m = grid.Length, n = grid[0].Length;
        dp = new int[m][];
        for (int i = 0; i < m; i++) dp[i] = new int[n];
        int answer = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                answer = (answer + DFS(grid, i, j)) % mod;
            }
        }
        return answer;
    }
}
```
```
Runtime
272 ms
Beats
100%
Memory
62.9 MB
Beats
80%
```
不用递归用bfs也是可以的。
```c#
//https://leetcode.com/problems/number-of-increasing-paths-in-a-grid/solutions/2230147/python-topo-dp-solution-and-dfs-solution/
//在地下的评论区里
class Solution {
         public int CountPaths(int[][] grid)
    {
        long res = 0;
        long mod = 1_000_000_007;
        int m = grid.Length;
        int n = grid[0].Length;
        long[][] dp = new long[m][];
        for (int i = 0; i < m; i++)
        {
            dp[i] = new long[n];
            Array.Fill(dp[i], 1);//base case of every node is 1 , aka this node is smaller than all neighbors
        }
        //minHeap, traversal all nodes from smallest to biggest
        PriorityQueue<int[], int> pq = new PriorityQueue<int[], int>();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                pq.Enqueue(new int[] { i, j }, grid[i][j]);
        int[][] dxy4 = new int[4][] { new int[] { 1, 0 }, new int[] { -1, 0 }, new int[] { 0, 1 }, new int[] { 0, -1 } };
        while (pq.Count > 0)
        {
            var curr = pq.Dequeue();
            foreach (var d in dxy4)
            {
                int r = curr[0] + d[0];
                int c = curr[1] + d[1];
                if (r >= 0 && r < m && c >= 0 && c < n && grid[r][c] > grid[curr[0]][curr[1]])
                    dp[r][c] = (dp[r][c] + dp[curr[0]][curr[1]]) % mod;
            }
        }
        foreach (var row in dp)
            foreach (var cell in row)
                res = (res + cell) % mod;
        return (int)res;
    }
}
```
```
Runtime
480 ms
Beats
40%
Memory
62.1 MB
Beats
100%
```