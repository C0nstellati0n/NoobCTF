# Median of Two Sorted Arrays

[题目](https://leetcode.com/problems/median-of-two-sorted-arrays)

前排提示：此题难度较高，据前人所说，20-50分钟的面试里问这道题基本等于放弃。更关键的是，这题的思路很少见，见过就忘，后面也不会有类似的题了。综合建议，要不是面试的不用认真看这题。

荒谬的是，这还是我第一道完全独立无提示完成的hard题。因为我用了无敌trivial解法。
```c#
public class Solution {
    public double FindMedianSortedArrays(int[] nums1, int[] nums2) {
        int length=nums1.Length+nums2.Length;
        List<int> nums3=new();
        foreach(int num in nums1){
            nums3.Add(num);
        }
        foreach(int num in nums2){
            nums3.Add(num);
        }
        nums3.Sort();
        if(length%2==0){
            return (nums3[length/2]+nums3[length/2-1])/2f;
        }
        else{
            return nums3[length/2];
        }
    }
}
```
```
Runtime
77 ms
Beats
99.36%
Memory
52.6 MB
Beats
43.89%
```
[editorial](https://leetcode.com/problems/median-of-two-sorted-arrays/editorial)包含binary search及其优化版本解法。非常详细，无需我过多补充