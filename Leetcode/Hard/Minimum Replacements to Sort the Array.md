# Minimum Replacements to Sort the Array

[题目](https://leetcode.com/problems/minimum-replacements-to-sort-the-array/description/)

坏消息：hard

好消息：有人说其实只有medium难度

坏消息：但是和数学密切相关

好消息：discussion区的Shubham_Raj22已经把数学部分写出来了

更好的消息：本人有史以来第一个没看答案写出来的hard题
```c#
//https://leetcode.com/problems/minimum-replacements-to-sort-the-array/editorial/ 有图+详细解释
public class Solution {
    public long MinimumReplacement(int[] nums) {
        if(nums.Length==1){
            return 0;
        }
        long splitCount=0;
        int steps=0;
        for(int i=nums.Length-2;i>=0;i--){
            if(nums[i]>nums[i+1]){
                steps=(nums[i]-1)/nums[i+1];
                nums[i]=nums[i]/(steps+1);
                splitCount+=steps;
            }
        }
        return splitCount;
    }
}
```
```
Runtime
167 ms
Beats
100%
Memory
48.9 MB
Beats
66.67%
```
首先要知道的一点是，倒着来而不是正着来。因为我们要将数字分成几半，肯定是越分越小的。我们又要让数组变成non-decreasing order，假如从第一个开始处理的话，完全不知道第一个该分成多小才能让后面的不递降。以及，最后一个数字无需分块。毕竟分块越分越小，最后一个数字肯定越大我们才更好处理。

最后的问题是咋分？你肯定不能统一把每个数字分成1，太多步骤了。根据nums[i+1]分？比如，假如nums[i]大于nums[i+1]的话，我们把nums[i]分出一个nums[i+1]，不断重复直到剩下的数字不比nums[i+1]大。看着好像行，但是有个问题，不停分出nums[i+1]的话剩下的部分肯定就很小了，根据我们刚才得到的规律：“最后一个数字肯定越大我们才更好处理”，这样好像也不行。所以最佳的办法是将nums[i]分成若干个相等的块，或者说editorial里的`(long)(nums[i] + nums[i + 1] - 1) / (long)nums[i + 1];`。需要分的次数就是这个数-1。

所以为什么Shubham_Raj22的`(nums[i]-1)/nums[i+1]`也行？这个的思路似乎就是尝试把(nums[i]-1)分成每块大小为nums[i+1]的块。他在评论区解释了。emmm，还是editorial好理解。