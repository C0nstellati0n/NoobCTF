# Reducing Dishes

[题目](https://leetcode.com/problems/reducing-dishes/description/)

这题的解法非常简单，没有啥复杂的操作。

```c#
//https://leetcode.com/problems/reducing-dishes/solutions/3353418/python-java-c-simple-solution-easy-to-understand/
class Solution {
    public int MaxSatisfaction(int[] satisfaction) {
        Array.Sort(satisfaction);
        int n = satisfaction.Length;
        int presum = 0, res = 0;
        for (int i = n - 1; i >= 0; i--) {
            presum += satisfaction[i];
            if (presum < 0) {
                break;
            }
            res += presum;
        }
        return res;
    }
}
```

```
Runtime
78 ms
Beats
96.55%
Memory
38.6 MB
Beats
10.34%
```

勉强算得上一种dp，presum记录之前累加的和。根据题目的描述，我们希望数值越大的dish在越后面。于是有了开头的Sort。为了让大的dish在后面，有时需要保留一些负数的dish（题目里的Example 1）。但是怎么衡量保留负数的利弊是这道题的难点。hint里有提到这一点：

```
If adding the current element to the previous best like-time coefficient and its corresponding element sum would increase the best like-time coefficient, then go ahead and add it. Otherwise, keep the previous best like-time coefficient.
```

res是最终的结果，presum是要加的值。什么样的presum会导致res值减小？当然是小于0的。于是就有了if判断，进而得到完整算法。