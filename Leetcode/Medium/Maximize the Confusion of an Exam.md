# Maximize the Confusion of an Exam

[题目](https://leetcode.com/problems/maximize-the-confusion-of-an-exam/description/)

哇我的代码一次过，还是双100%！
```c#
public class Solution {
    public int MaxConsecutiveAnswers(string answerKey, int k) {
        if(k>answerKey.Length){
            return answerKey.Length;
        }
        int left = 0, right = 0;
        int res = 0;
        int tCount=0;
        int fCount=0;
        int min=0;
        for(right = 0; right < answerKey.Length; right++) {
            if(answerKey[right]=='T'){
                tCount++;
            }
            else{
                fCount++;
            }
            min=Math.Min(tCount,fCount);
            while (min>k) {
                if(answerKey[left++]=='T'){
                    tCount--;
                }
                else{
                    fCount--;
                }
                min=Math.Min(tCount,fCount);
            }
            res = Math.Max(res, right - left+1);
        }
        return res;
    }
}
```
```
Runtime
66 ms
Beats
100%
Memory
43.8 MB
Beats
100%
```
灵感完全来源于昨天的[Minimum Size Subarray Sum](./Minimum%20Size%20Subarray%20Sum.md). 我就说，同样的问题怎么可能死两次呢？sliding window已经难不住我啦！（开始飘了）

[editorial](https://leetcode.com/problems/maximize-the-confusion-of-an-exam/editorial/)有binary search做法，不过表现不怎么样。关键java版里用了好多getordefault，c#里没有现成的，每次就只能靠我乱写。到最后不仅花了我很多时间，关键还是wrong answer。md。