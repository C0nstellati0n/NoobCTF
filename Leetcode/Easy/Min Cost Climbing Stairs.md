# [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs)

难得有个easy+完整hint的dp题
```c#
public class Solution {
    public int MinCostClimbingStairs(int[] cost) {
        int[] dp=new int[cost.Length+2];
        for(int i=cost.Length-1;i>=0;i--){
            dp[i]=cost[i]+Math.Min(dp[i+1],dp[i+2]);
        }
        return Math.Min(dp[0],dp[1]);
    }
}
```
```
Runtime
75 ms
Beats
89.77%
Memory
39.8 MB
Beats
67.29%
```
内存优化版本：
```c#
//https://leetcode.com/problems/min-cost-climbing-stairs/solutions/476388/4-ways-step-by-step-from-recursion-top-down-dp-bottom-up-dp-fine-tuning
public class Solution {
    public int MinCostClimbingStairs(int[] cost) {
        int n = cost.Length;
        int first = cost[0];
        int second = cost[1];
        if (n<=2) return Math.Min(first, second);
        for (int i=2; i<n; i++) {
            int curr = cost[i] + Math.Min(first, second);
            first = second;
            second = curr;
        }
        return Math.Min(first, second);
    }
}
```
```
Runtime
62 ms
Beats
99.86%
Memory
39.1 MB
Beats
99.71%
```