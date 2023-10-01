# Reverse Words in a String III

[题目](https://leetcode.com/problems/reverse-words-in-a-string-iii)

我有充足的理由说这是假的leetcode。真正的leetcode不会在周末放easy。
```c#
public class Solution {
    public string ReverseWords(string s) {
        StringBuilder sb = new();
        foreach(string c in s.Split(' ')){
            sb.Append(Reverse(c));
            sb.Append(' ');
        }
        return sb.ToString()[..^1];
    }
    public string Reverse(string s)
    {
        char[] charArray = s.ToCharArray();
        Array.Reverse(charArray);
        return new string(charArray);
    }
}
```
```
Runtime
64 ms
Beats
97.4%
Memory
48.6 MB
Beats
46.9%
```
[editorial](https://leetcode.com/problems/reverse-words-in-a-string-iii/editorial)有其他做法。思路都差不多，不过没用split。