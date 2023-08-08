# Minimize the Maximum Difference of Pairs

[题目](https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/description/)

hint：这边我建议你用dp。dp很好，很厉害的，你看我都把dp之间的关系都告诉你了，为什么不写？

题目tag：greedy+binary search

discussion：为啥我的dp到最后MLE啊？

我：该binary search啥？emmm，我偷看一眼editorial不算抄吧？
```c#
//基本和 https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/editorial/ 一样
public class Solution {
    public int MinimizeMax(int[] nums, int p) {
        Array.Sort(nums);
        int start = 0;
        int end = nums[^1];
        while (start <= end) { //binary search找pair两个数之间的差值
            int mid = start + (end-start)/2;
            if (CountPairs(mid,nums)>=p){ //当这样的pair大于等于要求的数量，说明我们给的差值太高了，可以减小
                end=mid-1;
            }
            else{
                start=mid+1; //反之，说明差值太低了，需要调高一点
            }
            
        }
        return start;
    }
    public int CountPairs(int n,int[] nums){ //遍历一遍nums数组尝试找到差值小于等于n的pairs数量，我还以为会TLE
        int index=0;
        int count=0;
        while(index<nums.Length-1){
            if(nums[index+1]-nums[index]<=n){
                index++;
                count++;
            }
            index++;
        }
        return count;
    }
}
```
```
Runtime
178 ms
Beats
100%
Memory
57.3 MB
Beats
33.33%
```
关于为啥贪心可行： https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/solutions/3395952/in-case-you-are-wondering-why-greedy-works-for-this-problem/