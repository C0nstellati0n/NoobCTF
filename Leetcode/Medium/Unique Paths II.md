# Unique Paths II

[题目](https://leetcode.com/problems/unique-paths-ii/description/)

hint给出dp状态间的关系后我直接冲了遍历做法，十分钟结束。
```c#
public class Solution {
    public int UniquePathsWithObstacles(int[][] obstacleGrid) {
        if(obstacleGrid[0][0]==1){
            return 0;
        }
        int[,] dp=new int[obstacleGrid.Length,obstacleGrid[0].Length];
        dp[0,0]=1;
        for(int i=0;i<obstacleGrid.Length;i++){
            for(int j=0;j<obstacleGrid[0].Length;j++){
                if(j-1>=0&&i-1>=0){
                    dp[i,j]=dp[i,j-1]+dp[i-1,j];
                }
                else if(j-1>=0){
                    dp[i,j]=dp[i,j-1];
                }
                else if(i-1>=0){
                    dp[i,j]=dp[i-1,j];
                }
                if(obstacleGrid[i][j]==1){
                    dp[i,j]=0;
                }
            }
        }
        return dp[obstacleGrid.Length-1,obstacleGrid[0].Length-1];
    }
}
```
```
Runtime
74 ms
Beats
94.28%
Memory
38.6 MB
Beats
63.25%
```
https://leetcode.com/problems/unique-paths-ii/solutions/23250/short-java-solution/ 是空间优化做法，从二维dp转为只用一维dp。 https://leetcode.com/problems/unique-paths-ii/solutions/23410/python-different-solutions-o-m-n-o-n-in-place/ 还有个直接用obstacleGrid当dp的，space可能是O(1)?

连续两天dp没抄答案了，难道我要学会dp了？不过dp最关键的“关系”我是看hint的，好吧四舍五入等于啥也不会。