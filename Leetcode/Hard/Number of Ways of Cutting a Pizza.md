# Number of Ways of Cutting a Pizza

[题目](https://leetcode.com/problems/number-of-ways-of-cutting-a-pizza/description/)

切披萨，每块披萨至少要有一个苹果。问有多少种切法。不知道。

```c#
//https://leetcode.com/problems/number-of-ways-of-cutting-a-pizza/solutions/3360907/image-explanation-dp-prefix-sum-c-java-python/
class Solution {
    public int Ways(string[] pizza, int k) {
        int m = pizza.Length;
        int n = pizza[0].Length;
        int[,,] dp = new int[k,m,n];
        int[,] preSum = new int[m+1,n+1];

        for (int r = m - 1; r >= 0; r--)
            for (int c = n - 1; c >= 0; c--)
                preSum[r,c] = preSum[r,c+1] + preSum[r+1,c] - preSum[r+1,c+1] + (pizza[r][c] == 'A' ? 1 : 0);//算某一片区域的苹果数量。从右下角开始，如果当前位置有苹果就加上1。累加时加上旁边和下面的，减去斜下方的，因为不能斜着切

        return dfs(m, n, k-1, 0, 0, dp, preSum);
    }

    int dfs(int m, int n, int k, int r, int c, int[,,] dp, int[,] preSum) {
        if (preSum[r,c] == 0) return 0; 
        if (k == 0) return 1;
        if (dp[k,r,c] != 0) return dp[k,r,c];
        int ans = 0;
        
        for (int nr = r + 1; nr < m; nr++) 
            if (preSum[r,c] - preSum[nr,c] > 0)
                ans = (ans + dfs(m, n, k - 1, nr, c, dp, preSum)) % 1000000007;
        for (int nc = c + 1; nc < n; nc++) 
            if (preSum[r,c] - preSum[r,nc] > 0)
                ans = (ans + dfs(m, n, k - 1, r, nc, dp, preSum)) % 1000000007;
                
        return dp[k,r,c] = ans;
    }
}
```

```
Runtime
89 ms
Beats
100%
Memory
38.3 MB
Beats
71.43%
```

dfs+dp百试不厌。