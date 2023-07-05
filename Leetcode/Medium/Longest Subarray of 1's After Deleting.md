# Longest Subarray of 1's After Deleting One Element

[题目](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/description/)

我同意这题应该归为easy。
```c#
public class Solution {
    public int LongestSubarray(int[] nums) {
        int i=0;
        int j=0;
        int curWindowSum=0;
        int max=0;
        while(i<nums.Length&&j<nums.Length){
            curWindowSum+=nums[j];
            if(curWindowSum<j-i){
                curWindowSum-=nums[i];
                i++;
            }
            else{
                max=Math.Max(max,j-i);
            }
            j++;
        }
        return max;
    }
}
```
```
Runtime
117 ms
Beats
98.71%
Memory
50.9 MB
Beats
66.81%
```
大佬们的解法：
- https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/solutions/708112/java-c-python-sliding-window-at-most-one-0/
- https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/solutions/3719568/beat-s-100-c-java-python-beginner-friendly/
- 无sliding window： https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/solutions/708531/java-o-n-time-o-1-space-no-sliding-window/
- dp： https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/solutions/708109/python-o-n-dynamic-programming-detailed-explanation/