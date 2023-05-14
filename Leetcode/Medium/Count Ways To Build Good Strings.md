# Count Ways To Build Good Strings

[题目](https://leetcode.com/problems/count-ways-to-build-good-strings/description/)

当你看到这道题的答案时，你就会知道discussion里为什么有人推荐先去做[Climbing Stairs](../Easy/Climbing%20Stairs.md)了。

```c#
//https://leetcode.com/problems/count-ways-to-build-good-strings/solutions/3518124/python3-c-java-easy-and-understand-dp/
class Solution {
        public int CountGoodStrings(int low, int high, int zero, int one) {
        int[] dp = new int[high + 1];
        int res = 0;
        int mod = 1000000007;
        dp[0] = 1;
        for (int i = 1; i <= high; ++i) {
            if (i >= zero) dp[i] = (dp[i] + dp[i - zero]) % mod;
            if (i >= one) dp[i] = (dp[i] + dp[i - one]) % mod;
            if (i >= low) res = (res + dp[i]) % mod;
        }
        return res;
    }
}
```

```
Runtime
20 ms
Beats
100%
Memory
29.5 MB
Beats
90%
```

这题答案就和Climbing Stairs差了个if语句判断是否在范围里。“应该不会有人明明抄过答案了，但这题多了几个if语句就不会做了吧？”

你猜我为什么不说话。