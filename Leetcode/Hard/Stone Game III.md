# Stone Game III

[题目](https://leetcode.com/problems/stone-game-iii/description/)

我真的是搞不懂这个dp。dp说是要把大问题拆成小问题，这不是问题，问题是怎么拆？就算我隐隐约约知道怎么拆，比如这题结合[昨天的],能看出来要考虑3种不同的步骤。但是我dp数组怎么构造？我用多维数组还是交错数组？还是其实一维就好了？这题我下意识认为要多维，dp[i,j]表示i处石堆走j步。实际上大错特错，把昨天的思路带到今天了（主要discussion里面说看了昨天的今天的就很简单，我就以为是在昨天的基础上改动，结果他们的意思是今天的本来就比昨天的简单很多）。昨天用交错数组是因为不确定下一步怎么抓，昨天的题下一步怎么抓有规则，今天的就是1-3里面选。

假设我有幸猜对了dp数组的格式，dp[i]表示什么？是可使对方获得最少的石块数量，还是可让自己获得最多的石块数量？这个搞懂了，代码怎么实现？有两个人抓，我怎么在一个数组同一个位置表示出两个人？别看我这一连串问题，实际上代码非常短。
```c#
//https://leetcode.com/problems/stone-game-iii/solutions/564260/java-c-python-dp-o-1-space/
public class Solution {
    public string StoneGameIII(int[] A) {
        int n = A.Length;
        int[] dp = new int[4]; //优化版本，O(n)变O(1)。dp[i]表示“if we ignore before A[i],what's the highest score that Alice can win over the Bob？”。因为可能移动的步骤只有1-3，所以存4个就够了，当前步骤+可能移动步骤，i%4
        for (int i = n - 1; i >= 0; --i) { //经常搞不清楚for正着来还是倒着来
            dp[i % 4] = Int32.MinValue;
            for (int k = 0, take = 0; k < 3 && i + k < n; ++k) {
                take += A[i + k]; //拿上i+k步的石头
                dp[i % 4] = Math.Max(dp[i % 4], take - dp[(i + k + 1) % 4]); //这是个计算当前i赢取石头时的公式。至于为什么是减号，因为“when calculating dp[i] for Alice, dp[i+1] should be viewed as the amount Bob wins over Alice”
            }
        }
        if (dp[0] > 0) return "Alice";
        if (dp[0] < 0) return "Bob";
        return "Tie";
    }
}
```
```
Runtime
324 ms
Beats
100%
Memory
50.7 MB
Beats
30%
```
还有另一种用[minimax](https://en.wikipedia.org/wiki/Minimax)的。表现不如上面的，不过好像这类游戏都能用这个通解，作为参考学习。
```c#
//https://leetcode.com/problems/stone-game-iii/solutions/564896/java-2-solutions-minimax-bottom-up-dp-clean-code-o-n/
class Solution {
    public string StoneGameIII(int[] arr) {
        int score = minimax(arr, 0, 1, new int[arr.Length,2]);
        if (score > 0) return "Alice";
        if (score < 0) return "Bob";
        return "Tie";
    }
    int minimax(int[] arr, int i, int maxPlayer, int[,] dp) {
        if (i >= arr.Length) return 0;
        if (dp[i,maxPlayer] != 0) return dp[i,maxPlayer];
        int ans = maxPlayer == 1 ? int.MinValue : int.MaxValue;
        int score = 0;
        for (int j = i; j < Math.Min(arr.Length, i + 3); j++) {
            if (maxPlayer == 1) {
                score += arr[j];
                ans = Math.Max(ans, score + minimax(arr, j + 1, 0, dp));
            } else {
                score -= arr[j];
                ans = Math.Min(ans, score + minimax(arr, j + 1, 1, dp));
            }
        }
        return dp[i,maxPlayer] = ans;
    }
}
```
```
Runtime
388 ms
Beats
30%
Memory
53 MB
Beats
10%
```