# Minimum Path Sum

[题目](https://leetcode.com/problems/minimum-path-sum/description/)

感谢discussion里的好心人，看了他的思路后直接写出和大佬们差不多的代码。

```
The problem statement is to find the minimum path sum from the top-left corner to the bottom-right corner of a grid, where each cell in the grid has a non-negative integer value. The path can only move down or right at each step.

We can use dynamic programming to solve this problem efficiently. We will create a 2D array dp of the same size as the input grid, where each cell dp[i][j] represents the minimum path sum from the top-left corner to cell (i, j).

We can initialize the dp array as follows:

dp[0][0] = grid[0][0] since the minimum path sum to the top-left corner is the value of the top-left cell.
For the first row i=0 and first column j=0 < j < n, the minimum path sum can only be reached by moving right or down from the previous cell. So, we can compute dp[0][j] = dp[0][j-1] + grid[0][j] and dp[i][0] = dp[i-1][0] + grid[i][0] respectively.
For the rest of the cells, we can compute the minimum path sum as follows:
dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1]) since we can reach the current cell from the cell above or the cell to the left, and we want to take the path with the minimum sum.
Once we have filled the dp array, the minimum path sum to the bottom-right corner will be dp[m-1][n-1], where m is the number of rows and n is the number of columns of the input grid.
The time complexity of this approach is O(mn) since we visit each cell once. The space complexity is also O(mn) since we use the dp array to store the intermediate results.
```

```c#
public class Solution {
    public int MinPathSum(int[][] grid) {
        int row=grid.Length;
        int col=grid[0].Length;
        int[,] dp=new int[row,col];
        dp[0,0]=grid[0][0];
        for(int i=1;i<col;i++){
            dp[0,i]=dp[0,i-1]+grid[0][i];
        }
        for(int i=1;i<row;i++){
            dp[i,0]=dp[i-1,0]+grid[i][0];
        }
        for(int i=1;i<row;i++){
            for(int j=1;j<col;j++){
                dp[i,j]=Math.Min(dp[i-1,j]+grid[i][j],dp[i,j-1]+grid[i][j]);
            }
        }
        return dp[row-1,col-1];
    }
}
```

```
Runtime
84 ms
Beats
96.28%
Memory
40.1 MB
Beats
82.33%
```

或者再抠一点，无需新创建一个dp数组，直接用现成的grid。

```c#
//https://leetcode.com/problems/minimum-path-sum/solutions/2677369/recursion-to-space-optimized-in-java/?orderBy=most_votes
class Solution {
    public int MinPathSum(int[][] grid) {
        int m = grid.Length;
        int n = grid[0].Length;
        for(int i=1;i<m;i++)
            grid[i][0] += grid[i-1][0];
        for(int j=1;j<n;j++)
            grid[0][j] += grid[0][j-1];
        for(int i=1;i<m;i++){
            for(int j=1;j<n;j++){
                grid[i][j] += Math.Min(grid[i-1][j], grid[i][j-1]);
            }
        }
        return grid[m-1][n-1];
    }
}
```

```
Runtime
76 ms
Beats
99.53%
Memory
40.2 MB
Beats
82.33%
```

或者保留dp，但是for循环换成递归。

```c#
class Solution {
    int[,] memo;
    public int MinPathSum(int[][] grid) {
        int m = grid.Length;
        int n = grid[0].Length;
        memo = new int[m,n];
        return find(grid, m-1, n-1, memo);
    }
    
    private int find(int[][] grid, int m, int n, int[,] memo){
        if(m==0 && n==0)
            return grid[0][0];
        else if(m<0 || n<0)
            return Int32.MaxValue;
        else if(memo[m,n]!=0)
           return memo[m,n];
        return memo[m,n] = grid[m][n] + Math.Min(find(grid, m-1, n, memo), find(grid, m, n-1, memo));
    }
}
```

```
Runtime
81 ms
Beats
98.14%
Memory
40.5 MB
Beats
50.23%
```

也算是借此题了解了c#里面的[多维数组](https://learn.microsoft.com/zh-cn/dotnet/csharp/programming-guide/arrays/multidimensional-arrays)。适合方的数组（比如此题的grid就是个m\*n数组），那种数组套数组不一样长的就不行了。