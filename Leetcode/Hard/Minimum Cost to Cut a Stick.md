# Minimum Cost to Cut a Stick

[题目](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/description/)

为什么最近的dp题答案都给我一种很熟悉的感觉啊？总觉得之前看过很多遍了，每次只是dp数组或者循环有不同的地方。

```c#
//https://leetcode.com/problems/minimum-cost-to-cut-a-stick/solutions/780880/dp-with-picture-burst-balloons/
public class Solution {
    public int MinCost(int n, int[] cuts) {
        List<int> c = new();
        foreach(int cut in cuts)
            c.Add(cut);
        c.AddRange(new List<int>{0,n});
        c.Sort();
        int[,] dp = new int[c.Count,c.Count];
        for (int i = c.Count - 1; i >= 0; --i)
            for (int j = i + 1; j < c.Count; ++j) {
                for (int k = i + 1; k < j; ++k)
                    dp[i,j] = Math.Min(dp[i,j] == 0 ? Int32.MaxValue : dp[i,j],
                        c[j] - c[i] + dp[i,k] + dp[k,j]);
            }
        return dp[0,c.Count - 1];
    }
}
```
```
Runtime
86 ms
Beats
100%
Memory
39.6 MB
Beats
80%
```
递归版本。
```c#
//https://leetcode.com/problems/minimum-cost-to-cut-a-stick/solutions/3570562/image-explanation-recursion-memo-4-states-2-states-bottom-up-c-java-python/
public class Solution {
    int[,] dp;
    int solve(int start_stick, int end_stick, int[] cuts, int left, int right) {
        if (left > right) return 0;
        if (dp[left,right] != 0) return dp[left,right];
        int cost = Int32.MaxValue;
        for (int i = left; i <= right; i++) {
            int left_cost = solve(start_stick, cuts[i], cuts, left, i - 1);
            int right_cost = solve(cuts[i], end_stick, cuts, i + 1, right);
            int curr_cost = (end_stick - start_stick) + left_cost + right_cost;
            cost = Math.Min(cost, curr_cost);
        }
        return dp[left,right] = cost;
    }
    public int MinCost(int n, int[] cuts) {
        dp = new int[cuts.Length,cuts.Length];
        Array.Sort(cuts);
        return solve(0, n, cuts, 0, cuts.Length - 1);
    }
}
```
```
Runtime
126 ms
Beats
40%
Memory
39.1 MB
Beats
100%
```
发现一个把解法讲得比较详细的帖子：https://leetcode.com/problems/minimum-cost-to-cut-a-stick/solutions/1395121/4-minutes-read-simple-no-brainer-recursion-memoization/ ，还有个关于怎么把递归转成记忆递归的bonus，可以看一下。