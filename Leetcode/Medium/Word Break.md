# Word Break

[题目](https://leetcode.com/problems/word-break/description/)

怎么不backtrack了？你来dp我不会了啊，而且还是bool dp，好久没见了，完全忘了怎么写。
```c#
//https://leetcode.com/problems/word-break/editorial/ 有dp的递归和遍历做法解释，这里只放遍历的
public class Solution {
    public bool WordBreak(string s, IList<string> wordDict) {
        bool[] dp = new bool[s.Length + 1]; //dp[i]表示字符串s的长度为i的子字符串是否可被wordDict组合得来
        dp[0] = true; //base case，长度为0的话肯定可以，所以是true
        HashSet<string> set = new HashSet<string>(wordDict); //用个set把wordDict里面重复的排除掉，因为可以重复用。当然直接wordDict就能contains，可能是这样更快？
        for(int i = 0; i < dp.Length; i++) //考虑长度为i的子字符串
        {
            for(int j = 0; j < i; j++) //考虑子字符串里长度为j的子字符串
            {
                if(dp[j] && set.Contains(s.Substring(j, i - j))) //若j子字符串在wordDict里且i-j那段子字符串也在wordDict里，说明i整个处字符串都在wordDict里
                {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[s.Length];
    }
}
```
```
Runtime
81 ms
Beats
99.36%
Memory
47.3 MB
Beats
38.12%
```
算是比较简单的dp，但是我真忘了。