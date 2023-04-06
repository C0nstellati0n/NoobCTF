# Number of Closed Islands

[题目](https://leetcode.com/problems/number-of-closed-islands/)

找出图表中岛的数量。题目要求岛的四周都是水，因此边缘肯定不会出现岛。图表题+遍历肯定想到bfs/dfs，但是我脑子卡了，没有临接表不知道怎么访问邻居了。而且还不知道怎么处理碰到边缘的岛。

```c#
//https://leetcode.com/problems/number-of-closed-islands/solutions/3384770/image-explanation-clean-generalized-code-c-java-python/
class Solution {
    public void dfs(int i, int j, int[][] grid) {
        int m = grid.Length, n = grid[0].Length;
        if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] != 0)
            return;

        grid[i][j] = 1;//既代表水，又代表是否访问过
        int[] dx = {1, -1, 0, 0}; //邻居，任意一个方格的可能邻居为上下左右
        int[] dy = {0, 0, 1, -1};

        for(int k=0;k<4;k++){
            int nx = i + dx[k];
            int ny = j + dy[k];
            dfs(nx, ny, grid);
        }
    }
    
    public int ClosedIsland(int[][] grid) {
        int m = grid.Length, n = grid[0].Length;
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                if((i*j==0 || i==m-1 || j==n-1) && (grid[i][j]==0)) //先从边缘开始遍历，把任何接着边缘的岛排除掉
                    dfs(i, j, grid);
            }
        }
        
        int count = 0;
        for (int i = 1; i < m-1; i++) {
            for (int j = 1; j < n-1; j++) {
                if (grid[i][j] == 0) {
                    dfs(i, j, grid);
                    count++;//前面已经排除边缘的情况了，剩下的就是遍历中间的所有岛，数出数量了
                }
            }
        }
        return count;
    }
}
```

```
Runtime
91 ms
Beats
90%
Memory
42.9 MB
Beats
```

或者我们省略最开始边缘的for循环，全部放在一起执行。

```c#
//https://leetcode.com/problems/number-of-closed-islands/solutions/3384821/python3-c-java-easy-and-understand-dfs-solution-beats-100/
class Solution {
    public int ClosedIsland(int[][] grid) {
        int rows = grid.Length, cols = grid[0].Length, count = 0;
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == 0 && dfs(grid,i, j)) {
                    count++;
                }
            }
        }
        
        return count;
    }
    public bool dfs(int[][] grid,int i, int j) {
        int rows = grid.Length, cols = grid[0].Length;
        if (i < 0 || j < 0 || i >= rows || j >= cols) {
            return false;
        }
        if (grid[i][j] == 1) {
            return true;
        }
        grid[i][j] = 1; // mark as visited
        bool left = dfs(grid,i, j-1), right = dfs(grid,i, j+1);//岛是否和边缘连着这里已经检查了
        bool up = dfs(grid,i-1, j), down = dfs(grid,i+1, j);
        return left && right && up && down;
    }
}
```

```
Runtime
91 ms
Beats
90%
Memory
40.8 MB
Beats
78.57%
```

有人说在算法内部修改传入的参数不是一个好的习惯。没事，我们也可以用visited数组记录。

```c#
//https://leetcode.com/problems/number-of-closed-islands/solutions/3384860/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    public int ClosedIsland(int[][] grid) {
        int m = grid.Length; // number of rows in the grid
        int n = grid[0].Length; // number of columns in the grid
        int count = 0; // counter to keep track of number of closed islands
        bool[,] visited = new bool[m,n]; // to keep track of visited cells
        
        // loop through all cells, skipping the border cells
        for (int i = 1; i < m - 1; i++) {
            for (int j = 1; j < n - 1; j++) {
                if (grid[i][j] == 0 && !visited[i,j]) { // if this is an unvisited land cell
                    bool isClosed = dfs(grid, visited, i, j); // check if it is a closed island
                    if (isClosed) {
                        count++; // increment the counter if it is a closed island
                    }
                }
            }
        }
        return count; // return the number of closed islands
    }
    
    private bool dfs(int[][] grid, bool[,] visited, int i, int j) {
        int m = grid.Length; // number of rows in the grid
        int n = grid[0].Length; // number of columns in the grid
        if (i < 0 || i >= m || j < 0 || j >= n) { // if out of bounds, not a closed island
            return false;
        }
        if (visited[i,j]) { // if already visited, not a closed island
            return true;
        }
        visited[i,j] = true; // mark as visited
        if (grid[i][j] == 1) { // if water, not a closed island
            return true;
        }
        bool isClosed = true; // flag to check if all adjacent cells are water (closed island)
        isClosed &= dfs(grid, visited, i - 1, j); // check the cell to the left
        isClosed &= dfs(grid, visited, i + 1, j); // check the cell to the right
        isClosed &= dfs(grid, visited, i, j - 1); // check the cell above
        isClosed &= dfs(grid, visited, i, j + 1); // check the cell below
        return isClosed; // return whether all adjacent cells are water (closed island)
    }
}
```

```
Runtime
89 ms
Beats
95.71%
Memory
40.7 MB
Beats
87.14%
```