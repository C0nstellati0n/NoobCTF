# [Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome)

[KMP算法](https://www.ruanyifeng.com/blog/2013/05/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm.html)我来了，开始还之前欠的债
```c++
//https://leetcode.com/problems/shortest-palindrome/editorial
class Solution {
public:
    string shortestPalindrome(string s) {
        // Reverse the original string
        string reversedString = string(s.rbegin(), s.rend());
        // Combine the original and reversed strings with a separator
        string combinedString = s + "#" + reversedString;
        // Build the prefix table for the combined string
        vector<int> prefixTable = buildPrefixTable(combinedString);
        // Get the length of the longest palindromic prefix
        int palindromeLength = prefixTable[combinedString.length() - 1];
        // Construct the shortest palindrome by appending the reverse of the
        // suffix
        string suffix = reversedString.substr(0, s.length() - palindromeLength);
        return suffix + s;
    }
private:
    // Helper function to build the KMP prefix table
    vector<int> buildPrefixTable(const string& s) {
        vector<int> prefixTable(s.length(), 0);
        int length = 0;
        // Build the table by comparing characters
        for (int i = 1; i < s.length(); i++) {
            while (length > 0 && s[i] != s[length]) {
                length = prefixTable[length - 1];
            }
            if (s[i] == s[length]) {
                length++;
            }
            prefixTable[i] = length;
        }
        return prefixTable;
    }
};
```
这题只用了kmp算法的部分匹配表（Partial Match Table）概念。`table[i]`表示字符串s头部和尾部在i处构成回文的长度。比如`ABCDABD`，`table[4]=1`。表示`ABCDA`中回文的长度为1（头部的A和尾部的A）；`table[5]=2`,因为ABCDAB中AB和BA互为回文且长度为2

然后可以参考 https://leetcode.com/problems/shortest-palindrome/solutions/60113/clean-kmp-solution-with-super-detailed-explanation 里的思路，将这题转化一下。这题要求的其实是“找出字符串s位于0的最长回文字符串”。比如`aacecaaa`，从开头开始算，最长的回文字符串是`aacecaa`

为什么最开始要创建个combinedString？我是这么想的：想要构建部分匹配表，得有个目标字符串s。不能直接用题目给的字符串s，因为我们要找的是从开头开始的回文字符串，这个回文字符串不一定延伸到尾部，或者说我们根本就不知道它的结束点在哪，那部分匹配表的哪个索引处对应的是从开头开始的回文字符串长度？所以构造combinedString，`table[combinedString.length()-1]`就是我们要的值

editorial还提供了Rolling Hash和Manacher's Algorithm做法，前者似乎可以同时计算一个字符串s和倒着的s的哈希值；后者在回文字符串相关题里见过