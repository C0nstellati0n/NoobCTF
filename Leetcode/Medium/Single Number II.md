# Single Number II

[题目](https://leetcode.com/problems/single-number-ii/description/)

这题感觉我在这里记录没意义，solution区有很多讲的非常详细的，我把链接放在这里。

https://leetcode.com/problems/single-number-ii/solutions/43295/detailed-explanation-and-generalization-of-the-bitwise-operation-method-for-single-numbers/ （这篇有人翻译成中文了： https://blog.csdn.net/wlwh90/article/details/89712795 ）

https://leetcode.com/problems/single-number-ii/solutions/43294/challenge-me-thx/ （解析在评论区）

https://leetcode.com/problems/single-number-ii/solutions/43296/an-general-way-to-handle-all-this-sort-of-questions/ （解析同样在评论区）

bit manipulation不知道算不算个编程技巧，就算算的话也和其他的不一样。其他编程技巧讲究思想，位运算讲究观察和经验。这题还有个无脑的做法。
```c#
public class Solution {
    public int SingleNumber(int[] nums) 
    {
        Dictionary<int , int> records = new Dictionary<int , int>();
        for(int i = 0 ; i < nums.Length ;i++)
        {
            if(records.ContainsKey(nums[i]))
            {
                records[nums[i]]++;
            }
            else
            {
                records.Add(nums[i], 1);
            }
        }
        return  records.First(c=>c.Value == 1).Key;
    }
}
```
```
Runtime
83 ms
Beats
96.18%
Memory
39.8 MB
Beats
68.15%
```
我看到这题的第一个想法就是用字典记录。后来发现题目描述要求“You must implement a solution with a linear runtime complexity and use only constant extra space.”。我就寻思着c#字典查询没这么快吧，就没试。结果发现还真就这么快。