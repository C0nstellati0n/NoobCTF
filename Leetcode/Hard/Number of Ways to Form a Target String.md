# Number of Ways to Form a Target String Given a Dictionary

[题目](https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/description/)

大佬们写得这么简单让我觉得我智商有问题啊，关键给我看了我还不会。

```c#
//https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/solutions/3421395/python-java-c-simple-solution-easy-to-understand/
class Solution {
    public int NumWays(string[] words, string target) {
        int n = words[0].Length;
        int m = target.Length;
        int mod = 1000000007;
        int[] dp = new int[m+1];
        dp[0] = 1;
        
        int[,] count = new int[n,26];
        foreach(string word in words) {
            for (int i = 0; i < n; i++) {
                count[i,word[i] - 'a']++; //计算索引i处各个字符的数量
            }
        }
        
        for (int i = 0; i < n; i++) {
            for (int j = m-1; j >= 0; j--) {
                dp[j+1] += (int)((long)dp[j] * count[i,target[j] - 'a'] % mod);//从j=0开始思考（最开始初始化dp[0]=1），此时dp[j] * count[i,target[j] - 'a']为1乘上target第一个字符的数量，很好理解。结果存在j+1处，因为这是此处+之前全部可形成的字符串数量的值。那么到j=1时再次相乘，符合排列的计算
                dp[j+1] %= mod;
            }
        }
        
        return dp[m];
    }
}
```

```
Runtime
132 ms
Beats
83.33%
Memory
52.5 MB
Beats
100%
```