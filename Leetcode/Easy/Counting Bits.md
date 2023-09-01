# Counting Bits

[题目](https://leetcode.com/problems/counting-bits/description/)

题目：Can you do it without using any built-in function？

我：感谢提醒，差点忘了
```c#
public class Solution {
    public int[] CountBits(int n) {
        int[] res=new int[n+1];
        for(int i=0;i<=n;i++){
            res[i]=BitOperations.PopCount((uint)i);
        }
        return res;
    }
}
```
```
Runtime
79 ms
Beats
97.95%
Memory
39.7 MB
Beats
49.66%
```
个人觉得的最佳解法： https://leetcode.com/problems/counting-bits/solutions/79539/three-line-java-solution/ 。评论区有解释。当然还可以用dp（怎么到处都是dp啊？）： https://leetcode.com/problems/counting-bits/solutions/79557/how-we-handle-this-question-on-interview-thinking-process-dp-solution/