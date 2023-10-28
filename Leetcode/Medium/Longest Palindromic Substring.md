# [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring)

事实证明，看提示要看全，自以为是看一半不看一半只会怀疑人生
```c#
//https://leetcode.com/problems/longest-palindromic-substring/solutions/2921/share-my-java-solution-using-dynamic-programming
public class Solution {
    public string LongestPalindrome(string s) {
        int n = s.Length;
        var res = (0,0); //原解法用的是个字符串，我嫌字符串占内存就用了tuple
        bool[,] dp = new bool[n,n];
        for (int i = n - 1; i >= 0; i--) { //倒着遍历所有可能的substring
            for (int j = i; j < n; j++) {
                dp[i,j] = s[i] == s[j] && (j - i < 3 || dp[i + 1,j - 1]);  
                if (dp[i,j] && j - i + 1 > res.Item2-res.Item1+1) {
                    res = (i, j);
                }
            }
        }
        return s[res.Item1..(res.Item2+1)];
    }
}
```
一个普通的dp。连我这样的人都能在看了discussion区947876275的评论后写出嵌套for循环（虽然方向好像不太一样），res tuple和抄的dp equation。一般来说都到这了肯定已经出来了，那么我又死在了哪呢？我tm只看了一半：
```
So base cases are:
M[i][i] is true.
M[i][i + 1] = (s[i] == s[i + 1]);
recurrence relation is :
M[i][j] = (s[i] == s[j] AND M[i + 1][j - 1]);
```
我自动忽略了`M[i][i + 1] = (s[i] == s[i + 1]);`这句，对应上面的做法就是`j - i < 3`。因为长度为两个字符和三个字符的回文字符串比较特殊，只要头尾一致，中间的不用管，一定是回文字符；而更长的回文字符串就需要检查中间是否是了

接下来赏析[editorial](https://leetcode.com/problems/longest-palindromic-substring/editorial)。第一种无脑爆破就不看了，检查所有substring，然后检查substring是否是回文字符串。因为没用dp所有时间复杂度是 $O(n^3)$ 。第二种dp做法也是检查所有substring，但是用dp记录，所以省去了检查回文字符串的O(n)，时间复杂度是 $O(n^2)$ 。另外，editorial的dp思路和上面那个不一样，不过也不难理解

第三种那个从中间延伸的也不难懂。前两种都是考虑回文字符串的头和尾，这种做法考虑中间。遍历所有可能的索引作为中间，然后同时向两边延伸。如果它是回文字符串的话，延伸时两边字符肯定都是一样的。注意需要分开考虑奇数长度和偶数长度

然后到第四种瞬间上难度：[Manacher's Algorithm](https://www.zhihu.com/question/37289584)。非常复杂，我考虑以后再学