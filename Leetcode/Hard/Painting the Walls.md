# [Painting the Walls](https://leetcode.com/problems/painting-the-walls)

如果明天还是hard我将原地爆炸。
```c#
//https://leetcode.com/problems/painting-the-walls/solutions/3650707/java-c-python-7-lines-knapsack-dp
public class Solution {
    public int PaintWalls(int[] cost, int[] time) {
        int n = cost.Length;
        int [] dp = new int[n + 1]; //定义dp[i]=c：paint i个wall需要的最少cost为c
        Array.Fill(dp, (int)1e9);
        dp[0] = 0; //base case：0个wall cost自然是0
        for (int i = 0; i < n; ++i)
            for (int j = n; j > 0; --j)
            //当我们用cost[i]雇佣一个painter时，需要time[i]。同时可以用free painter刷time[i]个wall，因为free painter固定一个时间单位一面墙。总共就是time[i]+1个wall
            //dp equation：dp[j] = min(dp[j], dp[max(j - time[i] - 1, 0)] + cost[i]) 。max(j - time[i] - 1, 0)是为了防止索引小于0的情况，反正小于0面墙cost也是0
                dp[j] = Math.Min(dp[j], dp[Math.Max(j - time[i] - 1, 0)] + cost[i]);
        return dp[n];
    }
}
```
```
Runtime
82 ms
Beats
100%
Memory
55.4 MB
Beats
81.82%
```
这题[editorial](https://leetcode.com/problems/painting-the-walls/editorial)和lee佬讲解的不大一样。关键的dp equation是一样的，但是对dp的定义不同，导致实现起来不同。还是lee佬的好理解，空间也最少。