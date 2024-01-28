# [K Inverse Pairs Array](https://leetcode.com/problems/k-inverse-pairs-array)

找规律题，我总是懒得找
```c++
//https://leetcode.com/problems/k-inverse-pairs-array/solutions/846076/c-4-solutions-with-picture
//对着discussion区 anwendeng 的评论看会比较好理解
class Solution {
public:
    int kInversePairs(int n, int k) {
        int dp[2][1001] = { 1 };
        for (int N = 1; N <= n; ++N)
            for (int K = 0; K <= k; ++K) {
                dp[N % 2][K] = (dp[(N - 1) % 2][K] + (K > 0 ? dp[N % 2][K - 1] : 0)) % 1000000007;
                if (K >= N)
                    dp[N % 2][K] = (1000000007 + dp[N % 2][K] - dp[(N - 1) % 2][K - N]) % 1000000007;
            }
        return dp[n % 2][k];
    }
};
```
也是一个新的数学概念： Triangle of Mahonian numbers