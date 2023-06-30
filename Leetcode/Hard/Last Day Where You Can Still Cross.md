# Last Day Where You Can Still Cross

[题目](https://leetcode.com/problems/last-day-where-you-can-still-cross/description/)

提示有两个：
1. What graph algorithm allows us to find whether a path exists?
2. Can we use binary search to help us solve the problem?

第一个提示，我脑子里冒出的第一个答案是bfs。对的。好来看第二个：binary search？啊？我从来没听过bfs里能缝binary search来加速啊？最后看editorial，哦，不是在bfs里缝啊。
```c#
//https://leetcode.com/problems/last-day-where-you-can-still-cross/editorial/
class Solution {
    private int[][] directions = new int[][]
    {
        new int[]{1, 0}, 
        new int[]{-1, 0}, 
        new int[]{0, 1}, 
        new int[]{0, -1}
    };
    public bool canCross(int row, int col, int[][] cells, int day) {
        int[,] grid = new int[row,col];
        Queue<int[]> queue = new();
        
        for (int i = 0; i < day; i++) {
            grid[cells[i][0] - 1,cells[i][1] - 1] = 1; //根据天数判断哪些方格应该为水（1）
        }
        
        for (int i = 0; i < col; i++) { //从最上层出发，将最上层所有的格子入队列
            if (grid[0,i] == 0) {
                queue.Enqueue(new int[]{0, i});
                grid[0,i] = -1; //标-1表示已经走过了，省个visited数组
            }
        }

        while (queue.Count!=0) {
            int[] cur = queue.Dequeue();
            int r = cur[0], c = cur[1];
            if (r == row - 1) {
                return true;
            }
            
            foreach(int[] dir in directions) {
                int newRow = r + dir[0];
                int newCol = c + dir[1];
                if (newRow >= 0 && newRow < row && newCol >= 0 && newCol < col && grid[newRow,newCol] == 0) {
                    grid[newRow,newCol] = -1;
                    queue.Enqueue(new int[]{newRow, newCol});
                }
            }
        }
        return false;
    }
    
    public int LatestDayToCross(int row, int col, int[][] cells) {
        int left = 1;
        int right = row * col;
        
        while (left < right) {
            int mid = right - (right - left) / 2;
            if (canCross(row, col, cells, mid)) {
                left = mid;
            } else {
                right = mid - 1;
            }
        } 
        return left;
    }
}
```
```
Runtime
445 ms
Beats
41.18%
Memory
61.8 MB
Beats
70.59%
```
算法本身挺好理解的。每天都会有一个陆地格子转为水格子，也就是说每天的grid都不一样。bfs可以找到一条从上到下的路，然而如果对每天的grid都来次bfs，结果肯定TLE。有没有什么办法少执行几次bfs？这就要请出binary search了。我们知道，假如第i天没有路走，那第i+1天自然也没有路走；若第i天能走，第i-1天自然也能走。很明显的binary search特征，这回就不会TLE了。我最开始以为binary search放到bfs里面加速运行，自己把自己坑了。

所以有bfs怎么能没有dfs呢？
```c#
class Solution {
    private int[][] directions = new int[][]
    {
        new int[]{1, 0}, 
        new int[]{-1, 0}, 
        new int[]{0, 1}, 
        new int[]{0, -1}
    };
    public bool canCross(int row, int col, int[][] cells, int day) {
        int[,] grid = new int[row,col];
        for (int i = 0; i < day; ++i) {
            int r = cells[i][0] - 1, c = cells[i][1] - 1;
            grid[r,c] = 1;
        }
        
        for (int i = 0; i < day; ++i) {
            grid[cells[i][0] - 1,cells[i][1] - 1] = 1;
        }
        
        for (int i = 0; i < col; ++i) {
            if (grid[0,i] == 0 && dfs(grid, 0, i, row, col)) {
                return true;
            }
        }
        return false;
        
    }

    private bool dfs(int[,] grid, int r, int c, int row, int col) {
        if (r < 0 || r >= row || c < 0 || c >= col || grid[r,c] != 0) {
            return false;
        }
        if (r == row - 1) {
            return true;
        }
        grid[r,c] = -1;
        foreach(int[] dir in directions) {
            int newR = r + dir[0], newC = c + dir[1];
            if (dfs(grid, newR, newC, row, col)) {
                return true;
            }
        }
        return false;
    }

    public int LatestDayToCross(int row, int col, int[][] cells) {
        int left = 1, right = row * col;
        while (left < right) {
            int mid = right - (right - left) / 2;
            if (canCross(row, col, cells, mid)) {
                left = mid;
            } else {
                right = mid - 1;
            }
        }
        return left;
    }
}
```
```
Runtime
377 ms
Beats
94.12%
Memory
61.1 MB
Beats
70.59%
```
最后是union find。union find又有两种做法：连接陆地格还是水格。这个还是看editorial较好，那里有图。