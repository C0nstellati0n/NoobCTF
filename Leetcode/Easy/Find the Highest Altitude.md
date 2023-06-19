# Find the Highest Altitude

[题目](https://leetcode.com/problems/find-the-highest-altitude/description/)

不是吧，我写这题竟然还错了一次……
```c#
public class Solution {
    public int LargestAltitude(int[] gain) {
        int max=0;
        int sum=0;
        foreach(int g in gain){
            sum+=g;
            max=Math.Max(sum,max);
        }
        return max;
    }
}
```
```
Runtime
75 ms
Beats
95.2%
Memory
38.3 MB
Beats
58.57%
```