# New 21 Game

[题目](https://leetcode.com/problems/new-21-game/description/)

埋了吧，又不会数学又不会dp的我。

```c#
//https://leetcode.com/problems/new-21-game/solutions/132334/one-pass-dp-o-n/
public class Solution {
    public double New21Game(int N, int K, int W) {
        if (K == 0 || N >= K + W) return 1;
        double[] dp = new double[N + 1];
        double Wsum = 1;
        double res = 0;
        dp[0] = 1;
        for (int i = 1; i <= N; ++i) {
            dp[i] = Wsum / W;
            if (i < K) Wsum += dp[i]; else res += dp[i];
            if (i - W >= 0) Wsum -= dp[i - W];
        }
        return res;
    }
}
```
```
Runtime
29 ms
Beats
100%
Memory
29.3 MB
Beats
100%
```
评论区有个人帮忙解释了一下。
```
 When the game ends, the point is between K and K-1+W
    What is the probability that the the point is less than N?
    - If N is greater than K-1+W, probability is 1
    - If N is less than K, probability is 0
    
    If W == 3 and we want to find the probability to get a 5
    - You can get a card with value 1, 2, or 3 with equal probability (1/3)
    - If you had a 4 and you get a 1: prob(4) * (1/3)
    - If you had a 3 and you get a 2: prob(3) * (1/3)
    - If you had a 2 and you get a 3: prob(2) * (1/3)
    - If you had a 1, you can never reach a 5 in the next draw
    - prob(5) = prob(4) / 3 + prob(3) / 3 + prob(2) /3
    
    To generalize:
    The probability to get point K is
    p(K) = p(K-1) / W + p(K-2) / W + p(K-3) / W + ... p(K-W) / W
    
    let wsum = p(K-1) + p(K-2) + ... + p(K-W)
    p(K) = wsum / W
    
    dp is storing p(i) for i in [0 ... N]
    - We need to maintain the window by
      adding the new p(i), 
      and getting rid of the old p(i-w)
    - check i >= W because we would not have negative points before drawing a card
      For example, we can never get a point of 5 if we drew a card with a value of 6
    - check i < K because we cannot continue the game after reaching K
      For example, if K = 21 and W = 10, the eventual point is between 21 and 30
      To get a point of 27, we can have:
      - a 20 point with a 7
      - a 19 point with a 8
      - a 18 point with a 9
      - a 17 point with a 10
      - but cannot have 21 with a 6 or 22 with a 5 because the game already ends
```
大佬说这题像[Climbing Stairs](../Easy/Climbing%20Stairs.md)，也有sliding window的思想。Climbing Stairs里可以选择走一步或者两步，这里把范围放大，W步内都没问题。那么达到分数i有W中可能，分别是i-1,i-2...i-w。sliding window在于我们要保持Wsum中只有前W个和。如果i - W >= 0，说明Wsum里已经有W个了，需要减去最开始的一个，为新的腾位置。只要i < K，我们就保持这个W大小的window不断滑动。i > K时就能清算返回结果了，因为游戏到K时就结束了，不存在从K以上的地方像刚才那样继续滑动window。