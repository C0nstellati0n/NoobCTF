# Longest Arithmetic Subsequence

[题目](https://leetcode.com/problems/longest-arithmetic-subsequence/description/)

至少这题的for循环我自己写出来了。你问我dp数组？哈哈，完全错误。
```c#
//https://leetcode.com/problems/longest-arithmetic-subsequence/solutions/274611/java-c-python-dp/
//类似的解法（有解释）： https://leetcode.com/problems/longest-arithmetic-subsequence/solutions/3671662/beats-100-c-java-python-beginner-friendly/
public class Solution {
    public int LongestArithSeqLength(int[] nums) {
        int res = 2, n = nums.Length;
        Dictionary<int, int>[] dp = new Dictionary<int, int>[n];
        int temp;
        for (int j = 0; j < nums.Length; j++) { //考虑i-j范围里的数字
            dp[j] = new();
            for (int i = 0; i < j; i++) {
                int d = nums[j] - nums[i]; //计算所有可能的差值
                temp=1;
                if(dp[i].ContainsKey(d)){ //这块感觉逻辑是这样的：dp[i][d]表示nums[0..i]中差值为d的数列长度为temp。base case为1
                    temp=dp[i][d];
                }
                dp[j][d]=temp + 1; //i永远小于j，nums[0..i]中差值为d的数列长度为temp，那么到j就是temp+1（前提是差值d一样，不过键不一样也加不起来）
                res = Math.Max(res, dp[j][d]); //总感觉dp的另一个灵魂就在这，每个dp解法总会有类似的一句
            }
        }
        return res;
    }
}
```
```
Runtime
557 ms
Beats
74.69%
Memory
65.6 MB
Beats
35.19%
```
或者不用字典，根据description里的constraint直接初始化那么长的数组好了。
```c#
//采样区的最佳解
//感觉类似 https://leetcode.com/problems/longest-arithmetic-subsequence/solutions/910303/c-quadratic-time-space-bottom-up-dp/
public class Solution {
    public int LongestArithSeqLength(int[] nums) {
        int n = nums.Length; 
        if (n <= 2) return n; 
        int longest = 2; 
        int[][] dp = new int[n][]; 
        for (int i = 0; i < n; i++) { 
            dp[i] = new int[1002]; 
            Array.Fill(dp[i], 1); 
            for (int j = 0; j < i; j++) { 
                int diff = nums[i] - nums[j] + 501; //保证不会有负值
                dp[i][diff] = dp[j][diff] + 1; 
                longest = Math.Max(longest, dp[i][diff]);
            }
        }
        return longest;                                                 
    }
}
```
```
Runtime
117 ms
Beats
99.82%
Memory
61.1 MB
Beats
75.23%
```