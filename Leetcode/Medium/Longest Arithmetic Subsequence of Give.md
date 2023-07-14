# Longest Arithmetic Subsequence of Given Difference

[题目](https://leetcode.com/problems/longest-arithmetic-subsequence-of-given-difference/description/)

从对dp毫无头绪到wrong answer到TLE，这算进步吗？
```c#
//https://leetcode.com/problems/longest-arithmetic-subsequence-of-given-difference/editorial/
//采样区
public class Solution {
    public int LongestSubsequence(int[] arr, int difference) {
        var numAndSequenceCount = new Dictionary<int, int>();
        var result = 1;
        foreach (var num in arr)
        {
            var curSequence = numAndSequenceCount.ContainsKey(num - difference) ? 1 + numAndSequenceCount[num - difference] : 1; //计算当前数字所在的sequence的上一个数字作为key，若存在就取值，不存在说明当前数字是第一个
            
            if (numAndSequenceCount.ContainsKey(num)) numAndSequenceCount[num] = Math.Max(numAndSequenceCount[num], curSequence); //加上当前数字。值选择之前的长度和当前长度最大的那个
            else numAndSequenceCount.Add(num, curSequence);

            result = Math.Max(result, numAndSequenceCount[num]);
        }

        return result;
    }
}
```
```
Runtime
188 ms
Beats
67.86%
Memory
48.2 MB
Beats
46.43%
```
我自己写的参考了[Longest Arithmetic Subsequence](./Longest%20Arithmetic%20Subsequence.md)的嵌套循环。能算出正确答案，但是这道题的test case太长了，于是就TLE了。