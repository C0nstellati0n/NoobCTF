# Restore The Array

[题目](https://leetcode.com/problems/restore-the-array/description/)

又是寄了的一天。

```c#
//https://leetcode.com/problems/restore-the-array/solutions/3445455/image-explanation-easiest-concise-c-java-python/
class Solution {
    public int dfs(string s, long k, int i, int[] dp) { //i为截取的下标,s[i]就为当前字符
        if (i == s.Length) return 1; //base case
        if (s[i] == '0') return 0;
        if (dp[i] != -1) return dp[i];

        int ans = 0;
        long num = 0;
        //将其中一个截取下标固定在字符串末尾，改动开始下标：s[i..s.Length-1]。保证遍历每一个子字符串
        for (int j = i; j < s.Length; j++) {
            num = num * 10 + s[j] - '0'; //s[j]-'0'将字符转为数字。num为之前的累加和。很常见的字符串转数字方法。num记录当前子字符串转数字的值
            if (num > k) break;
            ans = (ans + dfs(s, k, j + 1, dp)) % 1000000007;//累加子字符串数量。i=0处的总数量等于i=0处本身的数量+i=1处+i=2处+...+i=s.Length-1处的数量
        }
        return dp[i] = ans;
    }

    public int NumberOfArrays(string s, int k) {
        int[] dp = new int[s.Length];
        Array.Fill(dp, -1);
        return dfs(s, k, 0, dp);
    }
}
```

```
Runtime
80 ms
Beats
50%
Memory
48.4 MB
Beats
50%
```

上面是递归，下面是遍历。
```c#
//https://leetcode.com/problems/restore-the-array/solutions/3445413/recursion-top-down-bottom-up-complete-explanation/
class Solution {
    public int NumberOfArrays(string s, int k) {
        int n = s.Length;
        int[] dp=new int[n + 1];
        //In top down 
        //1) For string starting from startIdx
        //   we needed answers of strings starting from [startIdx+1, startIdx+2, ....]
        //2) Recursion did that for us
        
        //In bottom up
        //1) We need to pre-calculate the desired results first
        //2) So we will go from startIdx = n - 1 to startIdx = 0
        //3) Now for startIdx = x, we would already have answers stored for 
        //           startIdx = [x+1, x+2, x+3......]
        
        dp[n] = 1; //base case implemented here
        for (int startIdx = n - 1; startIdx >= 0; startIdx--)
        {
            long currNum = 0, ways = 0;
            //=================================================
            for (int i = startIdx; i < s.Length; i++)
            {
                int currDig = s[i] - '0';
                currNum = (currNum * 10) + currDig; //building the number from L->R

                if (currNum < 1 || currNum > k) break;
                int nextWays = dp[i + 1]; 
                ways = (ways +  nextWays) % 1000000007;
            }
            //====================================================
            dp[startIdx] = (int)ways;
        }
        return dp[0];
    }
}
```

```
Runtime
76 ms
Beats
50%
Memory
41.2 MB
Beats
100%
```