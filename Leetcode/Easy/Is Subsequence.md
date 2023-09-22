# Is Subsequence

[题目](https://leetcode.com/problems/is-subsequence)

是个easy！肯定很简单！我不到3分钟就想出了大致思路——two pointers。然而edge case和语句的顺序让我debug了几十分钟。这就是通过率不到50%的原因吗？
```c#
public class Solution {
    public bool IsSubsequence(string s, string t) {
        if(s.Length==0){
            return true;
        }
        if(t.Length==0){
            return false;
        }
        int i=0;
        int j=0;
        while(true){
            if(i>=s.Length){
                return true;
            }
            if(j>=t.Length){
                return false;
            }
            if(s[i]==t[j]){
                i++;
                j++;
            }
            else{
                j++;
            }
        }
    }
}
```
```
Runtime
60 ms
Beats
86.48%
Memory
38 MB
Beats
17.92%
```
我发现我写two pointers的代码总是这样瘦瘦长长的。我的代码的逻辑等同于采样区的极简做法：
```c#
public class Solution {
    public bool IsSubsequence(string s, string t) {
        var i = 0;
        var j = 0;
        while (i < s.Length && j < t.Length) {
            if (s[i] == t[j]) {
                i++;
            }
            j++;
        }
        return i == s.Length;
    }
}
```
```
Runtime
53 ms
Beats
98.53%
Memory
37.5 MB
Beats
94.81%
```
所以几个if语句就多了我7ms，0.5mb？不管了，看看其他解法。
- https://leetcode.com/problems/is-subsequence/solutions/1811180/c-easy-3-approaches-brute-force-recursive-memoization ：递归+memo递归（递归dp？）
- https://leetcode.com/problems/is-subsequence/solutions/87302/binary-search-solution-for-follow-up-with-detailed-comments ：应对follow up提到情况的binary search做法。主要思路是，若s[i]==t[j]，则s[i]要么等于t[j+n]，要么后续没有其他字符与之匹配。若是第一种情况，用binary search找到j+n；第二种情况直接返回false