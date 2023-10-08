# [Build Array Where You Can Find The Maximum Exactly K Comparisons](https://leetcode.com/problems/build-array-where-you-can-find-the-maximum-exactly-k-comparisons/)

这才是我认识的leetcode，"make my life harder"
```c#
//https://leetcode.com/problems/build-array-where-you-can-find-the-maximum-exactly-k-comparisons/editorial
//Approach 5: Space-Optimized Better DP ，5种解法里空间时间均最佳
class Solution {
    public int NumOfArrays(int n, int m, int k) {
        //三维dp，dp[i,j,k]表示长度为i，最大元素为j，从左向右遍历有k个new maximums的array的个数
        //这里只用两维是因为当前state dp[i,j,k]的计算仅依赖dp[i-1,j,k]（或者也有k-1），所以下面用个prevDp记住上次的就行
        long[,] dp = new long[m + 1,k + 1];
        long[,] prefix = new long[m + 1,k + 1]; //prefix[i][maxNum][cost] = dp[i][0][cost] + dp[i][1][cost] + ... + dp[i][maxNum][cost].这个用于第二种情况
        long[,] prevDp = new long[m + 1,k + 1];
        long[,] prevPrefix = new long[m + 1,k + 1]; //类似prevDp，每次计算只依赖上一次的所以记个prev
        int MOD = (int) 1e9 + 7;
        for (int num = 1; num <= m; num++) {
            dp[num,1] = 1; //base case，maximums限定为1时，只有一种构造方式
        }
        for (int i = 1; i <= n; i++) {
            if (i > 1) { //创建新的用于替换的dp
                dp = new long[m + 1,k + 1];
            }
            prefix = new long[m + 1,k + 1];
            for (int maxNum = 1; maxNum <= m; maxNum++) {
                for (int cost = 1; cost <= k; cost++) {
                    long ans = (maxNum * prevDp[maxNum,cost]) % MOD; //第一种情况，新添加的数字不是new maximum。所有在1到maxNum范围内的数字都符合要求，总共maxNum个。之前有prevDp[maxNum,cost]种构造方法，而这种情况maxNum和cost都没有变化，乘上就是当前state的构造方式的数量
                    ans = (ans + prevPrefix[maxNum - 1,cost - 1]) % MOD; //第二种情况，新添加的数字是new maximum。那么为了达到这种state，就要从之前dp[i - 1][num][cost - 1],num取[1, maxNum - 1]加上来。cost-1是因为这个new maximum占用了一个cost，maxNum-1也是一样的道理。正好prefix就是需要的值
                    dp[maxNum,cost] += ans;
                    dp[maxNum,cost] %= MOD;    
                    prefix[maxNum,cost] = (prefix[maxNum - 1,cost] + dp[maxNum,cost]); //prefix计算dp[i - 1][num][cost - 1],num取[1, maxNum - 1]全部的值加起来
                    prefix[maxNum,cost] %= MOD;
                }
            }
            prevDp = dp;
            prevPrefix = prefix;
        }
        return (int) prefix[m,k]; //这种dp的结果为dp[n][m][k]，m取所有小于maxNum的值相加的结果。所以返回的是prefix而不是dp
    }
}
```
这次数据没有任何参考价值，因为“Sorry, there are not enough accepted submissions to show data”，所以只要提交了就是100%。c#这么冷门吗？java都有数据，这个异父异母的亲兄弟就这么没有排面？