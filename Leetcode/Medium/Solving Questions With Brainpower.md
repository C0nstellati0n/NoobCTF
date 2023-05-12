# Solving Questions With Brainpower

[题目](https://leetcode.com/problems/solving-questions-with-brainpower/description/)

虽然我从来没有正经好好学过算法，都是在这里抄。不过感觉这道dp已经有思路了，而且思路还是对的。然而我dp想错方向了，我计划返回dp[n]，不过更容易的做法是返回dp[0]。第一个是递归dfs。

```c#
//https://leetcode.com/problems/solving-questions-with-brainpower/solutions/1692920/python3-java-c-dfs-memoization-iterative-o-n/
class Solution {
    long[] dp;
    public long MostPoints(int[][] questions) {
        dp = new long[questions.Length];
        return dfs(questions, 0);
    }
    public long dfs(int[][] Q, int i) {
        if (i >= Q.Length) return 0;
        if (dp[i] > 0) return dp[i];
        int points = Q[i][0], jump = Q[i][1];
        return dp[i] = Math.Max(dfs(Q, i + 1), points + dfs(Q, i + jump + 1));
    }
}
```

```
Runtime
434 ms
Beats
88.89%
Memory
73.6 MB
Beats
50%
```

然后是遍历。

```c#
class Solution {
    public long MostPoints(int[][] questions) {
        int n = questions.Length;
        long[] dp = new long[n + 1]; 
        for (int i = n - 1; i >= 0; --i) { //我最开始的想法也是遍历，然而反了，我想直接正着遍历
            int points = questions[i][0], jump = questions[i][1];
            dp[i] = Math.Max(points + dp[Math.Min(jump + i + 1, n)], dp[i + 1]); //就是这里我觉得我想简单了。我打算直接遍历，然后遍历到哪就把那里的分+下一个brainpower处的分存到索引对应的dp。没做出来的原因是我dp的实现是倒着的，然而遍历却是正着的
        }
        return dp[0];
    }
}
```

```
Runtime
427 ms
Beats
100%
Memory
64.3 MB
Beats
83.33%
```