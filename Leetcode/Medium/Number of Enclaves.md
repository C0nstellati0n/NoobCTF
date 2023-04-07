# Number of Enclaves

[题目](https://leetcode.com/problems/number-of-enclaves/description/)

这题和昨天的[Number of Closed Islands](./Number%20of%20Closed%20Islands.md)基本一样啊，直接拿来写就完事了。

```c#
class Solution {
    public void dfs(int i, int j, int[][] grid) {
        int m = grid.Length, n = grid[0].Length;
        if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] != 1)
            return;

        grid[i][j] = 0;
        int[] dx = {1, -1, 0, 0};
        int[] dy = {0, 0, 1, -1};

        for(int k=0;k<4;k++){
            int nx = i + dx[k];
            int ny = j + dy[k];
            dfs(nx, ny, grid);
        }
    }
    
    public int NumEnclaves(int[][] grid) {
        int m = grid.Length, n = grid[0].Length;
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                if((i*j==0 || i==m-1 || j==n-1) && (grid[i][j]==1))
                    dfs(i, j, grid);
            }
        }
        
        int count = 0;
        for (int i = 1; i < m-1; i++) {
            for (int j = 1; j < n-1; j++) {
                if (grid[i][j] == 1) {
                    count++;
                }
            }
        }
        return count;
    }
}
````

```
Runtime
159 ms
Beats
89.19%
Memory
62.3 MB
Beats
14.86%
```

大佬们的解法也基本差不多，差别很小，就不多赘述了。