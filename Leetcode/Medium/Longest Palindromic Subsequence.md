# Longest Palindromic Subsequence

[题目](https://leetcode.com/problems/longest-palindromic-subsequence/description/)

dp题，可以从各种方向得到答案。但我自己不懂就是了。

```c#
//https://leetcode.com/problems/longest-palindromic-subsequence/solutions/3415577/image-explanation-best-on-internet-recursion-top-down-bottom-up-bottom-up-o-n/
class Solution {
    public int LongestPalindromeSubseq(string s) {
        int n = s.Length;
        int[] dp = new int[n];
        for (int i = n - 1; i >= 0; i--) {//相当于进行substring，i表示起始位置
            int[] newdp = new int[n];
            newdp[i] = 1; //在起始位置截取并且长度为1的话，肯定是回文字符
            for (int j = i + 1; j < n; j++) {//j表示截取的长度
                if (s[i] == s[j]) { //如果起始处和截取处字符相同
                    newdp[j] = 2 + dp[j-1]; //假如有回文字符，长度至少为2，还要加上直到上个字符处的回文字符数量
                } else {
                    newdp[j] = Math.Max(dp[j], newdp[j-1]); //要是不一样，当前字符处回文字符数量和上一个字符处回文字符数量取最大
                }
            }
            dp = newdp; //更新dp
        }
        return dp[n-1];
    }
}
```

```
Runtime
73 ms
Beats
98.72%
Memory
54.6 MB
Beats
30.77%
```

上一个解法的dp和newdp不断更换，或许可以直接来个二维数组？for循环如果难以理解，就递归吧。

```c#
class Solution {
    int solve(string s, int[][] dp, int start, int end)
    {
        if (start == end) return 1;
        if (start > end) return 0; //起始处要是大于截取处，没有字符故不可能有回文字符串
        if (dp[start][end] != -1) return dp[start][end]; //如果之前计算过了就直接返回，防止TLE的关键步骤
        
        if (s[start] == s[end]) return (2 + solve(s, dp, start + 1, end - 1));
        
        int leaveLeft = solve(s, dp, start + 1, end);
        int leaveRight = solve(s, dp, start, end - 1);
        return dp[start][end] = Math.Max(leaveLeft, leaveRight);
    }
    public int LongestPalindromeSubseq(string s) 
    {
        int n = s.Length;
        int[][] dp=new int[n][];
        for(int i=0;i<n;i++){
            int[] temp=new int[n];
            Array.Fill(temp,-1);
            dp[i]=temp;
        }
        int ans = solve(s, dp, 0, n - 1);
        return ans;
    }
}
```

```
Runtime
97 ms
Beats
76.92%
Memory
55.8 MB
Beats
26.92%
```

最开始的for循环+二维数组。

```c#
//https://leetcode.com/problems/longest-palindromic-subsequence/solutions/3414570/recursion-top-down-bottom-up-intuitive-bottom-up/
class Solution {
    public int LongestPalindromeSubseq(string s) 
    {
        int n = s.Length;
        int[][] dp=new int[n][];
        for(int i=0;i<n;i++){ //注意不能用Array.Fill(new int[n])
            dp[i]=new int[n];
        }
        //for n length string we need LPS for string with length (n - 1) or (n - 2)
        //We need to already have LPS for smaller lengths before moving to greater lengths
        //so we need to go bottom up 
        //Calculating LPS for all strings of length = 1 to length = n
        //================================================================================
        for (int len = 1; len <= n; len++)
        {
            for (int start = 0; start <= (n - len); start++)
            {
                int end = start + len - 1; //[start, end] denotes the string under consideration
                if (len == 1) { dp[start][end] = 1; continue; }
                
                if (s[start] == s[end]) dp[start][end] = 2 + dp[start + 1][end - 1];
                else dp[start][end] = Math.Max(dp[start + 1][end], dp[start][end - 1]); 
            }
        }
        //=====================================================================================
        return dp[0][n - 1];
    }
}
```

```
Runtime
76 ms
Beats
98.72%
Memory
55.8 MB
Beats
26.92%
```