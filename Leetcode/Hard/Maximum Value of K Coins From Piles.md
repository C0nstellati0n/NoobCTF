# Maximum Value of K Coins From Piles

[题目](https://leetcode.com/problems/maximum-value-of-k-coins-from-piles/description/)

我是一个没有灵魂的抄答案机器。第一种是递归版。

```c#
//https://leetcode.com/problems/maximum-value-of-k-coins-from-piles/solutions/3417959/image-explanation-top-down-dp-easy-concise-c-java-python/
public class Solution {
    public int func(int i, int k, IList<IList<int>> piles, int[,] dp) {
        if (dp[i,k] > 0) return dp[i,k];
        if (i == piles.Count || k == 0) return 0;
        int res = func(i + 1, k, piles, dp), cur = 0;
        for (int j = 0; j < piles[i].Count && j < k; ++j) {
            cur += piles[i][j];
            res = Math.Max(res, func(i + 1, k - j - 1, piles, dp) + cur);
        }
        dp[i,k] = res;
        return res;
    }
    public int MaxValueOfCoins(IList<IList<int>> piles, int k) {
        int n = piles.Count;
        int[,] dp = new int[n + 1,k + 1];
        return func(0, k, piles, dp);
    }
}
```

```
Runtime
289 ms
Beats
83.33%
Memory
45.7 MB
Beats
100%
```

第二种是遍历。

```c#
//https://leetcode.com/problems/maximum-value-of-k-coins-from-piles/solutions/3418129/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    public int MaxValueOfCoins(IList<IList<int>> piles, int k) {
        // create a 2D array to store the maximum value of coins for choosing j coins from the first i piles
        int[,] dp = new int[piles.Count + 1,k + 1];
        // iterate through the array and compute the maximum value of coins for each subproblem
        for (int i = 1; i <= piles.Count; i++) {
            for (int j = 1; j <= k; j++) {
                int cur = 0;
                // try all possible choices for the current pile and update the maximum result
                for (int x = 0; x < Math.Min(piles[i - 1].Count, j); x++) {
                    cur += piles[i - 1][x];
                    dp[i,j] = Math.Max(dp[i,j], cur + dp[i - 1,j - x - 1]);
                }
                // if not choosing any coin from the current pile gives a better result, use that instead
                dp[i,j] = Math.Max(dp[i,j], dp[i - 1,j]);
            }
        }
        // the last element of the array is the maximum value of coins for choosing k coins from all the piles
        return dp[piles.Count,k];
    }
}
```

```
Runtime
401 ms
Beats
33.33%
Memory
45.4 MB
Beats
100%
```

最后一种是也是遍历，不过改良了dp数组。

```c#
//https://leetcode.com/problems/maximum-value-of-k-coins-from-piles/solutions/3418159/day-380-1508-100-0ms-python-java-c-explained-intution-dry-run-proof/
public class Solution {
    public int MaxValueOfCoins(IList<IList<int>> piles, int k) {
        int[] mv = new int[k + 1];
		int[] pileSum = new int[k + 1];
		foreach(IList<int> pile in piles) {
			int n = Math.Min(k, pile.Count);
			int sum = 0;
			for (int i = 1; i <= n; i++)
				pileSum[i] = sum += pile[i - 1];
			for (int i = k; i > 0; i--) {
				int max = 0;
				for (int j = Math.Min(i, n); j >= 0; j--)
					max = Math.Max(max, pileSum[j] + mv[i - j]);
				mv[i] = max;
			}
		}
		return mv[k];
    }
}
```

```
Runtime
131 ms
Beats
100%
Memory
40.6 MB
Beats
100%
```