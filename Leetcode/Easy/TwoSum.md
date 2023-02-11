# Two Sum

[题目地址](https://leetcode.com/problems/two-sum/)

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.You may assume that each input would have exactly one solution, and you may not use the same element twice.You can return the answer in any order.给定nums数组和目标target，返回nums中相加得target的数字的索引。假设只有一对解，索引顺序不重要。

```c#
public class Solution {
    public int[] TwoSum(int[] nums, int target) {
        Dictionary<int,int> table=new(); //使用字典，空间换时间
        for(int i=0;i<nums.Length;i++){
            if(table.ContainsKey(target-nums[i])){
                return new int[2]{i,table[target-nums[i]]};
            }
            table.TryAdd(nums[i],i); //TryAdd防止键重复
        }
        return new int[2]{0,0};
    }
}
```