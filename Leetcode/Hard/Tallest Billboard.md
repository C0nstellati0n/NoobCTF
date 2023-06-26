# Tallest Billboard

[题目](https://leetcode.com/problems/tallest-billboard/description/)

阴间hard题。
```c#
//https://leetcode.com/problems/tallest-billboard/solutions/3529313/solution/
class Solution {
    public int TallestBillboard(int[] rods) {
        int sum = 0;
        foreach(int rod in rods) {
            sum += rod;
        }
        int[,] dp = new int[rods.Length + 1,sum + 1];
        for (int i = 1; i <= rods.Length; i++) {
            for (int j = 0; j <= sum; j++) {
                if (dp[i - 1,j] < j) {
                    continue;
                }
                dp[i,j] = Math.Max(dp[i,j], dp[i - 1,j]);
                int k = j + rods[i - 1];
                dp[i,k] = Math.Max(dp[i,k], dp[i - 1,j] + rods[i - 1]);
                k = Math.Abs(j - rods[i - 1]);
                dp[i,k] = Math.Max(dp[i,k], dp[i - 1,j] + rods[i - 1]);
            }
        }
        return dp[rods.Length,0] / 2;
    }
}
```
```
Runtime
92 ms
Beats
97.62%
Memory
41.8 MB
Beats
95.24%
```
换个有解释的solution。这题的关键在于dp数组的索引表示的是“一组棍子的差值”，那么dp[i]表示的就是“一组差值为i的棍子中最高的那个”
```c#
//https://leetcode.com/problems/tallest-billboard/solutions/203181/java-c-python-dp-min-o-sn-2-o-3-n-2-n/
public class Solution {
    public int TallestBillboard(int[] rods) {
        int[] dp = new int[5001];
        for (int d = 1; d < 5001; d++) dp[d] = -10000;
        foreach(int x in rods) {
            int[] cur = (int[])dp.Clone();
            for (int d = 0; d + x < 5001; d++) {
                dp[d + x] = Math.Max(dp[d + x], cur[d]);
                dp[Math.Abs(d - x)] = Math.Max(dp[Math.Abs(d - x)], cur[d] + Math.Min(d, x));
            }
        }
        return dp[0];
    }
}
```
```
Runtime
110 ms
Beats
85.71%
Memory
56.6 MB
Beats
53.57%
```
还有说当成knapsack问题来解的大佬。
```c#
//https://leetcode.com/problems/tallest-billboard/solutions/203261/java-knapsack-o-n-sum/
class Solution {
    public int TallestBillboard(int[] rods) {
		// For each rod r, 
        // we can:
        //     add (dp[i+r], means add to right side), 
        //     minus (dp[i-r], means add to left side), 
        //     or no ops (not using that rod)
		// The meaning of dp[i] = val: 
		// stands for after arrange (add rod to left, add rod to right, or not using the rod )the rods, 
        // we have arranged_sum == i, and at the same time, the total sum of using those rods equals val.
        //     if i > 0 it means the right is taller then left. 
        //     if i < 0 it means the left is taller then right.
        //     if i == 0 it means left and right are even height.
        
        // Our target is to get dp[0], which means the left side and right side are of equal length.
        // However, we want to represent the dp as an array. Thus we offset the dp[0] to dp[5000]. (range from -5000~ +5000, and offset -5000 to zero. Thus totally 10001)
        int[] dp=new int[10001];
        Array.Fill(dp,-1);
        dp[5000] = 0;
        foreach(int r in rods){
            int[] dp2 = (int[])dp.Clone();
            for(int i = 0; i<dp.Length; i++){
                if(dp[i]<0) continue;
                // add rod to left side.
                dp2[i-r] = Math.Max(dp2[i-r], dp[i]+r); //这里测试发现i-r可能是个负数，c#里又没有负索引，这是怎么做到的？
                // add rod to right side.
                dp2[i+r] = Math.Max(dp2[i+r], dp[i]+r);
                // note that no ops is considered implicitly by copying the dp2 = dp.
            }
            (dp,dp2)=(dp2,dp); //原来c#里也可以像python一样直接交换
        }
        return dp[5000]/2;
    }
}
```
```
Runtime
93 ms
Beats
96.43%
Memory
56.4 MB
Beats
54.76%
```