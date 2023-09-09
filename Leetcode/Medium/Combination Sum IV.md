# Combination Sum IV

[题目](https://leetcode.com/problems/combination-sum-iv)

但凡我用5分钟想一下dp关系就做出来了。
```c#
//https://leetcode.com/problems/combination-sum-iv/solutions/4020218/98-22-dynamic-programming-recursion-with-memoization
//难得遍历比递归好理解的题
public class Solution {
    public int CombinationSum4(int[] nums, int target) {
        int[] dp=new int[target+1]; //定义dp[i]:使用nums凑成i的方式的个数
        dp[0]=1; //base case
        for(int i=1;i<=target;i++){
            foreach(int num in nums){
                if(i-num>=0){
                    dp[i]+=dp[i-num]; //dp[i]=已知可以构成i的方式的个数+减去这次选择的num后能构成i-num的方式的个数
                }
            }
        }
        return dp[target];
    }
}
```
```
Runtime
74 ms
Beats
85.6%
Memory
38.4 MB
Beats
21.84%
```