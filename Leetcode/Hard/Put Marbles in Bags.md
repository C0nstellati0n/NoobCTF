# Put Marbles in Bags

[题目](https://leetcode.com/problems/put-marbles-in-bags/description/)

一道代码不难不过非常反直觉的题。
```c#
//采样区最佳
//与 https://leetcode.com/problems/put-marbles-in-bags/editorial/ 相同思路
public class Solution {
    public long PutMarbles(int[] weights, int k) {
        /* Score is determined by split points.

           [s1 . . . e1][s2 . . e2][s3 . . . . e3]
                     split1     split2

            Define split1=e1+s2, split2=e2+s3 and so on
            So the total score is s1 + split1 + split2 + e3
        
            We can create this split array, sort it, and calculate min/max scores:

            min score = s1 + e3 + sum(first k-1 elements of sorted split array)
            max score = s1 + e3 + sum(last k-1 elements of sorted split array)

            max score-min score = sum(last k-1 elements of sorted split array)
                                  - sum(first k-1 elements of sorted split array)
        */

        int[] pairs = new int[weights.Length - 1];

        for (int i = 0; i < weights.Length - 1; i++) {
            pairs[i] = weights[i] + weights[i + 1];
        }

        Array.Sort(pairs);

        long diff = 0;

        for (int i = 0; i < k - 1; i++) {
            diff += pairs[^(i + 1)] - pairs[i];
        }

        return diff;
    }
}
```
```
Runtime
245 ms
Beats
100%
Memory
51.8 MB
Beats
33.33%
```
要求找最大值和最小值，weights没有规律。乍一看好像只能爆破，不把全部情况试一遍怎么知道谁最大谁最小？关键点在于计算score时使用subarray的第一个和最后一个。拿代码里的例子：
```
[s1 . . . e1][s2 . . e2][s3 . . . . e3]
          split1     split2
```
根据题目要求，计算时应该把s1和e1加起来，s2和e2加起来对吧？真要按照题目要求加时间复杂度直接炸，为何不把e1和s2加起来？或者说，0<=i< k-1,把i和i+1加起来。我的直觉感觉就是，这怎么行？但是转念一想，不要把e1和s2看成相邻的weight，要看成两个split的分界点。(s1+e1)+(s2+e2)+(s3+e3)与s1+(e1+s2)+(e2+s3)+e3，又有什么区别呢？

现在到第二个问题：pairs固定为前一个与后一个的和，这么看每次只能分成上述的三块啊，不是说好k份吗？这里我是这么理解的：pair是不重复的分法，因为中间我们排序了，所以从前面数起k个是score最小的分法，从后面数起k个是score最大的分法。那么把这两种分法一一对应，从后面数起的分法-前面数起的分法就是差值了，根本不用费时费力加起来。

所以某种意义上这是个brute force，已经把所有可能的分法列举出来了，只不过是聪明人的brute force。