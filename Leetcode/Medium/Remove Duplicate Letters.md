# Remove Duplicate Letters

[题目](https://leetcode.com/problems/remove-duplicate-letters)

看了一圈solution都没搞懂hint说的bitmask做法是啥。
```c#
//https://leetcode.com/problems/remove-duplicate-letters/solutions/1859410/java-c-detailed-visually-explained
//discussion区ealejandria的评论解释了此题要求的smallest in lexicographical order是什么（感觉应该说smallest lexicographical order possible subsequence）
public string RemoveDuplicateLetters(string s) {
        int[] lastIndex = new int[26];
        for (int i = 0; i < s.Length; i++){
            lastIndex[s[i] - 'a'] = i; // track the lastIndex of character presence
        }
        bool[] seen = new bool[26]; // keep track seen
        Stack<int> st = new();
        for (int i = 0; i < s.Length; i++) {
            int curr = s[i] - 'a';
            if (seen[curr]) continue; // if seen continue as we need to pick one char only
            while (st.Any() && st.Peek() > curr && i < lastIndex[st.Peek()]){ //进到这个while循环里要满足3个条件：stack有字符，stack最顶端的字符大于curr，当前所在index i小于stack顶部字符最后出现的index
                //st.Peek() > curr 是为了尽量保持lexicographical order。比如stack里有个b，curr目前是a。我们希望最后的结果是ab而不是ba。所以把里面的b pop出来，再把a放进去
                //i < lastIndex[st.Peek()] 是为了保证把字符pop出来后后面还有字符。还是刚才那个例子，如果stack里的b是字符串里最后一个b，pop后就没有了，就算我们想保持lexicographical order也没法，只能保留
                seen[st.Pop()] = false; // pop out and mark unseen
            }
            st.Push(curr); // add into stack
            seen[curr] = true; // mark seen
        }
        StringBuilder sb = new();
        while (st.Any())
            sb.Append((char) (st.Pop() + 'a'));
        return new string(sb.ToString().Reverse().ToArray());
    }
}
```
```
Runtime
72 ms
Beats
67.11%
Memory
38.3 MB
Beats
60.53%
```
差不多的思路还有个递归做法。
```c#
//采样区
//类似 https://leetcode.com/problems/remove-duplicate-letters/solutions/76768/a-short-o-n-recursive-greedy-solution
public class Solution 
{
    public string RemoveDuplicateLetters(string s) 
    {
        int[] counts = new int[26];
        for (int i = 0; i < s.Length; i++) 
            counts[s[i] - 'a']++;
        int index = 0;
        for (int i = 0; i < s.Length; i++) 
        {
            counts[s[i] - 'a']--;
            if (s[i] < s[index])  //尽量找lexicographical order最小的字符
                index = i;
            if (counts[s[i] - 'a'] == 0)  //当当前字符是字符串里最后一个时，不用考虑lexicographical order了，毕竟不可能再把这个换掉
                break;
        }
        if(s.Length == 0) return string.Empty;
        string rest = s.Substring(index + 1);
        rest = rest.Replace(s[index].ToString(), string.Empty);
        return s[index] + RemoveDuplicateLetters(rest);
    }
}
```
```
Runtime
68 ms
Beats
89.47%
Memory
39.3 MB
Beats
5.26%
```