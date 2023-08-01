# Minimum ASCII Delete Sum for Two Strings

[题目](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/description/)

掌声送给[editorial](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/editorial/),这辈子没见过这么详细的官方分析。特别是最后一种解给了14种语言的解法（带c#玩了好耶！），nb！
```c#
public class Solution {
    public int MinimumDeleteSum(string s1, string s2) {
        // Make sure s2 is smaller string
        if (s1.Length < s2.Length) {
            return MinimumDeleteSum(s2, s1);
        }
        // Case for empty s1
        int m = s1.Length, n = s2.Length;
        int[] currRow = new int[n + 1];
        for (int j = 1; j <= n; j++) {
            currRow[j] = currRow[j - 1] + s2[j - 1];
        }
        // Compute answer row-by-row
        for (int i = 1; i <= m; i++) {  
            int diag = currRow[0];
            currRow[0] += s1[i - 1]; 
            for (int j = 1; j <= n; j++) {
                int answer;    
                // If characters are the same, the answer is top-left-diagonal value
                if (s1[i - 1] == s2[j - 1]) {
                    answer = diag;
                }   
                // Otherwise, the answer is minimum of top and left values with
                // deleted character's ASCII value
                else {
                    answer = Math.Min(
                        s1[i - 1] + currRow[j],
                        s2[j - 1] + currRow[j - 1]
                    );
                }
                // Before overwriting currRow[j] with answer, save it in diag
                // for the next column
                diag = currRow[j];
                currRow[j] = answer;
            }
        }
        // Return the answer
        return currRow[n];
    }
}
```
```
Runtime
58 ms
Beats
100%
Memory
36.4 MB
Beats
94.12%
```
我在这里分析就是在editorial面前班门弄斧。这里记录几个关键点（我又发现dp的共同点了！）。editorial里面提到了个叫Bellman Equation的东西，其实就是dp中可能遇见的所有情况的总结。A为某个字符的ascii值，C为计算最小cost的函数，接受两个参数i和j，表示“考虑 $s_1$ 长度为i的子字符串和 $s_2$ 长度为j的子字符串”（注意这个i和j的定义与cache递归的定义不一样）。所有情况可以分个类：
1. base case：i = 0,j = 0，结果为0。那两个字符串都没有长度还要什么cost来将它俩变成一样的？
2. 特殊情况。对于这种两种状态相关的i和j，通常是：
- i = 0但j不等于0 ： $A(s_2[j-1])+C(i,j-1)$ 。因为dp用的数组没有负索引，而i和j又代表考虑的长度。所以要把索引减去1，防止数组越界。这里因为 $s_1$ 没有考虑任何长度，所以要减掉 $s_2$ 的字符
- j = 0但i不等于0：类似上面的情况，只不过反过来
- i=j： $C(i-1,j-1)$ :两者一样，不用减，把之前的拿上来
这些特殊情况特殊就特殊在它不需要Math.Max（或Min）来选择最优的做法。在特殊情况下，最优做法已经决定了。
3. 其他情况。除了上面之外都是其他情况，为 $min(A(s_1[i-1])+C(i-1,j),A(s_2[j-1])+C[i,j-1])$ 。两种情况，要么 $s_1$ 不变减 $s_2$ 的字符，要么 $s_2$ 不变减 $s_1$ 的字符。

找到了上面三种情况的关系后，理解个普通的dp应该就不是问题了。但是最佳做法是优化了内存的，这个就要靠找规律了。普通dp很容易看出要个二维数组，dp[length of s1][length of s2]。但是再仔细一看，好像不用这么多吧，算的时候只用到 C(i,j-1)，C(i-1,j)，C(i-1,j-1)。后两个值都来自于dp[i-1],第一个来源于当前的dp[i]。这是否意味着我们只需要两个数组即可完成dp的记忆？

然而上面的解只用了一个数组。啊？怎么做到的？我们可以叫dp[i-1]为prevRow，dp[i]为curRow。能不能只要个curRow？curRow[j-1]=之前的curRow[j-1]，即C(i,j-1)。剩下的prevRow[j]我们把它和curRow[j]合并在一起，因为curRow[j]算完后，prevRow[j]就不用了，直接覆盖即可。还剩个prevRow[j-1]，即之前的C(i-1,j-1)。这个直接用个diag变量记录就好了，用个数组太浪费了。至此我们完成了空间的优化。