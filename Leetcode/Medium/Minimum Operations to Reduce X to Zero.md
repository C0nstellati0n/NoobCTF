# Minimum Operations to Reduce X to Zero

[题目](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero)

hint：尝试换一种思路，跳出常见思维的盒子

我：思维？盒子？哪有思维？哪有盒子？
```c#
//https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/solutions/2136570/change-your-perspective-java-explanation
public class Solution {
    public int MinOperations(int[] nums, int x) {
        int sum = nums.Sum();
        int maxLength = -1, currSum = 0;
        for (int l=0, r=0; r<nums.Length; r++) {
            currSum += nums[r];
            while (l <= r && currSum > sum - x) currSum -= nums[l++];
            if (currSum == sum - x) maxLength = Math.Max(maxLength, r-l+1);
        }
        return maxLength == -1 ? -1 : nums.Length - maxLength;
    }
}
```
```
Runtime
228 ms
Beats
90.48%
Memory
54.4 MB
Beats
85.71%
```
这题要求我们在数组nums两边选数字删除，使得删除的数字构成x。我一下就想到了dp（是怎么做到每天想着dp但又完全不会dp的？），但是这题dp好像没有什么好的关系，除了爆破没啥别的。而且constraint也很高，dp怕不是会TLE。

换个思路，在nums两边删除数字，意味着删除完成后中间会留下一些没动过的数字，对吧？如果我们直接去找中间那些不用删除的数字呢？利用sliding window，当windows中数字之和为nums.Sum()-x时，说明nums的长度减去窗户的长度就是全部要删除数字的长度。