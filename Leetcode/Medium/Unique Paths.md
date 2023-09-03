# Unique Paths

[题目](https://leetcode.com/problems/unique-paths/)

我说怎么这么眼熟，原来我早就做过[Unique Paths II](./Unique%20Paths%20II.md)了。好，那就在这里实现我不看任何提示(看之间的笔记不算……吧？)独自写出dp的愿望吧。
```c#
public class Solution {
    public int UniquePaths(int m, int n) {
        int[,] dp=new int[m,n];
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                if(j==0||i==0){
                    dp[i,j]=1;
                }
                if(j-1>=0&&i-1>=0){
                    dp[i,j]=dp[i,j-1]+dp[i-1,j];
                }
                else if(j-1>=0){
                    dp[i,j]=dp[i,j-1];
                }
                else if(i-1>=0){
                    dp[i,j]=dp[i-1,j];
                }
            }
        }
        return dp[m-1,n-1];
    }
}
```
```
Runtime
16 ms
Beats
94.47%
Memory
26.8 MB
Beats
64.6%
```
空间优化+数学做法（基本是所有解法的集合）： https://leetcode.com/problems/unique-paths/solutions/1581998/c-python-5-simple-solutions-w-explanation-optimization-from-brute-force-to-dp-to-math/