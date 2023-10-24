# [Power of Four](https://leetcode.com/problems/power-of-four)

数学！是数学！他用了数学！
```c#
//采样区，发现用BitOperations会比较快
public class Solution {
    public bool IsPowerOfFour(int n) {
        return
            n > 0 && BitOperations.PopCount((uint)n) == 1 &&
            BitOperations.TrailingZeroCount((uint)n)%2 == 0;
    }
}
```
其他做法：
- https://leetcode.com/problems/power-of-four/solutions/80457/java-1-line-cheating-for-the-purpose-of-not-using-loops
- https://leetcode.com/problems/power-of-four/solutions/80461/python-one-line-solution-with-explanations ，这个讲得更详细一点