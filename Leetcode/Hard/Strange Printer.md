# Strange Printer

[题目](https://leetcode.com/problems/strange-printer/description/)

我脑子要打结了，建议买个新的打印机:P
```c#
//采样区，类似 https://leetcode.com/problems/strange-printer/editorial/ 的第一种做法。不同点在于editorial没用使用字典存储相同字符的索引，导致每次都要用for循环去找。这里使用后便快了不少
public class Solution {
    public int StrangePrinter(string s) {
        var dp = new int[s.Length, s.Length]; //dp定义：dp[i,j]表示打印出子字符串s[i..j]所需要的最小步骤
        var charMap = new Dictionary<char, List<int>>();
        for (var i = 0; i < s.Length; i++) {
            var c = s[i];
            if (charMap.ContainsKey(c)) { //记录字符串s里每个字符出现的索引
                charMap[c].Add(i);
            }
            else {
                charMap[c] = new List<int> { i };
            }
        }
        // init costs for substrings of length n = 1
        for (var i = 0; i < s.Length; i++) {
            dp[i, i] = 1; //假如只有一个字符的话，至少需要打印一次。base case
        }
        // calculate costs for substrings of length n >= 2
        for (var n = 2; n <= s.Length; n++) { //n为子字符串的长度
            for (var i = 0; i <= s.Length - n; i++) { //i为子字符串的左索引
                var j = i + n - 1; //j为右索引
                if (s[j] == s[j - 1]) {
                    // extending the current run。如果当前字符跟上一个字符一样，那上一次打印时可以一起打印出来，当前最小消耗等于上次的
                    dp[i, j] = dp[i, j - 1];
                }
                else { //此时s[j] != s[j - 1],参考editorial的lemma，我们要让s[j - 1]等于s[j]
                    var extensionCost = int.MaxValue;
                    if (charMap.ContainsKey(s[j])) {
                        foreach (var k in charMap[s[j]]) {
                            if (k >= j) { //遍历s[j]字符在s里所有的索引，取在范围i,j之内的，称为k
                                break;
                            }
                            if (k < i) {
                                continue;
                            }
                            extensionCost = Math.Min(extensionCost, dp[i, k] + dp [k + 1, j - 1]); //这里editorial有详细解释，从“Now we need to write down the transitions for this DP.”开始看（不过好像有点不同）
                            //这里尝试从相同的k处把要打印的s[i..j]分为两半，s[i..k],s[(k+1)..(j-1)]。那么根据dp的定义，cost就是dp[i, k] + dp [k + 1, j - 1]
                            //为什么从这里分要参考editorial里的lemma。最优的打印方式结尾一定是s[j]对应的字符
                        }
                    }
                    var startNewRunCost = dp[i, j - 1] + 1; //直接把不同的那个字符覆盖掉，cost相对于之前的加上一
                    dp[i, j] = Math.Min(extensionCost, startNewRunCost);
                }
            }
        }
        return dp[0, s.Length - 1];
    }
}
```
```
Runtime
66 ms
Beats
100%
Memory
38.1 MB
Beats
80%
```