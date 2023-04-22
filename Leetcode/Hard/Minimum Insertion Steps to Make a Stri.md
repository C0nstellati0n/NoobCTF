# Minimum Insertion Steps to Make a String Palindrome

[题目](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/description/)

这就体现出做过前置题的快乐了。提示里有一句：`If we know the longest palindromic sub-sequence is x and the length of the string is n then, what is the answer to this problem? It is n - x as we need n - x insertions to make the remaining characters also palindrome.`。“longest palindromic sub-sequence”，诶我好像做（抄）过。

```c#
public class Solution {
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
    public int MinInsertions(string s) {
        return s.Length-LongestPalindromeSubseq(s);
    }
}
```

```
Runtime
55 ms
Beats
100%
Memory
52 MB
Beats
16.13%
```

打破个人做hard题用时的最快纪录：3分钟。1分钟看题+hint，2分钟翻discussion+自己的笔记。还有更厉害的做法。

```c#
//https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/solutions/3442303/python-java-c-simple-solution-easy-to-understand/
class Solution {
    public int MinInsertions(string s) {
        int n = s.Length;
        int[] dp = new int[n];
        for (int i = n - 2; i >= 0; i--) {//倒着开始截取字符串s[i..j]
            int prev = 0;
            for (int j = i + 1; j < n; j++) {
                int temp = dp[j]; //用于记录上一个子字符串位置需要的字符数
                if (s[i] == s[j]) { //如果两者相等，当前是个回文字符，需要添加的字符数等于上次的
                    dp[j] = prev;
                } else {
                    dp[j] = Math.Min(dp[j], dp[j-1]) + 1;//如果不一样，肯定要加至少一个字符
                }
                prev = temp;
            }
        }
        return dp[n-1];
    }
}
```

```
Runtime
62 ms
Beats
100%
Memory
36 MB
Beats
100%
```

至于为什么使用Math.Min而不是直接dp[j-1]或者Math.Max,我用脑子跑了一下，让参数等于abc，确实是只有Math.Min才行。然后思考了一下，假设i固定为0，dp[j]表示s[..j]（一直截取到j）处需要添加的字符数；dp[j-1]则是s[..(j-1)]。假如两者相等，那没啥好说的了，加一个字符。若dp[j-1]> dp[j]，说明dp[j-1]处需要的字符串比dp[j]处多，可是s[..j]明显比s[..(j-1)]长，说明真正需要的字符数应该是更小的那个。总之以最小的为准。