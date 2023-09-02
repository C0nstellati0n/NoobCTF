# Extra Characters in a String

[题目](https://leetcode.com/problems/extra-characters-in-a-string/description/)

dp题我想5分钟都是煎熬。这里记录三种方法。第一、三种都来自[editorial](https://leetcode.com/problems/extra-characters-in-a-string/editorial/)
```c#
//Approach 2
//还可以参考discussion区zhibin-wang09的评论
public class Solution {
    public int MinExtraChar(string s, string[] dictionary) {
        int[] dp=new int[s.Length+1]; //Define DP[i] as the min extra character if breaking up s[0:i] optimally
        for(int i = s.Length-1; i >=0; i--)
        {
            //默认情况是，当前字符不在dictionary里，所以数量是之前的加上1
            dp[i]=dp[i+1]+1;
            for(int j = i; j < s.Length; j++)
            {
                if(dictionary.Contains(s[i..(j+1)])) //如果子字符串在字典里
                {
                    dp[i] = Math.Min(dp[i],dp[j+1]); //有两种选择。1:不包含当前字符，数量是dp[i](之前累积的加上当前字符的长度1)。2:包含当前字符，整体构成子字符串。那么这次数量不会增加，而是延续之前的（j+1处，这个dp的顺序是倒着来的）
                }
            }
        }
        return dp[0];
    }
}
```
```
Runtime
219 ms
Beats
11.11%
Memory
98.1 MB
Beats
33.33%
```
但是上面做法的实力真的战五渣。换一个。
```c#
//采样区
public class Solution {
    public int MinExtraChar(string s, string[] dictionary) {
        int n = s.Length;
        int[] dp = new int[n+1];
        for (int i = 1; i <= n; i++) //考虑所有字符串长度
        {
            dp[i] = dp[i - 1] + 1; //类似思路，不过这回是正着遍历，自然dp[i-1]是上一个的数量
            foreach (var word in dictionary) //考虑字典里的所有词。要是当前子字符串在字典里的话，肯定是其中之一
            {
                if (i >= word.Length && s.Substring(i - word.Length, word.Length).Equals(word)) //子字符串在字典里
                {
                    dp[i] = Math.Min(dp[i], dp[i - word.Length]); //上一次的数量是dp[i-word.Length]，延续下来
                }
            }
        }
        return dp[n];
    }
}
```
```
Runtime
116 ms
Beats
100%
Memory
89.3 MB
Beats
33.33%
```
以及最佳解法。
```c#
//Approach 4
//感觉和Approach 2类似思路，但是用Trie结构加速了substring
class TrieNode {
    public Dictionary<char, TrieNode> children = new();
    public bool isWord = false;
}
class Solution {
    public int MinExtraChar(String s, String[] dictionary) {
        int n = s.Length;
        var root = buildTrie(dictionary);
        var dp = new int[n + 1];
        for (int start = n - 1; start >= 0; start--) {
            dp[start] = dp[start + 1] + 1;
            var node = root;
            for (int end = start; end < n; end++) {
                if (!node.children.ContainsKey(s[end])) { //根据trie的构造，trie里是字典里有的词。这里按照字符一个一个走下去，若有一个字符不在里面，说明后续的词肯定也不在里面，直接break即可
                    break;
                }
                node = node.children[s[end]];
                if (node.isWord) {
                    dp[start] = Math.Min(dp[start], dp[end + 1]);
                }
            }
        }
        return dp[0];
    }
    private TrieNode buildTrie(String[] dictionary) {
        var root = new TrieNode();
        foreach(var word in dictionary) {
            var node = root;
            foreach(var c in word) {
                if(!node.children.ContainsKey(c)){
                    node.children[c]=new TrieNode();
                }
                node = node.children[c];
            }
            node.isWord = true;
        }
        return root;
    }
}
```
```
Runtime
107 ms
Beats
100%
Memory
85 MB
Beats
55.56%
```