# Monotonic Array

[题目](https://leetcode.com/problems/monotonic-array)

接近周末了却连续两道easy，我感觉大的要来了。
```c#
//总体思路是不要检查数组什么时候是Monotonic Array，而要默认它是，检查它什么时候不是
public class Solution {
    public bool IsMonotonic(int[] nums) {
        bool decreasing=true;
        bool increasing=true;
        for(int i=1;i<nums.Length;i++){
            if(nums[i]>nums[i-1]){
                decreasing=false;
            }
            else if(nums[i]<nums[i-1]){
                increasing=false;
            }
        }
        return decreasing||increasing;
    }
}
```
```
Runtime
216 ms
Beats
98.21%
Memory
61.5 MB
Beats
14.73%
```