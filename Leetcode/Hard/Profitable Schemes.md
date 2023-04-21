# Profitable Schemes

[题目](https://leetcode.com/problems/profitable-schemes/)

dp一生之敌。

```c#
//https://leetcode.com/problems/profitable-schemes/solutions/3439788/image-explanation-memoization-b-up-dp-dp-optimized-c-java-python/
class Solution {
    private int mod = (int)1e9 + 7;
    public int ProfitableSchemes(int n, int minProfit, int[] group, int[] profit) {
        int[,] dp = new int[n + 1,minProfit + 1]; //dp[i,j]表示i个人可获得j profit的数量
        dp[0,0] = 1;
        for (int k = 0; k < group.Length; k++) {
            int g = group[k];
            int p = profit[k];
            for (int i = n; i >= g; i--) {
                for (int j = minProfit; j >= 0; j--) {
                    dp[i,j] = (dp[i,j] + dp[i - g,Math.Max(0, j - p)])%mod;
                }
            }
        }
        int sum = 0;                                                       
        for(int i = 0; i <= n; i++){
            sum = (sum + dp[i,minProfit])%mod;
        }
        return sum;
    }
}
```

```
Runtime
113 ms
Beats
50%
Memory
38.6 MB
Beats
100%
```

大佬们说这是一道类knapsack问题，即判断是否选择某个值。问题是knapsack题我连见也没见过啊。