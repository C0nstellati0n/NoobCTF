# [Number of Ways to Stay in the Same Place After Some Steps](https://leetcode.com/problems/number-of-ways-to-stay-in-the-same-place-after-some-steps)

一直在出发，从未在路上。结局是被连续这么多的hard炸成碎片
```c#
//https://leetcode.com/problems/number-of-ways-to-stay-in-the-same-place-after-some-steps/editorial
class Solution {
    public int NumWays(int steps, int arrLen) {
        int MOD = (int) 1e9 + 7;
        arrLen = Math.Min(arrLen, steps); //因为不能越界，所以取两者的最小值即可
        int[] dp = new int[arrLen]; //dp[i,j]表示从i走j步到达0的方式的数量
        int[] prevDp = new int[arrLen]; //节省空间做法，算dp[i,j]时只需要dp[i,j-1]，因此无需完整的二维dp，只记前一个就行
        prevDp[0] = 1; //base case：0步到0的方式只有一种
        for (int remain = 1; remain <= steps; remain++) {
            dp = new int[arrLen];
            for (int curr = arrLen - 1; curr >= 0; curr--) {
                int ans = prevDp[curr];
                if (curr > 0) { //curr大于0，表示可以往左走
                    ans = (ans + prevDp[curr - 1]) % MOD;
                }
                if (curr < arrLen - 1) { //curr小于arrLen-1，表示可以往右走
                    ans = (ans + prevDp[curr + 1]) % MOD;
                }
                dp[curr] = ans;
            }
            prevDp = dp;
        }  
        return dp[0];
    }
}
```
```
Runtime
17 ms
Beats
100%
Memory
31.4 MB
Beats
92.86%
```
我真找不到dp equation。对我来说理解dp和写dp最难的地方一定是dp equation。其他都还好